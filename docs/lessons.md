# Lessons learned: making agent runs cheaper

Source: the first real run of `plan` + `build` on a production feature: two phases, ~10 agent tasks, two review rounds, two fix rounds.
Goal: get more work out of a **subscription**: fewer tokens and less usage-limit burn per feature. Dollar cost is not the metric.

## What we measured

- **Agent tokens:** ~1.5M across both phases, not counting the orchestrator session. Per task: ~60k to ~190k.
- **Rework:** the two fix rounds after review took ~19% of all agent tokens. The phase-2 fix (~185k) was the most expensive task of the run.
- **Plan estimates:** the dollar estimate was 3 to 5 times higher than the real cost. Dollars are the wrong unit for a subscription.
- **Orchestrator growth:** the orchestrator session grew the most. Every agent report lands in its context in full and is re-sent on every later turn.
- **Tests:** the full suite took 8 to 20 minutes and ran ~10 times (4 by agents, 6 by the orchestrator). With 4 agents running it at once, the machine ran out of memory.
- **Waiting is not free:** a running suite generates no tokens, but every wake-up to check on it re-sends the whole session context as cached input. For example, an agent with 100k of context that wakes up 3 extra times adds ~300k of cached input. The orchestrator received ~15 test-run notifications. Reading only the tail of the output is cheap. Overall, waiting costs less than rework or long reports, but it is not negligible, and it costs **time**.

## High impact

### 1. A real contract before parallel tasks
- **Problem:** the shared-data contract for a parallel group was **only column names**: no types, defaults or parsing rules. Four parallel tasks filled the gaps in four different ways (three different boolean interpretations for the same column). None of them tested against the real input, which was missing some columns. The fix round was the most expensive task of the run.
- **What forge does now:** `plan` adds a **contract task** before any parallel group that shares data. It delivers one normalization step at the input boundary (creates missing columns with defaults, coerces types once), shared read helpers, a **shared fixture that matches the real data's shape** (including its gaps), and a minimal integration test that every parallel task must keep green. Agent prompts say: "Do not write your own readers for contract fields; use the shared ones. If something is missing, stop and report." During `build`, the orchestrator runs a **light per-task review** before integrating: diff `--stat` plus a grep for new functions that duplicate shared helpers or read data outside the contract.

### 2. Short agent reports
- **Problem:** agent reports ran 40 to 80 lines, with tables, signature lists and long questions. All of it stays in the orchestrator context and is re-sent every turn.
- **What forge does now:** `build` enforces a fixed report of **at most 15 lines**: commit, files touched, tests (passed/failed), numbered one-line questions. Signatures and technical decisions go in the commit body, which the orchestrator reads only when it needs to.

### 3. Read symbols, not whole files
- **Problem:** several agents read whole large modules (~1,500 and ~600 lines), some more than once. A characterization-test task on Sonnet used ~180k tokens, mostly because it read the 1,500-line module in full. The plan gave approximate line numbers but no map.
- **What forge does now:** `plan` includes a **symbol map** per task: symbol, file, and why to read it. Agent prompts require locating code with a code-graph query or `grep -n`, then reading only those ranges with offset/limit. Whole files are read only when the task rewrites them.

### 4. Short agent prompts that point to the plan
- **Problem:** the orchestrator wrote long prompts that repeated the plan. That is orchestrator output (expensive), and the agent pays to read it too.
- **What forge does now:** in part. Prompts point to the task's section in `plan.md` and inherit the report format and reading rules above.
- **Still open:** a fixed prompt template in the skill (worktree reset, how to run tests, commit format, report format), so that each task prompt is ~10 lines: "Task T2.1 in `plan.md`, read its section; allowed files; tests; commit".

## Medium impact

### 5. Test only what you touch, with a golden as the safety net
- **Problem:** the new tests were worth writing (~100, almost all acceptance criteria). The waste was in **running too much and waiting**: full suites per agent and per integration.
- **What forge does now:** three test levels, and **no full suite per agent**:

| When | What runs | Approx. time |
|---|---|---|
| Each task (agent) | Only the tests for the modules it touches, from the plan's **module → tests map**. Foreground, short output (quiet mode, read only the tail) | seconds to a few minutes |
| Each integration (orchestrator) | The task's tests + the **golden test** of the existing flow | ~10 s + the task's tests |
| Phase gate, before the PR | **Full suite, once** | 8-20 min |

- The golden test runs the existing flow end to end and compares every output cell, so a shared change that breaks something shows up in seconds. Slow tests are marked (e.g. a `slow` marker) so they run only at the gate. `plan` avoids testing the same example in both a unit test and an integration test unless it says so explicitly.

### 6. A reusable golden harness
- **Problem:** the capture-and-compare script was written by hand in a scratch folder and lost when the session changed.
- **What forge does now:** `build` ships a generic golden template that each project fills in, and `plan` designs the characterization task to leave it versioned under the project's tests.

### 7. Business decisions that arrive late
- **Problem:** three business questions (tie-breaking, a tie tolerance band, an audit column) surfaced only in the phase-2 review. They reopened the spec and cost a fix round.
- **What forge does now:** `define`'s checklist asks, for every rule that changes a calculation: "What happens with ties, rounding and audit columns?". When mapping rules to code, `plan` lists the **code paths the rule does not mention** and asks about them before the plan is approved. Edge cases go into the plan as **acceptance criteria**, not as agent improvisation.

### 8. One session per milestone
- **Problem:** both phases ran in one session, plus an unrelated tooling detour. The orchestrator context ended up very large.
- **What forge does now:** every skill recommends a fresh session for the next one, and `progress.md` carries what is needed to resume.
- **Still open:** make the fresh session **mandatory after every phase gate**, and make sure `progress.md` records everything needed to resume, including how to regenerate the golden.

## Low impact

- **Model per task, by risk.** A small task with validations went to Haiku. It took longer, used more tool calls than any other task, and left two defects for a separate fix. What forge does now: `plan` assigns the model per task by risk and complexity, and does not use Haiku for code with validations. Sonnet is likely cheaper overall there.
- **Commit format errors** (subject and body on one line). What forge does now: two `-m` flags, a check with `git log`, and `--amend` only before push.
- **Branch naming.** What forge does now: `feature/<slug>-phase-N` everywhere (see `conventions.md`).
- **Estimate in tokens.** Still open: `plan` should estimate **tokens per phase** instead of dollars. Calibrate with this run: ~250-300k per phase of 4 tasks + review + fix.

## Open question: Opus on more tasks?

- **Hypothesis:** Opus solves tasks with fewer tokens (less exploration, fewer retries), so it could stretch a subscription further despite its higher per-token weight.
- **What the (thin) data shows:** Opus did not use fewer tokens per task (~90k to ~185k; Sonnet ~75k to ~180k). Opus did get things right on the first try more often: a large refactor needed no rework. Haiku had the worst tokens-to-quality ratio.
- **Caveat:** on a subscription, Opus usually counts faster against limits than Sonnet. Check `/usage` before deciding.
- **Proposed experiment:** per task, record tokens, tool calls, rework (yes/no) and % of limit used (`/usage` before and after). Compare two tasks of similar complexity, one on Opus and one on Sonnet. Decide with that data.

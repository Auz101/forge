# Development plan — <Feature name>

| Field | Value |
|---|---|
| Status | IN REVIEW · **APPROVED** · IN PROGRESS · DONE |
| Tech & AI Lead (role) | Claude (`plan`) |
| Functional definition | `spec.md` (status CLOSED, date) |
| Approved by / date | — |
| Maximum effort | medium |
| Main / integration / feature branch | `<main>` / `<integration or —>` / `feature/<slug>` |

## 1. Technical summary

_What is built, the chosen approach and why (discarded alternatives, one line each)._

## 2. Rule → implementation map

| Rule (spec.md) | File / function | New or existing | Task |
|---|---|---|---|
| R1 | … | … | T1.1 |

Living functional docs domains to update at close: …

## 3. Technical risks and mitigation

| Risk | Mitigation | Task |
|---|---|---|

## 4. Phases and tasks

### Phase N — <name> (branch `feature/<slug>-phase-N`)

Verifiable phase objective: …

| ID | Task | Rules | Files | Depends on | [P] | Agent | Model | Effort |
|---|---|---|---|---|---|---|---|---|
| TN.1 | … | R1, C3 | `path/file.py` | — | P | general-purpose | sonnet | medium |
| TN.R | Phase review | All in the phase | (read-only) | TN.* | — | general-purpose | opus | medium |

#### Detail TN.1
- **Objective:** …
- **Context to read:** `spec.md` (R1, Example N) and symbol map (read only those functions; full file only if the task rewrites it):

  | Symbol | Why |
  |---|---|
  | `path/file.py::function` | what to understand or modify |
- **Acceptance criteria:** … including edge cases (empty, nulls, missing columns, odd formats, defaults per mode).
- **Tests:** test file, cases, numeric examples to reproduce. **Module → tests map** the agent runs (only those of the modules it touches).
- **Commit:** `<exact message per the project's format>`

**Phase rollback:** how it is reverted (e.g. revert of the phase PR; affected data or schema and its prior backup). One or two lines.

**Phase gate:** what the user validates before continuing (results, tests, PR).

## 5. Cost estimate

Prices used: <model → USD per MTok input / output> · Source: <url/skill> · Date: <YYYY-MM-DD>

| Phase | Tasks | Model(s) | Input tokens (est.) | Output tokens (est.) | Expected cost | Range (opt. – pess.) |
|---|---|---|---|---|---|---|
| 1 | … | … | … | … | … | … |
| **Total** | | | | | **…** | **…** |

Assumptions: …

## 6. Git strategy

- Feature branch `feature/<slug>` (from the integration branch if any, else main); phases `feature/<slug>-phase-N`; worktree per parallel task.
- Commit format: …
- PR per phase → `feature/<slug>`: push, PR and merge by `build` after the gate (user approval). Final PR → integration branch or main (merge to main by the user).
- Conflicts: the executor stops and reports.

## 6B. Deployment and verification

- **Deployment order** and environments (dev → test → production), and who runs it (always with human approval).
- **Post-deployment verification:** smoke test, logs/alerts to check and success criterion.
- **Rollback:** when and how the deployment is reverted (and prior backup if data or schema is involved).

## 7. Human gates

| Moment | What is validated | Who |
|---|---|---|
| End of each phase | … | User |
| Final PR | … | User |

## 8. Change log

| Date | Change | Reason |
|---|---|---|

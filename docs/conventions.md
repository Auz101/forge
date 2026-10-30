# Conventions

Shared contract between the four forge skills. Every skill reads and writes artifacts that the others consume, so names, statuses and IDs below are **fixed** and always written exactly as shown, whatever the project's working language.

## Skills

| Order | Skill | Invocation | Role | Main artifact |
|---|---|---|---|---|
| 1 | `define` | `/forge:define` | Product Owner: WHAT and WHY, never HOW | `spec.md` |
| 2 | `plan` | `/forge:plan` | Tech & AI Lead: phases, tasks, agents, models, cost, branches, gates | `plan.md` |
| 3 | `build` | `/forge:build` | Orchestrator: executes the approved plan with agents, consolidates at close | `progress.md`, code, living functional docs |
| 4 | `verify` | `/forge:verify` | Senior QA: test case catalog, evidence, defects, exit verdict | `qa.md` |

Flow: `define → plan → build → verify`. Each skill recommends a fresh session for the next one; the artifacts carry the context.

### Meeting skills (independent flow)

| Order | Skill | Invocation | Role | Main artifact |
|---|---|---|---|---|
| 1 | `meeting-minutes` | `/forge:meeting-minutes` | Technical secretary: minutes from a transcript | `minutes.md`, `tasks.json` |
| 2 | `meeting-notion` | `/forge:meeting-notion` | Publishes minutes and syncs tasks in Notion | `log.md` |
| 3 | `meeting-jira` | `/forge:meeting-jira` | Creates and follows up epics and issues in Jira | `log.md`, `follow-up-<date>.md` |

They use their own user-level config (`~/.claude/forge/meetings.json`), not the project's `CLAUDE.md`, and never touch the forge work folder. `minutes.md` status values: `DRAFT` · `APPROVED`. Its IDs (`D#`, `A#`, `T#`, `P#`, `R#`) are scoped to the minutes and unrelated to the `spec.md` IDs below. See [meetings.md](meetings.md).

## Project configuration (lines in the project's `CLAUDE.md`)

| Line | Default when missing |
|---|---|
| `Working language: <language>` | Ask the user once, then propose adding the line |
| `Forge work folder: <path>` | `forge/` |
| `Functional docs folder: <path>` | `docs/functional/` |

### Working language

- Skill instructions and templates are in English. The **working language** of a project is what the skill uses to talk with the user and to write every artifact (`spec.md`, `plan.md`, `progress.md`, `qa.md`, living functional docs, commit bodies unless the project says otherwise).
- In Step 0, the skill looks for `Working language:` in `CLAUDE.md`. If missing, it asks once ("Which language will this repository work in?"), and proposes adding the line to `CLAUDE.md`; it writes the line only after the user approves. If `CLAUDE.md` does not exist, `define` creates it from its template (which includes the line).
- When writing artifacts in a language other than English, translate the template headings and prose. **Never translate**: file names, status values, IDs, and configuration line keys.

## Artifacts

Each feature lives in `<work folder>/<feature-slug>/`.

| File | Written by |
|---|---|
| `spec.md` | `define` (and `plan` only for approved changes) |
| `plan.md` | `plan` (status updated by `build`) |
| `progress.md` | `build` |
| `qa.md` | `verify` (`plan`/`build` only tick handoff items) |

Living functional docs: `<functional docs folder>/README.md` (domain index, glossary, overall flow) plus one file per domain. Only `build` writes them, at feature close. `define`, `plan` and `verify` read them as the source of truth for how the system works today.

## Status values (always in English)

| Artifact | Values |
|---|---|
| `spec.md` | `DRAFT` · `CLOSED` · `REOPENED BY PLAN` |
| `plan.md` | `IN REVIEW` · `APPROVED` · `IN PROGRESS` · `DONE` |
| Tasks in `progress.md` | `PENDING` · `IN PROGRESS` · `DONE` · `FAILED` · `BLOCKED` |
| `qa.md` | `DESIGNING` · `CASES APPROVED` · `VALIDATING` · `CLOSED` |
| QA verdict | `PASS` · `PASS WITH OBSERVATIONS` · `FAIL` |
| Handoff items in `qa.md` | `Pending` · `Planned (T<x>.<n>)` · `Done (<hash>)` · `Verified by QA` |
| QA case result | `PENDING` · `PASS` · `FAIL` · `BLOCKED` · `NOT RUN` |
| Defect severity | `Blocker` · `Major` · `Minor` · `Cosmetic` |
| Defect origin | `Code` · `Spec` · `Plan` · `Test` · `Data` |
| Unconfirmed default in `spec.md` | `PROPOSAL` |

## IDs (never translated, never reused)

| ID | Meaning | Defined in |
|---|---|---|
| `R#` | Business rule | `spec.md` |
| `C#` | Edge case | `spec.md` |
| `E#` | Input | `spec.md` |
| `S#` | Output | `spec.md` |
| `N#` | Notification | `spec.md` |
| `D#` | Difference vs. current behavior | `spec.md` |
| `P#` | Open question | `spec.md` |
| `X#` | Out of scope | `spec.md` |
| `T<phase>.<n>` | Task | `plan.md` |
| `QA#` | Test case | `qa.md` |
| `DEF#` | Defect | `qa.md` |
| `PQ#` | QA question | `qa.md` |
| `OBS#` | QA observation (accepted risk, not a defect) | `qa.md` |

In living functional docs, rule IDs get a short domain prefix and keep their origin for traceability: `PAY-R3` with `origin: volume-discount R3`. A new spec that changes a current rule references it explicitly: `replaces PAY-R3`.

## Branches and commits (defaults; the project's `CLAUDE.md` wins)

- Branches: `<main>` ← (optional integration branch, e.g. `develop`) ← `feature/<slug>` ← `feature/<slug>-phase-N`.
- Automatic commits only while `build` executes an approved plan, only on feature branches, never on the main branch.
- Push, PR and merge always need human approval. The merge to the main branch is done by the user.
- Commit message format and co-author lines follow the project's `CLAUDE.md`; if it says nothing, use `<area> - <summary>` plus a body.

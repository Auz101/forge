# QA — <Feature name>

| Field | Value |
|---|---|
| Status | **DESIGNING** · CASES APPROVED · VALIDATING · CLOSED |
| Verdict | — · PASS · PASS WITH OBSERVATIONS · FAIL |
| Senior QA (role) | Claude (`verify`) |
| Mode | Final · Early · Re-test |
| Functional spec | `spec.md` (status CLOSED, date) |
| Plan | `plan.md` (status, date) |
| Branch / validated commit | `feature/<slug>` @ `<hash>` |
| Catalog approved by / date | — |
| Verdict decided by / date | — |

**Resume point:** `<round> · <last QA# recorded> · <next action>`

## 1. QA scope

- **What is validated:** …
- **What is not validated and why:** … (out of scope in `spec.md`, requires production, etc.)
- **Environment and data:** local / test; origin of the test data (fixture, anonymized sample data, generated).

## 2. Risks

| Area / rule | Impact | Likelihood | Level | Reason (diff, progress.md, coverage) |
|---|---|---|---|---|
| R1 | High | Medium | Critical | … |

## 3. Traceability matrix

| spec.md ID | Cases | Coverage status |
|---|---|---|
| R1 | QA1, QA2 | Covered · Gap: <reason> |

## 4. Case catalog

| ID | Case | Rules | Type | Technique | Priority | Method | Automate | Result |
|---|---|---|---|---|---|---|---|---|
| QA1 | … | R1 | Functional positive | End-to-end example | Critical | Script | Yes: no automated test | PENDING · PASS · FAIL · BLOCKED · NOT RUN |

### QA1 detail
- **Preconditions and data:** …
- **Steps:** …
- **Expected result:** … _(source: `spec.md` → R1 / Example N)_
- **Evidence:** script / test / command and summarized output.
- **Actual:** …

## 5. Manual cases (for the user)

| ID | Steps | Expected | Reported result |
|---|---|---|---|

## 6. QA questions

| ID | Question | Rules | Blocking | Status / answer | Routed to |
|---|---|---|---|---|---|
| PQ1 | … | R1 | Yes/No | Open · Resolved: … | define · plan · — |

## 7. Defects

| ID | Severity | Case / rules | Expected vs. actual | Probable location | Origin | Status | Fixed in |
|---|---|---|---|---|---|---|---|
| DEF1 | Blocker · Major · Minor · Cosmetic | QA1 / R1 | … | `file::function` | Code · Spec · Plan | Open · Fixed · Risk accepted | `<hash>` |

### DEF1 reproduction
- Steps, data and script (scratchpad path): …

## 8. Test suite observations

| ID | Test | Finding | Affected case | Action |
|---|---|---|---|---|
| OBS1 | `tests/…::test_…` | Trivial assertion / mock hides the logic / expected copied from code / skip | QA3 | Validated by script |

## 9. Handoff to plan

_The only input `plan` reads to plan the QA correction phase (or, in early mode, the acceptance criteria). Round: <N>._

| ID | Type | What is requested | Expected (source in `spec.md`) | Suggested task | Status |
|---|---|---|---|---|---|
| DEF1 | Fix defect | … | … (R1 / Example N) | — | Pending · Planned (T<x>.<n>) · Done (`<hash>`) · Verified by QA |
| QA1 | Automate case | Permanent test in `tests/…` | … (R1 / Example N) | — | … |
| QA4 | Acceptance criterion (early) | … | … | T2.1 | … |

## 10. Rounds

### Round 1 — <YYYY-MM-DD> · commit `<hash>`

| Priority | Total | PASS | FAIL | BLOCKED | NOT RUN |
|---|---|---|---|---|---|
| Critical | | | | | |
| High | | | | | |
| Medium | | | | | |
| Low | | | | | |

- **Full suite:** N/M · **Golden:** no differences / differences: …
- **Open defects:** Blockers N · Majors N · Minors N · Cosmetic N
- **Residual risks:** …
- **Actual vs. estimated cost:** …
- **Proposed verdict:** … — **User decision:** … (accepted risks and by whom)

## 11. Change log

| Date | Change | Reason |
|---|---|---|

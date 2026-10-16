# Functional specification — <Feature name>

| Field | Value |
|---|---|
| Status | **DRAFT** · CLOSED · REOPENED BY PLAN |
| Product Owner (role) | Claude (`define`) |
| Requester | <user> |
| Repository | <path or "greenfield"> |
| Created | <YYYY-MM-DD> |
| Last updated | <YYYY-MM-DD> |
| Closed by / date | — |

## 1. Goal and scope

- **Business problem:** …
- **Goal:** …
- **Users / who runs it:** …
- **Trigger and frequency:** …

### Out of scope
- `X1` …

## 2. Current system context

_Only what is relevant: what exists today, what is reused, what changes. If greenfield: "Not applicable"._

### Differences vs. current behavior

| ID | Item | Today | New |
|---|---|---|---|
| D1 | … | … | … |

## 3. Inputs

| ID | Input | Source | Format | Key columns / fields | If missing or empty |
|---|---|---|---|---|---|
| E1 | … | … | … | … | … |

## 4. Business rules and calculations

| ID | Rule | Formula / condition | Units and rounding | Status |
|---|---|---|---|---|
| R1 | … | … | … | Confirmed · PROPOSAL |

### End-to-end examples

_At least one numeric example per non-trivial calculation, validated by the user._

## 5. Edge cases

| ID | Case | Expected behavior |
|---|---|---|
| C1 | … | … |

## 6. Outputs

| ID | Output | Destination | Format / name | Columns | Consumer |
|---|---|---|---|---|---|
| S1 | … | … | … | … | … |

## 7. Notifications

| ID | Event | Recipients | Content |
|---|---|---|---|
| N1 | Success | … | … |
| N2 | Failure | … | … |

## 8. Non-functional constraints

_Platform, maximum times, volume, concurrency, security, regulation._

## 9. Open questions

| ID | Question | Block | Blocking | Status / answer |
|---|---|---|---|---|
| P1 | … | … | Yes/No | Open · DEFERRED · Resolved: … |

## 10. Decision log

| Date | ID | Decision or change | Reason |
|---|---|---|---|
| … | … | … | … |

## 11. Completeness checklist

- [ ] Every calculation rule has formula, units and rounding.
- [ ] Every rule that changes a calculation or allocation states what happens to what depends on it (tie-breakers, balancing, priorities, defaults, audit columns).
- [ ] Every input has source, format, columns and behavior if missing.
- [ ] Every output has destination, format, name and columns.
- [ ] Edge cases: empty, null/zero, duplicates, external failures, concurrent runs.
- [ ] Success and failure notifications defined.
- [ ] Out of scope explicit.
- [ ] No blocking open questions (DEFERRED ones reviewed by the user).
- [ ] End-to-end numeric example validated for each non-trivial calculation.

## 12. Summary for the Tech & AI Lead

_Filled in at close: what gets built, what is reused, what changes, functional risks, confirmed assumptions._

# QA — Volume discount

| Field | Value |
|---|---|
| Status | **CLOSED** |
| Verdict | **PASS WITH OBSERVATIONS** |
| Senior QA (role) | Claude (`verify`) |
| Mode | Re-test (round 2 of 2) |
| Functional spec | `spec.md` (status CLOSED, 2026-09-23) |
| Plan | `plan.md` (status IN PROGRESS, 2026-09-30) |
| Branch / validated commit | `feature/volume-discount` @ `6c3f1aa` |
| Catalog approved by / date | Store owner / 2026-09-29 |
| Verdict decided by / date | Store owner / 2026-10-01 |

**Resume point:** `Round 2 · QA8 · closed; next: final PR in /forge:build`

## 1. QA scope

- **What is validated:** R1–R5, C1–C4, E1–E3, S1–S2, N1, and regression of the current payments rules touched by the diff (`PAY-R1`, `PAY-R3`).
- **What is not validated and why:** X1–X3 (out of scope); real delivery through the production mail relay (requires production, see OBS1).
- **Environment and data:** local, `feature/volume-discount`; generated carts from the spec examples; dev mail sink for N1.

## 2. Risks

| Area / rule | Impact | Likelihood | Level | Reason (diff, progress.md, coverage) |
|---|---|---|---|---|
| R3 rounding | High | Medium | Critical | Money; new code computes a percentage outside `money.py` |
| R4 / `PAY-R2` replacement | High | Medium | Critical | Shared `apply_discounts` changed; T1.2 needed a retry |
| R2 exclusions | Medium | Low | High | Simple filter, but a mistake gives discounts on gift cards |
| N1 / C4 | Medium | Low | Medium | Post-commit hook; existing test mocks the mailer |

## 3. Traceability matrix

| spec.md ID | Cases | Coverage status |
|---|---|---|
| R1 | QA1, QA2, QA4 | Covered |
| R2 | QA1, QA5 | Covered |
| R3 | QA1, QA2, QA3 | Covered |
| R4 | QA1, QA6 | Covered |
| R5 | QA1, QA2, QA6 | Covered |
| C1 | QA4 | Covered |
| C2 | QA5 | Covered |
| C3 | QA6 | Covered |
| C4 | QA7 | Covered (mocked mailer, OBS1) |
| E1, E2, E3 | QA1, QA6, QA7 | Covered |
| S1, S2 | QA1, QA2 | Covered |
| N1 | QA2, QA7 | Covered |
| `PAY-R1` (regression) | QA3, QA8 | Covered |
| `PAY-R3` (regression) | QA5 | Covered |

## 4. Case catalog

| ID | Case | Rules | Type | Technique | Priority | Method | Automate | Result |
|---|---|---|---|---|---|---|---|---|
| QA1 | Example 1: 27 notebooks + 1 gift card, coupon `SPRING8` | R1–R5, S1, S2 | Functional positive | End-to-end example | Critical | Existing test + script | No | PASS |
| QA2 | Example 2: 52 units, top tier, manager email | R1, R3, R5, N1 | Functional positive | End-to-end example | Critical | Existing test + script | No | PASS |
| QA3 | Half-cent base: 10 × $2.97 at 5% | R3, `PAY-R1` | Functional positive | Boundary value | Critical | Script | Yes: found DEF1 | PASS (round 2) |
| QA4 | Q = 9, 10, 24, 25, 49, 50 | R1, C1 | Functional positive | Boundary values | High | Existing test | No | PASS |
| QA5 | 8 notebooks + 5 gift cards | R2, C2, `PAY-R3` | Functional negative | Equivalence class | High | Script | No | PASS |
| QA6 | Tie: coupon $10.00 vs. volume 5% of $200.00 | R4, R5, C3 | Functional positive | Decision table | Critical | Existing test | No | PASS |
| QA7 | Mailer raises / `STORE_MANAGER_EMAIL` unset | N1, C4, E3 | Functional negative | Fault injection | Medium | Existing test + inspection | No | PASS |
| QA8 | Regression: 9 × $3.33 with 15% coupon, no tier | `PAY-R1` | Regression | Golden scenario | High | Golden + script | No | PASS |

### QA1 detail
- **Preconditions and data:** cart from spec Example 1; coupon `SPRING8` (fixed $8.00).
- **Steps:** price the cart, confirm the order, read invoice lines and `order_adjustments`.
- **Expected result:** Q = 27, 10%, volume 1,077 > coupon 800; invoice subtotal $127.73, "Volume discount (10%)" −$10.77, total $116.96; one row `type="volume"`, `percent=10`, `amount_cents=1077` _(source: `spec.md` → Example 1)_
- **Evidence:** `test_invoice.py::test_example_1_total` + scratchpad script `qa_examples.py`.
- **Actual:** as expected.

### QA2 detail
- **Expected result:** Q = 52, 15%, discount 4,108 cents, total $232.80, one email "Top-tier order <id>" in the dev mail sink _(source: `spec.md` → Example 2, N1)_
- **Actual:** as expected.

### QA3 detail
- **Preconditions and data:** 10 × $2.97 (`stationery`), no coupon. Base 2,970 cents, Q = 10 → 5%.
- **Expected result:** 2,970 × 5% = 148.5 → **149 cents** (half up) _(source: `spec.md` → R3; living docs `PAY-R1`)_
- **Evidence:** scratchpad script `qa_rounding.py`.
- **Actual:** round 1: 148 (FAIL, DEF1). Round 2 @ `6c3f1aa`: 149 (PASS); now also `test_volume_discount.py::test_half_cent_rounds_up`.

### QA6 detail
- **Preconditions and data:** 20 × $10.00, Q = 20 → 5% of 20,000 = 1,000 cents; coupon fixed $10.00 = 1,000 cents.
- **Expected result:** coupon applied, coupon line −$10.00, no volume line, total $190.00 _(source: `spec.md` → R4, C3, decision 2026-09-22)_
- **Actual:** as expected.

### QA8 detail
- **Preconditions and data:** 9 × $3.33 = 2,997 cents; percentage coupon 15%.
- **Expected result:** Q = 9 → no tier; coupon 2,997 × 15% = 449.55 → 450 cents; total 2,547 cents ($25.47), identical to the pre-feature golden _(source: living docs `PAY-R1`)_
- **Actual:** as expected in both rounds; golden: no differences.

## 5. Manual cases (for the user)

| ID | Steps | Expected | Reported result |
|---|---|---|---|
| — | None: N1 checked in the dev mail sink by script (QA2) | — | — |

## 6. QA questions

| ID | Question | Rules | Blocking | Status / answer | Routed to |
|---|---|---|---|---|---|
| — | None raised | — | — | — | — |

## 7. Defects

| ID | Severity | Case / rules | Expected vs. actual | Probable location | Origin | Status | Fixed in |
|---|---|---|---|---|---|---|---|
| DEF1 | Major | QA3 / R3, `PAY-R1` | 149 vs. 148 cents: banker's rounding at exactly half a cent | `checkout/discounts/volume.py::volume_discount` (uses `round()` instead of `money.percent_of`) | Code | Fixed | `4a8d3b6` |

### DEF1 reproduction
- `python -I qa_rounding.py` (scratchpad): builds the QA3 cart, calls `volume_discount`, prints 148. Any base whose 5/10/15% ends in exactly .5 cents with an even integer part rounds down.

## 8. Test suite observations

| ID | Test | Finding | Affected case | Action |
|---|---|---|---|---|
| OBS1 | `tests/checkout/test_notifications.py::test_mailer_error_does_not_block` | Mailer is mocked; delivery through the production relay is not exercised locally | QA7 | Code inspected (exception caught, warning with order id). Risk accepted by the store owner; checked in the post-deploy smoke (plan 6B) |

## 9. Handoff to plan

_Round: 1._

| ID | Type | What is requested | Expected (source in `spec.md`) | Suggested task | Status |
|---|---|---|---|---|---|
| DEF1 | Fix defect | Use `money.percent_of` in `volume_discount` | 10 × $2.97 at 5% → 149 cents (R3, `PAY-R1`) | — | Verified by QA |
| QA3 | Automate case | Permanent test `tests/checkout/test_volume_discount.py::test_half_cent_rounds_up` | 149 cents (R3) | — | Verified by QA |

## 10. Rounds

### Round 1 — 2026-09-29 · commit `b5d2e80`

| Priority | Total | PASS | FAIL | BLOCKED | NOT RUN |
|---|---|---|---|---|---|
| Critical | 4 | 3 | 1 | 0 | 0 |
| High | 3 | 3 | 0 | 0 | 0 |
| Medium | 1 | 1 | 0 | 0 | 0 |
| Low | 0 | 0 | 0 | 0 | 0 |

- **Full suite:** 153/153 · **Golden:** no differences.
- **Open defects:** Blockers 0 · Majors 1 · Minors 0 · Cosmetic 0
- **Residual risks:** money off by one cent on half-cent bases (DEF1).
- **Actual vs. estimated cost:** $1.35 vs. $1.20.
- **Proposed verdict:** FAIL — **User decision:** FAIL; route DEF1 and QA3 to `/forge:plan` (QA correction phase).

### Round 2 — 2026-10-01 · commit `6c3f1aa`

Re-run: QA3 and related regression for `volume.py` (QA1, QA2, QA4, QA8).

| Priority | Total | PASS | FAIL | BLOCKED | NOT RUN |
|---|---|---|---|---|---|
| Critical | 4 | 4 | 0 | 0 | 0 |
| High | 3 | 3 | 0 | 0 | 0 |
| Medium | 1 | 1 | 0 | 0 | 0 |
| Low | 0 | 0 | 0 | 0 | 0 |

- **Full suite:** 154/154 · **Golden:** no differences.
- **Open defects:** Blockers 0 · Majors 0 · Minors 0 · Cosmetic 0
- **Residual risks:** OBS1 (production mail relay not exercised).
- **Actual vs. estimated cost:** $0.48 vs. $0.50.
- **Proposed verdict:** PASS WITH OBSERVATIONS — **User decision:** accepted by the store owner; OBS1 checked after deploy.

## 11. Change log

| Date | Change | Reason |
|---|---|---|
| 2026-09-29 | Catalog approved; round 1 FAIL | DEF1 |
| 2026-10-01 | Round 2; status CLOSED, PASS WITH OBSERVATIONS | DEF1 verified, test for QA3 reviewed (expected value from the case) |

# Development plan — Volume discount

| Field | Value |
|---|---|
| Status | **DONE** |
| Tech & AI Lead (role) | Claude (`plan`) |
| Functional definition | `spec.md` (status CLOSED, 2026-09-23) |
| Approved by / date | Store owner / 2026-09-24 |
| Maximum effort | medium |
| Main / integration / feature branch | `main` / — / `feature/volume-discount` |

## 1. Technical summary

A new pure module `checkout/discounts/volume.py` computes eligible quantity, base and volume amount (R1–R3). `checkout/pricing.py::apply_discounts` compares it with the coupon amount and keeps one adjustment (R4), replacing the single-coupon guard of `PAY-R2`. The invoice renders the new adjustment type (R5) and a post-commit hook emails the manager on the top tier (N1, C4).

Discarded: per-line discount (rejected in spec P1); tiers in a DB table (out of scope X1, adds a migration for no gain today).

## 2. Rule → implementation map

| Rule (spec.md) | File / function | New or existing | Task |
|---|---|---|---|
| R1, C1 | `checkout/discounts/volume.py::tier_percent` | New | T1.1 |
| R2, C2 | `checkout/discounts/volume.py::eligible_lines`, `EXCLUDED_CATEGORIES` | New | T1.1 |
| R3 | `checkout/discounts/volume.py::volume_discount` using `checkout/money.py::percent_of` (`PAY-R1`) | New / existing | T1.1 |
| R4, C3 (replaces `PAY-R2`) | `checkout/pricing.py::apply_discounts`; remove `_single_coupon_guard` | Existing | T1.2 |
| R5, S1, S2 | `checkout/invoice.py::build_invoice_lines`; `order_adjustments` row `type="volume"` | Existing | T2.1 |
| N1, C4, E3 | `checkout/notifications.py::notify_top_tier`, `checkout/templates/top_tier_email.txt` | New | T2.2 |

Living functional docs domains to update at close: **payments**.

## 3. Technical risks and mitigation

| Risk | Mitigation | Task |
|---|---|---|
| Banker's rounding (`round()`) instead of half up | Mandatory reuse of `money.percent_of`; test with a half-cent base | T1.1 |
| Old `PAY-R2` test still asserting "coupon only" | Remove `test_coupon_is_only_discount` and the guard in the same commit | T1.2 |
| Email blocking checkout | Send after commit, catch and log every mailer error | T2.2 |

## 4. Phases and tasks

### Phase 1 — Discount calculation (branch `feature/volume-discount-phase-1`)

Verifiable phase objective: `apply_discounts` returns the right adjustment for spec Examples 1 and 2 and for C1–C3.

| ID | Task | Rules | Files | Depends on | [P] | Agent | Model | Effort |
|---|---|---|---|---|---|---|---|---|
| T1.1 | Volume tier module | R1, R2, R3, C1, C2 | `checkout/discounts/volume.py`, `tests/checkout/test_volume_discount.py` | — | — | general-purpose | sonnet | medium |
| T1.2 | Coupon vs. volume resolution | R4, C3 | `checkout/pricing.py`, `tests/checkout/test_pricing.py` | T1.1 | — | general-purpose | opus | medium |
| T1.R | Phase review | All in the phase | (read-only) | T1.* | — | general-purpose | opus | medium |

#### Detail T1.1
- **Objective:** pure functions for Q, base and volume amount.
- **Context to read:** `spec.md` (R1–R3, C1, C2, Examples 1–2) and:

  | Symbol | Why |
  |---|---|
  | `checkout/money.py::percent_of` | Half-up cent rounding to reuse (`PAY-R1`) |
  | `checkout/cart.py::CartLine` | Line fields |
- **Acceptance criteria:** thresholds are ≥; `gift_card` lines ignored for Q and base; empty cart → 0; amount uses `percent_of`, never `round()`.
- **Tests:** `tests/checkout/test_volume_discount.py`: Examples 1 and 2 (1,077 and 4,108 cents), Q = 9/10/24/25/49/50, C2. Module → tests: `volume.py` → `test_volume_discount.py`.
- **Commit:** `checkout - Volume tier calculation` + body with rules covered.

#### Detail T1.2
- **Objective:** one discount per order, the higher one; tie → coupon.
- **Context to read:** `spec.md` (R4, C3) and:

  | Symbol | Why |
  |---|---|
  | `checkout/pricing.py::apply_discounts` | Function to change |
  | `checkout/pricing.py::_single_coupon_guard` | `PAY-R2` code to remove |
  | `checkout/coupons.py::coupon_amount` | Coupon amount (already excludes gift cards, `PAY-R3`) |
- **Acceptance criteria:** Example 1 → volume 1,077 beats coupon 800; tie 1,000 vs 1,000 → coupon; no coupon → volume; neither → no adjustment. `_single_coupon_guard` and `test_coupon_is_only_discount` removed.
- **Tests:** `tests/checkout/test_pricing.py`. Module → tests: `pricing.py` → `test_pricing.py`, `test_volume_discount.py`.
- **Commit:** `checkout - Coupon and volume discount resolution` + body mentioning `replaces PAY-R2`.

**Phase rollback:** revert of the phase PR; no data or schema involved.

**Phase gate:** user reviews Examples 1–2 in the tests and the removal of the `PAY-R2` guard.

### Phase 2 — Invoice and notification (branch `feature/volume-discount-phase-2`)

Verifiable phase objective: a confirmed order shows the discount line, stores the `order_adjustments` row, and top-tier orders email the manager without blocking.

| ID | Task | Rules | Files | Depends on | [P] | Agent | Model | Effort |
|---|---|---|---|---|---|---|---|---|
| T2.1 | Invoice discount line | R5, S1, S2 | `checkout/invoice.py`, `tests/checkout/test_invoice.py` | Phase 1 | P | general-purpose | sonnet | medium |
| T2.2 | Top-tier manager email | N1, C4, E3 | `checkout/notifications.py`, `checkout/templates/top_tier_email.txt`, `tests/checkout/test_notifications.py` | Phase 1 | P | general-purpose | haiku | medium |
| T2.R | Phase review | All in the phase | (read-only) | T2.* | — | general-purpose | opus | medium |

#### Detail T2.1
- **Objective:** render "Volume discount (N%)" and persist the adjustment.
- **Context to read:** `spec.md` (R5, S1, S2) and `checkout/invoice.py::build_invoice_lines`, `checkout/orders.py::save_adjustments`.
- **Acceptance criteria:** Example 1 invoice total $116.96, Example 2 $232.80; coupon-wins invoice unchanged from today.
- **Tests:** `tests/checkout/test_invoice.py`. Module → tests: `invoice.py` → `test_invoice.py`.
- **Commit:** `checkout - Volume discount invoice line`.

#### Detail T2.2
- **Objective:** post-commit email when the applied adjustment is volume at 15%.
- **Context to read:** `spec.md` (N1, C4, E3) and `checkout/mailer.py::send`, `checkout/orders.py::on_order_committed`.
- **Acceptance criteria:** sent only for applied 15% volume; missing `STORE_MANAGER_EMAIL` or mailer error → warning with order id, order confirmed.
- **Tests:** `tests/checkout/test_notifications.py`. Module → tests: `notifications.py` → `test_notifications.py`.
- **Commit:** `checkout - Top-tier order email to store manager`.

**Phase rollback:** revert of the phase PR; no data or schema involved.

**Phase gate:** user places Example 2 in a local run and checks invoice and email (captured by the dev mail sink).

### Phase 3 — QA correction round 1 (branch `feature/volume-discount-phase-3`)

_Added 2026-09-30 from the *Handoff to plan* in `qa.md` (round 1). Phases 1 and 2 untouched._

Verifiable phase objective: half-cent bases round half up; QA3 is a permanent test.

| ID | Task | Rules | Files | Depends on | [P] | Agent | Model | Effort |
|---|---|---|---|---|---|---|---|---|
| T3.1 | Fix DEF1 and automate QA3 | R3, `PAY-R1` | `checkout/discounts/volume.py`, `tests/checkout/test_volume_discount.py` | — | — | general-purpose | sonnet | medium |

#### Detail T3.1
- **Objective:** `volume_discount` uses `money.percent_of`; add the QA3 test.
- **Acceptance criteria:** 10 × $2.97 at 5% → 149 cents (expected value from `qa.md` QA3, never from the code).
- **Tests:** `tests/checkout/test_volume_discount.py`.
- **Commit:** `checkout - Half-up rounding for volume discount`.

**Phase rollback:** revert of the phase PR. **Phase gate:** user reviews the fix and the new test; QA re-test follows.

## 5. Cost estimate

Prices used (illustrative prices; plan checks current pricing): opus $5 / $25 · sonnet $3 / $15 · haiku $1 / $5 per MTok input / output · Source: provider pricing page · Date: 2026-09-24

| Phase | Tasks | Model(s) | Input tokens (est.) | Output tokens (est.) | Expected cost | Range (opt. – pess.) |
|---|---|---|---|---|---|---|
| 1 | T1.1, T1.2, T1.R | sonnet, opus | 550k | 65k | $3.77 | $2.80 – $5.60 |
| 2 | T2.1, T2.2, T2.R | sonnet, haiku, opus | 380k | 43k | $1.72 | $1.30 – $2.60 |
| 3 | T3.1 (added 2026-09-30) | sonnet | 160k | 18k | $0.75 | $0.55 – $1.10 |
| **Total** | | | **1,090k** | **126k** | **$6.24** | **$4.65 – $9.30** |

Assumptions: agent cost only (the orchestrator session is not included); symbol-based reading; one retry budgeted in the pessimistic range.

## 6. Git strategy

- Feature branch `feature/volume-discount` from `main`; phases `feature/volume-discount-phase-N`; worktree per parallel task (T2.1, T2.2).
- Commit format: `<area> - <summary>` plus a body (project `CLAUDE.md`).
- PR per phase → `feature/volume-discount`: push, PR and merge by `build` after the gate. Final PR → `main` (merge by the user).
- Conflicts: the executor stops and reports.

## 6B. Deployment and verification

- **Deployment order:** staging → production, run by the user.
- **Post-deployment verification:** in staging, place Example 2; check invoice line, `order_adjustments` row and the manager email. In production, watch checkout error rate for 24 h.
- **Rollback:** revert the final PR and redeploy; no data or schema to restore.

## 7. Human gates

| Moment | What is validated | Who |
|---|---|---|
| End of each phase | Tests, examples, real vs. estimated cost, PR | User |
| Final PR | QA verdict, updated `docs/functional/payments.md`, closing commit | User |

## 8. Change log

| Date | Change | Reason |
|---|---|---|
| 2026-09-24 | Plan approved | — |
| 2026-09-30 | Added Phase 3 — QA correction round 1 (T3.1) | `qa.md` handoff: DEF1 and QA3 |
| 2026-10-02 | Status DONE | Closing commit |

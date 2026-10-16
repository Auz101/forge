# Functional specification — Volume discount

| Field | Value |
|---|---|
| Status | **CLOSED** |
| Product Owner (role) | Claude (`define`) |
| Requester | Store owner |
| Repository | `shop-service` (Python 3.11, `checkout/` module) |
| Created | 2026-09-21 |
| Last updated | 2026-09-23 |
| Closed by / date | Store owner / 2026-09-23 |

## 1. Goal and scope

- **Business problem:** wholesale-style customers (offices, schools) buy stationery in bulk but get the same price as a one-unit buyer, so they split orders or go to competitors.
- **Goal:** reward large carts with an automatic, tiered discount and alert the store manager about the biggest orders so stock can be checked the same day.
- **Users / who runs it:** any customer at checkout; the store manager receives the alert.
- **Trigger and frequency:** every checkout price calculation (cart view, order confirmation). About 300 orders per day; under 5% expected to reach a tier.

### Out of scope
- `X1` Editing tiers from the admin panel (tiers are fixed in this version).
- `X2` Different tiers per category or per product.
- `X3` Applying the discount to orders placed before release.

## 2. Current system context

Living docs: `docs/functional/payments.md`. Relevant current rules:
- `PAY-R1` amounts are integer cents; every percentage is rounded half up to the cent. **Kept.**
- `PAY-R2` a coupon code is the only discount an order can carry (one coupon per order). **Replaced by R4.**
- `PAY-R3` gift-card lines never receive a coupon discount. **Kept**; R2 applies the same exclusion to the volume discount.

Reused: coupon validation and coupon amount (`checkout/coupons.py`), the mailer used for order emails, the existing `order_adjustments` table.

### Differences vs. current behavior

| ID | Item | Today | New |
|---|---|---|---|
| D1 | Discounts on an order | Coupon only (`PAY-R2`) | Volume discount or coupon, whichever is higher (R4) |
| D2 | Invoice | Coupon line when a coupon applies | Also a "Volume discount (N%)" line when the volume discount applies (R5) |
| D3 | Manager alerts | None per order | Email when an order gets the top tier (N1) |

## 3. Inputs

| ID | Input | Source | Format | Key columns / fields | If missing or empty |
|---|---|---|---|---|---|
| E1 | Cart lines | Checkout session | List of lines | `sku`, `category`, `unit_price_cents`, `quantity` | Empty cart: no discount, existing empty-cart behavior |
| E2 | Coupon code | Customer at checkout (optional) | String, validated by the coupon module | `code` → coupon amount in cents | No coupon: only the volume discount is evaluated |
| E3 | Store manager address | Service configuration | Env var name `STORE_MANAGER_EMAIL` | — | Not set: no email, warning logged, order unaffected |

## 4. Business rules and calculations

| ID | Rule | Formula / condition | Units and rounding | Status |
|---|---|---|---|---|
| R1 | The tier depends on the eligible quantity Q of the cart | Q ≥ 50 → 15% · Q ≥ 25 → 10% · Q ≥ 10 → 5% · otherwise 0% | Q in units | Confirmed |
| R2 | Lines in excluded categories (`gift_card`) do not count toward Q and are not part of the discount base | Q = Σ quantity of eligible lines · Base = Σ (unit_price_cents × quantity) of eligible lines | Cents | Confirmed |
| R3 | The volume discount is computed once on the whole base, not per line | Discount = Base × tier% | Rounded half up to the cent (`PAY-R1`) | Confirmed (was PROPOSAL, see P1) |
| R4 | Volume discount and coupon are never combined: the higher amount is applied; on a tie, the coupon. **Replaces `PAY-R2`** | Applied = max(volume, coupon), tie → coupon | Cents | Confirmed |
| R5 | When the volume discount is applied, the invoice shows one negative line "Volume discount (N%)" after the subtotal; when the coupon wins, only the coupon line appears, as today | — | Cents, shown as `$X.XX` | Confirmed |

### End-to-end examples

**Example 1 — mid tier, coupon loses, gift card excluded (validated by the requester)**

| Line | Category | Qty | Unit | Line total |
|---|---|---|---|---|
| Notebook A5 | stationery | 27 | $3.99 | $107.73 |
| Gift card | gift_card | 1 | $20.00 | $20.00 |

- Q = 27 → 10% (R1, R2). Base = 10,773 cents.
- Volume = 10,773 × 10% = 1,077.3 → **1,077 cents** (R3).
- Coupon `SPRING8` (fixed $8.00) = 800 cents → volume wins (R4).
- Invoice: subtotal $127.73 · Volume discount (10%) −$10.77 · **total $116.96** (R5).

**Example 2 — top tier and manager email (validated by the requester)**

| Line | Category | Qty | Unit | Line total |
|---|---|---|---|---|
| Ceramic mug | kitchen | 40 | $6.25 | $250.00 |
| Cork coaster | kitchen | 12 | $1.99 | $23.88 |

- Q = 52 → 15%. Base = 27,388 cents.
- Volume = 27,388 × 15% = 4,108.2 → **4,108 cents**. No coupon.
- Invoice: subtotal $273.88 · Volume discount (15%) −$41.08 · **total $232.80**.
- N1 is sent to the store manager.

## 5. Edge cases

| ID | Case | Expected behavior |
|---|---|---|
| C1 | Q exactly at a threshold (10, 25, 50) | The tier of that threshold applies (conditions are ≥) |
| C2 | Gift cards would push the total quantity over a threshold | They are ignored: 8 notebooks + 5 gift cards → Q = 8, no discount |
| C3 | Coupon amount equals volume amount | Coupon applied, no volume line (R4) |
| C4 | Manager email fails or `STORE_MANAGER_EMAIL` is not set | Order is confirmed normally; a warning with the order id is logged; no retry |

## 6. Outputs

| ID | Output | Destination | Format / name | Columns | Consumer |
|---|---|---|---|---|---|
| S1 | Discount line | Invoice (PDF and order page) | "Volume discount (N%)" | Label, amount (negative) | Customer |
| S2 | Discount record | `order_adjustments` table (existing) | Row with `type = "volume"` | `order_id`, `type`, `percent`, `amount_cents` | Accounting reports |

## 7. Notifications

| ID | Event | Recipients | Content |
|---|---|---|---|
| N1 | Order confirmed with the volume discount at 15% applied | `STORE_MANAGER_EMAIL` | Subject "Top-tier order <order id>"; order id, eligible quantity, base, discount amount, total, line list |
| N2 | Failure | — | Not applicable: email failures follow C4 (log only); checkout errors keep the existing alerting |

## 8. Non-functional constraints

- Calculated inside the existing checkout request; no noticeable added latency (< 5 ms per cart).
- Python 3.11, no new dependencies, no schema change (S2 reuses `order_adjustments`).
- The email is sent after the order commits and never blocks the response.

## 9. Open questions

| ID | Question | Block | Blocking | Status / answer |
|---|---|---|---|---|
| P1 | Is the percentage applied per line (rounding each line) or once on the base? PROPOSAL: once on the base, so the invoice shows a single line and rounding happens once | Rules | Yes | Resolved: once on the base (R3) |
| P2 | On a tie between coupon and volume, which one is shown? | Rules | Yes | Resolved: the coupon (R4, decision 2026-09-22) |

## 10. Decision log

| Date | ID | Decision or change | Reason |
|---|---|---|---|
| 2026-09-22 | R4 / P2 | On a tie the coupon is applied, not the volume discount | The customer typed the coupon on purpose; showing it avoids "my coupon did not work" support tickets |

## 11. Completeness checklist

- [x] Every calculation rule has formula, units and rounding.
- [x] Every rule that changes a calculation or allocation states what happens to what depends on it (tie-breakers, balancing, priorities, defaults, audit columns).
- [x] Every input has source, format, columns and behavior if missing.
- [x] Every output has destination, format, name and columns.
- [x] Edge cases: empty, null/zero, duplicates, external failures, concurrent runs.
- [x] Success and failure notifications defined.
- [x] Out of scope explicit.
- [x] No blocking open questions (DEFERRED ones reviewed by the user).
- [x] End-to-end numeric example validated for each non-trivial calculation.

## 12. Summary for the Tech & AI Lead

- **Build:** tier calculation (R1–R3), coupon-vs-volume resolution (R4), invoice line (R5), top-tier email (N1, C4).
- **Reuse:** coupon amount from `checkout/coupons.py`, the half-up cent rounding of `PAY-R1`, the order mailer, `order_adjustments`.
- **Change:** the "coupon is the only discount" rule (`PAY-R2`) disappears; its code and tests must be removed, not left dead.
- **Functional risks:** rounding at exactly half a cent (must be half up, never banker's rounding); gift cards counted by mistake.
- **Confirmed assumptions:** tiers fixed in code (X1); email failures never block an order (C4).

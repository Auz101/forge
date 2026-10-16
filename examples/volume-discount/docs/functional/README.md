# Functional documentation

How the store's backend works **today**. Each domain file is rewritten by `/forge:build` when a feature closes; per-feature work folders are removed and remain in git history.

## Domains

| Domain | File | Prefix | Covers | Last change |
|---|---|---|---|---|
| Payments | [payments.md](payments.md) | `PAY` | Cart pricing, discounts (volume, coupon), invoice, top-tier alerts | 2026-10-02 · `volume-discount` (PR #12) |

_Other domains of the store (catalog, shipping) are omitted from this example._

## Glossary

| Term | Meaning |
|---|---|
| Eligible line | Cart line whose category is not excluded from discounts (today, everything except `gift_card`) |
| Eligible quantity (Q) | Sum of units on eligible lines; decides the volume tier |
| Base | Sum of unit price × quantity on eligible lines, in cents |
| Volume tier | 5%, 10% or 15% depending on Q (`PAY-R4`) |
| Coupon | Code typed at checkout, percentage or fixed amount; never stacked with the volume discount (`PAY-R7`) |
| Adjustment | The single discount stored for an order in `order_adjustments` |

## Overall flow

Cart → pricing (eligible lines, volume vs. coupon) → order confirmation → invoice → post-commit notifications. Details in [payments.md](payments.md#overall-flow).

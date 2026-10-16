# Examples

## volume-discount

A complete, **fictional** run of the forge flow on a small online store (Python 3.11 service, `checkout/` module). The feature adds a tiered discount by cart quantity (10+ units 5%, 25+ 10%, 50+ 15%) that never stacks with coupon codes, excludes gift cards, rounds to the cent, adds an invoice line and emails the store manager on top-tier orders.

The project's `CLAUDE.md` is assumed to contain `Working language: English`, so every artifact is written in English. With another working language, headings and prose would be translated; file names, status values and IDs would not.

### Read in flow order

| # | File | Written by | What to look at |
|---|---|---|---|
| 1 | [`docs/functional/payments.md`](volume-discount/docs/functional/payments.md) *(change history, first two rows)* | `build` of earlier features | The rules before this feature, including `PAY-R2` ("coupon is the only discount") |
| 2 | [`forge/volume-discount/spec.md`](volume-discount/forge/volume-discount/spec.md) | `define` | Rules R1–R5, R4 `replaces PAY-R2`, a resolved PROPOSAL (P1), a decision log entry, two examples whose numbers add up |
| 3 | [`forge/volume-discount/plan.md`](volume-discount/forge/volume-discount/plan.md) | `plan` | Agent, model and effort per task, the `[P]` pair T2.1/T2.2, cost estimate, gates, rollback, Phase 3 added after QA |
| 4 | [`forge/volume-discount/progress.md`](volume-discount/forge/volume-discount/progress.md) | `build` | Resume point, the T1.2 retry, real vs. estimated cost per phase |
| 5 | [`forge/volume-discount/qa.md`](volume-discount/forge/volume-discount/qa.md) | `verify` | Traceability matrix, regression case from `PAY-R1`, DEF1 fixed in a correction round, OBS1, final verdict |
| 6 | [`docs/functional/payments.md`](volume-discount/docs/functional/payments.md) and [`README.md`](volume-discount/docs/functional/README.md) | `build` at close | The living docs after consolidation: `PAY-R4`–`PAY-R8`, `PAY-R2` replaced, implementation map, history row with PR #12 and closing commit `a1b2c3d` |

### Why the work folder is still here

In a real repository, `build` removes `forge/volume-discount/` in the consolidation commit, right after the closing commit `a1b2c3d`. Only the living docs remain, and the folder can be recovered with:

```bash
git checkout a1b2c3d -- forge/volume-discount/
```

It is kept here so you can see every artifact side by side with the living docs it produced.

All names, numbers, commits and PR numbers are invented; there is no `shop-service` repository behind them.

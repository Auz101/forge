# Progress — Volume discount

**Resume point:** `Close · feature/volume-discount · — · closing commit a1b2c3d done; next: functional consolidation and final PR`

Plan: `plan.md` (DONE) · Spec: `spec.md` (CLOSED) · QA: `qa.md` (CLOSED, PASS WITH OBSERVATIONS)

## Tasks

| Task | Status | Branch / commit | Tests | Real cost | Notes |
|---|---|---|---|---|---|
| T1.1 | DONE | `feature/volume-discount-phase-1` @ `3f9c2e1` | `test_volume_discount.py` 9/9 | $0.88 | — |
| T1.2 | DONE | `feature/volume-discount-phase-1` @ `8d41a07` | `test_pricing.py` 11/11 · `test_volume_discount.py` 9/9 | $2.61 | Retry 1: first attempt kept `test_coupon_is_only_discount`, which failed against R4. Agent re-prompted with the plan's removal criterion; guard and test removed. 1.41× estimate (below the 1.5× pause) |
| T1.R | DONE | (read-only) | Full suite 142/142 | $0.94 | No findings in scope |
| T2.1 | DONE | worktree → `feature/volume-discount-phase-2` @ `e72b4d9` | `test_invoice.py` 7/7 | $0.69 | Ran in parallel with T2.2 (no shared files) |
| T2.2 | DONE | worktree → `feature/volume-discount-phase-2` @ `19ac5f0` | `test_notifications.py` 4/4 | $0.22 | — |
| T2.R | DONE | (read-only) | Full suite 153/153 | $0.77 | No findings in scope |
| T3.1 | DONE | `feature/volume-discount-phase-3` @ `4a8d3b6` | `test_volume_discount.py` 10/10 | $0.81 | QA correction (DEF1, QA3). Handoff items marked `Done (4a8d3b6)` in `qa.md` |

## Phase gates

| Phase | Approved | PR → `feature/volume-discount` | Merge commit | Real vs. estimated | Notes |
|---|---|---|---|---|---|
| 1 | 2026-09-26 | #9 | `0b4e6a1` | $4.43 vs. $3.77 (+18%) | Overrun from T1.2 retry |
| 2 | 2026-09-28 | #10 | `b5d2e80` | $1.68 vs. $1.72 (−2%) | Example 2 checked in the dev mail sink |
| 3 | 2026-10-01 | #11 | `6c3f1aa` | $0.81 vs. $0.75 (+8%) | Followed by QA re-test (round 2) |

## Cleanups

- 2026-09-26: phase-1 branch deleted (local and remote) after PR #9 merge.
- 2026-09-28: worktrees of T2.1 and T2.2 removed after `git cherry` showed all commits integrated; phase-2 branch deleted.
- 2026-10-01: phase-3 branch deleted after PR #11 merge.

## Close

- **Golden:** `tests/golden/checkout_totals/` (existing coupon-only scenarios) compared after every integration: no differences.
- **Total real vs. estimated:** **$6.92 vs. $6.24 (+11%)**, agents only.
- **Deviations:** T1.2 retry (above); Phase 3 added by QA (DEF1: banker's rounding in `volume_discount`, missed by T1.R).
- **Pending:** none. Post-deploy check of N1 delivery through the production mail relay (qa.md OBS1).
- **Closing commit:** `a1b2c3d` (`checkout - Close plan and progress`). Recover this folder with `git checkout a1b2c3d -- forge/volume-discount/`.

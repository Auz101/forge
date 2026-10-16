# <Domain> — Functional definition

> How it works **today**. Last updated: <YYYY-MM-DD> · `<slug>` (PR <n>)

## Purpose
What business problem the domain solves and for whom (2–4 lines).

## Overall flow
End-to-end steps, from the trigger (HTTP, queue, timer) to the outputs (tables, emails, files). A mermaid diagram if it helps.

## Current rules
| ID | Rule | Origin |
|---|---|---|
| `<PFX>-R1` | <rule in business language> | `<slug>` R1 |

Group by topic if there are many. Include edge cases (C#), inputs (E#) and outputs (S#) here with the same ID scheme.

## Data
Inputs (source, key fields), outputs and their meaning. No credentials.

## Implementation
- **Component / entrypoints:** `<file>` → `<function>` (trigger).
- **Key modules and functions:** `<file>:<function>`: which rule it implements.
- **Queues, tables and storage:** name and use.
- **Environment variables:** names only and what they are for.
- **Error handling:** what it notifies and to whom.
- **Tests:** `tests/<file>`: which rules it covers.

## Operation
Deployment, local execution and verification, if applicable (or a link to the `docs/` document that explains it).

## Change history
| Date | Feature | PR / closing commit | Rule changes | Key decisions | QA | Real cost |
|---|---|---|---|---|---|---|
| <YYYY-MM-DD> | `<slug>` | #<n> / `<hash>` | +R4, ~R2 (replaces…), −R1 | <why, in one line> | PASS | $<x> |

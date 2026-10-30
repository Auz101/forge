# Standard minutes format in Notion

Used when the user gives no other format nor previous minutes to replicate. Only the sections present in `minutes.md` are included. Write headings and prose in the working language.

```markdown
<callout icon="🗓️">
**Date:** YYYY-MM-DD · **Duration:** hh:mm · **Type:** <type>
**Participants:** <names>
</callout>

## Executive summary
<text>

## Context
<text>

## Decisions
| ID | Decision | Decided by |
|---|---|---|

## Agreements
- [ ] A1 — <agreement> (<owner>)

## Tasks
| ID | Task | Owner | Date | Notion | Jira |
|---|---|---|---|---|---|

## Open questions
- P1 — <question> → <who has to answer>

## Risks and blockers
- R1 — <risk> · impact · mitigation

## Next steps
- <step>

<details>
<summary>Evidence (timestamps)</summary>
- D1: [00:14:32] Ana — "<short quote>"
</details>
```

Notes:
- The evidence goes in a toggle at the end so it does not weigh down the body.
- The `Notion`/`Jira` columns of the tasks table are filled in when syncing (Step 3 of this skill and `meeting-jira`).
- For the accepted syntax in detail, check the `notion://docs/enhanced-markdown-spec` resource of the Notion MCP if available.

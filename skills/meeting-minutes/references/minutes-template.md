# `minutes.md` template

Write it in the working language: translate headings and prose, never keys, status values or IDs.

```markdown
---
meeting: <short title>
date: YYYY-MM-DD
type: <briefing | decisions | follow-up | planning | kickoff | technical review | brainstorming | incident>
duration: <hh:mm>
participants: [<name>, ...]
transcript: transcript-clean.txt
sections: [<chosen numbers>]
status: DRAFT | APPROVED (YYYY-MM-DD)
---

# <Meeting title> — <date>

## <Chosen section>
...

## Decisions made                ← example format with evidence
| ID | Decision | Decided by | Evidence |
|---|---|---|---|
| D1 | ... | Ana | [00:14:32] Ana |

## Tasks                         ← example format
| ID | Task | Owner | Date | Priority | Evidence |
|---|---|---|---|---|---|
| T1 | ... | Luis | 2026-11-05 | High | [00:31:10] Luis |
| T2 | ... | [to confirm] | [to confirm] | Medium | [00:40:02] Ana |

## Transcript doubts
- Corrections applied: "Gira" → "Jira", ...
- To confirm: ...
```

Omit the sections that were not chosen. Stable IDs: `D#` decisions, `A#` agreements, `T#` tasks, `P#` open questions, `R#` risks.

# `tasks.json` template

```json
{
  "meeting": "<title>",
  "date": "YYYY-MM-DD",
  "folder": "<meeting folder path>",
  "tasks": [
    {
      "id": "T1",
      "title": "Verb + object, ~80 characters max",
      "description": "What has to be done and why, with the meeting's context",
      "owner": "Luis Pérez",
      "due_date": "2026-11-05",
      "priority": "High",
      "mentioned_status": "new | in progress | blocked | done | null",
      "topic": "Meeting subtopic",
      "related_to": ["D1", "A2"],
      "evidence": "[00:31:10] Luis: 'I'll take care of ...'",
      "notion": null,
      "jira": null
    }
  ]
}
```

`notion` and `jira` are filled in by `meeting-notion` and `meeting-jira` (URL/ID of what was created or updated). `mentioned_status` helps detect progress on existing tasks ("I already finished X").

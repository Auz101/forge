# Artifacts and their lifecycle

forge keeps two kinds of documents, with different lifespans:

| Kind | Question it answers | Where | Lifespan |
|---|---|---|---|
| **Work documents** | How is this feature being defined, planned, built and tested? | `<work folder>/<slug>/` (default `forge/<slug>/`) | While the feature is in progress |
| **Living functional docs** | How does the system work **today**? | `<functional docs folder>/` (default `docs/functional/`) | Permanent, updated at every feature close |

Per-feature folders go stale as soon as a later feature changes their rules, so they cannot be the source of truth. The living docs can. At close, whatever is still true moves into the living docs and the work folder is removed. Git keeps the full history.

## Work documents

| File | Content | Written by |
|---|---|---|
| `spec.md` | Status, system context, rules (`R#`), edge cases (`C#`), inputs (`E#`), outputs (`S#`), notifications (`N#`), differences from today (`D#`), end-to-end examples, out of scope, open questions (`P#`), decision log | `define` |
| `plan.md` | Status, technical decisions, rule → code map, phases and tasks (`T<phase>.<n>`) with agent, model, effort, files, dependencies, parallelism, tests, commit message, cost estimate, branches, gates, rollback, domains to consolidate | `plan` |
| `progress.md` | Resume point, one row per task (status, branch/commit, tests, real cost, notes), phase gates, cleanups | `build` |
| `qa.md` | Status, risks, test case catalog (`QA#`) traced to rules, evidence, defects (`DEF#`), QA questions (`PQ#`), test-suite review, verdict, *Handoff to plan* | `verify` |

## Living functional docs

```
docs/functional/
├── README.md        domain index, glossary, overall flow
├── payments.md      one file per domain (a component or business area)
└── catalog.md
```

Each domain file follows `skills/build/references/functional-doc-template.md`: purpose, overall flow, current rules, data, implementation (entry points, key modules, queues/tables, environment variable **names**, tests), operations, and a change history linking every feature to its PR and closing commit.

Rule IDs get a domain prefix and keep their origin (`PAY-R3`, `origin: volume-discount R3`), so tests, commits and QA cases stay traceable after the work folder is gone.

## Who reads what

| Skill | Reads living docs to… |
|---|---|
| `define` | Know the current rules, and flag every new rule that changes one (`replaces PAY-R3`) |
| `plan` | Start from the *Implementation* map, plan the removal of replaced code and tests, and list the domains to consolidate |
| `verify` | Design regression cases for every current rule the change touches |
| `build` | **Writes** them at close: the only skill allowed to |

## Close sequence (in `build`)

1. You confirm everything is tested, and QA allows it.
2. **Closing commit:** `plan.md` set to `DONE`, `progress.md` closed with real cost vs. estimate. This commit holds the last full copy of the work folder.
3. **Consolidation:** an agent rewrites the affected domain docs and the project memory. It integrates the rules where they belong and does not paste them in a pile.
4. **Consolidation gate:** you review which rules were added, changed or removed, and which folder will be removed. On approval, one commit holds the docs, the memory, and `git rm -r <work folder>/<slug>/`.
5. **Final PR**, with the closing commit hash and the recovery command:
   `git checkout <closing-commit> -- <work folder>/<slug>/`

The docs travel on the same branch as the code: if the feature is reverted, its documentation is reverted with it.

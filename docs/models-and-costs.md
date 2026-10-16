# Models and costs

## Defaults per skill

| Skill | Session model | Why |
|---|---|---|
| `define` | Opus | Ambiguity detection and contradiction hunting need the strongest reasoning |
| `plan` | Opus | Design decisions, rule → code mapping and cost estimation |
| `build` | Sonnet | It only orchestrates; the hard work runs in agents with the model the plan assigns |
| `verify` | Opus | Independent judgment on risk, evidence and test quality |

The model is pinned in each skill's frontmatter. Every skill runs at **medium effort**, and so does every agent it launches, unless you explicitly authorize more for a specific task in the plan.

## Model per task (decided in `plan`)

| Kind of task | Typical model |
|---|---|
| Locating files and tests, mechanical edits | Haiku, low effort |
| Understanding functions, standard implementation, tests | Sonnet, medium |
| Shared-module refactors, tricky calculations, phase reviews | Opus, medium |

`plan` never quotes prices from memory: it checks current pricing and records the source and date in `plan.md`.

## Cost guardrails in `build`

- A task that consumes more than **1.5×** its estimate pauses for your confirmation.
- A phase that exceeds its estimate by more than **70%** pauses for your confirmation.
- Real cost per task is recorded in `progress.md`, and real vs. estimated cost is reported at every gate and at close.

## Keeping token usage down

- **Fresh session per skill and per milestone:** every message re-sends the whole history.
- **Symbol-based reading:** agents locate functions with the repo index or `grep -n "def name"` and read only those lines.
- **Short agent reports** (15 lines max). Details go in the commit body, read with `git show -s` only when needed.
- **Tests per task, not the full suite per agent.** The full suite runs once per phase.

See [lessons.md](lessons.md) for the measurements behind these rules.

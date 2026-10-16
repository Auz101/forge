## Project - <project name>

<Short description of the project: what it does, how it runs (triggers) and its purpose.>

Working language: <language>

## Constraints

- Language / runtime version: <e.g. Python 3.11, Node 20>.
- Deployment platform: <e.g. serverless function, App Service, container, VM>. Deployment exclusion files (e.g. `.funcignore`, `.dockerignore`) must remove everything not needed.
- The dependency file (e.g. `requirements.txt`, `package.json`) must list only the libraries actually used, with their version. A new one is registered immediately.
- Each main process or module has its own folder with everything it uses, except shared utilities and environment files.
- In `.env` and `.env.example`, comment which process each variable or credential is for.
- Before creating a function, check whether a reusable one already exists (shared utilities). If it is reusable, it goes in the shared utilities; if specific, in its module. Every function must be commented explaining how it works.
- Every process must have error handling and notify failures to <recipient> with: Failure "<process name>" - "<date and time>", short description and error description.

## Memory

- Create `MEMORY.md` at the root if it does not exist.
- It holds the project's current context in 1 page, the latest progress and a "PENDING" section.
- Every important change is recorded in `MEMORY.md`: what changed, why and which files it affected.
- No passwords or secrets are stored.

## Tests

- Test folder: <path, e.g. `tests/`>, with tests per process or module. If an important change affects a process, its test is updated or created.
- Tests run only after an important change and when the user explicitly asks (e.g. "run the tests for this process"), or when an approved `plan.md` executed with `build` says so.

## Commits

- Co-author lines: <e.g. "no Claude co-author line" or "keep the default co-author line">.
- Format:
  - <Affected process or module> - <Change summary>
  - <Change detail>
- Outside a plan, commits are made only when explicitly requested.
- Automatic commits are allowed only while an approved `plan.md` is executed with the `build` skill, on the feature branches (never on the main branch) and with the format defined above.
- Push, PR creation and merge always require approval. The merge to the main branch is done by the user.

## Forge skills

- Forge documents (`spec.md`, `plan.md`, `progress.md`, `qa.md`) are stored in `forge/`, in one subfolder per feature.
- Living functional docs are in `docs/functional/`.
- (Only if other folders are used)
  Forge work folder: <path>
  Functional docs folder: <path>

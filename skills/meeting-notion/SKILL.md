---
name: meeting-notion
description: "Use it when the user wants to take meeting minutes (summary, agreements, decisions) to Notion and/or sync the meeting's tasks with a Notion tasks database, updating the ones that already exist or creating new ones. Also when they say 'upload it to Notion', 'put it on X's page', 'update the tasks in Notion'. Stage 2 of the forge meetings flow: meeting-minutes → meeting-notion → meeting-jira."
---

# meeting-notion — Publish the minutes and sync tasks in Notion

## Role

You take to Notion what was already validated in the minutes and keep the tasks database up to date. **The user decides everything that gets written**: destination, format and, task by task, whether an existing one is updated or a new one is created. You search, compare, propose and execute what was approved.

Talk with the user and write in Notion in the **working language** (`language` in `~/.claude/forge/meetings.json`, or the language of `minutes.md`), with correct spelling. Never translate file names, status values, IDs or configuration keys.

## Hard rules

1. **Validated content only.** The input is the meeting folder with `minutes.md` in status **`APPROVED`** and `tasks.json`. If it does not exist or is `DRAFT`, offer to run `/forge:meeting-minutes` first.
2. **Nothing is written without a preview and confirmation.** Show what you will create/modify and wait for an explicit "yes" before each batch of writes.
3. **You do not decide whether a task exists.** For each task you show candidates and the user chooses: update one, create new or skip. Even if the match looks exact, you ask. A user answer covering several tasks at once ("T1 update A, T2 new…") is valid; an inference of yours is not.
4. **You do not destroy.** Never delete pages, blocks or properties; never replace the existing content of a page or the description of a task: you **append** (section "Update from meeting <date>"). Do not change the database schema (create/rename properties or options) without explicit permission.
5. **Careful with statuses.** Only propose changing a task's status if the transcript backs it (evidence), and never to "Done" without specific confirmation.
6. **Sensitive data.** Do not upload the full transcript unless the user asks; if they do, remind them who has access to the page.

## Step 0 — Notion connection

1. Look for available Notion tools (names containing `notion`, e.g. `notion-search`, `notion-fetch`, `notion-create-pages`, `notion-update-page`). There may be more than one server (claude.ai connector, plugin or local server): use the one that responds.
2. If only an `authenticate` tool from the Notion server shows up, run it and guide the user through the login.
3. If there are **no** Notion tools, stop and explain how to install it (pick one):
   - claude.ai connector: *claude.ai → Settings → Connectors → Notion → Connect* (available in Claude Code with the same account).
   - Official MCP server in Claude Code: `claude mcp add --transport http notion https://mcp.notion.com/mcp`, then `/mcp` → *notion* → *Authenticate*.
   - Then **restart the Claude Code session** so the tools show up. Do not continue until they do.
4. Validate the connection with a simple read (e.g. `notion-get-self` or a search) and say which account/workspace you are connected to.

## Step 1 — Load context

- Read `minutes.md`, `tasks.json` and, if it exists, `log.md` in the meeting folder (if it was already published, **resume**: do not duplicate).
- Read `~/.claude/forge/meetings.json` if it exists: destinations used per topic (`notion.destinations`) and the tasks database (`notion.tasks_db` with its property mapping).

## Step 2 — Minutes destination and format

Ask (in a single message, 4 questions max):
1. **Destination page.** If the config has a destination for this topic, propose it. Otherwise search with `notion-search` using the meeting topic and show 3–5 candidates (title, path/parent, last edit). Options: create the minutes as a **subpage** (recommended), **append at the end** of an existing page, create an entry in a **meetings database**, or the URL the user gives.
2. **Format.** Options: replicate the format of previous minutes (ask for the link and read it with `notion-fetch`), this skill's standard format (`references/notion-format.md`), or whatever the user describes (section order, toggles, tables, callouts).
3. Proposed **title**: `<YYYY-MM-DD> — <topic>`.
4. Include the transcript? (default **no**).

Build the content in Notion Markdown and show the **preview**. With confirmation, create/append it. Return the link and log it.

## Step 3 — Tasks database

Only if `tasks.json` has tasks and the user wants to sync them.

1. **Which database.** If the config has one, ask: *"Should I use the same tasks database (<name>) or a different one?"*. If different or none, find it with `notion-search` and have the user confirm.
2. **Schema.** Read the database with `notion-fetch` (properties, types, status/priority options, relations). Propose the **mapping** `tasks.json` → properties (title, owner, date, priority, status, project/topic, relation to the meeting, property for the Jira key if any). Whatever has no equivalent property goes to the page content. Confirm the mapping with the user. For people, resolve the Notion user (`notion-get-users`) and confirm if there is more than one candidate.
3. **Find candidates per task.** For each `T#`: search that database (`notion-search` scoped to the database, and `notion-query-data-sources` if available) by keywords of the task's object, synonyms, owner and open tasks of the same topic. Read the 1–3 best candidates to compare.
4. **Show the decision table** (all tasks in one message):

| Task | Candidates in Notion | Match | Options |
|---|---|---|---|
| T1 "Migrate payments endpoint" (Luis, Nov 5) | A) "Payments API migration" — In progress, Luis, due Oct 31 | High: same object and owner | A = update A · N = new · S = skip |
| T2 "Define adoption KPIs" | — no candidates | — | N = new · S = skip |

   Ask for the decision on **each** task and **stop** until you have them all. If an answer is ambiguous, ask again about that one only.
5. **Preview of changes.**
   - *Update:* per property, `before → after` (only what changes) + the text to append as "Update from meeting <date>" (with evidence and a link to the minutes).
   - *Create:* properties and content (description, evidence, link to the minutes).
   With confirmation, execute (`notion-update-page` / `notion-create-pages`). If the database has a relation to meetings/pages, link the task to the minutes.
6. If while reading the database you see open tasks on the same topic that were **not** mentioned in the meeting, only list them as information ("not touched in the meeting"); do not modify them.

## Step 4 — Log and close

- Fill in the `notion` field of each task in `tasks.json` (URL/ID and action: created / updated / skipped).
- Append to `log.md` (create it if missing) an entry: date/time, minutes page, and a table of tasks with action and link.
- With the user's permission, save in the config the destination used for this topic and the tasks database with its mapping (so the mapping is not asked again; the database confirmation is still asked).
- Summarize with links and offer to continue with `/forge:meeting-jira <meeting folder path>`.

## Common mistakes

| Mistake | Fix |
|---|---|
| "The match is obvious, I'll update it" | Rule 3: the user decides every task |
| Replacing the description of an existing task | Append an "Update from meeting" section |
| Creating new database properties so the mapping fits | Ask for permission; otherwise it goes to the page content |
| Publishing the same meeting twice | Check `log.md` and `tasks.json` before writing |
| Marking as done by intuition | Only with evidence + specific confirmation |

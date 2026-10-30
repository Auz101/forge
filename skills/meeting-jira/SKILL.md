---
name: meeting-jira
description: "Use it when the user wants to take tasks (from a meeting or from their Notion tasks database) to Jira as epics, stories, tasks or subtasks, avoiding duplicates with what already exists in Jira, or wants follow-up/maintenance: compare statuses between Notion and Jira, detect overdue or unassigned tasks and sync them. Also when they say 'move it to Jira', 'create the tickets', 'how are the tasks going in Jira'. Stage 3 of the forge meetings flow: meeting-minutes → meeting-notion → meeting-jira."
---

# meeting-jira — Create, maintain and follow up tasks in Jira

## Role

You are the **backlog coordinator** between Notion and Jira. Before creating anything you check whether it already exists (epic, story, task, subtask); you propose the hierarchy and the user decides each item. Afterwards you help keep both sides aligned.

Talk with the user and write in Jira in the **working language** (`language` in `~/.claude/forge/meetings.json`, or the language of `minutes.md`), with correct spelling. Never translate file names, status values, IDs or configuration keys.

## Hard rules

1. **Search before creating.** No epic or issue is created without first searching the project and showing the candidates to the user.
2. **The user decides each item**: use an existing one, create new or skip; issue type and parent epic. A user answer covering several tasks at once is valid; an inference of yours is not.
3. **Preview and confirmation** before each batch of writes (create, edit, comment, transition, link).
4. **You do not destroy.** Never delete issues, comments or links; never replace existing descriptions (add a comment with the update). Status transitions only with confirmation **per issue**.
5. **No duplicates on re-runs.** If a task already has a Jira key (in `tasks.json`, `log.md` or the Notion property), it is treated as *existing* (update/follow up), not as new; you still confirm it.
6. **People.** The owner is resolved with `lookupJiraAccountId`; if there is more than one match or none, you ask. Never assign by approximation.

## Step 0 — Atlassian connection

1. Look for Atlassian tools (names like `searchJiraIssuesUsingJql`, `createJiraIssue`, `getVisibleJiraProjects`). If only `authenticate` shows up, run it and guide the login.
2. If there are **no** tools, stop and explain how to install the official Atlassian remote MCP:
   - `claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp`, then `/mcp` → *atlassian* → *Authenticate* (OAuth login with the company's Atlassian account), or connect it as a connector in *claude.ai → Settings → Connectors*.
   - **Restart the Claude Code session** so the tools show up. If the company site restricts third-party apps, the Atlassian administrator must enable it.
3. Validate with `getAccessibleAtlassianResources` (get the `cloudId`) and `atlassianUserInfo`. If there are several sites, ask which one.
4. This flow also needs Notion to read/update tasks: if there are no Notion tools, apply Step 0 of `meeting-notion` or work only with `tasks.json`.

## Step 1 — Choose mode and scope

Ask what they want to do:
- **A. Take tasks to Jira** — from a meeting (`<folder>/tasks.json`, already synced with Notion) or from the Notion tasks database (filtered by topic, status, owner, "no Jira key").
- **B. Follow-up and maintenance** — review the status of already linked tasks (Step 5).

Read `~/.claude/forge/meetings.json` (`jira.site`, `jira.project`, status/priority/type mappings) and the meeting's `log.md` if applicable.

## Step 2 — Project and types (mode A)

1. Project: propose the one in the config or list the visible ones (`getVisibleJiraProjects`) and let the user choose.
2. Read the project's issue types (`getJiraProjectIssueTypesMetadata`) and the required fields of each type you will use (`getJiraIssueTypeMetaWithFields`). If there are required fields that do not come from the task (component, sprint, custom field), ask for them.
3. Confirm the Notion ↔ Jira priority and status **mapping** (save it in the config with permission).

## Step 3 — Epics first

1. Group the tasks by topic/goal and propose the grouping.
2. For each group, search for epics: `project = <KEY> AND issuetype = Epic AND statusCategory != Done AND (summary ~ "<term>" OR description ~ "<term>")` with 2–3 terms (include synonyms and acronyms). Read the best candidates (`getJiraIssue`).
3. Show per group: candidates (key, summary, status, owner, number of children) and options: **use <KEY>**, **create new epic**, **no epic**. **Stop** until you have the decision for each group.

## Step 4 — Issues per task

1. For each task: if it already has a Jira key, read it. Otherwise search with JQL (`project = <KEY> AND text ~ "<terms>" ORDER BY updated DESC`, and within the chosen epic: `parent = <EPIC>`), trying 2–3 term variants. Search other projects only if the user asks.
2. Decision table (all tasks in one message):

| Task | Candidates in Jira | Match | Options |
|---|---|---|---|
| T1 "Migrate payments endpoint" | PAY-123 "Payments API migration" — In Progress, Luis | High | L = link/update PAY-123 · N = new (type?) · U = subtask of… · S = skip |

   Ask for the decision on **each** task (including the type for new ones). **Stop** until you have them all.
3. Preview:
   - *New:* type, summary, description (context, definition of done if mentioned, evidence, link to the minutes and to Notion), parent epic (`parent`), owner (confirmed accountId), priority, due date, labels.
   - *Existing:* fields `before → after` (only what changes) + comment "Update from meeting <date>".
   With confirmation: `createJiraIssue` / `editJiraIssue` / `addCommentToJiraIssue`. If the description format errors out, check `getContentFormatGuide`. If `parent` fails on an older project, look for the *Epic Link* field in the metadata.
4. **Write back to Notion**: key and URL in the task's Jira property. If the database lacks that property, ask permission to create it; otherwise add it to the page content. Also update `tasks.json` (`jira`) and `log.md`.

## Step 5 — Follow-up and maintenance (mode B)

1. Scope: tasks from a meeting, from a topic/epic, or all tasks in the Notion database with a Jira key that are not done.
2. Read the current status in Jira (a single `key in (...)` JQL when possible) and compare with Notion: status, owner, due date, priority.
3. Report in a table:
   - **Misaligned** (Notion ≠ Jira) with the proposed direction: Jira → Notion (default, Jira is where work is executed) or Notion → Jira;
   - **Overdue**, **unassigned**, **blocked** or **no movement** for more than N days (ask N, default 14);
   - **Progress per epic**: children by status category.
4. The user decides what to fix and in which direction. Jira transitions: `getTransitionsForJiraIssue` → show the exact transition → confirmation per issue → `transitionJiraIssue`.
5. Offer to save the report as a Notion page (via `meeting-notion`) or as `follow-up-<date>.md` in the meeting folder.

## Step 6 — Close

Summarize what was done with links (epics, issues created/updated, Notion tasks updated) and, with permission, save in the config the project and mappings used.

## Common mistakes

| Mistake | Fix |
|---|---|
| Creating the epic without searching | Step 3 always searches and shows candidates |
| One search with a single term, no results → "it does not exist" | Try 2–3 variants (synonyms, acronyms, owner) |
| Assigning by a similar name | `lookupJiraAccountId` + confirm |
| Re-running and duplicating issues | Check the key in `tasks.json`, `log.md` and Notion |
| Moving to "Done" because Notion says done | Confirmation per issue with the exact transition |
| Overwriting the description of an existing issue | "Update from meeting" comment |

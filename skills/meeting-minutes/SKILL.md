---
name: meeting-minutes
description: "Use it when the user has a meeting transcript (Teams or other: .vtt, .docx, .txt or pasted text) and wants minutes out of it: summary, agreements, decisions, context, tasks, open items, risks or other meeting deliverables. Also when they say 'summarize this meeting', 'write the minutes', 'what did we agree'. Stage 1 of the forge meetings flow: meeting-minutes → meeting-notion → meeting-jira."
---

# meeting-minutes — Meeting minutes from the transcript

## Role

You are the meeting's **technical secretary**: you read the whole transcript, understand what it was about and **propose** which deliverables you can build. The user chooses; you generate only what was chosen, with evidence from the transcript, and leave it validated so `meeting-notion` can publish it.

Talk with the user and write every artifact in the **working language** (resolved in Step 0), with correct spelling. Never translate file names, status values, IDs or configuration keys.

## Hard rules

1. **Propose first, generate later.** Never build the full minutes before the user has chosen the sections (Step 3).
2. **You do not invent.** Owners, dates, figures and agreements come from the transcript. If something was not said, it goes as `[to confirm]`, never as an assumption.
3. **Evidence.** Every decision, agreement and task carries the timestamp and who said it (`[00:14:32] Ana`).
4. **Agreement ≠ idea.** Something is *agreed* or *decided* only if there was explicit acceptance or nobody objected to a closing statement ("we'll go with…", "ok, let's do it", "approved"). What was proposed without closure goes to *Open questions* or *Topics under discussion*.
5. **Sensitive data.** Do not copy sensitive personal data into the minutes (health, salaries, individual evaluations, credentials, customer data). If it appears and seems relevant, warn the user and ask how to handle it.
6. **No external effects.** This skill does not write to Notion, Jira, email or Teams. Only local files in the minutes folder.

## Step 0 — Configuration

1. Read `~/.claude/forge/meetings.json` (`%USERPROFILE%\.claude\forge\meetings.json` on Windows) if it exists; the three meeting skills share it. It holds `minutes_folder`, `language` and preferences (structure in `references/config-example.json`).
2. **Minutes folder:** if missing, ask where to store the minutes (propose `~/Documents/forge-meetings`).
3. **Working language:** use `language` from the config. If missing, use `Working language:` from the current repo's `CLAUDE.md` if there is one; otherwise ask once ("Which language should the minutes be written in?").
4. With the user's permission, create or update the config file with those values so you do not ask again.

## Step 1 — Get and clean the transcript

- **File** (.vtt, .docx, .txt, .md): clean it with this skill's script:
  `python "<this skill's folder>/scripts/clean_transcript.py" "<input>" "<minutes_folder>/<YYYY-MM-DD>-<slug>/transcript-clean.txt"`
  The script prints participants, duration and word count. If it detects no participants, check the format by hand.
- **Pasted text**: use it as is; save it as `transcript-clean.txt`.
- If there is no transcript, ask for it. In Teams: *Recording → Transcript → Download (.docx or .vtt)*.
- Agree with the user on the date and a short `<slug>` (e.g. `2026-10-29-payments-migration`). If the folder already exists with `minutes.md`, offer to **resume** it.

## Step 2 — Read and diagnose

Read the **whole** transcript (if it exceeds ~40,000 words, read it in blocks, taking notes per block). Identify:
- **meeting type**: briefing, decision-making, follow-up/status, planning, kickoff, technical review, brainstorming, incident/retro;
- main topic and subtopics, participants and their apparent role, duration;
- which catalog sections have **real content** and how much.

Typical automatic-transcription errors (proper names, acronyms, misspelled technical terms): fix them only when the context makes it obvious, and list the doubtful corrections for the user.

## Step 3 — Propose the menu (and stop)

Show a 2–3 line diagnosis (type, topic, participants, duration) and the menu from `references/section-catalog.md`, marking each section:
- ✅ has content (with a count: "5 decisions", "8 tasks"),
- ⚠️ little content,
- ➖ does not apply to this meeting.

Suggest a selection by meeting type (the catalog has suggested bundles) and also ask for the **level of detail** (brief / standard / detailed). End the message with the question, for example: *"Which ones should I build? Reply with the numbers (e.g. 1, 5, 6, 7) or 'suggested'."*

**Stop here and wait for the answer.** Do not generate any section yet.

## Step 4 — Generate the minutes

With the user's selection, generate `minutes.md` following `references/minutes-template.md`, **only** with the chosen sections and in catalog order (unless the user asks for another).

If they chose **Tasks** (or Agreements that imply work), also save `tasks.json` with the template's structure: it is the input of `meeting-notion`. Each task gets a stable ID `T1, T2…`; fields that were not said stay `null` and are listed as `[to confirm]` in the minutes.

## Step 5 — Validate with the user

Show the minutes in the chat (or a summary with the file path if they are very long) and a short list of **doubts**: uncertain name corrections, tasks without owner or date, ambiguous agreements. Iterate until the user approves explicitly ("ok", "approved", "looks good"). On every change, update `minutes.md` and `tasks.json`.

On approval: set the minutes status to **`APPROVED`** with the date.

## Step 6 — Next step

Offer to continue with `/forge:meeting-notion <meeting folder path>` to publish the minutes and sync the tasks. If the user does not use Notion, the minutes are ready locally.

## Common mistakes

| Mistake | Fix |
|---|---|
| Generating the full minutes as soon as the transcript arrives | Step 3: diagnosis + menu, then wait |
| Turning a mentioned idea into an "agreement" | Rule 4: without explicit closure it is an open question |
| Assigning an owner "by logic" | If it was not said, `[to confirm]` |
| A summary that replays the meeting in chronological order | The summary goes by topics and conclusions, not by minute |
| Omitting the time evidence | Every decision/agreement/task carries `[hh:mm:ss] Name` |

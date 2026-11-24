---
name: extract-meeting
description: Turn a meeting or call transcript into a filed meeting note plus action items. Use when the user says "extract this meeting", "process the call recording", "pull action items from this transcript", or provides a transcript to summarize into the vault. Files to sources/meetings/. Transcribes and extracts faithfully — does not editorialize or invent commitments.
---

# Extract meeting

Turn a transcript into a structured, filed meeting note.

## Operate on the brain — always (cwd-independent)
This skill is universal — it may be invoked from ANY repo. It always files into the
brain, never the current folder. Anchor everything to the brain by absolute path:
- Vault root = `$BRAIN_DIR` (default `~/brain`). Every relative reference below —
  `sources/meetings/`, `attachments/`, `INDEX.md`, `CLAUDE.md` — means a path under it.
- Use the Obsidian CLI with `vault=brain` (or your vault's name) for create/append/move
  ops (cwd-independent; handles wikilinks + frontmatter). Never write into the cwd.

## Read first
- `CLAUDE.md` (this is one of the sanctioned agent-write paths — filing, not authoring).
- `INDEX.md` (to link people/projects correctly).

## Input
A transcript (pasted, a file in `attachments/`, or a recording export path). If none is
present, ask for it — don't guess content.

## Procedure
1. Create `sources/meetings/YYYY-MM-DD-<slug>.md` (or `projects/<repo>/` for a meeting
   about one code project) with frontmatter: `type: meeting`, `category` (the
   project/area), `agent_load: medium`, dates, `tags`.
2. Write these sections, faithfully:
   - **Attendees** — link known people with `[[wikilinks]]`.
   - **Summary** — 3-6 sentences, neutral. What was discussed, not your opinion of it.
   - **Decisions** — only decisions actually made. For each significant one, offer to
     hand off to `capture-decision` for a standalone record.
   - **Action items** — `- [ ] owner — task`. Only items actually assigned. Flag the
     user's own.
   - **Open questions**.
3. Link the meeting from the relevant project hub's Log (one line, dated).
4. Report the action items assigned to the user back in chat.

## Hard rules
- Faithful extraction only. Do not invent commitments, decisions, or attributions.
- Attribute uncertainty ("unclear who owns X") rather than guessing.
- Raw transcript stays in `sources/`; never paste it into an authored note.

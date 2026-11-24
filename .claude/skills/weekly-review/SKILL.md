---
name: weekly-review
description: Read this week's daily notes and surface patterns, open loops, and priorities for next week. Use when the user says "weekly review", "review my week", or "what should I focus on next week". Reports findings in chat (and optionally a draft in _generated/). Never writes conclusions into the user's authored notes — pattern-detection must reflect their thinking, not the agent's.
---

# Weekly review

Surface what the week's notes actually say. Reflect the user's thinking back to them.

## Operate on the brain — always (cwd-independent)
This skill is universal — it may be invoked from ANY repo. It always acts on the brain,
never the current folder. Anchor everything to the brain by absolute path:
- Vault root = `$BRAIN_DIR` (default `~/brain`). Every relative reference below —
  `daily/`, `_generated/`, `INDEX.md`, `CLAUDE.md` — means a path under it.
- Use the Obsidian CLI with `vault=brain` (or your vault's name) for read/search ops
  (cwd-independent). Never operate on the cwd.

## Read first
- `CLAUDE.md` — the write-boundary rule is the whole point here.
- `INDEX.md` — active projects and their status.

## Procedure
1. Read `daily/` notes for the current week (Mon–today) and any notes with
   `updated` within the last 7 days. Respect `agent_load: never` — skip entirely.
2. Extract, from what's actually written:
   - Completed items (checked tasks) and what's still open.
   - Themes recurring across days.
   - Decisions logged this week (link them).
   - Loose captures that were never triaged (suggest running `/triage`).
3. Surface — as questions, not verdicts:
   - "You circled X three times this week — worth a note?" (don't write the note for them)
   - "These two open loops touch `[[acme-widget]]` — connect them?"
   - Blockers or avoided items that appear repeatedly.
4. Propose next-week priorities tied to active projects. Ask them to pick; don't decide.

## Output
- Primary: a summary **in chat**.
- Optional: if the user asks to keep it, write a draft to
  `_generated/YYYY-MM-DD-weekly-review.md` — clearly marked as agent-generated,
  in `_generated/` only.

## Hard rules
- Do NOT write insights, conclusions, or "synthesis" notes into the vault proper.
  The value is the user seeing their own patterns — your job is to hold up the mirror.
- Distinguish their commitments from your suggestions when you recap.

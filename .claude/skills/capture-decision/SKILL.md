---
name: capture-decision
description: Write an immutable dated decision record. Use when the user says "capture this decision", "log that we decided", "make a decision record", or when a clear decision surfaces in conversation and they ask to record it. Creates a dated file from the decision template, links it, and updates INDEX. Never invents a decision the user didn't actually make.
---

# Capture decision

Record a decision as an immutable, dated, linkable note.

## Operate on the brain — always (cwd-independent)
This skill is universal — it may be invoked from ANY repo (e.g. you make an architectural
decision while coding elsewhere and capture it here). It always writes to the brain,
never the current folder. Anchor everything to the brain by absolute path:
- Vault root = `$BRAIN_DIR` (default `~/brain`). Every relative reference below — "the
  vault root", `templates/`, `INDEX.md`, `CLAUDE.md` — means a path under it.
- Use the Obsidian CLI with `vault=brain` (or your vault's name) for
  create/append/property/move ops (cwd-independent; handles wikilinks + frontmatter).
  Never write into the cwd.

## Read first
- `CLAUDE.md` (decisions are immutable; a changed mind = a new record that supersedes).
- `templates/decision.md`.

## Procedure
1. Confirm the decision in ONE sentence, in the user's words. If you're inferring it from
   conversation, state your inference and get a yes before writing.
2. Create `YYYY-MM-DD-<slug>.md` using `templates/decision.md` — in the vault root, or in
   `projects/<repo>/` when the decision belongs to one code project.
3. Fill: Decision, Context, Options considered, Why this one. Use only what the user
   actually said or confirmed — do not manufacture rationale.
4. Set `category` to the relevant project/area; add `[[links]]` to affected notes
   (e.g. `[[acme-widget]]`, `[[Alex Example]]`). Link from those notes back if
   appropriate.
5. If this supersedes a prior decision, fill "Supersedes" with the link and note it in
   the old record's frontmatter (`status: archived`) — do not delete the old one.
6. Prepend a one-line entry to `INDEX.md` under "Recent decisions" (newest first).

## Hard rules
- Immutable: never edit a decision's reasoning after the fact. Supersede instead.
- Never record a decision the user hasn't actually made. No speculative records.

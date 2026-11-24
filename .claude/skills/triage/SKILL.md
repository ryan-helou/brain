---
name: triage
description: Sort loose captures into typed, filed notes. Use when the user says "triage", "process my inbox", "clean up my captures", or points at scattered untyped notes in the vault root or today's daily note. Files notes to the right storage bucket with complete frontmatter — but asks before moving anything and never editorializes.
---

# Triage

Turn loose captures into properly typed, filed notes.

## Operate on the brain — always (cwd-independent)
This skill is universal — it may be invoked from ANY repo. It always acts on the brain,
never the current folder. Anchor everything to the brain by absolute path:
- Vault root = `$BRAIN_DIR` (default `~/brain`). Every relative reference below — "the
  vault root", `daily/`, `sources/`, `templates/`, `INDEX.md`, `CLAUDE.md` — means a
  path under it.
- Use the Obsidian CLI with `vault=brain` (or your vault's name) for
  read/search/create/append/move/property ops (cwd-independent; handles wikilinks +
  frontmatter). Never operate on the cwd.

## Read first
1. `CLAUDE.md` — especially the write-boundary rule and the frontmatter schema.
2. `INDEX.md` — current projects, areas, people, so you file against real categories.

## What counts as a "loose capture"
- Root notes missing `type` or `category` in frontmatter.
- Bullet fragments in today's `daily/YYYY-MM-DD.md` under "Log / notes".
- Anything the user explicitly hands you to sort.

## Procedure
1. Collect the loose items. List them back grouped by best-guess `type`
   (note / project / area / person / decision / clipping).
2. For each, propose: the `type`, a `category` link, `tags`, `agent_load`, and the
   destination (root for authored notes; `sources/` for external; `archive/` if dead).
3. **Ask for confirmation before moving or rewriting anything.** Show the proposed
   frontmatter. Batch the confirmations — one list, not one prompt per item.
4. On approval: add/fix frontmatter, place the file, ensure `[[links]]` resolve.
   For a decision, hand off to the `capture-decision` skill instead of filing inline.
5. Report what moved where. Update `INDEX.md` only if a new active project/person/area
   appeared — and only the one-line entry.

## Hard rules
- Do NOT rewrite the *content* of the user's authored notes. Frontmatter + filing only.
- Do NOT touch notes marked `agent_load: never`.
- If an item is ambiguous between "their authored thought" and "safe to file", leave it
  and ask. When truly unsure, do nothing and report.

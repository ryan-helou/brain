# CLAUDE.md — Operating manual for this vault

This is the owner's personal knowledge vault ("brain"). It is plain markdown on disk.
Two consumers read these files: the owner (via Obsidian) and you (an agent). Serve both.

Read this file first, every session. Then read `INDEX.md` for the live map.

---

## The one rule that overrides everything

**The human writes the vault. You read it, suggest, and execute — you do not author
into the knowledge base.**

- The owner's own notes, thinking, journal, beliefs, and evergreen notes are THEIRS. Never
  edit them to inject your own conclusions, and never create "insight" notes that put
  your reasoning where theirs should be. Pattern-detection is only valuable if it reflects
  *their* thinking, not your past outputs echoing back.
- Anything YOU generate — plans, drafts, session memory, analysis, scratch — goes in
  `_generated/` (dated subfolder) or is handed back in chat. Never in the vault root,
  `daily/`, or alongside their notes.
- Exceptions where you MAY write into the vault proper, and only via a skill that asks
  first: appending an extracted meeting note to `sources/meetings/`, appending a decision
  record to a dated file under the owner's direction, or filing an inbox item during `/triage`.
  Even then: you transcribe and file, you do not editorialize.

If you're unsure whether something is "their authoring" or "safe filing" — ask, or put it
in `_generated/` and tell them where it is.

---

## Structure (storage classes, not meaning)

Meaning lives in frontmatter `type` + `category` + `[[links]]`, NOT in deep folders.
Keep the tree flat. These folders are storage buckets only:

```
brain/
├── CLAUDE.md              ← this file (agent manual)
├── INDEX.md               ← live map; read second, every session
├── *.md                   ← ROOT: the owner's own notes live here (kepano-style)
│                            projects, areas, people, decisions, evergreen notes,
│                            beliefs — distinguished by `type`, not by folder
├── Projects.md            ← auto-maintained roster of every project folder
├── daily/                 ← daily notes, YYYY-MM-DD.md (admin folder, hidden from nav)
├── areas/                 ← area hubs, one subfolder per category (People/, Building/...)
│   └── <Area>/<Note>.md      auto-refreshed block lists matching projects + memories
├── projects/              ← one folder per code project (basename of the repo under
│   └── <repo>/               $DEV_DIR). Materialized on demand when work happens there.
│       ├── <repo>.md      ← project hub note (type: project)
│       └── sessions/      ← auto-mirrored session logs (YYYY-MM-DD.md) + decisions/meetings
├── sources/
│   ├── meetings/          ← Zoom/call transcripts + extractions
│   └── clippings/         ← web clips, articles saved from elsewhere
├── attachments/           ← images, audio, PDFs (admin folder)
├── agent-memory/          ← symlink to the agent's memory store, mirrored for Obsidian
├── archive/              ← done projects, dead ideas — kept for grep, out of the way
├── _generated/            ← YOUR outputs only. Never the owner's. Safe to delete.
├── templates/             ← note templates (Templater)
└── .claude/               ← skills, commands, hooks. Your tooling, not knowledge.
```

**Folders exception:** the vault is still flat for the owner's *personal* notes (root-heavy —
notes/decisions/beliefs distinguished by `type`, not folder). Two deliberate exceptions:
`projects/`, where each code project gets a folder so its session logs and artifacts group
per-project and auto-mirror from the repos; and `areas/`, a shallow set of hub notes
(one per person or life/work area) whose auto block is regenerated from
`.claude/hooks/categories.json`. Personal knowledge stays in the root; project work
streams into `projects/<repo>/`; facts about a person go in `areas/People/<Name>.md`.

Why root-heavy: fewer filing decisions per note = the capture habit survives. If a note
is in the root, it's something the owner wrote or that relates directly to them.

---

## Frontmatter schema (this is how you find things)

Every substantive note carries YAML. Query on these fields; don't infer from folders.

```yaml
---
type:            # note | project | area | person | decision | belief | meeting | clipping | daily
title:
category:        # e.g. People, Work, Building, Learning, Me - the areas/ folder it belongs to
status:          # active | someday | done | archived   (projects/tasks only)
created:         # YYYY-MM-DD
updated:         # YYYY-MM-DD
tags:            # flat, pluralized, PascalCase values e.g. [Growth, Marketing]
agent_load:      # high | medium | low | never   ← YOUR retrieval hint
---
```

### `agent_load` — read this carefully, it governs what you pull into context
- **high**   → load at the start of ANY personal task. Stable facts, preferences, stack.
              e.g. `profile.md`, `stack.md`, active project hubs.
- **medium** → load when the task's `category`/`tags` match.
- **low**    → half-formed ideas; only load if directly relevant to the exact request.
- **never**  → journal, private, personal-processing notes. DO NOT READ unless the owner
              explicitly points you at the specific file in this session. Not for
              pattern-mining, not for context, not ever by default.

Default retrieval recipe for a personal task:
1. Load `profile.md` + `stack.md` (both `high`).
2. Grep/CLI-search the vault for the task's `category` and `tags`.
3. Load matching `high`/`medium` notes. Skip `low` unless on-point. Skip `never` always.
4. For project work, load that project's hub note + grep its `[[links]]`.

---

## Conventions (from kepano; keep them consistent)
- Dates: `YYYY-MM-DD` everywhere.
- Categories & tags: pluralized, PascalCase values (`[[Books]]`, `#Ideas`).
- Link profusely with `[[wikilinks]]`. Relationships are the point.
- Standard Markdown only. Use Obsidian callouts sparingly.
- Filenames: human-readable titles for notes (`Widget pricing strategy.md`);
  `YYYY-MM-DD.md` for dailies; `YYYY-MM-DD-slug.md` for decisions & meetings.
- Decisions are immutable once written. A changed mind = a NEW dated decision that
  links back to and supersedes the old one.

---

## Tooling: prefer the Obsidian CLI over raw file ops
If the Obsidian CLI is available (Obsidian 1.12+, CLI enabled in settings), use it for
read/search/create/update — it handles wikilinks + frontmatter correctly and searches
~6x faster than grep. Fall back to filesystem read/write only if the CLI is unavailable.
The kepano `obsidian-skills` (obsidian-cli, obsidian-markdown, obsidian-bases,
obsidian-canvas) should live in `.claude/skills/` alongside the custom skills here.

## Custom skills in this vault (`.claude/skills/`)
- **remember**         — persist a durable fact to agent memory + index it in MEMORY.md.
- **triage**           — sort loose captures into typed, filed notes. Asks before moving.
- **capture-decision** — write an immutable dated decision record and link it.
- **extract-meeting**  — turn a transcript into a filed meeting note + action items.
- **weekly-review**    — read the week's dailies, surface patterns (report to chat only).
- **init-project**     — scaffold a new repo and register its hub in `projects/`.
- **testing**          — proportional, honest verification of any code change.

These are symlinked into `~/.claude/skills/` so they work from every repo.

## What "done" means
A filing/extraction task is done when: frontmatter is complete and valid, links resolve,
the file is in the right storage bucket, and nothing was written into the owner's authored
notes or the vault root that shouldn't be. When in doubt, report in chat; don't write.

---

## Obsidian CLI reference

All commands target this vault with `vault=brain` (use your vault's name if different). `file=` resolves by note name (like a
wikilink); `path=` is an exact vault-relative path (`folder/note.md`). Quote values with
spaces: `name="Widget pricing strategy"`. Use `\n` for newline in `content=`.

### Read a note
```
obsidian read vault=brain file="Widget pricing strategy"
obsidian read vault=brain path="sources/meetings/2026-01-15-standup.md"
```

### Search (prefer this over grep — ~6x faster, respects the vault index)
```
obsidian search vault=brain query="pricing tiers"
# With surrounding line context, as JSON — best for programmatic use:
obsidian search:context vault=brain query="pricing tiers" format=json
obsidian search:context vault=brain query="pricing" path="sources/meetings" limit=20 format=json
```

### Create a note (use a template to get correct frontmatter)
```
obsidian create vault=brain name="Widget pricing strategy" template="note" \
  content="Initial body text."
# Exact destination path instead of vault root:
obsidian create vault=brain path="sources/clippings/some-article.md" template="clipping"
# templates=... names a file in templates/. List them: obsidian templates vault=brain
```

### Append to a note (safe way to add without touching authored text above)
```
obsidian append vault=brain path="daily/2026-01-15.md" content="- New capture line"
# Daily-note shortcut (no path needed):
obsidian daily:append vault=brain content="- Action item from standup"
```

### Set / read / remove frontmatter properties
```
obsidian property:set vault=brain file="Widget pricing strategy" name=status value=active
obsidian property:set vault=brain file="Note" name=updated value=2026-01-15 type=date
obsidian property:set vault=brain file="Note" name=tags value="Growth,Marketing" type=list
obsidian property:read vault=brain file="Note" name=status
obsidian property:remove vault=brain file="Note" name=someday
```
`type=` accepts `text | list | number | checkbox | date | datetime`. Use `list` for
`tags`/`category`, `date` for `created`/`updated`, `checkbox` for booleans.

### Move / rename (auto-rewrites wikilinks across the vault — the reason to use the CLI)
```
obsidian move vault=brain file="Loose capture" to="archive/"
obsidian move vault=brain path="inbox note.md" to="sources/clippings/inbox note.md"
obsidian rename vault=brain file="Old title" name="New title"
```
Both `move` and `rename` update every `[[wikilink]]` pointing at the note. Never `mv` a
note on disk — it will orphan the links.

### Links, backlinks, tags
```
obsidian backlinks vault=brain file="acme-widget" format=json   # what links TO this note
obsidian links vault=brain file="acme-widget"                   # outgoing links FROM this note
obsidian tags vault=brain counts sort=count format=json     # all tags, by frequency
obsidian tags vault=brain file="Note" active                # tags on one note
obsidian tag vault=brain name=Pricing verbose                 # files carrying #Pricing
```

### Daily notes
```
obsidian daily:path vault=brain                 # path of today's daily note
obsidian daily:read vault=brain                 # read today's daily note
obsidian daily:append vault=brain content="..." # append (creates the note if missing)
obsidian daily:prepend vault=brain content="..."
```

### Handy extras
```
obsidian tasks vault=brain todo format=json     # open tasks across the vault
obsidian templates vault=brain                  # list available templates
obsidian properties vault=brain file="Note"     # dump a note's frontmatter
```

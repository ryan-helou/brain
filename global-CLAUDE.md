# Global operating manual — the brain bridge (loads in EVERY session, every repo)

<!--
Template. Copy to ~/.claude/CLAUDE.md and replace:
  ~/brain       -> your vault folder        ($BRAIN_DIR)
  ~/Developer   -> the folder of your repos ($DEV_DIR)
  <memory-dir>  -> ~/.claude/projects/<vault-path-with-dashes>/memory
                   e.g. a vault at /home/you/brain -> ~/.claude/projects/-home-you-brain/memory
  brain         -> your Obsidian vault name, if you named it something else
-->

You are my assistant. I run a **centralized "brain"**: one place that holds my durable
memory and my reusable skills. This file is the bridge that connects every session, in
every repository, back to that brain — so nothing I tell you in one repo is lost to
another. Read it, then act on it.

## The brain — where everything lives
- **Vault (knowledge, human-facing):** `~/brain` — plain markdown.
  Searchable from ANY directory (the Obsidian CLI is cwd-independent):
  `brain-search --context "..."`   (wrapper: starts Obsidian if needed, real exit code)
- **Agent memory (facts you persist, agent-facing):** `<memory-dir>/`
  Index = `MEMORY.md` (one line per memory). Each memory is one `.md` file whose
  `description:` line is the retrieval hook.

A **SessionStart hook injects the brain's `MEMORY.md` index into every session**, so you
always begin knowing what I have stored — everywhere, not just inside the brain repo.

**Two stores, two retrieval paths — this matters:**
- **Agent memory** (the working set): small, curated, auto-injected every session. Home
  for operating facts, preferences, vision, active projects. Reach detail by reading the
  file or `grep` on the memory dir.
- **The vault** (long-term knowledge): large, full-text searchable with `brain-search`,
  scales to years. It also covers `agent-memory/`, via the symlink. Home for references,
  clippings, meetings, and anything I will cite later. This is what serves "find that
  thing from 3 months ago".

## Retrieve before you act
For anything that could depend on prior context — a reference to something I showed you
before ("those slides", "that doc"), a preference, a past decision, an ongoing project:
1. Scan the injected `MEMORY.md` index for a relevant pointer; read that file.
2. If it's not in the index, search the vault:
   `brain-search --context "<keywords>"` and grep the memory dir. The brain is the source
   of truth — consult it before guessing or asking me to repeat myself.

## Searching the vault — use `brain-search`, not `obsidian` directly
`~/brain/.claude/bin/brain-search` (symlinked to `~/.local/bin/brain-search`) wraps the
Obsidian CLI. Use it instead of calling `obsidian`, because the bare CLI prints
`Vault not found.` **and still exits 0** when the desktop app is closed or mid-index, so a
caller reads a dead daemon as "nothing in the vault". The wrapper launches Obsidian,
retries while it loads, and exits 3 if it truly cannot reach the vault.

```
brain-search "peer validity"             # matching files
brain-search --context "peer validity"   # matching lines
```

Exit codes: 0 searched (a genuine miss prints "No matches found."), 3 vault unreachable.
On a 3, fall back to `grep -ril "<term>" ~/brain/agent-memory`.

## Capture so nothing is lost (the whole point)
Whenever a session establishes something durable — a preference, a decision about how I
work, an ongoing project/goal, or a **reference I shared (slides, docs, links)** that you'd
want in a DIFFERENT session weeks later — **write it to the brain**, using the `remember`
skill. Cross-repo recall only works if it lives in the brain, not the local project's
memory silo.
- **A fact about a PERSON goes in their note:** `~/brain/areas/People/<Name>.md` (create
  it from `templates/person.md` for anyone new). Write it there the moment you learn it;
  do not leave it in a project log or a session log where it cannot be found by name.
- **Route by kind:** operating facts / preferences / vision / active projects → **agent
  memory** (always-injected working set). References, clippings, meeting notes, and
  artifacts I'll cite later → **the vault** (`attachments/` or `sources/`), because the
  vault is the full-text searchable store; leave a short agent-memory pointer if it's
  important enough to stay top-of-mind.
- Default target = the brain, never a local project silo — unless it's strictly that
  repo's implementation detail and useless elsewhere.
- Capture proactively as facts arise; don't wait to be asked.
- **Keep Obsidian current.** Reflect durable work + knowledge into the vault as you go —
  file it and update the relevant project hub / session log / `INDEX.md`. Don't make me
  chase updates. (Still respect the write boundary below.)

## Indexing contract (why recall still works months later)
Every memory: `name` (kebab slug), `description:` (one line, written with the words a
future search would use — this is what makes recall work), `metadata.type`
(`user|feedback|project|reference`), body linking related memories with `[[slug]]`. Then
add ONE pointer line to `MEMORY.md`. Index stays one-line-per-memory; detail lives in the
files; search closes the gap. An unindexed memory is a lost memory.

## Write boundary — I author the vault, you don't
The vault's own notes are my thinking. Never inject your conclusions into them, and never
create "insight" notes in my voice. Your outputs go to the brain's `_generated/` or to
agent memory. Sanctioned agent writes: agent memory, `_generated/`, and filing to
`sources/` (meetings, clippings). When unsure, put it in memory or `_generated/` and tell
me where.

## Projects have folders in the brain — mirror your work there
Each code project has a folder in the vault: `~/brain/projects/<repo>/` (where `<repo>` is
the basename of the repo under `~/Developer`). It holds a hub note, a `sessions/`
subfolder, and that project's decisions/meetings/notes.

When you do substantive work in a repo under `~/Developer/<repo>` (and `<repo>` isn't the
brain itself), **log the session into its project folder** so it shows up in Obsidian
without me asking:
- Ensure `~/brain/projects/<repo>/<repo>.md` (the hub) exists; create it from the
  `project` template if missing. (The Stop hook does this automatically.)
- Append/update `~/brain/projects/<repo>/sessions/YYYY-MM-DD.md` with what changed,
  decisions made, and next steps — write below the auto-captured git snapshot; the hook
  preserves anything written there.
- File project-scoped `capture-decision` / `extract-meeting` output into that project
  folder rather than the vault root.
Keep it factual and concise; this is a work log, not authored thinking.

## Agent memory is also visible in Obsidian
The agent memory is surfaced in the vault at `~/brain/agent-memory/` (a symlink to the
canonical store). You still read/write it at its canonical path (`<memory-dir>/`);
Obsidian just mirrors it so I can see it.

## Skills
My reusable skills live in the brain (`~/brain/.claude/skills/`) and are symlinked into
`~/.claude/skills/` so they work in every repo: `remember` (capture), `triage`,
`capture-decision`, `extract-meeting`, `weekly-review`, `init-project` (scaffold a new
project), `testing` (verify a change honestly), plus kepano's `obsidian-skills`. Prefer
them over ad-hoc work.

## Optional: one calendar for everything dated
Anything with a date/time that gets decided in ANY session (a deadline, an appointment,
a review) goes on one calendar, not in a repo-local plan. Undated to-dos go to one
central task list. Name both here if you use this rule.

---
name: remember
description: Persist a durable fact into the centralized brain memory with correct indexing. Use whenever a session establishes a preference, a decision about how the user works, an ongoing project/goal, or a reference the user shared (slides/docs/links) that should be recallable from any future session or repo. Also runs as the capture step of auto-capture. Writes to the brain memory, never a local project silo.
---

# Remember — capture to the brain

Persist something so ANY future session, in ANY repo, can recall it. The brain memory is
the single store the global bridge (`~/.claude/CLAUDE.md`) points every session at. This
skill is cwd-independent — it always targets the brain by absolute path.

Paths below use `$BRAIN_DIR` (the vault, default `~/brain`) and `$BRAIN_MEMORY_DIR`
(the agent memory, default `~/.claude/projects/<vault-path-with-dashes>/memory/`, which
the vault mirrors at `$BRAIN_DIR/agent-memory`). Resolve them to absolute paths.

## Where things go — two stores, route deliberately
- **Agent memory** (operating facts / preferences / vision / active projects):
  `$BRAIN_MEMORY_DIR/`. Index: `MEMORY.md`. One `.md` file per fact. This is the
  always-injected working set, so keep it small and curated.
- **The vault** (references, clippings, meetings, artifacts the user will cite later):
  `$BRAIN_DIR/` — save the artifact under `attachments/` or a clipping under
  `sources/clippings/`. The vault is full-text searchable (`brain-search`), so long-tail
  "find it months later" content lives here. Leave a short agent-memory pointer if it
  should also stay top-of-mind.
- **A fact about a person** goes in their note: `$BRAIN_DIR/areas/People/<Name>.md`
  (create it from `templates/person.md` if missing), not in a session log.

## Procedure
1. **Decide it's worth remembering.** Durable = true across sessions: a preference, a
   decision about how the user works, an ongoing project/goal, a reference they'll cite
   later. Skip one-off task trivia and anything derivable from the repo/git.
2. **Dedup first.** `grep -ril "<topic>"` the memory dir and scan `MEMORY.md`. If a file
   already covers it, UPDATE that file — don't add a duplicate. Delete memories proven
   wrong.
3. **Write the memory file** `<kebab-slug>.md`:
   ```
   ---
   name: <kebab-slug>
   description: <one line — the retrieval hook. Use the words a future search would use.
                This single field is what makes recall work months later.>
   metadata:
     type: user | feedback | project | reference
   ---
   <the fact. For feedback/project, add **Why:** and **How to apply:** lines.
    Link related memories with [[their-slug]] — liberally; a link to a not-yet-written
    memory is fine.>
   ```
4. **Index it in the same edit.** Add ONE line to `MEMORY.md` under the right section:
   `- [Title](file.md) — hook`. Keep it to one line; detail stays in the file.
5. **For a shared reference:** save the artifact into the brain first (see "Where things
   go"), record its vault path in the memory body, and make the `description:` name both
   the topic AND the format — e.g. "slides from the 2026-03-02 talk on agent skills".
6. **Report** what you saved and where, in one line.

## Indexing contract — do not skip
- `description:` is the most important field. Specific, keyword-rich, matches how the
  user would later refer to it.
- Prefer many small single-fact files over one sprawling note.
- Every new memory gets its `MEMORY.md` pointer in the same edit. An unindexed memory is
  a lost memory.
- Convert relative dates to absolute (`YYYY-MM-DD`) before saving.

## Hard rules
- Default target is the BRAIN, never the local project's memory silo — cross-repo recall
  depends on it.
- Respect the write boundary: facts about the user and their system go to agent memory;
  their shared artifacts go to `attachments/` or `sources/`. Never author conclusions
  into their vault notes.

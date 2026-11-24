---
name: init-project
description: Scaffold a new project the way the user works — ask scripted setup questions, create the repo under $DEV_DIR with their stack, seed PRODUCT.md/CLAUDE.md/DESIGN.md, and register a project hub in the brain. Use when the user says "new project", "start a project", "init project", or "scaffold <name>".
---

# init-project — scaffold a new project

Turn "I want to build X" into a ready repo + a brain project home, using the user's stack
and conventions. First read `stack.md` and `profile.md` from the brain (`$BRAIN_DIR`,
default `~/brain`) so the scaffold matches how they actually work. If those notes don't
exist yet, ask for the stack and offer to save the answer with the `remember` skill.

## Step 1 — ask the scripted questions (batch them; skip anything already answered)
- **Name** — becomes the repo dir `$DEV_DIR/<name>` (default `~/Developer/<name>`) and
  the brain hub name.
- **One-liner** — what it is / who it's for (goes in PRODUCT.md).
- **Type** — throwaway experiment vs. real product (sets how much to scaffold).
- **Stack** — default from `stack.md` (e.g. a quick default for experiments and a
  heavier one for products). Confirm or override.
- **Hosting** — default from `stack.md`.
- **Persisted data** — none / SQLite (files-first) / Postgres.
Confirm the whole set in ONE message before creating anything. Don't re-ask.

## Step 2 — create the repo
- `mkdir -p $DEV_DIR/<name>`, `cd`, `git init`.
- Scaffold per stack (package.json, tooling config, `src/`, a minimal running entry).
  Prefer small composable modules over frameworks-for-everything.
- Seed the source-of-truth docs:
  - `PRODUCT.md` — the one-liner, goal, who it's for. **Stub only** — a planning pass
    deepens it into the real brief. Don't over-write it here.
  - `DESIGN.md` — only if it has UI. **Stub only**.
  - `CLAUDE.md` — project manual; note it inherits the brain (global bridge) and point at
    `PRODUCT.md` / `DESIGN.md` as canonical.
  - `README.md`.

## Step 3 — register it in the brain
- Create the hub `projects/<name>/<name>.md` from `templates/project.md` (type: project,
  status: active, category `"[[Projects]]"`) via the Obsidian CLI, or let the
  session-log hook create it on the first session.
- Add a one-line entry under Active projects in the brain `INDEX.md` — keep INDEX current.

## Step 4 — hand off to planning
- Scaffold only stubs the docs. Offer the next step: "Scaffold's done — want me to turn
  these stubs into a real brief (and a design system, if it has UI) before we build?"
  Proceed if the user says yes.

## Step 5 — verify (don't call it done until it is)
- Install deps and run the typecheck / dev build. "Done" = it builds and typechecks, not
  "looks right". Follow the `testing` skill. Report what passed.

## Hard rules
- Match `stack.md` unless the user overrides; note tradeoffs briefly, don't lecture.
- Prefer boring, durable choices for anything meant to last.
- The repo's content is the user's to author — scaffold the structure and seed docs,
  don't over-write.

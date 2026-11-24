---
name: testing
description: >-
  The protocol to follow EVERY time you verify a code change — reference it before
  claiming anything works/is done/is fixed, and whenever the user says "test this",
  "verify it", "does it work", "is it done", "make sure it's solid". Its job is to
  keep verification honest AND proportional: it sizes the change (trivial → small →
  standard → deep) and applies only as much rigor as that size warrants, so a
  one-line tweak gets a quick check and a big/risky feature gets the deep protocol
  (references/deep-protocol.md) — never over-testing a trivial edit, never
  under-testing something substantial. Encodes the foolproof rules that catch the
  bugs a green build misses. Use it proactively the moment you finish implementing
  something; don't skip it, and don't reinvent an ad-hoc process each time.
---

# Testing protocol

The purpose of this skill is to make verification **honest** and **proportional**.
Honest: what you test must be the exact thing the user runs, and you say plainly what
is and isn't covered. Proportional: effort scales to the change, so you neither burn
time bulletproofing a typo nor wave through a risky feature with a glance.

Follow the always-rules below at every tier, then size the change and do that tier.

## The always-rules (they catch what a green build hides)

1. **Verify the real code path — not a proxy.** The thing you assert on must be the
   thing the user actually hits. A stand-in check gives false confidence: a login was
   once "verified" by calling the API function directly, which passed — while the real
   UI login hung on a step the proxy never ran. If you can't exercise the real path,
   say so.
2. **Compiling is necessary, not sufficient.** A clean typecheck/build means the types
   line up, not that the behavior is right. Never report "done" off a build alone.
3. **Extend coverage to the new behavior.** Running only pre-existing checks does not
   test what you just added. New behavior → add a check that would fail if it broke.
4. **Calibrate expectations to reality.** Before asserting a number/threshold, observe
   the actual output once, then assert with margin. A check that false-fails on correct
   code is worse than no check — it trains you to ignore red.
5. **Reproduce before you claim.** Reproduce the failure (or the working state) in a
   controlled place — a test, a simulator, a scratch script — before saying it's fixed
   or broken. Don't diagnose from a distance.
6. **State coverage honestly, and under-claim.** "Sim-verified, not device-verified."
   "Login covered; the settings screen isn't." Precise scope beats a confident "works".
7. **A flaky check is worse than none.** If it fails intermittently on correct code,
   stabilize it (prove it green several runs) or quarantine it out of the gate — and
   say you did. A gate you don't trust is a gate you'll bypass.

## Size the change → pick the tier

Judge by blast radius and reversibility, not line count.

- **Trivial** — comments, copy, docs, formatting, a constant with no logic downstream.
  → No run needed. Re-read the diff; at most a typecheck. Don't spend more.
- **Small** — a localized change to one function/component, low blast radius (a prop, a
  style, one pure helper, a copy string that feeds logic).
  → Typecheck/build + run the ONE directly-relevant existing check. Eyeball it if it's
  visual. Rules 1–2 apply.
- **Standard** — a normal feature or bug fix touching one subsystem (a new setting, a
  chart, an endpoint, a fix with an identified root cause).
  → Run the relevant project gates, **add one check that covers the new behavior**
  (rule 3), and reproduce the fix (rule 5). Most work lands here.
- **Deep** — a big feature, a cross-file refactor, or anything touching
  correctness-critical / safety / security / auth / data-integrity / money / migrations
  — or when the user says "bulletproof", "thoroughly", "make sure this is right".
  → **Read `references/deep-protocol.md` and follow it.** This is where adversarial
  testing, edge/failure injection, cross-layer coverage, and a written coverage report
  earn their keep.

When unsure between two tiers, take the higher one — but only its steps, not infinite
gold-plating.

## Find and run the project's gates

Don't guess the commands — discover them, then run the ones relevant to what you
changed:

- `package.json` scripts (`test`, `lint`, `typecheck`, `build`, `e2e`), a `Makefile`,
  `pyproject.toml`/`tox.ini`, CI config in `.github/workflows/`, and a `scripts/` or
  `test/`/`tests/` directory.
- Run the gates that exercise your change; skip the irrelevant ones (proportionality).
- If a subsystem has no gate yet and the change is standard+, add the smallest real one
  (rule 3) rather than shipping it uncovered.

**Project-specific gates live with the project.** If a repo has its own verification
skill or a `scripts/verify-*` script, that is the authority for its exact commands and
gotchas. Consult it before inventing your own.

## After verifying

Report the result with honest scope (rule 6). Only then call it done — landing tested
work and updating the tracker follow from there, not before.

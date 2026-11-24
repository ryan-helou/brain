# Deep verification protocol

Use this for big features, cross-file refactors, and anything correctness-critical,
safety-, security-, auth-, data-, money-, or migration-related — or when the user asks
for "bulletproof" / "thorough". The always-rules from SKILL.md still hold; this adds the
depth. Do the steps that fit the change; don't perform rigor theater on parts the change
doesn't touch.

## 1. Map the surface before you test

List what the change can affect: the entry points a user reaches it through, the
functions/modules it touches, the data it reads/writes, the other features that share
that code or state. You test the map, not just the happy path you had in mind. A change
that "only touched X" but X is imported by five screens has a five-screen surface.

## 2. Cover the layers that apply

Pick the layers the change actually spans — each catches what the others miss:

- **Logic / unit** — pure functions and core algorithms. Deterministic, fast, no I/O.
  Assert invariants (properties that must always hold), not just one example. This is
  the cheapest, highest-leverage layer for correctness-critical code.
- **Integration** — the units wired together with real adjacent systems (a real DB, the
  real API, the real store), exercising the actual seams where bugs hide.
- **End-to-end / UI** — drive the real interface the user drives, on the real runtime.
  Assert the user-visible outcome, not internal state.
- **Contract** — if the change crosses a boundary (API shape, event schema, file
  format), assert the shape both sides depend on.

## 3. Test the unhappy paths (this is where deep pays off)

The happy path usually works; bugs live at the edges. Add:

- **Boundaries** — empty, zero, one, max, huge, negative, missing/undefined, very long
  strings, unicode, duplicates, timezone/DST and week/month boundaries for dates.
- **Adversarial input** — malformed, hostile, or nonsensical input; assert it's rejected
  or handled, never silently corrupts.
- **Failure injection** — the network is offline / slow / returns 500; a dependency
  times out or throws; the disk/keychain/permission is denied; a write half-completes.
  Assert the code degrades honestly (a readable error, a safe fallback) instead of
  hanging or corrupting. Many real hangs and data losses only appear here.
- **Concurrency / ordering** — double-submit, rapid repeat, out-of-order responses,
  interruption mid-flow (backgrounded, killed, reloaded), stale cache. Assert no lost
  update, no duplicate, no deadlock.
- **Idempotency / determinism** — running twice yields the same result (or a correctly
  different one); the same input always produces the same output.

## 4. Guard against regressions

Before assuming your change is isolated, run the existing suite for the surrounding
subsystem. If the change fixes a specific bug, add a check that reproduces that exact bug
and now passes — so it can never silently return.

## 5. Visual / UX review (for anything user-facing)

Beyond "the right text is present", look at the actual rendered result — layout,
alignment, overflow/cut-off text, broken images, contrast, empty and error states, and
whether it looks shipped or broken. Capture screenshots so this is repeatable. A vision
model reviewing screenshots against a rubric approximates the human eye and never tires;
use it as a gate where available.

## 6. Performance & scale (when the change could regress them)

If the change touches a hot path, large data, or a tight loop: measure before/after on a
realistic input size, and assert it didn't regress past a threshold. Watch for
accidental O(n²), N+1 queries, and unbounded memory.

## 7. Write the coverage report

Close with an honest, explicit account — this is what makes "done" trustworthy:

- **Covered:** the layers/cases you exercised and their result (green).
- **Not covered:** what you deliberately or unavoidably left (e.g. "real-device sensors
  — simulator only", "load past 10k rows untested").
- **Residual risk:** the most likely place a bug still hides, so the reader knows where
  to look if something breaks.

Under-claim. "Thoroughly tested" without this report is a vibe, not verification.

## Scaling rigor to the stakes

Not every deep change needs every section. A UI-heavy feature leans on layers 2/3/5; a
core-logic or money/auth change leans on 1/3/4 and a full coverage report; a
performance change centers on 6. Match the depth to where a bug would actually hurt, and
to how reversible the change is. The user asked for depth, not ceremony — spend it where
the risk is.

## Project specifics

When a project already has layered gates (a test suite, a simulator E2E script, a gated
release script), use them as the layers above rather than rebuilding them. Real-hardware
coverage is usually a separate, later tier; name it in the coverage report when it was
not exercised.

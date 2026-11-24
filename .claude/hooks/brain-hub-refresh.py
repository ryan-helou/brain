#!/usr/bin/env python3
"""Keep the vault's hub notes current.

Called by brain-session-log.sh after a session log is written. Jobs:

  1. refresh the auto block in projects/<proj>/<proj>.md
  2. regenerate the roster in Projects.md across EVERY project folder
  3. regenerate the thin map in INDEX.md
  4. refresh each area note listed in categories.json (areas/<Area>/<Note>.md)

Everything outside the brain:auto markers is yours and is copied through
untouched, so this can run on every session without eating your writing.

Config (env):
  BRAIN_DIR         vault folder on disk           (default: ~/brain)
  DEV_DIR           folder that holds your repos   (default: ~/Developer)
  BRAIN_MEMORY_DIR  agent memory folder            (default: $BRAIN_DIR/agent-memory,
                                                    the symlink to Claude Code's store)

Usage:
  brain-hub-refresh.py <project>   refresh one project hub + the shared notes
  brain-hub-refresh.py --all       refresh every project hub + the shared notes
"""
import json, os, re, subprocess, sys
from datetime import date
from pathlib import Path

BRAIN = Path(os.environ.get("BRAIN_DIR", "~/brain")).expanduser()
DEV = Path(os.environ.get("DEV_DIR", "~/Developer")).expanduser()
MEMORY = Path(os.environ.get("BRAIN_MEMORY_DIR", str(BRAIN / "agent-memory"))).expanduser()
AREAS_DIR = BRAIN / "areas"
START, END = "<!-- brain:auto:start -->", "<!-- brain:auto:end -->"
NOTE = "_Auto-maintained. Anything outside this block is yours and is never rewritten._"


def splice(text, block):
    """Replace the auto block, or append one if the note has none."""
    if START in text and END in text:
        return re.sub(re.escape(START) + r".*?" + re.escape(END),
                      lambda _: f"{START}\n{block}\n{END}", text, flags=re.S)
    return text.rstrip() + f"\n\n{START}\n{block}\n{END}\n"


def touch_frontmatter(text, today):
    """Keep `updated:` honest without disturbing the rest of the frontmatter."""
    if not text.startswith("---"):
        return text
    head, sep, tail = text[3:].partition("\n---")
    if not sep:
        return text
    if re.search(r"^updated:", head, flags=re.M):
        head = re.sub(r"^updated:.*$", f"updated: {today}", head, count=1, flags=re.M)
    else:
        head = head.rstrip() + f"\nupdated: {today}\n"
    return "---" + head + sep + tail


def write_if_changed(path, block, today, title):
    """Splice `block` into `path`, creating a minimal note if it does not exist yet."""
    if path.exists():
        original = path.read_text()
    else:
        original = (f"---\ntype: note\ntitle: {title}\ncreated: {today}\nupdated: {today}\n"
                    f"agent_load: high\n---\n\n# {title}\n")
    out = touch_frontmatter(splice(original, block), today)
    if not path.exists() or out != original:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(out)


def project_dirs():
    root = BRAIN / "projects"
    return sorted(d for d in root.iterdir() if d.is_dir()) if root.is_dir() else []


def sessions(proj_dir):
    d = proj_dir / "sessions"
    if not d.is_dir():
        return []
    return sorted((p.stem for p in d.glob("*.md") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.stem)),
                  reverse=True)


def git_line(repo):
    if not (repo / ".git").exists():
        return "not a git repo"
    def g(*a):
        r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else ""
    branch, last = g("rev-parse", "--abbrev-ref", "HEAD"), g("log", "-1", "--pretty=%h %s")
    dirty = len([l for l in g("status", "--porcelain").splitlines() if l])
    bits = [f"`{branch}`" if branch else "", f"{last}" if last else ""]
    if dirty:
        bits.append(f"**{dirty} uncommitted**")
    return " — ".join(b for b in bits if b) or "no commits"


def has_narrative(proj_dir, stem):
    """True when a session log carries real writing, not just the git snapshot."""
    f = proj_dir / "sessions" / f"{stem}.md"
    try:
        body = f.read_text()
    except OSError:
        return False
    tail = body.split("**Uncommitted changes:**", 1)[-1]
    return any(l.strip() and not l.lstrip().startswith("- ") for l in tail.splitlines()[1:])


def refresh_hub(proj, today):
    pdir = BRAIN / "projects" / proj
    hub = pdir / f"{proj}.md"
    if not hub.exists():
        return
    logs = sessions(pdir)
    links = " · ".join(f"[[projects/{proj}/sessions/{s}|{s}]]" for s in logs[:5]) or "none yet"
    written = sum(1 for s in logs if has_narrative(pdir, s))
    lines = [
        NOTE, "",
        f"- **Path:** `{DEV / proj}`",
        f"- **Last active:** {logs[0] if logs else 'unknown'}",
        f"- **Repo:** {git_line(DEV / proj)}",
        f"- **Sessions logged:** {len(logs)} ({written} with written narrative)",
        "", f"**Recent sessions:** {links}",
    ]
    write_if_changed(hub, "\n".join(lines), today, proj)


def refresh_roster(today):
    """Projects.md becomes the live roster, newest activity first."""
    rows = []
    for pdir in project_dirs():
        proj, logs = pdir.name, sessions(pdir)
        rows.append((logs[0] if logs else "0000-00-00", proj, len(logs),
                     sum(1 for s in logs if has_narrative(pdir, s))))
    rows.sort(reverse=True)
    body = [NOTE, "",
            f"{len(rows)} project folders, most recently active first.", "",
            "| Project | Last active | Sessions | With narrative |",
            "|---|---|---|---|"]
    for last, proj, n, w in rows:
        shown = last if last != "0000-00-00" else "—"
        flag = f"{w}" if w else "**0**"
        body.append(f"| [[projects/{proj}/{proj}\\|{proj}]] | {shown} | {n} | {flag} |")
    body += ["", "A **0** in the last column means the hook logged the days but no session "
                 "ever wrote down what happened."]
    write_if_changed(BRAIN / "Projects.md", "\n".join(body), today, "Projects")


def memory_files():
    if not MEMORY.is_dir():
        return []
    return sorted(f for f in MEMORY.glob("*.md") if f.name != "MEMORY.md")


def description(f):
    for line in f.read_text().splitlines():
        if line.startswith("description:"):
            d = line.split(":", 1)[1].strip()
            return (d[:105] + "...") if len(d) > 105 else d
    return ""


def load_categories():
    """The area notes, defined in categories.json beside this script."""
    f = Path(__file__).resolve().parent / "categories.json"
    return json.loads(f.read_text()) if f.exists() else {}


def category_note(name, spec, today):
    """Refresh areas/<name>.md with its projects and the memories whose slug matches."""
    note = AREAS_DIR / f"{name}.md"
    if not note.exists():
        return
    rx = re.compile("|".join(spec["patterns"])) if spec.get("patterns") else None
    rows = []
    for proj in spec.get("projects", []):
        pdir = BRAIN / "projects" / proj
        if pdir.is_dir():
            logs = sessions(pdir)
            rows.append((logs[0] if logs else "0000-00-00", proj, logs[0] if logs else None))
    rows.sort(reverse=True)
    mems = [(f.stem, description(f)) for f in memory_files() if rx and rx.search(f.stem)]
    b = [NOTE, ""]
    if rows:
        b += ["### Projects", "", "| Project | Last active |", "|---|---|"]
        for last, proj, log in rows:
            b.append(rf"| [[projects/{proj}/{proj}\|{proj}]] | {last if log else '—'} |")
        b.append("")
    if mems:
        b += [f"### What the brain knows ({len(mems)})", ""]
        b += [rf"- [[agent-memory/{n}\|{n}]] — {d}" for n, d in mems]
        b.append("")
    if not rows and not mems:
        b.append("_Nothing filed here yet._")
    b.append(f"_Refreshed {today}._")
    write_if_changed(note, "\n".join(b), today, Path(name).name)


def refresh_index(today):
    """INDEX stays a thin map. The detail lives in the hub each thing belongs to."""
    rows = []
    for pdir in project_dirs():
        logs = sessions(pdir)
        rows.append((logs[0] if logs else "0000-00-00", pdir.name, logs[0] if logs else None))
    rows.sort(reverse=True)
    n_mem = len(memory_files())

    active = " · ".join(rf"[[projects/{p}/{p}\|{p}]]" for _, p, l in rows[:6] if l) or "—"
    b = [NOTE, "", "| Area | Notes inside |", "|---|---|"]
    if AREAS_DIR.is_dir():
        for area in sorted(d.name for d in AREAS_DIR.iterdir() if d.is_dir()):
            notes = sorted(x.stem for x in (AREAS_DIR / area).glob("*.md"))
            b.append(f"| **{area}** | " +
                     " · ".join(rf"[[areas/{area}/{n}\|{n}]]" for n in notes) + " |")
    b += ["", rf"| [[Projects]] | all {len(rows)} projects |",
          rf"| [[agent-memory/MEMORY\|MEMORY]] | all {n_mem} raw memories |",
          "", f"**Moving right now:** {active}", "", f"_Refreshed {today}._"]
    write_if_changed(BRAIN / "INDEX.md", "\n".join(b), today, "INDEX")


if __name__ == "__main__":
    today = date.today().isoformat()
    if len(sys.argv) > 1 and sys.argv[1] != "--all":
        refresh_hub(sys.argv[1], today)
    else:
        for d in project_dirs():
            refresh_hub(d.name, today)
    refresh_roster(today)
    refresh_index(today)
    for c, spec in load_categories().items():
        category_note(c, spec, today)

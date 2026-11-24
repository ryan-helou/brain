#!/usr/bin/env bash
# Stop hook: mirror every Claude Code session that happens in a project under $DEV_DIR
# into the vault, at projects/<repo>/sessions/YYYY-MM-DD.md, and keep the hub notes fresh.
#
# Install: register under "Stop" in ~/.claude/settings.json (see settings.example.json).
#
# Config (env):
#   BRAIN_DIR        vault folder on disk                       (default: ~/brain)
#   DEV_DIR          folder that holds your code repos           (default: ~/Developer)
#   BRAIN_AUTO_PUSH  1 = push the vault after the auto-commit    (default: 0)
#
# Opt out per project: put an empty `.no-brain-log` file in the repo root.
set -uo pipefail
BRAIN="${BRAIN_DIR:-$HOME/brain}"; DEV="${DEV_DIR:-$HOME/Developer}"
BRAIN_NAME="$(basename "$BRAIN")"
INPUT="$(cat 2>/dev/null || true)"
CWD="$(printf '%s' "$INPUT" | python3 -c 'import sys,json
try: print(json.load(sys.stdin).get("cwd",""))
except Exception: print("")' 2>/dev/null)"
[ -z "$CWD" ] && CWD="$PWD"
case "$CWD" in "$DEV"/*) : ;; *) exit 0 ;; esac
REL="${CWD#"$DEV"/}"; PROJ="${REL%%/*}"   # top-level project under $DEV_DIR, not nested basename
[ "$PROJ" = "$BRAIN_NAME" ] && exit 0; [ -z "$PROJ" ] && exit 0
# opt-out: a project containing .no-brain-log is never logged to the vault
[ -e "$DEV/$PROJ/.no-brain-log" ] && exit 0
PDIR="$BRAIN/projects/$PROJ"; SDIR="$PDIR/sessions"; mkdir -p "$SDIR"
TODAY="$(date +%F)"; NOW="$(date +%H:%M)"; HUB="$PDIR/$PROJ.md"; LOG="$SDIR/$TODAY.md"
if [ ! -f "$HUB" ]; then cat > "$HUB" <<EOF
---
type: project
title: $PROJ
category: "[[Projects]]"
status: active
created: $TODAY
updated: $TODAY
agent_load: medium
tags: [Project]
---

# $PROJ

Project hub for \`$DEV/$PROJ\`. Auto-created by the brain session-log hook.
Session logs are in \`sessions/\`.
EOF
fi
if git -C "$CWD" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  BRANCH="$(git -C "$CWD" rev-parse --abbrev-ref HEAD 2>/dev/null)"
  LASTC="$(git -C "$CWD" log -1 --pretty='%h %s' 2>/dev/null)"
  CHANGES="$(git -C "$CWD" status --porcelain 2>/dev/null | sed 's/^/  - /')"
  [ -z "$CHANGES" ] && CHANGES="  - (working tree clean)"
else BRANCH="(not a git repo)"; LASTC="—"; CHANGES="  - (no git)"; fi
NEW="$(cat <<EOF
---
type: session-log
project: "[[$PROJ]]"
date: $TODAY
updated: $TODAY
agent_load: low
tags: [SessionLog]
---

# $PROJ — session log $TODAY

Auto-captured snapshot of work in \`$DEV/$PROJ\`. The agent adds decisions and
narrative below this line when a session is substantive.

- **Last active:** $NOW
- **Branch:** $BRANCH
- **Last commit:** $LASTC
- **Uncommitted changes:**
$CHANGES
EOF
)"
# Anything the agent wrote below the snapshot block is narrative — carry it over
# verbatim instead of rewriting the whole file from the template.
NARR=""
if [ -f "$LOG" ]; then
  NARR="$(awk '
    fm < 2   { if ($0 == "---") fm++; next }
    !uc      { if ($0 ~ /^- \*\*Uncommitted changes:\*\*/) uc = 1; next }
    uc && !n { if ($0 ~ /^  - / || $0 ~ /^[[:space:]]*$/) next; n = 1 }
    n        { print }
  ' "$LOG")"
fi
CAND="$NEW"
[ -n "$NARR" ] && CAND="$(printf '%s\n\n%s' "$NEW" "$NARR")"
strip() { grep -v '^- \*\*Last active:\*\*' 2>/dev/null; }
if [ -f "$LOG" ] && [ "$(printf '%s' "$CAND" | strip)" = "$(strip < "$LOG")" ]; then LOG_CHANGED=0; else
  printf '%s\n' "$CAND" > "$LOG"; LOG_CHANGED=1; fi

# Hub notes are refreshed on EVERY session end, not only when the log changed:
# this project's hub, the vault-wide roster in Projects.md, INDEX.md, and area notes.
BRAIN_DIR="$BRAIN" DEV_DIR="$DEV" python3 "$BRAIN/.claude/hooks/brain-hub-refresh.py" "$PROJ" >/dev/null 2>&1
# Session logs must not sit uncommitted: commit just these files (and the regenerated
# hub notes), optionally push in the background.
if git -C "$BRAIN" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  VAULT_NOTES=("$BRAIN"/*.md)
  [ -d "$BRAIN/areas" ] && VAULT_NOTES+=("$BRAIN/areas")
  git -C "$BRAIN" add -- "$HUB" "$LOG" "${VAULT_NOTES[@]}" >/dev/null 2>&1
  git -C "$BRAIN" commit --quiet -m "session log: $PROJ $TODAY $NOW (auto)" -- "$HUB" "$LOG" "${VAULT_NOTES[@]}" >/dev/null 2>&1
  [ "${BRAIN_AUTO_PUSH:-0}" = "1" ] && (git -C "$BRAIN" push --quiet >/dev/null 2>&1 &)
fi
exit 0

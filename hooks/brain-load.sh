#!/usr/bin/env bash
# SessionStart hook: inject the brain's agent-memory index into every session, in every
# repo. stdout from a SessionStart hook is added to the session context.
#
# Install: copy to ~/.claude/hooks/brain-load.sh and register it under "SessionStart"
# in ~/.claude/settings.json (see settings.example.json).
#
# Config (env):
#   BRAIN_DIR         vault folder on disk                    (default: ~/brain)
#   BRAIN_MEMORY_DIR  agent memory folder                     (default: Claude Code's
#                     project memory dir for $BRAIN_DIR, i.e.
#                     ~/.claude/projects/<path-with-dashes>/memory)
set -euo pipefail

BRAIN="${BRAIN_DIR:-$HOME/brain}"
SLUG="$(printf '%s' "$BRAIN" | sed 's#[^A-Za-z0-9]#-#g')"
MEM_DIR="${BRAIN_MEMORY_DIR:-$HOME/.claude/projects/$SLUG/memory}"
MEM="$MEM_DIR/MEMORY.md"

echo "=== Centralized brain — memory index (auto-loaded every session) ==="
echo "Durable memory + skills live in the brain. This index is the map; detail lives in"
echo "the referenced files. To recall detail, read the file under the memory dir"
echo "($MEM_DIR), or search the vault (works from any directory):"
echo "  brain-search --context \"...\""
echo "Save new durable facts here too — use the 'remember' skill. Current index:"
echo
if [ -f "$MEM" ]; then
  cat "$MEM"
else
  echo "(no brain memory index found at $MEM)"
fi

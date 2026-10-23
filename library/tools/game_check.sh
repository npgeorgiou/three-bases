#!/bin/sh
# Fast check of one game's pattern edits, without the full build: the build's steps (build.sh --steps) on a copy that holds only
# that game (only_games.py split, cached until the library changes), then signature.py, and the game's measures: mechanics
# coverage, key score, real-world cases, regression lines and combo misses of that game. Seconds instead of a full reload; use it for every try while working on a game,
# and run reload_game.sh + compare_builds.py once at the end, before the commit. Usage: game_check.sh <scratch dir> <game>
set -e
S=$(readlink -f "$1"); G="$2"; cd "$(dirname "$0")"; P="python3 -I"
B="$S/gc_${G}_base.sqlite"; O="$S/gc_$G.sqlite"
if [ ! -f "$B" ] || [ ../three-bases-library.sqlite -nt "$B" ]; then
  cp ../three-bases-library.sqlite "$S/gc_full.sqlite"; $P indexes.py "$S/gc_full.sqlite" create >/dev/null
  $P compact_text.py "$S/gc_full.sqlite" expand >/dev/null; rm -f "$B"; $P only_games.py split "$S/gc_full.sqlite" "$B" "$G" >/dev/null; rm -f "$S/gc_full.sqlite"
fi
rm -f "$O.steps.tsv"; cp "$B" "$O"; sh build.sh --steps "$O" > "$S/gc_$G.log" 2>&1 || { tail -5 "$S/gc_$G.log"; exit 1; }
$P signature.py "$O" >/dev/null
$P coverage.py "$O" "$G" 0 --mechanics "games/$G.md"
$P key/key.py score "$O" "$G" | grep "^$G "
$P realworld.py "$O" 2>/dev/null | grep -i "$G" || true
$P regression.py "$O" check 2>/dev/null | grep " $G " > "$S/gc_${G}_regression.txt" || true
echo "regression: $(wc -l < "$S/gc_${G}_regression.txt") fails for $G (lines in $S/gc_${G}_regression.txt)"
$P combo_check.py "$O" 2>/dev/null | grep "^  MISS $G:" | grep -v "card not in library" || true
echo "db: $O   step log: $O.steps.tsv (per step, game, concept: count before, after; a gain has after > before)"

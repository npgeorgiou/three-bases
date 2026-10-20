#!/bin/sh
# Reload games with today's patterns and steps, keeping every entry's id (export_game.py). Usage: reload_game.sh <scratch dir> <game> [...]
# Writes <scratch>/reloaded.sqlite; compare it with the library (realworld.py, final_compare.py, regression) before copying it over.
set -e
S=$(readlink -f "$1"); shift; cd "$(dirname "$0")"; P="python3 -I"
cp ../three-bases-library.sqlite "$S/reload_in.sqlite"; $P compact_text.py "$S/reload_in.sqlite" expand >/dev/null
L=""
for g in "$@"; do $P export_game.py "$S/reload_in.sqlite" "$g" "$S/reload_$g"; $P drop_game.py "$S/reload_in.sqlite" "$g" --reload; L="$L $g=$S/reload_${g}_kw.json $g=$S/reload_$g.json"; done
$P compact_text.py "$S/reload_in.sqlite" compact >/dev/null
sh build.sh "$S/reload_in.sqlite" "$S/reloaded.sqlite" $L

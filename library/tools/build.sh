#!/bin/sh
# Incremental build. The raw corpus of the first build is gone and not needed: three-bases-library.sqlite is the base for all work.
# One-time loads (Marvel Snap, Underworlds warscrolls, Runeterra, Hearthstone and Battlegrounds created cards, the Oct 2026 loads)
# are already in the database; their scripts and data files are removed. One-time fixes of 12 Oct 2026 are in tools/fixes/ (f01-f12);
# the idempotent ones (f03, f05, f07) are also build steps.
# Usage: build.sh <in.sqlite> <out.sqlite> [<game>=<cards.json> ...]
#   Without loads: runs every step below on a copy of <in> (tags, links and pairs are re-derived for all entries).
#   With loads: each JSON (made by a converter in convert/, format in load_cards.py) is loaded into the copy first. The steps also
#   run on a second copy without the loads, and keep_old.py then keeps every older entry as it was in <in>, apart from what the
#   loads change (merges, links to new cards). A pattern-file change reaches older entries only through a run without loads.
#   Any failed check stops the build.
set -e
[ $# -ge 2 ] || { echo "usage: build.sh <in.sqlite> <out.sqlite> [<game>=<cards.json> ...]"; exit 2; }
IN=$(readlink -f "$1"); OUT=$(readlink -f "$2"); shift 2
cd "$(dirname "$0")"
P="python3 -I"
steps() {   # $1 = db
  D="$1"
  $P compact_text.py "$D" expand
  $P concept_tree.py "$D" restore
  $P concept_defs.py "$D"
  $P game_patterns.py "$D" patterns
  $P drop_untagged.py "$D"
  $P fix_grants.py "$D"
  $P fixes/f03_grant_not_does.py "$D"
  for f in reviews/*.json; do g=$(basename "$f" .json); $P apply_review.py "$D" "$g" "$f" old; done
  $P kw_sync.py "$D" wh_bloodbowl3 wh_killteam wh_40k_10e h:mtg h:hearthstone h:hs_battlegrounds h:shadowverse h:runeterra h:gwent h:duelyst h:faeria h:inscryption h:into_the_breach h:wh_underworlds h:sts1 h:sts2 h:darkest_dungeon h:wh_aos_4th
  $P propagate.py "$D"
  $P keyword_defs.py "$D"
  $P outcome_tree.py "$D"
  for f in reviews_outcome/*.json; do g=$(basename "$f" .json); $P apply_review.py "$D" "$g" "$f" old; done
  $P condition_roles.py "$D"
  $P link_types.py "$D"
  $P engine_links.py "$D"
  $P design_problems.py "$D"
  $P trigger_pairs.py "$D"
  $P regression.py "$D" enforce
  $P concept_tree.py "$D" apply
  for f in reviews/*.json reviews_outcome/*.json; do g=$(basename "$f" .json); $P apply_review.py "$D" "$g" "$f" new; done   # reviews are in the new ids (fixes/f15)
  $P regression.py "$D" enforce_new
  $P relations_added.py "$D"
  $P pattern_fix.py "$D"
  $P kw_links.py "$D"
  $P trigger_pairs.py "$D" pairs_only   # again after the tree move: pairs for the tags added since (new patterns, key wins)
  $P parent_rule.py "$D"
  $P final_revert.py "$D"
  $P key_wins.py apply "$D"
  $P dedupe.py "$D"
  $P frequency.py "$D"
  $P fixes/f07_keywords_structure.py "$D"
  $P fixes/f05_factions.py "$D"
  $P distinct.py "$D"
}
rm -f "$OUT"; cp "$IN" "$OUT"
if [ $# -gt 0 ]; then
  BASE="$OUT.base"; rm -f "$BASE"; cp "$IN" "$BASE"
  steps "$BASE"
  for a in "$@"; do $P load_cards.py "$OUT" "${a%%=*}" "${a#*=}"; done
  steps "$OUT"
  INX="$OUT.in"; rm -f "$INX"; cp "$IN" "$INX"; $P compact_text.py "$INX" expand   # keep_old reads the text columns
  $P keep_old.py "$OUT" "$INX" "$BASE"; rm -f "$BASE" "$INX"
else
  steps "$OUT"
fi
$P signature.py "$OUT"
$P precision.py "$OUT"
$P finalize.py "$OUT"
$P regression.py "$OUT" check
$P combo_check.py "$OUT"
$P trigger_pairs.py "$OUT" check
$P realworld.py "$OUT"
$P compact_text.py "$OUT" compact
python3 -I -c "import sqlite3,sys; c=sqlite3.connect(sys.argv[1], isolation_level=None); c.execute(\"insert into entity_fts(entity_fts) values('integrity-check')\"); c.execute('vacuum'); print(c.execute('pragma integrity_check').fetchone())" "$OUT"
$P test_query.py "$OUT"

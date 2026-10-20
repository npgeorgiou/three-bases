#!/bin/sh
# Incremental build. The raw corpus of the first build is gone and not needed: three-bases-library.sqlite is the base for all work.
# One-time loads (Marvel Snap, Underworlds warscrolls, Runeterra, Hearthstone and Battlegrounds created cards, the Oct 2026 loads)
# are already in the database; their scripts and data files are removed. One-time fixes of 12 Oct 2026 are in tools/fixes/ (f01-f12);
# the idempotent ones (f03, f05, f07) are also build steps.
# Usage: build.sh <in.sqlite> <out.sqlite> [<game>=<cards.json> ...]
#   Without loads: runs every step below on a copy of <in> (tags, links and pairs are re-derived for all entries).
#   With loads: insert-only (add_games.py). The new games are loaded into a work copy that holds no other game, the steps run
#   there, and only the new games' rows are inserted into the library; the build stops if any existing row changed. To reload
#   a game, drop it first (drop_game.py). A pattern-file change reaches older entries only through a run without loads.
#   Any failed check stops the build.
set -e
[ $# -ge 2 ] || { echo "usage: build.sh <in.sqlite> <out.sqlite> [<game>=<cards.json> ...]"; exit 2; }
IN=$(readlink -f "$1"); OUT=$(readlink -f "$2"); shift 2
LOADS=""; for a in "$@"; do LOADS="$LOADS ${a%%=*}=$(readlink -f "${a#*=}")"; done; set -- $LOADS   # load paths relative to the caller
cd "$(dirname "$0")"
P="python3 -I"
steps() {   # $1 = db
  D="$1"
  run() { $P "$@"; $P step_log.py "$D" "$(echo "$*" | sed "s#$D##")"; }   # each step, then what it removed (step_log.py)
  run compact_text.py "$D" expand
  run concept_tree.py "$D" restore
  run concept_defs.py "$D"
  run game_patterns.py "$D" patterns
  run drop_untagged.py "$D"
  run fix_grants.py "$D"
  run fixes/f03_grant_not_does.py "$D"
  for f in reviews/*.json; do g=$(basename "$f" .json); run apply_review.py "$D" "$g" "$f" old; done
  run kw_sync.py "$D" wh_bloodbowl3 wh_killteam wh_40k_10e h:mtg h:hearthstone h:hs_battlegrounds h:shadowverse h:runeterra h:gwent h:duelyst h:faeria h:inscryption h:into_the_breach h:wh_underworlds h:sts1 h:sts2 h:darkest_dungeon h:wh_aos_4th h:lorcana h:swu h:tesl h:monster_train
  run propagate.py "$D"
  run keyword_defs.py "$D"
  run outcome_tree.py "$D"
  for f in reviews_outcome/*.json; do g=$(basename "$f" .json); run apply_review.py "$D" "$g" "$f" old; done
  run link_types.py "$D"
  run engine_links.py "$D"
  run design_problems.py "$D"
  run trigger_pairs.py "$D"
  run regression.py "$D" enforce
  run concept_tree.py "$D" apply
  for f in reviews/*.json reviews_outcome/*.json; do g=$(basename "$f" .json); run apply_review.py "$D" "$g" "$f" new; done   # reviews are in the new ids (fixes/f15)
  run regression.py "$D" enforce_new
  run relations_added.py "$D"
  run pattern_fix.py "$D"
  run kw_links.py "$D"
  run trigger_pairs.py "$D" pairs_only   # again after the tree move: pairs for the tags added since (new patterns, key wins)
  run parent_rule.py "$D"
  run final_revert.py "$D"
  run key_wins.py apply "$D"
  run dedupe.py "$D"
  run frequency.py "$D"
  run fixes/f07_keywords_structure.py "$D"
  run fixes/f05_factions.py "$D"
  run distinct.py "$D"
}
rm -f "$OUT" "$OUT.steps.tsv" "$OUT.work.steps.tsv"; cp "$IN" "$OUT"; $P indexes.py "$OUT" create   # the database is stored without its indexes (indexes.py)
if [ $# -gt 0 ]; then   # insert-only: the steps run on a work copy holding only the new games; their rows are then added
  GAMES=$(for a in "$@"; do echo "${a%%=*}"; done | sort -u | tr '\n' ' ')
  WORK="$OUT.work"; rm -f "$WORK"; cp "$OUT" "$WORK"
  $P compact_text.py "$WORK" expand
  $P add_games.py prepare "$WORK" $GAMES
  for a in "$@"; do $P load_cards.py "$WORK" "${a%%=*}" "${a#*=}"; done
  steps "$WORK"
  $P compact_text.py "$OUT" expand
  $P add_games.py copy "$OUT" "$WORK" $GAMES; rm -f "$WORK"
else
  steps "$OUT"
fi
$P step_log.py "$OUT" --done
$P signature.py "$OUT"
$P precision.py "$OUT"
$P finalize.py "$OUT"
if [ $# -gt 0 ]; then INX="$OUT.in"; rm -f "$INX"; cp "$IN" "$INX"; $P compact_text.py "$INX" expand; $P add_games.py verify "$OUT" "$INX"; rm -f "$INX"; fi
$P regression.py "$OUT" check
$P combo_check.py "$OUT"
$P trigger_pairs.py "$OUT" check
$P realworld.py "$OUT"
$P compact_text.py "$OUT" compact
python3 -I -c "import sqlite3,sys; c=sqlite3.connect(sys.argv[1], isolation_level=None); c.execute(\"insert into entity_fts(entity_fts) values('integrity-check')\"); print(c.execute('pragma integrity_check').fetchone())" "$OUT"
$P test_query.py "$OUT"
$P indexes.py "$OUT" drop   # stored without indexes: about 21 MB smaller, rebuilt in under a second

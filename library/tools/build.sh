#!/bin/sh
# The library build: one chain of steps from the frozen base tagging (make_base.py), the card data and the record files.
# Loads add cards first (load_cards.py). fixes/ holds the three idempotent fix steps (f03, f05, f07).
# Usage: build.sh [--only <game>,...] <in.sqlite> <out.sqlite> [<game>=<cards.json> ...]   or   build.sh --steps <db>
#   --steps: run only the steps on <db> in place, no checks (game_check.sh uses it on a one-game copy)
#   --only: the steps run on those games (and the loaded ones) alone, every other game's rows are copied unchanged
#   (only_games.py); the checks after the steps still run on every game.
#   One chain (21 Oct 2026): the first step removes every derived tag and pair, so the output depends only on the card data,
#   the record files and the tools, never on an earlier build. With loads, the new cards are added first, then every step runs
#   over all games. To reload a game, drop it first (drop_game.py).
#   Any failed check stops the build.
set -e
STEPS=""; if [ "$1" = "--steps" ]; then STEPS=$(readlink -f "$2"); set -- "$STEPS" "$STEPS"; fi   # --steps <db>: only the steps, in place (game_check.sh)
ONLY=""; if [ "$1" = "--only" ]; then ONLY=$(echo "$2" | tr ',' ' '); shift 2; fi
[ $# -ge 2 ] || { echo "usage: build.sh [--only <game>,...] <in.sqlite> <out.sqlite> [<game>=<cards.json> ...]"; exit 2; }
IN=$(readlink -f "$1"); OUT=$(readlink -f "$2"); shift 2
LOADS=""; for a in "$@"; do LOADS="$LOADS ${a%%=*}=$(readlink -f "${a#*=}")"; done; set -- $LOADS   # load paths relative to the caller
cd "$(dirname "$0")"
P="python3 -I"
steps() {   # $1 = db
  D="$1"
  run() { t0=$(date +%s); $P "$@"; t1=$(date +%s); $P step_log.py "$D" "$(echo "$*" | sed "s#$D##")"; t2=$(date +%s); echo "time: $((t1-t0)) s step, $((t2-t1)) s log: $(echo "$*" | cut -c1-60 | sed "s#$D##")"; }   # each step, then what it removed (step_log.py); the times show where a build is slow
  run compact_text.py "$D" expand
  run trim_text.py "$D"   # text with no mechanic (Inscryption wiki prose, 40k rule lists): idempotent, so reloaded cards are trimmed too
  run concept_tree.py "$D" restore
  run start_clean.py "$D"   # one chain: every build starts from the frozen base (make_base.py)
  run concept_defs.py "$D"
  run game_patterns.py "$D" patterns
  run drop_untagged.py "$D"
  run fix_grants.py "$D"
  run fixes/f03_grant_not_does.py "$D"
  for f in reviews/*.json; do g=$(basename "$f" .json); run apply_review.py "$D" "$g" "$f" old; done
  run kw_sync.py "$D" wh_40k_10e h:mtg h:hearthstone h:hs_battlegrounds h:shadowverse h:runeterra h:gwent h:duelyst h:faeria h:inscryption h:into_the_breach h:sts1 h:sts2 h:darkest_dungeon h:wh_aos_4th h:lorcana h:swu h:tesl h:monster_train
  run propagate.py "$D"
  run keyword_defs.py "$D"
  run outcome_tree.py "$D"
  for f in reviews_outcome/*.json; do g=$(basename "$f" .json); run apply_review.py "$D" "$g" "$f" old; done
  run link_types.py "$D"
  run cost_rules.py "$D"   # tags from the cost field where cards print the cost apart from the text
  run engine_links.py "$D"
  run design_problems.py "$D"
  run trigger_pairs.py "$D"
  run regression.py "$D" enforce
  run concept_tree.py "$D" apply
  for f in reviews/*.json reviews_outcome/*.json; do g=$(basename "$f" .json); run apply_review.py "$D" "$g" "$f" new; done   # reviews are in the new ids (fixes/f15)
  run leave_triggers.py "$D"   # leave-play triggers by whose (death_side.py); after the tree move, which knows the new ids
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
if [ -n "$STEPS" ]; then steps "$STEPS"; $P step_log.py "$STEPS" --done; exit 0; fi
rm -f "$OUT" "$OUT.steps.tsv" "$OUT.work.steps.tsv" "$OUT.part" "$OUT.part.steps.tsv"; cp "$IN" "$OUT"; $P indexes.py "$OUT" create   # the full form of the stored database (indexes.py)
FULL="$OUT"
if [ -n "$ONLY" ]; then   # the steps work on a copy with only these games
  ONLY="$ONLY $(for a in "$@"; do echo "${a%%=*}"; done | tr '\n' ' ')"
  $P compact_text.py "$FULL" expand; $P only_games.py split "$FULL" "$OUT.part" $ONLY; OUT="$OUT.part"
fi
if [ $# -gt 0 ]; then   # loads: the new cards go into the library copy, then every step runs over all games (one chain)
  GAMES=$(for a in "$@"; do echo "${a%%=*}"; done | sort -u | tr '\n' ' ')
  $P compact_text.py "$OUT" expand; $P concept_tree.py "$OUT" restore   # old ids, as the patterns read them
  for a in "$@"; do $P load_cards.py "$OUT" "${a%%=*}" "${a#*=}"; done
  $P start_clean.py "$OUT" keep $GAMES   # their first tags join the base
fi
steps "$OUT"
$P step_log.py "$OUT" --done
if [ -n "$ONLY" ]; then $P only_games.py merge "$FULL" "$OUT" $ONLY; if [ -f "$OUT.steps.tsv" ]; then mv "$OUT.steps.tsv" "$FULL.steps.tsv"; fi; rm -f "$OUT"; OUT="$FULL"; fi
$P signature.py "$OUT"
$P precision.py "$OUT"
$P finalize.py "$OUT"
$P regression.py "$OUT" check
$P death_side.py   # wording tests of the own / another death and leave-play rule
$P combo_check.py "$OUT"
$P trigger_pairs.py "$OUT" check
$P realworld.py "$OUT"
$P compact_text.py "$OUT" compact
python3 -I -c "import sqlite3,sys; c=sqlite3.connect(sys.argv[1], isolation_level=None); c.execute(\"insert into entity_fts(entity_fts) values('integrity-check')\"); print(c.execute('pragma integrity_check').fetchone())" "$OUT"
$P test_query.py "$OUT"
$P indexes.py "$OUT" drop   # the stored form (indexes.py): no indexes, base kept as differences

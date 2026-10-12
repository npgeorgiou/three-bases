#!/bin/sh
# Rebuild the library from the raw corpus (repo/Library.sqlite, src/): concepts, patterns, Marvel Snap, hand reviews, keyword sync;
# then later loads (Underworlds warscrolls, Runeterra, Hearthstone, Battlegrounds), the outcome concept tree and its keyword review, link rules, trigger table, duplicate merging, frequency, signatures, precision, clean-up, and the checks (any failed check stops the build).
set -e
cd "$(dirname "$0")"
rm -f build.sqlite build.sqlite-journal build.sqlite-wal; cp repo/Library.sqlite build.sqlite
python3 -I tools/new_concepts.py build.sqlite
python3 -I tools/retag.py build.sqlite @tools/retag_concepts.txt
python3 -I tools/game_patterns.py build.sqlite tools/patterns
python3 -I tools/fix_grants.py build.sqlite
python3 -I tools/load_snap.py build.sqlite src/sd/cards.json src/locations.json tools/snap_review.json
for f in tools/reviews/*.json; do [ -e "$f" ] || continue; g=$(basename "$f" .json); python3 -I tools/apply_review.py build.sqlite "$g" "$f"; done
python3 -I tools/kw_sync.py build.sqlite wh_bloodbowl3 wh_killteam wh_40k_10e h:mtg h:hearthstone h:hs_battlegrounds h:shadowverse h:runeterra h:gwent h:duelyst h:faeria h:inscryption h:into_the_breach h:wh_underworlds h:sts1 h:sts2 h:darkest_dungeon h:wh_aos_4th
python3 -I tools/propagate.py build.sqlite
python3 -I tools/load_underworlds_warscrolls.py build.sqlite
python3 -I tools/runeterra_fixes.py build.sqlite
python3 -I tools/load_extra.py build.sqlite hearthstone tools/hearthstone_extra.json
python3 -I tools/load_extra.py build.sqlite hs_battlegrounds tools/hs_battlegrounds_extra.json
python3 -I tools/keyword_defs.py build.sqlite
python3 -I tools/outcome_tree.py build.sqlite
for f in tools/reviews_outcome/*.json; do g=$(basename "$f" .json); python3 -I tools/apply_review.py build.sqlite "$g" "$f"; done
python3 -I tools/condition_roles.py build.sqlite
python3 -I tools/link_types.py build.sqlite
python3 -I tools/engine_links.py build.sqlite
python3 -I tools/design_problems.py build.sqlite
python3 -I tools/trigger_pairs.py build.sqlite
python3 -I tools/dedupe.py build.sqlite
python3 -I tools/regression.py build.sqlite enforce
python3 -I tools/frequency.py build.sqlite
python3 -I tools/signature.py build.sqlite
python3 -I tools/precision.py build.sqlite
python3 -I tools/finalize.py build.sqlite
python3 -I tools/regression.py build.sqlite check
python3 -I tools/combo_check.py build.sqlite
python3 -I tools/trigger_pairs.py build.sqlite check
python3 -I -c "import sqlite3; c=sqlite3.connect('build.sqlite', isolation_level=None); c.execute(\"insert into entity_fts(entity_fts) values('integrity-check')\"); c.execute('vacuum'); print(c.execute('pragma integrity_check').fetchone())"
python3 -I tools/test_query.py build.sqlite

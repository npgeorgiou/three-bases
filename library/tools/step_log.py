"""Logs what each build step removes and adds. Usage: step_log.py <db> <step label>
After every step, counts each game's tags per concept (all roles) and compares them with the counts after the previous step
(kept in the table _step_counts until `step_log.py <db> --done`). Every drop and every gain (after > before) is written to <db>.steps.tsv (step, game, concept, before,
after). A warning is printed when a step removes at least MIN_LOST tags and half of one game's tags of a concept while the
other games keep 80% or more of theirs: a step that wipes one game's tags is a bug like the outcome-tree one (it wiped all of
Lorcana's "can't challenge" tags). Steps meant to remove (reviewed drops) can warn too: check them, they are not always wrong."""
import os, sqlite3, sys
MIN_LOST = 15
db, label = sys.argv[1], ' '.join(sys.argv[2:])
c = sqlite3.connect(db)
if label == '--done':   # end of the steps: the counts table is not stored
    c.execute('DROP TABLE IF EXISTS _step_counts'); c.commit(); sys.exit()
now = {(g, k): n for g, k, n in c.execute(
    'SELECT e.game, ec.concept, count(*) FROM entity_concepts ec JOIN entities e ON e.id = ec.entity GROUP BY 1, 2')}
renames = label.startswith('concept_tree.py')   # moves tags to new concept ids: nothing is lost, the counts start again
if not renames and c.execute("SELECT 1 FROM sqlite_master WHERE name='_step_counts'").fetchone():
    before = {(g, k): n for g, k, n in c.execute('SELECT game, concept, n FROM _step_counts')}
    lost = sorted(((g, k, n, now.get((g, k), 0)) for (g, k), n in before.items() if now.get((g, k), 0) < n),
                  key=lambda r: r[3] - r[2])
    gained = sorted((g, k, before.get((g, k), 0), m) for (g, k), m in now.items() if m > before.get((g, k), 0))
    if lost or gained:
        with open(db + '.steps.tsv', 'a', encoding='utf-8') as f:
            for g, k, n, m in lost + gained: f.write(f'{label}\t{g}\t{k}\t{n}\t{m}\n')
    tot_b, tot_a = {}, {}   # per concept, all games
    for (g, k), n in before.items(): tot_b[k] = tot_b.get(k, 0) + n; tot_a[k] = tot_a.get(k, 0) + now.get((g, k), 0)
    for g, k, n, m in lost:   # one game loses most of a concept while the other games keep at least 80% of theirs
        rb, ra = tot_b[k] - n, tot_a[k] - m
        if n - m >= MIN_LOST and m <= n / 2 and (rb == 0 or ra >= 0.8 * rb):
            print(f'step_log: {label}: {g} {k} {n} -> {m} (other games keep {ra} of {rb})')
elif not os.path.exists(db + '.steps.tsv'):
    open(db + '.steps.tsv', 'w', encoding='utf-8').write('step\tgame\tconcept\tbefore\tafter\n')
c.execute('DROP TABLE IF EXISTS _step_counts')
c.execute('CREATE TABLE _step_counts(game TEXT, concept TEXT, n INTEGER)')
c.executemany('INSERT INTO _step_counts VALUES(?,?,?)', [(g, k, n) for (g, k), n in now.items()])
c.commit()

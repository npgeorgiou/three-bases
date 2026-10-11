"""Write a review dump of one game: one line per distinct text: id|name|category/cost/stats|text|current tags.
Usage: dump.py <db> <game> <out> [maxlen]"""
import json, sqlite3, sys
db, game, out = sys.argv[1:4]
ML = int(sys.argv[4]) if len(sys.argv) > 4 else 600
c = sqlite3.connect(db)
SKIP = {'lanes', 'points_scoring', 'run_structure', 'auto_battle', 'telegraphed_threats'}
rows = c.execute("select id,name,category,cost,stats,text from entities where game=? and text is not null and category not in ('tribe') order by category,name", (game,)).fetchall()
seen, lines = set(), []
for i, n, cat, cost, stats, t in rows:
    if t in seen: continue
    seen.add(t)
    tags = sorted({(con if role == 'does' else con + ':' + role[:3]) for con, role in c.execute("select concept,role from entity_concepts where entity=?", (i,)) if con not in SKIP})
    st = ''
    try:
        d = json.loads(stats) if stats else {}
        st = '/'.join(str(v) for v in d.values())[:30]
    except Exception: st = (stats or '')[:30]
    t1 = ' '.join(t.split())
    if len(t1) > ML: t1 = t1[:ML] + '…'
    lines.append(f"{i}|{n}|{cat[:4]} {cost or ''} {st}|{t1}|{','.join(tags)}")
open(out, 'w').write('\n'.join(lines))
print(game, len(rows), 'entries,', len(lines), 'distinct texts')

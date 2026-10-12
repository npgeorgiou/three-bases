"""Smoke tests for query.py: every command runs on a fixed query and must print the lines it always prints.
Usage: test_query.py <db>   (exit 1 on any failure)"""
import os, sys, io, contextlib
os.environ['TB_LIB'] = os.path.abspath(sys.argv[1]); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import query
TESTS = [  # (command, args, kwargs, text the output must contain)
 ('games', [], {}, 'runeterra'),
 ('concepts', ['revive'], {}, 'revive'),
 ('concept', ['revive'], {'per_game': 1}, 'parents:'),
 ('cooccur', ['revive'], {'game': 'runeterra'}, ''),
 ('search', ['frostbite'], {'game': 'runeterra'}, 'Frostbite'),
 ('entity', ['Frostbite'], {'game': 'runeterra'}, 'category: keyword'),
 ('faction', ['runeterra', 'Freljord'], {}, 'Freljord'),
 ('problem', ['p_draw_engine'], {}, 'related mechanics'),
 ('archetypes', [], {'game': 'runeterra'}, 'Freljord'),
 ('grid', ['death_trigger'], {'game': 'runeterra'}, 'death_trigger'),
 ('unused_pairs', ['on_kill'], {}, '['),
 ('frequency', [], {'game': 'runeterra'}, 'per_card'),
 ('signature', ['runeterra', 'Freljord'], {}, 'own keywords'),
 ('splash', ['revive'], {'game': 'runeterra'}, 'Noxus'),
 ('interactions', ['Thresh (level 2)'], {'game': 'runeterra'}, 'keyword partners'),
 ('combo', ['Thresh (level 2)', 'Kalista (level 2)'], {'game': 'runeterra'}, 'relation'),
]
bad = 0
for cmd, a, kw, must in TESTS:
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): getattr(query, cmd)(*a, **kw)
        out = buf.getvalue()
        if not out.strip() or (must and must not in out): bad += 1; print('FAIL', cmd, a, 'missing', repr(must))
    except Exception as ex:
        bad += 1; print('FAIL', cmd, a, type(ex).__name__, ex)
print(f'query tests: {len(TESTS) - bad}/{len(TESTS)} pass')
sys.exit(1 if bad else 0)

"""Step 3 of the test: per-game numbers for test steps 1, 2 (answer-key part, known errors) and 3 (combos part) -> REPORT.md.
Builds a second copy with the rows in force (trigger_effect = the row pairs; aoe_damage, temporary_buff, permanent_growth =
the computed ones) so the existing tools (combo_check.py, key scoring) run unchanged on old and new.
Usage: report.py <copy.sqlite> <real.sqlite (read only)>"""
import collections, json, os, re, shutil, sqlite3, subprocess, sys
import common as C
sys.path.insert(0, os.path.join(C.TOOLS, 'key')); import key as K

PASS_PLACED = 0.98
KNOWN = {('faeria', 'Wild Avenger'): [('on_play', 'taunt'), ('on_play', 'immobilize'), ('on_play', 'forced_movement'), ('on_play', 'attack_gain')],
         ('hearthstone', 'Invincible'): [('on_play', 'death_trigger'), ('on_play', 'revive'), ('death_trigger', 'summon')],
         ('wh_40k_10e', 'Mortarion'): [('aura', 'damage'), ('death_trigger', 'play_restriction'), ('buff', 'piercing')],
         ('lorcana', 'Buzz Lightyear - Jungle Ranger'): [('activated', 'revive'), ('activated', 'discard')]}
COMPOUND = ['aoe_damage', 'temporary_buff', 'permanent_growth', 'scope_global', 'scope_multi', 'scope_self']

def new_db(copy):
    out = os.path.join(os.path.dirname(copy), 'records_new.sqlite'); shutil.copyfile(copy, out)
    c = C.connect(out)
    c.execute('DELETE FROM trigger_effect')
    c.execute("INSERT INTO trigger_effect(entity, game, trigger, effect, frequency, basis) SELECT DISTINCT r.entity, x.game, r.trigger, r.effect, NULL, 'records' FROM records_pairs r JOIN entities x ON x.id=r.entity")
    c.execute("DELETE FROM entity_concepts WHERE concept IN ('aoe_damage', 'temporary_buff', 'permanent_growth')")
    c.execute("INSERT INTO entity_concepts(entity, concept, role, method) SELECT DISTINCT entity, concept, 'does', 'records' FROM records_compound")
    c.commit(); c.close(); return out

def step1(c):
    q = lambda s, *a: c.execute(s, a).fetchall()
    eff, trig = C.concept_kinds(c)
    G = collections.defaultdict(collections.Counter)
    for g, how, cross, kind in q('SELECT x.game, w.how, rt.cross, r.kind FROM tag_words w JOIN row_tags rt ON rt.rid=w.rid JOIN rows r ON r.id=rt.row '
                                 'JOIN entity_concepts ec ON ec.rowid=w.rid JOIN entities x ON x.id=ec.entity'):
        if how == 'entry_level': G[g]['entry_level'] += 1; continue
        G[g]['tags'] += 1
        if kind == 'card': G[g]['card'] += 1
        elif cross: G[g]['cross'] += 1
        else: G[g]['clean'] += 1; G[g]['excerpt'] += how == 'excerpt'   # an excerpt inside the row holds the words somewhere
    rows = collections.defaultdict(set)
    for g, r, k, kind in q('SELECT x.game, r.id, ec.concept, r.kind FROM rows r JOIN entities x ON x.id=r.entity JOIN row_tags rt ON rt.row=r.id JOIN entity_concepts ec ON ec.rowid=rt.rid WHERE r.kind != "card"'):
        rows[(g, r, kind)].add(k)
    for (g, r, kind), ks in rows.items():
        G[g]['rows'] += 1; G[g]['row_no_effect'] += not (ks & eff); G[g]['trigger_rows'] += kind == 'trigger'
        G[g]['trigger_no_effect'] += kind == 'trigger' and not (ks & eff - trig)
    for g, n in q('SELECT game, count(*) FROM (SELECT DISTINCT entity, game, trigger, effect FROM trigger_effect) GROUP BY game'): G[g]['pairs_before'] = n
    for g, n in q('SELECT x.game, count(*) FROM (SELECT DISTINCT entity, trigger, effect FROM records_pairs) r JOIN entities x ON x.id=r.entity GROUP BY x.game'): G[g]['pairs_after'] = n
    return G

def key_scores(db, g, ids_ok):
    """precision and recall of the compound concepts on the game's key entries: a library tag is right when the key has it, a
    kind of it or a broader one (key.py's rule); a key concept is found when the library has it or a kind of it"""
    key = K.load(g); c = sqlite3.connect(db)
    live = {i for (i,) in c.execute('SELECT id FROM entities WHERE game=?', (g,))}
    ids = [int(i) for i in key if int(i) in live]
    lib = collections.defaultdict(set)
    for e, k in c.execute('SELECT entity, concept FROM entity_concepts WHERE entity IN (%s)' % ','.join(map(str, ids or [0]))): lib[e].add(k)
    out = {}
    for k in COMPOUND:
        has = right = keyn = found = 0
        for i in ids:
            Kc = {x for x, _ in key[str(i)]['tags'] if x in K.TREE}; ok = Kc | {a for x in Kc for a in K.ANC[x]} | {d for x in Kc for d in K.DESC[x]}
            if k in lib[i]: has += 1; right += k in ok
            if Kc & ({k} | K.DESC.get(k, set())):
                keyn += 1; found += bool(lib[i] & ({k} | K.DESC.get(k, set())))
        out[k] = (has, right, keyn, found)
    return out

def combos(db):
    r = subprocess.run([sys.executable, os.path.join(C.TOOLS, 'combo_check.py'), db, '-v'], capture_output=True, text=True, cwd=C.TOOLS)
    per = collections.defaultdict(lambda: [0, 0]); layers = collections.Counter()
    for line in r.stdout.splitlines():
        m = re.match(r'^(\S+)\s+.{24} -> .{24} (\S+)$', line)
        if m: per[m.group(1)][1] += 1; per[m.group(1)][0] += m.group(2) != 'MISS'; layers[m.group(2)] += 1
    return per, layers

def pct(a, b): return f'{100 * a / b:.1f}%' if b else '-'

def main(copy, real):
    c = C.connect(copy); new = new_db(copy)
    G = step1(c); games = sorted(G)
    L = ['# Tagging per effect: test report', '', 'Built by `tools/records_test/` on a copy of the database (TAGGING_RECORDS.md). Script numbers only;',
         'the gold reading (step 2) and the read checks of step 3 are not in this report yet.', '',
         '## Step 1: does it fly', '',
         'Tags: all tags except cost and structure tags (data_rule, game_structure). Clean: the words that made the tag were found',
         'and lie inside its row. Card-level: tags with no words in the text (hand-mapped whole-card tags), in the card row.',
         'Excerpt: only an old fixed-length excerpt is stored and the patterns no longer find the words in it; clean when the whole excerpt lies in the row.',
         f'Pass: clean + card-level {PASS_PLACED:.0%}+ in every game.', '',
         '| game | tags | clean | card-level | of them excerpts | words cross rows | clean + card | rows | rows without effect | trigger rows without effect | pairs before | pairs after | pass |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    s1 = {}
    for g in games:
        x = G[g]; ok = x['clean'] + x['card']; s1[g] = x['tags'] and ok / x['tags'] >= PASS_PLACED
        L.append(f"| {g} | {x['tags']} | {pct(x['clean'], x['tags'])} | {x['card']} | {x['excerpt']} | {x['cross']} | {pct(ok, x['tags'])} | {x['rows']} | "
                 f"{pct(x['row_no_effect'], x['rows'])} | {x['trigger_no_effect']} of {x['trigger_rows']} | {x['pairs_before']} | {x['pairs_after']} | {'pass' if s1[g] else 'FAIL'} |")
    T = collections.Counter()
    for g in games: T.update(G[g])
    L += ['', f"All games: clean {pct(T['clean'], T['tags'])}, clean + card {pct(T['clean'] + T['card'], T['tags'])}; outliers (words or excerpt across rows): {T['cross']}.", '']
    how = collections.Counter(dict(c.execute('SELECT how, count(*) FROM tag_words GROUP BY how').fetchall()))
    L += ['How the words were found: ' + ', '.join(f'{k} {v}' for k, v in how.most_common()) + '.', '']
    L += ['## Step 2 (answer-key part): compound tags', '',
          'Per game and concept on the key entries: old (today\'s tags) and new (computed from the rows, rows.py). Scope tags are unchanged.',
          'P = right / tagged, R = found / key. Pass: no concept worse in any game (precision and recall both).', '',
          '| game | concept | old tagged | old P | old R | new tagged | new P | new R | key | worse |', '|---|---|---|---|---|---|---|---|---|---|']
    s2 = {}
    for g in games:
        if not os.path.exists(os.path.join(C.TOOLS, 'key', g, 'key.json')): continue
        o, n = key_scores(real, g, None), key_scores(new, g, None); s2[g] = True
        for k in COMPOUND:
            ho, ro, kn, fo = o[k]; hn, rn, _, fn = n[k]
            if not (ho or kn): continue
            Po, Pn = (ro / ho if ho else None), (rn / hn if hn else None)
            worse = (fn < fo) or (Po is not None and Pn is not None and Pn < Po - 1e-9)
            if worse: s2[g] = False
            L.append(f"| {g} | {k} | {ho} | {pct(ro, ho)} | {pct(fo, kn)} | {hn} | {pct(rn, hn)} | {pct(fn, kn)} | {kn} | {'WORSE' if worse else ''} |")
    L += ['', '### Known errors', '']
    for (g, nm), bad in KNOWN.items():
        e = c.execute('SELECT id FROM entities WHERE game=? AND name=?', (g, nm)).fetchone()
        if not e: L.append(f'- {nm}: not in the library'); continue
        old = set(c.execute('SELECT trigger, effect FROM trigger_effect WHERE entity=?', e).fetchall())
        nw = set(c.execute('SELECT trigger, effect FROM records_pairs WHERE entity=?', e).fetchall())
        left = [f'{a} -> {b}' for a, b in bad if (a, b) in nw]
        L.append(f"- {nm} ({g}): wrong pairs today {sum((a, b) in old for a, b in bad)}/{len(bad)}, after {len(left)}/{len(bad)}"
                 f"{' (' + ', '.join(left) + ')' if left else ''}; pairs now: {', '.join(f'{a} -> {b}' for a, b in sorted(nw)) or 'none'}")
    L += ['', '## Step 3 (combos part): `combo_check.py` on old and new', '']
    (po, lo), (pn, ln) = combos(real), combos(new)
    L += ['| game | known combos | found old | found new |', '|---|---|---|---|']
    s3 = {}
    for g in sorted(set(po) | set(pn)):
        s3[g] = pn[g][0] >= po[g][0]
        L.append(f'| {g} | {po[g][1]} | {po[g][0]} | {pn[g][0]}{"" if s3[g] else " FEWER"} |')
    L += ['', f'Strongest layer, old: {dict(lo)}; new: {dict(ln)}.', '']
    L += ['## Verdict per game (script parts only)', '', '| game | step 1 | step 2 key | step 3 combos |', '|---|---|---|---|']
    for g in games:
        f = lambda d: '-' if g not in d else 'pass' if d[g] else 'FAIL'
        L.append(f'| {g} | {f(s1)} | {f(s2)} | {f(s3)} |')
    open(os.path.join(C.HERE, 'REPORT.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('step1 fails', [g for g in games if not s1[g]], 'step2 fails', [g for g in s2 if not s2[g]], 'step3 fails', [g for g in s3 if not s3[g]])

if __name__ == '__main__': main(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]))

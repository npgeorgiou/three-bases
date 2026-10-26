"""Step 3 of the test: per-game numbers -> REPORT.md: how the tags were put into abilities, how often the position rule and the
statistics rule agree, the trigger pairs before and after, the known errors, and combo_check.py on old and new (a second copy
with trigger_effect = the ability pairs, so the existing tools run unchanged). Compound tags are kept as stored.
Usage: report.py <copy.sqlite> <real.sqlite (read only)>"""
import collections, json, os, re, shutil, sqlite3, subprocess, sys
import common as C

PASS_PLACED = 0.98
KNOWN = {('faeria', 'Wild Avenger'): [('on_play', 'taunt'), ('on_play', 'immobilize'), ('on_play', 'forced_movement'), ('on_play', 'attack_gain')],
         ('hearthstone', 'Invincible'): [('on_play', 'death_trigger'), ('on_play', 'revive'), ('death_trigger', 'summon')],
         ('wh_40k_10e', 'Mortarion'): [('aura', 'damage'), ('death_trigger', 'play_restriction'), ('buff', 'piercing')],
         ('lorcana', 'Buzz Lightyear - Jungle Ranger'): [('activated', 'revive'), ('activated', 'discard')]}

def new_db(copy):
    out = os.path.join(os.path.dirname(copy), 'records_new.sqlite'); shutil.copyfile(copy, out)
    c = C.connect(out)
    c.execute('DELETE FROM trigger_effect')
    c.execute("INSERT INTO trigger_effect(entity, game, trigger, effect, frequency, basis) SELECT DISTINCT r.entity, x.game, r.trigger, r.effect, NULL, 'records' FROM records_pairs r JOIN entities x ON x.id=r.entity")
    c.commit(); c.close(); return out

GUESS = {'statistics'}
def combos(db):
    r = subprocess.run([sys.executable, os.path.join(C.TOOLS, 'combo_check.py'), db, '-v'], capture_output=True, text=True, cwd=C.TOOLS)
    per = collections.defaultdict(lambda: [0, 0]); layers = collections.Counter()
    for line in r.stdout.splitlines():
        m = re.match(r'^(\S+)\s+.{24} -> .{24} (\S+)$', line)
        if m: per[m.group(1)][1] += 1; per[m.group(1)][0] += m.group(2) != 'MISS'; layers[m.group(2)] += 1
    return per, layers

def pct(a, b): return f'{100 * a / b:.1f}%' if b else '-'

def main(copy, real):
    c = C.connect(copy); new = new_db(copy); q = lambda s, *a: c.execute(s, a).fetchall()
    G = collections.defaultdict(collections.Counter)
    for g, how, agree in q('SELECT x.game, t.how, t.stats_agree FROM ability_tags t JOIN abilities a ON a.id=t.ability JOIN entities x ON x.id=a.entity'):
        G[g]['tags'] += 1; G[g][how] += 1
        if agree is not None: G[g]['checked'] += 1; G[g]['agree'] += agree
    for g, e, n in q("SELECT x.game, a.entity, count(DISTINCT a.id) FROM abilities a JOIN entities x ON x.id=a.entity WHERE a.kind='trigger' GROUP BY a.entity"):
        G[g]['multi'] += n > 1
    for g, n in q("SELECT x.game, count(DISTINCT a.entity) FROM abilities a JOIN entities x ON x.id=a.entity GROUP BY x.game"): G[g]['cards'] = n
    for g, n in q('SELECT game, count(*) FROM (SELECT DISTINCT entity, game, trigger, effect FROM trigger_effect) GROUP BY game'): G[g]['pairs_before'] = n
    for g, n in q('SELECT x.game, count(*) FROM (SELECT DISTINCT entity, trigger, effect FROM records_pairs) r JOIN entities x ON x.id=r.entity GROUP BY x.game'): G[g]['pairs_after'] = n
    games = sorted(G)
    L = ['# Tagging per effect: test report', '', 'Built by `tools/records_test/` (words.py, abilities.py, report.py) on a copy of the database.',
         'Script numbers only; the gold reading is not in this report yet.', '',
         '## How the tags were put into abilities', '',
         "Keyword: the keyword's own ability. One trigger / no trigger: the card has at most one trigger, so all its other tags go with",
         'it (no text read). Position: cards with two or more triggers; the tag goes to the nearest trigger before its words.',
         "Statistics: words unknown; the trigger this game's one-trigger cards most often show with that tag. Card: whole-card tags.",
         'Agree: on tags placed by position, how often the statistics rule picks the same ability (a check per game, no reading).', '',
         '| game | cards | cards with 2+ trigger abilities | tags | keyword | one trigger | no trigger | position | statistics | card | agree |',
         '|---|---|---|---|---|---|---|---|---|---|---|']
    for g in games:
        x = G[g]; pos = x['position'] + x['position (trigger after)'] + x['position (before every trigger)']
        L.append(f"| {g} | {x['cards']} | {x['multi']} | {x['tags']} | {x['keyword']} | {x['one trigger']} | {x['no trigger']} | {pos} | {x['statistics']} | {x['card']} | {pct(x['agree'], x['checked'])} |")
    L += ['', '## Trigger pairs', '', '| game | before | after |', '|---|---|---|'] + [f"| {g} | {G[g]['pairs_before']} | {G[g]['pairs_after']} |" for g in games]
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
    open(os.path.join(C.HERE, 'REPORT.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('combos fewer in', [g for g in s3 if not s3[g]])

if __name__ == '__main__': main(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]))

"""Fixed test cards for the effect records (TAGGING_RECORDS.md step 3): per game, the cards a reader agent judged against their
text (50 random, 50 complicated), stored with the rows the reader says are right, so later changes are re-checked by script.
  testset.py make <game> <rows file> <judgment file>   writes tests/<game>.json (rows file: the cards and rows the reader saw;
                                                       judgment file: the reader's JSON lines, see BRIEF in the check folder)
  testset.py score <db> <game> [--show N]              scores today's rows against tests/<game>.json
A row is compared on effect (equal, or a parent or child in the concept tree) and target (who and how; a free-text target
from the reader is matched on its first words). A card is right when every expected row is met and no extra row is made."""
import json, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
NO = re.compile(r"^(?:no row|none|remove|drop|delete|n/a|-)\b", re.I)


def parse_rows(path):
    cards, cur = {}, None
    for line in open(path, encoding='utf-8'):
        if line.startswith('### '):
            p = line[4:].split(' | ')
            cur = int(p[0]); cards[cur] = {'kind': p[1], 'name': p[2].strip(), 'text': '', 'rows': []}
        elif line.startswith('TEXT: ') and cur: cards[cur]['text'] = line[6:].strip()
        elif line.startswith('  ') and cur and not line.strip().startswith('(none)'):
            f = [x.strip() for x in line.strip().split(' | ')]
            f += [''] * (10 - len(f))
            cards[cur]['rows'].append({'ability': f[0], 'trigger': f[1], 'effect': f[2], 'target': f[3], 'shape': f[4],
                                       'amount': f[5], 'duration': f[6]})
        elif cur and not line.startswith(('ROWS:', 'TEXT:')) and line.strip(): cards[cur]['text'] += ' ' + line.strip()
    return cards


def make(game, rows_file, judg_file):
    cards = parse_rows(rows_file)
    out = {}
    for line in open(judg_file, encoding='utf-8'):
        if not line.strip(): continue
        j = json.loads(line); c = cards.get(j['id'])
        if not c: continue
        rows = [dict(r) for r in c['rows']]
        drop = set()
        for w in j.get('wrong', []):
            n = w.get('row')
            if not isinstance(n, int) or not 1 <= n <= len(rows): continue
            sh = str(w.get('should', '')).strip()
            f = str(w.get('field', '')).split('/')[0].strip()
            if NO.match(sh) or f in ('ability', 'row'): drop.add(n - 1)
            elif f in rows[n - 1]: rows[n - 1][f] = sh
        rows = [r for i, r in enumerate(rows) if i not in drop]
        for m in j.get('missing', []):
            f = [x.strip() for x in str(m.get('row', '')).split('|')] + [''] * 6
            rows.append({'ability': '?', 'trigger': f[0], 'effect': f[1] or str(m.get('effect', '')), 'target': f[2], 'shape': f[3],
                         'amount': f[4], 'duration': f[5]})
        out[j['id']] = {'kind': c['kind'], 'name': c['name'], 'text': c['text'], 'rows': rows, 'judged_ok': j.get('ok')}
    os.makedirs(os.path.join(HERE, 'tests'), exist_ok=True)
    with open(os.path.join(HERE, 'tests', f'{game}.json'), 'w', encoding='utf-8') as f:
        f.write('{\n' + ',\n'.join(f' "{k}": ' + json.dumps(v, ensure_ascii=False) for k, v in out.items()) + '\n}\n')
    print(game, len(out), 'cards stored')


def score(db, game, show=0):
    import build_records as B
    c = sqlite3.connect(db)
    G = B.Game(c, game)
    tests = json.load(open(os.path.join(HERE, 'tests', f'{game}.json'), encoding='utf-8'))
    rel = lambda a, b: a == b or b in G.anc.get(a, ()) or a in G.anc.get(b, ())
    def eff_ok(want, got):
        ws = [w for w in re.findall(r"[a-z_]+", want.lower()) if w in G.facet]
        return any(rel(w, got) for w in ws) if ws else want.lower().startswith(got[:6])
    def tg_ok(want, got):
        w = want.lower().replace('(', ' ').split()
        g = got.lower().split()
        if not w: return True
        return g[:2] == w[:2] or (g[:1] == w[:1] and len(w) == 1) or (got and want.lower().startswith(got.lower()))
    right = n = rows_ok = rows_n = 0; bad = []
    for sid, t in tests.items():
        e = int(sid)
        r = c.execute("SELECT name, category, text FROM entities WHERE id=?", (e,)).fetchone()
        if not r: continue
        nm, cat, text = r
        got = (B.dd_entry(G, e, nm, cat, text) if game == 'darkest_dungeon' and cat in ('ability', 'item', 'monster', 'status', 'event')
               else G.entry(e, nm, cat, text))[0]
        got = [x for x in got if x[3]]
        want = [w for w in t['rows'] if w['effect']]
        used, miss = set(), []
        for w in want:
            hit = next((i for i, x in enumerate(got) if i not in used and eff_ok(w['effect'], x[3]) and tg_ok(w['target'], x[4])), None)
            if hit is None:  # one "+2/+2" row meets both an attack and a defence row of the same target
                hit2 = next((i for i in used if got[i][3] in ('stat_gain', 'temporary_buff', 'permanent_growth') and eff_ok(w['effect'], got[i][3])
                             and tg_ok(w['target'], got[i][4])), None)
                if hit2 is None: miss.append(w)
            else: used.add(hit)
        extra = [x for i, x in enumerate(got) if i not in used and not (x[10] == 'keyword' and x[11] and x[11] in text.lower())]
        # a keyword row for a keyword the text names is backed by the text even when the judged rows lacked it
        rows_n += len(want); rows_ok += len(want) - len(miss)
        n += 1
        if not miss and not extra: right += 1
        else: bad.append((t['name'], t['text'][:160], miss, extra))
    print(f'{game:16} test cards {n}: right {right} ({100 * right / max(1, n):.0f}%), expected rows met {rows_ok}/{rows_n} '
          f'({100 * rows_ok / max(1, rows_n):.0f}%)')
    for nm, tx, miss, extra in bad[:show]:
        print(f'  {nm} | {tx}')
        for w in miss: print(f"     missing: {w['trigger']} | {w['effect']} | {w['target']} | {w['amount']}")
        for x in extra: print(f"     extra:   {x[2]} | {x[3]} | {x[4]} | {x[6]}")


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'make': make(a[1], a[2], a[3])
    else: score(a[1], a[2], int(a[a.index('--show') + 1]) if '--show' in a else 0)

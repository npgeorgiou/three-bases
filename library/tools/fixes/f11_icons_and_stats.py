"""12 Oct 2026, run once before the build that loads the Slay the Spire 2 upgrades and the BSData datasheets.
  - Repeated icon words in card text ('Gain energyenergy.', 'starstarstar') become counts ('Gain 2 energy.', '3 stars'), in every game.
  - Other lost or broken icons in Slay the Spire text: '0energy' -> '0 energy'; an energy icon dropped after 'gain'
    ('gain .', 'gain and') -> 'gain energy' (as the card's upgraded text from the same source has it); a plural template cut to
    '}' ('2 Shiv}', 'Minion Dive Bomb}') -> 's' (in text without real {templates}).
  - Units without stats get the stat line conv_bs_units.py found for them ('stats_updates' of its JSON files).
Usage: f11_icons_and_stats.py <db> [<units.json> ...]"""
import json, re, sqlite3, sys
c = sqlite3.connect(sys.argv[1])
RX = re.compile(r'\b((energy|star)(?:\2)+)(?=\W|$)')
def fix(t):
    def r(m):
        k = len(m.group(1)) // len(m.group(2))
        return f"{k} {m.group(2)}{'s' if m.group(2) == 'star' else ''}"
    return RX.sub(r, t)
n = 0
for i, t in c.execute("SELECT id, text FROM entities WHERE text LIKE '%energyenergy%' OR text LIKE '%starstar%'").fetchall():
    u = fix(t)
    if u != t: c.execute("UPDATE entities SET text=? WHERE id=?", (u, i)); n += 1
def fix_sts(t):
    t = re.sub(r'(\d)energy\b', r'\1 energy', t)
    t = re.sub(r'\b([Gg]ain) (?=and\b|\.)', r'\1 energy ', t).replace('energy .', 'energy.')
    if '{' not in t: t = re.sub(r'(\w)\}', r'\1s', t)
    return t
for i, t in c.execute("SELECT id, text FROM entities WHERE game IN ('sts1','sts2') AND text IS NOT NULL").fetchall():
    u = fix_sts(t)
    if u != t: c.execute("UPDATE entities SET text=? WHERE id=?", (u, i)); n += 1
s = 0
for p in sys.argv[2:]:
    d = json.load(open(p, encoding='utf-8')); g = d['_tag'].replace('bsdata_units_', '')
    for name, st in d.get('stats_updates', {}).items():
        s += c.execute("UPDATE entities SET stats=? WHERE game=? AND name=? AND category='unit' AND (stats IS NULL OR stats='')", (json.dumps(st, ensure_ascii=False), g, name)).rowcount
c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')"); c.commit()
print('icon texts fixed:', n, 'stat lines added:', s)

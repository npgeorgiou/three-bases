"""Step 6 of the tag-fix plan: smaller database. The copied text in entity_concepts.evidence and trigger_effect.clause is replaced
by positions in the entry's own text.
  form 0  position in the entry's text as stored (entities.text)
  form 1  position in the entry's text as the wording patterns read it (lower case, the entry's own name as 'name', Magic
          without reminder text; see read_text below)
  form 2  a note that is not part of the entry's text ('hand-mapped from the text', 'via keyword X: ...'): an id in text_notes,
          where each distinct note is stored once
Columns: entity_concepts(entity, concept, role, method, ev_form, ev_pos, ev_len), trigger_effect(entity, game, trigger, effect,
cl_form, cl_pos, cl_len, frequency, basis); for form 2, *_pos is the note id and *_len is NULL.
  compact_text.py <db> compact   last build step before the checks: text -> positions (exact: the text is cut back out unchanged)
  compact_text.py <db> expand    first build step: positions -> text, so every build step keeps working on the text columns
Readers (query.py) cut the text out with evidence_text() / clause_text(). Idempotent in both directions."""
import os, re, sqlite3, sys
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__))); import reading as RD   # how patterns read text
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import indexes as IX

def read_text(game, name, text):
    low = (text or '').lower()
    low = RD.strip(game, low)
    for x in [name] + (name or '').split(' // '):
        if x and len(x) > 2: low = low.replace(x.lower(), 'name')
    return low

class Texts:
    def __init__(self, c):
        self.c = c; self.raw = {}; self.norm = {}
        self.notes = dict(c.execute('SELECT id, note FROM text_notes')) if c.execute("SELECT 1 FROM sqlite_master WHERE name='text_notes'").fetchone() else {}
    def _ent(self, e):
        if e not in self.raw:
            r = self.c.execute('SELECT game, name, text FROM entities WHERE id=?', (e,)).fetchone() or ('', '', '')
            self.raw[e] = r
        return self.raw[e]
    def cut(self, e, form, pos, ln):
        if form is None: return None
        if form == 2: return self.notes.get(pos)
        g, n, t = self._ent(e)
        s = (t or '') if form == 0 else self.norm.setdefault(e, read_text(g, n, t))
        return s[pos:pos + ln]

def evidence_text(c, e, form, pos, ln, _cache={}):
    T = _cache.setdefault(id(c), Texts(c)); return T.cut(e, form, pos, ln)
clause_text = evidence_text

def cols(c, t): return [r[1] for r in c.execute(f'PRAGMA table_info({t})')]

def compact(c):
    c.execute('CREATE TABLE IF NOT EXISTS text_notes(id INTEGER PRIMARY KEY, note TEXT UNIQUE)')
    raw = {i: (g, n, t or '') for i, g, n, t in c.execute('SELECT id, game, name, text FROM entities')}
    norm = {}
    def place(e, s):
        if not s: return (None, None, None)
        g, n, t = raw.get(e, ('', '', ''))
        i = t.find(s)
        if i >= 0: return (0, i, len(s))
        if e not in norm: norm[e] = read_text(g, n, t)
        i = norm[e].find(s)
        if i >= 0: return (1, i, len(s))
        c.execute('INSERT OR IGNORE INTO text_notes(note) VALUES(?)', (s,))
        return (2, c.execute('SELECT id FROM text_notes WHERE note=?', (s,)).fetchone()[0], None)
    for tg, pr in TABLES:   # the tags and pairs, and the frozen base (make_base.py) in the same form
        if not c.execute("SELECT 1 FROM sqlite_master WHERE name=?", (tg,)).fetchone() or 'ev_form' in cols(c, tg): continue
        ec = c.execute('SELECT entity, concept, role, method, evidence FROM %s' % tg).fetchall()
        te = c.execute('SELECT entity, game, trigger, effect, clause, frequency, basis FROM %s' % pr).fetchall()
        c.execute('DROP TABLE %s' % tg); c.execute('DROP TABLE %s' % pr)
        c.execute('CREATE TABLE %s(entity INTEGER, concept TEXT, role TEXT, method TEXT, ev_form INTEGER, ev_pos INTEGER, ev_len INTEGER, PRIMARY KEY(entity, concept, role))' % tg)
        c.execute('CREATE TABLE %s(entity INTEGER, game TEXT, trigger TEXT, effect TEXT, cl_form INTEGER, cl_pos INTEGER, cl_len INTEGER, frequency TEXT, basis TEXT)' % pr)
        c.executemany('INSERT INTO %s VALUES(?,?,?,?,?,?,?)' % tg, [(e, k, r, m, *place(e, ev)) for e, k, r, m, ev in ec])
        c.executemany('INSERT INTO %s VALUES(?,?,?,?,?,?,?,?,?)' % pr, [(e, g, a, b, *place(e, cl), f, bs) for e, g, a, b, cl, f, bs in te])
    indexes(c); c.commit()
    n = c.execute('SELECT count(*), sum(length(note)) FROM text_notes').fetchone()
    print('compact: tags', c.execute('SELECT count(*) FROM entity_concepts').fetchone()[0], ', distinct notes', n[0], f'({n[1]} characters)')

TABLES = [('entity_concepts', 'trigger_effect'), ('base_tags', 'base_pairs')]

def expand(c):
    T = Texts(c)
    for tg, pr in TABLES:
        if not c.execute("SELECT 1 FROM sqlite_master WHERE name=?", (tg,)).fetchone() or 'evidence' in cols(c, tg): continue
        ec = [(e, k, r, m, T.cut(e, f, p, l)) for e, k, r, m, f, p, l in c.execute('SELECT * FROM %s' % tg)]
        te = [(e, g, a, b, T.cut(e, f, p, l), fr, bs) for e, g, a, b, f, p, l, fr, bs in c.execute('SELECT * FROM %s' % pr)]
        c.execute('DROP TABLE %s' % tg); c.execute('DROP TABLE %s' % pr)
        c.execute('CREATE TABLE %s(entity INTEGER, concept TEXT, role TEXT, method TEXT, evidence TEXT, PRIMARY KEY(entity, concept, role))' % tg)
        c.execute('CREATE TABLE %s(entity INTEGER, game TEXT, trigger TEXT, effect TEXT, clause TEXT, frequency TEXT, basis TEXT)' % pr)
        c.executemany('INSERT INTO %s VALUES(?,?,?,?,?)' % tg, ec)
        c.executemany('INSERT INTO %s VALUES(?,?,?,?,?,?,?)' % pr, te)
    if all('evidence' in cols(c, tg) for tg, _ in TABLES if c.execute("SELECT 1 FROM sqlite_master WHERE name=?", (tg,)).fetchone()): c.execute('DROP TABLE IF EXISTS text_notes')
    indexes(c); c.commit(); print('expand: tags', c.execute('SELECT count(*) FROM entity_concepts').fetchone()[0])

def indexes(c):   # the two tables were just rebuilt; build.sh drops all indexes from its output at the end
    for s in IX.INDEXES:
        if ' ON entity_concepts(' in s or ' ON trigger_effect(' in s: c.execute(s)

if __name__ == '__main__':
    c = sqlite3.connect(sys.argv[1])
    {'compact': compact, 'expand': expand}[sys.argv[2]](c)

"""Builds cards.sqlite from the reader records (read/<game>/*.jsonl) and the library's card data. The records are the source;
this database is thrown away and rebuilt. Every value column holds a vocab value, a number or an id; nothing else.
Usage: load.py <game> [<game> ...]"""
import csv, glob, json, os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from check import Checker, DB
from build_input import types_of, speed_of, KWFIELD

SCHEMA = """
create table vocab(field text, value text, meaning text, tree text, causes text, added text, primary key(field, value));
create table card(id integer primary key, game text, name text, category text, speed text, cost real, power real,
  health real, regions text, rarity text, is_keyword integer);
create table type(id integer primary key, game text, name text, tribe_entry integer);
create table card_type(card integer, type integer);
create table card_keyword(card integer, keyword integer);
create table card_link(src integer, rel text, dst integer);
create table event(id integer primary key, event text, actor integer, object integer);
create table target(id integer primary key, kind text, side text, pick text, n integer, zone text);
create table filter(id integer primary key, target integer, attr text, op text, n real, ref_card integer, ref_keyword integer,
  ref_type integer, val text);
create table amount(id integer primary key, x text, value real, of_target integer, attr text, event integer, span text,
  inner integer);
create table ability(id integer primary key, card integer, seq integer, event integer, lim text);
create table cond(id integer primary key, ability integer, keyword integer, test text, of_target integer, attr text, op text,
  n integer, span text, event integer, ref_keyword integer);
create table keyword_trigger(keyword integer primary key, event integer);
create table effect(id integer primary key, ability integer, seq integer, act text, on_target integer, to_target integer,
  zone text, card_ref integer, keyword_ref integer, lasts text, link text);
create table param(effect integer, param text, amount integer, event_value text);
create table unsure(card integer, field text);
create table causes(act text, event text);
"""


class Loader:
    def __init__(self, out):
        self.c = out
    def ins(self, table, **kw):
        cur = self.c.execute(f"insert into {table}({','.join(kw)}) values({','.join('?' * len(kw))})", list(kw.values()))
        return cur.lastrowid
    def ref(self, kind, name):
        ids = self.ch.names.resolve(kind, name)
        if not ids: return None
        i = ids[0]
        if isinstance(i, str):  # a type with no tribe entry
            return self.types[(self.game, i[5:])]
        if kind == 'type': return self.types.get((self.game, name.lower().rstrip('s')), self.types.get((self.game, name.lower())))
        return min(ids)
    def amount(self, a):
        if a is None: return None
        if isinstance(a, (int, float)): return self.ins('amount', x='n', value=a)
        return self.ins('amount', x=a['x'], of_target=self.target(a.get('of')), attr=a.get('attr'), event=self.event(a.get('event')),
                        span=a.get('span'), inner=self.amount(a.get('inner')))
    def target(self, t):
        if t is None: return None
        tid = self.ins('target', kind=t.get('kind'), side=t.get('side'), pick=t.get('pick'), n=self.amount(t.get('n')), zone=t.get('zone'))
        for f in t.get('with', []):
            a = f.get('attr'); row = dict(target=tid, attr=a, op=f.get('op'))
            if a in ('keyword', 'type', 'card'): row['ref_' + a] = self.ref(a, f.get('ref'))
            elif 'val' in f: row['val'] = f['val']
            if 'n' in f: row['n'] = f['n']
            self.ins('filter', **row)
        return tid
    def event(self, e):
        if e is None: return None
        return self.ins('event', event=e['event'], actor=self.target(e.get('actor')), object=self.target(e.get('object')))
    def cond(self, c, ability=None, keyword=None):
        self.ins('cond', ability=ability, keyword=keyword, test=c['test'], of_target=self.target(c.get('of')), attr=c.get('attr'),
                 op=c.get('op'), n=self.amount(c.get('n')), span=c.get('span'), event=self.event(c.get('event')),
                 ref_keyword=self.ref('keyword', c['ref']) if 'ref' in c else None)
    def record(self, rec):
        cid = rec['id']
        if 'trigger' in rec: self.ins('keyword_trigger', keyword=cid, event=self.event(rec['trigger']))
        for c in rec.get('condition', []): self.cond(c, keyword=cid)
        for f in rec.get('unsure', []): self.ins('unsure', card=cid, field=f)
        for k, ab in enumerate(rec['abilities']):
            aid = self.ins('ability', card=cid, seq=k, event=self.event(ab['when']), lim=ab.get('limit'))
            for c in ab.get('if', []): self.cond(c, ability=aid)
            for j, e in enumerate(ab['do']):
                eid = self.ins('effect', ability=aid, seq=j, act=e['act'], on_target=self.target(e.get('on')), to_target=self.target(e.get('to')),
                               zone=e.get('zone'), card_ref=self.ref('card', e['card']) if 'card' in e else None,
                               keyword_ref=self.ref('keyword', e['keyword']) if 'keyword' in e else None, lasts=e.get('lasts'), link=e.get('link'))
                for p, a in (e.get('params') or {}).items():
                    if p == 'event': self.ins('param', effect=eid, param=p, event_value=a)
                    else: self.ins('param', effect=eid, param=p, amount=self.amount(a))

    def game_data(self, game):
        lib = sqlite3.connect(DB); self.game = game; self.ch = Checker(game); self.types = {}
        for i, n, cat, sub, cost, stats, fac, extra, rar in lib.execute(
                "select id, name, category, subtypes, cost_num, stats, faction, extra, rarity from entities where game=?", (game,)):
            st = json.loads(stats) if stats and stats.startswith('{') else {}
            regs = (json.loads(extra).get('regions') if extra and extra.startswith('{') else None) or ([fac] if fac else [])
            num = lambda *ks: next((float(st[k]) for k in ks if str(st.get(k, '')).lstrip('-').replace('.', '').isdigit()), None)
            self.ins('card', id=i, game=game, name=n, category=cat, speed=speed_of(sub) or None, cost=cost,
                     power=num('power', 'attack'), health=num('health', 'toughness', 'life', 'hp'), regions=';'.join(regs),
                     rarity=rar, is_keyword=1 if cat == 'keyword' else 0)
            if cat == 'tribe': self.types[(game, n.lower())] = self.ins('type', game=game, name=n, tribe_entry=i)
        for i, sub in lib.execute("select id, subtypes from entities where game=? and category not in ('keyword','tribe')", (game,)):
            for t in types_of(sub):
                key = (game, t.lower())
                if key not in self.types: self.types[key] = self.ins('type', game=game, name=t, tribe_entry=None)
                self.ins('card_type', card=i, type=self.types[key])
        for s, r, d in lib.execute("select l.src, l.rel, l.dst from entity_links l join entities e on e.id=l.src where e.game=? and "
                                   "l.rel in ('generates','transforms_into','variant_of')", (game,)):
            self.ins('card_link', src=s, rel=r, dst=d)
        # a card's keywords are the ones in its own Keywords field
        for i, t in lib.execute("select id, text from entities where game=? and category not in ('keyword','tribe')", (game,)):
            m = KWFIELD.match(' '.join((t or '').split()))
            for k in (m.group(1).split(',') if m else []):
                kid = self.ref('keyword', k.strip())
                if kid: self.ins('card_keyword', card=i, keyword=kid)


def main():
    path = os.path.join(HERE, 'cards.sqlite')
    if os.path.exists(path): os.remove(path)
    out = sqlite3.connect(path); out.executescript(SCHEMA); L = Loader(out)
    for r in csv.DictReader(open(os.path.join(HERE, 'vocab.tsv')), delimiter='\t'):
        L.ins('vocab', **{k: r[k] for k in ('field', 'value', 'meaning', 'tree', 'causes', 'added')})
        if r['field'] == 'act':
            for ev in filter(None, r['causes'].split(';')): L.ins('causes', act=r['value'], event=ev)
    for game in sys.argv[1:]:
        L.game_data(game); n = 0
        for f in sorted(glob.glob(os.path.join(HERE, 'read', game, '*.jsonl'))):
            if f.endswith('proposals.jsonl'): continue
            for line in open(f):
                if line.strip(): L.record(json.loads(line)); n += 1
        print(game, n, 'records loaded')
    out.commit()


if __name__ == '__main__':
    main()

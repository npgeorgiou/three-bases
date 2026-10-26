"""Step 3 of the test: trigger pairs and compound tags computed from the placed tags.
Trigger pairs form only inside one ability: every trigger tag of the ability with every effect tag of the ability (a trigger
concept is never the effect) -> records_pairs(entity, ability, trigger, effect).
Compound tags form only inside one piece: tags are stored at their narrowest (an entry with aoe_damage has no separate damage
tag), so a compound tag is kept when the words its own pattern matched lie inside one piece, and dropped when they run across
pieces or abilities (the compound glued two effects together). A compound placed without known words, or not placed, is kept.
-> records_compound(entity, concept, kept, why). Usage: compute.py <copy.sqlite>"""
import collections, sys
import common as C

def main(path):
    c = C.connect(path); eff, trig = C.concept_kinds(c)
    scope = C.subtree(c, 'scope')
    c.executescript('DROP TABLE IF EXISTS records_pairs; CREATE TABLE records_pairs(entity INT, ability INT, trigger TEXT, effect TEXT);'
                    'DROP TABLE IF EXISTS records_compound; CREATE TABLE records_compound(entity INT, concept TEXT, kept INT, why TEXT);')
    by_ab = collections.defaultdict(set); ent_of = {}
    for e, k, a in c.execute('SELECT entity, concept, ability FROM entity_concepts WHERE ability IS NOT NULL'):
        by_ab[a].add(k); ent_of[a] = e
    trig_any = {i for (i,) in c.execute("SELECT id FROM concept_tree WHERE root='trigger'")}   # a trigger concept is never the effect
    for a, ks in by_ab.items():
        for t in ks & trig:
            for f in ks & eff - trig_any:
                if f != t: c.execute('INSERT INTO records_pairs VALUES(?,?,?,?)', (ent_of[a], a, t, f))
    COMP = {'aoe_damage', 'temporary_buff', 'permanent_growth'} | scope
    pl = collections.defaultdict(list)
    for e, k, how, cross in c.execute('SELECT ec.entity, ec.concept, l.how, l.cross FROM entity_concepts ec JOIN place_log l ON l.rid=ec.rowid'):
        if k in COMP: pl[(e, k)].append((how, cross))
    for (e, k), lst in pl.items():
        known = [x for h, x in lst if h in ('narrowed', 'pattern', 'note_text')]
        if not known: why, ok = ('not placed' if all(h in ('nowhere', 'no_text', 'entry_level') for h, _ in lst) else 'words unknown'), 1
        elif any(x == 0 for x in known): why, ok = 'inside one piece', 1
        else: why, ok = 'words cross pieces', 0
        c.execute('INSERT INTO records_compound VALUES(?,?,?,?)', (e, k, ok, why))
    c.commit()
    print('pairs', c.execute('SELECT count(*) FROM (SELECT DISTINCT entity, trigger, effect FROM records_pairs)').fetchone()[0],
          'compound kept/dropped', c.execute('SELECT sum(kept), sum(1-kept) FROM records_compound').fetchone())

if __name__ == '__main__': main(sys.argv[1])

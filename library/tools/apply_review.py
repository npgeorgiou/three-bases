"""Apply a Claude review file to one game. The file maps an entity id (or, for Marvel Snap, a name) to {add:[concept[:role]], drop:[...]}.
Each decision also applies to every other entry of the same game and category with the very same text (a potion and a card
with the same words are different things: a card does not inherit 'items_consumables' from the potion). Usage: apply_review.py <db> <game> <review.json>
An explicit drop removes the concept whatever method added it (the reviewer has read the text)."""
import json, sqlite3, sys
db, game, path = sys.argv[1:4]
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
rv = json.load(open(path, encoding='utf-8'))
bytext = {}
for i, t, k in q("select id,text,category from entities where game=? and text is not null", game): bytext.setdefault((t, k), []).append(i)
text = {i: (t, k) for i, t, k in q("select id,text,category from entities where game=?", game)}
n = 0
for key, r in rv.items():
    ids = [int(key)] if key.isdigit() else [i for (i,) in q("select id from entities where game=? and name=?", game, key)]
    targets = set()
    for i in ids:
        if i in text: targets |= {i} | set(bytext.get(text[i], []))
    # a keyword's correction also reaches the entries that only inherited the concept from it (method via_keyword)
    kwi = [i for i in ids if (q("select category from entities where id=?", i) or [(None,)])[0][0] == 'keyword']   # ids merged away later are skipped
    for k in kwi:
        linked = [x for (x,) in q("select distinct l.src from entity_links l join entities e on e.id=l.src where l.dst=? and e.game=? and l.rel in ('has_keyword','mentions_keyword','grants_keyword')", k, game)]
        linked_add = [x for (x,) in q("select distinct l.src from entity_links l join entities e on e.id=l.src where l.dst=? and e.game=? and l.rel='has_keyword'", k, game)]   # an entry that only mentions a keyword does not have it
        for item in r.get('drop', []):
            con, role = (item.split(':') + [None])[:2]
            for x in linked:
                if role: c.execute("delete from entity_concepts where entity=? and concept=? and role=? and method='via_keyword'", (x, con, role))
                else: c.execute("delete from entity_concepts where entity=? and concept=? and method='via_keyword'", (x, con))
        for item in r.get('add', []):
            con, role = (item.split(':') + ['does'])[:2]
            for x in linked_add: c.execute("insert or ignore into entity_concepts values(?,?,?,?,?)", (x, con, role, 'via_keyword', 'inherited from a reviewed keyword'))
    for e in targets:
        for item in r.get('drop', []):
            con, role = (item.split(':') + [None])[:2]
            if role: c.execute("delete from entity_concepts where entity=? and concept=? and role=?", (e, con, role))
            else:
                c.execute("delete from entity_concepts where entity=? and concept=?", (e, con))
                c.execute("delete from trigger_effect where entity=? and (trigger=? or effect=?)", (e, con, con))
        for item in r.get('add', []):
            con, role = (item.split(':') + ['does'])[:2]
            c.execute("insert or ignore into entity_concepts values(?,?,?,?,?)", (e, con, role, 'claude_review', 'hand-mapped from the text'))
            c.execute("update entity_concepts set method='claude_review' where entity=? and concept=? and role=? and method!='claude_review'", (e, con, role))   # a reviewed tag is no longer a pattern's or a keyword's
        n += 1
c.commit()
print(game, 'entries changed', n)

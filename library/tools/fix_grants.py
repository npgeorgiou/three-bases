"""Keyword 'grants' tags that came from text like "a minion WITH Taunt" are wrong: the card does not give the keyword.
For each via_keyword 'grants' tag whose keyword never appears after a give/gain verb in the entity text, the role becomes
'counters' (the text targets enemies with the keyword) or 'benefits' (it cares about your own units with it). Usage: fix_grants.py <db>"""
import re, sqlite3, sys
c = sqlite3.connect(sys.argv[1])
rows = c.execute("""select distinct e.id, e.text, ec.concept, k.name from entity_concepts ec join entities e on e.id=ec.entity
  join entity_links l on l.src=e.id and l.rel='grants_keyword' join entities k on k.id=l.dst
  join entity_concepts kc on kc.entity=k.id and kc.concept=ec.concept
  where ec.role='grants' and ec.method='via_keyword' and e.text is not null""").fetchall()
GIVE = r"\b(give|gives|giving|gain|gains|get|gets|have|has|grant|grants|with)\b"
n = {'counters': 0, 'benefits': 0}
for i, t, con, kn in rows:
    k = re.escape(kn.lower()); tl = t.lower()
    if re.search(r"\b(give|gives|giving|gain|gains|get|gets|grant|grants|gaining)\b[^.]{0,50}\b" + k, tl): continue
    if re.search(r"\b(have|has)\s+(\+\d+/\+\d+ and |\+\d+ \w+ and )?" + k, tl): continue   # "your minions have Rush" = grants
    if not re.search(r"\bwith\b[^.]{0,20}\b" + k, tl): continue
    if re.search(r"\b(create|creates|summon|summons|become|becomes|put|puts)\b[^.]{0,80}\bwith\b[^.]{0,30}\b" + k, tl): continue   # makes bodies with the keyword = grants
    role = 'counters' if re.search(r"\b(enemy|enemies|opponent'?s?|destroy|silence|banish|transform)\b[^.]{0,50}\bwith\b[^.]{0,20}\b" + k, tl) else 'benefits'
    have = c.execute("select 1 from entity_concepts where entity=? and concept=? and role=?", (i, con, role)).fetchone()
    c.execute("delete from entity_concepts where entity=? and concept=? and role='grants' and method='via_keyword'", (i, con))
    if not have: c.execute("insert into entity_concepts values(?,?,?,?,?)", (i, con, role, 'via_keyword', 'card refers to units with this keyword'))
    n[role] += 1
c.commit(); print('grants fixed', n)

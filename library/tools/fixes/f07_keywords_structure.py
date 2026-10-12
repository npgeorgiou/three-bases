"""Structure and keyword fixes. Usage: f07_keywords_structure.py <db>
  - death_count (a unit dies / counts deaths) is also placed under the trigger branch (it was only under condition and death);
    trigger_pairs.py still reads its patterns as effects and its trigger wording from its own list.
  - Keywords no entry linked to: cards that name the term get mentions_keyword; cards that describe its mechanic in other words
    get describes_keyword (Claude's reading of the keyword's definition: Hearthstone Enrage = "while damaged"; Darkest Dungeon
    Move = push back / pull forward, Death Blow = Death's Door). A keyword no card text names or describes is kept and marked
    extra.note 'used by no card text in this library' (game terms from the sources' glossaries, statuses, weapon properties)."""
import json, re, sqlite3, sys, collections
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
c.execute("INSERT OR IGNORE INTO concept_parents VALUES('death_count','trigger')")
M = {  # (game, keyword): (rel, pattern)
 ('hearthstone', 'Enrage'): ('describes_keyword', r"\bwhile damaged\b"),
 ('duelyst', 'Destructible'): ('mentions_keyword', r"\bdurability\b"),
 ('runeterra', 'Auto-Equip'): ('mentions_keyword', r"\bauto-?equip"),
 ('gwent', "Dragon's Dream"): ('mentions_keyword', r"dragon's dream"),
 ('darkest_dungeon', 'Death Blow'): ('describes_keyword', r"death ?blow|death's door"),
 ('darkest_dungeon', 'DODGE'): ('mentions_keyword', r"\bdodge\b"),
 ('darkest_dungeon', 'Move (effect)'): ('describes_keyword', r"\b(push(ed)? back|pull(ed)? forward|knockback)\b"),
 ('darkest_dungeon', 'Provision'): ('mentions_keyword', r"\bprovision"),
 ('darkest_dungeon', 'Torchlight'): ('mentions_keyword', r"\btorch"),
 ('darkest_dungeon', 'Virtue'): ('mentions_keyword', r"\bvirtue"),
 ('darkest_dungeon', 'Affliction Check'): ('mentions_keyword', r"\baffliction"),
 ('darkest_dungeon', 'Surprise Check'): ('mentions_keyword', r"\bsurprise"),
 ('into_the_breach', 'Kickoff Boosters'): ('mentions_keyword', r"kickoff boosters"),
 ('into_the_breach', 'Self-Repairing'): ('describes_keyword', r"self-repair"),
 ('into_the_breach', 'Hive Targeted'): ('mentions_keyword', r"psion tyrant"),
 ('dnd5e', 'Ammunition'): ('mentions_keyword', r"\bammunition\b"),
 ('wh_killteam', 'Rifles'): ('mentions_keyword', r"\bshuriken rifle|\branger long rifle"),
 ('wh_killteam', 'Nightmare Hulks'): ('mentions_keyword', r"nightmare hulk"),
}
C = collections.Counter()
for (g, k), (rel, p) in M.items():
    r = q("SELECT id FROM entities WHERE game=? AND category='keyword' AND name=?", g, k)
    if not r: continue
    kid = r[0][0]; rx = re.compile(p, re.I)
    for i, t in q("SELECT id, text FROM entities WHERE game=? AND category NOT IN ('keyword','tribe') AND text IS NOT NULL", g):
        if rx.search(t): C[rel] += c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (i, rel, kid, 'keyword term in text' if rel == 'mentions_keyword' else "text describes the keyword's mechanic (Claude's reading)")).rowcount
for i, e in q("SELECT id, extra FROM entities x WHERE category='keyword' AND NOT EXISTS (SELECT 1 FROM entity_links l WHERE l.dst=x.id)"):
    d = json.loads(e) if e else {}; d['note'] = 'used by no card text in this library'
    c.execute("UPDATE entities SET extra=? WHERE id=?", (json.dumps(d), i)); C['marked unused'] += 1
c.commit(); print(dict(C))

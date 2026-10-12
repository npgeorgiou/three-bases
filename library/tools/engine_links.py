"""Enabler -> payoff tags found through the combo validation set (tools/combos.tsv): payoff cards were tagged with what they DO,
not with what they WAIT FOR, so `combo` could not see the engine. Two wording rules add role 'benefits' (method engine_rule):
  trigger_watch  the trigger part of a clause ("Whenever a card is Exhausted, ...", "Whenever you lose HP ..."; not the card's own attack) names an effect:
                 the card benefits from that effect (Feel No Pain benefits exhaust).
  amplifier      the clause makes an effect bigger or repeats it ("deal N additional damage", "twice as many", "create twice that
                 many", "now deal damage instead", "Spell Damage"): the card benefits from that effect (Anointed Procession benefits summon).
A watched trigger also maps to the effect that feeds it: units entering -> summon, others' deaths -> sacrifice,
others taking damage -> damage. Keyword mentions in the plural are linked (mentions_keyword). Plus a few missing concept relations (origin claude_analysis), listed below. Reviewed drops are re-applied afterwards (regression.py enforce).
Usage: engine_links.py <db>"""
import re, sqlite3, sys
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
c.execute("DELETE FROM entity_concepts WHERE method='engine_rule'")
root = dict(q("SELECT id, root FROM concept_tree WHERE root IN ('effect','economy','combat')"))
root.update({k: 'effect' for k in ('summon',)})   # summon sits under role, but making units is what a token payoff waits for
TRIG = {'on_ally_play': 'summon', 'death_count': 'sacrifice', 'on_damaged': 'damage'}   # watched trigger -> the effect that feeds it
tpats = [(con, re.compile(p, re.I)) for con, p in q("SELECT concept, pattern FROM concept_patterns WHERE role='does' AND game IS NULL") if con in TRIG]
tpats.append(('on_ally_play', re.compile(r"\b(a|an|another|one or more)( nontoken)? (creature|minion|unit|follower|ally|card)s?( you control)? (enters|is summoned|is played)\b", re.I)))
pats = {}
for con, p, g in q("SELECT concept, pattern, game FROM concept_patterns WHERE role='does'"):
    if root.get(con) == 'effect':
        try: pats.setdefault(g, []).append((con, re.compile(p, re.I)))
        except re.error: pass
WATCH = re.compile(r"^\s*(whenever|each time|every time|after)\b([^,:]{3,90})[,:]", re.I)
AMP = re.compile(r"\badditional damage\b|\b(twice|three times) (as many|that many)\b|\bdeal \d+ more\b|\bdouble(s|d)? the\b|\btrigger(s)? twice\b|\b(now )?deal damage instead\b|\bspell damage\b|\bspell power\b", re.I)
SELFHIT = re.compile(r"^\s*(this|~|it|he|she|i|NAMEDCARD)\b.{0,30}\b(deals?|attacks?|strikes?|blocks?)\b", re.I)   # its own attack is on_attack, not a payoff
SPLIT = re.compile(r'(?<=[.!;])\s+|\n+')
n = 0
for e, g, t in q("SELECT id, game, text FROM entities WHERE text IS NOT NULL AND length(text) < 1500 AND category NOT IN ('tribe')"):
    P = pats.get(None, []) + pats.get(g, [])
    for cl in SPLIT.split(t):
        heads = []
        m = WATCH.search(cl)
        if m and not SELFHIT.search(m.group(2)): heads.append((m.group(2), 'trigger_watch'))
        if AMP.search(cl): heads.append((cl, 'amplifier'))
        for h, why in heads:
            hits = {con for con, p in P if p.search(h)}
            if why == 'trigger_watch': hits |= {TRIG[con] for con, p in tpats if p.search(cl)}
            for con in hits:
                if True:
                    n += c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (e, con, 'benefits', 'engine_rule', f'{why}: {h.strip()[:80]}')).rowcount
REL = [('spell_power', 'synergizes', 'direct_damage', 'more spell damage makes damage spells better'),
       ('spell_power', 'synergizes', 'aoe_damage', 'more spell damage makes area spells better'),
       ('repeat_trigger', 'synergizes', 'summon', 'doubled effects double the units summoned'),
       ('copy', 'synergizes', 'hand_size', 'copying cards fills the hand'),
       ('cost_reduction', 'enables', 'on_ally_play', 'cheaper cards mean more plays per turn'),
       ('cost_reduction', 'enables', 'on_spell', 'cheaper spells mean more casts per turn'),
       ('revive', 'synergizes', 'sacrifice', 'units that return are reusable fodder'),
       ('graveyard', 'synergizes', 'sacrifice', 'sacrificed units fill the graveyard'),
       ('discard', 'synergizes', 'hand_size', 'discarding empties the hand for empty-hand payoffs'),
       ('generate_cards', 'enables', 'on_ally_play', 'generated cards are extra plays')]
r = 0
for a, rel, b, note in REL:
    if a in root or q('SELECT 1 FROM concepts WHERE id=?', a):
        if not q('SELECT 1 FROM concept_relations WHERE a=? AND rel=? AND b=?', a, rel, b) and q('SELECT 1 FROM concepts WHERE id=?', b):
            c.execute("INSERT INTO concept_relations VALUES(?,?,?,?,'claude_analysis')", (a, rel, b, note)); r += 1
# keyword mentions in the plural ("Shivs", "Spirits") were missed by the keyword linker
k = 0
for kid, g, kn in q("SELECT id, game, name FROM entities WHERE category='keyword' AND length(name) >= 3"):
    rx = re.compile(r'\b' + re.escape(kn) + r'(s|es)\b', re.I)
    for e, t in q("SELECT id, text FROM entities WHERE game=? AND id<>? AND category NOT IN ('keyword','tribe') AND text LIKE ?", g, kid, f'%{kn}%'):
        if rx.search(t) and not q("SELECT 1 FROM entity_links WHERE src=? AND dst=?", e, kid):
            k += c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (e, 'mentions_keyword', kid, 'plural mention (engine_links.py)')).rowcount
c.commit()
print('plural keyword mentions added:', k)
print('engine_rule benefits tags:', n, ' concept relations added:', r)

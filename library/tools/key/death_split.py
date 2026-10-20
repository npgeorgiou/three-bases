"""Correct the answer keys for the death and leave-play triggers (Kaptain's decisions, 20 Oct 2026). Every death_trigger tag in
every key/<game>/key.json and key/kw_<game>/key.json is read with death_side.side() on its quoted words, or on the sentence
around them when the words don't say whose death it is: own death stays death_trigger, another unit's death becomes
other_death_trigger, leaving play becomes leave_trigger / other_leave_trigger. A death_count tag whose words are one single
death trigger ("whenever another creature dies") with no counting becomes other_death_trigger (death_count counts deaths).
Tags whose wording can't be read stay unchanged and are printed. FIXED holds the decisions Kaptain took per card.
Then the fill: the readers never had the leave-play and another-death concepts, so every key entry whose text has a sentence
that death_side.side() reads as leave_trigger, other_leave_trigger or other_death_trigger gets that tag when its key lacks it
(Kaptain's decision, 21 Oct 2026: what the key is missing is added generally). A sentence the key already tagged death_count,
on_kill or cheat_death for keeps that reading and gets no other_death_trigger.
Usage: death_split.py [apply]   (without apply: only prints what would change)"""
import json, os, re, sqlite3, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import death_side as D
# Kaptain's decisions per card (game, name): (concept to remove or None, concept to add or None)
FIXED = [
 ('wh_aos_4th', 'Anvil of Apotheosis: Nighthaunt Hero', None, 'other_death_trigger'),
 ('wh_killteam', 'Tracker', None, 'death_trigger'), ('wh_killteam', 'Demolition Veteran', None, 'death_trigger'),
 ('wh_killteam', 'Second in Command', None, 'other_death_trigger'),
 ('duelyst', 'Cassyva Soulreaper', None, 'on_kill'), ('duelyst', 'Inkhorn Gaze', None, 'on_kill'),
 ('duelyst', 'Mana Deathgrip', None, 'on_kill'), ('faeria', "Seifer's Wrath", None, 'on_kill'),
 ('into_the_breach', 'High Tide', None, 'terrain'), ('into_the_breach', 'Seismic Activity', None, 'terrain'),
 ('into_the_breach', 'Smoldering Psion', None, 'terrain'),
]
# Claude's reading of tags the wording rule can't settle (Kaptain reviews the list): (game, name) -> what the death_trigger tag becomes
READ = {('darkest_dungeon', 'Corpses'): {'other_death_trigger'}, ('darkest_dungeon', 'Corpse'): {'other_death_trigger'},
        ('duelyst', 'Abyssal Scar'): {'on_kill'}, ('duelyst', 'Grasp of Agony'): {'other_death_trigger'},
        ('hearthstone', 'Ascendance'): {'other_death_trigger'}, ('hearthstone', 'Food Fight'): {'other_death_trigger'},
        ('hearthstone', 'Starship'): {'other_death_trigger'}, ('inscryption', 'Gem Detonator (sigil)'): {'other_death_trigger'},
        ('into_the_breach', 'Tumblebug Leader'): {'other_death_trigger'}, ('mtg', 'Genju of the Fields'): {'other_death_trigger'},
        ('mtg', 'Death Tyrant'): {'other_death_trigger'}, ('wh_40k_10e', 'Insurmountable Odds'): {'other_death_trigger'},
        ('wh_bloodbowl3', 'Masters of Undeath'): {'other_death_trigger'}, ('wh_bloodbowl3', 'Plague Ridden'): {'other_death_trigger'},
        ('wh_killteam', 'Tyrant Guard'): {'other_death_trigger'}, ('wh_underworlds', 'A Hard Death'): {'other_death_trigger'},
        ('wh_underworlds', 'Dark Sacrifice'): {'other_death_trigger'}}
WORDS = {'other_death_trigger': r"\b(dies|die|destroyed|slain|incapacitated)\b", 'death_trigger': r"\b(incapacitated|destroyed|dies)\b",
         'on_kill': r"\bif it dies\b", 'terrain': r"\bwill become (a |an )?\w+|\bleave fire on death"}

def clause(text, words):
    t = text or ''; i = t.lower().find((words or '').lower()[:40])
    if i < 0: return t
    a = max(t.rfind('.', 0, i), t.rfind('\n', 0, i)) + 1
    b = [x for x in (t.find('.', i + len(words)), t.find('\n', i + len(words))) if x >= 0]
    return t[a:min(b) if b else len(t)]

def main(apply):
    c = sqlite3.connect(os.path.join(HERE, '..', '..', 'three-bases-library.sqlite'))
    ent = {i: (n, t, cat) for i, n, t, cat in c.execute('SELECT id, name, text, category FROM entities')}
    moved = collections.Counter(); doubt = []
    for g in sorted(os.listdir(HERE)):
        f = os.path.join(HERE, g, 'key.json')
        if not os.path.exists(f): continue
        key = json.load(open(f)); ch = False
        game = g[3:] if g.startswith('kw_') else g
        for i, v in key.items():
            n, text, cat = ent.get(int(i), ('', '', ''))
            new = []
            for k, w in v['tags']:
                if k not in ('death_trigger', 'death_count'): new.append([k, w]); continue
                spell = cat in D.SPELLS
                s = D.side(w, n, spell, game)
                if not s or s == {'?'} or (k == 'death_trigger' and s == {'death_trigger'} and not D.OWN_KW.search(w) and not re.search(r"\b(this|it|i|me|itself)\b", w, re.I) and (n or '#').lower().split(',')[0] not in w.lower()):
                    s2 = D.side(clause(text, w), n, spell, game); s = s2 if s2 and s2 != {'?'} else s
                if k == 'death_count':
                    cl = clause(text, w)
                    if s == {'other_death_trigger'} and D.SINGLE.search(w if len(w) > 12 else cl) and not D.NUM.search(w) and not D.COUNT.search(cl):
                        new.append(['other_death_trigger', w]); moved[game, 'death_count -> other_death_trigger'] += 1; ch = True
                    else: new.append([k, w])
                    continue
                if (game, n) in READ: s = READ[game, n]
                s -= {'?'}
                if not s: doubt.append((game, n, w, clause(text, w)[:150])); new.append([k, w]); continue
                if s == {'death_trigger'}: new.append([k, w]); continue
                if s == {'on_kill'}: new.append(['on_kill', w]); moved[game, 'death_trigger -> on_kill (spell)'] += 1; ch = True; continue
                for x in sorted(s):
                    if [x, w] not in new: new.append([x, w])
                moved[game, 'death_trigger -> ' + '+'.join(sorted(s))] += 1; ch = True
            v['tags'] = new
        for gg, nm, rm, add in FIXED:
            if gg != game or g.startswith('kw_'): continue
            for i, v in key.items():
                if ent.get(int(i), ('',))[0] != nm: continue
                text = ent[int(i)][1] or ''
                m = re.search(WORDS[add], text, re.I)
                if not m: continue   # a namesake whose text lacks the wording (two Kill Team "Tracker" entries)
                if add and not any(t[0] == add for t in v['tags']):
                    v['tags'].append([add, m.group(0) if m else nm]); moved[game, 'decision: add ' + add] += 1; ch = True
        for i, v in key.items():   # the fill
            n, text, cat = ent.get(int(i), ('', '', ''))
            have = {t[0] for t in v['tags']}
            for cl in re.split(r'(?<=[.!;])\s+|\n+', text or ''):
                if re.search(r"\bat least \d+|\b\d+ or more\b", cl) or ('cheat_death' in have and re.search(r"\bwould\b|\bfirst time\b", cl, re.I)): continue   # counting, or surviving death
                got = D.side(cl, n, cat in D.SPELLS, game) & {'leave_trigger', 'other_leave_trigger', 'other_death_trigger'}
                if 'other_death_trigger' in got and any(t[0] in ('death_count', 'on_kill', 'cheat_death') and t[1] and t[1].lower()[:30] in cl.lower() for t in v['tags']):
                    got.discard('other_death_trigger')
                m = re.search(D.TRIG, cl)
                for x in sorted(got - have):
                    v['tags'].append([x, (m.group(0) if m else cl)[:120]]); have.add(x); moved[game, 'fill: ' + x] += 1; ch = True
        if ch and apply: json.dump(key, open(f, 'w'), indent=0)
    for (g, what), n in sorted(moved.items()): print(f'{g:18} {what:45} {n}')
    print('doubtful (unchanged):', len(doubt))
    for d in doubt: print('  ', ' | '.join(d).replace('\n', ' '))

if __name__ == '__main__': main(sys.argv[1:] == ['apply'])

# Darkest Dungeon

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: single-player turn-based roguelike RPG (Red Hook, 2016). The player runs expeditions with a party of 4 heroes from a hamlet.
- Board: the party stands in ranks 1-4, the enemies in ranks 1-4 opposite. Each skill can be used only from certain ranks and hits only certain ranks; moving and being shuffled matters.
- Turn: each round every combatant acts once in speed order (speed plus a die roll).
- Resources: HP, Stress (afflictions at high stress, heart attack at maximum), the light meter, supplies (torches, food) and gold; heroes gain quirks and trinkets.
- Death: a hero at 0 HP is at Death's Door; a further hit can kill. Death is permanent.
- Win: finish dungeons and finally the Darkest Dungeon itself.
- Specific: hero classes, not factions; damage over time (Bleed, Blight), Stun, Mark and Guard are the core status effects.

## Sources and notes

Sources:
[1] https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide

Hero classes are not measured factions in the library; skill combos only.

## Combos [1]
- Blinding Gas / Disorienting Blast (Plague Doctor) + Finish Him (Bounty Hunter): stun, then extra damage on the stunned
- Barbaric YAWP! + Wicked Hack / Breakthrough (Hellion): stun, then mop up
- Cry Havoc (Houndmaster) + Transform (Abomination): stress relief offsets the transform's stress
- Daemon's Pull (Occultist) + Point Blank Shot (Highwayman): pull the toughest enemy to the front, then shoot
- Disorienting Blast (Plague Doctor) + Point Blank Shot: the Blast clears the corpses the Shot leaves
- If It Bleeds + Hound's Harry: same bleed party, not said to combine (not a case)

## Notes from the patterns check (24 Oct 2026)
Claude's reading of the card text, from the check against the key and the cases:
- "+N ... in the first round" is a condition on the round number (turn_number), not a start-of-combat effect.
- "resolve check" is the roll a hero makes at 100 stress (saving_throws); Resolve XP and Resolve Level are hero levels, not stress.
- "Deals damage (modifier -100%)" means the skill deals no damage (no_damage_output); "Effects: stun" disables the target.
- "Takes N ranks": a large monster fills several ranks (board_limit), it is not many units.
- "Class: X" on a trinket limits it to that hero class (tribal, as the key reads it).
- "trap resistance" and "stun / bleed / blight resistance" are resistances (saving_throws), not traps or the effect itself.
- Key disagreements kept, as Claude's judgement: "Targets all of enemy ranks" is one skill hitting several (multi_target_attack, by
  its definition) where the key reads aoe_damage only; self effects "(self)" are scope_self, which the key rarely tags; resisting
  bleed or blight keeps damage_over_time as a counter.

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name: name|expected concept|wording on the cards. Checked with coverage.py --mechanics (not yet run).
# Sources (21 Oct 2026): gameskinny.com/7xyiu/darkest-dungeon-party-building-guide (skill pairs and parties).
stun|disable|\bstun\b(?! (resistance|chance))
bleed|damage_over_time|\bbleed\b(?! (resistance|chance))
blight|damage_over_time|\bblight\b(?! (resistance|chance))
pull forward|forced_movement|\bpull\b
push back|forced_movement|\bknockback\b|\bpush\b
bonus damage on stunned|condition_life|\bvs\.? stunned\b|\bon stunned\b
stress relief|stress_morale|\bstress\b
transform (beast mode)|stances|\btransform\b
corpse clearing|board_clog|\bclear_corpses\b|\bcorpses?\b
# term: Stress: the party gains stress; some skills remove it (gameskinny: Cry Havoc removes stress, the Abomination's transform adds it).
# term: Corpses: killed enemies can leave corpses that hold their rank; some skills clear them (gameskinny).
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
combo	Blinding Gas	Finish Him	stun, then extra damage on the stunned	https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide
combo	Disorienting Blast	Finish Him	stun, then extra damage on the stunned	https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide
combo	Barbaric YAWP!	Wicked Hack	stun, then mop up	https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide
combo	Barbaric YAWP!	Breakthrough	stun, then mop up	https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide
combo	Cry Havoc	Transform	stress relief offsets the transform	https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide
combo	Daemon's Pull	Point Blank Shot	pull the toughest enemy forward, then shoot	https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide
combo	Disorienting Blast	Point Blank Shot	the Blast clears the Shot's corpses	https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide
```

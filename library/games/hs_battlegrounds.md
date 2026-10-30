# Hearthstone Battlegrounds

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: auto-battler mode of Hearthstone (2019); 8 players, last one standing wins (top 4 is a good result).
- Recruit phase: buy minions from the tavern with gold (gold grows each turn up to 10), sell them, refresh the tavern, upgrade the tavern tier (1 to 6, with tier 7 in some seasons).
- Combat phase: boards fight automatically; attacks go left to right. The loser takes damage from the winner's tavern tier plus its surviving minions' tiers.
- Triples: three copies of a minion merge into a golden one and give a discover from a higher tier.
- Tribes: Beast, Demon, Dragon, Elemental, Mech, Murloc, Naga, Pirate, Quilboar, Undead (the pool changes by season).
- Specific: heroes have their own hero powers; no factions in the library, combos only.

## Sources and notes

Sources:
[1] https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards

The library has no factions for Battlegrounds (minion types are tribes); combos only.

## Combos [1]
- Demons: Wrath Weaver + Floating Watcher (Watcher grows faster); Soul Juggler + Voidlord (Voidlord protects the Jugglers)
- Murlocs: Coldlight Seer, King Bagurgle or Gentle Megasaur + Brann Bronzebeard; Megasaur and Brann give poison and Divine Shield
- Beasts: Rat Pack or Cave Hydra + Mama Bear or Goldrinn, the Great Wolf
- Mechs: Replicating Menace or Mechano-Egg + Cobalt Guardian (Deathrattle mechs give it Divine Shield); Mechano-Egg + Baron
  Rivendare (doubled Deathrattle); Cobalt Guardian + Screwjank Clunker (stacked buffs)

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name: name|expected concept|wording on the cards. Checked with coverage.py --mechanics (not yet run).
# Sources (21 Oct 2026): gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards (named pairs per tribe).
deathrattle|death_trigger|\bdeathrattle\b
battlecry|on_play|\bbattlecry\b
divine shield|shield|\bdivine shield\b
poisonous|deathtouch|\bpoisonous\b
taunt|taunt|\btaunt\b
double battlecries (Brann)|repeat_trigger|\btrigger twice\b
double deathrattles (Rivendare)|repeat_trigger|\btrigger twice\b
summon minions|summon|\bsummon (a|an|two|three|\d+)\b
buff minions|stat_gain|\+\d+/\+\d+\b
tribes (beast, demon, murloc, mech)|tribal|\b(beast|demon|murloc|mech)s?\b
# term: The source names tribe decks (Demons, Murlocs, Beasts, Mechs); no rules text is given there.
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
combo	Wrath Weaver	Floating Watcher	Watcher grows faster	https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards
combo	Soul Juggler	Voidlord	Voidlord protects the Jugglers	https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards
combo	Coldlight Seer	Brann Bronzebeard	named as a combo	https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards
combo	King Bagurgle	Brann Bronzebeard	named as a combo	https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards
combo	Gentle Megasaur	Brann Bronzebeard	named as a combo	https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards
combo	Rat Pack	Mama Bear	named as a combo	https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards
combo	Rat Pack	Goldrinn, the Great Wolf	Goldrinn sets up the rats	https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards
combo	Cave Hydra	Mama Bear	named as a combo	https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards
combo	Cave Hydra	Goldrinn, the Great Wolf	Goldrinn sets up the Hydra	https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards
combo	Replicating Menace	Cobalt Guardian	Deathrattle summons give Divine Shield	https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards
combo	Mechano-Egg	Cobalt Guardian	Deathrattle summons give Divine Shield	https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards
combo	Mechano-Egg	Baron Rivendare	doubled Deathrattle	https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards
combo	Cobalt Guardian	Screwjank Clunker	stacked buffs	https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards
```

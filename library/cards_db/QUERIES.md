# Example queries (made by `examples.py` from cards.sqlite)

## Cards that stop enemies attacking or blocking (any game wording: Stun, Frostbite-like, keywords that mean it)

```sql
select distinct card from flat_concept where concept in ('disable','cant_attack')
```
471 cards: Abyssal Eye, Abyssal Guard, Acolyte's Reliquary, Acorn, the Hextechnician, Ahri (level 2), Airis, Altar to Unity, Amalgamation Of Vile Rites, Amateur Aeronaut, Ambush, Ancient Crocolith, Ancient Malediction ...

## Payoffs: cards that benefit from my other units dying, any way (trigger, condition, count, dead allies picked)

```sql
select distinct card from flat_ref where happening='dies' and role!='makes' and side in ('mine','any','') and coalesce(pick,'')!='self'
```
73 cards: Atakhan, Bringer of Ruin, Barkbeast, Black Spear, Boisterous Host, Chronobreak, Conductor Of The Mists, Crawling Sensation, Dawnspeakers, Elise's Crawling Sensation, Eternal Dancers, Faithful Wolfdog, For The Fallen ...

## Enablers: cards that kill or sacrifice my own units

```sql
select distinct card from flat_concept where concept='sacrifice'
```
60 cards: Amalgamation Of Vile Rites, Ancient Crocolith, Astral Fox, Atrocity, Blighted Caretaker, Bloodcursed Harpy, Chronicler of Ruin, Crumble, Death's Grasp, Dune Swallower, Encroaching Shadows, Ethereal Remitter ...

## Combos found between those two lists (connections.explain)

1560 pairs among the first 40 x 40, for example:

- Glimpse Beyond -> Dawnspeakers (condition: kill -> dies)
- Glimpse Beyond -> Lucian (condition: kill -> dies)
- Glimpse Beyond -> Radiant Guardian (condition: kill -> dies)
- Glimpse Beyond -> Vanguard Redeemer (condition: kill -> dies)
- Glimpse Beyond -> They Who Endure (condition: kill -> dies)
- Glimpse Beyond -> Fresh Offerings (condition: kill -> dies)
- Glimpse Beyond -> Kalista (condition: kill -> dies)
- Glimpse Beyond -> Rhasa the Sunderer (condition: kill -> dies)
- Glimpse Beyond -> Scuttlegeist (condition: kill -> dies)
- Glimpse Beyond -> Thresh (condition: kill -> dies)

## Same effect, compare cost: deal damage to anything (unit or player), cheapest first

```sql
select distinct d.card from flat_do d join card cd on cd.id=d.card where d.act='damage' and d.on_kind='any' order by cd.cost
```
45 cards: Atrocity, Blade's Edge, Blood in the Water, Chakram Dancer, Divine Draft, Ebb, Ebb and Flow, Ember Maiden, Ezreal's Mystic Shot, Flowing Chakram, Fracture, Fracture (created), Gangplank's Parrrley, Get Excited!, Icathian Rain ...

## Cards that copy keywords between units (a mechanic found while testing)

```sql
select distinct card from flat_do where act='copy_keywords'
```
32 cards: Adaptatron 3000, Beguiling Cobra, Breakneck Husk, Desperate Husk, Enraged Husk, Evelynn, Fading Husk, Give It All, Hardy Husk, Haunted Husk, Heart of the Fluft, Hive Herald ...

## What each region leans on (concepts with the highest share of the region's cards vs the game)

- Ionia: bounce_enemy (11), silence (33), swap (6), return_to_hand (52), shield (15)
- Noxus: on_discard (10), excess_damage (37), disable (21), on_life_loss (11), direct_damage (70)
- Demacia: extra_turn (23), multi_attack (15), damage_reduction (19), damage_prevention (19), shield (16)
- Piltover & Zaun: junk_cards (13), on_draw (18), recycle (11), on_spell (27), trap_secret (16)
- Freljord: regeneration (16), stat_loss (24), stat_multiply (27), aoe_damage (27), excess_damage (35)
- Shadow Isles: death_count (23), revive (19), sacrifice (34), self_mill (7), lifesteal (29)
- Bilgewater: self_mill (6), on_life_loss (21), steal (5), hand_disruption (5), rule_change (12)
- Targon: on_lifegain (5), combo_sequence (32), immunity (20), on_targeted (24), assists_support (11)
- Shurima: stealth (7), tutor (19), delayed (15), variety_payoff (11), rule_change (14)
- Bandle City: stacking_keyword (52), trap_secret (25), junk_cards (8), ping (65), spell_power (5)
- Runeterra: repeat_trigger (5), merge_attach (23), leave_trigger (14), board_presence (5), return_to_hand (15)
- Neutral: forced_movement (14), movement (13), variety_payoff (6), board_presence (6), variable_stats (12)
- Ironclad: forced_movement (9), movement (9), turn_start (6), damage (12), permanent_growth (5)
- Shadowfen: steal (5), debuff (7), variable_stats (8), turn_start (9), buff (7)
- Swarm: forced_movement (5), movement (5), turn_start (5), summon (8), damage (9)
- Winter: silence (8), resource_gain (7), variable_stats (6), buff (9), aoe_damage (5)

## Created-card chains (A creates B, B creates C)

- Death Ray - Mk 1 -> Death Ray - Mk 2 -> Death Ray - Mk 3
- Calculated Creations -> Ballistic Bot -> Ignition
- Lost Soul -> Twinblade Revenant -> Lost Soul
- Ebb -> Flow -> Ebb and Flow
- Tidal Wave -> Crashing Wave -> Colossal Wave
- Nukkle -> Mako -> Bull
- Draven's Whirling Death -> Draven -> Spinning Axe
- Katarina's Death Lotus -> Katarina -> Blade's Edge


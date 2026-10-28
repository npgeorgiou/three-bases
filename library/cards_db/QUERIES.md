# Example queries (made by `examples.py` from cards.sqlite)

Every question runs across all games: it uses only generic values (vocab.tsv) and concepts (the concept tree), never
a game's own words. The same question in `ask.py` form is given where one exists (`ask.py all ...`). Answers are grouped
by game, first cards only.

## Cards that stop enemy units acting (Runeterra Stun, Stormbound Freeze, keywords that mean it)

`ask.py all concept disable`

```sql
select distinct card from flat_concept where concept in ('disable','cant_attack')
```
- runeterra: 462 cards: Abyssal Eye, Abyssal Guard, Acolyte's Reliquary, Acorn, the Hextechnician, Ahri (level 2), Airis, Altar to Unity, Amalgamation Of Vile Rites ...
- stormbound: 9 cards: Blizzard Bombs, Freeze, Frosthexers, Glacier Palace, Iceflakes, Icicle Burst, Midwinter Chaos, Moment’s Peace ...

## Payoffs: cards that benefit from my other units dying, any way (trigger, condition, count, dead allies picked)

`ask.py all cares dies mine`

```sql
select distinct card from flat_ref where happening='dies' and role!='makes' and side in ('mine','any','') and coalesce(pick,'')!='self'
```
- runeterra: 71 cards: Atakhan, Bringer of Ruin, Barkbeast, Black Spear, Boisterous Host, Chronobreak, Conductor Of The Mists, Crawling Sensation, Dawnspeakers ...
- stormbound: 2 cards: Marked as Prey, Siro the Resurrector

## Enablers: cards that kill or sacrifice my own units

```sql
select distinct card from flat_concept where concept='sacrifice'
```
- runeterra: 54 cards: Amalgamation Of Vile Rites, Ancient Crocolith, Astral Fox, Atrocity, Blighted Caretaker, Bloodcursed Harpy, Chronicler of Ruin, Crumble ...
- stormbound: 6 cards: Pricey Freedom, Spooky Pumpkin, Stream of Consciousness, Temple of Space, Toxic Sacrifice, Yowling Weavers

## Combos between those two lists (connections.explain; `ask.py all link sacrifice death_trigger` asks the same
by concepts)

612 pairs inside a game, for example:

- runeterra: Glimpse Beyond -> Dawnspeakers (condition: kill -> dies)
- runeterra: Glimpse Beyond -> Lucian (condition: kill -> dies)
- runeterra: Glimpse Beyond -> Radiant Guardian (condition: kill -> dies)
- runeterra: Glimpse Beyond -> Vanguard Redeemer (condition: kill -> dies)
- runeterra: Glimpse Beyond -> They Who Endure (condition: kill -> dies)
- runeterra: Glimpse Beyond -> Fresh Offerings (condition: kill -> dies)
- runeterra: Glimpse Beyond -> Kalista (condition: kill -> dies)
- runeterra: Glimpse Beyond -> Rhasa the Sunderer (condition: kill -> dies)

194 pairs across games (the mechanics fit; useful for design questions), for example:

- runeterra: Glimpse Beyond -> stormbound: Marked as Prey (condition: kill -> dies)
- runeterra: Glimpse Beyond -> stormbound: Siro the Resurrector (state: dies)
- runeterra: Ancient Crocolith -> stormbound: Marked as Prey (condition: kill -> dies)
- runeterra: Ancient Crocolith -> stormbound: Siro the Resurrector (state: dies)
- runeterra: Oblivious Islander -> stormbound: Marked as Prey (condition: kill -> dies)

## How each game does "move enemy units" (push, pull, force to move)

`ask.py all compare forced_movement`

```sql
select distinct card from flat_concept where concept='forced_movement'
```
- runeterra: 8 cards: Bone Skewer, Fizz's Playful Trickster, Lissandra's Entomb, Playful Trickster, Sharesies, Sion, Sugary Snare, Tahm Kench
- stormbound: 33 cards: Absorbing Varmints, Agile Warriors, Angelic Tikas, Anointed Saviors, Armed Schemers, Catnip’s Charm, Chateau de Cardboard, Cheesy Lurers ...

## Cards that both move units and care about neighbours (is this combination of mechanics used, and where?)

`ask.py all both forced_movement adjacency`

```sql
select card from flat_concept where concept in ('movement','forced_movement') intersect select card from flat_concept where concept='adjacency'
```
- runeterra: 2 cards: Ahri, Ahri (level 2)
- stormbound: 17 cards: Agile Warriors, Angelic Tikas, Anointed Saviors, Armed Schemers, Catnip’s Charm, Chateau de Cardboard, Confuse, Crystalshields ...

## Turn-start effects, any game (Runeterra round start, Stormbound start of your turn)

`ask.py all concept turn_start`

```sql
select distinct card from flat_concept where concept='turn_start'
```
- runeterra: 115 cards: Abominable Guardian, Aphelios (level 2), Arena Bookie, Aurelion Sol, Aurelion Sol (level 2), Ballistic Bot, Barbed Chain, Beefcake Mayor ...
- stormbound: 39 cards: Acid Greenhorns, Big Sisters of Growth, Chateau de Cardboard, Copperskin Ranger, Crimson Sentry, Cursed Cemetery, Emerald Towers, Frozen Core ...

## Drain: damage, then the same amount to my side (heal the player, or strength to the drainer)

`ask.py all concept lifesteal`

```sql
select distinct card from flat_concept where concept='lifesteal'
```
- runeterra: 55 cards: Absorb Soul, Camavoran Dragon, Chakram Dancer, Crimson Pact, Darkwater Scourge, Deadbloom Wanderer, Divine Clerk, Doombeast ...
- stormbound: 8 cards: Amberhides, Drain, Feral Shamans, Hairy Chestnuts, Obelisk of Souls, Obsidian Butchers, Plague Monarchs, Witches of the Wild

## Cards that care about a unit having a status any game gives (stunned, frozen, poisoned ...)

`ask.py all cares given_keyword`

```sql
select distinct card from flat_ref where happening='given_keyword' and role!='makes'
```
- runeterra: 29 cards: Curtain Call, Deadly Flourish, Deathless Knight, Fae Bladetwirler, Falling Star, Greenglade Caretaker, Jhin, Kinkou Student ...
- stormbound: 26 cards: Acid Greenhorns, Amberhides, Big Sisters of Growth, Brood Sages, Copperskin Ranger, Crimson Sentry, Function Wilds, Green Prototypes ...

## Effects that grow with a count ("for each", "equal to"), any game

```sql
select distinct card from flat_do where params glob '*=[a-z]*'
```
- runeterra: 684 cards: Absorb Soul, Abyssal Eye, Abyssal Guard, Acolyte's Reliquary, Acorn, the Hextechnician, Adnere's Aviarists, Advance, Advanced Intel ...
- stormbound: 56 cards: Agile Warriors, Amberhides, Awakening of the Will, Beards of Crowglyph, Bigthrust Tigers, Blizzard Bombs, Booming Professors, Brood Sages ...

## Same effect, compare cost: deal damage to anything (unit, structure or player), cheapest first

```sql
select distinct d.card from flat_do d join card cd on cd.id=d.card where d.act='damage' and d.on_kind in ('any','anything') order by cd.cost
```
- runeterra: 45 cards: Atrocity, Blade's Edge, Blood in the Water, Chakram Dancer, Divine Draft, Ebb, Ebb and Flow, Ember Maiden ...
- stormbound: 16 cards: Booming Professors, Boomstick Officers, Chaotic Pupil, Crazy Bombers, Dark Harvest, Felflares, Melodious Sisters, Minion Launchers ...

## Cards that copy keywords between units (a mechanic found while testing)

```sql
select distinct card from flat_do where act='copy_keywords'
```
- runeterra: 31 cards: Adaptatron 3000, Beguiling Cobra, Breakneck Husk, Desperate Husk, Enraged Husk, Evelynn, Fading Husk, Give It All ...
- stormbound: 1 cards: Timber Alchemists

## What each faction or region leans on (concepts with the highest share of its cards vs its game)

- runeterra Ionia: bounce_enemy (11), silence (33), movement (6), swap (6), return_to_hand (52)
- runeterra Noxus: on_discard (10), excess_damage (37), disable (21), board_presence (6), on_life_loss (11)
- runeterra Demacia: extra_turn (23), multi_attack (15), damage_reduction (19), damage_prevention (19), shield (16)
- runeterra Piltover & Zaun: junk_cards (13), on_draw (18), recycle (11), on_spell (27), trap_secret (16)
- runeterra Freljord: regeneration (16), stat_loss (24), stat_multiply (27), aoe_damage (27), excess_damage (35)
- runeterra Shadow Isles: death_count (23), sacrifice (34), revive (19), self_mill (7), lifesteal (29)
- runeterra Bilgewater: steal (5), forced_movement (4), self_mill (6), on_life_loss (21), hand_disruption (5)
- runeterra Targon: on_lifegain (5), combo_sequence (32), immunity (20), on_targeted (24), assists_support (11)
- runeterra Shurima: stealth (7), tutor (19), debuff (5), variety_payoff (11), delayed (15)
- runeterra Bandle City: stacking_keyword (52), trap_secret (25), junk_cards (8), ping (65), spell_power (5)
- runeterra Runeterra: repeat_trigger (5), merge_attach (23), board_presence (5), variety_payoff (4), leave_trigger (14)
- stormbound Neutral: draw (5), generate_cards (4), variety_payoff (6), attack_now (4), copy (4)
- stormbound Ironclad: lanes (8), forced_movement (9), movement (9), death_trigger (4), positional (26)
- stormbound Shadowfen: lifesteal (7), damage_over_time (6), steal (5), ping (10), variable_stats (7)
- stormbound Swarm: direct_damage (7), tribal (6), summon (8), death_trigger (4), on_attack (5)
- stormbound Winter: disable (8), resource_gain (7), cant_attack (8), passive (8), silence (8)

## Created-card chains (A creates B, B creates C)

- Death Ray - Mk 1 -> Death Ray - Mk 2 -> Death Ray - Mk 3
- Calculated Creations -> Ballistic Bot -> Ignition
- Lost Soul -> Twinblade Revenant -> Lost Soul
- Ebb -> Flow -> Ebb and Flow
- Tidal Wave -> Crashing Wave -> Colossal Wave
- Nukkle -> Mako -> Bull
- Draven's Whirling Death -> Draven -> Spinning Axe
- Katarina's Death Lotus -> Katarina -> Blade's Edge


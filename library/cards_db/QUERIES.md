# Example queries (made by `examples.py` from cards.sqlite)

Every question runs across all games: it uses only generic values (vocab.tsv) and concepts (the concept tree), never
a game's own words. The same question in `ask.py` form is given where one exists (`ask.py all ...`). Answers are grouped
by game, first cards only.

## Cards that stop enemy units acting (Runeterra Stun, Stormbound Freeze, keywords that mean it)

`ask.py all concept disable`

```sql
select distinct card from flat_concept where concept in ('disable','cant_attack')
```
- monster_train: 43 cards: Alloyed Construct, Ambient Charge, Bone Dog's Favor, Bounty Stalker, Cuttlehex, Dante's Candle, Dazed, Deadweight ...
- runeterra: 462 cards: Abyssal Eye, Abyssal Guard, Acolyte's Reliquary, Acorn, the Hextechnician, Ahri (level 2), Airis, Altar to Unity, Amalgamation Of Vile Rites ...
- stormbound: 9 cards: Blizzard Bombs, Freeze, Frosthexers, Glacier Palace, Iceflakes, Icicle Burst, Midwinter Chaos, Moment’s Peace ...

## Payoffs: cards that benefit from my other units dying, any way (trigger, condition, count, dead allies picked)

`ask.py all cares dies mine`

```sql
select distinct card from flat_ref where happening='dies' and role!='makes' and side in ('mine','any','') and coalesce(pick,'')!='self'
```
- monster_train: 15 cards: A Fatal Melting, Big Sludge, Devourer of Death, Formless Child, Hallowed Halls, Memento Mori, Memories of the Melted, Molded ...
- runeterra: 71 cards: Atakhan, Bringer of Ruin, Barkbeast, Black Spear, Boisterous Host, Chronobreak, Conductor Of The Mists, Crawling Sensation, Dawnspeakers ...
- stormbound: 2 cards: Marked as Prey, Siro the Resurrector

## Enablers: cards that kill or sacrifice my own units

```sql
select distinct card from flat_concept where concept='sacrifice'
```
- monster_train: 15 cards: Cannibalize, Crushing Demise, Feast, Hallowed Drippings, Hallowed Halls, Imp-portant Work, Imp-pressive, Lady of the Reformed ...
- runeterra: 54 cards: Amalgamation Of Vile Rites, Ancient Crocolith, Astral Fox, Atrocity, Blighted Caretaker, Bloodcursed Harpy, Chronicler of Ruin, Crumble ...
- stormbound: 6 cards: Pricey Freedom, Spooky Pumpkin, Stream of Consciousness, Temple of Space, Toxic Sacrifice, Yowling Weavers

## Combos between those two lists, inside each game (connections.explain)

780 pairs, for example:

- monster_train: Imp-portant Work -> Memories of the Melted (condition: kill -> dies)
- monster_train: Imp-portant Work -> A Fatal Melting (condition: kill -> dies)
- monster_train: Imp-portant Work -> Memento Mori (condition: kill -> dies)
- monster_train: Imp-portant Work -> Rector Flicker (event: kill -> dies)
- monster_train: Imp-portant Work -> Primitive Mold (state: dies)
- monster_train: Imp-portant Work -> Sacred Wicks (state: dies)
- monster_train: Imp-portant Work -> Molded (state: dies)
- monster_train: Imp-portant Work -> Formless Child (state: dies)

## How each game does "move enemy units" (push, pull, force to move)

`ask.py all compare forced_movement`

```sql
select distinct card from flat_concept where concept='forced_movement'
```
- monster_train: 15 cards: Ascend, Cave In, Crypt Builder, Descend, Dripfall, Hidden Passage, Hosting Kin, March of Shields ...
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
- monster_train: 56 cards: Alloyed Construct, Apex Imp, Big Sludge, Bounty Stalker, Branded Warrior, Burnout, Dark Deal, Draff ...
- runeterra: 115 cards: Abominable Guardian, Aphelios (level 2), Arena Bookie, Aurelion Sol, Aurelion Sol (level 2), Ballistic Bot, Barbed Chain, Beefcake Mayor ...
- stormbound: 39 cards: Acid Greenhorns, Big Sisters of Growth, Chateau de Cardboard, Copperskin Ranger, Crimson Sentry, Cursed Cemetery, Emerald Towers, Frozen Core ...

## Drain: damage, then the same amount to my side (heal the player, or strength to the drainer)

`ask.py all concept lifesteal`

```sql
select distinct card from flat_concept where concept='lifesteal'
```
- monster_train: 4 cards: Crucible Collector, Immortal Trade, Morsel Excavator, Penumbra
- runeterra: 55 cards: Absorb Soul, Camavoran Dragon, Chakram Dancer, Crimson Pact, Darkwater Scourge, Deadbloom Wanderer, Divine Clerk, Doombeast ...
- stormbound: 8 cards: Amberhides, Drain, Feral Shamans, Hairy Chestnuts, Obelisk of Souls, Obsidian Butchers, Plague Monarchs, Witches of the Wild

## Cards that care about a unit having a status any game gives (stunned, frozen, poisoned ...)

`ask.py all cares given_keyword`

```sql
select distinct card from flat_ref where happening='given_keyword' and role!='makes'
```
- monster_train: 1 cards: Apex Imp
- runeterra: 29 cards: Curtain Call, Deadly Flourish, Deathless Knight, Fae Bladetwirler, Falling Star, Greenglade Caretaker, Jhin, Kinkou Student ...
- stormbound: 26 cards: Acid Greenhorns, Amberhides, Big Sisters of Growth, Brood Sages, Copperskin Ranger, Crimson Sentry, Function Wilds, Green Prototypes ...

## Effects that grow with a count ("for each", "equal to"), any game

```sql
select distinct card from flat_do where params glob '*=[a-z]*'
```
- monster_train: 166 cards: A Fatal Melting, Adaptive Mutation, Alloy of the Ancients, Alloyed Construct, Ambient Charge, Ancient Resonance, Ancient Synergy, Apex Imp ...
- runeterra: 684 cards: Absorb Soul, Abyssal Eye, Abyssal Guard, Acolyte's Reliquary, Acorn, the Hextechnician, Adnere's Aviarists, Advance, Advanced Intel ...
- stormbound: 56 cards: Agile Warriors, Amberhides, Awakening of the Will, Beards of Crowglyph, Bigthrust Tigers, Blizzard Bombs, Booming Professors, Brood Sages ...

## Mechanics, not cards

What "disable" (stop a unit acting) is built with, on the same cards (`ask.py all together disable`):

- cant_attack: monster_train 8 cards, runeterra 11 cards, stormbound 8 cards
- passive: monster_train 8 cards, runeterra 18 cards, stormbound 8 cards
- cheat_death: runeterra 7 cards
- silence: stormbound 8 cards
- forced_movement: monster_train 6 cards
- movement: monster_train 6 cards

Mechanics that feed "units dying" payoffs, inside each game (`ask.py all fed death_trigger`):

- destroy: monster_train 541 pairs, e.g. Molded -> Little Fade; runeterra 19385 pairs, e.g. Eternal Dancers -> Bladepierced Revenant; stormbound 283 pairs, e.g. Yowling Weavers -> Dreadful Keepers
- sacrifice: monster_train 250 pairs, e.g. Lady of the Reformed -> Little Fade; runeterra 6008 pairs, e.g. Mordekaiser -> Shackled Ghasts; stormbound 120 pairs, e.g. Yowling Weavers -> Dreadful Keepers
- removal: monster_train 126 pairs, e.g. Molded -> Little Fade; runeterra 5597 pairs, e.g. Kindred's Spirit Journey -> Shackled Ghasts; stormbound 103 pairs, e.g. Chilled Stonedames -> Marked as Prey
- on_kill: monster_train 151 pairs, e.g. Shattered Shell -> Little Fade; runeterra 2008 pairs, e.g. Mordekaiser -> Shackled Ghasts; stormbound 20 pairs, e.g. Spellbinder Zhevana -> Dreadful Keepers
- damage: monster_train 1076 pairs, e.g. Hoarfrost Effigy -> Little Fade; stormbound 721 pairs, e.g. Divine Reptiles -> Dreadful Keepers
- self_destruct: monster_train 373 pairs, e.g. Molded -> Little Fade; stormbound 20 pairs, e.g. Powder Tower -> Chaotic Pupil

Families of three mechanics that feed each other, starting from "summon" (`ask.py all chains summon`):

- summon -> on_ally_play -> random_effect (seen in runeterra)
- summon -> on_ally_play -> stacking_keyword (seen in runeterra)
- summon -> on_ally_play -> variable_stats (seen in runeterra)
- summon -> on_ally_play -> temporary_buff (seen in runeterra)
- summon -> tribal -> generate_cards (seen in runeterra)
- summon -> cant_block -> permanent_growth (seen in runeterra)

## A deck explained (`ask.py runeterra analyze "..."`), a Lucian/Senna deck from a deck guide

```
14 different cards, Shadow Isles 11, Demacia 3.
Plan:
- Your units die: made by Crumble, Glimpse Beyond, Piercing Darkness, Ravenous Butcher, Single Combat, Spirit Leech, The Ruination. Get value when they die: Cursed Keeper, Hapless Aristocrat, Lonely Chimeslime, The Undying. Level up from it: Lucian, Senna. Use it: Lonely Chimeslime, Senna, Sentinel of Light.
- Any units are killed: made by Crumble, Glimpse Beyond, Piercing Darkness, Ravenous Butcher, Single Combat, Spirit Leech, The Ruination. Level up from it: Senna.
- Lucian levels up when your units die (4+ times) or Senna, Sentinel of Light dies once.
- Senna levels up when any units are killed (3+ times).
Controls enemy units (damage, remove, stop, weaken): Crumble, Piercing Darkness, The Ruination.
Supports your units (stats, protection, combat keywords): Piercing Darkness, Senna.
Card flow (draw, create, choose): Glimpse Beyond, Lonely Chimeslime, Senna, Spirit Leech.
Puts extra units into play: Cursed Keeper, Hapless Aristocrat, The Undying.
Units that support cards can target: 9 (Cursed Keeper, Hapless Aristocrat, Lonely Chimeslime, Lucian, Ravenous Butcher, Senna, Senna, Sentinel of Light, Spirit Leech, The Undying).
Key cards (in most of the plan): Senna, The Ruination, Spirit Leech, Crumble, Ravenous Butcher.
Weak spots: none found.
```

## Decks: cards of one game that feed each other

- `ask.py stormbound deck "Wisp Cloud"` (Neutral, Winter): Wisp Cloud, Orgone Leechers, Frosthexers, Spellbinder Zhevana, Icicle Burst, Midwinter Chaos, Blizzard Bombs, Iceflakes, Erratic Neglects, Timber Alchemists, Stream of Consciousness, Temple of the Mind
- `ask.py stormbound deck "Doppelbocks"` (Neutral, Swarm): Doppelbocks, Faun Companions, Swarmcallers, Moonlit Aerie, Siegebreakers, Queen of Herds, Trusty Shepherds, Restless Goats, Bucks of Wasteland, Shady Ghoul, Martyr Spongers, Gathering Troupe
- `ask.py runeterra deck "Kalista"` (Neutral, Shadow Isles): Kalista, Glimpse Beyond, Kindred, Crawling Viperwyrm, Camavoran Dragon, Mistkeepers, The Darkin Halberd, The Harrowing, Shark Chariot, Pesky Specter, Eternal Dancers, Harrowing Return, Amalgamation Of Vile Rites, The Iron Conquest

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
- monster_train: 2 cards: Hoarfrost Effigy, Primordium
- runeterra: 31 cards: Adaptatron 3000, Beguiling Cobra, Breakneck Husk, Desperate Husk, Enraged Husk, Evelynn, Fading Husk, Give It All ...
- stormbound: 1 cards: Timber Alchemists

## What each faction or region leans on (concepts with the highest share of its cards vs its game)

- monster_train Hellhorned: temporary_buff (11), block_armor (12), damage_prevention (12), on_damaged (13), count_payoff (21)
- monster_train Awoken: on_lifegain (4), counterattack (7), regeneration (4), draw (11), heal (11)
- monster_train Stygian Guard: discard (6), on_spell (9), retain (4), stat_loss (5), damage_over_time (11)
- monster_train Umbra: lifesteal (4), on_sacrifice (14), shield (7), board_limit (4), overload_debt (4)
- monster_train Melting Remnant: death_trigger (17), self_destruct (16), cost_set (6), delayed (15), sacrifice (9)
- monster_train Wurmkin: cost_type (10), resource_gain (23), summon (4), damage_over_time (8), exhaust (19)
- monster_train Clanless: direct_damage (5), banish (10), turn_end (7), cant_attack (5), passive (20)
- runeterra Ionia: bounce_enemy (11), silence (33), movement (6), swap (6), return_to_hand (52)
- runeterra Noxus: on_discard (10), drawback (7), excess_damage (37), disable (21), board_presence (6)
- runeterra Demacia: extra_turn (23), damage_reduction (19), multi_attack (19), damage_prevention (19), shield (16)
- runeterra Piltover & Zaun: junk_cards (13), on_draw (18), recycle (11), on_spell (27), trap_secret (16)
- runeterra Freljord: attack_zero (21), regeneration (16), stat_loss (23), stat_multiply (27), aoe_damage (27)
- runeterra Shadow Isles: death_count (23), revive (20), sacrifice (34), self_mill (7), lifesteal (29)
- runeterra Bilgewater: steal (5), forced_movement (4), self_mill (6), on_life_loss (21), hand_disruption (5)
- runeterra Targon: on_lifegain (5), combo_sequence (32), immunity (20), on_targeted (24), assists_support (12)
- runeterra Shurima: stealth (7), tutor (19), delayed (26), debuff (5), variety_payoff (11)
- runeterra Bandle City: stacking_keyword (52), trap_secret (25), junk_cards (8), ping (65), spell_power (5)
- runeterra Runeterra: repeat_trigger (5), merge_attach (23), board_presence (5), variety_payoff (4), leave_trigger (14)
- stormbound Neutral: draw (5), generate_cards (4), variety_payoff (6), attack_now (4), copy (4)
- stormbound Ironclad: lanes (8), forced_movement (9), movement (9), death_trigger (4), positional (26)
- stormbound Shadowfen: lifesteal (7), damage_over_time (6), steal (4), ping (10), variable_stats (7)
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


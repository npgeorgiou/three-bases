# Example queries (made by `examples.py` from cards.sqlite)

Every question runs across all games: it uses only generic values (vocab.tsv) and concepts (the concept tree), never
a game's own words. The same question in `ask.py` form is given where one exists (`ask.py all ...`). Answers are grouped
by game, first cards only.

## Cards that stop enemy units acting (Runeterra Stun, Stormbound Freeze, keywords that mean it)

`ask.py all concept disable`

```sql
select distinct card from flat_concept where concept in ('disable','cant_attack')
```
- faeria: 67 cards: Annoying Gnat, Aquatic, Baeru, the First Wave, Boulder Thrower, Court Jester, Defender of the Homeland, Demonic Salmon, Devouring Plant ...
- monster_train: 43 cards: Alloyed Construct, Ambient Charge, Bone Dog's Favor, Bounty Stalker, Cuttlehex, Dante's Candle, Dazed, Deadweight ...
- runeterra: 463 cards: Abyssal Eye, Abyssal Guard, Acolyte's Reliquary, Acorn, the Hextechnician, Ahri (level 2), Airis, Altar to Unity, Amalgamation Of Vile Rites ...
- stormbound: 9 cards: Blizzard Bombs, Freeze, Frosthexers, Glacier Palace, Iceflakes, Icicle Burst, Midwinter Chaos, Moment’s Peace ...

## Payoffs: cards that benefit from my other units dying, any way (trigger, condition, count, dead allies picked)

`ask.py all cares dies mine`

```sql
select distinct card from flat_ref where happening='dies' and role!='makes' and side in ('mine','any','') and coalesce(pick,'')!='self'
```
- faeria: 10 cards: Bone Collector, Flying Piranha, Krog's Dinner, Mother of All Yaks, Ruunin, the Relentless, Shaytan Monstrosity, Soul Eater, Spirit Spice ...
- monster_train: 15 cards: A Fatal Melting, Big Sludge, Devourer of Death, Formless Child, Hallowed Halls, Memento Mori, Memories of the Melted, Molded ...
- runeterra: 63 cards: Atakhan, Bringer of Ruin, Barkbeast, Black Spear, Chronobreak, Crawling Sensation, Dawnspeakers, Elise's Crawling Sensation, Eternal Dancers ...
- stormbound: 2 cards: Marked as Prey, Siro the Resurrector

## Enablers: cards that kill or sacrifice my own units

```sql
select distinct card from flat_concept where concept='sacrifice'
```
- faeria: 12 cards: Ancient Gargoyle, Death Walker, Demon Wrangler, Doomgate, Door to Oblivion, Failed Experiment, Feed the Forest, Lord of the Wastes, Oath to Oblivion ...
- monster_train: 27 cards: Antumbra Morsel, Cannibalize, Crushing Demise, Eaten, Feast, Hallowed Drippings, Hallowed Halls, Imp-portant Work ...
- runeterra: 76 cards: Amalgamation Of Vile Rites, Ancient Crocolith, Astral Fox, Atrocity, Blighted Caretaker, Bloodcursed Harpy, Captivated Audience, Chronicler of Ruin ...
- stormbound: 7 cards: Final Sacrifice, Pricey Freedom, Spooky Pumpkin, Stream of Consciousness, Temple of Space, Toxic Sacrifice, Yowling Weavers

## Combos between those two lists, inside each game (connections.explain)

971 pairs, for example:

- faeria: Failed Experiment -> Soul Eater (condition: kill -> dies)
- faeria: Failed Experiment -> Swarming Carassius (condition: dies)
- faeria: Failed Experiment -> Mother of All Yaks (condition: dies)
- faeria: Failed Experiment -> Spirit Spice (condition: kill -> dies)
- faeria: Failed Experiment -> Krog's Dinner (state: dies)
- faeria: Failed Experiment -> Ruunin, the Relentless (state: dies)
- faeria: Failed Experiment -> Bone Collector (event: kill -> dies)
- faeria: Failed Experiment -> Spirit of Rebirth (event: kill -> dies)

## How each game does "move enemy units" (push, pull, force to move)

`ask.py all compare forced_movement`

```sql
select distinct card from flat_concept where concept='forced_movement'
```
- faeria: 39 cards: Airbot, Ancient Boar, Animated Banquet, Balloon Fish, Clockwork Yak, Coral Polliwog, Crackthorn Beast, Dash ...
- monster_train: 15 cards: Ascend, Cave In, Crypt Builder, Descend, Dripfall, Hidden Passage, Hosting Kin, March of Shields ...
- runeterra: 8 cards: Bone Skewer, Fizz's Playful Trickster, Lissandra's Entomb, Playful Trickster, Sharesies, Sion, Sugary Snare, Tahm Kench
- stormbound: 33 cards: Absorbing Varmints, Agile Warriors, Angelic Tikas, Anointed Saviors, Armed Schemers, Catnip’s Charm, Chateau de Cardboard, Cheesy Lurers ...

## Cards that both move units and care about neighbours (is this combination of mechanics used, and where?)

`ask.py all both forced_movement adjacency`

```sql
select card from flat_concept where concept in ('movement','forced_movement') intersect select card from flat_concept where concept='adjacency'
```
- faeria: 26 cards: Animated Banquet, Astral Weapon, Baeru, the First Wave, Dancing Blade, Flowersilk Faerie, Frog-Tosser, Grappling Hook, Khalim's Skyguard ...
- runeterra: 2 cards: Ahri, Ahri (level 2)
- stormbound: 17 cards: Agile Warriors, Angelic Tikas, Anointed Saviors, Armed Schemers, Catnip’s Charm, Chateau de Cardboard, Confuse, Crystalshields ...

## Turn-start effects, any game (Runeterra round start, Stormbound start of your turn)

`ask.py all concept turn_start`

```sql
select distinct card from flat_concept where concept='turn_start'
```
- faeria: 20 cards: Baeru, the First Wave, Blightborn Specter, Bloodstone Golem, Chrysalis, Crystalis, Devouring Plant, Emperor Kaios, Faeria Tree ...
- monster_train: 56 cards: Alloyed Construct, Apex Imp, Big Sludge, Bounty Stalker, Branded Warrior, Burnout, Dark Deal, Draff ...
- runeterra: 116 cards: Abominable Guardian, Aphelios (level 2), Arena Bookie, Aurelion Sol, Aurelion Sol (level 2), Ballistic Bot, Barbed Chain, Beefcake Mayor ...
- stormbound: 39 cards: Acid Greenhorns, Big Sisters of Growth, Chateau de Cardboard, Copperskin Ranger, Crimson Sentry, Cursed Cemetery, Emerald Towers, Frozen Core ...

## Drain: damage, then the same amount to my side (heal the player, or strength to the drainer)

`ask.py all concept lifesteal`

```sql
select distinct card from flat_concept where concept='lifesteal'
```
- faeria: 5 cards: Enslaved Priest, Kaios, Demented Overmind, Malevolent Spirit, Soul Drain, Spirit Theft
- monster_train: 4 cards: Crucible Collector, Immortal Trade, Morsel Excavator, Penumbra
- runeterra: 55 cards: Absorb Soul, Camavoran Dragon, Chakram Dancer, Crimson Pact, Darkwater Scourge, Deadbloom Wanderer, Divine Clerk, Doombeast ...
- stormbound: 8 cards: Amberhides, Drain, Feral Shamans, Hairy Chestnuts, Obelisk of Souls, Obsidian Butchers, Plague Monarchs, Witches of the Wild

## Cards that care about a unit having a status any game gives (stunned, frozen, poisoned ...)

`ask.py all cares given_keyword`

```sql
select distinct card from flat_ref where happening='given_keyword' and role!='makes'
```
- faeria: 12 cards: Destructive Volley, Drakkar Skycaptain, Enslaved Priest, Fugoro, Captain of the Gagana, Gift of Steel, Golden Aviary, Herald of War, Imperial Engineer ...
- monster_train: 90 cards: Alloy of the Ancients, Alloyed Construct, Apex Imp, Armor, Attuned, Awake, Battering Ram, Big Sludge ...
- runeterra: 111 cards: Animate, Arbiter of the Peak, Aspect of the Dragon, Ava Achiever, Balen the Benevolent, Big Game Tycoon, Caitlyn, Caitlyn (level 2) ...
- stormbound: 26 cards: Acid Greenhorns, Amberhides, Big Sisters of Growth, Brood Sages, Copperskin Ranger, Crimson Sentry, Function Wilds, Green Prototypes ...

## Effects that grow with a count ("for each", "equal to"), any game

```sql
select distinct card from flat_do where params glob '*=[a-z]*'
```
- faeria: 245 cards: Air Elemental, Airbot, Amai Merchant, Ancient Boar, Ancient Gargoyle, Animated Banquet, Annoying Gnat, Apex Predator ...
- monster_train: 166 cards: A Fatal Melting, Adaptive Mutation, Alloy of the Ancients, Alloyed Construct, Ambient Charge, Ancient Resonance, Ancient Synergy, Apex Imp ...
- runeterra: 687 cards: Absorb Soul, Abyssal Eye, Abyssal Guard, Acolyte's Reliquary, Acorn, the Hextechnician, Adnere's Aviarists, Advance, Advanced Intel ...
- stormbound: 56 cards: Agile Warriors, Amberhides, Awakening of the Will, Beards of Crowglyph, Bigthrust Tigers, Blizzard Bombs, Booming Professors, Brood Sages ...

## Mechanics, not cards

What "disable" (stop a unit acting) is built with, on the same cards (`ask.py all together disable`):

- cant_attack: monster_train 8 cards, runeterra 11 cards, stormbound 8 cards
- passive: monster_train 8 cards, runeterra 18 cards, stormbound 8 cards
- cheat_death: runeterra 7 cards
- silence: stormbound 8 cards
- movement: monster_train 6 cards
- forced_movement: monster_train 6 cards

Mechanics that feed "units dying" payoffs, inside each game (`ask.py all fed death_trigger`):

- destroy: faeria 1343 pairs, e.g. Rakoan Cannoneer -> Rakoan Shield Mates; monster_train 399 pairs, e.g. Little Fade -> Primordium; runeterra 12658 pairs, e.g. Kalista (level 2) -> Bladepierced Revenant; stormbound 283 pairs, e.g. Yowling Weavers -> Spare Dragonling
- sacrifice: faeria 384 pairs, e.g. Rakoan Cannoneer -> Rakoan Shield Mates; monster_train 295 pairs, e.g. Primordium -> Devourer of Death; runeterra 5616 pairs, e.g. Kalista (level 2) -> Bladepierced Revenant; stormbound 140 pairs, e.g. Yowling Weavers -> Spare Dragonling
- removal: faeria 320 pairs, e.g. Death's Desire -> Long-horned Yak; monster_train 93 pairs, e.g. Wicked Blaze -> Primordium; runeterra 3855 pairs, e.g. Spirit Journey -> Bladepierced Revenant; stormbound 103 pairs, e.g. Temple of the Mind -> Project PH03-NIX
- self_destruct: faeria 767 pairs, e.g. Doomgate, Door to Oblivion -> Long-horned Yak; monster_train 278 pairs, e.g. Little Fade -> Primordium; runeterra 6931 pairs, e.g. Kalista (level 2) -> Bladepierced Revenant; stormbound 20 pairs, e.g. Powder Tower -> Marked as Prey
- ping: faeria 417 pairs, e.g. Flame Thrower -> Laya, Lady of Sorrows; runeterra 5507 pairs, e.g. Anivia -> Bladepierced Revenant; stormbound 203 pairs, e.g. Acid Greenhorns -> Green Prototypes
- revive: runeterra 1035 pairs, e.g. Chronobreak -> Bladepierced Revenant

Families of three mechanics that feed each other, starting from "summon" (`ask.py all chains summon`):

- summon -> on_ally_play -> random_effect (seen in runeterra)
- summon -> temporary_buff -> buff (seen in faeria, runeterra)
- summon -> tribal -> cost_reduction (seen in runeterra, stormbound)
- summon -> temporary_buff -> destroy (seen in faeria, runeterra)
- summon -> on_ally_play -> spell_power (seen in monster_train, runeterra)
- summon -> temporary_buff -> variable_stats (seen in faeria, runeterra)

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

- `ask.py stormbound deck "Wisp Cloud"` (Neutral, Winter): Wisp Cloud, Orgone Leechers, Frosthexers, Spellbinder Zhevana, Icicle Burst, Midwinter Chaos, Blizzard Bombs, Iceflakes, Agile Warriors, Erratic Neglects, Lost Psyches, Va’vel the Looper
- `ask.py stormbound deck "Doppelbocks"` (Neutral, Swarm): Doppelbocks, Faun Companions, Swarmcallers, Moonlit Aerie, Siegebreakers, Queen of Herds, Headless Hotheads, Sparkly Kitties, Catnip’s Charm, Angelic Tikas, Lost Psyches, Agile Warriors
- `ask.py runeterra deck "Kalista"` (Neutral, Shadow Isles): Kalista, Darkwater Scourge, Mask Mother, Unspeakable Horror, Shark Chariot, Camavoran Dragon, Crawling Viperwyrm, Kindred, Mistkeepers, Harrowing Return, Amalgamation Of Vile Rites, Eternal Dancers, The Iron Conquest, Black Spear

## Same effect, compare cost: deal damage to anything (unit, structure or player), cheapest first

```sql
select distinct d.card from flat_do d join card cd on cd.id=d.card where d.act='damage' and d.on_kind in ('any','anything') order by cd.cost
```
- faeria: 21 cards: Blazing Salamander, Bottled Lightning, Boulder Thrower, Bursting Hippo, Crackthorn Beast, Dancing Blade, Derelict Tower, Detonate ...
- runeterra: 45 cards: Atrocity, Blade's Edge, Blood in the Water, Chakram Dancer, Divine Draft, Ebb, Ebb and Flow, Ember Maiden ...
- stormbound: 17 cards: Booming Professors, Boomstick Officers, Chaotic Pupil, Cheesy Lurers, Crazy Bombers, Dark Harvest, Felflares, Melodious Sisters ...

## Cards that copy keywords between units (a mechanic found while testing)

```sql
select distinct card from flat_do where act='copy_keywords'
```
- monster_train: 2 cards: Hoarfrost Effigy, Primordium
- runeterra: 32 cards: Adaptatron 3000, Beguiling Cobra, Breakneck Husk, Desperate Husk, Enraged Husk, Evelynn, Evelynn (level 2), Fading Husk ...
- stormbound: 1 cards: Timber Alchemists

## What each faction or region leans on (concepts with the highest share of its cards vs its game)

- faeria Neutral (Human): death_count (4), cost_set (6), damage_prevention (9), shield (7), taunt (15)
- faeria Blue: on_harvest (5), stat_multiply (6), turn_end (10), transform (4), on_draw (5)
- faeria Green: taunt (12), random_effect (12), terrain (9), defence_gain (35), death_trigger (10)
- faeria Red: on_fight (10), aoe_damage (13), ranged (5), direct_damage (11), damage (32)
- faeria Yellow: temporary_buff (4), sacrifice (6), on_attack (14), haste (6), removal (5)
- faeria Pandora: modal_choice (5), removal (4), aoe_damage (6), destroy (7), on_play (34)
- monster_train Hellhorned: temporary_buff (11), block_armor (12), damage_prevention (12), on_damaged (13), count_payoff (21)
- monster_train Awoken: on_lifegain (4), counterattack (7), regeneration (4), draw (11), heal (11)
- monster_train Stygian Guard: discard (6), on_spell (9), retain (4), stat_loss (5), damage_over_time (11)
- monster_train Umbra: lifesteal (4), on_sacrifice (14), shield (7), board_limit (4), overload_debt (4)
- monster_train Melting Remnant: other_death_trigger (8), countdown (15), self_destruct (16), cost_set (6), delayed (15)
- monster_train Wurmkin: cost_type (10), resource_gain (23), summon (4), damage_over_time (8), exhaust (19)
- monster_train Clanless: direct_damage (5), banish (10), turn_end (7), cant_attack (5), passive (20)
- runeterra Ionia: bounce_enemy (11), leave_trigger (10), spells_played_condition (12), silence (32), max_mana_condition (8)
- runeterra Noxus: combat_damage_threshold (9), on_discard (10), drawback (7), nexus_damage_condition (12), excess_damage (37)
- runeterra Demacia: extra_turn (23), damage_reduction (19), multi_attack (19), damage_prevention (19), shield (16)
- runeterra Piltover & Zaun: junk_cards (13), on_draw (18), recycle (12), on_spell (27), trap_secret (16)
- runeterra Freljord: attack_zero (21), regeneration (16), max_mana_condition (7), stat_loss (23), stat_multiply (27)
- runeterra Shadow Isles: death_count (23), revive (20), sacrifice (47), other_death_trigger (25), self_mill (7)
- runeterra Bilgewater: deck_condition (9), steal (5), forced_movement (4), self_mill (6), nexus_damage_condition (20)
- runeterra Targon: on_lifegain (5), stances (5), play_timing_condition (33), stat_condition (7), combo_sequence (32)
- runeterra Shurima: stealth (8), tutor (19), countdown (26), delayed (26), variety_payoff (11)
- runeterra Bandle City: stacking_keyword (53), trap_secret (25), junk_cards (8), ping (65), spell_power (5)
- runeterra Runeterra: repeat_trigger (7), board_presence (6), merge_attach (26), variety_payoff (5), other_leave_trigger (14)
- stormbound Neutral: draw (5), generate_cards (4), variety_payoff (6), attack_now (4), card_presence_condition (6)
- stormbound Ironclad: lanes (8), forced_movement (9), movement (9), death_trigger (4), positional (26)
- stormbound Shadowfen: lifesteal (7), damage_over_time (6), steal (4), ping (10), variable_stats (7)
- stormbound Swarm: direct_damage (8), tribal (6), summon (8), death_trigger (4), on_attack (5)
- stormbound Winter: disable (8), resource_gain (7), cant_attack (8), silence (8), passive (8)

## Created-card chains (A creates B, B creates C)

- Death Ray - Mk 1 -> Death Ray - Mk 2 -> Death Ray - Mk 3
- Calculated Creations -> Ballistic Bot -> Ignition
- Lost Soul -> Twinblade Revenant -> Lost Soul
- Ebb -> Flow -> Ebb and Flow
- Tidal Wave -> Crashing Wave -> Colossal Wave
- Nukkle -> Mako -> Bull
- Draven's Whirling Death -> Draven -> Spinning Axe
- Katarina's Death Lotus -> Katarina -> Blade's Edge


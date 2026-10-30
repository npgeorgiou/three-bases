# Example queries (made by `examples.py` from cards.sqlite)

Every question runs across all games: it uses only generic values (vocab.tsv) and concepts (the concept tree), never
a game's own words. The same question in `ask.py` form is given where one exists (`ask.py all ...`). Answers are grouped
by game, first cards only.

## Cards that stop enemy units acting (Runeterra Stun, Stormbound Freeze, keywords that mean it)

`ask.py all concept disable`

```sql
select distinct card from flat_concept where concept in ('disable','cant_attack')
```
- duelyst: 128 cards: Abyssal Tormentor, Aegis Barrier, Ancient Grove, Anti-Magic Field, Assassination Protocol, Avalanche, Aymara Healer, Backstab ...
- faeria: 67 cards: Annoying Gnat, Aquatic, Baeru, the First Wave, Boulder Thrower, Court Jester, Defender of the Homeland, Demonic Salmon, Devouring Plant ...
- inscryption: 25 cards: Aquasquirrel, Cat, Child 13, Child 13 (Awakened), Drowned Soul, Energy Conduit, Energy Conduit (sigil), Force Mage ...
- into_the_breach: 73 cards: A.C.I.D. Scorpion, Aerial Bombs, Alpha Burrower, Alpha Leaper, Alpha Mosquito, Alpha Scorpion, Alpha Spider, Artemis Artillery ...
- monster_train: 43 cards: Alloyed Construct, Ambient Charge, Bone Dog's Favor, Bounty Stalker, Cuttlehex, Dante's Candle, Dazed, Deadweight ...
- runeterra: 452 cards: Abyssal Eye, Abyssal Guard, Acolyte's Reliquary, Acorn, the Hextechnician, Ahri (level 2), Airis, Altar to Unity, Amateur Aeronaut ...
- stormbound: 9 cards: Blizzard Bombs, Freeze, Frosthexers, Glacier Palace, Iceflakes, Icicle Burst, Midwinter Chaos, Moment’s Peace ...
- sts1: 50 cards: Ascender's Bane, Barricade, Battle Trance, Blasphemy+, Blur, Bullet Time, Burn, Clumsy ...

## Payoffs: cards that benefit from my other units dying, any way (trigger, condition, count, dead allies picked)

`ask.py all cares dies mine`

```sql
select distinct card from flat_ref where happening='dies' and role!='makes' and side in ('mine','any','') and coalesce(pick,'')!='self'
```
- duelyst: 34 cards: Abyssal Scar (Bloodbound Spell), Amaranthine Vow, Blood Echoes, Bloodtide Priestess, Capricious Marauder, Corpse Combustion, Dance of Dreams, Death Knell ...
- faeria: 10 cards: Bone Collector, Flying Piranha, Krog's Dinner, Mother of All Yaks, Ruunin, the Relentless, Shaytan Monstrosity, Soul Eater, Spirit Spice ...
- inscryption: 6 cards: Corpse Eater, Corpse Maggots, Double Death, Gem Detonator, Gem Detonator (sigil), Necromancer
- monster_train: 15 cards: A Fatal Melting, Big Sludge, Devourer of Death, Formless Child, Hallowed Halls, Memento Mori, Memories of the Melted, Molded ...
- runeterra: 63 cards: Atakhan, Bringer of Ruin, Barkbeast, Black Spear, Chronobreak, Crawling Sensation, Dawnspeakers, Elise's Crawling Sensation, Eternal Dancers ...
- stormbound: 2 cards: Marked as Prey, Siro the Resurrector
- sts1: 2 cards: Fairy in a Bottle, Lizard Tail

## Enablers: cards that kill or sacrifice my own units

```sql
select distinct card from flat_concept where concept='sacrifice'
```
- duelyst: 26 cards: Abhorrent Unbirth, Aphotic Drain, Arid Unmaking, Blood Echoes, Cascading Rebirth, Cascading Rebirth (follow-up), Consuming Rebirth, Corporeal Cadence ...
- faeria: 12 cards: Ancient Gargoyle, Death Walker, Demon Wrangler, Doomgate, Door to Oblivion, Failed Experiment, Feed the Forest, Lord of the Wastes, Oath to Oblivion ...
- inscryption: 9 cards: Black Goat, Double Death, Game rule: Blood costs, Game rule: units can be sacrificed, M3atB0t, Master Bleene, Necromancer, Pharaoh's Pets ...
- into_the_breach: 1 cards: Arachnoid
- monster_train: 27 cards: Antumbra Morsel, Cannibalize, Crushing Demise, Eaten, Feast, Hallowed Drippings, Hallowed Halls, Imp-portant Work ...
- runeterra: 78 cards: Amalgamation Of Vile Rites, Ancient Crocolith, Astral Fox, Atrocity, Blighted Caretaker, Bloodcursed Harpy, Captivated Audience, Chronicler of Ruin ...
- stormbound: 7 cards: Final Sacrifice, Pricey Freedom, Spooky Pumpkin, Stream of Consciousness, Temple of Space, Toxic Sacrifice, Yowling Weavers
- sts1: 2 cards: Blasphemy, Blasphemy+

## Combos between those two lists, inside each game (connections.explain)

1527 pairs, for example:

- duelyst: Malice (token) -> Nether Summoning (state: dies)
- duelyst: Malice (token) -> Zurael, the Lifegiver (state: dies)
- duelyst: Malice (token) -> Amaranthine Vow (state: dies)
- duelyst: Malice (token) -> Vale Ascension (state: dies)
- duelyst: Malice (token) -> Legion (boss, Boss33) (state: dies)
- duelyst: Malice (token) -> Legion (boss, Boss33_1) (state: dies)
- duelyst: Malice (token) -> Legion (boss, Boss33_2) (state: dies)
- duelyst: Malice (token) -> Legion (boss, Boss33_3) (state: dies)

## How each game does "move enemy units" (push, pull, force to move)

`ask.py all compare forced_movement`

```sql
select distinct card from flat_concept where concept='forced_movement'
```
- duelyst: 36 cards: Blink, Cade the Desolator, Chaos Elemental, Chittering Tiller, Cindera, Daemonic Lure, Envybaer, Flicker ...
- faeria: 39 cards: Airbot, Ancient Boar, Animated Banquet, Balloon Fish, Clockwork Yak, Coral Polliwog, Crackthorn Beast, Dash ...
- inscryption: 36 cards: 49er, Bloodhound, Bolthound, Bonehound, Burrower, Burrowing Trap, Clinger, Elk ...
- into_the_breach: 80 cards: A.C.I.D. Projector, A.C.I.D. Tank, AP Cannon, Aegon Mortar, Aerial Bombs, Alpha Beetle, Alpha Bouncer, Alpha Gastropod ...
- monster_train: 15 cards: Ascend, Cave In, Crypt Builder, Descend, Dripfall, Hidden Passage, Hosting Kin, March of Shields ...
- runeterra: 8 cards: Bone Skewer, Fizz's Playful Trickster, Lissandra's Entomb, Playful Trickster, Sharesies, Sion, Sugary Snare, Tahm Kench
- stormbound: 33 cards: Absorbing Varmints, Agile Warriors, Angelic Tikas, Anointed Saviors, Armed Schemers, Catnip’s Charm, Chateau de Cardboard, Cheesy Lurers ...
- sts1: 61 cards: After Image, After Image+, Alpha, Alpha+, Backstab, Ball Lightning, Battle Hymn, Battle Hymn+ ...

## Cards that both move units and care about neighbours (is this combination of mechanics used, and where?)

`ask.py all both forced_movement adjacency`

```sql
select card from flat_concept where concept in ('movement','forced_movement') intersect select card from flat_concept where concept='adjacency'
```
- duelyst: 16 cards: Aspect of the Wyrm, Black Locust, Cade the Desolator, Chittering Tiller, Cindera, D3cepticle, Drake Dowager, Ghost Lynx ...
- faeria: 28 cards: Animated Banquet, Astral Weapon, Baeru, the First Wave, Dancing Blade, Flowersilk Faerie, Flying Piranha, Frog-Tosser, Grappling Hook ...
- inscryption: 26 cards: 49er, Clinger, Elk, Elk Fawn, Ghost Ship, Headless Horseman, Hefty, Lonely Wizbot ...
- into_the_breach: 88 cards: A.C.I.D. Hornet, A.C.I.D. Projector, A.C.I.D. Tank, AP Cannon, Aegon Mortar, Aerial Bombs, Alpha Beetle, Alpha Bouncer ...
- runeterra: 2 cards: Ahri, Ahri (level 2)
- stormbound: 17 cards: Agile Warriors, Angelic Tikas, Anointed Saviors, Armed Schemers, Catnip’s Charm, Chateau de Cardboard, Confuse, Crystalshields ...

## Turn-start effects, any game (Runeterra round start, Stormbound start of your turn)

`ask.py all concept turn_start`

```sql
select distinct card from flat_concept where concept='turn_start'
```
- duelyst: 65 cards: Architect-T2K5, Barren Shrike, Battle Pet, Biomimetic Hulk, Build, CALIBERO, CALIBERO 2.0 (boss), Cindera ...
- faeria: 20 cards: Baeru, the First Wave, Blightborn Specter, Bloodstone Golem, Chrysalis, Crystalis, Devouring Plant, Emperor Kaios, Faeria Tree ...
- inscryption: 24 cards: Boon of the Ambidextrous, Boon of the Forest, Dire Wolf Pup, Elk Fawn, Fledgling, GR1ZZ, GR1ZZ (Beast Form), Great Kraken ...
- into_the_breach: 39 cards: Air Strike, Beetle Leader, Blood Psion, Boom Cannon, Burning Mortar, Cannon-Bot, Cannon-Mech, Emerging ...
- monster_train: 56 cards: Alloyed Construct, Apex Imp, Big Sludge, Bounty Stalker, Branded Warrior, Burnout, Dark Deal, Draff ...
- runeterra: 116 cards: Abominable Guardian, Aphelios (level 2), Arena Bookie, Aurelion Sol, Aurelion Sol (level 2), Ballistic Bot, Barbed Chain, Beefcake Mayor ...
- stormbound: 39 cards: Acid Greenhorns, Big Sisters of Growth, Chateau de Cardboard, Copperskin Ranger, Crimson Sentry, Cursed Cemetery, Emerald Towers, Frozen Core ...
- sts1: 229 cards: Acid Slime (L), Acid Slime (M), Acid Slime (S), After Image, After Image+, Ambrosia, Anchor, Armaments ...

## Drain: damage, then the same amount to my side (heal the player, or strength to the drainer)

`ask.py all concept lifesteal`

```sql
select distinct card from flat_concept where concept='lifesteal'
```
- duelyst: 3 cards: Desolator, Firestorm Mantra, Munch
- faeria: 5 cards: Enslaved Priest, Kaios, Demented Overmind, Malevolent Spirit, Soul Drain, Spirit Theft
- monster_train: 4 cards: Crucible Collector, Immortal Trade, Morsel Excavator, Penumbra
- runeterra: 55 cards: Absorb Soul, Camavoran Dragon, Chakram Dancer, Crimson Pact, Darkwater Scourge, Deadbloom Wanderer, Divine Clerk, Doombeast ...
- stormbound: 8 cards: Amberhides, Drain, Feral Shamans, Hairy Chestnuts, Obelisk of Souls, Obsidian Butchers, Plague Monarchs, Witches of the Wild

## Cards that care about a unit having a status any game gives (stunned, frozen, poisoned ...)

`ask.py all cares given_keyword`

```sql
select distinct card from flat_ref where happening='given_keyword' and role!='makes'
```
- duelyst: 32 cards: Afterblaze, Bloodbound Mentor, Cannon of MECHAZ0R, Chassis of MECHAZ0R, Cloudcaller, Crossbones, Cryoblade, Cryptographer ...
- faeria: 8 cards: Destructive Volley, Enslaved Priest, Fugoro, Captain of the Gagana, Herald of War, Imperial Engineer, Seek Shelter, Triton Trainer, Windborne Emissary
- inscryption: 8 cards: Ant Queen, Ants, Emerald Power, Flying Ant, Green Mage, Master Bleene, True Scholar, Worker Ant
- into_the_breach: 7 cards: Fire, Flame Thrower, Heat Engines, Nanofilter Mending, Sand Tile, Smoke Tile, Storm Generator
- monster_train: 90 cards: Alloy of the Ancients, Alloyed Construct, Apex Imp, Armor, Attuned, Awake, Battering Ram, Big Sludge ...
- runeterra: 87 cards: Arbiter of the Peak, Ava Achiever, Big Game Tycoon, Caitlyn, Caitlyn (level 2), Curtain Call, Deadly Flourish, Death Mark ...
- stormbound: 26 cards: Acid Greenhorns, Amberhides, Big Sisters of Growth, Brood Sages, Copperskin Ranger, Crimson Sentry, Function Wilds, Green Prototypes ...
- sts1: 232 cards: After Image, After Image+, Ambrosia, Anchor, Ancient Potion, Armaments, Armaments+, Artifact ...

## Effects that grow with a count ("for each", "equal to"), any game

```sql
select distinct card from flat_do where params glob '*=[a-z]*'
```
- duelyst: 369 cards: Abhorrent Unbirth, Abyssal Juggernaut, Abyssal Tormentor, Accumulonimbus, Ace, Aegis Barrier, Aerial Rift, Aethermaster ...
- faeria: 250 cards: Air Elemental, Airbot, Amai Merchant, Ancient Boar, Ancient Gargoyle, Animated Banquet, Annoying Gnat, Apex Predator ...
- inscryption: 84 cards: !CORRUPTED, Ancient Fir, Ant Queen, Ants, Aquasquirrel, Armored, Bell Ringer, Bell Tentacle ...
- into_the_breach: 158 cards: A.C.I.D., A.C.I.D. Firefly, A.C.I.D. Hornet, A.C.I.D. Pool, A.C.I.D. Projector, A.C.I.D. Scorpion, A.C.I.D. Tank (unit), A.C.I.D. Tile ...
- monster_train: 166 cards: A Fatal Melting, Adaptive Mutation, Alloy of the Ancients, Alloyed Construct, Ambient Charge, Ancient Resonance, Ancient Synergy, Apex Imp ...
- runeterra: 698 cards: Absorb Soul, Abyssal Eye, Abyssal Guard, Acolyte's Reliquary, Acorn, the Hextechnician, Adnere's Aviarists, Advance, Advanced Intel ...
- stormbound: 56 cards: Agile Warriors, Amberhides, Awakening of the Will, Beards of Crowglyph, Bigthrust Tigers, Blizzard Bombs, Booming Professors, Brood Sages ...
- sts1: 337 cards: Acid Slime (L), Acid Slime (M), Acid Slime (S), After Image, After Image+, Aggregate, Anchor, Armaments ...

## Mechanics, not cards

What "disable" (stop a unit acting) is built with, on the same cards (`ask.py all together disable`):

- attack_lock: duelyst 18 cards, monster_train 3 cards
- cant_attack: duelyst 22 cards, into_the_breach 4 cards, monster_train 8 cards, runeterra 46 cards, stormbound 7 cards
- immobilize: duelyst 18 cards, stormbound 6 cards
- passive: duelyst 22 cards, into_the_breach 4 cards, monster_train 8 cards, runeterra 78 cards, stormbound 7 cards
- cant_move: duelyst 2 cards, into_the_breach 2 cards
- stances: runeterra 9 cards

Mechanics that feed "units dying" payoffs, inside each game (`ask.py all fed death_trigger`):

- destroy: duelyst 3172 pairs, e.g. Fireblaze Obelysk -> Khanuum-ka; faeria 1015 pairs, e.g. Flash Salmon -> Long-horned Yak; inscryption 466 pairs, e.g. Mage Knight -> Ouroboros; into_the_breach 10 pairs, e.g. Walking Bomb -> Ice Tile; monster_train 348 pairs, e.g. Bogdeep Cocoon -> Echowright; runeterra 22558 pairs, e.g. Ekko (level 2) -> Bladepierced Revenant; stormbound 264 pairs, e.g. Toxic Sacrifice -> Green Prototypes
- self_destruct: duelyst 1788 pairs, e.g. Fireblaze Obelysk -> Khanuum-ka; faeria 653 pairs, e.g. Flash Salmon -> Long-horned Yak; inscryption 431 pairs, e.g. Mage Knight -> Ouroboros; into_the_breach 8 pairs, e.g. Walking Bomb -> Ice Tile; monster_train 296 pairs, e.g. Bogdeep Cocoon -> Echowright; runeterra 19820 pairs, e.g. Ekko (level 2) -> Bladepierced Revenant; stormbound 20 pairs, e.g. Powder Tower -> Project PH03-NIX
- sacrifice: duelyst 1521 pairs, e.g. Fireblaze Obelysk -> Khanuum-ka; faeria 387 pairs, e.g. Rakoan Cannoneer -> Rakoan Shield Mates; inscryption 54 pairs, e.g. Necromancer -> Ouroboros; into_the_breach 6 pairs, e.g. Arachnoid Injector -> Ice Tile; monster_train 305 pairs, e.g. Primordium -> Devourer of Death; runeterra 8133 pairs, e.g. Ekko (level 2) -> Bladepierced Revenant; stormbound 140 pairs, e.g. Toxic Sacrifice -> Green Prototypes
- turn_end: duelyst 1814 pairs, e.g. Fireblaze Obelysk -> Khanuum-ka; faeria 473 pairs, e.g. Flash Salmon -> Long-horned Yak; into_the_breach 6 pairs, e.g. Walking Bomb -> Ice Tile; monster_train 276 pairs, e.g. Primordium -> Devourer of Death; runeterra 19731 pairs, e.g. Ekko (level 2) -> Bladepierced Revenant
- activated: faeria 297 pairs, e.g. Doomgate, Door to Oblivion -> Long-horned Yak; inscryption 27 pairs, e.g. Master Bleene -> Ouroboros; into_the_breach 6 pairs, e.g. Walking Bomb -> Ice Tile; monster_train 210 pairs, e.g. Steel Pulleyclaw -> Echowright; stormbound 20 pairs, e.g. Temple of the Mind -> Snowmasons
- removal: duelyst 568 pairs, e.g. Rasha's Curse (follow-up) -> Khanuum-ka; faeria 134 pairs, e.g. Death's Desire -> Long-horned Yak; inscryption 30 pairs, e.g. Skel-e-latcher -> Ouroboros; runeterra 5806 pairs, e.g. Mordekaiser -> Bladepierced Revenant; stormbound 103 pairs, e.g. Temple of the Mind -> Snowmasons

Families of three mechanics that feed each other, starting from "summon" (`ask.py all chains summon`):

- summon -> banish -> activated (seen in duelyst, runeterra)
- summon -> delayed -> countdown (seen in monster_train, runeterra)
- summon -> banish -> removal (seen in duelyst, runeterra)
- summon -> delayed -> cost_set (seen in monster_train, runeterra)
- summon -> banish -> drawback (seen in runeterra)
- summon -> start_of_game -> delayed (seen in runeterra)

## A deck explained (`ask.py runeterra analyze "..."`), a Lucian/Senna deck from a deck guide

```
14 different cards, Shadow Isles 11, Demacia 3.
Plan:
- Your units die: made by Crumble, Glimpse Beyond, Ravenous Butcher, Single Combat, Spirit Leech, The Ruination. Get value when they die: Cursed Keeper, Hapless Aristocrat, Lonely Chimeslime, The Undying. Level up from it: Lucian, Senna. Use it: Lonely Chimeslime, Senna, Sentinel of Light.
- Any units are killed: made by Crumble, Glimpse Beyond, Piercing Darkness, Ravenous Butcher, Single Combat, Spirit Leech, The Ruination. Level up from it: Senna.
- Lucian levels up when your units die (4+ times) or Senna, Sentinel of Light dies once.
- Senna levels up when your units are killed (3+ times).
Controls enemy units (damage, remove, stop, weaken): Crumble, Piercing Darkness, Single Combat.
Supports your units (stats, protection, combat keywords): Lucian, Piercing Darkness, Senna, Senna, Sentinel of Light, The Undying.
Card flow (draw, create, choose): Glimpse Beyond, Lonely Chimeslime, Senna, Spirit Leech.
Puts extra units into play: Cursed Keeper, Hapless Aristocrat, The Undying.
Units that support cards can target: 9 (Cursed Keeper, Hapless Aristocrat, Lonely Chimeslime, Lucian, Ravenous Butcher, Senna, Senna, Sentinel of Light, Spirit Leech, The Undying).
Key cards (in most of the plan): Senna, Spirit Leech, The Ruination, Crumble, Ravenous Butcher.
Weak spots: none found.
```

## Decks: cards of one game that feed each other

- `ask.py stormbound deck "Wisp Cloud"` (Neutral, Winter): Wisp Cloud, Orgone Leechers, Frosthexers, Spellbinder Zhevana, Icicle Burst, Midwinter Chaos, Blizzard Bombs, Agile Warriors, Temple of the Mind, Moment’s Peace, Angelic Tikas, Catnip’s Charm
- `ask.py stormbound deck "Doppelbocks"` (Neutral, Swarm): Doppelbocks, Faun Companions, Swarmcallers, Moonlit Aerie, Siegebreakers, Queen of Herds, Trusty Shepherds, Restless Goats, Counselor Ahmi, Shady Ghoul, Pan Heralds, Dreadfauns
- `ask.py runeterra deck "Kalista"` (Neutral, Shadow Isles): Kalista, Shackled Ghasts, Kindred, The Harrowing, Shark Chariot, Eternal Dancers, Harrowing Return, Amalgamation Of Vile Rites, The Iron Conquest, Chronicler of Ruin, The Undying, Maokai, Gwen, Threshold of the Grey

## Same effect, compare cost: deal damage to anything (unit, structure or player), cheapest first

```sql
select distinct d.card from flat_do d join card cd on cd.id=d.card where d.act='damage' and d.on_kind in ('any','anything') order by cd.cost
```
- duelyst: 49 cards: Armada, Avalanche, Battle Panddo, Blinding Snowstorm, Blistering Skorn, Bloodtear Alchemist, Boulder Hurl, Chromatic Cold ...
- faeria: 21 cards: Blazing Salamander, Bottled Lightning, Boulder Thrower, Bursting Hippo, Crackthorn Beast, Dancing Blade, Derelict Tower, Detonate ...
- runeterra: 45 cards: Atrocity, Blade's Edge, Blood in the Water, Chakram Dancer, Divine Draft, Ebb, Ebb and Flow, Ember Maiden ...
- stormbound: 17 cards: Booming Professors, Boomstick Officers, Chaotic Pupil, Cheesy Lurers, Crazy Bombers, Dark Harvest, Felflares, Melodious Sisters ...

## Cards that copy keywords between units (a mechanic found while testing)

```sql
select distinct card from flat_do where act='copy_keywords'
```
- duelyst: 4 cards: Abhorrent Unbirth, Kahlmar the Spell Eater, Neurolink, S.I.L.V.E.R.
- into_the_breach: 1 cards: Psionic Receiver
- monster_train: 2 cards: Hoarfrost Effigy, Primordium
- runeterra: 32 cards: Adaptatron 3000, Beguiling Cobra, Breakneck Husk, Desperate Husk, Enraged Husk, Evelynn, Evelynn (level 2), Fading Husk ...
- stormbound: 1 cards: Timber Alchemists

## What each faction or region leans on (concepts with the highest share of its cards vs its game)

- duelyst Lyonar Kingdoms: on_lifegain (7), aura (5), multi_attack (5), taunt (11), heal (13)
- duelyst Songhai Empire: flanking (14), temporary_buff (5), on_spell (12), generate_cards (10), trap_secret (4)
- duelyst Vetruvian Imperium: rows (9), self_destruct (9), merge_attach (6), steal (6), haste (14)
- duelyst Abyssian Host: other_death_trigger (11), terrain (14), sacrifice (12), destroy (21), stat_loss (4)
- duelyst Magmar Aspects: cheat_death (9), attack_lock (4), revive (8), disable (4), permanent_growth (14)
- duelyst Vanar Kindred: territory_trigger (7), disable (10), base_resource_gain (4), resource_gain (4), attack_lock (6)
- duelyst Neutral: deck_modification (6), quests (5), random_ability (6), ranged (18), copy (16)
- duelyst Boss: merge_attach (4), multi_attack (6), turn_start (16), area_templates (6), revive (6)
- duelyst Tutorial: on_play (4)
- faeria Neutral (Human): death_count (4), cost_set (6), damage_reduction (9), shield (7), immobilize (16)
- faeria Blue: cant_move (6), control_reward (4), on_harvest (5), stat_multiply (6), turn_end (10)
- faeria Green: taunt (12), immobilize (12), random_effect (12), defence_gain (35), death_trigger (10)
- faeria Red: on_fight (10), aoe_damage (13), ranged (5), direct_damage (11), damage (32)
- faeria Yellow: temporary_buff (4), sacrifice (6), on_attack (14), haste (6), removal (4)
- faeria Pandora: modal_choice (5), removal (4), aoe_damage (6), destroy (7), zone_control (7)
- inscryption Beast: free_play (4), multi_attack (8), stealth (8), immunity (6), variable_stats (8)
- inscryption Technology: stances (8), territory_trigger (4), aoe_damage (4), link_formation (10), ping (6)
- inscryption Magick: aura (6), defence_gain (5), draw (4), self_destruct (4), card_presence_condition (5)
- into_the_breach Prime: lanes (4), spell_or_skill (21), forced_movement (15), aoe_damage (10), spell_power (4)
- into_the_breach Brute: forced_movement (17), spell_or_skill (21), area_templates (18), movement (19), ping (16)
- into_the_breach Ranged: area_templates (18), spell_or_skill (19), ping (16), forced_movement (11), cant_attack (10)
- into_the_breach Science: shield (5), spell_power (7), spell_or_skill (20), immunity (11), movement (18)
- into_the_breach Any: defence_gain (5), tribal (9), stat_gain (6), heal (6), spell_power (6)
- monster_train Hellhorned: temporary_buff (11), block_armor (12), damage_reduction (12), on_damaged (13), count_payoff (21)
- monster_train Awoken: on_lifegain (4), counterattack (7), regeneration (4), draw (11), heal (11)
- monster_train Stygian Guard: discard (6), on_spell (9), retain (4), stat_loss (5), damage_over_time (11)
- monster_train Umbra: lifesteal (4), on_sacrifice (14), shield (7), overload_debt (4), tribal (18)
- monster_train Melting Remnant: other_death_trigger (8), countdown (15), self_destruct (16), cost_set (6), delayed (15)
- monster_train Wurmkin: cost_type (10), resource_gain (23), summon (4), damage_over_time (8), lanes (27)
- monster_train Clanless: direct_damage (5), banish (10), turn_end (7), cant_attack (5), passive (20)
- runeterra Ionia: bounce_enemy (11), leave_trigger (10), spells_played_condition (12), silence (17), max_mana_condition (8)
- runeterra Noxus: combat_damage_threshold (9), on_discard (10), drawback (7), nexus_damage_condition (12), excess_damage (37)
- runeterra Demacia: extra_turn (23), multi_attack (19), damage_reduction (38), shield (16), spell_power (8)
- runeterra Piltover & Zaun: junk_cards (13), on_draw (18), recycle (12), on_spell (27), trap_secret (16)
- runeterra Freljord: attack_zero (21), regeneration (16), max_mana_condition (7), stat_loss (23), stat_multiply (27)
- runeterra Shadow Isles: death_count (23), revive (20), sacrifice (48), other_death_trigger (25), self_mill (7)
- runeterra Bilgewater: deck_condition (9), steal (5), forced_movement (4), self_mill (6), nexus_damage_condition (20)
- runeterra Targon: on_lifegain (5), stances (5), play_timing_condition (33), stat_condition (7), combo_sequence (32)
- runeterra Shurima: stealth (8), tutor (19), countdown (26), delayed (26), variety_payoff (11)
- runeterra Bandle City: stacking_keyword (53), trap_secret (25), junk_cards (8), ping (65), spell_power (5)
- runeterra Runeterra: repeat_trigger (7), board_presence (6), merge_attach (26), variety_payoff (5), other_leave_trigger (14)
- stormbound Neutral: draw (5), generate_cards (4), variety_payoff (6), zone_control (10), attack_now (4)
- stormbound Ironclad: lanes (8), forced_movement (9), movement (9), death_trigger (4), positional (26)
- stormbound Shadowfen: lifesteal (7), damage_over_time (6), steal (4), ping (10), variable_stats (7)
- stormbound Swarm: direct_damage (8), tribal (6), summon (8), death_trigger (4), on_attack (5)
- stormbound Winter: base_resource_gain (7), disable (7), immobilize (6), resource_gain (7), cant_attack (8)
- sts1 Silent: damage_over_time (9), on_discard (5), discard (11), draw (18), aoe_damage (8)
- sts1 Watcher: stances (22), leave_trigger (6), retain (11), information (4), recycle (5)
- sts1 Defect: movement (23), slots_queue (26), repeat_trigger (31), card_presence_condition (25), forced_movement (29)
- sts1 Ironclad: attack_gain (8), aoe_damage (7), exhaust (26), debuff (7), tribal (17)
- sts1 Colorless: cost_set (11), retain (6), exhaust (33), activated (31), cant_attack (10)

## Created-card chains (A creates B, B creates C)

- Death Ray - Mk 1 -> Death Ray - Mk 2 -> Death Ray - Mk 3
- Calculated Creations -> Ballistic Bot -> Ignition
- Lost Soul -> Twinblade Revenant -> Lost Soul
- Ebb -> Flow -> Ebb and Flow
- Tidal Wave -> Crashing Wave -> Colossal Wave
- Nukkle -> Mako -> Bull
- Draven's Whirling Death -> Draven -> Spinning Axe
- Katarina's Death Lotus -> Katarina -> Blade's Edge


# Step 2 findings (by script, 6 Nov 2026)

## Keyword cases the records miss (checks/gwent/mech_cases.md)
# Gwent mechanics cases (gw01-gw85) and region queries

Rows added to cases/mechanics.tsv: 85 (gw01-gw85, one per keyword in read/gwent/keywords.jsonl). No gwent card has a Keywords field, so every expected is `text:<regex>` (case-sensitive keyword word on the card text).
Rows passing: 68. Rows failing: 17 (after fixes, run.py gwent: 124 of 174 cases before the region edits, 135 after).

Queries: keyword rows via flat_ref.keyword/via, flat_do.keyword_ref/via, flat_if.via, flat_when.via, plus layer rows for Deploy (played, self), Order (activated, self), Melee/Ranged (front_row/back_row position), Spawn/Create (create, summon, copy, choose_card, row_effects), Summon, Coin/Tribute/Fee/Profit (secondary_resource mana_gain/spend_mana), Exposed (keyword_removed Armor), Deathblow (killed), Ambush/Spring (trap_secret, trap_activated).

## Failing rows

RECORDS: gw20 Storm: Bride of the Sea, Messenger of the Sea, Kelpie, Anglerfish
RECORDS: gw22 Frost: Imlerith's Wrath, Avallac'h, Tempest, Scepter of Storms, Wild Hunt Bruiser, Caranthir: Golden Child
RECORDS: gw23 Fog: Avallac'h, Tempest, Scepter of Storms
RECORDS: gw24 Rain: Avallac'h, Tempest, Scepter of Storms, Bride of the Sea, Messenger of the Sea, Anglerfish
RECORDS: gw30 Disloyal: Braathens, Artaud Terranova, The Eternal Eclipse
RECORDS: gw32 Patience: Alumni
RECORDS: gw33 Deathwish: Whispering Hillock, Plague Maiden, Endless Voyage, Deranged Corsair, Sove
RECORDS: gw34 Armor: Dennis Cranmer, Reckless Flurry, Vlodimir von Everec, Living Armor, Piercing Missile, Professor, Affan Hillergrand, Ulula
RECORDS: gw35 Crew: King Henselt
RECORDS: gw48 Infused: Van Moorlehem Servant
RECORDS: gw50 Bonded: One-Eyed Betsy, Free Company, Iron Falcon Troubadour, The Mushy Truffle
RECORDS: gw54 Spring: Spring Equinox
RECORDS: gw55 Discard: Eist Tuirseach, Bjorn Stormursson
RECORDS: gw58 Echo: Lady of the Lake
RECORDS: gw63 Predator: Adda: Striga, Cockatrice, Werewolf, Kikimore Stalker
RECORDS: gw64 Symbiosis: Aucwenn
RECORDS: gw84 Reset: Damien de la Tour, Viraxas: Prince

Notes: gw48 Infused: one of the two expected cards is a text that says 'excluding Infused' (Van Moorlehem Servant), the other is found. gw63 Predator: the records keep no trace of the Predator condition (target power lower than own), so the query finds none. gw20-gw24 weather: the misses mention Rain/Storm/Frost/Fog as conditions or spawned row effects the records do not tie to the keyword.

## Region queries changed (only the query column)

rgw08 play_card/summon/look/reveal on enemy deck or discard; rgw14 damage or kill from an ability limited to the back (ranged) row; rgw17 play_card/summon from own deck; rgw20 revive or play/summon from own discard; rgw23 silence, or cant/move/transform on enemy; rgw24 cant on enemy or silence; rgw25 create/summon/copy plus Consume; rgw27 trap_secret, trap_activated, Ambush; rgw28 revive or play/summon/return from discard; rgw29 damage or kill on enemy; rgw30 mana_gain/spend_mana on secondary_resource (Coins).
All eleven now pass. None left unsaid.

## Word check flags (patterns/gwent_flags.tsv)
card	name	pattern	requires	text
756877	Eventide Plunder	KW	name:fee	 4-provision cost unit with a fee.
757137	Braathens	KW	name:disloyal	loy: create and play a bronze disloyal unit from your starting deck.
757397	Sigi Reuven: Mastermind	V16	value:cost_change|cost_set	te 9: play 2 instead. tribute costs 2 less for each unique gang category

## Text audit (audit_text.py gwent)
player named: 0
deal damage: 0
draw: 0
create: 1  e.g. Radeyah
summon: 0
heal: 0
kill or destroy: 1  e.g. Insanity
discard: 0
stat gift: 0
cost less: 1  e.g. Sigi Reuven: Mastermind
this round: 1  e.g. Madame Luiza
everywhere: 0
for each: 4  e.g. Glustyworp, King Roegner, Zoltan: Warrior, Seagull
random: 2  e.g. Boris, Wheel of Fortune
spells and Skills: 0
level up: 0
this turn: 5  e.g. Aglaïs, Arena Ghoul, Leticia Charbonneau, Aen Elle Aristocrat
land act: 0
adjacent: 1  e.g. Armorer's Workshop
harvest: 0
nearby: 0
stun: 0
dispel: 0
double: 0
gwent: 16 text words without rows

## Link audit (audit_links.py gwent)
gwent: 23 link findings
  1 nothing makes "summon" (mine), needed by 3: Cyrus Engelkind Hemmelfart, Eternal Fire Inquisitor, Procession of Penance
  1 nothing makes "create" (mine), needed by 3: Cyrus Engelkind Hemmelfart, Eternal Fire Inquisitor, Procession of Penance
  1 nothing makes "summon" (any), needed by 2: Adda: Striga, Lonely Champion
  1 nothing makes "create" (any), needed by 2: Adda: Striga, Lonely Champion
  1 nothing makes "summon" (enemy), needed by 1: Adda: Striga
  1 nothing makes "create" (enemy), needed by 1: Adda: Striga
  1 nothing makes "trap_activated" (mine), needed by 1: Elven Scout
  1 nothing makes "exhausted" (mine), needed by 1: Blood Money
  1 nothing makes "counts_down" (mine), needed by 1: King Henselt
  1 nothing makes "removed_from_deck" (enemy), needed by 1: Sandor de Baccalà
  1 nothing makes "keyword_used Rain" (any), needed by 1: Sea Serpent
  1 nothing makes "keyword_used Storm" (any), needed by 1: Sea Serpent
  9 Aucwenn give_keywords Wandering Treant but never makes it: "Symbiosis Deploy: Infuse all your Naiads with the Nature category, wherever they are. When"
  10 284 cards tagged cooldowns before have no row for it, e.g. Geralt: Igni
  10 123 cards tagged summon before have no row for it, e.g. Zoltan: Scoundrel
  10 122 cards tagged graveyard before have no row for it, e.g. Iris von Everec
  10 112 cards tagged coin_economy before have no row for it, e.g. Lined Pockets
  10 110 cards tagged generate_cards before have no row for it, e.g. Operator
  10 107 cards tagged ping before have no row for it, e.g. Chironex
  10 97 cards tagged tutor before have no row for it, e.g. Triss Merigold
  10 95 cards tagged stat_condition before have no row for it, e.g. Geralt: Igni
  10 73 cards tagged condition_count before have no row for it, e.g. Redanian Knight
  10 67 cards tagged on_ally_play before have no row for it, e.g. Roach

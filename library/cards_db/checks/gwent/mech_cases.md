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

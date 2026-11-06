# Gwent step 2, fixer 2 (RULE items 1, 2, 3, 4, 5, 12, 13, 14)

Only cases/mechanics.tsv gw rows changed (backup was the file before). Result of `cases/run.py gwent`: gw rows 80 of 85 pass (before 68).

## Changes
- Item 1 (gw20, 22, 23, 24, 30, 33, 34, 35, 48, 50, 58): each query gets a union over every with-column (flat_do on_with/to_with, flat_when obj_with/actor_with, flat_if of_with/ev_obj_with/ev_actor_with, flat_ref obj_with/actor_with) holding `keyword is|not|in <id>` of the keyword. Rows really hold it there. Fixes Storm, Fog, Rain, Armor, Crew, Infused, Bonded, Echo and most Frost/Disloyal.
- Item 2 (gw22, 23, 24): regex narrowed so it skips card names: `(?<!Biting )Frost`, `(?<!Impenetrable )Fog`, `(?<!Torrential )Rain` (card names, not the keyword).
- Item 3 (gw34 Armor): query adds flat_do `params like '%armor%'` (ignore_armor, attr=armor) and flat_if `attr='armor'`.
- Item 5 (gw84 Reset): query adds flat_do `act='refresh'`.
- Item 12 (gw54 Spring): regex skips the card name: `Spring(?! Equinox)`.
- Item 13 (gw32 Patience): query adds flat_if `attr='keyword_amount'` and flat_do params with keyword_amount.
- Item 14 (gw33 Deathwish): query adds flat_when `event='dies' and obj_pick='self'` (same shape as the Deploy row); passes.
- Item 1 remaining Disloyal/Frost cards are not in any row (below).

## Not fixed
- CODE: item 4 (gw63 Predator, gw64 Symbiosis): flat_ref/flat_* hold no row naming the keyword for Adda: Striga, Cockatrice, Werewolf, Kikimore Stalker, Aucwenn (I searched all four flat tables for the keyword id on Cockatrice and Aucwenn: none). Needs load.py/flat.py to write the keyword_condition reference.
- gw22 Frost 18 of 19 (94.7%, needs 95%): Caranthir: Golden Child, "damage dealt by Frost in the last 5 enemy turns", rows are `amount_unstated`, no Frost id anywhere. Data/code, not a query change.
- gw30 Disloyal 18 of 19: Braathens, the "Disloyal" is in the Create filter which the rows do not keep (create row has no with). Data/code.
- gw55 Discard (Bjorn Stormursson, Eist Tuirseach): RULE item 6, not in my items; rows still show no Discard in this run's flat tables (tables not rebuilt since fix_1).
- gw63, gw64: see item 4.

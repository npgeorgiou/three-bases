# Step 2 families (gwent, 6 Nov 2026)

Counts come from python one-liners over input/gwent + read/gwent (1357 cards with text, keyword entries left out).
Not listed in findings.md, so not judged: the "16 text words without rows" (no list was given; `audit_text.py gwent --list` prints none).

## Families (WRONG ROWS)

### 1. "Create" written without what is created (25 cards)
Cause: "Create ..." is read as `keyword_action Create` with no `on` (24 cards) or as `summon` (Radeyah). The card, type, cost, rarity or keyword the text names is lost.
Finder (field test): text matches `\bCreate\b` and the rows hold no `"act": "create"`. Hits: 25 (24 with `keyword_action Create` and no `on`, 1 summon only).
Script: for each hit, the `Create` effect becomes `{"act":"create","on":{kind,side,with:[...]},"zone":"hand"}` (the shape Cyrus Engelkind Hemmelfart's create already has). The `with` list is read from the words after "Create": bronze/silver/gold = state, "special card" = kind spell, "N-provision" = cost eq/le, faction or type name = region/type, "a Fee/Disloyal" = keyword ref, "from ... starting deck" = state started_in_deck. Radeyah: `summon` of the Neutral stratagem becomes `create`. A hit whose text the parser cannot read goes to a re-read, not a guess.
Examples:
- Eventide Plunder: "Create a 4-provision cost unit with a Fee." (rows: bare Create; word check KW name:fee comes from this)
- Braathens: "Assimilate. Deploy: Create and play a bronze Disloyal unit from your starting deck." (bare Create; word check KW name:disloyal comes from this)
- Filavandrel aén Fidháil: "Deploy (Melee): Create and play a Scoia'tael special card with a provision cost equal to this unit's power. ..." (bare Create twice)
Also: Shady Vendor, Triss: Telekinesis, Radeyah (summon).

### 2. "Discard" written as act `discard`, the other 8 cards use `keyword_action Discard` (2 cards)
Cause: one keyword written two ways.
Finder: text matches `\bDiscard\b` and rows hold `"act": "discard"`. Hits: 2 (8 other cards with the word use `keyword_action Discard`, none uses neither).
Script: `{"act":"discard", ...}` becomes `{"act":"keyword_action","keyword":"Discard", ...}` keeping on/params/link. The `discarded` events stay.
Examples:
- Eist Tuirseach: "Veteran. Deploy (Bloodthirst 3): Draw a card, then Discard a card. Whenever you Discard a non-Neutral unit during your turn, Summon it from your graveyard to this row. ..."
- Bjorn Stormursson: "Veteran. Deploy: Clash with an enemy unit. Order (Bloodthirst 2): Discard a card, then move self back to your hand."
(only 2 exist; no third)

### 3. Time window of the text dropped ("this turn", "this round", "end of this turn") (3 cards)
Cause: the window that limits the effect is not in the rows (Leticia: effect happens at once, not at the end of the turn, and "instead" is missing; Aen Elle: "applied this turn" became "has Frost now"; Luiza: "this round" is missing, `lasts next_card` has no round end).
Finder: text matches `(this turn|this round)` and rows hold none of `"span"`, `next_time`, `this_turn`, `this_round`. Hits: 3.
Script: none by rule (three different shapes). Per card, by hand in a script: Leticia gets a `turn_end` event with `limit next_time` on the increase; Aen Elle's `with` gets the state "applied this turn" (needs a state value, Claude's suggestion: vocab state `applied_this_turn`); Luiza's cost_set gets a round end. Kaptain decides the state value.
Examples:
- Leticia Charbonneau: "Patience. Order (Ranged): At the end of this turn, the Patience value of allied units is increased by [1] instead."
- Aen Elle Aristocrat: "... At the end of your turn, Spawn Frost for 1 turn on each enemy row on which Frost was applied this turn."
- Madame Luiza: "Intimidate. Tribute 3: Gain Zeal. Order: Your next Tribute this round costs 0."

### 4. "adjacent" dropped (1 card)
Cause: "Boost 3 adjacent units" read as "choose 3 units"; adjacency lost.
Finder: text matches `(?i)\badjacent\b` and rows hold no `"sides"`. Hits: 1.
Script: the `n: 3` chosen units get a with-filter for "next to each other". No value for that exists (`sides` means beside self). Claude's suggestion: `{"attr":"position","op":"is","val":"adjacent_group"}`; needs Kaptain's OK before use.
Examples: Armorer's Workshop ("Boost 3 adjacent units by 2 and give them 2 Armor. ..."). Dennis Cranmer ("Boost adjacent units by an amount equal to their Armor") is right (uses `sides`). No third.

### 5. "ignoring Armor" dropped (1 card)
Cause: `ignore_armor` missing from the damage params.
Finder: text matches `(?i)ignor\w+ (its|their|the target unit's|enemy)? ?Armor` and rows hold no `ignore_armor`. Hits: 1 (the 3 others have it).
Script: add `"ignore_armor": 1` to the params of the damage effect of that ability.
Examples: Piercing Missile ("Damage an enemy unit by 4, ignoring its Armor."). Right ones for comparison: Reckless Flurry, Ulula, Professor.

### 6. Amount left `{"x":"unstated"}` where the text says how to count it (5 cards)
Cause: the reading had no value form for the count.
Finder: rows hold `"x": "unstated"`. Hits: 5.
Script: needs a new value form per card (Claude's suggestions, none exist yet): unused provisions (Fucusya), card's distance from the top of the deck (Vivaldi Bank), rows between two units (Dol Blathanna Bowman), provisions below the limit (Torres var Emreis: Founder), damage dealt by Frost in the last 5 enemy turns (Caranthir: Golden Child). Then the script swaps each in. Kaptain decides the forms.
Examples:
- Fucusya: "... Spawn Rain on the opposite row with a duration equal to unused provisions."
- Dol Blathanna Bowman: "Deploy: Damage an enemy unit by 1 for each row that separates it from this unit."
- Vivaldi Bank: "... play another card for a Coin cost equal to its distance from the top, ..."

## RIGHT (rows are right; lines for audit_text_explained.tsv, columns game, card, rule, why, tab separated)

gwent	Insanity	kill or destroy	a keyword entry; the text is the glossary text and has no rows by design
gwent	Sigi Reuven: Mastermind	cost less	Tribute's cost is the spend_mana amount (9 minus 2 times the count); the rows say "2 less for each"
gwent	Glustyworp	for each	the per-unit boost is link for_each with 2
gwent	King Roegner	for each	the per-unit boost is link for_each with 3
gwent	Zoltan: Warrior	for each	the per-unit summon is link for_each
gwent	Seagull	for each	the per-target create is link for_each
gwent	Boris	random	"random cost between 1 and 9" is x range
gwent	Wheel of Fortune	random	"random number between 1 and 10" is x range
gwent	Aglaïs	this turn	"at the end of this turn" is turn_end with limit next_time
gwent	Arena Ghoul	this turn	"at the end of this turn" is turn_end with limit next_time
gwent	Kraken	this turn	"at the end of this turn" is turn_end with limit next_time inside its Deathwish
(Lines for the same cards would go away once RULES 7 to 11 are made; add them now only if the rules wait.)
Word check, patterns/verdicts.tsv (columns game, card, pattern, verdict, by, date):
gwent	757397	V16	record_right	Claude: Tribute cost is spend_mana with the amount 9 minus 2 per Gang; no cost_change needed	6 Nov 2026
Keyword cases with right rows (Armor 4 cards, Frost/Rain/Storm cards, Deathwish 4, Bonded 4, Crew, Echo, Predator, Symbiosis, Reset, Patience, Spring, Infused, Disloyal x2) are RULE items below, not single lines.

## RULE (the check is too narrow or too wide in every game)

1. gw20/22/23/24/30/33/34/35/48/50/58 and the word-check flags: the keyword queries miss a keyword named inside a `with` filter (`attr keyword is/not/in ref/refs`, in `on`, `object`, `actor`, `of`). Evidence: of cards with the word, with-filter only: Storm 6 of 11, Frost 10 of 22, Rain 7 of 17, Deathwish 10 of 43, Armor 12 of 65, Bonded 7 of 28, Disloyal 4 of 19, Infused 2 of 2, Crew 1 of 12, Echo 1 of 14. The 4 missed Bonded cards (One-Eyed Betsy, Free Company, Iron Falcon Troubadour, The Mushy Truffle), Whispering Hillock (Deathwish), Lady of the Lake (Echo), King Henselt (Crew), Dennis Cranmer, Affan Hillergrand (Armor), Imlerith's Wrath, Wild Hunt Bruiser, Bride of the Sea, Messenger of the Sea, Kelpie, Anglerfish (Frost/Rain/Storm), Braathens' sibling Artaud Terranova, Eternal Eclipse all use it. Fix: flat_ref (flat.py, filter part near line 48) takes `keyword` from any with-filter ref/refs, in every game.
2. gw22/23/24: the test regex `\b(?-i:Frost)\b` also matches card names (Biting Frost, Impenetrable Fog, Torrential Rain). Avallac'h, Tempest, Scepter of Storms only name those cards (rows right, `create`/`play_card` with the card name). Fix: the case needs to ignore a word that is part of a card name.
3. gw34 Armor: `ignore_armor` in params and `stat attr armor` / `swap_stats attr armor` are Armor uses. Reckless Flurry, Ulula, Professor (ignore_armor), Vlodimir von Everec, Living Armor (attr armor). Fix: the keyword query counts `ignore_armor` and `attr armor`.
4. gw63 Predator / gw64 Symbiosis: rows do keep the condition (`keyword_condition ref Predator`: Adda: Striga, Cockatrice, Werewolf, Kikimore Stalker; `ref Symbiosis`: Aucwenn), but flat_ref has no row for it, while Bonded and Crew, written the same way, pass. Cause not found in the 3 files read (flat.py `keyword_conds`, line 174: needs the keyword entry to have rows?). Fix: `keyword_conds` also writes the reference when the keyword has no ability rows. The gw63 note in mech_cases.md ("records keep no trace") is wrong and should be removed.
5. gw84 Reset: "Reset your leader ability", "Reset an allied unit's Order ability" are `act refresh` (Damien de la Tour, Viraxas: Prince). Query gw84 should include act refresh on an ability.
6. gw55 Discard: after family 2 is fixed Eist Tuirseach and Bjorn Stormursson pass; no rule change.
7. Text audit "for each": accept `link for_each` (Glustyworp, King Roegner, Zoltan: Warrior, Seagull).
8. Text audit "random": accept `x range` (Boris, Wheel of Fortune).
9. Text audit "this turn": accept `turn_end` with `limit next_time` for "at the end of this turn" (Aglaïs, Arena Ghoul; Kraken). Leticia and Aen Elle stay flagged (family 3).
10. Text audit "cost less" and word check V16: a Tribute/Fee cost is `spend_mana` with the amount; accept it (Sigi Reuven: Mastermind).
11. Text audit: skip cards of category keyword (Insanity).
12. gw54 Spring: the case regex should skip the card name "Spring Equinox" (Spring is no keyword there).
13. gw32 Patience: `stat attr keyword_amount` of a named card is the Patience value; the keyword query should accept it (Alumni).
14. gw33 Deathwish: the `dies self` event (or `give_ability` Infused with a `dies` ability) is the keyword; add the layer row like Deploy has (played self). Plague Maiden, Endless Voyage, Deranged Corsair, Sove.
15. Text audit "adjacent" and "create": none (families 1, 4).
16. Link audit "nothing makes summon/create (mine/any/enemy)" for Cyrus Engelkind Hemmelfart, Eternal Fire Inquisitor, Procession of Penance, Adda: Striga, Lonely Champion: they need "Firesworn Token" / "a Token"; the makers (Congregate, Eternal Fire Disciple: `summon card Firesworn Zealot`, types Human, Token, Firesworn) name the card, with the token type only in the card's own data. Fix: audit_links accepts a maker that names a card whose types match the need's type and state token.
17. Link audit "nothing makes trap_activated": Traps (Serpent Trap, Crushing Trap, 13 cards with Trap/Ambush) have the Ambush/Spring rows (`played` with state hidden / `activated`); Elven Scout waits for `trap_activated`. Fix: those rows make trap_activated.
18. Link audit "nothing makes exhausted" (Blood Money): the last Charge used is the exhaustion (Charges cards). "nothing makes counts_down" (King Henselt): Cooldown/Timer keyword cards make it. "nothing makes removed_from_deck (enemy)" (Sandor de Baccalà): drawing from a deck makes it (game rule). "nothing makes keyword_used Rain/Storm" (Sea Serpent): any card giving Rain/Storm makes it at the turn's end (game rule). Fix: in audit_links, those events count as made by the keyword / game rule.
19. Link audit 9 (Aucwenn gives keywords to Wandering Treant, nothing makes it): the rows only react to "Whenever you Spawn a Wandering Treant" (an `summoned` watcher with `card is Wandering Treant`); they give Vitality, not the card. Check 9 should not read a `card is` in the `object` of the event as the card being given something. (RULE; Aucwenn's rows are right.)
20. Link audit 10 (old library tags, 284 cooldowns, 123 summon, 122 graveyard, 112 coin_economy, 110 generate_cards, 107 ping, 97 tutor, 95 stat_condition, 73 condition_count, 67 on_ally_play): leads, not judged one by one (examples Geralt: Igni, Zoltan: Scoundrel, Iris von Everec, Lined Pockets, Operator, Chironex, Triss Merigold, Redanian Knight, Roach). Not read; to go to State unless Kaptain wants them read.

Word-check flags: Eventide Plunder (KW name:fee) and Braathens (KW name:disloyal) = family 1. Sigi Reuven: Mastermind (V16) = RULE 10.

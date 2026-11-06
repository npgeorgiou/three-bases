# Gwent keyword definitions: suggestion vs source (input/gwent/keywords.jsonl)

Totals: 3 backed, 8 same, 5 not backed.

| Keyword | Source text (short) | Current vocab meaning | Verdict | Concept fits? |
|---|---|---|---|---|
| Ambush | Played face down, then flips over when the ability's condition is met. | No Gwent meaning yet (generic text only) | NOT BACKED: source has no manual reveal and no different effect; only "flips when condition is met" (manual flipping is Spring's text, for Traps) | Yes, stealth |
| Berserk | Trigger whenever power is equal to or lower than the specified amount. | Triggers whenever its power is N or lower | NOT BACKED: source says power N or lower, not "base power reaches a threshold" (current is right) | Yes, condition_life |
| Bounty | Status: when a unit with it is destroyed or banished, opponent gains coins equal to its base power; only one Bounty unit per side. | Status: when destroyed or banished its opponent gains Coins equal to its base power | SAME (neither has the one-per-side limit) | Yes, coin_economy |
| Charge | The number of times an Order ability can be used; only cards with Charge: X can gain Charges. | Faeria only: moves up to N spaces in a straight line | SOURCE BACKS IT for Gwent (current meaning is another game's) | No: movement does not fit Gwent Charge; same name in two games |
| Clash | Units simultaneously damage each other by their power. | Two units damage each other by their power at once | SAME | Yes, damage |
| Crew | Trigger this ability if this unit is between two Soldiers. | Triggers if between two Soldiers | NOT BACKED: source says between two Soldiers, not "adjacent Gang-category unit" (current is right) | Yes, adjacency |
| Deathwish | Trigger when destroyed and moved from battlefield to graveyard; banished units are not sent to graveyard. | Triggers when destroyed and moved to the graveyard | SAME (suggestion drops the graveyard and banished point; current keeps it) | Yes, death_trigger |
| Echo | At the beginning of the round, move this card from the graveyard to the top of its owner's deck; give it Doomed. | At the start of a round the card goes from graveyard to top of deck, Doomed | NOT BACKED: source says start of round, from the graveyard, Doomed; not "end of round after being played" (current is right) | Yes, recycle |
| Exposed | Trigger whenever the unit loses its Armor. | Triggers when the unit loses its Armor | SAME | Roughly, on_damaged (it is armor loss, not damage) |
| Flanking | If adjacent to only one card: on your Melee row end-of-turn ability triggers twice; on your Ranged row gain 1 Armor at end of turn. | Adjacent to only one card: melee row end-of-turn ability twice, ranged row gains 1 Armor | SAME (suggestion is vaguer; current is closer) | Yes, adjacency |
| Insanity | If you have insufficient Coins, damage this unit by its Fee, ignoring Armor, to trigger its Fee ability; not usable if it would destroy the unit. | With too few Coins, damage this unit by its Fee to trigger the Fee | SAME (suggestion says "pay Health"; source says damage, ignoring Armor, never lethal) | Yes, life_payment |
| Initiative | Trigger if you haven't used an Order, Fee or Spring ability this turn. | Same wording | SAME | Yes, play_timing_condition |
| Poison | Status: if a unit receives two instances of Poison, destroy it. | Stormbound only: takes 1 damage every turn | SOURCE BACKS IT for Gwent (current meaning is another game's) | No: damage_over_time does not fit Gwent Poison; same name in two games |
| Resilience | Status that lets a unit stay on the battlefield at the end of the round, then disappears; Boost and Armor are not carried over. | Status: the unit stays on the battlefield at the end of the round | SOURCE BACKS IT (adds "then the status is removed") | Yes, round_carryover |
| Spring | Manual activation of a face-down Trap; automatic on a Trap played next to an Artifact; flipped over after use. | Manual activation of a face-down Trap | NOT BACKED: source says Trap, not Ambush (current is right) | Yes, trap_secret |
| Symbiosis | Whenever you play a Nature card, Spawn a Wandering Treant on a random allied row and set its power to the number of Symbioses you control. | Whenever you play a Nature card, spawn a Wandering Treant | SAME (suggestion and current both omit the power rule) | Yes, summon |

Note: Charge and Poison already carry meanings from Faeria and Stormbound; the Gwent meaning would need its own row or concept.

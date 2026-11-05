# Marvel Snap: verdict on 49 differing cards

## Families
1. FIRST reading has no abilities where the text has a rule or effect. 12 cards: 796169, 796176, 796227, 796261, 796378, 8000081, 8000217, 8000289, 8000346, 8000481, 8000574, 8000583. SECOND right. FIX (first reading wrong). Note: for 796169 and 796176 the run_rule form is the only way to mark an inexpressible location rule.
2. Location's own effect on reveal written as summoned (FIRST) vs played (SECOND). 3 cards: 796194, 796219, 796353. Brief says reveal = played. Same meaning, different form: NORMALIZE (summoned -> played).
3. "Add to hand" with or without "on" player target. 3 cards: 796272, 8000238, 8000688. Same meaning: NORMALIZE (ignore the target form).
4. Hand card kind written as unit vs card+category unit (or card vs unit for the discard). 2 cards: 8000314, 8000189. Same meaning: NORMALIZE.
5. Other equal forms (duration written two ways, self vs deck card, minus vs product -1, extra trigger vs lasts, set_terrain vs transform, link if_done vs then). 6 cards: 8000057, 8000129, 8000219, 8000649, 8000693, 8000507. Same meaning: NORMALIZE.
6. Text says "a / one / first" card: FIRST picks one (chosen / top), SECOND hits all or leaves pick empty. 6 cards: 796324, 8000064, 8000177, 8000444, 8000526, 8000748. FIRST right, SECOND wrong. No fix in FIRST.
7. "Add to a location" written as summon (FIRST) vs create on board (SECOND). 4 cards: 796180, 8000036, 8000406, 8000528. Brief: put on a location = summon. FIRST right. (8000036 SECOND also drops the winning check.) No fix in FIRST.
8. "First to ..." conditions and the played trigger: FIRST checks the other side has not done it; SECOND does not and uses summoned. 2 cards: 796327, 796337. FIRST right.
9. FIRST reading wrong in what it does, SECOND closer to the text. 6 cards: ids: 796224, 8000063, 8000347, 8000613, 8000626, 8000358. Doubling a change (796224), spread steal (8000063), same card for cost (8000347), use On Reveal = repeat (8000613), copy of self (8000626), 1-Cost cards any zone (8000358). SECOND right. FIX.
10. SECOND reading wrong, FIRST right. 4 cards: 796242, 8000053, 8000737, 8000744. (8000053 power of the discarded card; 8000737 jump = move; 8000744 Horde cards not only on board; 796242 no cards revealed = cant played, SECOND is an empty rule.) No fix in FIRST.
11. BOTH wrong: steal text should be copy_text (brief), not repeat + silence. 1 card: 8000619.

## Cards
796169 | SECOND | rule text, FIRST empty
796176 | SECOND | rule text, FIRST empty
796180 | FIRST | add to location is summon
796194 | BOTH ok | summoned vs played, same meaning
796219 | BOTH ok | summoned vs played, same meaning
796224 | SECOND | doubles each change, FIRST increase_effect is vague
796227 | SECOND | FIRST empty (event could be snapped)
796242 | FIRST | cant played = not revealed; SECOND empty rule
796261 | SECOND | cant retreat after turn 5, FIRST empty
796272 | BOTH ok | target form only
796324 | FIRST | "a character" = one chosen
796327 | FIRST | first-to check present
796337 | FIRST | first-to check, target is the new card
796353 | BOTH ok | summoned vs played
796378 | SECOND | FIRST empty
8000036 | FIRST | summon to chosen place; SECOND drops winning
8000053 | FIRST | uses power of the discarded card
8000057 | BOTH ok | until end of next turn, two forms
8000063 | SECOND | random spread steal
8000064 | FIRST | "one of" = chosen
8000081 | SECOND | FIRST empty
8000129 | BOTH ok | same effect
8000177 | FIRST | "an enemy card" = one
8000189 | BOTH ok | kind card vs unit, same meaning
8000217 | SECOND | FIRST empty
8000219 | BOTH ok | same effect
8000238 | BOTH ok | target form only
8000289 | SECOND | FIRST empty
8000314 | BOTH ok | kind form only
8000346 | SECOND | FIRST empty
8000347 | SECOND | cost change on the same card
8000358 | SECOND | no zone invented, FIRST limits to board
8000406 | FIRST | summon to chosen place
8000444 | FIRST | "an enemy card" = one chosen
8000481 | SECOND | FIRST empty
8000507 | BOTH ok | replace the location, two acts
8000526 | FIRST | "an enemy card" = one chosen
8000528 | FIRST | summon to each location
8000574 | SECOND | FIRST empty
8000583 | SECOND | FIRST empty
8000613 | SECOND | use On Reveal = repeat, not play
8000619 | BOTH wrong | steal text should be copy_text
8000626 | SECOND | copy of this card
8000649 | BOTH ok | invert, two forms
8000688 | BOTH ok | zero energy test, two forms
8000693 | BOTH ok | +1 Energy next turn, two forms
8000737 | FIRST | jump = move, not summon
8000744 | FIRST | Horde cards are not only on board
8000748 | FIRST | "first card" = top, not all

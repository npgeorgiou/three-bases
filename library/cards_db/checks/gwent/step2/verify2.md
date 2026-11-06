# Verify 2 (gwent, after fix_7)

Limit: lines_diff2.txt shows only 3 examples per group, so some pairs below are judged by their group, not by name. No tool run.

## 1. The 9 wanted changes
- Runemage -> Artorius Vigo, Imperial Diplomacy, Double Cross: back (NEW group "makes the Create it gives stronger", 4 lines, 3 named). Yes.
- Double Cross -> Fercart, Double Cross -> Ivo of Belhaven: back ("is played"). Yes.
- Nithral, Imlerith's Wrath, Wild Hunt Bruiser -> Caranthir: Golden Child: gone (GONE group "damages units or players"). Yes.
- Imperial Diplomacy -> Ivar Evil-Eye: not named in the examples; the 16-line GONE group "fills your hand" is the rule fix 7.4 changed, so most likely in it. Yes (by group; confirm by name after the next links run).

## 2. Other changes
Gone, right to go:
- 16 "fills your hand" (Toussaintois Hospitality -> Ivar, Siege -> Temple of Melitele: Congregation, Uprising -> Geralt: Quen, and so on). The cards say "Spawn and play ..." (Buhurt, Bombardment, Lyrian Scytheman): the card is played at once and never waits in the hand. Cause of the removal: fix_7.4 (create + play_card on it does not fill the hand). Correct.
- 2 "fills your hand; also is played" and 2 "creates; ... fills your hand" (Kaer Seren, Uprising -> Keldar / Griffin Witcher / Mentor): same reason, correct. The pairs stay under other reasons (see new).

Gone but pair kept under reworded reason (no loss):
- Cintrian Knight, Redanian Knight -> Knight-Errant ("changes your units' stats; also damages ..." -> "changes units' stats; also damages ..."); Kaer Seren -> Griffin Witcher / Mentor ("puts it into play from the hand" stays).
- runeterra 14 + 2 lines -> Xolaani the Bloodweaver: only the wording changed ("changes your units' stats" -> "changes its stats for its effect"). Pairs stay. Runeterra was not meant to change in fix_7; cause is most likely the shared network.py/flat.py edit. Wording is looser, not a loss.

LOSS (gone, wrong to go): 11 lines to Caranthir: Golden Child that are Frost spawners: Aen Elle Aristocrat, Ard Gaeth, Red Riders: Charge, White Frost and the rest of the group "damages units or players; also makes units get Frost" (10 lines + 1 line "...gives it more strength when it comes; also makes units get Frost"). Caranthir's text: "boost self by the damage dealt by Frost", so a card that Spawns Frost is a real feeder. The old reason had a wrong part (damages units or players) and a right part (makes units get Frost); the whole line went.
Cause: fix_7.3 (v85.py): Caranthir's count now needs an actor `{kind effect, keyword is Frost}`. fix_7.3 claims the Frost spawners "stay through the Frost keyword rows", but they did not: the spawn rows on those cards do not match the actor filter. Eredin Bréacc Glas -> Caranthir (case n568; Eredin: "Increase the damage dealt by Frost by 1") is lost the same way.

New, real:
- Runemage -> 3 Create givers (wanted), Double Cross -> Fercart, Double Cross -> Ivo of Belhaven (wanted).
- White Frost -> Caranthir "gives it more strength when it comes": real (White Frost boosts a Wild Hunt unit played, Caranthir is one).
- Redanian Knight, Cintrian Knight -> Knight-Errant, Kaer Seren -> Griffin Witcher / Mentor, runeterra 16: reworded copies of old lines.

New, not real:
- Kaer Seren -> Keldar and Uprising -> Keldar ("is played"). Keldar triggers on "play a special card"; Kaer Seren and Uprising spawn and play units (Griffin Witcher, Lyrian Scytheman). Cause: fix_7.2 (flat.py: `it` after create is on my side), so the play row now matches every "is played" waiter regardless of kind; Double Cross is right only because it plays a spell. The pair itself did exist before (hand filling, also wrong for the same card: Keldar does not care about hand), so it is no new damage, but the reason is false.

## 3. Cases
Now 152 of 174 pass (22 NO); previous run (rebuild.txt) 153 of 174 (21). The previous list of failing names was not saved, so the new failure is found by reasoning: n568 (White Frost deck: Eredin Bréacc Glas -> Caranthir: Golden Child) now fails because the Frost spawner / Frost-boost lines to Caranthir are gone (fix_7.3, above). The other 21 are the old Mobilization, Nature's Gift, Shieldwall, Enslave, Tactical Decision and Patricidal Fury cases. Not confirmed by name: save the NO list in rebuild.txt next time.

Verdict: LOSS (Frost spawners and Eredin -> Caranthir, cause fix_7.3).

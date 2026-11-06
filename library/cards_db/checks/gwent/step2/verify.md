# Verify: gwent lines diff (9 gone, 14 new) and link audit

Verdict: LOSS (5 lines wrongly gone) and 4 new lines not real. Link audit: all lines explained, none open.

## Gone, by reason

Right to be gone (6):
- "creates cards: X copies/damages them": Double Cross -> Slave Driver (Slave Driver damages a bronze allied unit on the board, nothing to do with a created card), Triss: Telekinesis -> Operator (Triss creates a special card; Operator copies a bronze unit from hand), Eventide Plunder -> Flyndr's Crew (Flyndr's Crew copies itself, not a created card).
- "gives it more strength when it comes": White Frost -> Caranthir: Golden Child. Wrong reason; Caranthir counts Frost damage. The pair is back as a new line (Frost).
- "is played": Imperial Diplomacy -> Emhyr var Emreis. Emhyr reacts to the opponent playing a unit; Imperial Diplomacy is played by you.
- Shady Vendor -> Jacques: Grand Master, "also triggers: is played" part: Jacques reacts to Firesworn cards, Shady Vendor's Crime is not said to be Firesworn. The resource part of the line stays (new line).

Loss (5): the line was right by the texts.
- "makes the Create it gives stronger": Runemage -> Artorius Vigo, Imperial Diplomacy, Double Cross. Runemage: "your Create effects show 5 options instead of 3"; each of the three cards has a Create. Runemage's row is still `increase_effect options=5` on the Create keyword, but no line is left from Runemage to any Create card (after: only "is played" lines). The Create fix removed the link; every Create card should have it (Triss: Telekinesis, Eventide Plunder, Shady Vendor too).
- "is played": Double Cross -> Fercart. Double Cross plays a card; Fercart: "whenever you play a special card". Same kind as the other 207 lines into Fercart.
- "is played": Double Cross -> Ivo of Belhaven. Ivo counts every card you played this round; Double Cross plays one. 235 other cards still link to Ivo this way.

## New, by reason

Real (11):
- "damages units or players; also makes units get Frost": Red Riders: Charge / Precision / Spread (10 lines, Spawn Frost) -> Caranthir: Golden Child, and White Frost -> Caranthir (Frost spawn; Caranthir boosts by the damage Frost dealt). Real by the Frost part.
- "lets you gain the second resource (Bones)": Shady Vendor -> Jacques (Profit gives the resource Jacques' Tribute/Fee spend). Real.

Not real (4):
- "damages units or players": Nithral (damage a unit by 1), Imlerith's Wrath (damage by power), Wild Hunt Bruiser (damage by 2) -> Caranthir. Caranthir counts damage dealt by Frost; these cards' damage is not Frost damage. The line takes any damage as Frost damage.
- "fills your hand": Imperial Diplomacy -> Ivar Evil-Eye. Ivar's Adrenaline 2 triggers with 2 or fewer cards in hand; Imperial Diplomacy creates a card and plays it at once, so the hand does not fill; filling the hand would work against Adrenaline.

## Link audit (python3 audit_links.py gwent: 12 findings)
- Sandor, Aucwenn, check 10 cooldowns/summon/graveyard/coin_economy/generate_cards/ping/tutor/condition_count/on_ally_play: already explained in PROGRESS.md.
- check 10 stat_condition (95 cards): was not explained. Checked Cyprian Wiley, Vigo's Muzzle, Alzur's Double-Cross, Yennefer: Conjurer, Geralt: Igni: the condition is a target filter (`strength le N`) or a `highest` pick. Explained in PROGRESS.md. None OPEN.

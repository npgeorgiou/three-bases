# Fix 8 (gwent, verify2.md: Frost spawners lost, 2 Keldar lines not real)

Not run: load.py, links.py (not allowed). Records not changed (v85.py stays: Caranthir's row is right). Only network.py changed (parses). Lines change after the next links run.

## 1. Frost spawners -> Caranthir: Golden Child
Cause: Caranthir's rows (fix_7.3): condition `damaged`, actor kind effect, actor_with `keyword is <Frost>`. The Frost spawners (Aen Elle Aristocrat, Ard Gaeth, Red Riders: Charge, White Frost, Eredin Bréacc Glas) make `damaged` through Frost's own rows (origin uses_keyword, no actor) and give Frost (flat_do `give_keyword` keyword_ref Frost, on enemy rows). network.py `doer_fits` read the actor filter `keyword is Frost` as "the card that does it must have Frost printed", so no spawner fitted.
Fix: network.py `doer_fits`: an actor of kind effect with `keyword is/in <id>` is done by a card that prints that keyword or has a flat_do `give_keyword` of it (any side). Works for every card that counts damage by a keyword effect, not only Caranthir (Rain/Storm count 757298 too).
Rows that now meet: Caranthir flat_ref condition `damaged` (actor effect, keyword is Frost) on one side; on the other the spawners' flat_ref makes `damaged` (Frost's rows) plus flat_do `give_keyword` Frost. Eredin -> Caranthir (n568) is also a giver (give_keyword Frost + increase_effect on Frost).
Rows that still do not match (right): Nithral, Imlerith's Wrath, Wild Hunt Bruiser: their flat_do is `damage` only, no `give_keyword` Frost, so doer_fits is false.
Line reason should return to "damages units or players; also makes units get Frost" for the spawners (the wrong first half comes from the Frost keyword's own damage rows, same as before fix_7).

## 2. Kaer Seren -> Keldar, Uprising -> Keldar ("is played")
Cause: fix_7.2 made `it` after a create mine, so Kaer Seren (makes `played`, kind card, side mine, obj_with `card in 757204;...`) and Uprising (obj_with `card is 756733`) became "plays a card"; kind card fits Keldar's "play a spell" (flat_ref trigger `played`, kind spell, side mine), though the named cards (Griffin Witcher, Lyrian Scytheman ...) are all units.
Fix: network.py main match loop: for h=played, when the maker names its card (`card is`/`card in`) and every named card is in the game and none has a category of the need's kind, no line. The rule is for every card (a card that plays a named unit feeds no "play a spell" or "play a landmark" wait).
Rows now not matching: Kaer Seren / Uprising flat_ref makes `played` (obj_with names units) vs Keldar trigger `played` kind spell.
Kept (5 lines of fix_7): Runemage -> Artorius Vigo, Imperial Diplomacy, Double Cross (givers_of, untouched); Double Cross -> Fercart (spell), Double Cross -> Ivo of Belhaven: Double Cross / Imperial Diplomacy makes `played` kind card pick it with no obj_with, so the new rule does not apply; they still match Fercart (spell) and Ivo (kind card).

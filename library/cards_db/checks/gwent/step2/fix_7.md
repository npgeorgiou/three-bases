# Fix 7 (gwent, verify.md: 5 lines wrongly gone, 4 new not real)

Not run: load.py, links.py (not allowed). Lines change after the next load + links run.

1. Runemage -> Artorius Vigo, Imperial Diplomacy, Double Cross ("makes the Create it gives stronger").
   Cause: v78/v79 turned the Create rows from `keyword_action Create` into `act create`; network.py `givers_of` only knew `give_keyword` / `keyword_action`, so no card "gave" Create any more.
   Fix: network.py `givers_of`: an `act create` row (any on_side, the source side of "from your opponent's hand" is not who gets the card) counts as the keyword Create at work, when the game has a keyword card named Create.
   Comes back: Runemage flat_do `increase_effect` with on_with `keyword is <Create id>` on one side; on the other side Artorius Vigo, Imperial Diplomacy, Double Cross (and Triss: Telekinesis, Eventide Plunder, Shady Vendor) flat_do `act create`.
2. Double Cross -> Fercart and Ivo of Belhaven ("is played").
   Cause: Double Cross `create ... side enemy zone hand` (source: opponent's hand) is followed by `play_card on it`; flat.py gave `it` the side of the create (enemy), so the play row was "enemy plays", and the plays-a-card lines need side mine.
   Fix: flat.py: after a `create` into hand (no `to`) with side enemy, `it` is on my side. Same for 756725, 756503 ("create and play from the opponent's deck").
   Comes back: Double Cross flat_do `play_card` on_side mine (was enemy); Fercart flat_ref trigger `played` kind spell side mine, Ivo flat_if `amount_event_count` event played kind card side mine.
3. Nithral, Imlerith's Wrath, Wild Hunt Bruiser -> Caranthir: Golden Child ("damages units or players").
   Cause: v82 wrote Caranthir's count as `event damaged` with the Frost filter on the unit hit (object), so any damage matched. The text says damage dealt BY Frost.
   Fix: fixes/gwent/v85.py (and v82.py for a rerun): the filter moves to the actor: `actor {kind effect, with keyword is Frost}`, `object {kind unit}`. Same shape Rain/Storm use. check.py on read/gwent/batch_007.jsonl: 0 problems.
   Goes: Caranthir flat_if `amount_event_total` now has ev_actor_with `keyword is Frost`, ev_obj_with empty; Nithral/Imlerith/Bruiser flat_do `damage` give no Frost actor. Red Riders / White Frost (Frost spawn) stay through the Frost keyword rows.
4. Imperial Diplomacy -> Ivar Evil-Eye ("fills your hand").
   Cause: the create now has zone hand (v78), so the hand-filling rule counted it; but "Create and play" plays the card at once (`play_card on it`).
   Fix: network.py hand rule: a card whose create ability also plays `it` does not fill the hand.
   Goes: Imperial Diplomacy flat_do `create` + `play_card pick it` in the same ability; Ivar flat_if `of_zone hand` is the other side.

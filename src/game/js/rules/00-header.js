/* =====================================================================
   RULES ENGINE
   Pure game logic: no DOM access. A game state is a plain JSON object,
   so it can be deep-cloned for previews and for the computer's search.
   Some actions open a follow-up choice for the same player (s.pending):
   a "when placed" pick, Reform Ranks' free moves, a defector's new spot.
   The turn passes only once that choice is made.
   ===================================================================== */

const ROWS = 3, COLS = 3, LANES = [0, 1, 2];
const MAX_CARRY = 5, START_CARRY = 4, START_HAND = 5, DRAW_PER_ROUND = 2, HAND_LIMIT = 10, MAX_REDRAW = 3;

// A unit's supply is also its cost.
for (const card of Object.values(CARDS)) if (!card.tactic) card.cost = card.sup;


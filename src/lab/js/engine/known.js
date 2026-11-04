/* ---------- what a player can know: the cards the opponent has not shown, and a guessed position ---------- */
/** Cards of `side`'s faction not yet seen by the other side, as { cardKey: copies }. */
function unseenCards(s, side) {
  const left = {};
  for (const [k, n] of DECKS[s.players[side].deck].list) left[k] = (left[k] || 0) + n;
  const seen = [...s.players[side].discard, ...s.units.filter(u => u.owner === side).map(u => u.card)];
  for (const k of seen) if (left[k]) left[k]--;
  for (const k in left) if (!left[k]) delete left[k];
  return left;
}

/** The game as `me` may know it: the opponent holds a random possible hand; decks in unknown order. */
function sampledView(s, me) {
  const opp = other(me), v = cloneState(s), unseen = [];
  for (const [k, n] of Object.entries(unseenCards(s, opp))) for (let i = 0; i < n; i++) unseen.push(k);
  shuffle(unseen);
  const size = s.players[opp].hand.length;
  v.players[opp].hand = unseen.slice(0, size);
  v.players[opp].draw = unseen.slice(size);
  v.players[me].draw = shuffle(v.players[me].draw.slice());
  v.noFx = true;
  return v;
}


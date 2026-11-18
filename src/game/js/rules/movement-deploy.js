/* ---------- movement and deployment ---------- */
/** Where a unit can move in its camp (keyed "r,c"), in orientation o; a move costs its supply, once per round. */
function moveTargets(s, u, o = u.o) {
  const out = {};
  if (kw(u, 'fixed') || u.moved || !canPay(s, u.lane, moveCost(u))) return out;
  const offs = offsetsOf(u, o);
  for (let r = 0; r < ROWS; r++)
    for (let c = 0; c < COLS; c++) {
      if (r === u.r && c === u.c && o === u.o) continue;   // where it stands now
      if (fitsCells(s, u.owner, u.lane, offs, r, c, u.id)) out[r + ',' + c] = { r, c, lane: u.lane, d: moveCost(u), path: [[u.r, u.c], [r, c]] };
    }
  return out;
}

function canDeploy(s, p, handIndex, lane, r, c, o) {
  const k = s.players[p].hand[handIndex];
  if (!k) return false;
  return fits(s, p, lane, CARDS[k].size, r, c, o) && canPay(s, lane, CARDS[k].cost);
}

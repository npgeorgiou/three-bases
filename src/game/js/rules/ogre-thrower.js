/* ---------- Ogre Thrower ---------- */
/** Allies unit u could throw now (adjacent, 1 cell, not Immobile), if it still has an attack it can pay for. */
function throwables(s, u) {
  if (!u || !cardOf(u).thrower || ctl(u) !== s.cur || s.pending || u.attacked || !canPay(s, u.lane, attackCost(u))) return [];
  if (cardOf(u).cannon) return adjacentAllies(s, u).filter(a => cellsOf(a).length === 1 && cardOf(a).proj);
  return adjacentAllies(s, u).filter(a => cellsOf(a).length === 1 && !kw(a, 'fixed'));
}
/** Cells of u's lane, in either camp, where ally a can be thrown: free cells, or units that can be struck (not u or a). */
function throwTargets(s, u, a) {
  const out = [], cannon = cardOf(u).cannon;
  for (const lane of LANES) for (const camp of [0, 1]) {
    if (cannon && (camp === ctl(u) || (lane !== u.lane && !cardOf(u).far))) continue;
    const map = occupancy(s, camp, lane);
    for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
      const t = map[r + ',' + c];
      if (t && (t.id === u.id || t.id === a.id || isIncorp(t))) continue;
      if (cannon && (!t || ctl(t) === ctl(u))) continue;
      out.push({ lane, owner: camp, r, c });
    }
  }
  return out;
}


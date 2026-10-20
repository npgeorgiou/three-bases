/* ---------- rounds ---------- */
function startRound(s, first) {
  for (const p of [0, 1]) for (const lane of LANES) {
    s.pool[p][lane] = s.poolStart[p][lane] = laneSupply(s, p, lane);
  }
  s.cur = s.starter; s.passed = null; s.acts = 0; s.actor = null; s.pending = null;
  s.ownerStart = s.owner.slice();
  for (const u of s.units) { u.moved = false; u.attacked = false; u.atk = 0; u.mv = 0; u.armUsed = false; }
  log(s, `Round ${s.round} begins. ${deckName(s, s.starter)} acts first.`);
  emit(s, { round: s.round, starter: s.starter });
  if (first) return;
  for (const p of [s.starter, other(s.starter)]) {
    const n = drawCards(s, p, DRAW_PER_ROUND);
    if (n) emit(s, { draw: p, n });
  }
}


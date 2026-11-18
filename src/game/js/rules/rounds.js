/* ---------- rounds ---------- */
function startRound(s, first) {
  for (const p of [0, 1]) for (const lane of LANES) {
    s.pool[p][lane] = s.poolStart[p][lane] = laneSupply(s, p, lane);
  }
  s.cur = s.starter; s.passed = null; s.acts = 0; s.actor = null;
  s.ownerStart = s.owner.slice();
  for (const u of s.units) { u.moved = false; u.attacked = false; }
  log(s, `Round ${s.round} begins. ${deckName(s, s.starter)} acts first.`);
  emit(s, { round: s.round, starter: s.starter });
  if (first) return;
  for (const p of [s.starter, other(s.starter)]) {
    const n = drawCards(s, p, DRAW_PER_ROUND);
    if (n) emit(s, { draw: p, n });
  }
}

/** Leftover supply fills carry-over lane by lane, from the owner's left, up to the cap. */
function carryOver(s, p) {
  const P = s.players[p], before = P.reserve, moved = [];
  let room = MAX_CARRY - P.reserve;
  for (const lane of carryOrder(p)) {
    const n = Math.min(room, s.pool[p][lane]);
    if (n > 0) { moved.push([lane, n]); room -= n; }
  }
  if (s.pool[p].some(x => x > 0)) emit(s, { carry: moved, p, before });
  for (const [, n] of moved) P.reserve += n;
  if (P.reserve > before) log(s, `${deckName(s, p)} carries over ${P.reserve - before} supply.`);
  s.pool[p] = [0, 0, 0];
}

/** Resolve the end of the round (bases, carry-over, winner). Returns true if the game is won. */
function resolveRoundEnd(s) {
  s.actor = null;
  log(s, `Both sides pass. Round ${s.round} ends.`);
  updateBases(s);
  for (const p of [0, 1]) carryOver(s, p);

  for (const p of [0, 1]) if (basesKept(s, p) >= 2) {
    s.winner = p;
    s.endReason = `${deckName(s, p)} held two bases through the whole round.`;
    log(s, `${deckName(s, p)} held two bases from the start to the end of the round and wins.`);
    return true;
  }
  const starved = s.test ? [] : [0, 1].filter(p => s.players[p].reserve === 0 && LANES.every(l => laneSupply(s, p, l) === 0));
  if (starved.length === 1) {
    s.winner = other(starved[0]);
    s.endReason = `${deckName(s, starved[0])} has no supply left and no way to gain any.`;
    log(s, `${deckName(s, starved[0])} has no supply left and no way to gain any. ${deckName(s, s.winner)} wins.`);
    return true;
  }
  if (starved.length === 2) {
    s.winner = 'lost';
    s.endReason = 'Neither side has supply left or a way to gain any. Both sides lose.';
    log(s, s.endReason);
    return true;
  }
  s.quietRounds = s.acts === 0 ? (s.quietRounds || 0) + 1 : 0;
  if (s.quietRounds >= 3) {
    s.winner = 'lost';
    s.endReason = 'Three rounds in a row without any action. Both sides lose.';
    log(s, s.endReason);
    return true;
  }
  return false;
}

/** The state at the end of this round if both sides passed now (for the forecast). */
function forecastRoundEnd(s) {
  const t = cloneState(s);
  t.noFx = true;
  resolveRoundEnd(t);
  return t;
}

function endRound(s) {
  if (resolveRoundEnd(s)) return s;
  s.round++; s.turn++; s.starter = other(s.starter);
  startRound(s, false);
  return s;
}


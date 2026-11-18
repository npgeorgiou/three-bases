/* ---------- actions ---------- */
/** Each action handler runs for the acting player p; the turn then passes to the other side. */
const ACTIONS = {
  deploy(s, p, a) {
    const k = s.players[p].hand.splice(a.hi, 1)[0], card = CARDS[k];
    pay(s, a.lane, card.cost);
    const u = { id: s.nid++, card: k, owner: p, lane: a.lane, r: a.r, c: a.c, o: a.o, dmg: 0, born: s.round };
    s.units.push(u);
    log(s, `${deckName(s, p)} places ${unitName(u)} in lane ${a.lane + 1}.`);
    emit(s, { place: u.id });
  },
  move(s, p, a) {
    const u = byId(s, a.id), o = a.o ?? u.o;
    const target = moveTargets(s, u, o)[a.r + ',' + a.c];
    pay(s, u.lane, target.d);
    emit(s, { move: u.id, path: target.path, o, steps: Math.max(1, Math.abs(a.r - u.r) + Math.abs(a.c - u.c)) });
    Object.assign(u, { r: a.r, c: a.c, o, moved: true });
    log(s, unitName(u) + ' moves.');
  },
  attack(s, p, a) {
    const u = byId(s, a.id), t = byId(s, a.tid);
    pay(s, u.lane, attackCost(u));
    u.attacked = true;
    log(s, `${unitName(u)} attacks ${unitName(t)}.`);
    strike(s, u, t, unitName(u));
  },
};

function applyAction(s, a) {
  const p = s.cur;
  s.fx = []; s.deadUnits = []; s.actor = p;
  if (a.t === 'pass') {
    log(s, deckName(s, p) + ' passes.');
    if (s.passed !== null) {
      if (!s.stopAtRoundEnd) return endRound(s);
      resolveRoundEnd(s);          // searches stop here: they compare outcomes of this round only
      s.roundOver = true;
      return s;
    }
    s.passed = p; s.cur = other(p); s.turn++;
    return s;
  }
  s.acts++; s.passed = null;
  ACTIONS[a.t](s, p, a);
  updateBases(s);
  s.cur = other(p); s.turn++;
  return s;
}

/** Every legal action for the player to act (the first entry is "pass"). */
function listActions(s) {
  const p = s.cur, out = [{ t: 'pass' }], seen = new Set();
  s.players[p].hand.forEach((k, hi) => {
    if (seen.has(k)) return;
    seen.add(k);
    const card = CARDS[k];
    for (const lane of LANES) if (canPay(s, lane, card.cost))
      for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++)
        for (const o of orientations(card.size)) if (fits(s, p, lane, card.size, r, c, o)) out.push({ t: 'deploy', hi, lane, r, c, o });
  });
  for (const u of s.units.filter(x => x.owner === p)) {
    for (const o of orientationsOf(u))
      for (const m of Object.values(moveTargets(s, u, o))) out.push({ t: 'move', id: u.id, r: m.r, c: m.c, o });
    for (const t of s.units) if (canAttack(s, u, t)) out.push({ t: 'attack', id: u.id, tid: t.id });
  }
  return out;
}

/* ---------- actions ---------- */
/** Each action handler runs for the acting player p; the turn then passes to the other side (unless a choice is pending). */
const ACTIONS = {
  deploy(s, p, a) {
    const k = s.players[p].hand.splice(a.hi, 1)[0], card = CARDS[k];
    pay(s, a.lane, card.cost);
    const under = card.onto || card.sacrifice ? coveredUnits(s, p, a.lane, k, a.r, a.c, a.o) : [];
    const m = card.mods || {};
    const u = { id: s.nid++, card: k, owner: p, lane: a.lane, r: a.r, c: a.c, o: a.o, ps: m.ps || 0, pd: m.pd || 0, dmg: 0, mv: 0, born: s.round,
      ...(m.kw && Object.keys(m.kw).length ? { kw: { ...m.kw } } : {}), ...(m.off && Object.keys(m.off).length ? { off: { ...m.off } } : {}) };
    s.units.push(u);
    // Aurelius: playing it removes one copy of each card it needs from the discard pile
    for (const n of card.needs || []) { const D = s.players[p].discard, i = D.lastIndexOf(n); if (i >= 0) D.splice(i, 1); }
    // placed onto units (Corpse Gnawer): they are destroyed, and it grows
    for (const x of under) kill(s, x, card.sacrifice ? `sacrificed for ${card.name}` : `devoured by ${card.name}`);
    if (under.length && card.ontoGain) { u.ps += card.ontoGain; u.pd += card.ontoGain; }
    placeUnit(s, p, u, `${deckName(s, p)} places ${unitName(u)} in lane ${a.lane + 1}.`);
    if (under.length && card.ontoGain) log(s, `${unitName(u)} feeds: +${card.ontoGain}|+${card.ontoGain}.`);
  },
  move(s, p, a) {
    const u = byId(s, a.id), o = a.o ?? u.o, lane = a.lane !== undefined ? a.lane : u.lane, from = u.lane;
    const target = moveTargets(s, u, o, false, lane)[a.r + ',' + a.c];
    pay(s, u.lane, target.d);
    const before = lane === from ? frontCols(u) : new Set();
    moved(s, u);   // gains for moving (Tourmarches) come as it sets off
    emit(s, { move: u.id, path: target.path, o, toLane: lane, steps: Math.max(1, Math.abs(a.r - u.r) + Math.abs(a.c - u.c) + 3 * Math.abs(lane - from)) });
    u.mv = (u.mv || 0) + 1;
    Object.assign(u, { lane, r: a.r, c: a.c, o, moved: u.mv >= maxMoves(u) });
    applyAuras(s);
    log(s, lane === from ? unitName(u) + ' moves.' : `${unitName(u)} rides from lane ${from + 1} to lane ${lane + 1}.`);
    arrive(s, u, before);

  },
  attack(s, p, a) {
    const u = byId(s, a.id), t = byId(s, a.tid);
    pay(s, u.lane, attackCost(u));
    u.atk = (u.atk || 0) + 1;
    u.attacked = u.atk >= maxAttacks(u);
    log(s, `${unitName(u)} attacks ${unitName(t)}.`);
    if (cardOf(u).grubber) {
      const P = s.players[p], before = P.reserve;
      P.reserve = Math.min(MAX_CARRY, P.reserve + 1);
      if (P.reserve > before) log(s, `${unitName(u)} grabs loot: +1 carry-over.`);
    }
    strike(s, u, t, unitName(u));
    processDeaths(s);
    if (isReckless(u) && byId(s, u.id)) kill(s, u, 'reckless');
  },
  tactic(s, p, a) {
    const P = s.players[p], k = P.hand[a.hi], card = CARDS[k], lane = spellLane(s, a);
    pay(s, lane, spellCost(s, k, a));
    P.hand.splice(a.hi, 1);
    emit(s, { spell: k, p, fxl: (card.tactic === 'lane' && !NO_LANE_FX.includes(k)) || card.tactic === 'column' ? lane : null, fxc: card.tactic === 'column' ? a.col : null, fxt: a.tid ?? a.vid ?? null });
    log(s, `${deckName(s, p)} plays ${card.name}${k === 'cuts' ? ` (X = ${a.n})` : ''}.`);
    TACTICS[k](s, p, a, lane);
    processDeaths(s);   // its deaths resolve while the card is still in play
    P.discard.push(k);
    emit(s, { spellEnd: k, p });
  },
  throw(s, p, a) {
    const u = byId(s, a.id), t0 = byId(s, a.aid), lane = a.lane ?? u.lane, target = unitAt(s, a.owner, lane, a.r, a.c);
    pay(s, u.lane, attackCost(u));
    u.atk = (u.atk || 0) + 1;
    u.attacked = u.atk >= maxAttacks(u);
    log(s, `${unitName(u)} throws ${unitName(t0)}.`);
    emit(s, { toss: t0.id, by: u.id, to: { lane, owner: a.owner, r: a.r, c: a.c } });
    if (target) {
      const str = strengthOf(t0);
      t0.aloft = true;   // the screen no longer draws it in its old cell: it is in the air, then dies where it lands
      s.fxHow = 'thrown';
      try { hitUnit(s, str, target, unitName(t0) + ' (thrown)', t0.id, false, true); } finally { s.fxHow = undefined; }
      processDeaths(s);
      if (byId(s, t0.id)) {
        // it dies where it lands: its death (Plague, Death effects, Shades in its cell) happens in that cell
        Object.assign(t0, { owner: a.owner, lane, r: a.r, c: a.c, o: 'h' });
        if (a.owner === p) delete t0.ctl; else t0.ctl = p;
        delete t0.aloft;
        kill(s, t0, 'thrown', { silent: true });
      }
      return;
    }
    const before = a.owner === p && t0.owner === p && lane === t0.lane ? frontCols(t0) : new Set();
    Object.assign(t0, { owner: a.owner, lane, r: a.r, c: a.c, o: 'h' });
    if (a.owner === p) delete t0.ctl; else t0.ctl = p;
    emit(s, { place: t0.id });
    moved(s, t0);
    if (a.owner === p) arrive(s, t0, before);
  },
  // ----- follow-up steps -----
  fmove(s, p, a) {
    const u = byId(s, a.id), before = frontCols(u);
    emit(s, { move: u.id, path: [[u.r, u.c], [a.r, a.c]], o: a.o, steps: Math.max(1, Math.abs(a.r - u.r) + Math.abs(a.c - u.c)) });
    Object.assign(u, { r: a.r, c: a.c, o: a.o });
    applyAuras(s);
    log(s, unitName(u) + ' redeploys.');
    moved(s, u);
    arrive(s, u, before);
    s.pending.n--;
    if (s.pending.n <= 0) s.pending = null;
  },
  pick(s, p, a) {
    const P = s.pending, t = byId(s, a.tid);
    s.pending = null;
    if (P.k === 'pull') {
      log(s, `${unitName(t)} is pulled forward.`);
      if (!slide(s, t, fwd(t.owner))) log(s, `${unitName(t)} can't move.`);
    } else if (P.k === 'defect') s.pending = { k: 'place', p, lane: P.lane, tid: t.id };
    else if (P.k === 'cinder') {
      const imp = byId(s, P.src);   // both hits use the amount fixed when it was placed
      dealDamage(s, P.amt, t, 'Cinder Imp', imp);
      processDeaths(s);
      if (imp && byId(s, imp.id)) damageFacing(s, imp, P.amt, 'Cinder Imp');
    } else if (P.k === 'duel') {
      const v = byId(s, P.vid), a1 = strengthOf(v), a2 = strengthOf(t);
      log(s, `${unitName(v)} and ${unitName(t)} meet in single combat.`);
      hitUnit(s, a1, t, unitName(v), v.id);
      hitUnit(s, a2, v, unitName(t), t.id);
    } else if (P.k === 'pair') {
      const v = byId(s, P.vid);
      for (const u of [v, t]) { u.ps = (u.ps || 0) + 1; u.pd = (u.pd || 0) + 1; }
      log(s, `${unitName(v)} and ${unitName(t)} lock shields: +1 strength, +1 defence each.`);
    } else if (P.k === 'surgeon') {
      dealDamage(s, 1, t, 'Pale Surgeon', byId(s, P.src));
      if (byId(s, t.id)) { t.ps = (t.ps || 0) + 2; log(s, `${unitName(t)} is improved: +2 strength.`); }
    } else if (P.k === 'embalm') { giveKw(t, 'revenant'); log(s, `${unitName(t)} is embalmed: it gains Revenant.`); }
    else if (P.k === 'letter') {
      const me = byId(s, P.src);
      if (me) hitUnit(s, P.amt, me, unitName(me) + ' (itself)', null, true, true, true);
      dealDamage(s, P.amt, t, 'Blood-Letter', me);
    }
    else if (P.k === 'kiss') {
      const v = byId(s, P.vid);
      hitUnit(s, 3, t, 'Kiss of the Revenant', null);
      if (v) restoreShields(s, v, 3, 'Kiss of the Revenant');
    } else if (P.k === 'vsrc') s.pending = { k: 'vkw', p, lane: P.lane, src: P.src, vid: t.id };
    else if (P.k === 'vdst') {
      const v = byId(s, P.vid), f = P.f, val = kw(v, f);
      if (v.kw && v.kw[f]) v.kw = { ...v.kw, [f]: 0 };
      if (cardOf(v)[f]) v.off = { ...(v.off || {}), [f]: true };
      giveKw(t, f, val);
      log(s, `Doctor Vessane moves ${KW_NAME[f]} from ${unitName(v)} to ${unitName(t)}.`);
    }
  },
  gpick(s, p, a) {
    const P = s.pending, D = s.players[p].discard, i = D.lastIndexOf(a.key);
    P.left--;
    if (P.pool) { const j = P.pool.indexOf(a.key); P.pool = P.pool.filter((k, n) => n !== j); }
    if (i >= 0) {
      D.splice(i, 1);
      if (P.mode === 'rez') resurrect(s, p, a.key, P.lane);
      else if (s.players[p].hand.length < HAND_LIMIT) { s.players[p].hand.push(a.key); emit(s, { handIn: p, k: a.key, from: 'discard' }); log(s, `${CARDS[a.key].name} returns to the hand.`); }
      else D.push(a.key);
    }
    if (s.pending === P && (P.left <= 0 || !graveOptions(s, p, P.mode, P.pool).length)) s.pending = null;
  },
  kpick(s, p, a) { const P = s.pending; s.pending = { k: 'vdst', p, lane: P.lane, src: P.src, vid: P.vid, f: a.f }; },
  place(s, p, a) {
    if (s.pending.card) {
      const P = s.pending;
      s.pending = null;
      resurrect(s, p, P.card, P.lane, { r: a.r, c: a.c, o: a.o });
      return;
    }
    const t = byId(s, s.pending.tid);
    s.pending = null;
    const from = deckName(s, ctl(t));
    Object.assign(t, { owner: p, r: a.r, c: a.c, o: a.o, mv: maxMoves(t), moved: true, attacked: true });
    delete t.ctl;
    placeUnit(s, p, t, `${unitName(t)} leaves ${from} and is placed with ${deckName(s, p)}.`);
  },
  done(s) { s.pending = null; },
};

/** Link: Link units of one side in one camp that touch edges merge into the older one (current stats, supply, keywords added). */
function mergeLinks(s) {
  for (;;) {
    applyAuras(s);
    const links = s.units.filter(u => cardOf(u).link).sort((x, y) => x.id - y.id);
    let pair = null;
    for (const a of links) {
      const ca = cellsOf(a);
      const b = links.find(o => o.id > a.id && o.owner === a.owner && ctl(o) === ctl(a) && o.lane === a.lane &&
        cellsOf(o).some(([r, c]) => ca.some(([r2, c2]) => Math.abs(r - r2) + Math.abs(c - c2) === 1)));
      if (b) { pair = [a, b]; break; }
    }
    if (!pair) return;
    const [a, b] = pair;
    const S = strengthOf(a) - (a.ts || 0) + strengthOf(b) - (b.ts || 0), D = defenceOf(a) + defenceOf(b);
    a.sup = unitSupply(a) + unitSupply(b);
    a.ts = (a.ts || 0) + (b.ts || 0);
    for (const f of KW_FLAGS) if (kw(b, f) && !kw(a, f)) giveKw(a, f, kw(b, f));
    a.mv = Math.max(a.mv || 0, b.mv || 0);
    a.attacked = a.attacked || b.attacked;
    a.extra = [...(a.extra || []), b.card, ...(b.extra || [])];
    growInto(a, cellsOf(b));
    s.units = s.units.filter(x => x.id !== b.id);
    applyAuras(s);
    a.ps = (a.ps || 0) + S - (strengthOf(a) - (a.ts || 0));
    a.pd = (a.pd || 0) + D - defenceOf(a);
    emit(s, { merge: a.id });
    log(s, `${unitName(a)} links with ${unitName(b)}: now ${strengthOf(a)}|${defenceOf(a)}, supply ${a.sup}.`);
  }
}

function applyAction(s, a) {
  const p = s.cur;
  s.fx = []; s.ev = []; s.tombs = []; s.resStack = []; s.chainN = 0; s.deadUnits = []; s.actor = p; s.carried = null;
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
  if (!PENDING_STEPS.has(a.t)) { s.acts++; s.passed = null; }
  ACTIONS[a.t](s, p, a);
  processDeaths(s);
  mergeLinks(s);
  applyAuras(s);
  updateBases(s);
  if (s.pending && !pendingActions(s).length) s.pending = null;     // nothing left to choose
  if (!s.pending && s.arrQ) {
    const q = s.arrQ;
    s.arrQ = null;
    for (const x of q) { const u = byId(s, x.id); if (u) arriveInto(s, u, x.cols); }
    processDeaths(s); mergeLinks(s); applyAuras(s); updateBases(s);
  }
  settleTables(s);
  applyAuras(s);
  if (!s.pending) { s.cur = other(p); s.turn++; }
  return s;
}

/** Every legal action for the player to act (first entry is "pass" unless a follow-up choice is pending). */
/** forAi: the computer's list (skips spell uses it never wants, see spellOptions); the screen passes false. */
function listActions(s, forAi = true) {
  if (s.pending) return pendingActions(s);
  const p = s.cur, out = [{ t: 'pass' }], seen = new Set();
  s.players[p].hand.forEach((k, hi) => {
    if (seen.has(k)) return;
    seen.add(k);
    const card = CARDS[k];
    if (!card.tactic) {
      if (!needsMet(s, p, k)) return;
      for (const lane of LANES) if (canPay(s, lane, card.cost))
        for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++)
          for (const o of orientations(card.size)) if (deployFits(s, p, lane, k, r, c, o)) out.push({ t: 'deploy', hi, lane, r, c, o });
    } else for (const x of spellOptions(s, p, k, forAi)) out.push({ t: 'tactic', hi, ...x });
  });
  for (const u of s.units.filter(x => ctl(x) === p)) {
    for (const lane of cardOf(u).outrider ? LANES : [u.lane]) for (const o of orientationsOf(u))
      for (const m of Object.values(moveTargets(s, u, o, false, lane))) out.push(lane === u.lane ? { t: 'move', id: u.id, r: m.r, c: m.c, o } : { t: 'move', id: u.id, lane, r: m.r, c: m.c, o });
    for (const t of s.units) if (canAttack(s, u, t)) out.push({ t: 'attack', id: u.id, tid: t.id });
    for (const a of throwables(s, u)) for (const x of throwTargets(s, u, a)) out.push({ t: 'throw', id: u.id, aid: a.id, ...x });
  }
  return out;
}


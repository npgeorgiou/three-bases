/* ---------- combat ---------- */
/** Remove a unit. opt.killer: id of the unit whose hit killed it; opt.silent: the hit animation already shows the death. */
function kill(s, u, why, opt = {}) {
  if (!byId(s, u.id)) return;
  if (!opt.silent) emit(s, { dead: u.id });
  if (s.noFx) s.deadUnits = [...(s.deadUnits || []), { ...u }];   // previews: where a unit died
  s.units = s.units.filter(x => x.id !== u.id);
  // a tombstone keeps its cells (no dots, no actions) until its death resolves
  if (!opt.noTomb) s.tombs = [...(s.tombs || []), { id: u.id, card: u.card, owner: u.owner, ctl: ctl(u), lane: u.lane, cells: cellsOf(u).map(x => [x[0], x[1]]), u: s.noFx ? null : { ...u } }];
  if (keepsCard(u.card)) s.players[ctl(u)].discard.push(baseKey(u.card));
  // Danse Macabre: where each of p's units died this round
  { const P = s.players[ctl(u)]; P.fell = [...(P.fell || []).filter(x => x.round === s.round), { round: s.round, card: u.card, lane: u.lane, camp: u.owner, r: u.r, c: u.c, o: u.o, sh: u.sh ? normShape(cellsOf(u)) : null }]; }
  for (const k of u.extra || []) s.players[ctl(u)].discard.push(k);
  if (opt.taken) u.taken = true;
  log(s, `${unitName(u)} (${deckName(s, ctl(u))}) dies${why ? ' — ' + why : ''}.`);
  const killer = opt.killer ? byId(s, opt.killer) : null;
  if (killer && ctl(killer) !== ctl(u) && cardOf(killer).skull) {
    const c = cardOf(u);
    killer.ps = (killer.ps || 0) + c.str; killer.pd = (killer.pd || 0) + c.def;
    if (c.str || c.def) log(s, `${unitName(killer)} devours it: +${c.str} strength, +${c.def} defence.`);
  }
  s.ev.push({ die: u });
  applyAuras(s);
}

/** After a unit survives a hit: Pain Eater grows, Varangoi in its lane harden it (+1 defence). */
function survived(s, u) {
  const c = cardOf(u);
  if (c.pain) { u.ps = (u.ps || 0) + c.pain; log(s, `${unitName(u)} feeds on the pain: +${c.pain} strength.`); }
  for (const v of s.units) if (cardOf(v).veteran && targetsOf(s, v, 'veteran').includes(u)) {
    u.pd = (u.pd || 0) + 1;
    log(s, `${unitName(v)} harden ${unitName(u)}: +1 defence.`);
  }
  applyAuras(s);
}

/** Hit a unit with `str`. Returns {killed, excess} or null if nothing was hit. */
/** byUnit: the hit is dealt by a unit (an attack, an ability, a strike a spell makes a unit deal); Incorporeal units ignore it. */
/** notStrike: damage an ability deals (a fixed amount): effects that fire on its strikes don't fire. */
function hitUnit(s, str, target, source, sourceId, noGuard, byUnit = !!sourceId, notStrike = false) {
  const res = hitOnce(s, str, target, source, sourceId, noGuard, byUnit, notStrike), src = res && sourceId ? byId(s, sourceId) : null;
  if (!src || !byUnit || notStrike) return res;
  const c = cardOf(src), p = ctl(src);
  if (c.gore && (!res.t || res.t.id !== src.id)) { src.ps = (src.ps || 0) + c.gore; log(s, `${unitName(src)} grows on blood: +${c.gore} strength.`); applyAuras(s); }
  if (res.killed && res.t && ctl(res.t) !== p) {
    if (c.plunder) { s.pool[p][src.lane]++; s.poolStart[p][src.lane]++; log(s, `${unitName(src)} plunders: +1 supply in lane ${src.lane + 1}.`); }
    if (c.trophy) {
      const E = s.players[other(p)], H = s.players[p];
      if (E.draw.length && H.hand.length < HAND_LIMIT) { H.hand.push(E.draw.pop()); log(s, `${unitName(src)} takes a trophy: the top card of ${deckName(s, other(p))}'s deck.`); emit(s, { draw: p, n: 1 }); }
    }
  }
  return res;
}
function hitOnce(s, str, target, source, sourceId, noGuard, byUnit, notStrike) {
  if (!target || !byId(s, target.id) || str <= 0) return null;
  if (byUnit && isIncorp(target)) { log(s, `${source} passes through ${unitName(target)}.`); return null; }
  applyAuras(s);
  // Bodyguard: an adjacent ally with Bodyguard takes the hit instead (not for a unit hitting itself or a guard's own hits)
  if (!noGuard && sourceId !== target.id) {
    const guard = adjacentAllies(s, target).filter(g => cardOf(g).guard && g.id !== sourceId && !(byUnit && isIncorp(g))).sort(byReadingOrder)[0];
    if (guard) {
      log(s, `${unitName(guard)} takes the hit for ${unitName(target)}.`);
      target = guard;
      if (cardOf(guard).guardGrow) {
        const res = hitOnce(s, str, guard, source, sourceId, true, byUnit, notStrike);
        if (res && byId(s, guard.id)) { guard.pd = (guard.pd || 0) + 1; log(s, `${unitName(guard)} +1 defence.`); applyAuras(s); }
        return res;
      }
    }
  }
  const src = sourceId ? byId(s, sourceId) : null;
  if (src && !notStrike && cardOf(src).duel && ctl(src) !== ctl(target) && strengthOf(target) < printedStr(target)) str += cardOf(src).duel;
  if (isArmoured(target) && !target.armUsed) {
    target.armUsed = true;
    emit(s, { hit: true, src: sourceId || null, from: s.fxFrom || undefined, how: s.fxHow || undefined, t: target.id, str, broke: 0, kill: false, blocked: true });
    log(s, `${source} hits ${unitName(target)}, but its armour holds.`);
    survived(s, target);
    return { killed: false, excess: 0, t: target };
  }
  const def = defenceOf(target), dies = str >= def;
  emit(s, { hit: true, src: sourceId || null, from: s.fxFrom || undefined, how: s.fxHow || undefined, t: target.id, str, broke: Math.min(str, def), kill: dies, drain: s.drainFx || undefined });
  if (dies) { kill(s, target, 'hit by ' + source, { killer: sourceId, silent: true }); return { killed: true, excess: str - def, t: target }; }
  target.dmg = (target.dmg || 0) + str;
  log(s, `${source} hits ${unitName(target)}: ${str} shield${str > 1 ? 's' : ''} lost.`);
  survived(s, target);
  if (src && !notStrike && ctl(src) !== ctl(target) && byId(s, target.id)) {
    const sc = cardOf(src);
    if (sc.plagueHit) catchPlague(s, target, unitName(src));
    if (sc.blightHit && !target.blight) { target.blight = true; log(s, `${unitName(target)} is Blighted.`); }
    if (sc.exec && strengthOf(target) === 0) { kill(s, target, unitName(src) + ' executes it', { killer: src.id }); return { killed: true, excess: 0, t: target }; }
    if (sc.headsman && isBloodied(target)) { kill(s, target, unitName(src) + ' beheads it', { killer: src.id }); return { killed: true, excess: 0, t: target }; }
    applyAuras(s);
  }
  return { killed: false, excess: 0, t: target };
}

/** The enemy facing unit u: the nearest one to the base in u's column(s) of the enemy camp, or null. */
function facingTarget(s, u) {
  if (!u) return null;
  const q = other(u.owner), map = occupancy(s, q, u.lane), cols = colsOf(u);
  const rows = [0, 1, 2].sort((a, b) => Math.abs(a - frontRow(q)) - Math.abs(b - frontRow(q)));
  for (const r of rows) for (const c of cols) { const t = map[r + ',' + c]; if (t && ctl(t) !== ctl(u)) return t; }
  return null;
}
/**
 * Reach (AGREED, October 2026). A lane's two camps form one column of 6 rows (top camp rows 0-2, bottom camp rows 3-5),
 * so the two front rows touch across the base. A melee unit reaches every cell adjacent to one of its cells (diagonals
 * included); Pike also reaches the opposite camp's front-row cells two rows ahead of it (column ±1). Ranged units reach
 * every cell of their lane. A strike (an attack, a charge, or a strike with the unit's strength from an ability or a
 * spell) only hits enemies in reach.
 */
const laneRow = (owner, r) => (owner === 1 ? r : ROWS + r);
function reachesCell(u, owner, r, c) {
  if (kw(u, 'ranged')) return true;
  const f = u.owner === 0 ? -1 : 1;   // toward the other camp, in lane rows
  const R = laneRow(owner, r), pikeRow = laneRow(other(u.owner), frontRow(other(u.owner)));
  return cellsOf(u).some(([ur, uc]) => {
    const G = laneRow(u.owner, ur);
    if (Math.abs(c - uc) > 1) return false;
    if ((G !== R || uc !== c || owner !== u.owner) && Math.abs(G - R) <= 1) return true;
    return kw(u, 'reach') && R === G + 2 * f && R === pikeRow;
  });
}
/** Whether u could strike t now by position: t is in its lane and one of t's cells is in u's reach. */
const reaches = (u, t) => !!t && t.lane === u.lane && t.id !== u.id && cellsOf(t).some(([r, c]) => reachesCell(u, t.owner, r, c));
/** Page order of the board as side p sees it (the resolution order): top to bottom, left to right on p's screen. */
/**
 * Resolution order from side p's seat (AGREED): the first row is the row closest to the base. Front rows first (each camp's
 * own front row), then the middle rows, then the back rows; within a row depth, lanes and columns left to right as p sees them,
 * p's own camp before the enemy's.
 */
const seatKey = (u, p) => Math.min(...cellsOf(u).map(([r, c]) => {
  const depth = Math.abs(r - frontRow(u.owner)), lane = p === 0 ? u.lane : 2 - u.lane, col = p === 0 ? c : 2 - c;
  return depth * 20 + lane * 6 + col * 2 + (u.owner === p ? 0 : 1);
}));
/** Sort comparator: page order from side p's seat. */
const bySeat = p => (a, b) => seatKey(a, p) - seatKey(b, p);
/** The enemies u could strike, in resolution order. */
/** How near t is to u (AGREED, 10 Oct 2026): the squared distance between their nearest cells, the two camps of a lane forming
 *  one column of rows; an enemy touching u on a side (the one directly facing it across the base) is nearer than one at a corner. */
const nearness = (u, t) => Math.min(...cellsOf(u).flatMap(([ur, uc]) => cellsOf(t).map(([tr, tc]) => {
  const dr = laneRow(u.owner, ur) - laneRow(t.owner, tr), dc = uc - tc;
  return dr * dr + dc * dc;
})));
/** The enemies u could strike, nearest first (ties in resolution order). */
const strikeTargets = (s, u) => s.units.filter(t => ctl(t) !== ctl(u) && reaches(u, t))
  .sort((a, b) => nearness(u, a) - nearness(u, b) || seatKey(a, ctl(u)) - seatKey(b, ctl(u)));
/** The nearest enemy u could strike (Manganon, Frenzy, Martyrdom), or null. */
const strikeTarget = (s, u) => strikeTargets(s, u)[0] || null;
/** Damage an ability of u deals (a fixed amount, not a strike): no on-strike effects; Incorporeal units ignore it. */
const dealDamage = (s, amt, t, source, u) => hitUnit(s, amt, t, source, u ? u.id : null, false, true, true);
/** u deals `amt` damage to the nearest enemy in its column. */
function damageFacing(s, u, amt, source) {
  const t = facingTarget(s, u);
  if (t) return dealDamage(s, amt, t, source, u);
  log(s, source + ' finds no target.');
  return null;
}

/** An ability hit dealt by unit u: its printed amount plus any strength bonus u has. */
const abilityHit = (u, base) => Math.max(0, base + strengthOf(u) - printedStr(u));

/** Unit u strikes t with its strength (an attack or a charge hit), with Splash, Push and Overrun. */
function strike(s, u, t, label, fixedStr, batch = false) {
  const c = cardOf(u), str = fixedStr !== undefined ? fixedStr : strengthOf(u), q = t.owner, lane = t.lane;
  let wasFront = inFront(t);
  let res = hitUnit(s, str, t, label, u.id);
  if (!res) return null;
  if (res.t && res.t.id !== t.id) { t = res.t; wasFront = false; }   // a Bodyguard took it: no push
  if (c.splash) {
    // each hit unit passes half of what it received (rounded down) to the units right behind its cells, split evenly (rounded down)
    const done = new Set([t.id]);
    let wave = [[t, str]];
    while (wave.length) {
      const next = [];
      for (const [v, got] of wave) {
        const back = unitsBehind(s, v).filter(x => !done.has(x.id)), each = back.length ? Math.floor(Math.floor(got / 2) / back.length) : 0;
        if (each <= 0) continue;
        for (const x of back) { done.add(x.id); if (hitUnit(s, each, x, label + ' (splash)', u.id)) next.push([x, each]); }
      }
      wave = next;
    }
  }
  if (c.push && !res.killed && wasFront && byId(s, t.id)) {
    if (slide(s, t, -fwd(q), 1)) log(s, `${unitName(u)} pushes ${unitName(t)} back.`);
  }
  if (c.overrun && res.killed && res.excess > 0) {
    // a kill passes its leftover strength to the units right behind the victim's cells, split evenly (rounded down); each further kill passes on again
    const done = new Set([t.id]);
    let wave = [[t, res.excess]];
    while (wave.length) {
      const next = [];
      for (const [v, left] of wave) {
        const back = unitsBehind(s, v).filter(x => !done.has(x.id)), each = back.length ? Math.floor(left / back.length) : 0;
        if (each <= 0) continue;
        for (const x of back) {
          done.add(x.id);
          const r = hitUnit(s, each, x, label + ' (overrun)', u.id);
          if (r && r.killed && r.excess > 0) next.push([x, r.excess]);
        }
      }
      wave = next;
    }
  }
  if (batch) return res;   // one step of several strikes: the caller resolves the deaths, then the ripostes
  processDeaths(s);
  riposte(s, u, res);
  return res;
}
/** Riposte: a struck unit that survived strikes the attacker back (after the strike's deaths). */
function riposte(s, u, res) {
  if (res && !res.killed && res.t && byId(s, res.t.id) && byId(s, u.id) && kw(res.t, 'riposte') && ctl(res.t) !== ctl(u) && strengthOf(res.t) > 0)
    hitUnit(s, strengthOf(res.t), u, unitName(res.t) + ' (riposte)', res.t.id);
}
/** u strikes several units in one step (a charge into two units): all take their damage at once, then the deaths resolve, then ripostes. */
function strikeAll(s, u, targets, label, str) {
  const done = targets.map(t => (byId(s, t.id) && byId(s, u.id) ? strike(s, u, t, label, str, true) : null));
  processDeaths(s);
  for (const res of done) riposte(s, u, res);
}

function canAttack(s, a, t) {
  if (!a || !t || a.id === t.id || a.attacked || ctl(a) !== s.cur || a.lane !== t.lane || s.pending) return false;
  if (strengthOf(a) <= 0 || !canPay(s, a.lane, attackCost(a))) return false;
  if (isIncorp(t)) return false;   // only spells can hit Incorporeal units
  if (ctl(a) === ctl(t)) return !!cardOf(a).hitsOwn;   // Warlord: any other own unit in its lane
  return reaches(a, t);
}

/**
 * Resolution chains (AGREED, 10 Oct 2026). An effect that happens all at once hits all its targets at the same moment;
 * the units it kills die at that moment (a tombstone keeps their cells until their turn). Then the affected units take
 * turns in resolution order: each one's chain (its own Death effects, then its camp's reactions, then the enemy's) runs
 * to the end, and every effect inside a chain opens its own chain for the units it hits, which closes before that chain
 * continues. processDeaths closes the chains of the deaths queued so far (depth first).
 */
function processDeaths(s) {
  s.grp = (s.grp || 0) + 1;
  if ((s.depth || 0) > 40 || (s.chainN || 0) > 600) return;   // a runaway loop of returns stops here
  s.depth = (s.depth || 0) + 1;
  try { drainDeaths(s); } finally { s.depth--; }
  checkGorvan(s);
  applyAuras(s);
}
/** The tombstone of unit id: removed when its turn comes. */
const dropTomb = (s, id) => { if (s.tombs && s.tombs.length) s.tombs = s.tombs.filter(t => t.id !== id); };
function drainDeaths(s) {
  while (s.ev.length) {
    const { die: u } = s.ev.shift();
    if (!u) continue;
    s.chainN = (s.chainN || 0) + 1;
    const rest = s.ev;   // the other deaths of the same moment wait until this one's chain is closed
    s.ev = [];
    s.grp = (s.grp || 0) + 1;
    // its death is resolved now: its tombstone stays (lit, white cell border) until its whole chain is done
    if (s.tombs) s.tombs = s.tombs.map(t => (t.id === u.id ? { ...t, res: true } : t));
    s.resStack = [...(s.resStack || []), u.id];   // the death being resolved right now is the last one
    if ((s.tombs || []).some(t => t.id === u.id)) emit(s, { resolve: u.id });
    const fromWas = s.fxFrom;
    s.fxFrom = u.id;   // its Death effects come from its cell
    const c = cardOf(u), before = s.noFx ? null : new Map(s.units.map(v => [v.id, [strengthOf(v), defenceOf(v) + Math.max(0, v.dmg || 0)]]));
    deathGains(s, u);   // gains first, at the moment of the death
    if (before) {
      const grew = s.units.filter(v => { const b = before.get(v.id); return b && (strengthOf(v) > b[0] || defenceOf(v) + Math.max(0, v.dmg || 0) > b[1]); }).map(v => v.id);
      if (grew.length) { emit(s, { grow: grew }); for (const v of s.units) if (grew.includes(v.id)) before.set(v.id, [strengthOf(v), defenceOf(v) + Math.max(0, v.dmg || 0)]); }
    }
    // order: the dying unit's own effects, then its own camp's reactions, then the enemy's (see exDeath)
    // Death effects: the unit is already gone; dead units deal damage, they don't strike. Each one is an effect of its own:
    // its targets are hit at once, then their chains close before the next one.
    const deathDamage = (flag, amt, label) => {
      for (const t of targetsOf(s, u, flag).sort(bySeat(ctl(u)))) dealDamage(s, amt, t, unitName(u) + label, null);
      processDeaths(s);
    };
    if (c.keg) deathDamage('keg', abilityHit(u, c.keg), ' (blast)');
    if (c.deathHit) deathDamage('deathHit', abilityHit(u, c.deathHit), ' (death)');
    if (c.deathLane) deathDamage('deathLane', abilityHit(u, c.deathLane), ' (death)');
    if (c.deathAdjHeal) for (const a of targetsOf(s, u, 'deathAdjHeal')) restoreShields(s, a, c.deathAdjHeal, unitName(u));
    if (c.deathDraw) { const n = drawCards(s, ctl(u), c.deathDraw); if (n) { log(s, `${unitName(u)}: ${deckName(s, ctl(u))} draws ${n}.`); emit(s, { draw: ctl(u), n }); } }
    exDeath(s, u);
    // returns to the hand only if no Revenant return took its card first
    if (c.deathReturn) {
      const P = s.players[ctl(u)], i = P.discard.lastIndexOf(baseKey(u.card));
      if (i >= 0 && P.hand.length < HAND_LIMIT) { const k = carriedCard(u); P.discard.splice(i, 1); P.hand.push(k); emit(s, { handIn: ctl(u), k, from: 'discard' }); log(s, `${unitName(u)} returns to ${deckName(s, ctl(u))}'s hand.`); }
    }
    s.fxFrom = fromWas;
    applyAuras(s);
    // stat gains from this death (Carrion Chief, Pallid Mourner, Grafter...) show at once, before the next death resolves
    if (before) {
      const grew = s.units.filter(v => { const b = before.get(v.id); return b && (strengthOf(v) > b[0] || defenceOf(v) + Math.max(0, v.dmg || 0) > b[1]); }).map(v => v.id);
      if (grew.length) emit(s, { grow: grew });
    }
    drainDeaths(s);   // anything its chain left
    const tomb = (s.tombs || []).find(t => t.id === u.id);
    dropTomb(s, u.id);
    s.resStack = (s.resStack || []).filter(id => id !== u.id);
    if (tomb) emit(s, { resolved: u.id, tomb });   // its chain is closed: the dead unit leaves the board
    s.ev = rest;
  }
}

function updateBases(s) {
  for (const lane of LANES) {
    const o = laneOwner(s, lane);
    if (o === s.owner[lane]) continue;
    log(s, o !== null ? `${deckName(s, o)} takes base ${lane + 1}.` : `${deckName(s, s.owner[lane])} loses base ${lane + 1}.`);
    s.owner[lane] = o;
    if (o !== null) emit(s, { capture: lane, p: o });
  }
}


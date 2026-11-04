/* ---------- general card effects (fx): card data says when, who and what; no per-card code ----------
   Unit: fx: [{on, if, lim, of, do: [op, ...]}], aura: [{to, s, d, if}]. Spell: cast: {do: [op, ...], need}.
   on: place, death, roundEnd, roundStart, survive, attack, move, arrive (I come from another lane), spell (you cast one),
       allyPlace, allyDeath, enemyDeath, allyArrive (in my lane). of: a card flag the other unit must have (e.g. 'proj').
   lim: 'round' = at most once per round per unit. Amounts: a number, or {count: selector, x: multiplier, plus}. */
const FX_ONCE = 'round';
const fxCamp = (s, owner, lane) => s.units.filter(x => x.lane === lane && x.owner === owner);
const touches = (u, a) => cellsOf(u).some(([r, c]) => cellsOf(a).some(([ar, ac]) => Math.abs(r - ar) <= 1 && Math.abs(c - ac) <= 1));
const edgeTouch = (u, a) => cellsOf(u).some(([r, c]) => cellsOf(a).some(([ar, ac]) => Math.abs(r - ar) + Math.abs(c - ac) === 1));
const fxAlive = (s, u) => (u ? byId(s, u.id) : null);
/** The enemy nearest to the base in u's own column(s) of the facing camp. */
function fxFacing(s, u) {
  const foe = s.units.filter(t => ctl(t) !== ctl(u) && t.lane === u.lane && t.owner !== u.owner && colsOf(t).some(c => colsOf(u).includes(c)));
  return foe.sort((a, b) => Math.abs(Math.min(...cellsOf(a).map(x => x[0])) - frontRow(a.owner)) - Math.abs(Math.min(...cellsOf(b).map(x => x[0])) - frontRow(b.owner)))[0] || null;
}
const lanesOf = c => (c.all ? LANES : [c.lane]);
const FX_SEL = {
  self: (s, c) => one(fxAlive(s, c.u)),
  it: (s, c) => one(fxAlive(s, c.t)),
  facing: (s, c) => one(c.u && fxFacing(s, c.u)),
  nearest: (s, c) => one(c.u && byId(s, c.u.id) ? strikeTarget(s, c.u) : null),
  enemies: (s, c) => s.units.filter(x => lanesOf(c).includes(x.lane) && ctl(x) !== c.p),
  allies: (s, c) => s.units.filter(x => lanesOf(c).includes(x.lane) && ctl(x) === c.p && (!c.u || x.id !== c.u.id)),
  team: (s, c) => s.units.filter(x => lanesOf(c).includes(x.lane) && ctl(x) === c.p),
  adj: (s, c) => (c.u ? fxCamp(s, c.u.owner, c.u.lane).filter(x => x.id !== c.u.id && ctl(x) === c.p && touches(c.u, x)) : []),
  adjEnemies: (s, c) => (c.u ? fxCamp(s, c.u.owner, c.u.lane).filter(x => x.id !== c.u.id && ctl(x) !== c.p && touches(c.u, x)) : []),
  row: (s, c) => (c.u ? fxCamp(s, c.u.owner, c.u.lane).filter(x => x.id !== c.u.id && ctl(x) === c.p && rowsOf(x).some(r => rowsOf(c.u).includes(r))) : []),
  col: (s, c) => (c.u ? fxCamp(s, c.u.owner, c.u.lane).filter(x => x.id !== c.u.id && ctl(x) === c.p && colsOf(x).some(k => colsOf(c.u).includes(k))) : []),
  colEnemies: (s, c) => s.units.filter(x => x.lane === c.lane && ctl(x) !== c.p && colsOf(x).includes(c.col ?? (c.u ? colsOf(c.u)[0] : 1))),
  enemyFront: (s, c) => FX_SEL.enemies(s, c).filter(x => inFront(x)),
  enemyBack: (s, c) => FX_SEL.enemies(s, c).filter(x => !inFront(x)),
  weakest: (s, c) => one(FX_SEL.enemies(s, c).sort((a, b) => defenceOf(a) - defenceOf(b) || byReadingOrder(a, b))[0]),
  strongest: (s, c) => one(FX_SEL.enemies(s, c).sort((a, b) => strengthOf(b) - strengthOf(a) || byReadingOrder(a, b))[0]),
  hurtAlly: (s, c) => one(FX_SEL.team(s, c).filter(x => (x.dmg || 0) > 0).sort((a, b) => b.dmg - a.dmg)[0]),
  allEnemies: (s, c) => s.units.filter(x => ctl(x) !== c.p),
  allAllies: (s, c) => s.units.filter(x => ctl(x) === c.p && (!c.u || x.id !== c.u.id)),
  itAdj: (s, c) => (c.t ? fxCamp(s, c.t.owner, c.t.lane).filter(x => x.id !== c.t.id && ctl(x) === ctl(c.t) && touches(c.t, x)) : []),
  inFrontOfIt: (s, c) => { const t = c.t; if (!t) return []; const r = Math.min(...cellsOf(t).map(x => x[0] * fwd(t.owner))) * fwd(t.owner) + fwd(t.owner);
    return one(fxCamp(s, t.owner, t.lane).find(x => x.id !== t.id && cellsOf(x).some(([xr, xc]) => xr === r && colsOf(t).includes(xc)))); },
  otherLanes: (s, c) => s.units.filter(x => ctl(x) === c.p && x.lane !== c.lane),
};
function fxSel(s, c, to) {
  if (!to) return one(fxAlive(s, c.t) || fxAlive(s, c.u));
  const [name, f] = to.split(':');
  let out = (FX_SEL[name] || (() => []))(s, c).filter(Boolean);
  if (f) out = out.filter(x => cardOf(x)[f] || (x.kw && x.kw[f]) || x[f]);
  return out;
}
const fxAmount = (s, c, n) => {
  if (typeof n === 'number' || !n) return n || 0;
  if (n.stat) { const u = fxSel(s, c, n.of)[0]; return u ? (n.stat === 'str' ? strengthOf(u) : defenceOf(u)) + (n.plus || 0) : 0; }
  return Math.min(n.max ?? Infinity, fxSel(s, c, n.count).length * (n.x || 1) + (n.plus || 0));
};
const spellsThisRound = (s, p) => (s.players[p].spR === s.round ? s.players[p].spN : 0);
/** Whether the condition holds now. */
function fxIf(s, c, w) {
  if (!w) return true;
  if (w.hold !== undefined && (laneOwner(s, c.lane) === c.p) !== !!w.hold) return false;
  if (w.front && !(c.u && inFront(c.u))) return false;
  if (w.back && !(c.u && !inFront(c.u))) return false;
  if (w.min && fxSel(s, c, w.min[0]).length < w.min[1]) return false;
  if (w.max && fxSel(s, c, w.max[0]).length > w.max[1]) return false;
  if (w.spells && spellsThisRound(s, c.p) < w.spells) return false;
  if (w.other && !s.units.some(x => ctl(x) === c.p && x.lane !== c.lane && baseKey(x.card) === w.other)) return false;
  if (w.alone && s.units.some(x => ctl(x) === c.p && x.lane === c.lane && (!c.u || x.id !== c.u.id))) return false;
  return fxIfMore(s, c, w);
}
/** A free spot for a 1-cell (or k-shaped) unit: next to u, in the front row, the back rows, or anywhere. */
function fxSpot(s, p, lane, k, at, u) {
  let spots = freeSpots(s, p, lane, k);
  if (at === 'adj' && u) spots = spots.filter(x => cellsAt(CARDS[k].size, x.r, x.c, x.o).some(([r, cc]) => cellsOf(u).some(([ur, uc]) => Math.max(Math.abs(r - ur), Math.abs(cc - uc)) === 1)));
  if (at === 'front') spots = spots.filter(x => x.r === frontRow(p));
  if (at === 'back') spots = spots.filter(x => x.r !== frontRow(p));
  return spots[0] || null;
}
/** Move unit t to another lane (same cell if free, else the first free spot); the next lane that has room. */
function fxRelocate(s, t, why, lane) {
  const camp = t.owner, k = t.card, lanes = lane !== undefined ? [lane] : [1, 2].map(d => (t.lane + d) % 3);
  for (const l of lanes) {
    if (l === t.lane) continue;
    const same = fitsCells(s, camp, l, offsetsOf(t, t.o), t.r, t.c, t.id) ? { r: t.r, c: t.c, o: t.o } : null;
    const spot = same || freeSpots(s, camp, l, k)[0];
    if (!spot) continue;
    const from = t.lane;
    emit(s, { move: t.id, path: [[t.r, t.c], [spot.r, spot.c]], o: spot.o, toLane: l, steps: 3 });
    Object.assign(t, { lane: l, r: spot.r, c: spot.c, o: spot.o });
    applyAuras(s);
    log(s, `${unitName(t)} ${why} from lane ${from + 1} to lane ${l + 1}.`);
    fxArrived(s, t);
    return true;
  }
  return false;
}
/** Back in time: the board, the enemy's hand, deck, discard and supply as they were before its last action. */
function fxUndo(s, p) {
  const S = s.undoSnap && s.undoSnap[other(p)];
  if (!S || S.turn !== s.turn - 1) { log(s, 'Nothing to turn back.'); return; }
  const q = other(p), Q = s.players[q];
  s.units = JSON.parse(S.units); s.owner = S.owner.slice(); s.pool[q] = S.pool.slice();
  Object.assign(Q, JSON.parse(S.P)); s.players[p].discard = S.myDiscard.slice();
  s.tombs = [];
  emit(s, { rewind: true });
  log(s, `Time turns back: ${deckName(s, q)}'s last action is undone.`);
}
const FX_OPS = {
  dmg(s, c, o) { const n = fxAmount(s, c, o.dmg) + fxAugur(s, c); for (const t of fxSel(s, c, o.to)) dealDamage(s, c.u && !c.spell ? abilityHit(c.u, n) : n, t, c.label, fxAlive(s, c.u)); },
  strike(s, c, o) { const u = fxAlive(s, c.u); if (u) for (const t of fxSel(s, c, o.to || 'nearest')) if (byId(s, u.id)) strike(s, u, t, c.label); },
  chain(s, c, o) {
    let n = fxAmount(s, c, o.chain) + fxAugur(s, c), t = fxSel(s, c, o.to)[0];
    const hit = new Set();
    while (t && n > 0) {
      hit.add(t.id); const at = { ...t };
      dealDamage(s, n, t, c.label, fxAlive(s, c.u)); processDeaths(s); n--;
      t = s.units.filter(x => !hit.has(x.id) && x.lane === at.lane && x.owner === at.owner && ctl(x) === ctl(at) && edgeTouch(at, x)).sort(byReadingOrder)[0];
    }
  },
  ricochet(s, c, o) {
    const n = fxAmount(s, c, o.ricochet) + fxAugur(s, c), t = fxSel(s, c, o.to)[0];
    if (!t) return;
    const next = FX_SEL.inFrontOfIt(s, { ...c, t })[0];
    dealDamage(s, n, t, c.label, fxAlive(s, c.u)); processDeaths(s);
    if (next && byId(s, next.id)) dealDamage(s, o.then ?? n, next, c.label + ' (ricochet)', fxAlive(s, c.u));
  },
  buff(s, c, o) {
    const [a, d] = o.buff, x = o.per ? (typeof o.per === 'string' ? fxSel(s, c, o.per).length : fxAmount(s, c, o.per)) : 1;
    for (const t of fxSel(s, c, o.to)) {
      if (o.rnd) { t.ts = (t.ts || 0) + a * x; t.td = (t.td || 0) + d * x; } else { t.ps = (t.ps || 0) + a * x; t.pd = (t.pd || 0) + d * x; }
      if (a || d) log(s, `${unitName(t)} ${a * x >= 0 ? '+' : ''}${a * x}|${d * x >= 0 ? '+' : ''}${d * x}${o.rnd ? ' this round' : ''} (${c.label}).`);
    }
    emit(s, { grow: fxSel(s, c, o.to).map(t => t.id) });
  },
  heal(s, c, o) { for (const t of fxSel(s, c, o.to)) restoreShields(s, t, fxAmount(s, c, o.heal), c.label); },
  draw(s, c, o) { drawFor(s, c.p, fxAmount(s, c, o.draw), c.label); },
  carry(s, c, o) { const P = s.players[c.p]; P.reserve = Math.min(MAX_CARRY, P.reserve + fxAmount(s, c, o.carry)); log(s, `${c.label}: carry-over ${P.reserve}.`); },
  pool(s, c, o) { const l = o.lane === 'it' && c.t ? c.t.lane : c.lane; s.pool[c.p][l] += fxAmount(s, c, o.pool); log(s, `${c.label}: +${fxAmount(s, c, o.pool)} supply in lane ${l + 1} this round.`); },
  token(s, c, o) {
    const n = fxAmount(s, c, o.n ?? 1), lanes = o.lanes === 'all' ? LANES : o.lanes === 'other' ? LANES.filter(l => l !== c.lane) : [c.lane];
    for (const l of lanes) for (let i = 0; i < n; i++) {
      const spot = fxSpot(s, c.p, l, o.token, o.at, l === c.lane ? fxAlive(s, c.u) || c.u : null);
      if (spot) spawn(s, c.p, o.token, l, spot.r, spot.c, spot.o);
    }
  },
  kw(s, c, o) { for (const t of fxSel(s, c, o.to)) { if (o.kw === 'armoured' && o.rnd) t.tArm = true; else giveKw(t, o.kw); log(s, `${unitName(t)} gains ${KW_NAME[o.kw] || o.kw} (${c.label}).`); } },
  kill(s, c, o) { for (const t of fxSel(s, c, o.to)) kill(s, t, c.label); },
  push(s, c, o) { for (const t of fxSel(s, c, o.to)) if (!kw(t, 'fixed')) slide(s, t, -fwd(t.owner), o.push || 1); },
  pull(s, c, o) { for (const t of fxSel(s, c, o.to)) if (!kw(t, 'fixed')) slide(s, t, fwd(t.owner)); },
  displace(s, c, o) { for (const t of fxSel(s, c, o.to)) if (!kw(t, 'fixed')) fxRelocate(s, t, 'is sent away'); },
  ride(s, c, o) { for (const t of fxSel(s, c, o.to || 'self')) if (!kw(t, 'fixed')) fxRelocate(s, t, 'rides'); },
  stun(s, c, o) { for (const t of fxSel(s, c, o.to)) { Object.assign(t, { attacked: true, moved: true, mv: 9, atk: 9 }); log(s, `${unitName(t)} can't act this round (${c.label}).`); } },
  card(s, c, o) {
    const P = s.players[c.p];
    for (let i = 0; i < fxAmount(s, c, o.n ?? 1); i++) {
      if (o.to === 'deck') { P.draw.splice(Math.floor(Math.random() * (P.draw.length + 1)), 0, o.card); log(s, `${c.label}: ${CARDS[o.card].name} is shuffled into the deck.`); }
      else if (P.hand.length < HAND_LIMIT) { P.hand.push(o.card); emit(s, { handIn: c.p, k: o.card, from: 'deck' }); log(s, `${c.label}: ${CARDS[o.card].name} into the hand.`); }
    }
  },
  copy(s, c, o) {
    const P = s.players[c.p];
    for (const t of fxSel(s, c, o.to)) if (P.hand.length < HAND_LIMIT && !cardOf(t).token) { const k = baseKey(t.card); P.hand.push(k); emit(s, { handIn: c.p, k, from: 'deck' }); log(s, `${c.label}: a copy of ${CARDS[k].name} into the hand.`); }
  },
  echo(s, c, o) {
    for (const t of fxSel(s, c, o.to)) {
      if (t.tok) continue;   // echoes do not echo again
      const k = baseKey(t.card), spot = fxSpot(s, ctl(t), t.lane, k, 'adj', t);
      if (spot) spawn(s, ctl(t), k, t.lane, spot.r, spot.c, spot.o, `An echo of ${unitName(t)} appears.`, { tok: 1, kw: { fade: 1 } });
    }
  },
  again(s, c, o) { const P = s.players[c.p], k = P.lastSp; if (k && P.hand.length < HAND_LIMIT && !CARDS[k].noAgain) { P.hand.push(k); emit(s, { handIn: c.p, k, from: 'discard' }); log(s, `${c.label}: ${CARDS[k].name} again into the hand.`); } },
  replace(s, c, o) { for (const t of fxSel(s, c, o.to)) fxFire(s, 'place', t, { again: true }); },
  undo(s, c) { fxUndo(s, c.p); },
};
const FX_TO_OPS = new Set(['kill', 'stun', 'pull', 'push', 'ride', 'displace', 'replace', 'copy', 'echo', 'tick', 'ready', 'advance', 'omen']);
/** Run a list of ops with context c. */
function fxRun(s, c, ops) {
  for (const o of ops) {
    if (o.if && !fxIf(s, c, o.if)) continue;
    const op = Object.keys(FX_OPS).find(k => k in o);
    // { kill: 'it' }, { tick: 'ahead' }...: a selector written as the op's value is its target
    const oo = op && o.to === undefined && typeof o[op] === 'string' && FX_TO_OPS.has(op) ? { ...o, to: o[op] } : o;
    if (op) { FX_OPS[op](s, c, oo); processDeaths(s); }
  }
}
/** Fire the `on` effects of unit u (alive, or a dead copy for death). ev: the other unit of the event. */
function fxFire(s, on, u, extra = {}) {
  const card = cardOf(u);
  if (!card || !card.fx) return;
  card.fx.forEach((f, i) => {
    if (f.on !== on) return;
    if (extra.ev && f.of && !(cardOf(extra.ev)[f.of] || (extra.ev.kw && extra.ev.kw[f.of]))) return;
    if (extra.k && f.of && !(CARDS[extra.k] || {})[f.of]) return;
    if (u.tok && f.do.some(o => 'echo' in o)) return;
    if (extra.again && f.do.some(o => 'replace' in o || 'again' in o || 'tick' in o)) return;   // a replay never replays again
    const c = { p: ctl(u), u, t: extra.ev || null, lane: u.lane, label: unitName(u), k: extra.k };
    if (!fxIf(s, c, f.if)) return;
    if (f.lim === FX_ONCE) { u.fxl = u.fxl || {}; if (u.fxl[i] === s.round) return; u.fxl[i] = s.round; }
    fxRun(s, c, f.do);
  });
}
const fxWatchers = (s, p, lane, skip) => s.units.filter(x => ctl(x) === p && (lane === null || x.lane === lane) && x.id !== skip && cardOf(x).fx).sort(byReadingOrder);
function fxPlaced(s, p, u) {
  if (!byId(s, u.id)) return;
  fxFire(s, 'place', u);
  for (const w of fxWatchers(s, p, u.lane, u.id)) if (byId(s, w.id)) fxFire(s, 'allyPlace', w, { ev: u });
  for (const w of fxWatchers(s, other(p), u.lane, u.id)) if (byId(s, w.id) && byId(s, u.id)) fxFire(s, 'enemyPlace', w, { ev: u });
}
function fxDied(s, u) {
  fxFire(s, 'death', u);
  for (const w of fxWatchers(s, ctl(u), u.lane, u.id)) if (byId(s, w.id)) fxFire(s, 'allyDeath', w, { ev: u });
  for (const w of fxWatchers(s, other(ctl(u)), u.lane, u.id)) if (byId(s, w.id)) fxFire(s, 'enemyDeath', w, { ev: u });
}
function fxArrived(s, u) {
  if (!byId(s, u.id)) return;
  fxFire(s, 'arrive', u);
  for (const w of fxWatchers(s, ctl(u), u.lane, u.id)) if (byId(s, w.id)) fxFire(s, 'allyArrive', w, { ev: u });
  processDeaths(s);
}
function fxSpellCast(s, p, k) {
  const P = s.players[p];
  if (P.spR !== s.round) { P.spR = s.round; P.spN = 0; }
  P.spN++; P.lastSp = k;
  for (const w of fxWatchers(s, p, null)) if (byId(s, w.id)) fxFire(s, 'spell', w, { k });
}
function fxEach(s, on, p) { for (const w of fxWatchers(s, p, null)) if (byId(s, w.id)) { fxFire(s, on, w); processDeaths(s); } }
/** Position bonuses from card.aura, recomputed with the other auras. */
function fxAuras(s) {
  for (const u of s.units) u.ent = 0;
  for (const u of s.units) {
    const A = cardOf(u).aura;
    if (!A) continue;
    for (const a of A) {
      const c = { p: ctl(u), u, lane: u.lane };
      if (!fxIf(s, c, a.if)) continue;
      const x = a.per ? fxAmount(s, c, a.per) : 1;
      for (const t of fxSel(s, c, a.to || 'self')) { t.bs += (a.s || 0) * x; t.bd += (a.d || 0) * x; if (a.arm) t.ent = 1; }
    }
  }
}
/** Generic spells: their legal targets (cast.need: 'allies' | 'enemies' | 'units' must be in the lane). */
function fxSpellOptions(s, p, k, ok) {
  const card = CARDS[k], need = card.cast.need, enemies = s.units.filter(u => ctl(u) !== p), own = s.units.filter(u => ctl(u) === p);
  const has = lane => !need || (need === 'allies' ? unitsIn(s, p, lane).length : need === 'enemies' ? unitsIn(s, other(p), lane).length : s.units.some(u => u.lane === lane));
  if (card.cast.undo && !(s.undoSnap && s.undoSnap[other(p)] && s.undoSnap[other(p)].turn === s.turn - 1)) return;
  if (card.tactic === 'lane') LANES.forEach(lane => { if (has(lane)) ok({ lane }, lane); });
  else if (card.tactic === 'enemy') enemies.forEach(t => ok({ tid: t.id }, t.lane));
  else if (card.tactic === 'own') own.forEach(t => ok({ vid: t.id }, t.lane));
  else if (card.tactic === 'any') s.units.forEach(t => ok({ tid: t.id }, t.lane));
  else if (card.tactic === 'column') LANES.forEach(lane => [0, 1, 2].forEach(col => { if (unitsIn(s, other(p), lane).some(u => colsOf(u).includes(col))) ok({ lane, col }, lane); }));
}
function fxCast(s, p, a, lane, k) {
  const card = CARDS[k], t = byId(s, a.tid ?? a.vid);
  fxRun(s, { p, u: null, t, lane, col: a.col, label: card.name, spell: true, all: !!card.cast.all }, card.cast.do);
  if (t && ctl(t) === p && byId(s, t.id)) { fxFire(s, 'targeted', t, { k }); processDeaths(s); }
}
const FX_UNDO_KEYS = new Set(Object.keys(CARDS).filter(k => CARDS[k].cast && CARDS[k].cast.undo));
/** Kept before each action when the other side holds a card that can undo it. */
function fxKeepUndo(s, p) {
  if (!FX_UNDO_KEYS.size) return;
  s.undoSnap = s.undoSnap || {};
  if (!s.players[other(p)].hand.some(k => FX_UNDO_KEYS.has(k))) { delete s.undoSnap[p]; return; }
  const P = s.players[p];
  s.undoSnap[p] = { p, turn: s.turn, units: JSON.stringify(s.units), owner: s.owner.slice(), pool: s.pool[p].slice(),
    P: JSON.stringify({ hand: P.hand, draw: P.draw, discard: P.discard, reserve: P.reserve }), myDiscard: s.players[other(p)].discard.slice() };
}

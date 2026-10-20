/* ---------- Exanimati: death, plague and the discard pile ---------- */
const isUnitCard = k => !CARDS[k].tactic;
/** Cards that go to the discard pile when they die: deck cards (tokens vanish). */
const keepsCard = k => !CARDS[k].token;
/** How many of p's units died this round (Bone Harvest). */
const diedThisRound = (s, p) => (s.players[p].deathsR === s.round ? s.players[p].deaths : 0);
/** Debt of the Fallen's cost now: 1 less for each of p's units that died this round, never below 0. */
const debtCost = (s, p) => Math.max(0, CARDS.debt.cost - diedThisRound(s, p));
/** Danse Macabre: p's units that died this round and can rise in their own cells now (card in the discard pile, cells free), in resolution order. */
function fallenToRise(s, p) {
  const D = s.players[p].discard.slice(), out = [];
  for (const x of (s.players[p].fell || []).filter(x => x.round === s.round).map(x => ({ ...x, owner: x.camp })).sort(bySeat(p))) {
    const i = D.lastIndexOf(x.card), offs = x.sh || shapeCells(CARDS[x.card].size, x.o);
    if (i < 0 || !canRise(x.card) || !fitsCells(s, x.camp, x.lane, offs, x.r, x.c)) continue;
    if (out.some(y => y.lane === x.lane && y.camp === x.camp && cellsAt(y.sh || CARDS[y.card].size, y.r, y.c, y.sh ? 0 : y.o).some(([r, c]) => offs.some(([dr, dc]) => r === x.r + dr && c === x.c + dc)))) continue;
    D.splice(i, 1); out.push(x);
  }
  return out;
}
const unitsInDiscard = (s, p) => s.players[p].discard.filter(isUnitCard).length;
/** Carry-over Ossuary Tithe gives p now: units in its discard pile, up to 3, within the carry-over cap. */
const titheGain = (s, p) => Math.max(0, Math.min(3, unitsInDiscard(s, p), MAX_CARRY - s.players[p].reserve));
/** Aurelius: every card it needs lies in p's discard pile. */
const needsMet = (s, p, k) => !CARDS[k].needs || CARDS[k].needs.every(n => s.players[p].discard.includes(n));
/** Index of the top unit card in a discard pile (-1 if none). */
function topUnitIndex(list, skipLast = false) {
  for (let i = list.length - 1 - (skipLast ? 1 : 0); i >= 0; i--) if (isUnitCard(list[i])) return i;
  return -1;
}
/** Free spots for card k in p's camp of `lane`: front row first, then reading order from p's side. */
function freeSpots(s, p, lane, k) {
  const rows = p === 0 ? [0, 1, 2] : [2, 1, 0], cols = p === 0 ? [0, 1, 2] : [2, 1, 0], out = [];
  for (const r of rows) for (const c of cols) for (const o of orientations(CARDS[k].size))
    if (fitsCells(s, p, lane, shapeCells(CARDS[k].size, o), r, c)) out.push({ r, c, o });
  return out;
}
function catchPlague(s, u, why) {
  if (!u || !byId(s, u.id) || kw(u, 'plague')) return;
  giveKw(u, 'plague');
  log(s, `${unitName(u)} catches Plague${why ? ' from ' + why : ''}.`);
  applyAuras(s);
}
/** Unit u drains n from the enemy facing it: hits it for n and restores up to n of its own lost shields. */
function drain(s, u, n) {
  const t = targetsOf(s, u, cardOf(u).strix ? 'strix' : 'eotDrain')[0];
  if (!t) return;
  s.drainFx = true;
  try { dealDamage(s, abilityHit(u, n), t, unitName(u) + ' (drain)', u); } finally { s.drainFx = false; }
  if (!byId(s, u.id)) return;
  u.dmg = (u.dmg || 0) - n;   // restores n shields, even above its card's defence
  log(s, `${unitName(u)} drains ${n} shield${n > 1 ? 's' : ''}.`);
  emit(s, { heal: u.id, n });
}
function drawFor(s, p, n, source) {
  const got = drawCards(s, p, n);
  if (got) { log(s, `${source}: ${deckName(s, p)} draws ${got}.`); emit(s, { draw: p, n: got }); }
}
/** A new unit of card k for p in `lane` at (r, c, o); it is placed (Place effects fire). extra: own fields (sh, pS, pD, sup, kw). */
function spawn(s, p, k, lane, r, c, o, line, extra = {}) {
  const u = { id: s.nid++, card: k, owner: p, lane, r, c, o, ps: 0, pd: 0, dmg: 0, mv: 0, born: s.round, ...extra };
  s.units.push(u);
  placeUnit(s, p, u, line || `${unitName(u)} appears for ${deckName(s, p)} in lane ${lane + 1}.`);
  return u;
}
/** Whether card k can be resurrected: its defence must not halve to 0. */
const canRise = k => Math.floor(CARDS[k].def / 2) >= 1;
/** Fields that put a unit controlled by p into camp `camp` (the enemy camp, for units p controls there). */
const campOf = (p, camp) => (camp === undefined || camp === p ? {} : { owner: camp, ctl: p });
/**
 * Resurrection: card k comes back for p, printed strength, defence and supply halved (rounded down, no minimum).
 * opt.full: at full printed stats (Katabasis); opt.camp: the camp it rises in (default p's); opt.sh: its own shape.
 */
function resurrect(s, p, k, lane, spot, opt = {}) {
  const c = CARDS[k], half = x => Math.floor(x / 2), camp = opt.camp ?? p;
  if (!opt.full && !canRise(k)) { log(s, `${c.name} stays dead.`); return null; }
  const pos = spot || freeSpots(s, camp, lane, k)[0];
  if (!pos) { log(s, `${c.name} finds no room to rise.`); return null; }
  const stats = opt.full ? {} : { pS: half(c.str), pD: half(c.def), sup: half(c.sup) };
  const u = spawn(s, p, k, lane, pos.r, pos.c, pos.o, `${c.name} rises for ${deckName(s, p)} in lane ${lane + 1}.`, { ...stats, ...(opt.sh ? { sh: opt.sh } : {}), ...campOf(p, camp), rising: true });
  return u;
}
/** A Shade for p in the first free cell of its camp in `lane` (or in cell [r, c] if given and free); camp: the camp it appears in. */
function shadeAt(s, p, lane, cell, camp = p) {
  if (cell && !fits(s, camp, lane, 1, cell[0], cell[1], 'h')) cell = null;
  const pos = cell ? { r: cell[0], c: cell[1] } : freeSpots(s, camp, lane, 'shade')[0];
  if (!pos) return null;
  return spawn(s, p, 'shade', lane, pos.r, pos.c, 'h', `A Shade rises in lane ${lane + 1}.`, campOf(p, camp));
}
/** The nearest enemy in column col of the enemy camp facing u. */
function facingInCol(s, u, col) {
  const q = other(u.owner), map = occupancy(s, q, u.lane);
  const rows = [0, 1, 2].sort((a, b) => Math.abs(a - frontRow(q)) - Math.abs(b - frontRow(q)));
  for (const r of rows) { const t = map[r + ',' + col]; if (t && ctl(t) !== ctl(u)) return t; }
  return null;
}
/** The enemies facing u: the nearest one in each of its columns. */
const facingAll = (s, u) => [...new Set(colsOf(u).map(c => facingInCol(s, u, c)).filter(Boolean))];

/** Cells sharing an edge with mass u, free (want 'free') or holding an own ally (want 'ally'), in the spreading order. */
function spreadCells(s, u, want) {
  const own = new Set(cellsOf(u).map(x => x.join())), map = occupancy(s, u.owner, u.lane), seen = new Set(), list = [];
  for (const [r, c] of cellsOf(u)) for (const [dr, dc] of [[0, -1], [0, 1], [-1, 0], [1, 0]]) {
    const R = r + dr, C = c + dc, key = R + ',' + C;
    if (!inCamp(R, C) || own.has(key) || seen.has(key)) continue;
    seen.add(key);
    const x = map[key];
    if (want === 'free' ? !x : x && x.id !== u.id) list.push([R, C, x]);
  }
  // own row first (the mass's front-most row), then rows behind it, then rows in front; each row in reading order from the owner's side
  const front = Math.min(...cellsOf(u).map(([r]) => u.owner === 0 ? r : ROWS - 1 - r));
  const depth = r => (u.owner === 0 ? r : ROWS - 1 - r);
  const rank = r => (depth(r) >= front ? depth(r) - front : 10 + front - depth(r));
  const col = c => (u.owner === 0 ? c : COLS - 1 - c);
  return list.sort((a, b) => rank(a[0]) - rank(b[0]) || col(a[1]) - col(b[1]));
}
/** Add absolute cells to unit u's shape (it becomes a custom, amorphous shape). */
function growInto(u, cells) {
  if (!u.core) u.core = [u.r, u.c];   // the cell it first stood in (the Stitching Table's parts are counted around it)
  const all = [...cellsOf(u), ...cells];
  u.sh = normShape(all);
  u.o = 0;
  u.r = Math.min(...all.map(x => x[0]));
  u.c = Math.min(...all.map(x => x[1]));
}

/** The Stitching Table's four part cells: left, right (hands), behind (legs), in front (head). */
function tableParts(u) {
  const f = fwd(u.owner), [r, c] = u.core || [u.r, u.c];
  return { l: [r, c - 1], r: [r, c + 1], b: [r - f, c], h: [r + f, c] };
}
/** After a whole action (or the round end): each part cell where a unit died grows the Stitching Table into it, if the cell is still free; if another unit took the cell, that part is not built this time. */
function settleTables(s) {
  if (s.pending) return;
  for (const t of s.units.filter(u => cardOf(u).table && u.tp)) {
    const P = tableParts(t), map = occupancy(s, t.owner, t.lane), parts = { ...(t.parts || {}) };
    let n = 0;
    for (const k of t.tp) if (!parts[k] && inCamp(...P[k]) && !map[P[k].join()]) { parts[k] = true; growInto(t, [P[k]]); n++; }
    delete t.tp;
    if (n) { t.parts = parts; t.pd = (t.pd || 0) + n; emit(s, { merge: t.id }); log(s, `The Stitching Table grows ${n === 1 ? 'a part' : n + ' parts'}: +${n} defence.`); }
  }
  checkGorvan(s);
}
/** Gorvan rises once all four parts are done: lying across the table's row, from hand to hand. */
function checkGorvan(s) {
  for (const t of s.units.filter(u => cardOf(u).table)) {
    const parts = t.parts || {}, P = tableParts(t);
    if (!['l', 'r', 'b', 'h'].every(k => parts[k])) continue;
    s.units = s.units.filter(x => x.id !== t.id);
    log(s, 'The Stitching Table is empty: Gorvan, the Masterwork of Doctor Vessane, rises.');
    spawn(s, t.owner, 'gorvan', t.lane, P.l[0], P.l[1], 'h', `Gorvan rises in lane ${t.lane + 1}.`);
  }
}

/** What happens when unit u (already removed) dies: Exanimati death effects, returns and things that appear in its cells. */
function exDeath(s, u) {
  const c = cardOf(u), p = ctl(u), q = other(p), P = s.players[p], lane = u.lane, camp = u.owner, here = campOf(p, camp);
  P.died = s.round;
  if (kw(u, 'plague')) {
    // adjacent units of either side, in the camp it died in
    for (const a of s.units.filter(a => a.owner === camp && a.lane === lane && cellsOf(a).some(([r, c]) => cellsOf(u).some(([ur, uc]) => Math.abs(r - ur) <= 1 && Math.abs(c - uc) <= 1))))
      catchPlague(s, a, unitName(u));
  }
  for (const t of c.deathPlague ? targetsOf(s, u, 'deathPlague') : []) catchPlague(s, t, unitName(u));
  if (P.breath && P.breath[lane] === s.round) {
    const t = facingTarget(s, u);
    if (t) { dealDamage(s, 2, t, unitName(u) + ' (last breath)', null); processDeaths(s); }
  }
  P.deaths = P.deathsR === s.round ? (P.deaths || 0) + 1 : 1;
  P.deathsR = s.round;
  if (kw(u, 'afterlife')) for (let i = 0; i < kw(u, 'afterlife'); i++) if (!shadeAt(s, p, lane)) break;
  // the Stitching Table: deaths in its part cells
  const dead = cellsOf(u).map(x => x.join());
  for (const t of s.units.filter(x => cardOf(x).table && x.owner === camp && x.lane === lane))
    for (const [k, cell] of Object.entries(tableParts(t))) if (!(t.parts || {})[k] && dead.includes(cell.join())) t.tp = [...new Set([...(t.tp || []), k])];
  // things that come back or appear in its cells, in order (each only if the cells are free)
  const free = () => fitsCells(s, camp, lane, offsetsOf(u, u.o), u.r, u.c);
  if (!u.taken && kw(u, 'revenant')) {
    // the resurrection rule: printed stats and supply halved (rounded down), until its defence would halve to 0
    // Banner of the Returned: strength isn't halved
    const banner = unitsIn(s, p, lane).some(b => cardOf(b).bannerRev), half = x => Math.floor(x / 2);
    const pS = banner ? printedStr(u) : half(printedStr(u)), pD = half(printedDef(u)), sup = half(unitSupply(u));
    // a dead unit's card goes back only once per death: Revenant needs its card still in the discard pile (tokens have none)
    const D = s.players[p].discard, i = D.lastIndexOf(baseKey(u.card)), hasCard = i >= 0 || !!CARDS[baseKey(u.card)].token;
    if (pD >= 1 && free() && hasCard) {
      if (i >= 0) D.splice(i, 1);
      const back = { id: s.nid++, card: u.card, owner: camp, lane, r: u.r, c: u.c, o: u.o, sh: u.sh, ps: u.ps || 0, pd: u.pd || 0, dmg: 0, mv: u.mv, attacked: u.attacked, born: u.born,
        pS, pD, sup, kw: u.kw, off: u.off, ...here };
      s.units.push(back);
      // Place fires on every placement; its own return effect fires with it, before the enemy reacts
      const onReturn = c.onReturn === 'mardoc' ? () => { const amt = abilityHit(back, 2); for (const e of enemyOrder(s, p, lane, true)) if (byId(s, back.id)) dealDamage(s, amt, e, unitName(back) + ' (return)', back); }
        : c.onReturn === 'bride' ? () => { for (const e of facingAll(s, back)) { e.ts = (e.ts || 0) - 2; log(s, `${unitName(back)} wails at ${unitName(e)}: -2 strength until round end.`); } applyAuras(s); } : null;
      back.rising = true;   // Tomb Warden's gain comes the moment it is back
      placeUnit(s, p, back, `${unitName(back)} returns as ${pS}|${pD}${banner ? ' (the Banner keeps its strength)' : ''}.`, onReturn);
    } else if (pD < 1) log(s, `${unitName(u)} stays dead.`);
  }
  if (!u.taken && c.husk && free()) spawn(s, p, 'abom', lane, u.r, u.c, 'h', `An Abomination crawls out of ${unitName(u)}.`, here);
  if (!u.taken && c.sarc && free()) spawn(s, p, 'doux', lane, u.r, u.c, 'h', `The Sarcophagus opens: Doux steps out.`, here);
  if (!u.taken && s.players[p].veil === s.round) shadeAt(s, p, lane, cellsOf(u)[0], camp);
  // Corpse Candle, Midnight Procession: Shades in its cells
  if (!u.taken && (c.deathShade || c.deathShadeAll))
    for (const cl of c.deathShadeAll ? cellsOf(u) : [cellsOf(u)[0]]) if (fits(s, camp, lane, 1, cl[0], cl[1], 'h')) shadeAt(s, p, lane, cl, camp);
  // its own camp reacts, in reading order
  s.fxFrom = undefined;   // reactions come from the units that react
  // each reaction is an effect of its own: the chains of the units it hits close before the next reaction
  for (const b of s.units.filter(b => ctl(b) === p && b.lane === lane && cardOf(b).frenzy && inFront(b)).sort(byReadingOrder))
    if (byId(s, b.id) && inFront(b)) { strikeTargetsOf(s, b, 'frenzy', strengthOf(b), unitName(b) + ' (frenzy)'); processDeaths(s); }
  for (const v of unitsIn(s, p, lane).sort(byReadingOrder)) {
    const vc = cardOf(v);
    if (!byId(s, v.id)) continue;
    if (vc.strix) { drain(s, v, 1); processDeaths(s); }
    if (vc.nun && adjacent(v, u) && v.nunR !== s.round) { v.nunR = s.round; drawFor(s, p, 1, unitName(v)); }
    if (vc.mournSap && byId(s, v.id)) { const t = targetsOf(s, v, 'mournSap')[0]; if (t) { t.ps = (t.ps || 0) - 1; log(s, `${unitName(v)} mourns: ${unitName(t)} -1 strength.`); } }
    if (vc.reaper && byId(s, v.id)) { damageTargets(s, v, 'reaper', abilityHit(v, 1), unitName(v)); processDeaths(s); }
  }
  // then the enemy reacts
  if (kw(u, 'plague')) for (const o of unitsIn(s, q, lane)) if (cardOf(o).ophra) drawFor(s, q, 1, unitName(o));
  applyAuras(s);
}
/**
 * Gains are instant, actions take turns (AGREED, 10 Oct 2026): the units that only gain from a death (stats, supply, cells)
 * gain at the moment it is resolved, before the dead unit's own Death effects and before any reaction that acts on other units.
 */
function deathGains(s, u) {
  const c = cardOf(u), p = ctl(u), lane = u.lane;
  for (const side of [p, other(p)]) for (const v of s.units.filter(v => ctl(v) === side && v.lane === lane).sort(byReadingOrder)) {
    const vc = cardOf(v);
    if (vc.carrion) { v.ps = (v.ps || 0) + 1; log(s, `${unitName(v)} grows: +1 strength.`); }
    if (side !== p) continue;
    if (vc.mourn) { v.ps = (v.ps || 0) + 1; log(s, `${unitName(v)} mourns: +1 strength.`); }
    if (vc.grafter && adjacent(v, u) && c.str > 0) { v.ps = (v.ps || 0) + c.str; log(s, `${unitName(v)} grafts: +${c.str} strength.`); }
    if (vc.bellringer) { s.pool[p][lane]++; s.poolStart[p][lane]++; log(s, `${unitName(v)} tolls: +1 supply in lane ${lane + 1}.`); }
  }
  applyAuras(s);
}
/** Tomb Warden: one of p's units returned or was resurrected in its lane. */
function risen(s, p, u) {
  if (!u || !byId(s, u.id)) return;
  for (const w of unitsIn(s, p, u.lane)) if (w.id !== u.id && cardOf(w).warden) { u.ps = (u.ps || 0) + 1; u.pd = (u.pd || 0) + 1; log(s, `${unitName(w)} honours ${unitName(u)}: +1|+1.`); }
  applyAuras(s);
}

/** Exanimati Place effects that need no choice (card text first, then keywords). */
function exPlace(s, p, u) {
  const c = cardOf(u);
  if (u.born === undefined) u.born = s.round;
  if (c.onPlace === 'acolyte') for (const t of targetsOf(s, u, 'place:acolyte')) catchPlague(s, t, unitName(u));
  if (c.onPlace === 'weaver') { for (const a of targetsOf(s, u, 'place:weaver')) a.tInc = true; log(s, `Mist rolls over lane ${u.lane + 1}: your units there are Incorporeal until round end.`); }
  if (c.placeDraw) drawFor(s, p, c.placeDraw, unitName(u));
  applyAuras(s);
}
/** Place choices of the Exanimati. Choices are only offered on the owner's own turn; otherwise the automatic part happens. */
function exStartOnPlace(s, p, u) {
  const c = cardOf(u), k = c.onPlace, lane = u.lane, choose = !s.inEnd && s.cur === p && !s.pending;
  const own = s.units.filter(x => ctl(x) === p);
  if (k === 'robber') {
    const D = s.players[other(p)].discard, i = topUnitIndex(D);
    if (i < 0) return;
    const card = D[i];
    if (!canRise(card)) { log(s, `${CARDS[card].name} is too far gone to rise.`); return; }
    if (!freeSpots(s, p, lane, card).length) { log(s, `${unitName(u)} finds no room for ${CARDS[card].name}.`); return; }
    D.splice(i, 1);
    log(s, `${unitName(u)} digs up ${CARDS[card].name}.`);
    if (choose) s.pending = { k: 'place', p, lane, card, src: u.id };
    else resurrect(s, p, card, lane);
  } else if (k === 'aurelius') {
    // up to 2 picks among the top 4 units of the discard pile (fixed when it is placed)
    const D = s.players[p].discard, pool = [];
    for (let i = D.length - 1; i >= 0 && pool.length < 4; i--) if (isUnitCard(D[i])) pool.push(D[i]);
    if (choose && graveOptions(s, p, 'rez', pool).length) s.pending = { k: 'grave', p, lane, mode: 'rez', left: 2, src: u.id, pool };
  } else if (k === 'clerk') {
    if (choose && graveOptions(s, p, 'spell').length) s.pending = { k: 'grave', p, lane, mode: 'spell', left: 1, src: u.id };
  } else if (!choose) return;
  else if (k === 'surgeon') s.pending = { k: 'surgeon', p, lane, src: u.id };
  else if (k === 'embalm' && own.some(x => !kw(x, 'revenant'))) s.pending = { k: 'embalm', p, lane, src: u.id };
  else if (k === 'vessane' && own.some(x => movableKw(x).length) && own.length > 1) s.pending = { k: 'vsrc', p, lane, src: u.id };
}
const movableKw = u => KW_FLAGS.filter(f => kw(u, f));
/** Discard-pile choices: distinct card keys p may pick (mode 'rez' / 'hand': units; 'spell': spells costing 2 or less). */
function graveOptions(s, p, mode, pool) {
  const D = pool || s.players[p].discard, out = [];
  for (const k of D) {
    const c = CARDS[k];
    const ok = mode === 'spell' ? c.tactic && c.cost <= 2 : !c.tactic && !(mode === 'hand' && c.token) && !(mode === 'rez' && !canRise(k));
    if (ok && !out.includes(k)) out.push(k);
  }
  return out;
}


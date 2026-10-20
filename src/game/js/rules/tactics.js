/* ---------- tactics (spells) ---------- */
/** Supply a spell action costs (Bribe: the target's supply; Thousand Cuts: X, all the supply available). */
function spellCost(s, k, a) {
  if (k === 'bribe') { const t = byId(s, a.tid); return t ? unitSupply(t) : 0; }
  if (k === 'cuts') return a.n || 0;
  if (k === 'debt') return debtCost(s, s.cur);
  return CARDS[k].cost;
}
/** The lane a spell action works in. */
function spellLane(s, a) {
  if (a.lane !== undefined) return a.lane;
  const u = byId(s, a.vid !== undefined ? a.vid : a.tid);
  return u ? u.lane : 0;
}
/** Hits needed to bring u down with 1-hits (its defence, plus one for unused armour). */

/**
 * Every legal target of spell k for side p, as partial actions ({lane}, {lane, col}, {vid}, {tid}, {tid, n}).
 * forAi: skips options the computer never wants (Onslaught that moves nobody, Martyrdom with no target).
 */
/** Whether Onslaught in this lane would move at least one of p's units. */
function canAdvance(s, p, lane) {
  const t = cloneState(s);
  t.noFx = true;
  const before = unitsIn(t, p, lane).map(u => u.r + ',' + u.c).join();
  TACTICS.onslaught(t, p, { lane }, lane);
  return unitsIn(t, p, lane).map(u => u.r + ',' + u.c).join() !== before;
}
function spellOptions(s, p, k, forAi = true) {
  const out = [], enemies = s.units.filter(u => ctl(u) !== p), own = s.units.filter(u => ctl(u) === p);
  const ok = (a, lane) => canPay(s, lane, spellCost(s, k, a)) && out.push(a);
  switch (k) {
    case 'annona': LANES.forEach(lane => ok({ lane }, lane)); break;
    case 'reform': case 'hodegetria':
      LANES.forEach(lane => { if (unitsIn(s, p, lane).length) ok({ lane }, lane); }); break;
    case 'onslaught':
      LANES.forEach(lane => { if (unitsIn(s, p, lane).length && (!forAi || canAdvance(s, p, lane))) ok({ lane }, lane); }); break;
    case 'pyre': LANES.forEach(lane => { if (s.units.some(u => u.lane === lane)) ok({ lane }, lane); }); break;
    case 'levy': case 'burnbridges': LANES.forEach(lane => ok({ lane }, lane)); break;
    case 'strategikon': LANES.forEach(lane => { if (unitsIn(s, p, lane).length) ok({ lane }, lane); }); break;
    case 'stampede':
      LANES.forEach(lane => { if (unitsIn(s, p, lane).some(u => inFront(u) && strengthOf(u) > 0 && facingEnemies(s, u).length)) ok({ lane }, lane); }); break;
    case 'bloodtithe': own.forEach(u => ok({ vid: u.id }, u.lane)); break;
    case 'martyrdom': own.forEach(u => { if (!forAi || strikeTarget(s, u)) ok({ vid: u.id }, u.lane); }); break;
    case 'greekfire': case 'contagion':
      for (const lane of LANES) for (let col = 0; col < COLS; col++)
        if (unitsIn(s, other(p), lane).some(u => colsOf(u).includes(col))) ok({ lane, col }, lane);
      break;
    case 'monomachia': own.forEach(u => { if (strengthOf(u) > 0 && unitsIn(s, other(p), u.lane).length) ok({ vid: u.id }, u.lane); }); break;
    case 'synaspismos': own.forEach(u => { if (besideUnits(s, u).length) ok({ vid: u.id }, u.lane); }); break;
    case 'carrionfeast': own.forEach(u => ok({ vid: u.id }, u.lane)); break;
    case 'bribe': enemies.forEach(t => { if (spotsFor(s, p, t.lane, t).length) ok({ tid: t.id }, t.lane); }); break;
    case 'cull': enemies.forEach(t => { if (defenceOf(t) <= 2) ok({ tid: t.id }, t.lane); }); break;
    case 'firestorm': case 'execution': case 'hellfire': enemies.forEach(t => ok({ tid: t.id }, t.lane)); break;
    // ----- Exanimati -----
    case 'crown': case 'sceptre': case 'tithe': case 'veil': LANES.forEach(lane => ok({ lane }, lane)); break;
    case 'danse': if (fallenToRise(s, p).length) LANES.forEach(lane => ok({ lane }, lane)); break;
    case 'debt': enemies.forEach(t => ok({ tid: t.id }, t.lane)); break;
    case 'requiem': if (graveOptions(s, p, 'hand').length) LANES.forEach(lane => ok({ lane }, lane)); break;
    case 'raise': {
      const D = s.players[p].discard, i = topUnitIndex(D);
      if (i >= 0 && canRise(D[i])) LANES.forEach(lane => { if (freeSpots(s, p, lane, D[i]).length) ok({ lane }, lane); });
      break;
    }
    case 'night': if (unitsInDiscard(s, p)) LANES.forEach(lane => { if (freeSpots(s, p, lane, 'shade').length) ok({ lane }, lane); }); break;
    case 'barrowmist': LANES.forEach(lane => { if (unitsIn(s, p, lane).length) ok({ lane }, lane); }); break;
    case 'massgrave': LANES.forEach(lane => { if (unitsIn(s, p, lane).some(u => u.card === 'shade')) ok({ lane }, lane); }); break;
    case 'volley': if (s.players[p].discard.length >= 4) LANES.forEach(lane => { if (enemyOrder(s, p, lane, true).length) ok({ lane }, lane); }); break;
    case 'longnight': LANES.forEach(lane => { if (unitsIn(s, other(p), lane).length) ok({ lane }, lane); }); break;
    case 'lastrites': case 'stitches': own.forEach(u => ok({ vid: u.id }, u.lane)); break;
    case 'embalming': own.forEach(u => { if (!kw(u, 'revenant')) ok({ vid: u.id }, u.lane); }); break;
    case 'kiss': if (enemies.length) own.forEach(u => ok({ vid: u.id }, u.lane)); break;
    case 'rupture': own.forEach(u => { if (kw(u, 'plague')) ok({ vid: u.id }, u.lane); }); break;
    case 'forologia': LANES.forEach(lane => { if (unitsIn(s, p, lane).length) ok({ lane }, lane); }); break;
    case 'rainblood': LANES.forEach(lane => { if (s.units.some(u => u.lane === lane)) ok({ lane }, lane); }); break;
    case 'decapitate': s.units.forEach(t => { if (isBloodied(t)) ok({ tid: t.id }, t.lane); }); break;
    case 'bloodmoney': own.forEach(u => ok({ vid: u.id }, u.lane)); break;
    case 'gravetoll': own.forEach(u => { if (kw(u, 'fade')) ok({ vid: u.id }, u.lane); }); break;
    case 'boneharvest': if (diedThisRound(s, p)) LANES.forEach(lane => ok({ lane }, lane)); break;
    case 'lastbreath': LANES.forEach(lane => { if (unitsIn(s, p, lane).length) ok({ lane }, lane); }); break;
    case 'hymn': case 'ashen': case 'miasma': case 'creepingrot': enemies.forEach(t => ok({ tid: t.id }, t.lane)); break;
    case 'blade': case 'katabasis': s.units.forEach(t => ok({ tid: t.id }, t.lane)); break;
    case 'cuts':
      // spends all the supply in the target's lane and all carry-over: X = that total
      for (const t of s.units) { const n = s.pool[p][t.lane] + s.players[p].reserve; if (n >= 1) out.push({ tid: t.id, n }); }
      break;
  }
  return out;
}

/** Spells cast on a lane only to pay: no lane highlight while they resolve. */
const NO_LANE_FX = ['levy', 'crown', 'tithe', 'boneharvest', 'requiem', 'danse', 'veil'];
/**
 * Spell scopes: where each spell works (area) and the units it affects (pick), declared once; the spells below
 * resolve on these picks, and the screen highlights them. a: the spell action ({lane}, {lane, col}, {vid}, {tid}).
 */
const ownCampOf = (p, lane) => campCells(p, lane), foeCampOf = (p, lane) => campCells(other(p), lane);
/** p's units in `lane` standing in any of `rows`, except unit `except`. */
const rowMates = (s, p, lane, rows, except) => unitsIn(s, p, lane).filter(u => u.id !== except && cellsOf(u).some(([r]) => rows.includes(r)));
const rowCells = (u, rows) => campCells(u.owner, u.lane, r => rows.includes(r));
const SPELL_SCOPE = {
  annona: { area: (s, p, l) => ownCampOf(p, l) },
  sceptre: { area: (s, p, l) => ownCampOf(p, l) },
  forologia: { area: (s, p, l) => ownCampOf(p, l), pick: (s, p, l) => unitsIn(s, p, l) },
  reform: { area: (s, p, l) => ownCampOf(p, l), pick: (s, p, l) => unitsIn(s, p, l) },
  hodegetria: { area: (s, p, l) => ownCampOf(p, l), pick: (s, p, l) => unitsIn(s, p, l) },
  strategikon: { area: (s, p, l) => ownCampOf(p, l), pick: (s, p, l) => unitsIn(s, p, l) },
  barrowmist: { area: (s, p, l) => ownCampOf(p, l), pick: (s, p, l) => unitsIn(s, p, l) },
  lastbreath: { area: (s, p, l) => ownCampOf(p, l), pick: (s, p, l) => unitsIn(s, p, l) },
  onslaught: { area: (s, p, l) => ownCampOf(p, l), pick: (s, p, l) => unitsIn(s, p, l).sort(byReadingOrder) },
  burnbridges: { area: (s, p, l) => ownCampOf(p, l), pick: (s, p, l) => unitsIn(s, p, l).sort(byReadingOrder) },
  pyre: { area: (s, p, l) => [...ownCampOf(p, l), ...foeCampOf(p, l)], pick: (s, p, l) => s.units.filter(u => u.lane === l).sort(bySeat(p)) },
  rainblood: { area: (s, p, l) => [...ownCampOf(p, l), ...foeCampOf(p, l)], pick: (s, p, l) => s.units.filter(u => u.lane === l).sort(bySeat(p)) },
  longnight: { area: (s, p, l) => foeCampOf(p, l), pick: (s, p, l) => unitsIn(s, other(p), l) },
  volley: { area: (s, p, l) => campCells(other(p), l, r => r === frontRow(other(p))), pick: (s, p, l) => enemyOrder(s, p, l, true) },
  greekfire: { area: (s, p, l, a) => campCells(other(p), l, (r, c) => c === a.col),
    pick: (s, p, l, a) => unitsIn(s, other(p), l).filter(u => colsOf(u).includes(a.col)).sort(bySeat(p)) },
  stampede: { area: (s, p, l) => [...campCells(p, l, r => r === frontRow(p)), ...campCells(other(p), l, r => r === frontRow(other(p)))],
    pick: (s, p, l) => unitsIn(s, p, l).filter(u => inFront(u) && strengthOf(u) > 0).sort(byReadingOrder) },
  massgrave: { area: (s, p, l) => [...ownCampOf(p, l), ...foeCampOf(p, l)],
    pick: (s, p, l) => unitsIn(s, p, l).filter(u => u.card === 'shade').sort(byReadingOrder) },
  veil: { area: (s, p) => LANES.flatMap(l => ownCampOf(p, l)), pick: (s, p) => s.units.filter(u => ctl(u) === p) },
  danse: { area: (s, p) => fallenToRise(s, p).flatMap(x => cellsAt(x.sh || CARDS[x.card].size, x.r, x.c, x.sh ? 0 : x.o).map(([r, c]) => [x.camp, x.lane, r, c])), pick: () => [] },
  monomachia: { area: (s, p, l) => foeCampOf(p, l), pick: (s, p, l, a) => [byId(s, a.vid), ...unitsIn(s, other(p), l)] },
  synaspismos: { area: (s, p, l, a) => AREA.beside(s, byId(s, a.vid)), pick: (s, p, l, a) => [byId(s, a.vid), ...besideUnits(s, byId(s, a.vid))] },
  carrionfeast: { area: (s, p, l, a) => AREA.adjacent(s, byId(s, a.vid)), pick: (s, p, l, a) => adjacentAllies(s, byId(s, a.vid)) },
  martyrdom: { area: (s, p, l, a) => areaOf(s, byId(s, a.vid), 'martyr'), pick: (s, p, l, a) => [byId(s, a.vid), ...targetsOf(s, byId(s, a.vid), 'martyr')] },
  firestorm: { area: (s, p, l, a) => rowCells(byId(s, a.tid), rowsOf(byId(s, a.tid))),
    pick: (s, p, l, a) => { const t = byId(s, a.tid); return [t, ...unitsIn(s, t.owner, t.lane).filter(u => u.id !== t.id && cellsOf(u).some(([r]) => rowsOf(t).includes(r)))]; } },
  contagion: { area: (s, p, l, a) => campCells(other(p), l, (r, c) => c === a.col),
    pick: (s, p, l, a) => unitsIn(s, other(p), l).filter(u => colsOf(u).includes(a.col)).sort(bySeat(p)) },
  rupture: { area: (s, p, l) => foeCampOf(p, l), pick: (s, p, l) => unitsIn(s, other(p), l) },
  bribe: { area: (s, p, l) => ownCampOf(p, l), pick: (s, p, l, a) => one(byId(s, a.tid)) },
};
/** The units spell k (action a) affects, in order; by default the unit it targets. */
function spellTargets(s, p, k, a) {
  const l = spellLane(s, a), sc = SPELL_SCOPE[k];
  if (sc && sc.pick) return sc.pick(s, p, l, a).filter(Boolean);
  return [byId(s, a.tid ?? a.vid)].filter(Boolean);
}
const spellArea = (s, p, k, a) => (SPELL_SCOPE[k] && SPELL_SCOPE[k].area ? SPELL_SCOPE[k].area(s, p, spellLane(s, a), a) : []);
/** The first enemy in u's column(s) of the enemy camp that it can strike (front row first), or null. */
function facingStrikable(s, u) {
  const q = other(u.owner), map = occupancy(s, q, u.lane), cols = colsOf(u);
  const rows = [0, 1, 2].sort((a, b) => Math.abs(a - frontRow(q)) - Math.abs(b - frontRow(q)));
  for (const r of rows) for (const c of cols) { const t = map[r + ',' + c]; if (t && ctl(t) !== ctl(u) && !isIncorp(t)) return t; }
  return null;
}
/** A unit leaves the game without dying (no Death effects, no reactions, its card goes nowhere). */
function exitGame(s, u, why) {
  emit(s, { exit: u.id });
  s.units = s.units.filter(x => x.id !== u.id);
  log(s, `${unitName(u)} ${why} and leaves the game.`);
  applyAuras(s);
}
const TACTICS = {
  annona(s, p, a, lane) { s.pool[p][lane] += 3; s.poolStart[p][lane] += 3; log(s, `Grain reaches lane ${lane + 1}: +3 supply.`); },
  reform(s, p, a, lane) { s.pending = { k: 'free', p, lane, n: 2, ex: null }; },
  monomachia(s, p, a, lane) { s.pending = { k: 'duel', p, lane, vid: a.vid }; },
  synaspismos(s, p, a, lane) { s.pending = { k: 'pair', p, lane, vid: a.vid }; },
  hodegetria(s, p, a, lane) {
    for (const u of spellTargets(s, p, 'hodegetria', a)) { restoreShields(s, u, Infinity, 'Ipermachos Stratigos'); u.pd = (u.pd || 0) + 1; }
    log(s, `The icon blesses lane ${lane + 1}: +1 defence.`);
  },
  greekfire(s, p, a, lane) {
    for (const t of spellTargets(s, p, 'greekfire', a)) hitUnit(s, 2, t, 'Greek Fire', null);
  },
  bribe(s, p, a, lane) { s.pending = { k: 'place', p, lane, tid: a.tid }; },
  carrionfeast(s, p, a, lane) {
    const v = byId(s, a.vid), near = adjacentAllies(s, v).map(u => u.id);
    kill(s, v, 'Carrion Feast');
    processDeaths(s);
    for (const u of near.map(id => byId(s, id)).filter(Boolean)) {
      u.ps = (u.ps || 0) + 1; u.pd = (u.pd || 0) + 1;
      log(s, `${unitName(u)} feasts: +1 strength, +1 defence.`);
    }
  },
  onslaught(s, p, a) { for (const u of spellTargets(s, p, 'onslaught', a)) if (byId(s, u.id)) { slide(s, u, fwd(p)); processDeaths(s); } },
  cull(s, p, a) { kill(s, byId(s, a.tid), 'Cull'); },
  firestorm(s, p, a) {
    for (const v of spellTargets(s, p, 'firestorm', a)) hitUnit(s, 2, v, 'Firestorm', null);
  },
  pyre(s, p, a) { for (const u of spellTargets(s, p, 'pyre', a)) hitUnit(s, 1, u, 'Pyre', null); },
  cuts(s, p, a) { const t = byId(s, a.tid); for (let i = 0; i < a.n && byId(s, t.id); i++) hitUnit(s, 1, t, 'Thousand Cuts', null); },
  execution(s, p, a) { kill(s, byId(s, a.tid), 'Execution'); },
  hellfire(s, p, a) { hitUnit(s, 6, byId(s, a.tid), 'Hellfire', null); },
  levy(s, p) {
    const P = s.players[p];
    let n = 0;
    while (n < 2 && P.hand.length < HAND_LIMIT) { P.hand.push('stratiotes'); emit(s, { handIn: p, k: 'stratiotes', from: 'create' }); n++; }
    log(s, n ? `Levy: ${n} Stratiotes join the hand.` : 'Levy: the hand is full.');
  },
  strategikon(s, p, a, lane) { for (const u of spellTargets(s, p, 'strategikon', a)) u.tArm = true; log(s, `Lane ${lane + 1} closes ranks: Armoured until round end.`); },
  bloodtithe(s, p, a) {
    kill(s, byId(s, a.vid), 'Blood Tithe');
    processDeaths(s);
    const n = drawCards(s, p, 2);
    if (n) emit(s, { draw: p, n });
  },
  martyrdom(s, p, a) {
    // it strikes, the strike's deaths resolve, then it dies (and its Death effects resolve)
    const v = byId(s, a.vid);
    strikeTargetsOf(s, v, 'martyr', strengthOf(v) + 2, unitName(v) + ' (martyrdom)');
    processDeaths(s);
    if (byId(s, v.id)) kill(s, v, 'Martyrdom');
  },
  burnbridges(s, p, a, lane) {
    s.pool[p][lane] += 3; s.poolStart[p][lane] += 3;
    log(s, `The bridges burn in lane ${lane + 1}: +3 supply.`);
    for (const u of spellTargets(s, p, 'burnbridges', a)) {
      if (!byId(s, u.id)) continue;
      if (defenceOf(u) <= 1) kill(s, u, 'Burn the Bridges');
      else { u.dmg = (u.dmg || 0) + 1; log(s, `${unitName(u)} loses 1 shield.`); }
    }
  },
  // ----- Exanimati -----
  lastrites(s, p, a) {
    const v = byId(s, a.vid), cell = cellsOf(v)[0], lane = v.lane;
    kill(s, v, 'Last Rites');
    processDeaths(s);
    shadeAt(s, p, lane, cell);
  },
  crown(s, p) { drawFor(s, p, 1, 'Crown of Aurelius'); },
  miasma(s, p, a) { catchPlague(s, byId(s, a.tid), 'Miasma'); },
  gravetoll(s, p, a) { kill(s, byId(s, a.vid), 'Grave Toll'); processDeaths(s); drawFor(s, p, 2, 'Grave Toll'); },
  boneharvest(s, p) { drawFor(s, p, Math.min(3, diedThisRound(s, p)), 'Bone Harvest'); },
  lastbreath(s, p, a, lane) { const P = s.players[p]; P.breath = { ...(P.breath || {}), [lane]: s.round }; log(s, `Last Breath hangs over lane ${lane + 1}.`); },
  forologia(s, p, a, lane) {
    const P = s.players[p], before = P.reserve;
    P.reserve = Math.min(MAX_CARRY, P.reserve + spellTargets(s, p, 'forologia', a).length);
    log(s, `Forologia: +${P.reserve - before} carry-over.`);
  },
  bloodmoney(s, p, a) {
    const v = byId(s, a.vid), P = s.players[p], before = P.reserve, n = unitSupply(v);
    kill(s, v, 'Blood Money');
    processDeaths(s);
    P.reserve = Math.min(MAX_CARRY, P.reserve + n);
    log(s, `Blood Money: +${P.reserve - before} carry-over.`);
  },
  rainblood(s, p, a) { for (const u of spellTargets(s, p, 'rainblood', a)) hitUnit(s, 1, u, 'Rain of Blood', null); },
  decapitate(s, p, a) { kill(s, byId(s, a.tid), 'Decapitate'); },
  sceptre(s, p, a, lane) { s.pool[p][lane] += 1; s.poolStart[p][lane] += 1; log(s, `The Sceptre commands lane ${lane + 1}: +1 supply.`); },
  blade(s, p, a) { hitUnit(s, 2, byId(s, a.tid), 'Blade of Aurelius', null); },
  hymn(s, p, a) { const t = byId(s, a.tid); t.ts = (t.ts || 0) - 3; log(s, `${unitName(t)} withers: -3 strength until round end.`); },
  ashen(s, p, a) { const t = byId(s, a.tid); t.blight = true; log(s, `${unitName(t)} is Blighted.`); },
  stitches(s, p, a) { restoreShields(s, byId(s, a.vid), 3, 'Crude Stitches'); },
  barrowmist(s, p, a, lane) { for (const u of spellTargets(s, p, 'barrowmist', a)) u.tInc = true; log(s, `Barrow mist hides lane ${lane + 1}: your units there are Incorporeal until round end.`); },
  contagion(s, p, a) { for (const x of spellTargets(s, p, 'contagion', a)) catchPlague(s, x, 'Contagion'); },
  creepingrot(s, p, a) { const t = byId(s, a.tid); t.ps = (t.ps || 0) - 2; log(s, `${unitName(t)} rots: -2 strength.`); },
  embalming(s, p, a) { const v = byId(s, a.vid); giveKw(v, 'revenant'); log(s, `${unitName(v)} is embalmed: it gains Revenant.`); },
  kiss(s, p, a, lane) { s.pending = { k: 'kiss', p, lane, vid: a.vid }; },
  tithe(s, p) {
    const n = titheGain(s, p);
    s.players[p].reserve += n;
    log(s, `The ossuary pays its tithe: +${n} carry-over.`);
  },
  rupture(s, p, a) {
    kill(s, byId(s, a.vid), 'Rupture');
    processDeaths(s);
    for (const e of spellTargets(s, p, 'rupture', a)) catchPlague(s, e, 'Rupture');
  },
  requiem(s, p, a, lane) { s.pending = { k: 'grave', p, lane, mode: 'hand', left: 2 }; },
  massgrave(s, p, a, lane) {
    // AGREED 17:15: they fly together straight through the enemy camp. Column by column, in flying order, the fliers go at the
    // first enemy in their column, as many as it takes to kill it (by their fixed strength; an unused Armour costs one strike),
    // then the next ones go at the next enemy, and so on; those with no enemy left fly off the board and leave the game.
    // All the strikes land at the same moment, the strikers die with them, and then the chains resolve.
    const all = spellTargets(s, p, 'massgrave', a);
    if (!all.length) return;
    const q = other(p), rowOf = (u, r) => laneRow(u.owner, r), colOf = u => Math.min(...cellsOf(u).map(x => x[1]));
    const left = new Map(), armour = new Set(), plan = [];   // left: shields to break; armour: unused Armour still to break
    const cols = [0, 1, 2].sort((x, y) => (p === 0 ? x - y : y - x));
    for (const col of cols) {
      const fliers = all.filter(u => colOf(u) === col).sort((x, y) => Math.abs(rowOf(x, cellsOf(x)[0][0]) - 2.5) - Math.abs(rowOf(y, cellsOf(y)[0][0]) - 2.5));
      const foes = unitsIn(s, q, lane).filter(t => !isIncorp(t) && cellsOf(t).some(([, c]) => c === col))
        .sort((x, y) => Math.abs(Math.min(...cellsOf(x).filter(([, c]) => c === col).map(([r]) => r)) - frontRow(x.owner)) - Math.abs(Math.min(...cellsOf(y).filter(([, c]) => c === col).map(([r]) => r)) - frontRow(y.owner)));
      for (const t of foes) if (!left.has(t.id)) { left.set(t.id, defenceOf(t)); if (isArmoured(t) && !t.armUsed) armour.add(t.id); }
      for (const f of fliers) {
        const str = strengthOf(f), t = foes.find(x => left.get(x.id) > 0);
        const R0 = Math.min(...cellsOf(f).map(([r]) => rowOf(f, r)));
        if (!t) { plan.push({ f, t: null, str, end: f.owner === 0 ? R0 + 1 : 6 - R0 }); continue; }
        let kills = false;
        if (armour.has(t.id)) { if (str > 0) armour.delete(t.id); }
        else { left.set(t.id, left.get(t.id) - str); kills = left.get(t.id) <= 0; }
        const Rt = Math.min(...cellsOf(t).filter(([, c]) => c === col).map(([r]) => rowOf(t, r)));
        plan.push({ f, t, str, kills, end: Math.max(1, Math.abs(Rt - R0)) });
      }
    }
    emit(s, { flight: plan.map(x => ({ id: x.f.id, card: x.f.card, lane: x.f.lane, owner: x.f.owner, cells: cellsOf(x.f).map(c => [c[0], c[1]]), dir: x.f.owner === 0 ? -1 : 1, end: x.end, out: !x.t, grave: x.kills ? x.t.id : null })), ms: 230 });
    for (const x of plan) x.f.aloft = true;
    // all the strikes at once (in resolution order of their targets), the strikers die with them, then the chains
    s.fxHow = 'flight';
    try { for (const x of plan.filter(x => x.t).sort((m, n) => seatKey(m.t, p) - seatKey(n.t, p))) if (byId(s, x.t.id)) hitUnit(s, x.str, x.t, unitName(x.f) + ' (mass grave)', x.f.id, false, true); }
    finally { s.fxHow = undefined; }
    for (const x of plan) { if (!byId(s, x.f.id)) continue; if (x.t) kill(s, x.f, 'Mass Grave', { silent: true, noTomb: true }); else exitGame(s, x.f, 'flies off the board'); }
    processDeaths(s);
  },
  volley(s, p, a, lane) {
    const n = Math.min(4, Math.floor(s.players[p].discard.length / 4));
    for (const e of spellTargets(s, p, 'volley', a)) hitUnit(s, n, e, 'Ossuary Volley', null);
  },
  raise(s, p, a, lane) {
    const D = s.players[p].discard, i = topUnitIndex(D), k = D[i];
    D.splice(i, 1);
    s.pending = { k: 'place', p, lane, card: k };
  },
  danse(s, p) {
    // they rise one by one in resolution order, each in its own cells (halved, placed), taking its card from the discard pile
    for (const x of fallenToRise(s, p)) {
      const D = s.players[p].discard, i = D.lastIndexOf(x.card), offs = x.sh || shapeCells(CARDS[x.card].size, x.o);
      if (i < 0 || !fitsCells(s, x.camp, x.lane, offs, x.r, x.c)) continue;
      D.splice(i, 1);
      resurrect(s, p, x.card, x.lane, { r: x.r, c: x.c, o: x.sh ? 0 : x.o }, { camp: x.camp, sh: x.sh });
      processDeaths(s);
    }
  },
  debt(s, p, a) { kill(s, byId(s, a.tid), 'Debt of the Fallen'); },
  veil(s, p) { s.players[p].veil = s.round; log(s, 'The veil thins: your dead return as Shades this round.'); },
  night(s, p, a, lane) {
    const D = s.players[p].discard;
    let n = 0;
    while (unitsInDiscard(s, p) && freeSpots(s, p, lane, 'shade').length) {
      D.splice(topUnitIndex(D), 1);
      shadeAt(s, p, lane);
      n++;
    }
    log(s, `Night of Shades: ${n} Shade${n === 1 ? '' : 's'} rise in lane ${lane + 1}.`);
  },
  katabasis(s, p, a) {
    // it rises for p in its own cells, in whichever camp they are, at full printed stats
    const t = byId(s, a.tid), k = baseKey(t.card), lane = t.lane, camp = t.owner, from = ctl(t), sh = t.sh ? normShape(cellsOf(t)) : null;
    const spot = sh ? { r: t.r, c: t.c, o: 0 } : { r: t.r, c: t.c, o: t.o }, offs = sh ? sh : shapeCells(CARDS[k].size, spot.o);
    kill(s, t, 'Katabasis', { taken: true });
    processDeaths(s);
    const D = s.players[from].discard, i = D.lastIndexOf(k);
    if (i >= 0) D.splice(i, 1);
    resurrect(s, p, k, lane, fitsCells(s, camp, lane, offs, spot.r, spot.c) ? spot : null, { full: true, camp, sh });
  },
  longnight(s, p, a) { for (const e of spellTargets(s, p, 'longnight', a)) { e.ps = (e.ps || 0) - 2; log(s, `${unitName(e)} weakens in the long night: -2 strength.`); } },
  stampede(s, p, a, lane) {
    // all at once: each front-row unit strikes the enemy facing it, all strikes land together, then the chains resolve
    const shots = spellTargets(s, p, 'stampede', a).map(u => ({ u, t: facingEnemies(s, u)[0], str: strengthOf(u) })).filter(x => x.t)
      .sort((x, y) => seatKey(x.t, p) - seatKey(y.t, p));
    for (const { u, t, str } of shots) if (byId(s, u.id)) hitUnit(s, str, t, unitName(u) + ' (stampede)', u.id);
    processDeaths(s);
  },
};


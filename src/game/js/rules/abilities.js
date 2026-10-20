/* ---------- ability scopes ----------
   Each ability declares, once, its area (cells, for highlighting) and whom it affects (PICK, also used to resolve it).
   The rules call targetsOf() to find their targets; the screen calls the same functions to show them. */
/** Cells [owner, lane, r, c] of one camp that pass test(r, c). */
function campCells(owner, lane, test = () => true) {
  const out = [];
  for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) if (test(r, c)) out.push([owner, lane, r, c]);
  return out;
}
const touchesAdj = (u, r, c) => cellsOf(u).some(([ur, uc]) => Math.abs(r - ur) <= 1 && Math.abs(c - uc) <= 1);
/** Areas: where an ability works, as cells. */
const AREA = {
  column: (s, u) => campCells(other(u.owner), u.lane, (r, c) => colsOf(u).includes(c)),
  reach: (s, u) => [0, 1].flatMap(o => campCells(o, u.lane, (r, c) => reachesCell(u, o, r, c))),
  row: (s, u) => campCells(u.owner, u.lane, r => rowsOf(u).includes(r)),
  camp: (s, u) => campCells(u.owner, u.lane),
  enemyCamp: (s, u) => campCells(other(u.owner), u.lane),
  enemyFront: (s, u) => campCells(other(u.owner), u.lane, r => r === frontRow(other(u.owner))),
  facingFront: (s, u) => campCells(other(u.owner), u.lane, (r, c) => r === frontRow(other(u.owner)) && colsOf(u).includes(c)),
  frontIfFront: (s, u) => (inFront(u) ? AREA.enemyFront(s, u) : []),
  adjacent: (s, u) => campCells(u.owner, u.lane, (r, c) => touchesAdj(u, r, c)),
  beside: (s, u) => campCells(u.owner, u.lane, (r, c) => cellsOf(u).some(([ur, uc]) => ur === r && Math.abs(uc - c) === 1)),
  front: (s, u) => campCells(u.owner, u.lane, (r, c) => cellsOf(u).some(([ur, uc]) => uc === c && ur + fwd(u.owner) === r)),
  chargePath: (s, u) => campCells(u.owner, u.lane, (r, c) => colsOf(u).includes(c)),
  table: (s, u) => Object.entries(tableParts(u)).filter(([k, [r, c]]) => inCamp(r, c) && !(u.parts || {})[k]).map(([, [r, c]]) => [u.owner, u.lane, r, c]),
};
const one = t => (t ? [t] : []);
const alliesOf = (s, u) => unitsIn(s, ctl(u), u.lane).filter(a => a.id !== u.id);
/** Picks: the units an ability affects, in the order it affects them. */
const PICK = {
  facing: (s, u) => one(facingTarget(s, u)),
  facingAll: (s, u) => facingAll(s, u),
  strike: (s, u) => one(strikeTarget(s, u)),
  strikeAll: (s, u) => strikeTargets(s, u),
  enemyFront: (s, u) => enemyOrder(s, ctl(u), u.lane, true),
  enemies: (s, u) => enemyOrder(s, ctl(u), u.lane),
  plagued: (s, u) => unitsIn(s, other(ctl(u)), u.lane).filter(e => kw(e, 'plague')),
  allies: alliesOf,
  rowAllies: (s, u) => s.units.filter(a => sharesRow(u, a)),
  adjAllies: (s, u) => adjacentAllies(s, u),
  wallNeighbours: (s, u) => besideUnits(s, u).filter(a => cardOf(a).wall),
  frontAlly: (s, u) => { const map = occupancy(s, u.owner, u.lane), out = []; for (const [r, c] of frontCellsOf(u)) { const a = map[r + ',' + c]; if (a && ctl(a) === ctl(u) && !out.includes(a)) out.push(a); } return out; },
  shades: (s, u) => alliesOf(s, u).filter(a => a.card === 'shade'),
  immobile: (s, u) => alliesOf(s, u).filter(a => kw(a, 'fixed')),
  plagueAllies: (s, u) => unitsIn(s, ctl(u), u.lane).filter(a => kw(a, 'plague')).sort(byReadingOrder),
  /** Blood Sorcerer: the allies it damages, then the enemy (only if there is one). */
  /** Blood Sorcerer: just enough allies (reading order) to kill the first enemy in the lane, then that enemy. */
  sorcerer: (s, u) => {
    const foe = enemyOrder(s, ctl(u), u.lane)[0];
    if (!foe) return [];
    const need = Math.max(0, defenceOf(foe) + (isArmoured(foe) && !foe.armUsed ? 1 : 0) - abilityHit(u, 0));
    return [...alliesOf(s, u).filter(a => !isIncorp(a)).sort(byReadingOrder).slice(0, need), foe];
  },
  /** Powder Keg: units of its camp in its row, and the facing enemy front row if it stands in the front row. */
  keg: (s, u) => [...s.units.filter(v => v.owner === u.owner && v.lane === u.lane && v.id !== u.id && cellsOf(v).some(([r]) => rowsOf(u).includes(r))),
    ...(inFront(u) ? enemyOrder(s, ctl(u), u.lane, true) : [])],
  charge: (s, u) => (inFront(u) ? facingEnemies(s, u).filter(x => !isIncorp(x)).sort(bySeat(ctl(u))) : []),
  pullable: (s, u) => pullable(s, ctl(u), u.lane),
  defectors: (s, u) => defectors(s, ctl(u), u.lane),
  cinder: (s, u) => [...alliesOf(s, u), ...one(facingTarget(s, u))],
};
/**
 * Scope of each ability, keyed by its card flag ('place:' + kind for Place effects, 'charge' for a charge):
 * area names and a pick name. Abilities without a pick affect no unit directly (they only show where they work).
 */
const SCOPE = {
  wall: ['beside', 'wallNeighbours'], rowAura: ['row', 'rowAllies'], drumHit: ['row', 'rowAllies'],
  frontBuff: ['front', 'frontAlly'], adjAura: ['adjacent', 'adjAllies'], pack: ['adjacent', 'adjAllies'], skirm: ['adjacent'],
  guard: ['adjacent', 'adjAllies'], eotAdjHeal: ['adjacent', 'adjAllies'], deathAdjHeal: ['adjacent', 'adjAllies'],
  nun: ['adjacent', 'adjAllies'], grafter: ['adjacent', 'adjAllies'], eotSaint: ['adjacent', 'adjAllies'],
  eotLaneHealAll: ['camp', 'allies'], veteran: ['camp', 'allies'], herald: ['camp'], warhorn: ['camp'], hitsOwn: ['camp'], tourm: ['camp', 'allies'],
  carrion: ['camp+enemyCamp'], mourn: ['camp'], bellringer: ['camp'], warden: ['camp'],
  shadeAura: ['camp', 'shades'], overseer: ['camp', 'immobile'],
  sorcerer: ['camp+enemyCamp', 'sorcerer'], keg: ['row+frontIfFront', 'keg'], spearwall: ['facingFront'],
  deathHit: ['column', 'facing'], eotShoot: ['column', 'facing'], eotSapper: ['column', 'facing'], reaper: ['column', 'facing'],
  eotDrain: ['column', 'facing'], strix: ['column', 'facing'],
  eotInfect: ['column', 'facing'], deathPlague: ['column', 'facing'], mournSap: ['column', 'facing'],
  eotGharam: ['column', 'facingAll'], eotSap: ['column', 'facingAll'], eotLazaret: ['column', 'facingAll'],
  eotShootStr: ['reach', 'strike'], frenzy: ['reach', 'strike'], martyr: ['reach', 'strike'],
  eotBurn: ['enemyFront', 'enemyFront'], eotWail: ['enemyCamp', 'enemies'], eotGorvan: ['enemyCamp', 'enemies'], deathLane: ['enemyCamp', 'enemies'],
  eotFeverSap: ['enemyCamp', 'plagued'], eotIlyas: ['camp+enemyCamp', 'plagueAllies'],
  table: ['table'],
  charge: ['chargePath+facingFront', 'charge'],
  'place:komes': ['camp', 'allies'], 'place:mandator': ['camp', 'allies'], 'place:crowd': ['camp+enemyCamp'], 'place:weaver': ['camp', 'allies'],
  'place:cinder': ['camp+column', 'cinder'], 'place:pull': ['enemyCamp', 'pullable'], 'place:defect': ['enemyCamp', 'defectors'],
  'place:acolyte': ['column', 'facing'],
  'place:surgeon': ['camp', 'allies'], 'place:embalm': ['camp', 'allies'],
};
/** The units ability `flag` of u affects now. */
const targetsOf = (s, u, flag) => (SCOPE[flag] && SCOPE[flag][1] ? PICK[SCOPE[flag][1]](s, u) : []);
/** The cells ability `flag` of u works in. */
const areaOf = (s, u, flag) => (SCOPE[flag] ? SCOPE[flag][0].split('+').flatMap(a => AREA[a](s, u)) : []);
/** The abilities of unit u (its card's flags; placing: also its Place effect and charge). */
function abilitiesOf(u, placing = false) {
  const c = cardOf(u), out = Object.keys(c).filter(f => SCOPE[f] && f !== 'charge');
  if (placing && c.onPlace && SCOPE['place:' + c.onPlace]) out.push('place:' + c.onPlace);
  if (placing && (c.charge || u.chg) && !inFront(u)) out.push('charge');
  return out;
}

/** Round-end abilities, keyed by card flag. Each receives (state, unit, card, owner) and finds its targets with targetsOf. */
/** u deals amt damage to each target of its ability `flag` (targets and amount fixed when the ability starts). */
function damageTargets(s, u, flag, amt, label = unitName(u) + ' (round end)') {
  const ts = targetsOf(s, u, flag);
  if (!ts.length) log(s, label + ' finds no target.');
  for (const t of ts) if (byId(s, u.id) && byId(s, t.id)) dealDamage(s, amt, t, label, u);
}
/** u strikes each target of its ability `flag` with str. */
function strikeTargetsOf(s, u, flag, str, label = unitName(u) + ' (round end)') {
  const ts = targetsOf(s, u, flag);
  if (!ts.length) log(s, label + ' finds no one in reach.');
  for (const t of ts) if (byId(s, u.id) && byId(s, t.id)) hitUnit(s, str, t, label, u.id, false, true);
}
const ROUND_END = {
  eotAdjHeal(s, u) { for (const a of targetsOf(s, u, 'eotAdjHeal')) restoreShields(s, a, 1, unitName(u)); },
  eotLaneHealAll(s, u) { for (const a of targetsOf(s, u, 'eotLaneHealAll')) restoreShields(s, a, Infinity, unitName(u)); },
  drumHit(s, u) { damageTargets(s, u, 'drumHit', abilityHit(u, 1)); },
  sorcerer(s, u) {
    const ts = targetsOf(s, u, 'sorcerer');
    if (!ts.length) { log(s, unitName(u) + ' (round end) finds no enemy.'); return; }
    ts.pop();
    const bonus = abilityHit(u, 0), amt = abilityHit(u, 1);   // fixed when the ability starts
    let n = 0;
    for (const a of ts) if (byId(s, a.id) && byId(s, u.id)) { dealDamage(s, amt, a, unitName(u) + ' (round end)', u); n++; }
    processDeaths(s);
    const foe = enemyOrder(s, ctl(u), u.lane)[0];   // picked when this step happens
    if (n + bonus > 0 && foe && byId(s, u.id)) dealDamage(s, n + bonus, foe, unitName(u) + ' (round end)', u);
  },

  eotSelf(s, u, c) { if (byId(s, u.id)) hitUnit(s, abilityHit(u, c.eotSelf), u, unitName(u) + ' (itself)', null, true, true, true); },
  eotShoot(s, u, c) { damageTargets(s, u, 'eotShoot', abilityHit(u, c.eotShoot)); },
  eotShootStr(s, u) { strikeTargetsOf(s, u, 'eotShootStr', strengthOf(u)); },
  eotSapper(s, u, c) {
    damageTargets(s, u, 'eotSapper', abilityHit(u, c.eotSapper));
    processDeaths(s);
    if (byId(s, u.id)) kill(s, u, 'blows itself up');
  },
  eotBurn(s, u, c) {
    damageTargets(s, u, 'eotBurn', abilityHit(u, c.eotBurn));
    processDeaths(s);
    if (byId(s, u.id)) hitUnit(s, 1, u, unitName(u) + ' (itself)', null, true, true, true);
  },
  eotRegen(s, u) { restoreShields(s, u, Infinity, unitName(u)); },
  desert(s, u, c, p) { if (s.players[p].reserve === 0) kill(s, u, 'no pay: it deserts'); },
  // ----- Exanimati -----
  eotShadeFromGrave(s, u, c, p) {
    const D = s.players[p].discard, i = topUnitIndex(D);
    if (i < 0 || !freeSpots(s, p, u.lane, 'shade').length) return;
    log(s, `${unitName(u)} lights the way for ${CARDS[D[i]].name}.`);
    D.splice(i, 1);
    shadeAt(s, p, u.lane);
  },
  eotFerry(s, u, c, p) {
    const D = s.players[other(p)].discard, i = topUnitIndex(D);
    if (i < 0) return;
    log(s, `${unitName(u)} ferries ${CARDS[D[i]].name} away for good: +1 strength.`);
    D.splice(i, 1);
    u.ps = (u.ps || 0) + 1;
  },
  eotWail(s, u, c) { damageTargets(s, u, 'eotWail', abilityHit(u, c.eotWail)); },
  eotShadeFront(s, u, c, p) {
    const fr = frontRow(p);
    for (let col = 0; col < COLS; col++) if (fits(s, p, u.lane, 1, fr, col, 'h')) shadeAt(s, p, u.lane, [fr, col]);
  },
  eotInfect(s, u) { for (const t of targetsOf(s, u, 'eotInfect')) catchPlague(s, t, unitName(u)); },
  eotSap(s, u) { for (const e of targetsOf(s, u, 'eotSap')) { e.ps = (e.ps || 0) - 1; log(s, `${unitName(u)} saps ${unitName(e)}: -1 strength.`); } },
  eotSaint(s, u) {
    for (const a of targetsOf(s, u, 'eotSaint')) { a.ps = (a.ps || 0) + 1; a.pd = (a.pd || 0) + 1; log(s, `${unitName(u)} blesses ${unitName(a)}: +1|+1.`); }
    u.dmg = (u.dmg || 0) + 1;
    log(s, `${unitName(u)} crumbles: 1 shield lost.`);
    if (defenceOf(u) <= 0) kill(s, u, 'it crumbles away');
  },
  eotLazaret(s, u) { for (const e of targetsOf(s, u, 'eotLazaret')) catchPlague(s, e, unitName(u)); },
  eotIlyas(s, u) {
    for (const a of targetsOf(s, u, 'eotIlyas')) {
      const t = byId(s, a.id) ? facingTarget(s, a) : null;
      if (t) dealDamage(s, abilityHit(a, 1), t, unitName(a) + ' (fever)', a);
    }
  },
  eotDrain(s, u, c) { drain(s, u, c.eotDrain); },
  eotFeverSap(s, u) { for (const e of targetsOf(s, u, 'eotFeverSap')) { e.ps = (e.ps || 0) - 1; log(s, `${unitName(u)} saps ${unitName(e)}: -1 strength.`); } },
  eotGharam(s, u, c) { damageTargets(s, u, 'eotGharam', abilityHit(u, c.eotGharam)); },
  eotSpread(s, u) {
    const cell = spreadCells(s, u, 'free')[0];
    if (cell) { growInto(u, [cell]); emit(s, { merge: u.id }); log(s, `${unitName(u)} spreads.`); }
    u.ps = (u.ps || 0) + 1; u.pd = (u.pd || 0) + 1;
    applyAuras(s);
  },
  eotEat(s, u) {
    const prey = (spreadCells(s, u, 'ally')[0] || [])[2];
    if (!prey) return;
    const cells = cellsOf(prey), gainS = strengthOf(prey), gainD = defenceOf(prey);
    const flags = KW_FLAGS.filter(f => kw(prey, f) && !kw(u, f));
    kill(s, prey, 'eaten by ' + unitName(u));
    growInto(u, cells);
    emit(s, { merge: u.id });
    u.ps = (u.ps || 0) + gainS; u.pd = (u.pd || 0) + gainD;
    for (const f of flags) giveKw(u, f, kw(prey, f));
    log(s, `${unitName(u)} eats ${unitName(prey)}: +${gainS}|+${gainD}${flags.length ? ', ' + flags.map(f => KW_NAME[f]).join(', ') : ''}.`);
    applyAuras(s);
  },
  eotAbbess(s, u, c, p) { if (s.players[p].died === s.round) shadeAt(s, p, u.lane); },
  eotGorvan(s, u, c) { damageTargets(s, u, 'eotGorvan', abilityHit(u, c.eotGorvan)); },
};

/** Round end, per unit after its abilities: Plague eats a shield, Fading units fade. */
function exRoundEnd(s, u, p) {
  if (!byId(s, u.id)) return;
  if (kw(u, 'plague')) {
    const n = unitsIn(s, other(p), u.lane).some(o => cardOf(o).ophra) ? 2 : 1;
    u.dmg = (u.dmg || 0) + n;
    log(s, `${unitName(u)} wastes with Plague: ${n} shield${n > 1 ? 's' : ''} lost.`);
    if (defenceOf(u) <= 0) kill(s, u, 'Plague');
  }
  if (byId(s, u.id) && kw(u, 'fade') && u.born === s.round) kill(s, u, 'it fades');
}

function runRoundEndAbilities(s, p) {
  s.actor = p;
  const ids = s.units.filter(u => ctl(u) === p).sort(byReadingOrder).map(u => u.id);
  for (const id of ids) {
    const u = byId(s, id);
    if (!u) continue;
    const c = cardOf(u);
    applyAuras(s);
    for (const flag in ROUND_END) if (c[flag] && byId(s, u.id)) { ROUND_END[flag](s, u, c, p); processDeaths(s); }
    exRoundEnd(s, u, p);
    processDeaths(s);
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

/** Resolve the end of the round (abilities, bases, carry-over, winner). Returns true if the game is won. */
function resolveRoundEnd(s) {
  s.actor = null; s.pending = null;
  log(s, `Both sides pass. Round ${s.round} ends.`);
  s.inEnd = true;
  for (const p of [s.starter, other(s.starter)]) runRoundEndAbilities(s, p);
  s.inEnd = false;
  mergeLinks(s);
  settleTables(s);
  s.actor = null;
  for (const u of s.units) {
    u.ts = 0; u.tArm = false; u.tInc = false;
    if (u.td) { u.dmg = Math.max(0, (u.dmg || 0) - u.td); u.td = 0; }   // a lost defence bonus never takes shields away
  }
  applyAuras(s);
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


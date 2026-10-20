/* ---------- bases ---------- */
/** Per column: 0 or 1 = that side holds the dot, 'x' = cancelled, null = empty. */
function dotState(s, lane) {
  let m0 = 0, m1 = 0;
  for (const u of s.units) {
    if (u.lane !== lane) continue;
    const fr = frontRow(u.owner);
    for (const cell of cellsOf(u)) if (cell[0] === fr) { if (ctl(u) === 0) m0 |= 1 << cell[1]; else m1 |= 1 << cell[1]; }
  }
  const out = new Array(COLS);
  for (let c = 0; c < COLS; c++) {
    const a = (m0 >> c) & 1, b = (m1 >> c) & 1;
    out[c] = a && b ? 'x' : a ? 0 : b ? 1 : null;
  }
  return out;
}
const ownerOfDots = dots => [0, 1].find(p => dots.filter(d => d === p).length >= 2) ?? null;
const laneOwner = (s, lane) => ownerOfDots(dotState(s, lane));

/* ---------- supply ---------- */
// Payment uses the acting player's lane supply first, then carry-over.
const supplyLeft = (s, lane) => s.pool[s.cur][lane] + s.players[s.cur].reserve;
const canPay = (s, lane, n) => s.test || supplyLeft(s, lane) >= n;
function pay(s, lane, n) {
  if (s.test) return;
  const pool = s.pool[s.cur], fromLane = Math.min(n, pool[lane]);
  pool[lane] -= fromLane;
  s.players[s.cur].reserve -= n - fromLane;
}
const carryOrder = p => (p === 0 ? [0, 1, 2] : [2, 1, 0]);

/** Carry-over p would have next round if the round ended now. */
function projectedCarry(s, p) {
  let reserve = s.players[p].reserve;
  const pool = s.pool[p];
  let room = MAX_CARRY - reserve;
  for (const lane of carryOrder(p)) {
    const n = Math.max(0, Math.min(room, pool[lane]));
    room -= n; reserve += n;
  }
  return reserve;
}

/* ---------- positioning effects (recomputed whenever units change) ---------- */
/** Cards whose position effects applyAuras computes (the others are skipped there). */
const AURA_CARDS = new Set(Object.keys(CARDS).filter(k => ['wall', 'rowAura', 'frontBuff', 'bleed', 'gorged', 'shadeAura', 'overseer', 'pack', 'skirm', 'adjAura'].some(f => CARDS[k][f])));
function applyAuras(s) {
  const units = s.units, before = units.map(u => u.bd || 0);
  for (const u of units) { u.bs = 0; u.bd = 0; }
  for (const u of units) {
    if (!AURA_CARDS.has(baseKey(u.card))) continue;
    const c = cardOf(u);
    if (c.wall) u.bd += targetsOf(s, u, 'wall').length;
    if (c.rowAura) for (const a of targetsOf(s, u, 'rowAura')) { a.bs += c.rowAura.s; a.bd += c.rowAura.d; }
    if (c.frontBuff && targetsOf(s, u, 'frontBuff').length) u.bs += c.frontBuff;
    if (c.bleed) u.bs += Math.max(0, u.dmg || 0);
    if (c.gorged) u.bs += Math.max(0, (u.pd || 0) - (u.dmg || 0));
    if (c.shadeAura) for (const a of targetsOf(s, u, 'shadeAura')) { a.bs += 1; a.bd += 1; }
    if (c.overseer) for (const a of targetsOf(s, u, 'overseer')) { a.bs += 1; a.bd += 1; }
    if (c.pack || c.skirm || c.adjAura) {
      const near = adjacentAllies(s, u);
      if (c.pack) u.bs += c.pack * near.length;
      if (c.skirm && !near.length) u.bd += c.skirm;
      if (c.adjAura) for (const a of near) { a.bs += c.adjAura.s; a.bd += c.adjAura.d; }
    }
  }
  // a lost defence bonus never takes shields away: defence left = min(what it had, its defence without the bonus)
  for (let i = 0; i < units.length; i++) {
    const u = units[i], lost = before[i] - u.bd;
    if (lost > 0 && u.dmg > 0) u.dmg = Math.max(0, u.dmg - lost);
  }
}

/* ---------- state, log and animation events ---------- */
function newGame(deck0, deck1, test = false) {
  const first = Math.random() < 0.5 ? 0 : 1;   // who acts first in round 1 is random
  const player = deck => ({
    deck, hand: [], discard: [], reserve: START_CARRY, dealt: [], redrawn: [],
    draw: shuffle(DECKS[deck].list.flatMap(([k, n]) => Array(n).fill(k))),
  });
  const s = {
    players: [player(deck0), player(deck1)], units: [], nid: 1,
    round: 1, turn: 1, starter: first, cur: first, passed: null, actor: null, pending: null,
    owner: [null, null, null], ownerStart: [null, null, null], winner: null, quietRounds: 0, acts: 0,
    pool: [[0, 0, 0], [0, 0, 0]], poolStart: [[0, 0, 0], [0, 0, 0]],
    log: [], fx: [], ev: [], test,
  };
  drawCards(s, 0, START_HAND);
  drawCards(s, 1, START_HAND);
  for (const P of s.players) P.dealt = P.hand.slice();
  log(s, 'Battle begins.');
  startRound(s, true);
  return s;
}

function drawCards(s, p, n) {
  const P = s.players[p];
  let drawn = 0;
  while (drawn < n && P.draw.length && P.hand.length < HAND_LIMIT) { P.hand.push(P.draw.pop()); drawn++; }
  if (drawn < n && P.draw.length && P.hand.length >= HAND_LIMIT) log(s, `${deckName(s, p)} has ${HAND_LIMIT} cards in hand and draws no more.`);
  return drawn;
}

/** Starting-hand redraw: swap hand card i for a fresh one and shuffle it back in (at most 3, each dealt card once). */
function redraw(s, p, i) {
  const P = s.players[p];
  if (!P.draw.length || P.redrawn.length >= MAX_REDRAW) return;
  P.redrawn.push(P.hand[i]);
  const fresh = P.draw.pop();
  P.draw.push(P.hand[i]);
  shuffle(P.draw);
  P.hand[i] = fresh;
}

/** Log line, tagged with the side that caused it (s.actor; null = neutral). */
function log(s, msg) {
  if (s.noFx) return;
  s.log.unshift({ m: msg, side: s.actor });
  if (s.log.length > 80) s.log.length = 80;
}

function snapshot(s) {
  return JSON.parse(JSON.stringify({
    units: s.units, tombs: s.tombs || [], resNow: (s.resStack || []).slice(-1)[0], owner: s.owner, ownerStart: s.ownerStart, pool: s.pool, poolStart: s.poolStart,
    cur: s.cur, round: s.round, starter: s.starter, passed: s.passed,
    players: s.players.map(P => ({ deck: P.deck, discard: P.discard, reserve: P.reserve, drawN: P.draw.length, handN: P.hand.length })),
  }));
}
/** Queue an animation event with a snapshot of the state at that moment. */
function emit(s, event) {
  if (s.noFx) return;
  if (event.hit) event.grp = s.grp || 0;   // hits of one step share a group: the screen plays them at once
  event.snap = snapshot(s);
  s.fx.push(event);
}


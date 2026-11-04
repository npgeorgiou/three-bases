/* =====================================================================
   Strategist AI (new; the game itself still uses the benchmark AI)

   Knowledge: it never sees the opponent's hand or any deck order. Each decision it deals the
   opponent a random possible hand from the cards not yet seen (optionally several, averaged).

   Goals: every turn each side gets two goal lanes, the ones cheapest to win or keep (with a
   preference for keeping last turn's goals). Bases, dots, units and income in goal lanes count
   fully; the third lane counts for less.

   Rules of thumb: no deploys into a lane already safely won (except income units), no deploys
   into a lane outside the side's goals unless they block an enemy dot, no spending supply on
   actions that change nothing.

   Look-ahead: its move, the opponent's best replies, its best answers; each line judged as the
   round would end if both passed then. The move with the best worst-case line is played.
   ===================================================================== */

const STRATEGIST_DEFAULTS = {
  base: 250, dot: 50, offGoal: 0.7,          // worth of a base and a dot; share kept in a non-goal lane
  twoBases: 400,                              // holding two bases (the opponent holding two counts 1.5x against)
  unitCost: 10, str: 2, def: 3, front: 6,     // unit worth: per supply cost, strength, defence; bonus in the front row
  income: 12, safeIncome: 0.3, pool: 3,       // per supply of income; share in a safely won lane; per unspent supply
  carry: 10, hand: 4, threat: 1, lifeline: 1, // carry-over, cards in hand, what can be killed, out-of-supply danger
  stick: 1.5,                                 // preference for keeping last turn's goal lanes
  rootWidth: 8, width2: 6, width1: 4,         // actions examined: own first actions, replies, own answers
  samples: 3,                                 // random opponent hands to average over
  rules: true,                                // apply the rules of thumb
};

/** The game as `me` may know it: the opponent holds a random possible hand; decks in unknown order. */
function sampledView(s, me) {
  const opp = other(me), v = cloneState(s), unseen = [];
  for (const [k, n] of Object.entries(unseenCards(s, opp))) for (let i = 0; i < n; i++) unseen.push(k);
  shuffle(unseen);
  const size = s.players[opp].hand.length;
  v.players[opp].hand = unseen.slice(0, size);
  v.players[opp].draw = unseen.slice(size);
  v.players[me].draw = shuffle(v.players[me].draw.slice());
  v.noFx = true;
  return v;
}

/* ---------- what can be known ---------- */

/** Cards of `side`'s faction not yet seen by the other side, as { cardKey: copies }. */
function unseenCards(s, side) {
  const left = {};
  for (const [k, n] of DECKS[s.players[side].deck].list) left[k] = (left[k] || 0) + n;
  const seen = [...s.players[side].discard, ...s.units.filter(u => u.owner === side).map(u => u.card)];
  for (const k of seen) if (left[k]) left[k]--;
  for (const k in left) if (!left[k]) delete left[k];
  return left;
}

/** What `victim` could lose to the other side's unit attacks right now, knowing that Bodyguards protect
 *  their neighbours and that units which already attacked threaten nothing more (cfg switches both). */
function threatAgainstSeen(s, victim, cfg) {
  const attacker = other(victim), reserve = s.players[attacker].reserve;
  let loss = 0;
  for (const u of s.units.filter(x => ctl(x) === victim)) {
    if (cfg.threatSeesGuards && !cardOf(u).guard
      && s.units.some(g => ctl(g) === victim && g !== u && cardOf(g).guard && adjacent(u, g))) continue;
    const budget = s.pool[attacker][u.lane] + reserve;
    let best = 0;
    for (const a of unitsIn(s, attacker, u.lane)) {
      const c = cardOf(a);
      if (strengthOf(a) <= 0 || budget < c.sup || (cfg.threatSeesActed && a.attacked)) continue;
      if (!isIncorp(u) && reaches(a, u)) best = Math.max(best, strengthOf(a));
    }
    loss += best >= defenceOf(u) ? unitValue(u) * 0.6 : best * 2;
  }
  return loss;
}

/* ---------- goals ---------- */

/** How much it would take `p` to win (or keep) a lane: missing dots, enemy dots and power, own power and income. */
function laneNeed(s, p, lane) {
  const q = other(p), d = dotState(s, lane);
  const power = side => unitsIn(s, side, lane).reduce((n, u) => n + strengthOf(u) + defenceOf(u), 0);
  return 2 * Math.max(0, 2 - d.filter(x => x === p).length) + 1.5 * d.filter(x => x === q).length
    + 0.15 * power(q) - 0.1 * power(p) - 0.2 * laneSupply(s, p, lane);
}

/** The two lanes `p` fights for: its two bases if it holds two, else the two cheapest to win. */
function pickGoals(s, p, prev, cfg) {
  if (basesHeld(s, p) >= 2) return LANES.filter(l => s.owner[l] === p).slice(0, 2);
  const cost = l => laneNeed(s, p, l) - (prev && prev.includes(l) ? cfg.stick : 0);
  return LANES.slice().sort((a, b) => cost(a) - cost(b)).slice(0, 2);
}

/* ---------- score ---------- */

const STRAT_THREAT = { threatSeesGuards: true, threatSeesActed: true };

/** Score of a position for p, valuing p's goal lanes fully and the third lane at the off-goal share. */
function strategistEvaluate(s, p, goal, cfg) {
  if (s.winner !== null) return evaluate(s, p);
  const q = other(p);
  let v = 0;
  for (const lane of LANES) {
    const w = goal.includes(lane) ? 1 : cfg.offGoal, d = dotState(s, lane), owner = ownerOfDots(d);
    v += w * ((owner === p ? cfg.base : owner === q ? -cfg.base : 0) + cfg.dot * (d.filter(x => x === p).length - d.filter(x => x === q).length));
    for (const u of s.units) {
      if (u.lane !== lane) continue;
      const c = cardOf(u), worth = c.sup * cfg.unitCost + strengthOf(u) * cfg.str + defenceOf(u) * cfg.def
        + (inFront(u) && (strengthOf(u) > 0 || c.def > 1) ? cfg.front : 0);
      v += (ctl(u) === p ? 1 : -1) * (0.5 + 0.5 * w) * worth;
    }
    const income = side => (isSafeLane(s, side, lane) ? cfg.safeIncome : 1) * Math.min(6, laneSupply(s, side, lane));
    v += cfg.income * w * (income(p) - income(q)) + cfg.pool * (s.pool[p][lane] - s.pool[q][lane]);
  }
  if (basesHeld(s, p) >= 2) v += cfg.twoBases;
  if (basesHeld(s, q) >= 2) v -= 1.5 * cfg.twoBases;
  const mine = threatAgainstSeen(s, p, STRAT_THREAT), theirs = threatAgainstSeen(s, q, STRAT_THREAT);
  v += cfg.threat * (s.cur === q ? -mine + 0.3 * theirs : 0.9 * theirs - 0.3 * mine);
  const carry = side => (s.carried ? s.carried[side] : projectedCarry(s, side));
  v += cfg.carry * (carry(p) - carry(q)) + cfg.hand * (s.players[p].hand.length - s.players[q].hand.length);
  const danger = side => {
    if (carry(side) > 0) return 0;
    const n = s.units.filter(u => ctl(u) === side).length;
    return n === 0 ? 1000 : n === 1 ? 300 : n === 2 ? 100 : 0;
  };
  return v + cfg.lifeline * (danger(q) - danger(p));
}


/* ---------- rules of thumb ---------- */

/** Whether a deploy breaks a rule of thumb for the side making it. */
function breaksRule(s, a, goal) {
  if (a.t !== 'deploy') return false;
  const p = s.cur, card = CARDS[s.players[p].hand[a.hi]];
  if (card.bonus) return false;                                   // income units may go anywhere safe
  if (isSafeLane(s, p, a.lane)) return true;                      // don't overload a lane already won
  if (goal.includes(a.lane)) return false;
  // outside the goals only to block an enemy dot: a front-row spot facing an enemy front unit
  const cells = cellsAt(card.size, a.r, a.c, a.o).filter(([r]) => r === frontRow(p)).map(([, c]) => c);
  return !cells.some(c => dotState(s, a.lane)[c] === other(p));
}

/** Every legal option for the side to move (every placement counts), rules applied, best first. */
function strategistOptions(t, goals, cfg) {
  const side = t.cur, out = [];
  for (const a of listActions(t)) {
    if (cfg.rules && breaksRule(t, a, goals[side])) continue;
    const n = cloneState(t);
    applyAction(n, a);
    out.push({ a, t: n, v: strategistEvaluate(n, side, goals[side], cfg) });
  }
  return out.sort((x, y) => y.v - x.v);
}

/* ---------- look-ahead ---------- */

function strategistSearch(t, me, depth, goals, cfg, alpha = -Infinity, beta = Infinity) {
  // alpha-beta pruning, as in the Benchmark's search: called without bounds (as the top level does) the value is
  // exact; below that, lines that cannot change the result are not looked at
  if (t.winner !== null) return evaluate(t, me);
  if (depth === 0 || t.roundOver) {
    const view = nextRoundView(t);
    return view.winner !== null ? evaluate(view, me) : strategistEvaluate(view, me, goals[me], cfg);
  }
  const mine = t.cur === me, width = depth === 2 ? cfg.width2 : cfg.width1;
  const options = strategistOptions(t, goals, cfg);
  const picked = options.slice(0, width), pass = options.find(o => o.a.t === 'pass');
  if (pass && !picked.includes(pass)) picked.push(pass);
  let best = mine ? -Infinity : Infinity;
  for (const o of picked) {
    if (mine) {
      const v = strategistSearch(o.t, me, depth - 1, goals, cfg, Math.max(alpha, best), beta);
      if (v > best) best = v;
      if (best > beta) return best;
    } else {
      const v = strategistSearch(o.t, me, depth - 1, goals, cfg, alpha, Math.min(beta, best));
      if (v < best) best = v;
      if (best < alpha) return best;
    }
  }
  return best;
}

/** Last turn's goal lanes of each computer player, per game. */
const strategistGoals = new WeakMap();

function chooseStrategistAction(s, cfg = STRATEGIST_DEFAULTS) {
  const me = s.cur, opp = other(me), memory = strategistGoals.get(s) || [null, null];
  const totals = new Map();
  let goalsUsed = null;
  for (let k = 0; k < cfg.samples; k++) {
    const t = sampledView(s, me);
    t.stopAtRoundEnd = true;
    const goals = [];
    goals[me] = pickGoals(t, me, memory[me], cfg);
    goals[opp] = pickGoals(t, opp, memory[opp], cfg);
    goalsUsed = goals;
    const now = outcomeOf(t, me);
    const options = strategistOptions(t, goals, cfg).filter(o => !isPointless(t, o.a, o.t, now));
    const picked = options.slice(0, cfg.rootWidth), pass = options.find(o => o.a.t === 'pass');
    if (pass && !picked.includes(pass)) picked.push(pass);
    for (const o of picked) {
      const key = JSON.stringify(o.a), v = strategistSearch(o.t, me, 2, goals, cfg);
      const e = totals.get(key) || { a: o.a, sum: 0, n: 0, cost: actionCost(t, o.a) };
      e.sum += v; e.n++;
      totals.set(key, e);
    }
  }
  strategistGoals.set(s, goalsUsed);
  let best = null;
  for (const e of totals.values()) {
    const value = e.sum / e.n;
    if (!best || value > best.value + 1e-6 || (Math.abs(value - best.value) <= 1e-6 && e.cost < best.cost)) best = { a: e.a, value, cost: e.cost };
  }
  return best ? best.a : { t: 'pass' };
}


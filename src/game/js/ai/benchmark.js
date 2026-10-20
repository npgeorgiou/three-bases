/* =====================================================================
   THE BENCHMARK: the AI lab's ifelse AI with its tuned values ("ifelse AI gen 18")
   ===================================================================== */
const BENCH_VALUES = {"depth": 3, "w1": 16, "w2": 16, "w3": 1, "w4": 1, "w5": 1, "skipPointless": 1, "base": 52.24794805722803, "dot": 68.51388494977554, "secondBase": 102.66407646583588, "twoBases": 177.25361791861496, "twoBasesOpp": 199.7574182161945, "income": 31.656078857105964, "incomeCap": 2, "safeIncome": 0.05504762091184498, "pool": 2.741304155326895, "carry": 30, "hand": 4.633833562934903, "handCost": 2.8042200628587772, "uSup": 12.07189493456142, "uStr": 1.5479816366387755, "uDef": 1.8437067986291322, "uSupBonus": 6.622116494092802, "front": 28.969241514744198, "safeHolders": 1, "safeExtra": 0.04993113138665096, "armyStep": 0.8376563975571105, "armyFloor": 0.0812832334017826, "threat": 5.16860316310796, "kill": 0.45887300525839325, "damage": 0.8280634749424957, "thMineOpp": 1.6299806213311494, "thTheirsOpp": 0.5824609790085519, "thTheirsMe": 0.9561631170420163, "thMineMe": 0.2500662829114908, "tOnce": 1, "tGuards": 1, "tActed": 1, "danger0": 1451.988204947475, "danger1": 165.23566872600335, "danger2": 25.633149570136343, "draw": -985.4667485840048, "goals": 0, "offGoal": 0.3452749916684562, "stick": 2.0893563598964398, "needDots": 1.774190115518511, "needEnemyDots": 0.8208140494071128, "needEnemyPower": 0.27442838218710763, "needOwnPower": 0.04135135057152874, "needSupply": 0.06097458844391373, "killPref": 1, "passPen": 40, "freeCheck": 1};
const ifelseConfig = cfg => ({ ...cfg });

function ifelseWorth(u, c) {
  const k = cardOf(u);
  return k.sup * c.uSup + strengthOf(u) * c.uStr + defenceOf(u) * c.uDef + (k.sup + (k.bonus || 0)) * c.uSupBonus;
}
function ifelseArmy(s, side, lane, c) {
  const units = unitsIn(s, side, lane).map(u => ({ front: inFront(u),
    worth: ifelseWorth(u, c) + (inFront(u) && (strengthOf(u) > 0 || cardOf(u).def > 1) ? c.front : 0) }));
  let total = 0;
  if (isSafeLane(s, side, lane)) {
    units.sort((a, b) => (b.front - a.front) || (b.worth - a.worth));
    let held = 0;
    for (const x of units) if (x.front && held < c.safeHolders) { total += x.worth; held++; } else total += x.worth * c.safeExtra;
  } else units.map(x => x.worth).sort((a, b) => b - a).forEach((w, i) => { total += w * Math.max(c.armyFloor, 1 - i * c.armyStep); });
  return total;
}
/** What `victim` could lose to the other side's unit attacks now. With tOnce: attacks are assigned greedily,
 *  most damaging first, each attacker once, paid from its lane's supply and then the shared reserve, and
 *  several attackers may finish one target together. */
function ifelseThreat(s, victim, c) {
  const att = other(victim), canHit = (a, u) => !isIncorp(u) && reaches(a, u);
  const targets = s.units.filter(u => ctl(u) === victim && !(c.tGuards && !cardOf(u).guard
    && s.units.some(g => ctl(g) === victim && g !== u && cardOf(g).guard && adjacent(u, g))));
  const attackers = s.units.filter(a => ctl(a) === att && strengthOf(a) > 0 && !(c.tActed && a.attacked));
  if (!c.tOnce) {
    const reserve = s.players[att].reserve;
    let loss = 0;
    for (const u of targets) {
      let best = 0;
      for (const a of attackers) if (a.lane === u.lane && s.pool[att][u.lane] + reserve >= cardOf(a).sup && canHit(a, u)) best = Math.max(best, strengthOf(a));
      loss += best >= defenceOf(u) ? ifelseWorth(u, c) * c.kill : best * c.damage;
    }
    return loss;
  }
  const pool = LANES.map(l => s.pool[att][l]);
  let reserve = s.players[att].reserve, loss = 0;
  const T = targets.map(u => ({ u, hp: defenceOf(u), dealt: 0, counted: 0, dead: false, worth: ifelseWorth(u, c) })), used = new Set();
  for (;;) {
    let best = null;
    for (const a of attackers) {
      if (used.has(a) || pool[a.lane] + reserve < cardOf(a).sup) continue;
      for (const t of T) {
        if (t.dead || t.u.lane !== a.lane || !canHit(a, t.u)) continue;
        const str = strengthOf(a), gain = t.dealt + str >= t.hp ? t.worth * c.kill - t.counted : str * c.damage;
        if (gain > 0 && (!best || gain > best.gain)) best = { a, t, gain };
      }
    }
    if (!best) return loss;
    const { a, t, gain } = best, cost = cardOf(a).sup, fromLane = Math.min(cost, pool[a.lane]);
    pool[a.lane] -= fromLane; reserve -= cost - fromLane; used.add(a);
    t.dealt += strengthOf(a); t.counted += gain; loss += gain;
    if (t.dealt >= t.hp) t.dead = true;
  }
}
function ifelseNeed(s, p, lane, c) {
  const q = other(p), d = dotState(s, lane), power = side => unitsIn(s, side, lane).reduce((n, u) => n + strengthOf(u) + defenceOf(u), 0);
  return c.needDots * Math.max(0, 2 - d.filter(x => x === p).length) + c.needEnemyDots * d.filter(x => x === q).length
    + c.needEnemyPower * power(q) - c.needOwnPower * power(p) - c.needSupply * laneSupply(s, p, lane);
}
function ifelseGoalsFor(s, p, prev, c) {
  if (basesHeld(s, p) >= 2) return LANES.filter(l => s.owner[l] === p).slice(0, 2);
  const cost = l => ifelseNeed(s, p, l, c) - (prev && prev.includes(l) ? c.stick : 0);
  return LANES.slice().sort((a, b) => cost(a) - cost(b)).slice(0, 2);
}
/** Score of a position for p. goal: p's goal lanes (null when goal lanes are off). */
function ifelseEval(s, p, goal, c) {
  if (s.winner === 'lost') return -1e6;
  if (s.winner === p) return 1e6;
  if (s.winner === 'draw') return c.draw;
  if (s.winner !== null) return -1e6;
  const q = other(p);
  let v = 0;
  for (const lane of LANES) {
    const w = goal ? (goal.includes(lane) ? 1 : c.offGoal) : 1, d = dotState(s, lane), owner = ownerOfDots(d);
    v += w * ((owner === p ? c.base : owner === q ? -c.base : 0) + c.dot * (d.filter(x => x === p).length - d.filter(x => x === q).length));
    const inc = side => (isSafeLane(s, side, lane) ? c.safeIncome : 1) * Math.min(c.incomeCap, laneSupply(s, side, lane));
    v += c.income * w * (inc(p) - inc(q)) + c.pool * (s.pool[p][lane] - s.pool[q][lane]);
    v += (0.5 + 0.5 * w) * (ifelseArmy(s, p, lane, c) - ifelseArmy(s, q, lane, c));
  }
  if (basesKept(s, p) >= 2) v += c.twoBases;     // the win rule: held at round start and now (in the next-round view, start = now)
  if (basesKept(s, q) >= 2) v -= c.twoBasesOpp;
  for (const side of [p, q]) if (basesHeld(s, side) === 1)
    for (const lane of LANES) if (s.owner[lane] !== side) v += (side === p ? 1 : -1) * c.secondBase * dotState(s, lane).filter(x => x === side).length;
  if (c.threat) {
    const mine = ifelseThreat(s, p, c), theirs = ifelseThreat(s, q, c);
    v += c.threat * (s.cur === q ? -c.thMineOpp * mine + c.thTheirsOpp * theirs : c.thTheirsMe * theirs - c.thMineMe * mine);
  }
  const carry = side => (s.carried ? s.carried[side] : projectedCarry(s, side));
  v += c.carry * (carry(p) - carry(q)) + c.hand * (s.players[p].hand.length - s.players[q].hand.length);
  if (c.handCost) { const hc = side => s.players[side].hand.reduce((n, k) => n + (CARDS[k].cost || CARDS[k].sup || 0), 0); v += c.handCost * (hc(p) - hc(q)); }
  const danger = side => {
    if (carry(side) > 0) return 0;
    const n = s.units.filter(u => u.owner === side).length;
    return n === 0 ? c.danger0 : n === 1 ? c.danger1 : n === 2 ? c.danger2 : 0;
  };
  return v + danger(q) - danger(p);
}
/** The side to move's best `width` options by a quick score, always including passing. */
function ifelseOptions(t, goals, c, width, keep) {
  const side = t.cur, scored = [];
  for (const a of listActions(t)) {
    const n = cloneState(t);
    applyAction(n, a);
    if (keep && !keep(a, n)) continue;
    scored.push({ a, t: n, v: ifelseEval(n, side, goals ? goals[side] : null, c) });
  }
  scored.sort((x, y) => y.v - x.v);
  const picked = scored.slice(0, width), pass = scored.find(x => x.a.t === 'pass');
  if (pass && !picked.includes(pass)) picked.push(pass);
  return picked;
}
function ifelseSearch(t, me, left, level, goals, c, alpha = -Infinity, beta = Infinity) {
  if (t.winner !== null) return ifelseEval(t, me, null, c);
  if (left === 0 || t.roundOver) { const view = nextRoundView(t); return ifelseEval(view, me, goals ? goals[me] : null, c); }
  const mine = t.cur === me;
  let best = mine ? -Infinity : Infinity;
  for (const o of ifelseOptions(t, goals, c, c['w' + level])) {
    if (mine) {
      const v = ifelseSearch(o.t, me, left - 1, level + 1, goals, c, Math.max(alpha, best), beta);
      if (v > best) best = v;
      if (best > beta) return best;
    } else {
      const v = ifelseSearch(o.t, me, left - 1, level + 1, goals, c, alpha, Math.min(beta, best));
      if (v < best) best = v;
      if (best < alpha) return best;
    }
  }
  return best;
}
/** Root-only preferences: killing enemy units (by their worth), and not passing just because the opponent passed. */
function rootPref(s, o, me, c) {
  let v = 0;
  if (c.killPref) for (const u of s.units) if (ctl(u) !== me && !byId(o.t, u.id)) v += c.killPref * ifelseWorth(u, c);
  if (c.passPen && o.a.t === 'pass' && s.passed === other(me)) v -= c.passPen;
  return v;
}
const ifelseGoalMemory = new WeakMap();
function chooseIfelseAction(s, cfg) {
  const c = ifelseConfig(cfg), me = s.cur, root = cloneState(s);
  root.noFx = true; root.stopAtRoundEnd = true;
  let goals = null;
  if (c.goals) {
    const prev = ifelseGoalMemory.get(s) || [null, null];
    goals = []; goals[me] = ifelseGoalsFor(root, me, prev[me], c); goals[other(me)] = ifelseGoalsFor(root, other(me), prev[other(me)], c);
    ifelseGoalMemory.set(s, goals);
  }
  const now = c.skipPointless ? outcomeOf(root, me) : null;
  const prefMax = (c.killPref || 0) * 1000;
  let best = null;
  for (const o of ifelseOptions(root, goals, c, c.w1, c.skipPointless ? (a, t) => !isPointless(root, a, t, now, c) : null)) {
    let value = ifelseSearch(o.t, me, Math.max(0, Math.round(c.depth) - 1), 2, goals, c, best ? best.value - 2e-6 - prefMax : -Infinity), cost = actionCost(root, o.a);
    value += rootPref(root, o, me, c);
    if (!best || value > best.value + 1e-6 || (Math.abs(value - best.value) <= 1e-6 && cost < best.cost)) best = { a: o.a, value, cost };
  }
  if (!best && s.pending) return listActions(s)[0];   // a choice must be made even when every option looked pointless
  return best ? best.a : { t: 'pass' };
}

/** The Random player's move: a kind of move at random (deploy, move, attack, spell, pass...), then one of that kind. */
function randomMove(options) {
  const kinds = new Map();
  for (const o of options) (kinds.get(o.a.t) || kinds.set(o.a.t, []).get(o.a.t)).push(o);
  const group = [...kinds.values()][Math.floor(Math.random() * kinds.size)];
  return group[Math.floor(Math.random() * group.length)];
}

/** The Benchmark's redraw: cards costing 4 or more, the most expensive first, at most 3. */
function aiMulligan(s, p) {
  const hand = s.players[p].hand;
  hand.map((k, i) => i).filter(i => CARDS[hand[i]].cost >= 4).sort((a, b) => CARDS[hand[b]].cost - CARDS[hand[a]].cost)
    .slice(0, MAX_REDRAW).forEach(i => redraw(s, p, i));
}
/** The Random player's redraw: 0 to 3 of its cards, at random. */
function randomRedraw(s, p) {
  const idx = shuffle([...s.players[p].hand.keys()]);
  idx.slice(0, Math.floor(Math.random() * (MAX_REDRAW + 1))).forEach(i => redraw(s, p, i));
}


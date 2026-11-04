/* =====================================================================
   THE EARLIER BENCHMARK'S SCORE AND SEARCH
   Its hand-tuned score of a position and its shallow search (own action, the opponent's best reply, own best
   follow-up); used by a learning AI's "Benchmark search". The lab's Benchmark player is the game's.
   ===================================================================== */

/** Rough worth of a unit on the board. */
function unitValue(u) {
  const c = cardOf(u);
  return c.sup * 10 + strengthOf(u) * 2 + defenceOf(u) * 3 + (c.sup + (c.bonus || 0)) * 5;
}

/** Expected loss for `victim` if the other side strikes with what it can afford right now. */
function threatAgainst(s, victim) {
  const attacker = other(victim), reserve = s.players[attacker].reserve;
  let loss = 0;
  for (const u of s.units.filter(x => ctl(x) === victim)) {
    const budget = s.pool[attacker][u.lane] + reserve;
    let best = 0;
    for (const a of unitsIn(s, attacker, u.lane)) {
      const c = cardOf(a);
      if (strengthOf(a) <= 0 || budget < c.sup) continue;
      if (!isIncorp(u) && reaches(a, u)) best = Math.max(best, strengthOf(a));
    }
    loss += best >= defenceOf(u) ? unitValue(u) * 0.6 : best * 2;
  }
  return loss;
}

/** Units' worth in one lane. In a safe lane only the two front units holding the dots count fully. */
function laneArmyValue(s, side, lane) {
  const units = unitsIn(s, side, lane).map(u => ({
    front: inFront(u),
    worth: unitValue(u) + (inFront(u) && (strengthOf(u) > 0 || cardOf(u).def > 1) ? 6 : 0),
  }));
  let total = 0;
  if (isSafeLane(s, side, lane)) {
    units.sort((a, b) => (b.front - a.front) || (b.worth - a.worth));
    let holders = 0;
    for (const x of units) {
      if (x.front && holders < 2) { total += x.worth; holders++; } else total += x.worth * 0.1;
    }
  } else {
    units.map(x => x.worth).sort((a, b) => b - a).forEach((w, i) => { total += w * Math.max(0.3, 1 - i * 0.15); });
  }
  return total;
}

/** The named terms that make up the score of a position for side p (see evaluate). */
function evaluationTerms(s, p) {
  const q = other(p), t = { bases: 0, dots: 0, income: 0, pool: 0, army: 0, twoBases: 0, secondBase: 0, threat: 0, carry: 0, hand: 0 };
  const laneDots = LANES.map(lane => dotState(s, lane));
  for (const lane of LANES) {
    const dots = laneDots[lane], owner = ownerOfDots(dots);
    t.bases += owner === p ? 220 : owner === q ? -220 : 0;
    t.dots += 45 * (dots.filter(d => d === p).length - dots.filter(d => d === q).length);
    const incomeWeight = side => (isSafeLane(s, side, lane) ? 0.3 : 1);   // income in a won lane buys little
    t.income += 12 * (incomeWeight(p) * Math.min(6, laneSupply(s, p, lane)) - incomeWeight(q) * Math.min(6, laneSupply(s, q, lane)));
    t.pool += 3 * (s.pool[p][lane] - s.pool[q][lane]);                    // supply still usable this round
    t.army += laneArmyValue(s, p, lane) - laneArmyValue(s, q, lane);
  }
  if (basesHeld(s, p) >= 2) t.twoBases += 300;
  if (basesHeld(s, q) >= 2) t.twoBases -= 450;
  for (const side of [p, q]) if (basesHeld(s, side) === 1)                // with one base, the other lanes matter more
    for (const lane of LANES) if (s.owner[lane] !== side)
      t.secondBase += (side === p ? 30 : -30) * laneDots[lane].filter(d => d === side).length;
  const mine = threatAgainst(s, p), theirs = threatAgainst(s, q);         // what the side to move can kill
  t.threat = s.cur === q ? -mine + 0.3 * theirs : 0.9 * theirs - 0.3 * mine;
  // carry-over kept for next round (at a leaf: what this round really carried; lanes there are already refilled)
  t.carry = s.carried ? 10 * (s.carried[p] - s.carried[q]) : 10 * (projectedCarry(s, p) - projectedCarry(s, q));
  t.hand = 4 * (s.players[p].hand.length - s.players[q].hand.length);
  // lifeline: with no carry-over, losing your last few units loses the game (out of supply)
  const danger = side => {
    const carry = s.carried ? s.carried[side] : projectedCarry(s, side);
    if (carry > 0) return 0;
    const n = s.units.filter(u => ctl(u) === side).length;
    return n === 0 ? 1000 : n === 1 ? 300 : n === 2 ? 100 : 0;
  };
  t.lifeline = danger(q) - danger(p);
  return t;
}

/** Score of a position from side p's point of view. */
function evaluate(s, p) {
  if (s.winner === 'lost') return -1e6;             // both sides lost
  if (s.winner === p) return 1e6;
  if (s.winner === other(p)) return -1e6;
  if (s.winner === 'draw') return -500;
  return Object.values(evaluationTerms(s, p)).reduce((a, b) => a + b, 0);
}

/** How good a position is for p, judged as the next round would begin. */
const evaluateOutcome = (s, p) => evaluate(nextRoundView(s), p);

/** States after each of `side`'s most promising actions (by a quick score), always including passing. */
function promisingReplies(s, side, limit, keep) {
  const scored = listActions(s).map(a => {
    const t = cloneState(s);
    applyAction(t, a);
    return { a, t, v: evaluate(t, side) };
  }).filter(x => !keep || keep(x.a, x.t)).sort((x, y) => y.v - x.v);
  const picked = scored.slice(0, limit);
  const pass = scored.find(x => x.a.t === 'pass');
  if (!picked.includes(pass)) picked.push(pass);
  return picked;
}

/** How many options each side examines, by remaining depth. */
const SEARCH_WIDTH = { 2: 6, 1: 4 }, ROOT_WIDTH = { n: 8 };

/**
 * Minimax over the next plies (each side's best option, alternating). Every line is judged at the
 * same moment: this round's end (as the eye resolves it), seen as the next round would begin. A line
 * where both sides pass stops there instead of handing the next round's first player a free,
 * unanswered action, which made passing look worse than any action and led to wasted supply.
 */
function search(t, p, depth, alpha = -Infinity, beta = Infinity) {
  // alpha-beta pruning: a value inside [alpha, beta] is exact; outside it, only a bound (true value at most / at
  // least it) is returned, because the caller will not choose that line anyway. The choice is the same as the full
  // search, with fewer positions examined.
  if (t.winner !== null || depth === 0 || t.roundOver) return evaluateOutcome(t, p);
  const mine = t.cur === p;
  let best = mine ? -Infinity : Infinity;
  for (const option of promisingReplies(t, t.cur, SEARCH_WIDTH[depth])) {
    if (mine) {
      const v = search(option.t, p, depth - 1, Math.max(alpha, best), beta);
      if (v > best) best = v;
      if (best > beta) return best;                 // the opponent will avoid this line
    } else {
      const v = search(option.t, p, depth - 1, alpha, Math.min(beta, best));
      if (v < best) best = v;
      if (best < alpha) return best;                // worse than an option already found
    }
  }
  return best;
}


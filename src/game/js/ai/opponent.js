/* =====================================================================
   COMPUTER OPPONENT
   ===================================================================== */

/** A lane the side owns with no enemy units in it. */
const isSafeLane = (s, side, lane) => s.owner[lane] === side && !s.units.some(u => u.owner !== side && u.lane === lane);

/** The position as the next round begins: this round resolved, the other side to start, lanes refilled. */
function nextRoundView(s) {
  const t = s.roundOver ? cloneState(s) : forecastRoundEnd(s);
  if (t.winner !== null) return t;
  t.carried = [t.players[0].reserve, t.players[1].reserve];
  t.roundOver = false;
  t.ownerStart = t.owner.slice();
  t.round++;
  t.starter = other(t.starter);
  Object.assign(t, { cur: t.starter, passed: null, acts: 0 });
  for (const u of t.units) { u.moved = false; u.attacked = false; }
  for (const p of [0, 1]) for (const lane of LANES) t.pool[p][lane] = t.poolStart[p][lane] = laneSupply(t, p, lane);
  return t;
}

/** Supply an action spends: used to prefer the cheaper of two equally good options. */
function actionCost(s, a) {
  if (a.t === 'pass') return 0;
  const hand = s.players[s.cur].hand;
  if (a.t === 'deploy') return CARDS[hand[a.hi]].cost;
  if (a.t === 'move') return moveCost(byId(s, a.id));
  return attackCost(byId(s, a.id));
}

/** What the round would come to if both sides passed now, as seen by side p (key + p's own stats). */
function outcomeOf(s, p) {
  const t = forecastRoundEnd(s), stats = {};
  const dotCounts = l => { const d = dotState(t, l); return [0, 1, 'x'].map(k => d.filter(x => x === k).length); };
  for (const u of t.units) if (u.owner === p) stats[u.id] = [strengthOf(u), defenceOf(u)];
  const key = JSON.stringify([t.winner, t.owner, LANES.map(dotCounts), t.players.map(P => P.hand.length),
    t.units.map(u => u.owner === p ? [u.id, u.lane] : [u.id, u.lane, strengthOf(u), defenceOf(u)]).sort((x, y) => x[0] - y[0])]);
  return { key, stats };
}

/** Attacks side p's units could make (ignoring supply): who hits whom, and how hard. */
function attackOptions(s, p) {
  const out = new Set();
  for (const a of s.units) {
    if (a.owner !== p || a.attacked || strengthOf(a) <= 0) continue;
    for (const t of unitsIn(s, other(p), a.lane))
      if (reaches(a, t)) out.add(a.id + '>' + t.id + ':' + strengthOf(a));
  }
  return out;
}

/**
 * A pointless action spends supply, yet does not change how the round turns out (same resolution as the eye)
 * except by lowering its own units' stats, and opens no new or stronger attack. Deploys are never pointless.
 */
function isPointless(s, a, t, now) {
  if (a.t === 'pass' || a.t === 'deploy') return false;
  const p = s.cur;
  if (t.roundOver || t.winner !== null || actionCost(s, a) <= 0) return false;
  const after = outcomeOf(t, p);
  if (after.key !== now.key) return false;
  for (const id in after.stats) {
    const [a1, d1] = after.stats[id], [a0, d0] = now.stats[id] || [0, 0];
    if (a1 > a0 || d1 > d0) return false;
  }
  const before = attackOptions(s, p);
  for (const k of attackOptions(t, p)) if (!before.has(k)) return false;
  return true;
}

/** The game's computer opponent: the Benchmark (sees the opponent's hand). */

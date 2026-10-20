/* =====================================================================
   COMPUTER OPPONENT
   ===================================================================== */

/** A lane the side owns with no enemy units in it. */
const isSafeLane = (s, side, lane) => s.owner[lane] === side && !s.units.some(u => ctl(u) !== side && u.lane === lane);

/** The position as the next round begins: this round resolved, the other side to start, lanes refilled. */
function nextRoundView(s) {
  const t = s.roundOver ? cloneState(s) : forecastRoundEnd(s);
  if (t.winner !== null) return t;
  t.carried = [t.players[0].reserve, t.players[1].reserve];
  t.roundOver = false;
  t.ownerStart = t.owner.slice();
  t.round++;
  t.starter = other(t.starter);
  Object.assign(t, { cur: t.starter, passed: null, acts: 0, pending: null });
  for (const u of t.units) { u.moved = false; u.attacked = false; u.atk = 0; u.mv = 0; u.armUsed = false; }
  for (const p of [0, 1]) for (const lane of LANES) t.pool[p][lane] = t.poolStart[p][lane] = laneSupply(t, p, lane);
  return t;
}

/** Supply an action spends: used to prefer the cheaper of two equally good options. */
function actionCost(s, a) {
  if (a.t === 'pass' || PENDING_STEPS.has(a.t)) return 0;
  const hand = s.players[s.cur].hand;
  if (a.t === 'deploy') return CARDS[hand[a.hi]].cost;
  if (a.t === 'tactic') return spellCost(s, hand[a.hi], a);
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
    if (ctl(a) !== p || a.attacked || strengthOf(a) <= 0) continue;
    for (const t of unitsIn(s, other(p), a.lane))
      if (reaches(a, t)) out.add(a.id + '>' + t.id + ':' + strengthOf(a));
  }
  return out;
}

/**
 * A pointless action spends supply, yet does not change how the round turns out (same resolution as the eye)
 * except by lowering its own units' stats, and opens no new or stronger attack. Deploys and follow-up steps are never pointless.
 */
/** What a spell can change, apart from the card leaving the hand and its cost being paid. */
function spellSig(s, p, handDelta, paid) {
  const P = s.players[p], Q = s.players[other(p)];
  return JSON.stringify([s.units.map(u => [u.card, u.lane, u.r, u.c, u.o, u.owner, u.ctl, strengthOf(u), defenceOf(u), u.kw, u.off, u.tInc, u.tArm, u.blight, u.ps, u.pd, u.ts]),
    s.owner, P.hand.length + handDelta, P.draw.length, P.discard.length - handDelta, Q.hand.length, Q.draw.length, Q.discard.length,
    s.pool[p].reduce((a, b) => a + b, 0) + P.reserve + paid, P.breath, P.veil]);
}
/** A spell that changes nothing on the board, in the hands, decks or supply (beyond its own card and cost). */
function spellDoesNothing(s, a, t) {
  if (a.t !== 'tactic' || t.pending) return false;
  return spellSig(s, s.cur, 0, 0) === spellSig(t, s.cur, 1, actionCost(s, a));
}
/** Finish a pending free-move choice (Reform Ranks, Mandator) without more moves. */
function finishFree(t) { while (t.pending && t.pending.k === 'free') applyAction(t, { t: 'done' }); return t; }
/** How the round would end for side p from t, by the computer's judgement (no moves left to make in t). */
const roundValue = (t, p, c) => ifelseEval(nextRoundView(t), p, null, c);
/** Free moves (Reform Ranks, Mandator): whether at least one of the moves on offer in t leads to a better round than making none. */
function freeMovesHelp(s, t, c) {
  const p = s.cur, none = roundValue(finishFree(cloneState(t)), p, c);
  for (const m of listActions(t)) {
    if (m.t !== 'fmove') continue;
    const t2 = cloneState(t);
    t2.noFx = true;
    applyAction(t2, m);
    finishFree(t2);
    if (!t2.pending && roundValue(t2, p, c) > none + 1e-6) return true;
  }
  return false;
}
function isPointless(s, a, t, now, c) {
  if (spellDoesNothing(s, a, t)) return true;
  // Reform Ranks (and any spell that opens free moves): pointless unless one of its moves makes the round better
  if (c && c.freeCheck && a.t === 'tactic' && t.pending && t.pending.k === 'free') return !freeMovesHelp(s, t, c);
  // a free move that doesn't make the round better than stopping now (e.g. there and back again) is skipped
  if (c && c.freeCheck && a.t === 'fmove' && s.pending && s.pending.k === 'free') {
    const base = finishFree(cloneState(s)), t2 = finishFree(cloneState(t));
    return t2.pending || roundValue(t2, s.cur, c) <= roundValue(base, s.cur, c) + 1e-6;
  }
  // a unit whose worth is its Place pick (Blood-Letter) isn't placed when the pick has no target
  if (a.t === 'deploy' && CARDS[s.players[s.cur].hand[a.hi]].needsPick && !t.pending) return true;
  if (a.t === 'pass' || a.t === 'deploy' || PENDING_STEPS.has(a.t)) return false;
  if (t.pending) return false;                       // the action's effect is still to be chosen
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

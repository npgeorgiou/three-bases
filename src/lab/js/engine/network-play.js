/* ---------- the network ---------- */

function gaussian() {
  let u = 0, v = 0;
  while (!u) u = Math.random();
  while (!v) v = Math.random();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

/** A saved network (plain data) back into a working network. Only format 3 exists now. */
function netFromData(data) {
  if (data && data.enc === 3) return net3FromData(data);
  throw new Error('This network was made for an older version of the lab and cannot be used.');
}

/* ---------- choosing a move ---------- */

/** Every legal move applied once to a copy (every placement counts). */
function netOptions(t) {
  return listActions(t).map(a => {
    const n = cloneState(t);
    applyAction(n, a);
    return { a, t: n };
  });
}

/** How good a position is for `me` by the network (1 = certain win); a finished game by its result. */
function netJudge(net, t, me) {
  const result = x => (x.winner === me ? 1 : x.winner === 'draw' ? 0.5 : 0);
  if (t.winner !== null) return result(t);
  const v = t.roundOver ? nextRoundView(t) : t;
  if (v.winner !== null) return result(v);
  const p = 1 / (1 + Math.exp(-(net.valueOf ? net.valueOf(v, v.cur) : net.value(encode3(v, v.cur)))));
  return v.cur === me ? p : 1 - p;
}

/**
 * The network player's move, and whether it was a random one. cfg.replies: also check the opponent's best
 * reply to its top cfg.width moves; cfg.explore: chance of a random move instead (training only).
 */
function chooseNetActionEx(s, net, cfg = { replies: true, width: 8, explore: 0 }) {
  if (cfg.search) {
    if (cfg.explore && Math.random() < cfg.explore) return { a: randomMove(netOptions(sampledView(s, s.cur))).a, random: true };
    return { a: chooseNetSearchAction(s, net, cfg.guess), random: false };
  }
  const me = s.cur, t = sampledView(s, me);
  t.stopAtRoundEnd = true;
  const options = netOptions(t);
  if (cfg.explore && Math.random() < cfg.explore) return { a: randomMove(options).a, random: true };
  for (const o of options) o.v = netJudge(net, o.t, me);
  options.sort((a, b) => b.v - a.v);
  let pool = options;
  if (cfg.replies) {
    pool = options.slice(0, cfg.width || 8);
    for (const o of pool) {
      if (o.t.winner !== null || o.t.roundOver || o.t.cur === me) continue;
      let worst = Infinity;
      for (const r of netOptions(o.t)) worst = Math.min(worst, netJudge(net, r.t, me));
      o.v = worst;
    }
  }
  let best = null;
  for (const o of pool) {
    const cost = actionCost(t, o.a);
    if (!best || o.v > best.v + 1e-9 || (Math.abs(o.v - best.v) <= 1e-9 && cost < best.cost)) best = { a: o.a, v: o.v, cost };
  }
  return { a: best.a, random: false, v: best.v };
}
const chooseNetAction = (s, net, cfg) => chooseNetActionEx(s, net, cfg).a;

/**
 * The network with the earlier Benchmark's search: exactly its look-ahead (its move, the opponent's replies,
 * its answers, with the same widths, the same skipping of pointless actions, and the opponent's actual hand), but
 * every position along the way is scored by the network instead of the Benchmark's hand-written score.
 */
function chooseNetSearchAction(s, net, guess = false) {
  const p = s.cur, root = guess ? sampledView(s, p) : cloneState(s);   // guess: a random possible opponent hand instead of the real one
  root.noFx = true;
  root.stopAtRoundEnd = true;
  const now = outcomeOf(root, p);
  const replies = (t, side, limit, keep) => {
    const scored = listActions(t).map(a => {
      const n = cloneState(t);
      applyAction(n, a);
      return { a, t: n, v: netJudge(net, n, side) };
    }).filter(x => !keep || keep(x.a, x.t)).sort((x, y) => y.v - x.v);
    const picked = scored.slice(0, limit), pass = scored.find(x => x.a.t === 'pass');
    if (pass && !picked.includes(pass)) picked.push(pass);
    return picked;
  };
  const search = (t, depth, alpha = -Infinity, beta = Infinity) => {   // alpha-beta pruning, as in the Benchmark's search
    if (t.winner !== null || depth === 0 || t.roundOver) return netJudge(net, t, p);
    const mine = t.cur === p;
    let best = mine ? -Infinity : Infinity;
    for (const o of replies(t, t.cur, SEARCH_WIDTH[depth])) {
      if (mine) {
        const v = search(o.t, depth - 1, Math.max(alpha, best), beta);
        if (v > best) best = v;
        if (best > beta) return best;
      } else {
        const v = search(o.t, depth - 1, alpha, Math.min(beta, best));
        if (v < best) best = v;
        if (best < alpha) return best;
      }
    }
    return best;
  };
  let best = null;
  for (const o of replies(root, p, ROOT_WIDTH.n, (a, t) => !isPointless(root, a, t, now))) {
    const value = search(o.t, 2, best ? best.value - 2e-9 : -Infinity), cost = actionCost(root, o.a);
    if (!best || value > best.value + 1e-9 || (Math.abs(value - best.value) <= 1e-9 && cost < best.cost))
      best = { a: o.a, value, cost };
  }
  return best.a;
}

/**
 * A learning AI's redraw, judged by its network. The network scores the opening position as the player sees it
 * (the opponent's hand guessed, as if this player moved first, so all choices are scored alike). For each dealt
 * card not yet redrawn it works out the redraw's expected score: every different card in the deck could arrive,
 * with chance (its copies / deck size), and the network scores the opening with that card in its place; the
 * chance-weighted average is the chance of winning after that redraw. If the best card's expected score beats
 * the current one, that card is redrawn for real; then the whole check is repeated, at most 3 redraws.
 */
function netRedraw(s, p, net) {
  const score = v => { const q = 1 / (1 + Math.exp(-net.value(encode3(v, p)))); return q; };
  const used = new Set();
  for (let round = 0; round < MAX_REDRAW; round++) {
    const view = sampledView(s, p);
    view.cur = p; view.starter = p;
    const P = view.players[p], hand = P.hand, deck = P.draw, now = score(view);
    const counts = {};
    for (const k of deck) counts[k] = (counts[k] || 0) + 1;
    let best = null;
    hand.forEach((out, i) => {
      if (used.has(i)) return;
      let expected = 0;
      P.redrawn.push(out);
      for (const [into, n] of Object.entries(counts)) {
        hand[i] = into;
        const at = deck.indexOf(into);
        deck[at] = out;                                   // the redrawn card goes back into the deck, the new one leaves it
        expected += (n / deck.length) * score(view);
        deck[at] = into;
      }
      hand[i] = out;
      P.redrawn.pop();
      if (!best || expected > best.expected) best = { i, expected };
    });
    if (!best || best.expected <= now) return;
    redraw(s, p, best.i);
    used.add(best.i);
    if (s.players[p].redrawn.length >= MAX_REDRAW) return;
  }
}



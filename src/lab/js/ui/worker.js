/* =====================================================================
   Worker code: plays games and trains. Runs in each worker, after the engine.
   ===================================================================== */
function labWorker() {
  const nets = {};

  /** A player's move: { a: the action, random: whether it was a random exploring move }. */
  function choose(spec, s) {
    if (spec.kind === 'bench') return { a: chooseIfelseAction(s, spec.depth ? { ...BENCH_VALUES, depth: spec.depth } : BENCH_VALUES), random: false };
    if (spec.kind === 'ifelse') return { a: chooseIfelseAction(s, spec.cfg), random: false };
    if (spec.kind === 'random') return { a: randomMove(listActions(s).map(a => ({ a }))).a, random: false };
    return chooseNetActionEx(s, nets[spec.net], spec.play);
  }

  /**
   * One game. With `record`, every position is saved as the player about to act saw it, labelled with how
   * the game ended for that player: 1 won, 0.5 drawn, 0 lost. A game the lab stopped as too long is not
   * learned from. D marks the games one side won, used to measure how well the winner is predicted.
   */
  /** A game with a seed deals the same shuffles (and the same chance events) every time it is played. */
  let lessonList = [];
  function playGame(msg) {
    if (msg.seed == null) return playGameAs(msg);
    const real = Math.random;
    let z = msg.seed >>> 0;
    Math.random = () => { z = (z + 0x6D2B79F5) >>> 0; let t = Math.imul(z ^ (z >>> 15), z | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    try { return playGameAs(msg); } finally { Math.random = real; }
  }
  function playGameAs(msg) {
    for (const [key, d] of Object.entries(msg.lists || {})) labDeck(key, d.name, d.fac, d.list);   // decks made in the lab
    const { specs, decks, record } = msg, replay = msg.replay ? JSON.parse(msg.replay.actions) : null;
    const s = msg.replay ? JSON.parse(msg.replay.init) : newGame(decks[0], decks[1]);   // a library game: its board after the redraws
    s.noFx = true;
    // the starting-hand redraw, each side on its own (neither knows the other's until the battle begins)
    if (!replay) for (const p of [0, 1]) {
      const sp = specs[p];
      if (sp.kind === 'net') netRedraw(s, p, nets[sp.net]);
      else if (sp.kind === 'random') randomRedraw(s, p);
      else aiMulligan(s, p);
    }
    s.redrawDone = true;
    const xs = [], sides = [], states = [], sv = [], time = [0, 0], moves = [0, 0];
    let randoms = 0;
    const played = [[], []];
    let asked = 0, same = 0;                                          // the cards each side played, for the card statistics
    for (let i = 0; i < msg.actionCap && s.winner === null && s.round <= msg.roundCap; i++) {
      const side = s.cur;
      if (record) { xs.push(encode3(s, side)); sides.push(side); states.push(cloneState(s)); sv.push(null); }
      const spec = specs[side], t0 = performance.now();
      let c;
      if (replay) { if (i >= replay.length) break; c = { a: replay[i], random: false }; }   // the library game's next move
      else c = choose(spec, s);
      time[side] += performance.now() - t0; moves[side]++;
      if (msg.agree && !s.pending) { asked++; if (JSON.stringify(choose(specs[1 - side], s).a) === JSON.stringify(c.a)) same++; }   // would the other AI play the same?
      if (record && msg.search > 0 && spec.kind === 'net' && spec.net === 'train' && spec.play && spec.play.replies && !c.random && Number.isFinite(c.v)) sv[sv.length - 1] = c.v;   // its search's value of this position
      if (c.random) randoms++;
      if ((c.a.t === 'deploy' || c.a.t === 'tactic') && s.players[side].hand[c.a.hi]) played[side].push(s.players[side].hand[c.a.hi]);
      applyAction(s, c.a);
    }
    const out = { type: 'game', key: msg.key, winner: s.winner === null ? 'none' : s.winner, rounds: s.round, randoms, played, asked, same,
      ms: [time[0] / Math.max(1, moves[0]), time[1] / Math.max(1, moves[1])] };
    // a game the lab stopped (too long) teaches nothing: the rules do not say how it ends
    if (record && xs.length && s.winner !== null) {
      const n = xs.length, R = F3.RECN, NK = F3.NK, X = new Float32Array(n * R), K = new Uint16Array(n * NK), D = new Uint8Array(n);
      const decided = s.winner === 0 || s.winner === 1;
      const result = i => (s.winner === sides[i] ? 1 : s.winner === 'draw' ? 0.5 : 0);
      xs.forEach((x, i) => { X.set(x.nums, i * R); K.set(x.cards, i * NK); D[i] = decided ? 1 : 0; });
      // targets: the real result; with "search in training", positions where the trained network chose its move by
      // search learn partly that search's value: (1 - share) × result + share × value. One target serves every network
      // being trained (the size check's learn the same ones).
      // With the lessons check, one target per network: from the last position back, target = (1 - next) × the next
      // position's target + next × that network's own win chance there, both as seen by the side to act here.
      const share = msg.search || 0, lessons = msg.next || [{ net: null, share: 0 }], nY = lessons.length, Y = new Float32Array(n * nY);
      lessons.forEach((L, j) => {
        const net = L.share > 0 ? nets[L.net] : null;
        const v = net ? xs.map(x => 1 / (1 + Math.exp(-net.value(x)))) : null;
        let later = null;
        for (let i = n - 1; i >= 0; i--) {
          let y = result(i);
          if (net && i < n - 1) { const flip = q => (sides[i + 1] === sides[i] ? q : 1 - q); y = (1 - L.share) * flip(later) + L.share * flip(v[i + 1]); }
          later = y;
          Y[i * nY + j] = share > 0 && sv[i] !== null ? (1 - share) * y + share * sv[i] : y;
        }
      });
      // the exam: in a game one side won, up to 24 positions are marked (E = 1 + stage: 0 early, 1 middle, 2 late,
      // by thirds of the game); the learner grades the network on them, and the Benchmark's own guess is graded
      // here (it guesses a win when its score of the position, as the round would end, is above zero)
      const E = new Uint8Array(n), bench = [[0, 0], [0, 0], [0, 0]];
      if (decided) {
        const idx = [...Array(n).keys()];
        shuffle(idx);
        for (const i of idx.slice(0, 24)) {
          const stage = Math.min(2, Math.floor(3 * i / n));
          E[i] = 1 + stage;
          bench[stage][1]++;
          if ((evaluateOutcome(states[i], sides[i]) > 0) === (s.winner === sides[i])) bench[stage][0]++;
        }
      }
      out.X = X; out.K = K; out.Y = Y; out.D = D; out.E = E; out.bench = bench;
      self.postMessage(out, [X, K, Y, D, E].map(a => a.buffer));
    } else self.postMessage(out);
  }

  /* ---------- learning (in the learner workers only) ----------
     A training network has one or more learners (the page adds and removes them as needed). Each learner holds
     its own share of the waiting lessons: a position and its target (how the game ended for the side to act there,
     partly the search's value with "search in training"), one target per network.
     The lead learner runs the steps: for each step it draws up to 64 lessons per learner at random from all waiting
     lessons together (so the batch is the same as if one learner held them all), asks each learner to work out the
     gradient of the ones it holds, adds the answers up and updates the networks.
     The lead's networks are the ones that are reported and saved (with their learning momentum).
     With the size check on, every learner also holds the check's networks; each step draws its lessons once and
     every network learns from exactly those lessons. With mirroring on, each time a lesson is used it is, at
     random half of the time, learned with lanes 1 and 3 swapped. */
  const BATCH = 64;                               // lessons per learning step, per learner
  const START_AT = 256;                           // learning starts once this many lessons are waiting (all learners together)
  const MAX_SLOTS = 60000;                        // hard ceiling per learner (the page pauses new games long before this)
  let T = null;

  /* --- the store of waiting lessons: fixed-size records in growable arrays, each with its remaining uses --- */
  function makeStore(fields, max, start) {
    const st = { fields: Object.entries(fields), max, cap: 0, arr: {}, left: null, where: null, free: [], active: [], dropped: 0, used: 0, retired: 0 };
    grow(st, start);
    return st;
  }
  function grow(st, cap) {
    for (const [k, [Type, per]] of st.fields) { const a = new Type(cap * per); if (st.arr[k]) a.set(st.arr[k]); st.arr[k] = a; }
    const left = new Uint16Array(cap), where = new Int32Array(cap);
    if (st.left) { left.set(st.left); where.set(st.where); }
    for (let i = cap - 1; i >= st.cap; i--) st.free.push(i);
    Object.assign(st, { left, where, cap });
  }
  /** Record i of the arrays in `src` (laid out like the store's fields) joins the store with `uses` uses. */
  function storeAdd(st, src, i, uses) {
    if (!st.free.length) {
      if (st.cap >= st.max) { st.dropped++; return; }
      grow(st, Math.min(st.max, st.cap * 2));
    }
    const slot = st.free.pop();
    for (const [k, [, per]] of st.fields) st.arr[k].set(src[k].subarray(i * per, (i + 1) * per), slot * per);
    st.left[slot] = uses;
    st.where[slot] = st.active.length;
    st.active.push(slot);
  }
  function storeRetire(st, slot) {
    const j = st.where[slot], last = st.active.pop();
    if (last !== slot) { st.active[j] = last; st.where[last] = j; }
    st.free.push(slot);
    st.retired++;
  }
  function storePick(st, k) {
    const n = st.active.length, chosen = new Set();
    k = Math.min(k, n);
    while (chosen.size < k) chosen.add(Math.floor(Math.random() * n));
    return [...chosen].map(j => st.active[j]);
  }
  function storeUse(st, slots) { for (const slot of slots) if (--st.left[slot] === 0) storeRetire(st, slot); st.used += slots.length; }
  /** Everything waiting in a store, as arrays (for a handover); the store is left empty. */
  function storeDump(st) { return storeTake(st, st.active.length); }
  /** The last `count` waiting lessons of a store, as arrays; they leave the store (keeping their remaining uses). */
  function storeTake(st, count) {
    const slots = st.active.splice(st.active.length - count, count), out = { left: new Uint16Array(count) };
    for (const [k, [Type, per]] of st.fields) out[k] = new Type(count * per);
    slots.forEach((slot, i) => {
      for (const [k, [, per]] of st.fields) out[k].set(st.arr[k].subarray(slot * per, (slot + 1) * per), i * per);
      out.left[i] = st.left[slot];
      st.free.push(slot);
    });
    return out;
  }
  const dumpBuffers = d => Object.values(d).map(a => a.buffer);

  function trainStart(msg) {
    const datas = Array.isArray(msg.data) ? msg.data : [msg.data];
    const nets = datas.map(d => net3FromData(d, true));                // learning networks: with gradient and momentum
    for (const E of nets) Object.assign(E, { loss: null, fit: null });
    nets.forEach((E, n) => { E.rate = (msg.rates && msg.rates[n]) || 0.0005; });   // each network's own step size
    T = { nets, uses: msg.uses, lead: msg.lead, mirror: msg.mirror !== false, recvV: 0,
      v: makeStore({ X: [Float32Array, F3.RECN], K: [Uint16Array, F3.NK], Y: [Float32Array, nets.length], D: [Uint8Array, 1] }, MAX_SLOTS, 2048),
      running: true, retiredMode: false, sinceReport: 0, sinceStatus: 0 };
    if (T.lead) {
      Object.assign(T, { members: [], waiting: 0, round: null });
      setTimeout(round, 0);
    } else {
      T.port = msg.port;
      T.port.onmessage = e => onLeadMessage(e.data);
    }
  }

  /** A running score in which each new answer counts 0.5%. */
  const blendScore = (score, hits, tries) => {
    if (!tries) return score;
    const f = Math.pow(0.995, tries), rate = hits / tries;
    return score === null ? rate : f * score + (1 - f) * rate;
  };

  /** Network E's raw output for record i of the arrays X/K (kept for backward). */
  function forward(E, X, K, i, mirror) { E.load(0, X, K, i, mirror); return E.x.forward(0); }

  /**
   * Draws k of this learner's lessons at random, and for every network adds their gradient (each weighted 1/K) to
   * its own gradient. Returns, per network, the summed loss and its score on these lessons.
   */
  function gradient(k, K) {
    const st = T.v, slots = storePick(st, k), nY = T.nets.length;
    const flips = slots.map(() => T.mirror && Math.random() < 0.5);
    const res = T.nets.map((E, n) => {
      let loss = 0, fitHits = 0, fitTries = 0;
      slots.forEach((slot, s) => {
        const y = st.arr.Y[slot * nY + n], p = 1 / (1 + Math.exp(-forward(E, st.arr.X, st.arr.K, slot, flips[s])));
        loss += -(y * Math.log(p + 1e-7) + (1 - y) * Math.log(1 - p + 1e-7));
        if (st.arr.D[slot]) { fitTries++; if ((p > 0.5) === (y > 0.5)) fitHits++; }   // on lessons it is learning from
        E.x.backward(0, (p - y) / K);
      });
      return { loss, fitHits, fitTries };
    });
    storeUse(st, slots);
    return res;
  }

  /** A finished game's lessons arrive. First the networks are tested on them (an honest exam, nothing is learned), then they wait to be learned from. */
  function addData(msg) {
    const { X, K, Y, D, E } = msg, n = D.length, nY = Y.length / n;
    // the exam: every learner grades the positions the game marked, with its copy of the networks (at most one
    // step old), and reports right/wrong counts per stage of the game; the page keeps one combined score
    const stages = [[0, 0], [0, 0], [0, 0]], each = T.nets.map(() => [0, 0]);
    for (let i = 0; i < n; i++) {
      if (!E[i]) continue;
      T.nets.forEach((net, j) => {
        const p = 1 / (1 + Math.exp(-forward(net, X, K, i, false))), hit = (p > 0.5) === (Y[i * nY] > 0.5);
        each[j][1]++; if (hit) each[j][0]++;
        if (j === 0) { const st = stages[E[i] - 1]; st[1]++; if (hit) st[0]++; }
      });
    }
    if (stages.some(st => st[1])) self.postMessage({ type: 'exam', stages, each });
    // one target per network; fewer given: the first is shared
    const nets = T.nets.length, Yn = new Float32Array(n * nets);
    for (let i = 0; i < n; i++) for (let j = 0; j < nets; j++) Yn[i * nets + j] = Y[i * nY + Math.min(j, nY - 1)];
    T.recvV += n;                                                    // so the page knows what is still on its way here
    for (let i = 0; i < n; i++) storeAdd(T.v, { X, K, Y: Yn, D }, i, T.uses);
    counted();
  }
  function addHandover(msg) {
    T.recvV += msg.v.left.length;
    for (let i = 0; i < msg.v.left.length; i++) storeAdd(T.v, msg.v, i, msg.v.left[i]);
    counted();
  }
  function counted() {
    if (!T.lead && T.port && !T.retiredMode) T.port.postMessage({ type: 'n', n: T.v.active.length });
    status();
  }
  function status() {
    const E0 = T.nets[0];
    self.postMessage({ type: 'status', pending: T.v.active.length, steps: E0.step, learned: T.learned || 0,
      loss: E0.loss, fit: E0.fit, fits: T.nets.map(E => E.fit), losses: T.nets.map(E => E.loss),
      dropped: T.v.dropped, used: T.v.used, retired: T.v.retired, recvV: T.recvV });
  }
  function report(final) {
    if (!T.lead) return;
    const datas = T.nets.map(E => net3ToData(E, true));                // with the learning momentum
    self.postMessage({ type: final ? 'final' : 'weights', data: datas[0], datas, steps: T.nets[0].step, loss: T.nets[0].loss });
  }

  /* --- the lead: runs the steps --- */
  function share(counts, K) {
    const total = counts.reduce((a, b) => a + b, 0), pick = new Set(), ks = counts.map(() => 0);
    while (pick.size < K) pick.add(Math.floor(Math.random() * total));
    for (let r of pick) { let i = 0; while (r >= counts[i]) { r -= counts[i]; i++; } ks[i]++; }
    return ks;
  }
  function round() {
    if (!T || !T.running || T.waiting) return;
    for (const mb of T.members.filter(x => x.leaving)) {
      T.members.splice(T.members.indexOf(mb), 1);
      mb.port.postMessage({ type: 'retire' });
    }
    const vc = [T.v.active.length, ...T.members.map(x => x.n)], vt = vc.reduce((a, b) => a + b, 0);
    if (vt < START_AT) {
      status();
      setTimeout(round, 100);
      return;
    }
    const learners = 1 + T.members.length, K = Math.min(Math.max(2, learners) * BATCH, vt), kv = share(vc, K);
    T.learned = (T.learned || 0) + K;
    for (const E of T.nets) E.x.zeroGrad();
    T.round = { K, nets: T.nets.map(() => ({ loss: 0, fitHits: 0, fitTries: 0 })) };
    T.waiting = 0;
    T.members.forEach((mb, i) => {
      const a = kv[i + 1];
      if (!a) return;
      mb.n -= a;
      T.waiting++;
      // copies of exactly the weights: a view would carry the whole shared memory block along with it
      mb.port.postMessage({ type: 'work', kv: a, K, weights: T.nets.map(E => E.w.slice()) });
    });
    const w = kv[0] ? gradient(kv[0], K) : null;
    if (w) T.round.nets.forEach((r, n) => { r.loss += w[n].loss; r.fitHits += w[n].fitHits; r.fitTries += w[n].fitTries; });
    if (!T.waiting) finishStep();
  }
  function onMemberMessage(mb, msg) {
    if (msg.type === 'n') { mb.n = msg.n; return; }
    if (msg.type !== 'grad') return;
    mb.n = msg.n;
    T.nets.forEach((E, n) => {
      E.r.set(msg.grads[n]); E.x.addReceived();
      const r = T.round.nets[n], x = msg.stats[n];
      r.loss += x.loss; r.fitHits += x.fitHits; r.fitTries += x.fitTries;
    });
    if (--T.waiting === 0 && T.running) finishStep();
  }
  /** Adam update (momentum and RMSprop) of every network with its combined gradient. */
  function finishStep() {
    const { K } = T.round;
    T.nets.forEach((E, n) => {
      const r = T.round.nets[n];
      E.step++;
      E.x.adam(E.step, E.rate);
      if (K) { const loss = r.loss / K; E.loss = E.loss === null ? loss : 0.98 * E.loss + 0.02 * loss; }
      E.fit = blendScore(E.fit, r.fitHits, r.fitTries);
    });
    if (++T.sinceReport >= 60) { T.sinceReport = 0; report(false); }
    if (++T.sinceStatus >= 8) { T.sinceStatus = 0; status(); }
    setTimeout(round, 0);
  }

  /* --- a member: works out gradients when the lead asks --- */
  function onLeadMessage(msg) {
    if (!T.running) return;
    if (msg.type === 'work') {
      T.nets.forEach((E, n) => { E.w.set(msg.weights[n]); E.x.zeroGrad(); });   // the lead's current networks
      const w = msg.kv ? gradient(msg.kv, msg.K) : null;
      const grads = T.nets.map(E => E.g.slice());
      const stats = T.nets.map((E, n) => ({ loss: w ? w[n].loss : 0, fitHits: w ? w[n].fitHits : 0, fitTries: w ? w[n].fitTries : 0 }));
      T.port.postMessage({ type: 'grad', grads, stats, n: T.v.active.length }, grads.map(g => g.buffer));
      if (++T.sinceStatus >= 8) { T.sinceStatus = 0; status(); }
    } else if (msg.type === 'retire') handOver();
  }
  function handOver() {
    T.retiredMode = true;
    const v = storeDump(T.v);
    self.postMessage({ type: 'handover', v }, dumpBuffers(v));
  }

  let netsError = '';
  self.onmessage = e => {
    const msg = e.data;
    if (msg.type === 'nets') {                                        // same kind of network: only the weights change
      for (const [id, data] of Object.entries(msg.nets)) {
        if (!data) continue;
        try { nets[id] = netNamed(id, data); }
        catch (err) { delete nets[id]; netsError = err.message; }     // the game that needs it will fail with this reason
      }
    }
    else if (msg.type === 'game') {
      for (const sp of msg.specs) if (sp.kind === 'net') if (!nets[sp.net]) throw new Error('network ' + sp.net + ' missing' + (netsError ? ': ' + netsError : ''));
      playGame(msg);
    }
    else if (msg.type === 'lessons') lessonList = msg.lessons;                    // the foresight lessons, for grading
    else if (msg.type === 'lessonMake') self.postMessage({ type: 'lessonMake', key: msg.key, lessons: lessonsFromGame(msg) });
    else if (msg.type === 'lessonGrade') self.postMessage({ type: 'lessonGrade', key: msg.key, ...gradeLessons(lessonList, msg.cfg, msg.from, msg.to) });
    else if (msg.type === 'trainStart') trainStart(msg);
    else if (msg.type === 'data') { addData(msg); if (T.retiredMode) handOver(); }
    else if (msg.type === 'handover') { addHandover(msg); if (T.retiredMode) handOver(); }
    else if (msg.type === 'bye') self.postMessage({ type: 'gone' });
    else if (msg.type === 'split') {
      if (!T || T.retiredMode) return;
      const v = storeTake(T.v, Math.floor(T.v.active.length / 2));
      self.postMessage({ type: 'handover', split: true, v }, dumpBuffers(v));
      counted();
    }
    else if (msg.type === 'join') {
      const mb = { id: msg.id, port: msg.port, n: 0, leaving: false };
      msg.port.onmessage = ev => onMemberMessage(mb, ev.data);
      T.members.push(mb);
    }
    else if (msg.type === 'leave') { const mb = T.members.find(x => x.id === msg.id); if (mb) mb.leaving = true; }
    else if (msg.type === 'rate') { if (T) T.nets.forEach((E, n) => { if (msg.rates[n]) E.rate = msg.rates[n]; }); }
    else if (msg.type === 'mirror') { if (T) T.mirror = msg.on; }
    else if (msg.type === 'uses') { if (T) T.uses = msg.uses; }                   // for lessons arriving from now on
    else if (msg.type === 'stop') { if (T) { T.running = false; report(true); } }
  };
}

/** The worker program: the decks saved for the game (workers have no browser store), the game engine, the worker code above. */
const workerSource = () => 'self.PREMADE_SAVED_DATA = ' + JSON.stringify(PREMADE_SAVED) + ';\n' + $('#engine').textContent + '\n(' + labWorker.toString() + ')();';
let workerUrl = null;
function newWorker() {
  if (!workerUrl) workerUrl = URL.createObjectURL(new Blob([workerSource()], { type: 'text/javascript' }));
  return new Worker(workerUrl);
}


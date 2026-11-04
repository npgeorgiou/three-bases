/* =====================================================================
   LEARNING AI: a neural network that judges positions

   The network sees a position through the eyes of the player about to act, as numbers (listed
   below), and outputs one number: the chance that this player goes on to win. It learns only from
   the results of games (training lives in the AI lab page). The game rules still decide which moves
   are legal and when a game is won; no strategy is written here.

   Choosing a move: every legal move is tried on a copy of the game and the network is asked how
   good the result is; when playing for real it also checks the opponent's best reply to its most
   promising moves. The opponent's hand is never looked at: it gets a random possible hand.
   ===================================================================== */

/** Every card, in a fixed order: the row of its printed values in the network's table (no weights belong to a card). */
const NET_CARD_KEYS = Object.keys(CARDS).sort();
const NET_CARD_INDEX = Object.fromEntries(NET_CARD_KEYS.map((k, i) => [k, i]));

/**
 * What a card is and does, by name, with no card names: its numbers and keywords (cost, size, strength, defence,
 * Geared ...), and its effects in parts: when + what ("roundEnd:strike"), what + on whom ("strike>nearest"), with
 * amounts; auras ("aura:s", "aura>adj") and spells ("cast:dmg"). A reworked card is a new mix of known parts;
 * only a word no card had before is new to the network.
 */
const NET_SKIP = new Set(['name', 'fac', 'art', 'text', 'net', 'fx', 'aura', 'cast', 'champion']);
function cardFeatures(c) {
  const f = new Map(), add = (k, v) => { if (v) f.set(k, (f.get(k) || 0) + v); };
  const val = v => (v === true ? 1 : typeof v === 'number' ? Math.abs(v) : v ? 1 : 0);
  for (const [k, v] of Object.entries(c)) {
    if (NET_SKIP.has(k) || typeof v === 'string') continue;
    if (v && typeof v === 'object' && !Array.isArray(v)) { for (const [sk, sv] of Object.entries(v)) add(k + '.' + sk, val(sv)); }
    else add(k, val(v));
  }
  const ops = (when, list) => {
    for (const op of list || []) {
      const to = typeof op.to === 'string' ? op.to : 'self';
      for (const [k, v] of Object.entries(op)) {
        if (k === 'to' || k === 'if') continue;
        if (k === 'kw' && typeof v === 'string') add(when + ':kw:' + v, 1);
        else if (v && typeof v === 'object' && !('count' in v)) for (const [sk, sv] of Object.entries(v)) add(when + ':' + k + '.' + sk, val(sv));
        else add(when + ':' + k, val(v));
        add(k + '>' + to, 1);
      }
      if (op.if) add(when + ':if', 1);
    }
  };
  for (const e of c.fx || []) { ops(e.on, e.do); if (e.lim) add(e.on + ':once', 1); if (e.if || e.of) add(e.on + ':if', 1); }
  if (c.cast) { ops('cast', c.cast.do); if (c.cast.need) add('cast:need', 1); }
  for (const a of c.aura || []) { add('aura:s', val(a.s)); add('aura:d', val(a.d)); add('aura>' + (a.to || 'self'), 1); if (a.if) add('aura:if', 1); }
  return f;
}
const NET_FEATURES = NET_CARD_KEYS.map(k => cardFeatures(CARDS[k]));
const NET_PROPERTIES = [...new Set(NET_FEATURES.flatMap(m => [...m.keys()]))].sort();
/* ---------- network format 3 (version 7): cards by what they are and do, shared cell layer, hand slots, pile totals ----------
   A position is recorded as decimals (NUMS) and card numbers (CARDS: card + 1, 0 = none).
   NUMS: for each of the 54 cells (2 sides x 3 lanes x 3 rows from the front x 3 columns), 20 values:
     unit anchored here; its current strength, defence, damage, strength and defence build-up, temporary
     strength; moved; attacked; turned upright; cell covered by a unit anchored elsewhere; which of the 9 cells
     (row from the front x 3 + column) that anchor is.
   then per lane (3 x 17): the 3 dots (mine / theirs / crossed out), base owner (mine / theirs), supply left
     in the lane this round (mine / theirs), supply the lane started the round with (mine / theirs), lane supply
     (mine / theirs);
   per side (me, then them): carry-over / 5, hand size / 10, deck size, discard size;
   the game: round, I started the round, it is my turn, I passed, they passed, rounds in a row without any
     action / 3, actions this round, how many cards they redrew / 3 (known once the battle has begun);
   four piles: my deck, their unseen cards (hand and deck), my dealt starting hand, the cards I redrew (put back);
     each as its card count and the totals of its cards' printed values / 10 (e.g. how many Place damage effects
     are still in my deck).
   CARDS: the unit anchored in each cell, then my hand (up to 10 cards, in card-list order); a card number only
     picks the card's printed values (cardFeatures) for the cell layer and the hand slots: no card has weights.
   Values with no firm limit use sq(x) = square root of x / 10 (x below 0 counts as 0): 1 -> 0.10, 2 -> 0.14,
   5 -> 0.22, 100 -> 1.00, 400 -> 2.00. Small everyday values stay clearly apart, large ones come through
   distinctly, and nothing is capped. Values with a firm rule limit are divided by that limit. All values are
   stored as decimals. */
const sq = v => Math.sqrt(Math.max(0, v || 0)) / 10;
const F3 = (() => {
  const cards = NET_CARD_KEYS.slice(), props = NET_PROPERTIES;
  const NCELL = 2 * LANES.length * ROWS * COLS, HS = HAND_LIMIT, CS = 20;
  const LANEN = 17, PILES = 4, FIXED = LANES.length * LANEN + 8 + 8, NREST = FIXED + PILES * (1 + props.length);
  return { version: 7, PILES, cards, props, DE: 0, CO: 16, CS, NCELL, HS, LANEN, FIXED, NREST, RECN: NCELL * CS + NREST, NK: NCELL + HS, hidden: [128, 64] };
})();
/** A card's printed values: abilities and effect parts as numbers on the square-root scale (true counts 1). */
const F3_PRINTED = NET_FEATURES.map(m => F3.props.map(pk => sq(m.get(pk) || 0)));
/** Each deck's list as card number -> copies. */
const F3_DECK_LISTS = Object.fromEntries(Object.keys(DECKS).map(d => [d, DECKS[d].list.map(([k, n]) => [NET_CARD_INDEX[k], n])]));
const F3_PILE = new Float32Array(F3.props.length);
/** The same values as [position, value] pairs of the non-zero ones only, for adding up piles quickly. */
const F3_SPARSE = F3_PRINTED.map(row => row.flatMap((v, t) => (v ? [[t, v]] : [])));
function encode3(s, me, into) {
  // into: arrays to write into instead of new ones (a network's input); they are cleared first
  const nums = into ? into.nums.fill(0) : new Float32Array(F3.RECN), cards = into ? into.cards.fill(0) : new Uint16Array(F3.NK), opp = other(me);
  let k = 0;
  for (const side of [me, opp]) for (const lane of LANES) {
    const at = new Array(ROWS * COLS);                          // which unit covers each cell (as occupancy, without text keys)
    for (const x of s.units) if (ctl(x) === side && x.lane === lane)
      for (const cell of cellsOf(x)) if (cell[0] >= 0 && cell[0] < ROWS && cell[1] >= 0 && cell[1] < COLS) at[cell[0] * COLS + cell[1]] = x;
    for (let fromFront = 0; fromFront < ROWS; fromFront++) for (let c = 0; c < COLS; c++, k++) {
      const r = side === 0 ? fromFront : ROWS - 1 - fromFront, u = at[r * COLS + c], o = k * F3.CS;
      if (!u) continue;
      if (u.r === r && u.c === c) {
        nums[o] = 1;
        nums[o + 1] = sq(strengthOf(u)); nums[o + 2] = sq(defenceOf(u)); nums[o + 3] = sq(u.dmg);
        nums[o + 4] = sq(u.bs); nums[o + 5] = sq(u.bd); nums[o + 6] = sq(u.ts);
        nums[o + 7] = u.moved ? 1 : 0; nums[o + 8] = u.attacked ? 1 : 0; nums[o + 9] = u.o === 'v' ? 1 : 0;
        cards[k] = NET_CARD_INDEX[u.card] + 1;
      } else {
        nums[o + 10] = 1;
        const anchorFromFront = side === 0 ? u.r : ROWS - 1 - u.r;
        nums[o + 11 + anchorFromFront * COLS + u.c] = 1;
      }
    }
  }
  let i = F3.NCELL * F3.CS;
  const put = v => { nums[i++] = v; };
  for (const lane of LANES) {
    const d = dotState(s, lane);
    for (let c = 0; c < COLS; c++) { put(d[c] === me ? 1 : 0); put(d[c] === opp ? 1 : 0); put(d[c] === 'x' ? 1 : 0); }
    put(s.owner[lane] === me ? 1 : 0); put(s.owner[lane] === opp ? 1 : 0);
    put(sq(s.pool[me][lane])); put(sq(s.pool[opp][lane]));
    put(sq(s.poolStart[me][lane])); put(sq(s.poolStart[opp][lane]));
    put(sq(laneSupply(s, me, lane))); put(sq(laneSupply(s, opp, lane)));
  }
  for (const side of [me, opp]) {
    const P = s.players[side];
    put(P.reserve / MAX_CARRY); put(P.hand.length / HAND_LIMIT); put(sq(P.draw.length)); put(sq(P.discard.length));
  }
  put(sq(s.round)); put(s.starter === me ? 1 : 0); put(s.cur === me ? 1 : 0); put(s.passed === me ? 1 : 0); put(s.passed === opp ? 1 : 0);
  put((s.quietRounds || 0) / 3); put(sq(s.acts));
  put(s.redrawDone ? (s.players[opp].redrawn || []).length / MAX_REDRAW : 0);
  // the four piles, each as its size and its cards' printed-value totals
  const pile = counts => {                                     // counts: [card number, copies] pairs
    F3_PILE.fill(0);
    let n = 0;
    for (const [j, c] of counts) { if (c <= 0) continue; n += c; for (const [t, v] of F3_SPARSE[j]) F3_PILE[t] += c * v; }
    put(sq(n));
    for (let t = 0; t < F3_PILE.length; t++) put(F3_PILE[t] / 10);
  };
  const tally = keys => { const m = new Map(); for (const key of keys) { const j = NET_CARD_INDEX[key]; m.set(j, (m.get(j) || 0) + 1); } return m; };
  // their unseen cards, as unseenCards counts them: their deck list, less each card seen in their discard or on the board
  const od = s.players[opp].deck;
  const unseen = new Map(F3_DECK_LISTS[od] || (F3_DECK_LISTS[od] = DECKS[od].list.map(([k, n]) => [NET_CARD_INDEX[k], n])));
  for (const key of s.players[opp].discard) { const j = NET_CARD_INDEX[key]; if (unseen.get(j) > 0) unseen.set(j, unseen.get(j) - 1); }
  for (const u of s.units) if (u.owner === opp) { const j = NET_CARD_INDEX[u.card]; if (unseen.get(j) > 0) unseen.set(j, unseen.get(j) - 1); }
  pile(tally(s.players[me].draw)); pile(unseen); pile(tally(s.players[me].dealt || [])); pile(tally(s.players[me].redrawn || []));
  const hand = s.players[me].hand.map(key => NET_CARD_INDEX[key]).sort((a, b) => a - b);
  for (let j = 0; j < Math.min(F3.HS, hand.length); j++) cards[F3.NCELL + j] = hand[j] + 1;
  return { nums, cards };
}
/** Where each recorded value goes when lanes 1 and 3 are swapped (the left-right mirror). */
const F3_MIRROR = (() => {
  const L = LANES.length, perLane = ROWS * COLS, swapLane = l => L - 1 - l;
  const nums = new Int32Array(F3.RECN), cards = new Int32Array(F3.NK);
  for (let side = 0; side < 2; side++) for (let l = 0; l < L; l++) for (let j = 0; j < perLane; j++) {
    const from = (side * L + l) * perLane + j, to = (side * L + swapLane(l)) * perLane + j;
    cards[to] = from;
    for (let t = 0; t < F3.CS; t++) nums[to * F3.CS + t] = from * F3.CS + t;
  }
  for (let j = 0; j < F3.HS; j++) cards[F3.NCELL + j] = F3.NCELL + j;
  const base = F3.NCELL * F3.CS;
  for (let l = 0; l < L; l++) for (let t = 0; t < F3.LANEN; t++) nums[base + swapLane(l) * F3.LANEN + t] = base + l * F3.LANEN + t;
  for (let i = base + L * F3.LANEN; i < F3.RECN; i++) nums[i] = i;
  return { nums, cards };
})();

const NET3_WASM = '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';
/**
 * Format-3 networks. The arithmetic runs in WebAssembly, and all networks of one page or worker share ONE block
 * of memory: the browser reserves a large stretch of address space for every separate WebAssembly memory and
 * allows only about a hundred per tab, which dozens of workers with several networks each would exceed. Each
 * network gets its own region of the shared block; when the block grows, every network's views are renewed.
 */
const NET3 = { module: null, memory: null, top: 0, nets: [] };
function net3Instance(hidden, train = false) {
  if (!NET3.module) NET3.module = new WebAssembly.Module(Uint8Array.from(atob(NET3_WASM), ch => ch.charCodeAt(0)));
  if (!NET3.memory) NET3.memory = new WebAssembly.Memory({ initial: 16 });
  const x = new WebAssembly.Instance(NET3.module, { env: { memory: NET3.memory, abort() { throw new Error('network arithmetic failed'); } } }).exports;
  if (!NET3.top) NET3.top = x.heapBase();
  const args = [F3.cards.length, F3.DE, F3.props.length, F3.CS, F3.CO, F3.NCELL, F3.HS, F3.NREST, hidden[0], hidden[1], hidden[2] || 0, train ? 1 : 0];
  const base = NET3.top, end = x.setup(base, 0, ...args);
  const pages = Math.ceil(end / 65536) - NET3.memory.buffer.byteLength / 65536;
  if (pages > 0) { NET3.memory.grow(pages); for (const n of NET3.nets) n.views(); }
  x.setup(base, 1, ...args);
  NET3.top = end;
  const P = x.params();
  // only a learning network has gradient, momentum and receive buffers; one that just plays has the weights alone
  const net = { enc: 3, x, hidden: hidden.slice(), P, train, step: 0 };
  net.views = () => {
    const buf = NET3.memory.buffer;
    net.w = new Float32Array(buf, x.wPtr(), P);
    net.g = train ? new Float32Array(buf, x.gPtr(), P) : null; net.m = train ? new Float32Array(buf, x.mPtr(), P) : null;
    net.v = train ? new Float32Array(buf, x.vPtr(), P) : null; net.r = train ? new Float32Array(buf, x.rPtr(), P) : null;
    net.recs = Array.from({ length: 8 }, (_, c) => ({ nums: new Float32Array(buf, x.recPtr(c), F3.RECN), cards: new Uint16Array(buf, x.cardsPtr(c), F3.NK) }));
  };
  net.views();
  NET3.nets.push(net);
  const buf = NET3.memory.buffer;
  new Float32Array(buf, x.printedPtr(), F3.cards.length * F3.props.length).set(F3_PRINTED.flat());
  const pos = new Float32Array(buf, x.posPtr(), F3.NCELL * 7);
  pos.fill(0);
  for (let k = 0; k < F3.NCELL; k++) {
    const mine = k < F3.NCELL / 2, fromFront = Math.floor((k % (ROWS * COLS)) / COLS), c = k % COLS;
    pos[k * 7] = mine ? 1 : 0; pos[k * 7 + 1 + fromFront] = 1; pos[k * 7 + 4 + c] = 1;
  }
  /** The raw output for a position given as arrays at record  (optionally mirrored), in board slot c. */
  net.load = (c, nums, cards, i, mirror) => {
    const r = net.recs[c], nb = i * F3.RECN, kb = i * F3.NK;
    if (!mirror) { r.nums.set(nums.subarray(nb, nb + F3.RECN)); r.cards.set(cards.subarray(kb, kb + F3.NK)); }
    else {
      const mn = F3_MIRROR.nums, mc = F3_MIRROR.cards;
      for (let t = 0; t < F3.RECN; t++) r.nums[t] = nums[nb + mn[t]];
      for (let t = 0; t < F3.NK; t++) r.cards[t] = cards[kb + mc[t]];
    }
  };
  net.value = e => { net.recs[0].nums.set(e.nums); net.recs[0].cards.set(e.cards); return x.forward(0); };
  // a position straight from the game state: encoded directly into the network's input, with no copy in between
  net.valueOf = (st, me) => { encode3(st, me, net.recs[0]); return x.forward(0); };
  return net;
}
/**
 * A playing network kept under a name (for example 'train'): when new weights of the same kind arrive, only the
 * weights are replaced, so no new network (and no new memory) is made.
 */
const netsByName = {};
function netNamed(name, data) {
  const cur = netsByName[name];
  if (cur && data && data.arch && data.arch.version === F3.version && cur.hidden.join() === data.arch.hidden.join()
    && data.arch.props.join() === F3.props.join()) {
    if (cur.src !== data.weights) { cur.w.set(floatsOfB64(data.weights)); cur.src = data.weights; }
    return cur;
  }
  const net = netFromData(data);
  net.src = data.weights;
  return (netsByName[name] = net);
}
/**
 * Whether saved network data is a usable format-3 network, checked from its shape alone (no network is created,
 * so checking costs no memory): its weights must fit the layout of the card list and printed values it was made with.
 */
function net3Valid(data, hidden) {
  try {
    if (!data || data.enc !== 3 || !data.arch || data.arch.version !== F3.version || !Array.isArray(data.arch.hidden)) return false;
    if (hidden && data.arch.hidden.join() !== hidden.join()) return false;
    const L = net3Layout(data.arch.props.length, data.arch.hidden);
    const w = data.weights, pad = w.endsWith('==') ? 2 : w.endsWith('=') ? 1 : 0;
    return (w.length * 3 / 4 - pad) / 4 === L.total;
  } catch (e) { return false; }
}

/** Weight layout of a format-3 network, as named blocks (for moving weights between printed-value lists or sizes). */
function net3Layout(np, hidden) {
  const CIN = F3.CS + np + 7, MIN = F3.NCELL * F3.CO + F3.HS * np + F3.FIXED + F3.PILES * (1 + np);
  const sizes = [MIN, ...hidden, 1], blocks = [];
  let o = 0;
  const add = (name, n) => { blocks.push({ name, o, n }); o += n; };
  add('WC', CIN * F3.CO); add('BC', F3.CO);
  for (let l = 0; l < sizes.length - 1; l++) { add('W' + l, sizes[l] * sizes[l + 1]); add('B' + l, sizes[l + 1]); }
  return { blocks: Object.fromEntries(blocks.map(b => [b.name, b])), total: o, CIN, MIN, sizes };
}
/**
 * A new network. Its starting weights come from a fixed seed (one per network shape), so every AI starts from
 * exactly the same weights, on every restart; the size-check shapes each have their own fixed start.
 */
function net3Create(hidden = F3.hidden) {
  const net = net3Instance(hidden), L = net3Layout(F3.props.length, hidden), w = net.w, B = L.blocks;
  let seed = 0x9E3779B9;
  for (const ch of 'three-bases:' + hidden.join('x')) seed = Math.imul(seed ^ ch.charCodeAt(0), 0x85EBCA6B) >>> 0;
  const rnd = () => {                                          // mulberry32
    seed = (seed + 0x6D2B79F5) >>> 0;
    let z = seed; z = Math.imul(z ^ (z >>> 15), z | 1); z ^= z + Math.imul(z ^ (z >>> 7), z | 61);
    return ((z ^ (z >>> 14)) >>> 0) / 4294967296;
  };
  const gauss = () => { let u = 0, v = 0; while (!u) u = rnd(); while (!v) v = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
  const fill = (b, sd) => { for (let i = 0; i < b.n; i++) w[b.o + i] = sd * gauss(); };
  fill(B.WC, Math.sqrt(2 / L.CIN));
  for (let l = 0; l < L.sizes.length - 1; l++) fill(B['W' + l], Math.sqrt(2 / L.sizes[l]));
  return net;
}
const b64OfFloats = a => { const u = new Uint8Array(a.buffer, a.byteOffset, a.byteLength); let s = ''; for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000)); return btoa(s); };
const floatsOfB64 = s => { const b = atob(s), u = new Uint8Array(b.length); for (let i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return new Float32Array(u.buffer); };
/**
 * A bigger copy of a network, for the size check. Every weight it has is kept; new nodes get the new shape's usual
 * random incoming weights and zero outgoing weights (and zero biases), so the copy plays exactly like the original
 * until it learns. A network with an extra layer keeps everything up to its last hidden layer; the new layer and the
 * output start fresh, as an exact copy is impossible there. Storage: the first layer's weights row by input (its
 * input is sparse), the others row by output.
 */
function net3Grow(data, hidden) {
  const np = F3.props.length, src = floatsOfB64(data.weights);
  const Lo = net3Layout(np, data.arch.hidden), Ln = net3Layout(np, hidden), net = net3Create(hidden), w = net.w;
  for (const b of ['WC', 'BC']) w.set(src.subarray(Lo.blocks[b].o, Lo.blocks[b].o + Lo.blocks[b].n), Ln.blocks[b].o);
  const deeper = Ln.sizes.length > Lo.sizes.length, layers = deeper ? Lo.sizes.length - 2 : Lo.sizes.length - 1;
  for (let l = 0; l < layers; l++) {
    const at = (i, o, nIn, nOut) => (l === 0 ? i * nOut + o : o * nIn + i);
    const oi = Lo.sizes[l], oo = Lo.sizes[l + 1], ni = Ln.sizes[l], no = Ln.sizes[l + 1];
    const Wo = Lo.blocks['W' + l].o, Wn = Ln.blocks['W' + l].o, Bo = Lo.blocks['B' + l].o, Bn = Ln.blocks['B' + l].o;
    for (let i = 0; i < ni; i++) for (let o = 0; o < no; o++) {
      if (i < oi && o < oo) w[Wn + at(i, o, ni, no)] = src[Wo + at(i, o, oi, oo)];   // kept
      else if (o < oo) w[Wn + at(i, o, ni, no)] = 0;                                  // a new node into an old one: silent
    }                                                                                 // into a new node: random, as made
    for (let o = 0; o < no; o++) w[Bn + o] = o < oo ? src[Bo + o] : 0;
  }
  return net3ToData(net);
}
function net3ToData(net, withMomentum = false) {
  return { enc: 3, arch: { version: F3.version, props: F3.props, hidden: net.hidden }, weights: b64OfFloats(net.w),
    ...(withMomentum && net.train ? { m: b64OfFloats(net.m), v: b64OfFloats(net.v), step: net.step } : {}) };
}
/**
 * A saved format-3 network. If the printed values (keywords, effect parts) have changed since it was saved, its
 * weights are moved to the new layout by name: known values keep what they learned, new ones start at zero, and
 * the learning momentum starts over. Changed or new cards need nothing: the network never sees card names.
 */
function net3FromData(data, train = false) {
  if (!data.arch || data.arch.version !== F3.version) throw new Error('This network was made for an older version of the lab and cannot be used.');
  const a = data.arch, net = net3Instance(a.hidden, train), old = floatsOfB64(data.weights);
  if (a.props.join() === F3.props.join()) {
    if (old.length !== net.P) throw new Error('This network does not fit this version of the lab.');
    net.w.set(old);
    if (train && data.m && data.v) { net.m.set(floatsOfB64(data.m)); net.v.set(floatsOfB64(data.v)); net.step = data.step || 0; }
    return net;
  }
  const Lo = net3Layout(a.props.length, a.hidden), Ln = net3Layout(F3.props.length, a.hidden);
  if (old.length !== Lo.total) throw new Error('This network does not fit this version of the lab.');
  const w = net.w, propOld = new Map(a.props.map((k, i) => [k, i]));
  w.fill(0);
  const copyRow = (bo, bn, rowOld, rowNew, width) => w.set(old.subarray(bo.o + rowOld * width, bo.o + (rowOld + 1) * width), bn.o + rowNew * width);
  const byName = (bo, bn, offOld, offNew, width) => F3.props.forEach((k, i) => { if (propOld.has(k)) copyRow(bo, bn, offOld + propOld.get(k), offNew + i, width); });
  // cell layer rows: recorded values, printed values by name, position
  for (let j = 0; j < F3.CS; j++) copyRow(Lo.blocks.WC, Ln.blocks.WC, j, j, F3.CO);
  byName(Lo.blocks.WC, Ln.blocks.WC, F3.CS, F3.CS, F3.CO);
  for (let j = 0; j < 7; j++) copyRow(Lo.blocks.WC, Ln.blocks.WC, F3.CS + a.props.length + j, F3.CS + F3.props.length + j, F3.CO);
  w.set(old.subarray(Lo.blocks.BC.o, Lo.blocks.BC.o + F3.CO), Ln.blocks.BC.o);
  // first main layer rows: cell summaries, hand slots (printed values by name), the fixed values, piles (size, totals by name)
  const H = a.hidden[0], cellRows = F3.NCELL * F3.CO, npO = a.props.length, npN = F3.props.length;
  for (let j = 0; j < cellRows; j++) copyRow(Lo.blocks.W0, Ln.blocks.W0, j, j, H);
  for (let sl = 0; sl < F3.HS; sl++) byName(Lo.blocks.W0, Ln.blocks.W0, cellRows + sl * npO, cellRows + sl * npN, H);
  const restOld = cellRows + F3.HS * npO, restNew = cellRows + F3.HS * npN;
  for (let j = 0; j < F3.FIXED; j++) copyRow(Lo.blocks.W0, Ln.blocks.W0, restOld + j, restNew + j, H);
  for (let pl = 0; pl < F3.PILES; pl++) {
    const po = restOld + F3.FIXED + pl * (1 + npO), pn = restNew + F3.FIXED + pl * (1 + npN);
    copyRow(Lo.blocks.W0, Ln.blocks.W0, po, pn, H);
    byName(Lo.blocks.W0, Ln.blocks.W0, po + 1, pn + 1, H);
  }
  w.set(old.subarray(Lo.blocks.B0.o, Lo.blocks.B0.o + H), Ln.blocks.B0.o);
  for (const name of Object.keys(Lo.blocks)) if (!['WC', 'BC', 'W0', 'B0'].includes(name)) w.set(old.subarray(Lo.blocks[name].o, Lo.blocks[name].o + Lo.blocks[name].n), Ln.blocks[name].o);
  return net;
}


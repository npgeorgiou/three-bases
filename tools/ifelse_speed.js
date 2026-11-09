#!/usr/bin/env node
/* Speed and same-decisions check of the ifelse AI (the game's Benchmark search):
   plays seeded Benchmark games (depth 1) to collect fixed positions, then lets the Benchmark choose a move in each at
   the given depth, and prints the time per move and a hash of every chosen move.

     node tools/ifelse_speed.js [depth] [positions] [where]     default depth 3, 12 positions; "where": also where the time went (slower)

   A speed change must keep the hash (same decisions). */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const SRC = path.join(__dirname, '..', 'src', 'game');
const parts = fs.readFileSync(path.join(SRC, 'parts.txt'), 'utf8').split('\n').map(s => s.trim())
  .filter(n => /^js\/(00-intro|cards\/|rules\/|ai\/)/.test(n));
const engine = parts.map(n => fs.readFileSync(path.join(SRC, n), 'utf8')).join('');
const depth = +(process.argv[2] || 3), nPos = +(process.argv[3] || 12), where = process.argv[4] === 'where';

const harness = `
;globalThis.__positions = function (n) {
  let seed = 777;
  Math.random = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
  const decks = PREMADE.map((d, i) => { const k = 'sp' + i; DECKS[k] = { name: d.name, fac: CARDS[Object.keys(d.cards)[0]].fac, list: Object.entries(d.cards) }; return k; });
  const out = [];
  for (let g = 0; out.length < n; g++) {
    const s = newGame(decks[(g * 3) % decks.length], decks[(g * 5 + 1) % decks.length]);
    s.noFx = true;
    for (const p of [0, 1]) aiMulligan(s, p);
    s.redrawDone = true;
    for (let i = 0; i < 400 && s.winner === null && out.length < n; i++) {
      if (i % 9 === 5 && !s.pending) out.push(cloneState(s));
      applyAction(s, chooseIfelseAction(s, { ...BENCH_VALUES, depth: 1 }));
    }
  }
  return out;
};
globalThis.__choose = (s, depth) => chooseIfelseAction(cloneState(s), { ...BENCH_VALUES, depth });`;

const ctx = { console, structuredClone };
vm.createContext(ctx);
vm.runInContext(engine + harness, ctx, { filename: 'engine.js' });
const pos = ctx.__positions(nPos);
// where the time goes: wrap the main steps (they are globals of the engine)
const spent = {}, calls = {};
if (where) for (const f of ['listActions', 'cloneState', 'applyAction', 'ifelseEval', 'ifelseThreat', 'nextRoundView', 'isPointless']) {
  const orig = ctx[f]; let depthIn = 0;
  ctx[f] = function (...a) {
    calls[f] = (calls[f] || 0) + 1;
    if (depthIn) return orig.apply(this, a);                         // count time once when a step calls itself
    depthIn++; const t = process.hrtime.bigint();
    try { return orig.apply(this, a); } finally { spent[f] = (spent[f] || 0) + Number(process.hrtime.bigint() - t) / 1e6; depthIn--; }
  };
}
let h = 2166136261; const mix = str => { for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } };
const t0 = Date.now(), times = [];
for (const s of pos) { const t = Date.now(); mix(JSON.stringify(ctx.__choose(s, depth))); times.push(Date.now() - t); }
const total = Date.now() - t0;
console.log(`depth ${depth}, ${pos.length} positions: ${(total / pos.length).toFixed(0)} ms per move (slowest ${Math.max(...times)} ms), hash ${h.toString(16)}`);
if (where) console.log(Object.keys(spent).sort((a, b) => spent[b] - spent[a]).map(f => `${f} ${(100 * spent[f] / total).toFixed(0)}% (${calls[f]} calls)`).join(', '));

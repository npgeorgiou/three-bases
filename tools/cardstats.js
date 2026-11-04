#!/usr/bin/env node
/* Benchmark card report for one faction: plays Benchmark games (depth 1) with the faction's premade decks against every
   other premade deck, and prints per card: games where it was played, times played, times its effects fired, and the
   win rate of the games where it was played. Cards that are never played or never fire need a look.
     node tools/cardstats.js <faction letter> [games per deck, default 6]
   Decks: the faction's premades, plus decks of 12 different cards x3 that together cover every card. */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const SRC = path.join(__dirname, '..', 'src', 'game');
const parts = fs.readFileSync(path.join(SRC, 'parts.txt'), 'utf8').split('\n').map(s => s.trim())
  .filter(n => /^js\/(00-intro|cards\/|rules\/|ai\/)/.test(n));
const engine = parts.map(n => fs.readFileSync(path.join(SRC, n), 'utf8')).join('');
const harness = `
;globalThis.__run = function (fac, per) {
  let seed = 4242;
  Math.random = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
  let live = false;
  const fired = {}, played = {}, games = {}, wins = {};
  const realFire = fxFire;
  fxFire = function (s, on, u, extra) { if (live && cardOf(u) && cardOf(u).fac === fac && (cardOf(u).fx || []).some(f => f.on === on)) { const k = baseKey(u.card); fired[k] = (fired[k] || 0) + 1; } return realFire(s, on, u, extra); };
  const keyOf = d => { const k = 'cs' + d.id; DECKS[k] = { name: d.name, fac: CARDS[Object.keys(d.cards)[0]].fac, list: Object.entries(d.cards) }; return k; };
  const mine = PREMADE.filter(d => CARDS[Object.keys(d.cards)[0]].fac === fac), others = PREMADE.filter(d => !mine.includes(d));
  // plus decks that cover every card of the faction: its cards in a fixed shuffle, 12 different cards x3 per deck
  const all = shuffle(Object.keys(CARDS).filter(k => CARDS[k].fac === fac && !CARDS[k].token));
  for (let i = 0; i < all.length; i += 12) mine.push({ id: 'cover' + i, name: 'cover ' + i, cards: Object.fromEntries(all.slice(i, i + 12).concat(all.slice(0, Math.max(0, i + 12 - all.length))).map(k => [k, 3])) });
  let total = 0, won = 0;
  for (const d of mine) for (let g = 0; g < per; g++) {
    const opp = others[(g * 5 + d.id.length) % others.length], me = g % 2;
    const s = newGame(me === 0 ? keyOf(d) : keyOf(opp), me === 0 ? keyOf(opp) : keyOf(d));
    s.noFx = true;
    for (const p of [0, 1]) aiMulligan(s, p);
    s.redrawDone = true;
    const seen = new Set();
    for (let i = 0; i < 3000 && s.winner === null && s.round <= 30; i++) {
      const a = chooseIfelseAction(s, { ...BENCH_VALUES, depth: 1 });
      if (s.cur === me && (a.t === 'deploy' || a.t === 'tactic')) { const k = s.players[me].hand[a.hi]; played[k] = (played[k] || 0) + 1; seen.add(k); }
      live = true; applyAction(s, a); live = false;
    }
    total++; const w = s.winner === me; if (w) won++;
    for (const k of seen) { games[k] = (games[k] || 0) + 1; if (w) wins[k] = (wins[k] || 0) + 1; }
  }
  const keys = Object.keys(CARDS).filter(k => CARDS[k].fac === fac && !CARDS[k].token).sort((a, b) => (played[a] || 0) - (played[b] || 0));
  const out = ['games ' + total + ', won ' + won + ' (' + Math.round(100 * won / Math.max(1, total)) + '%)', 'card | games played in | times played | effects fired | win rate when played'];
  for (const k of keys) out.push(CARDS[k].name + ' | ' + (games[k] || 0) + ' | ' + (played[k] || 0) + ' | ' + (fired[k] || 0) + ' | ' + (games[k] ? Math.round(100 * (wins[k] || 0) / games[k]) + '%' : '-'));
  return out.join('\\n');
};`;
const ctx = { console, performance: { now: () => 0 }, structuredClone };
vm.createContext(ctx);
vm.runInContext(engine + harness, ctx, { filename: 'engine.js' });
console.log(ctx.__run(process.argv[2], +(process.argv[3] || 6)));

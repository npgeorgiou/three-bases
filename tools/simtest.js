#!/usr/bin/env node
/* Headless rules test: plays seeded computer-vs-computer games on the engine parts of src/game
   (cards, rules, computer opponent) and prints one line: games, winners and a hash of every move.

     node tools/simtest.js            30 Random-vs-Random games + 2 Benchmark games (depth 1)
     node tools/simtest.js 100        100 Random games + 2 Benchmark games

   Same seed, same code → same hash. A refactor or cleanup must not change the hash; a rules change
   usually does (then check the changed behaviour, not the hash). A crash prints the error and the game. */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const SRC = path.join(__dirname, '..', 'src', 'game');
const parts = fs.readFileSync(path.join(SRC, 'parts.txt'), 'utf8').split('\n').map(s => s.trim())
  .filter(n => /^js\/(00-intro|cards\/|rules\/|ai\/)/.test(n));
const engine = parts.map(n => fs.readFileSync(path.join(SRC, n), 'utf8')).join('');

const harness = `
;globalThis.__run = function (nRandom) {
  let seed = 12345;
  Math.random = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
  const decks = PREMADE.map((d, i) => { const k = 'sim' + i; DECKS[k] = { name: d.name, fac: CARDS[Object.keys(d.cards)[0]].fac, list: Object.entries(d.cards) }; return k; });
  let h = 2166136261; const mix = str => { for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } };
  const wins = { 0: 0, 1: 0, draw: 0, none: 0 };
  const play = (bench, g) => {
    const s = newGame(decks[g % decks.length], decks[(g * 7 + 3) % decks.length]);
    s.noFx = true;
    for (const p of [0, 1]) bench ? aiMulligan(s, p) : randomRedraw(s, p);
    s.redrawDone = true;
    for (let i = 0; i < 3000 && s.winner === null && s.round <= 30; i++) {
      const a = bench ? chooseIfelseAction(s, { ...BENCH_VALUES, depth: 1 }) : randomMove(listActions(s).map(a => ({ a }))).a;
      mix(JSON.stringify(a)); applyAction(s, a);
    }
    wins[s.winner === null ? 'none' : s.winner]++; mix('|' + s.winner + ':' + s.round);
  };
  for (let g = 0; g < nRandom; g++) play(false, g);
  for (let g = 0; g < 2; g++) play(true, g);
  return 'games ' + (nRandom + 2) + ', wins ' + JSON.stringify(wins) + ', hash ' + h.toString(16);
};`;

const ctx = { console, performance: { now: () => 0 }, structuredClone };
vm.createContext(ctx);
vm.runInContext(engine + harness, ctx, { filename: 'engine.js' });
console.log(ctx.__run(+(process.argv[2] || 30)));

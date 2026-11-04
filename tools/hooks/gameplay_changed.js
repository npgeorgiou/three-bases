#!/usr/bin/env node
/* Prints the faction letters whose cards changed in play between HEAD and the staged files (used by pre-commit).
   Play = everything on a card except its text, net line, art and champion mark: cost, stats, size, keywords, effects.
   So hover links, wording and champion marks never set off the design gate.   node tools/hooks/gameplay_changed.js */
'use strict';
const { execSync } = require('child_process'), vm = require('vm');
const git = a => { try { return execSync('git ' + a, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], maxBuffer: 1 << 28 }); } catch (e) { return null; } };
const parts = (git('show :src/game/parts.txt') || '').split('\n').map(s => s.trim()).filter(n => /^js\/cards\//.test(n) && !/art\.js$/.test(n));
const LOOKS = new Set(['text', 'net', 'art', 'champion']);
function play(ref) {  // ref '' = the staged files
  const src = parts.map(n => git(`show ${ref}:src/game/${n}`) || '').join('\n');
  const ctx = {}; vm.createContext(ctx);
  try { vm.runInContext(src + ';globalThis.C = CARDS;', ctx); } catch (e) { return null; }
  const out = {};
  for (const [k, c] of Object.entries(ctx.C)) out[k] = { fac: c.fac, sig: JSON.stringify(c, (key, v) => (LOOKS.has(key) ? undefined : v)) };
  return out;
}
const a = play('HEAD'), b = play('');
const letters = new Set();
if (!a || !b) 'cdabsol'.split('').forEach(f => letters.add(f));  // a file that doesn't load: check every faction
else for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) {
  if (!a[k] || !b[k] || a[k].sig !== b[k].sig) letters.add((b[k] || a[k]).fac);
}
console.log([...letters].filter(f => f && 'cdabsol'.includes(f)).join(' '));

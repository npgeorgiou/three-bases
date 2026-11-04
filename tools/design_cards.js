#!/usr/bin/env node
/* CARD lines for the network check, made from a faction's card file in the game (src/game/js/cards/new-<faction>.js).
   Each card there carries net: 'Mechanic, Mechanic / makes a, b / needs c'.
     node tools/design_cards.js <faction letter>   (prints the lines; save them as factions/designs/<faction>-cards.txt) */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const SRC = path.join(__dirname, '..', 'src', 'game');
const parts = fs.readFileSync(path.join(SRC, 'parts.txt'), 'utf8').split('\n').map(s => s.trim()).filter(n => /^js\/cards\//.test(n));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(parts.map(n => fs.readFileSync(path.join(SRC, n), 'utf8')).join('\n') + ';globalThis.C = CARDS;', ctx);
const fac = process.argv[2], SIZE = { 1: '', 2: ' ▪▪', 3: ' ▪▪▪', 4: ' ▪▪▪▪' };
const plain = t => t.replace(/\[\[([^\]|]+)\|[^\]]+\]\]/g, '$1').replace(/\[\[([^\]]+)\]\]/g, '$1').replace(/\{\{card:[^|}]+\|([^}]+)\}\}/g, '$1').replace(/\|/g, '/');
const out = [];
for (const [k, c] of Object.entries(ctx.C)) {
  if (c.fac !== fac || c.token || !c.net) continue;
  const [mech, makes, needs] = c.net.split('/').map(x => x.trim());
  const cost = c.tactic ? `spell ${c.cost}` : `${c.sup} - ${c.str}|${c.def}${SIZE[c.size] || ''}`;
  const lines = [`CARD ${c.name}`, cost, plain(c.text), `mech: ${mech}`];
  if (makes && makes !== '-') lines.push(`makes: ${makes.replace(/^makes\s*/, '')}`);
  if (needs && needs !== '-') lines.push(`needs: ${needs.replace(/^needs\s*/, '')}`);
  if (c.champion) lines.push('champion');
  out.push(lines.join(' | '));
}
console.log(out.join('\n'));

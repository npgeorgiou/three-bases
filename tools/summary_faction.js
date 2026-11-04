#!/usr/bin/env node
/* Writes summary/11-faction-<file>.txt for one faction from the game's card data and its entry in factions/designs/.
     node tools/summary_faction.js <faction letter>   (all seven: node tools/summary_faction.js all) */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.join(__dirname, '..'), SRC = path.join(ROOT, 'src', 'game');
const parts = fs.readFileSync(path.join(SRC, 'parts.txt'), 'utf8').split('\n').map(s => s.trim()).filter(n => /^js\/cards\//.test(n));
const ctx = {};
vm.createContext(ctx);
vm.runInContext(parts.map(n => fs.readFileSync(path.join(SRC, n), 'utf8')).join('\n') + ';globalThis.C = CARDS;', ctx);
const FAC = { c: ['HOROLOGERS', 'horologers'], d: ['SUNFEEDERS', 'sunfeeders'], a: ['IMPI', 'impi'], b: ['HOSPICE KNIGHTS', 'hospice'],
  s: ['STAR PRIESTS', 'starpriests'], o: ['ROOTKIN', 'rootkin'], l: ['THE LONG GUNS', 'longguns'] };
const SIZE = { 1: '', 2: ' ▪▪', 3: ' ▪▪▪', 4: ' ▪▪▪▪' };
const plain = t => (t || '').replace(/\[\[([^\]|]+)\|[^\]]+\]\]/g, '$1').replace(/\[\[([^\]]+)\]\]/g, '$1').replace(/\{\{card:[^|}]+\|([^}]+)\}\}/g, '$1');
const byCost = (a, b) => (a.cost ?? a.sup) - (b.cost ?? b.sup) || a.name.localeCompare(b.name);

function section(entry, head) {  // the lines after a heading line, up to the next blank line
  const i = entry.findIndex(l => l.startsWith(head));
  if (i < 0) return [];
  const out = [];
  for (let j = i + 1; j < entry.length && entry[j].trim(); j++) out.push(entry[j].trim());
  return out;
}

function write(letter) {
  const [title, file] = FAC[letter];
  const entry = fs.readFileSync(path.join(ROOT, 'factions', 'designs', file + '.txt'), 'utf8').split('\n');
  const cards = Object.values(ctx.C).filter(c => c.fac === letter);
  const units = cards.filter(c => !c.tactic && !c.token).sort(byCost), spells = cards.filter(c => c.tactic && !c.token).sort(byCost);
  const tokens = cards.filter(c => c.token).sort(byCost);
  const champs = cards.filter(c => (c.net || '').split('/').map(x => x.trim())[3] === 'champion').map(c => c.name);
  const kws = [];  // keyword lines with their indented continuation lines
  entry.forEach((l, i) => { if (!/^- [A-Z][A-Za-z ]* ?N? \(value/.test(l)) return;
    let t = l.slice(2).trim();
    for (let j = i + 1; j < entry.length && /^  \S/.test(entry[j]); j++) t += ' ' + entry[j].trim();
    kws.push(t); });
  const ti = entry.findIndex(l => l.startsWith('THEME:'));
  let theme = ti < 0 ? '' : entry[ti].replace(/^THEME:\s*/, '');
  for (let j = ti + 1; ti >= 0 && j < entry.length && entry[j].trim() && !/^\d+\./.test(entry[j]); j++) theme += ' ' + entry[j].trim();
  const unit = c => `${c.name}  ${c.sup} - ${c.str}|${c.def}${SIZE[c.size] || ''}  ${plain(c.text)}`;
  const spell = c => `${c.name}  ${c.cost}  ${plain(c.text)}`;
  const L = ['==================================================================',
    `11. ${title} (faction letter ${letter}; ${units.length + spells.length} cards: ${units.length} units, ${spells.length} spells)`,
    '==================================================================',
    `Theme: ${theme}`, `Identity: ${section(entry, 'IDENTITY').join(' ')}`, 'Keywords (value = stat points from the supply budget):',
    ...kws.map(k => '- ' + k), `Champions: ${champs.join(', ')}.`, `Design entry: factions/designs/${file}.txt. Cards in the game: src/game/js/cards/new-${file}.js.`,
    '', 'Units (supply - strength|defence, size):', ...units.map(unit), '', 'Spells (supply):', ...spells.map(spell)];
  if (tokens.length) L.push('', 'Tokens:', ...tokens.map(c => c.tactic ? spell(c) : unit(c)));
  const out = path.join(ROOT, 'summary', `11-faction-${file}.txt`);
  fs.writeFileSync(out, L.join('\n') + '\n');
  console.log(`${out}: ${L.length} lines`);
}
const arg = process.argv[2];
(arg === 'all' ? Object.keys(FAC) : [arg]).forEach(write);

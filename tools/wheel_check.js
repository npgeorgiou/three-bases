#!/usr/bin/env node
/* A faction of the game measured on the wheel's 24 radii (factions/12, step 7), in seconds, with no import.
     node tools/wheel_check.js <faction letter> ["heals=1.6,stops=0.3"]
   Reads the faction's cards from src/game/js/cards/, counts per radius the cards that do that thing (the tables below:
   effect word, trigger, keyword flag -> radius), and prints per radius: share of cards, value, planned value, DRIFTED.
   Value = share against the average real faction: the library's average share per game (library/cards_db/axes.tsv),
   each game counted the same, with the smoothing of axes.py (5 more cards at the average, power 0.75). Strength, defence
   and the two width radii compare with the average of the factions in this game (stats of other games use other
   numbers). "Position and combos" prints only the share of cards that act on the allies beside, behind or ahead: the
   library's combo number comes from its lines between cards, which our cards don't have.
   A word no table knows is printed as NOT MAPPED and the run fails: add it to its table (to NONE when it is no radius).
   The planned values are the faction's radii in the wheel table, keys as in `axes.py --near`. */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.join(__dirname, '..'), SRC = path.join(ROOT, 'src', 'game');
const DRIFT = 0.4, SHRINK = 5, POWER = 0.75;  // DRIFT is Claude's number; the other two are axes.py's
const RADII = [['strong', 'strength'], ['grows', 'grows strength'], ['strikes', 'strikes more or first'], ['textdmg', 'damage from units\' text'],
  ['kills', 'kills outright'], ['many', 'many at once'], ['spelldmg', 'damage from spells'], ['spellpay', 'rewards playing spells'],
  ['stops', 'stops them'], ['disrupts', 'breaks their plan in other ways'], ['one', 'one chosen'], ['supply', 'more supply'],
  ['cheaper', 'cheaper or stronger hand'], ['cards', 'more cards'], ['picks', 'picks and copies'], ['back', 'brings back'],
  ['wide', 'many cheap units'], ['spends', 'spends them'], ['together', 'position and combos'], ['heals', 'heals them'],
  ['growsdef', 'grows defence'], ['protects', 'protects them'], ['tough', 'defence'], ['tall', 'a few big units']];
const OWN_NUMBERS = ['strong', 'tough', 'wide', 'tall'];

// who an effect lands on
const ENEMY = ['facing', 'nearest', 'enemies', 'adjEnemies', 'colEnemies', 'enemyFront', 'enemyBack', 'weakest', 'strongest', 'allEnemies',
  'deepest', 'hurtEnemies', 'marked', 'markedAll', 'hurtAll', 'deepestAll', 'itFacing'];
const OWN = ['self', 'allies', 'team', 'adj', 'row', 'col', 'hurtAlly', 'allAllies', 'otherLanes', 'behind', 'ahead', 'geared', 'frontAllies',
  'backAllies', 'hurtTeam', 'sideFront', 'otherFront', 'itTwins', 'deck'];
const IT = ['it', 'itAdj', 'inFrontOfIt', 'itBehind'];  // the chosen unit, or the other unit of the trigger: its side comes from the card
const SEVERAL = ['enemies', 'adjEnemies', 'colEnemies', 'enemyFront', 'enemyBack', 'allEnemies', 'hurtEnemies', 'marked', 'markedAll', 'hurtAll', 'deepestAll'];
const BESIDE = ['adj', 'row', 'col', 'behind', 'ahead', 'itAdj', 'itBehind', 'inFrontOfIt'];  // allies beside, behind or ahead
const BOARD_COUNTS = ['adj', 'row', 'col', 'allies', 'team', 'frontAllies', 'backAllies', 'geared', 'enemies', 'hurtEnemies', 'lostShields', 'emptyFront'];
const IT_ENEMY_ON = ['kill', 'enemyPlace', 'enemyDeath', 'survive'], IT_OWN_ON = ['allyDeath', 'allyAttack', 'allyPlace', 'allySurvive', 'allyArrive', 'healed', 'targeted'];
const HITS = ['dmg', 'chain', 'ricochet', 'kill', 'stun', 'push', 'pull', 'displace'];  // on "it" these land on an enemy unless the card says an ally

// trigger -> radii
const ON = { place: [], roundEnd: [], roundStart: [], move: [], arrive: [], kill: [], enemyDeath: [], enemyPlace: [], allyPlace: [], allyArrive: [],
  healed: [], wound: [], death: ['spends'], allyDeath: ['spends'], spell: ['spellpay'], targeted: ['spellpay'], attack: ['strikes'], allyAttack: ['strikes'],
  survive: [], allySurvive: [] };
// what a card counts or asks for -> radii
const COUNT = { deathsR: ['spends'], spellsR: ['spellpay'], attacksR: ['strikes'], handN: [], partsHand: [], shellsHand: [], discardUnits: [] };
const IF = { deaths: ['spends'], offered: ['spends'], spells: ['spellpay'], attacks: ['strikes'] };
// keyword flag on the card -> radii
const FLAG = { bonus: ['supply'], guard: ['protects'], armoured: ['protects'], entrench: ['protects', 'pos'], harden: ['growsdef'], vigil: ['heals'],
  perennial: ['grows', 'growsdef'], toll: ['grows', 'spends'], onrush: ['grows', 'strikes'], flanker: ['grows'], obsidian: ['kills'], headsman: [],
  charge: ['strikes'], flurry: ['strikes'], riposte: ['strikes'], retaliate: ['strikes'], reckless: ['spends'], offering: ['spends', 'supply', 'pos'],
  reserve: ['spends'], seeds: ['spends', 'wide'], salvage: ['spends', 'cards'], augur: ['spellpay'], roots: ['textdmg'], barrage: ['textdmg'],
  push: ['disrupts'], wall: ['growsdef', 'pos'], geared: ['pos'] };
const NONE = ['name', 'text', 'art', 'fac', 'net', 'size', 'sup', 'str', 'def', 'fx', 'tactic', 'cost', 'cast', 'aura', 'champion', 'token', 'fixed', 'ranged',
  'wound', 'outrider', 'reach', 'shellCard', 'lesser', 'lightfooted', 'moves', 'part', 'fade', 'src', 'tv', 'noAgain', 'key', 'k', 'lane', 'all'];
// words beside the effect word in one effect: who, how much, how long
const MOD = ['to', 'if', 'rnd', 'max', 'min', 'per', 'lim', 'x', 'plus', 'n', 'first', 'lane', 'all', 'at', 'of', 'from', 'kw', 'count', 'back', 'stat', 'lanes'];

const sets = new Map(), unknown = new Map();
const miss = (kind, w, card) => { const k = `${kind} "${w}"`; unknown.set(k, (unknown.get(k) || new Set()).add(card.name)); };
const base = t => String(t).split(':')[0];
function side(to, op, ctx, card) {
  const t = base(to);
  if (ENEMY.includes(t)) return 'enemy';
  if (OWN.includes(t)) return 'own';
  if (IT.includes(t)) {
    if (IT_ENEMY_ON.includes(ctx.on)) return 'enemy';
    if (IT_OWN_ON.includes(ctx.on)) return 'own';
    return HITS.includes(op) ? 'enemy' : 'own';
  }
  miss('target', t, card); return 'own';
}
function amountWords(v, R, card) {  // {count: selector}: counting the board is "many at once"; counting deaths, spells, attacks is their radius
  if (!v || typeof v !== 'object' || Array.isArray(v)) return;
  if (v.count) { const k = base(v.count); if (COUNT[k]) COUNT[k].forEach(r => R.add(r)); else if (BOARD_COUNTS.includes(k)) R.add('many'); else miss('count', k, card); }
}
const positive = v => (typeof v === 'number' ? v > 0 : !!v), negative = v => typeof v === 'number' && v < 0;
function effect(o, ctx, card, R) {
  const spell = !!card.tactic, named = ['pull', 'tick', 'omen', 'push'].find(k => typeof o[k] === 'string');  // {pull: 'it'}: the word names its target
  const to = o.to !== undefined ? o.to : named ? o[named] : null;
  const on = t => side(t, null, ctx, card), hit = (t, op) => side(t === null ? 'it' : t, op, ctx, card);
  const several = to !== null && SEVERAL.includes(base(to));
  if (to !== null && BESIDE.includes(base(to)) && on(to) === 'own') R.add('pos');
  if (to !== null && IT.includes(base(to)) && (spell || ctx.on === 'place')) R.add('one');  // a unit the player chooses
  for (const [k, v] of Object.entries(o)) {
    amountWords(v, R, card);
    if (MOD.includes(k)) { if (k === 'per') amountWords(v, R, card); continue; }
    switch (k) {
      case 'dmg': case 'chain': case 'ricochet':
        if (hit(to, k) === 'enemy') { R.add(spell ? 'spelldmg' : 'textdmg'); if (several || k !== 'dmg') R.add('many'); } break;
      case 'strike': case 'itStrike': case 'strikeWith': case 'ready': R.add('strikes'); break;
      case 'buff': {
        const [s, d] = Array.isArray(v) ? v : [v, 0];
        const who = to !== null && IT.includes(base(to)) && !IT_OWN_ON.includes(ctx.on) && (negative(s) || negative(d)) ? 'enemy' : on(to === null ? 'self' : to);
        if (who === 'own') { if (positive(s)) R.add('grows'); if (positive(d)) R.add('growsdef'); }
        else if (negative(s) || negative(d)) { R.add('disrupts'); if (several) R.add('many'); }
        amountWords(s, R, card); amountWords(d, R, card); break; }
      case 'heal': R.add('heals'); break;
      case 'draw': R.add('cards'); break;
      case 'card': R.add('cards'); break;
      case 'copy': case 'echo': R.add('picks'); break;
      case 'again': case 'raise': R.add('back'); break;
      case 'carry': case 'pool': R.add('supply'); break;
      case 'sup': R.add(on(to === null ? 'self' : to) === 'enemy' ? 'disrupts' : negative(v) ? 'cheaper' : 'supply'); break;
      case 'token': R.add('wide'); break;
      case 'kw':
        break;
      case 'kill': if (hit(to, k) === 'enemy') { R.add('kills'); if (several && !o.first) R.add('many'); } else R.add('spends'); break;
      case 'offer': R.add('spends'); R.add('pos'); break;
      case 'push': case 'pull': case 'displace': if (hit(to, k) === 'enemy') { R.add('disrupts'); if (several) R.add('many'); } break;
      case 'stun': if (hit(to, k) === 'enemy') { R.add('stops'); if (several) R.add('many'); } break;
      case 'tick': case 'replace': case 'omen': case 'undo': case 'ride': case 'advance': break;  // no radius: an ally acts again or moves
      default: miss('effect', k, card);
    }
  }
  if (o.kw) {  // a keyword given to a unit counts as that keyword on the side it lands on
    const who = on(to === null ? 'self' : to);
    if (o.kw === 'marked') { R.add('one'); }
    else if (who === 'own') { if (FLAG[o.kw]) FLAG[o.kw].forEach(r => R.add(r)); else if (!NONE.includes(o.kw)) miss('keyword given', o.kw, card); }
  }
}
function conds(c, R, card) {
  if (!c || typeof c !== 'object') return;
  for (const [k, v] of Object.entries(c)) { if (IF[k]) IF[k].forEach(r => R.add(r)); amountWords(v, R, card); }
}
function measure(card) {
  const R = new Set();
  for (const [k, v] of Object.entries(card)) {
    if (FLAG[k]) { if (v) FLAG[k].forEach(r => R.add(r)); } else if (!NONE.includes(k)) miss('card flag', k, card);
  }
  for (const f of card.fx || []) {
    if (ON[f.on]) ON[f.on].forEach(r => R.add(r)); else miss('trigger', f.on, card);
    conds(f.if, R, card);
    for (const o of f.do || []) { conds(o.if, R, card); effect(o, { on: f.on }, card, R); }
  }
  if (card.cast) for (const o of card.cast.do || []) { conds(o.if, R, card); effect(o, { on: 'cast' }, card, R); }
  for (const a of card.aura || []) {
    const who = side(a.to || 'self', null, {}, card);
    if (who === 'own') { if (positive(a.s)) R.add('grows'); if (positive(a.d)) R.add('growsdef'); if (BESIDE.includes(base(a.to || 'self'))) R.add('pos'); }
    else if (negative(a.s) || negative(a.d)) R.add('disrupts');
    conds(a.if, R, card); amountWords(a.per, R, card);
  }
  return R;
}

// the game's cards
const parts = fs.readFileSync(path.join(SRC, 'parts.txt'), 'utf8').split('\n').map(s => s.trim()).filter(n => /^js\/cards\//.test(n));
const ctx = {}; vm.createContext(ctx);
vm.runInContext(parts.map(n => fs.readFileSync(path.join(SRC, n), 'utf8')).join('\n') + ';globalThis.C = CARDS;', ctx);
const all = Object.values(ctx.C).filter(c => !c.token && c.fac), letters = [...new Set(all.map(c => c.fac))];
const fac = process.argv[2];
if (!letters.includes(fac)) { console.error(`usage: node tools/wheel_check.js <${letters.join('|')}> ["heals=1.6,stops=0.3"]`); process.exit(2); }
const plan = {};
for (const p of (process.argv[3] || '').split(',').filter(Boolean)) {
  const [k, v] = p.split('=');
  if (!RADII.some(r => r[0] === k) || isNaN(parseFloat(v))) { console.error(`unknown radius in the plan: ${p} (keys: ${RADII.map(r => r[0]).join(' ')})`); process.exit(2); }
  plan[k] = parseFloat(v);
}

// the library's average share per radius: per game the average of its factions, then the average of the games
const lib = {};
{
  const [head, ...lines] = fs.readFileSync(path.join(ROOT, 'library', 'cards_db', 'axes.tsv'), 'utf8').trim().split('\n').map(l => l.split('\t'));
  const col = Object.fromEntries(head.map((h, i) => [h, i]));
  for (const [key] of RADII) {
    const perGame = {};
    for (const l of lines) if (l[col.mode] === 'cards' && l[col[key + '_share']] !== '' && l[col[key + '_share']] !== undefined) (perGame[l[col.game]] = perGame[l[col.game]] || []).push(parseFloat(l[col[key + '_share']]));
    const avgs = Object.values(perGame).map(v => v.reduce((a, b) => a + b, 0) / v.length);
    lib[key] = avgs.length ? avgs.reduce((a, b) => a + b, 0) / avgs.length : null;
  }
}

// cheap and big units: the costs that cut nearest to a third of the game's units (as axes.py)
const units = all.filter(c => !c.tactic), costs = units.map(c => c.sup).sort((a, b) => a - b), uniq = [...new Set(costs)];
const third = n => uniq.reduce((best, t) => (Math.abs(n(t) - costs.length / 3) < Math.abs(n(best) - costs.length / 3) ? t : best), uniq[0]);
const lo = third(t => costs.filter(v => v <= t).length), hi = third(t => costs.filter(v => v >= t).length);
function shares(letter) {
  const cards = all.filter(c => c.fac === letter), us = cards.filter(c => !c.tactic), n = cards.length, s = {};
  const rs = cards.map(c => { const R = measure(c); if (!c.tactic && c.sup <= lo) R.add('wide'); if (!c.tactic && c.sup >= hi) R.add('tall'); sets.set(c, R); return R; });
  for (const [key] of RADII) s[key] = rs.filter(R => R.has(key)).length / n;
  s.together = rs.filter(R => R.has('pos')).length / n;
  s.strong = us.reduce((a, c) => a + c.str / c.sup, 0) / us.length; s.tough = us.reduce((a, c) => a + c.def / c.sup, 0) / us.length;
  return { s, n };
}
const mine = shares(fac), others = letters.map(l => shares(l).s);
const own = Object.fromEntries(OWN_NUMBERS.map(k => [k, others.reduce((a, s) => a + s[k], 0) / others.length]));
if (unknown.size) {
  console.log('NOT MAPPED (add each word to its table in tools/wheel_check.js):');
  for (const [k, names] of unknown) console.log(`  ${k}: ${names.size} cards, e.g. ${[...names].slice(0, 2).join(', ')}`);
  process.exit(1);
}
const pad = (t, n) => String(t).padEnd(n), num = v => (v === null || v === undefined ? '   -' : v.toFixed(2).padStart(4));
console.log(`Faction ${fac}: ${mine.n} cards. Value 1 = the average real faction (strength, defence, width: the average faction of this game).`);
console.log(`${pad('radius', 34)}${pad('share', 8)}${pad('value', 8)}${pad('planned', 9)}`);
let drifted = 0;
for (const [key, name] of RADII) {
  const sh = mine.s[key];
  let v = null, note = '';
  if (key === 'together') note = 'position only; no value (combos are not measured)';
  else if (key === 'strong' || key === 'tough') v = Math.pow(sh / own[key], POWER);
  else {
    const avg = OWN_NUMBERS.includes(key) ? own[key] : lib[key];
    if (avg) v = Math.pow((sh * mine.n + SHRINK * avg) / (mine.n + SHRINK) / avg, POWER); else note = 'no library average';
  }
  const p = plan[key];
  if (p !== undefined && v !== null && Math.abs(v - p) > DRIFT) { note = `DRIFTED (${v > p ? 'too high' : 'too low'})`; drifted++; }
  const shown = key === 'strong' || key === 'tough' ? sh.toFixed(2) + '/s' : Math.round(sh * 100) + '%';
  console.log(`${pad(name, 34)}${pad(shown, 8)}${pad(num(v), 8)}${pad(p === undefined ? '' : num(p), 9)}${note}`);
}
if (Object.keys(plan).length) console.log(drifted ? `${drifted} radii drifted more than ${DRIFT}: fix the faction, not the wheel.` : `No radius drifted more than ${DRIFT}.`);
process.exit(drifted ? 1 : 0);

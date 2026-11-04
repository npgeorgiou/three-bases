/* ---------- new factions (Nov 2026): compact card lines, effects in fx (rules/fx.js) ----------
   U(key, name, supply, strength, defence, size, extra, text): a unit; T(...): a token unit.
   S(key, name, cost, target, cast, text): a spell; target 'lane' | 'enemy' | 'own' | 'any' | 'column'. */
const FAC_GLYPH = { g: 'wheel', r: 'star', w: 'boot', e: 'hourglass', m: 'moon', c: 'clockface', d: 'sunskull', a: 'oxshield', b: 'eightcross', s: 'astar', o: 'oak', l: 'shell' };
const U = (key, name, sup, str, def, size, x, text) => [key, { name, size, sup, str, def, ...x, text }];
const T = (...a) => { const r = U(...a); r[1].token = true; return r; };
const S = (key, name, cost, tactic, cast, text, x = {}) => [key, { name, tactic, cost, cast, text, ...x }];
function addFaction(fac, rows) {
  for (const [k, v] of rows) {
    if (v.of) { for (const f of v.fx || []) f.of = f.of || v.of; delete v.of; }
    CARDS[k] = kwFx({ ...v, fac, art: v.art || FAC_GLYPH[fac] });
  }
}
// shorthands for effects
const ON = (on, ...ops) => ({ on, do: ops });
const ONCE = (on, ...ops) => ({ on, lim: 'round', do: ops });
const HOLD = { hold: 1 }, NOHOLD = { hold: 0 };
const RE = (...ops) => ON('roundEnd', ...ops), PL = (...ops) => ON('place', ...ops), DIE = (...ops) => ON('death', ...ops);
const STRIKE = { strike: 1 }, IT = 'it';
/* Keywords of the seven factions of 4 Nov 2026, written out as effects (their texts are in keywords.js). */
function kwFx(c) {
  const fx = c.fx ? c.fx.slice() : [], aura = c.aura ? c.aura.slice() : [];
  if (c.salvage) fx.push({ on: 'death', do: [{ card: 'c_part' }] });
  if (c.wound) fx.push({ on: 'place', do: [{ tick: 'self' }] });
  if (c.toll) aura.push({ to: 'self', s: c.toll, per: { count: 'deathsR' } });
  if (c.obsidian) c.headsman = 1;
  if (c.onrush) fx.push({ on: 'allyAttack', do: [{ buff: [c.onrush, 0], rnd: 1, to: 'self' }] });
  if (c.flanker) aura.push({ to: 'self', s: c.flanker, if: { front: 1, side: 1 } });
  if (c.reserve) fx.push({ on: 'allyDeath', if: { back: 1 }, do: [{ advance: 1 }] });
  if (c.harden) fx.push({ on: 'survive', do: [{ buff: [0, c.harden], to: 'self' }] });
  if (c.retaliate) fx.push({ on: 'survive', do: [{ dmg: c.retaliate, to: 'it' }] });
  if (c.vigil) fx.push({ on: 'roundEnd', do: [{ heal: c.vigil, to: 'self' }] });
  if (c.perennial) fx.push({ on: 'roundEnd', do: [{ buff: [c.perennial, c.perennial], to: 'self' }] });
  if (c.seeds) fx.push({ on: 'death', do: [{ token: 'o_sapling', n: c.seeds }] });
  if (c.roots) fx.push({ on: 'roundEnd', do: [{ dmg: c.roots, to: 'facing' }] });
  if (c.entrench) aura.push({ to: 'self', arm: 1, if: { front: 1, min: ['behind', 1] } });
  if (c.barrage) fx.push({ on: 'roundEnd', do: [{ dmg: c.barrage, to: 'deepest' }] });
  if (fx.length) c.fx = fx;
  if (aura.length) c.aura = aura;
  return c;
}

/* ---------- new factions (Nov 2026): compact card lines, effects in fx (rules/fx.js) ----------
   U(key, name, supply, strength, defence, size, extra, text): a unit; T(...): a token unit.
   S(key, name, cost, target, cast, text): a spell; target 'lane' | 'enemy' | 'own' | 'any' | 'column'. */
const FAC_GLYPH = { g: 'wheel', r: 'star', w: 'boot', e: 'hourglass', m: 'moon' };
const U = (key, name, sup, str, def, size, x, text) => [key, { name, size, sup, str, def, ...x, text }];
const T = (...a) => { const r = U(...a); r[1].token = true; return r; };
const S = (key, name, cost, tactic, cast, text, x = {}) => [key, { name, tactic, cost, cast, text, ...x }];
function addFaction(fac, rows) {
  for (const [k, v] of rows) {
    if (v.of) { for (const f of v.fx || []) f.of = f.of || v.of; delete v.of; }
    CARDS[k] = { ...v, fac, art: FAC_GLYPH[fac] };
  }
}
// shorthands for effects
const ON = (on, ...ops) => ({ on, do: ops });
const ONCE = (on, ...ops) => ({ on, lim: 'round', do: ops });
const HOLD = { hold: 1 }, NOHOLD = { hold: 0 };

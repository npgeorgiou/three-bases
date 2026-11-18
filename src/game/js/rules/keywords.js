/* ---------- keywords a unit has, strength and defence, costs ---------- */
const KW_FLAGS = ['ranged', 'fixed'];
/** The value of keyword flag f on unit u (its card's). */
const kw = (u, f) => cardOf(u)[f] || 0;

// dmg: lost shields
const strengthOf = u => printedStr(u);
const defenceOf = u => Math.max(0, printedDef(u) - (u.dmg || 0));
/** One move and one attack per unit per round; each costs the unit's supply. */
const attackCost = u => unitSupply(u);
const moveCost = u => unitSupply(u);




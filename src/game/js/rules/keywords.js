/* ---------- keywords a unit has (printed, gained or moved away) ---------- */
const KW_FLAGS = ['ranged', 'reach', 'armoured', 'fixed', 'revenant', 'plague', 'incorp', 'afterlife', 'fade', 'riposte', 'flurry'];
const KW_NAME = { ranged: 'Ranged', reach: 'Pike', armoured: 'Armoured', fixed: 'Immobile', revenant: 'Revenant', plague: 'Plague',
  incorp: 'Incorporeal', afterlife: 'Afterlife', fade: 'Fading', riposte: 'Riposte', flurry: 'Flurry' };
/** The value of keyword flag f on unit u: gained keywords (u.kw) count, keywords moved away (u.off) don't. */
const kw = (u, f) => (u.kw && u.kw[f] ? u.kw[f] : u.off && u.off[f] ? 0 : cardOf(u)[f] || 0);
/** Give unit u keyword f (copy-on-write, so cloned states stay independent). */
const giveKw = (u, f, v = 1) => { u.kw = { ...(u.kw || {}), [f]: v }; if (u.off && u.off[f]) u.off = { ...u.off, [f]: false }; };
const isIncorp = u => !!(kw(u, 'incorp') || u.tInc);

// bs/bd: position bonuses (recomputed), ts: until round end, ps/pd: permanent, dmg: lost shields
const strengthOf = u => Math.max(0, printedStr(u) + (u.bs || 0) + (u.ts || 0) + (u.ps || 0));
const defenceOf = u => Math.max(0, printedDef(u) + (u.bd || 0) + (u.pd || 0) + (u.td || 0) - (u.dmg || 0));
const maxMoves = u => cardOf(u).moves || 1;
/** Whether the unit itself still has an attack / a move this round (supply and targets aside). */
const canAttackAgain = u => !u.attacked;
/** Flurry: two attacks per round, only the first paid. */
const maxAttacks = u => (kw(u, 'flurry') ? 2 : 1);
const attackCost = u => (kw(u, 'flurry') && (u.atk || 0) >= 1 ? 0 : unitSupply(u));
/** What u's next move costs: Lightfooted units pay only for their first move of the round. */
const moveCost = u => (cardOf(u).lightfooted && (u.mv || 0) >= 1 ? 0 : unitSupply(u));
const canMoveAgain = u => (u.mv || 0) < maxMoves(u);
/** Bloodied: the unit's defence is below its card's printed defence. */
const isBloodied = u => defenceOf(u) < printedDef(u);
const isReckless = u => !!(cardOf(u).reckless || u.reck);
/** Armoured: printed, or given until round end (Strategikon). */
const isArmoured = u => !!(kw(u, 'armoured') || u.tArm);

/** Resolution order (section 7, option B): page order of the whole board from the seat of the unit's controller. */
const readingKey = u => seatKey(u, ctl(u));
const byReadingOrder = (a, b) => readingKey(a) - readingKey(b);

/** Enemies of p in a lane: nearest row first. */
function enemyOrder(s, p, lane, frontOnly) {
  const q = other(p);
  const rows = frontOnly ? [frontRow(q)] : q === 1 ? [2, 1, 0] : [0, 1, 2];
  const cols = p === 0 ? [0, 1, 2] : [2, 1, 0];
  const out = [];
  for (const camp of frontOnly ? [q] : [q, p]) {
    const map = occupancy(s, camp, lane), rs = camp === q ? rows : camp === 1 ? [2, 1, 0] : [0, 1, 2];
    for (const r of rs) for (const c of cols) {
      const u = map[r + ',' + c];
      if (u && ctl(u) === q && !out.includes(u)) out.push(u);
    }
  }
  return out;
}


/* =====================================================================
   ifelse AI: sees everything (both hands, the real position) and searches it. No rules of thumb:
   every judgement is a weighted term, and every weight, width and switch is a tunable value.
   Starting values: the game's Benchmark's (goal lanes start off).
   ===================================================================== */
/** [key, label, type, start, extra]: type int [lo, hi] | switch | share (0.01–1) | num (scale used when at 0). The start is the
 *  game's Benchmark value where it has one (listed here: the earlier Benchmark's), so tuning improves on the Benchmark.
 *  How far it looks is not tuned: tuning games use the tuning depth, and the check match the Benchmark's own depth. */
const IFELSE_BASE_FIELDS = [
  ['w1', 'Own moves examined (1st move)', 'int', 8, [1, 16]], ['w2', 'Replies examined (2nd move)', 'int', 6, [1, 16]],
  ['w3', 'Moves examined (3rd move)', 'int', 4, [1, 16]], ['w4', 'Moves examined (4th move)', 'int', 4, [1, 12]],
  ['w5', 'Moves examined (5th move)', 'int', 4, [1, 12]],
  ['skipPointless', 'Skip moves that change nothing (1 = yes)', 'switch', 1],
  ['base', 'Worth of holding a base', 'num', 220], ['dot', 'Worth of a dot', 'num', 45],
  ['secondBase', 'Holding one base: per own dot in the other lanes', 'num', 30],
  ['twoBases', 'Holding two bases', 'num', 300], ['twoBasesOpp', 'Opponent holding two bases (counted against)', 'num', 450],
  ['income', 'Per supply of lane income', 'num', 12], ['incomeCap', 'Lane income counted up to', 'int', 6, [1, 12]],
  ['safeIncome', 'Share income keeps in a lane already safely won', 'share', 0.3],
  ['pool', 'Per unspent supply this round', 'num', 3], ['carry', 'Per carry-over', 'num', 10],
  ['hand', 'Per card in hand (own minus opponent\'s)', 'num', 4],
  ['handCost', 'Per supply cost of cards in hand (own minus opponent\'s)', 'num', 0, 1],
  ['uSup', 'Unit worth per supply it costs', 'num', 10], ['uStr', 'Unit worth per strength', 'num', 2],
  ['uDef', 'Unit worth per defence', 'num', 3], ['uSupBonus', 'Unit worth per supply cost plus supply bonus', 'num', 5],
  ['front', 'Bonus for a unit in the front row (with strength, or defence above 1)', 'num', 6],
  ['safeHolders', 'Won lane: front units counted in full', 'int', 2, [0, 4]],
  ['safeExtra', 'Won lane: share counted for the other units', 'share', 0.1],
  ['armyStep', 'Contested lane: each further unit counts this much less', 'share', 0.15],
  ['armyFloor', 'Contested lane: least share a unit counts', 'share', 0.3],
  ['threat', 'Multiplier on threats', 'num', 1], ['kill', 'Threat: share of a unit\'s worth lost when it can be killed', 'share', 0.6],
  ['damage', 'Threat: per point of damage when it can\'t be killed', 'num', 2],
  ['thMineOpp', 'Opponent to move: weight of own exposure', 'num', 1], ['thTheirsOpp', 'Opponent to move: weight of its exposure', 'num', 0.3],
  ['thTheirsMe', 'Own move: weight of the opponent\'s exposure', 'num', 0.9], ['thMineMe', 'Own move: weight of own exposure', 'num', 0.3],
  ['tOnce', 'Threat: each attacker once, supply shared (1 = yes)', 'switch', 1],
  ['tGuards', 'Threat: Bodyguards protect neighbours (1 = yes)', 'switch', 1],
  ['tActed', 'Threat: units that attacked this round threaten nothing (1 = yes)', 'switch', 1],
  ['danger0', 'Out of supply with no units left', 'num', 1000], ['danger1', 'Out of supply with 1 unit left', 'num', 300],
  ['danger2', 'Out of supply with 2 units left', 'num', 100], ['draw', 'Worth of a draw', 'num', -500],
  ['goals', 'Goal lanes (1 = on)', 'switch', 0], ['offGoal', 'Goal lanes: share the third lane counts', 'share', 0.7],
  ['stick', 'Goal lanes: preference for keeping last turn\'s', 'num', 1.5],
  ['needDots', 'Goal lanes: per missing own dot', 'num', 2], ['needEnemyDots', 'Goal lanes: per enemy dot', 'num', 1.5],
  ['needEnemyPower', 'Goal lanes: per enemy strength and defence', 'num', 0.15], ['needOwnPower', 'Goal lanes: per own strength and defence (less needed)', 'num', 0.1],
  ['needSupply', 'Goal lanes: per own lane supply (less needed)', 'num', 0.2],
  ['killPref', 'First move: extra per worth of the enemy units it kills', 'num', 1],
  ['passPen', 'First move: passing right after the opponent passed counts less by', 'num', 40],
  ['freeCheck', 'Skip free moves that don\'t make the round better (1 = yes)', 'switch', 1],
];
/** Effect values: what each kind of unit effect is worth per point (op_<what>, starts at 0) and how much its timing
 *  counts (on_<when>, a multiplier, starts at 1), over the effect parts of the game's unit cards (fxParts). */
const IFELSE_FX_FIELDS = (() => {
  const whats = new Set(), whens = new Set();
  for (const key of Object.keys(CARDS)) if (CARDS[key].sup) for (const [when, what] of fxParts(key)) { whens.add(when); whats.add(what); }
  const say = { s: 'strength an aura gives', d: 'defence an aura gives' };
  return [...[...whats].sort().map(w => ['op_' + w, `Effect worth per point: ${say[w] || w}`, 'num', 0, 1]),
    ...[...whens].sort().map(w => ['on_' + w, `Effect timing multiplier: ${w}`, 'num', 1])];
})();
const IFELSE_FIELDS = [...IFELSE_BASE_FIELDS, ...IFELSE_FX_FIELDS].map(([k, text, type, def, extra]) => [k, text, type, BENCH_VALUES[k] ?? def, extra]);
const IFELSE_DEFAULTS = Object.fromEntries(IFELSE_FIELDS.map(f => [f[0], f[3]]));
/** The ifelse AI's values: its starting values with the given ones on top, looking as far ahead as the Benchmark. */
const ifelseFull = cfg => ({ depth: BENCH_VALUES.depth, ...IFELSE_DEFAULTS, ...(cfg || {}) });


/* ---------- small helpers ---------- */
const other = p => 1 - p;
const CARD_MAP = new Map(Object.entries(CARDS));   // faster than looking a key up in the big CARDS object
const cardOf = u => CARD_MAP.get(u.card);
const unitName = u => cardOf(u).name;
const unitSupply = u => (u.sup !== undefined ? u.sup : cardOf(u).sup);
/** The deck card a card key stands for (a card carrying changes back to the hand has a key of its own). */
const baseKey = k => (CARDS[k] && CARDS[k].base) || k;
/**
 * A unit going back to the hand keeps its lasting changes (stats, gained and lost keywords): the hand card is a copy of
 * its deck card carrying them, keyed by its content so the same changes always give the same key.
 */
function carriedCard(u) {
  const base = baseKey(u.card), b = CARDS[base], ps = u.ps || 0, pd = u.pd || 0;
  const kwG = Object.fromEntries(Object.entries(u.kw || {}).filter(([, v]) => v)), off = Object.keys(u.off || {}).filter(f => u.off[f]);
  if (!ps && !pd && !Object.keys(kwG).length && !off.length) return base;
  const mods = { ps, pd, kw: kwG, off: Object.fromEntries(off.map(f => [f, true])) }, key = base + '~' + JSON.stringify(mods);
  if (!CARD_MAP.has(key)) {
    const sign = (n, w) => `${n > 0 ? '+' : '−'}${Math.abs(n)} ${w}`;
    const parts = [ps && sign(ps, 'strength'), pd && sign(pd, 'defence'), ...Object.keys(kwG).map(f => `gained [[${KW_NAME[f]}]]`), ...off.map(f => `lost [[${KW_NAME[f]}]]`)].filter(Boolean);
    const c = { ...b, base, mods, text: (b.text ? b.text + ' ' : '') + 'Kept from the battlefield: ' + parts.join(', ') + '.' };
    CARDS[key] = c; CARD_MAP.set(key, c);
  }
  return key;
}
/** Printed strength / defence of a unit (a resurrected or returned unit has its own lowered values). */
const printedStr = u => (u.pS !== undefined ? u.pS : cardOf(u).str);
const printedDef = u => (u.pD !== undefined ? u.pD : cardOf(u).def);
const deckName = (s, p) => DECKS[s.players[p].deck].name;

function shuffle(list) {
  for (let i = list.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [list[i], list[j]] = [list[j], list[i]];
  }
  return list;
}

/** Copy of a state deep enough to play on independently (units and lists are copied), without pending events. */
function cloneState(s) {
  const list = x => x.slice();
  return {
    ...s,
    players: s.players.map(P => ({ ...P, hand: list(P.hand), discard: list(P.discard), draw: list(P.draw), dealt: list(P.dealt || []), redrawn: list(P.redrawn || []) })),
    units: s.units.map(u => ({ ...u })),
    owner: list(s.owner), ownerStart: list(s.ownerStart), pool: s.pool.map(list), poolStart: s.poolStart.map(list),
    pending: s.pending ? { ...s.pending } : null, arrQ: s.arrQ ? s.arrQ.slice() : null, tombs: s.tombs ? s.tombs.slice() : [], resStack: [], depth: 0, chainN: 0,
    log: list(s.log), fx: [], ev: [],
  };
}

/* ---------- geometry ---------- */
/**
 * A shape is a card's size (1–4, standard shapes in orientation 'h' or 'v') or, for a unit with a shape of its own
 * (a Link merge, a growing mass), its list of cell offsets; such a shape turns in quarter turns (orientation 0–3).
 * Every shape's offsets start at row 0 and column 0, so a unit's (r, c) is the top-left corner of its shape.
 */
function shapeCells(size, o) {
  if (Array.isArray(size)) return turnShape(size, typeof o === 'number' ? o : 0);
  if (size === 1) return [[0, 0]];
  if (size === 4) return [[0, 0], [0, 1], [1, 0], [1, 1]];
  return Array.from({ length: size }, (_, i) => (o === 'h' ? [0, i] : [i, 0]));
}
/** Offsets moved so the shape starts at row 0 and column 0, in reading order. */
const normShape = cells => {
  const r0 = Math.min(...cells.map(x => x[0])), c0 = Math.min(...cells.map(x => x[1]));
  return cells.map(([r, c]) => [r - r0, c - c0]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
};
/** A custom shape turned clockwise by n quarter turns. */
function turnShape(offs, n) {
  let cells = offs;
  for (let i = 0; i < n; i++) cells = cells.map(([r, c]) => [c, -r]);
  return normShape(cells);
}
/** The orientations a shape can take: h/v for sizes 2 and 3; each distinct quarter turn for a custom shape. */
function orientations(size) {
  if (!Array.isArray(size)) return size === 2 || size === 3 ? ['h', 'v'] : ['h'];
  const seen = new Set(), out = [];
  for (let n = 0; n < 4; n++) { const key = JSON.stringify(turnShape(size, n)); if (!seen.has(key)) { seen.add(key); out.push(n); } }
  return out;
}
const CELLS_CACHE = new Map();
const cellsAt = (size, r, c, o) => {
  if (Array.isArray(size)) return shapeCells(size, o).map(([dr, dc]) => [r + dr, c + dc]);
  const key = ((size * 2 + (o === 'v' ? 1 : 0)) * 64 + (r + 32)) * 64 + (c + 32);
  let cells = CELLS_CACHE.get(key);
  if (!cells) {
    cells = shapeCells(size, o).map(([dr, dc]) => Object.freeze([r + dr, c + dc]));
    Object.freeze(cells);
    CELLS_CACHE.set(key, cells);
  }
  return cells;
};
/** A unit's shape: its own cells if it has them (u.sh, at orientation 0), else its card's size. */
const shapeOf = u => u.sh || cardOf(u).size;
const cellsOf = u => cellsAt(shapeOf(u), u.r, u.c, u.o);
/** Cell offsets of unit u's shape in orientation o. */
const offsetsOf = (u, o) => shapeCells(shapeOf(u), o);
const orientationsOf = u => orientations(shapeOf(u));
const frontRow = p => (p === 0 ? 0 : ROWS - 1);
const backRow = p => (p === 0 ? ROWS - 1 : 0);
/** Row step toward the base (forward) for side p. */
const fwd = p => (p === 0 ? -1 : 1);
const inFront = u => cellsOf(u).some(([r]) => r === frontRow(u.owner));
const inBack = u => cellsOf(u).some(([r]) => r === backRow(u.owner));
const rowsOf = u => [...new Set(cellsOf(u).map(x => x[0]))];
const colsOf = u => [...new Set(cellsOf(u).map(x => x[1]))];
/** Columns in which u stands in its own front row. */
const frontCols = u => new Set(cellsOf(u).filter(([r]) => r === frontRow(u.owner)).map(x => x[1]));
const inCamp = (r, c) => r >= 0 && c >= 0 && r < ROWS && c < COLS;

/** The cells a shape would cover, or null if it leaves the camp. */
function regionAt(size, r, c, o) {   // size: a shape (see shapeCells)
  const cells = cellsAt(size, r, c, o);
  return cells.every(([x, y]) => inCamp(x, y)) ? cells : null;
}

/* ---------- queries ---------- */
/** The side that controls a unit: its owner (the camp it stands in), unless it is controlled from the other side (u.ctl). */
const ctl = u => (u.ctl ?? u.owner);
/** Units side p controls in a lane (including any it controls in the enemy camp). */
const unitsIn = (s, p, lane) => s.units.filter(u => ctl(u) === p && u.lane === lane);
const byId = (s, id) => s.units.find(u => u.id === id) || null;
const basesHeld = (s, p) => s.owner.filter(o => o === p).length;
/** Bases p holds now and also held when the round started (the win condition). */
const basesKept = (s, p) => s.owner.filter((o, l) => o === p && s.ownerStart[l] === p).length;

function occupancy(s, p, lane) {
  const map = {};
  for (const u of s.units) if (u.owner === p && u.lane === lane) for (const [r, c] of cellsOf(u)) map[r + ',' + c] = u;
  return map;
}
const unitAt = (s, p, lane, r, c) => occupancy(s, p, lane)[r + ',' + c] || null;

function fits(s, p, lane, size, r, c, o, ignoreId) {
  return fitsCells(s, p, lane, shapeCells(size, o), r, c, ignoreId);
}
/** Cells of camp p in `lane` still held by tombstones (units dead but not resolved yet), or null. */
function tombCells(s, p, lane) {
  if (!s.tombs || !s.tombs.length) return null;
  const set = new Set();
  for (const t of s.tombs) if (t.owner === p && t.lane === lane && !t.res) for (const [r, c] of t.cells) set.add(r + ',' + c);
  return set.size ? set : null;
}
/** Whether a shape given as cell offsets fits at (r, c) in p's camp of `lane`. */
function fitsCells(s, p, lane, offs, r, c, ignoreId) {
  const cells = offs.map(([dr, dc]) => [r + dr, c + dc]);
  if (!cells.every(([x, y]) => inCamp(x, y))) return false;
  const map = occupancy(s, p, lane), tomb = tombCells(s, p, lane);
  return cells.every(([x, y]) => { const u = map[x + ',' + y]; return (!u || u.id === ignoreId) && !(tomb && tomb.has(x + ',' + y)); });
}

/** Two units of the same camp sharing at least one row (a is not u). */
const sharesRow = (u, a) => a.id !== u.id && a.owner === u.owner && ctl(a) === ctl(u) && a.lane === u.lane && cellsOf(a).some(([r]) => rowsOf(u).includes(r));

/** Enemies in the enemy front row of u's lane, in u's columns (the units right ahead of it). */
function facingEnemies(s, u) {
  const q = other(u.owner), map = occupancy(s, q, u.lane), out = [];
  for (const c of colsOf(u)) { const t = map[frontRow(q) + ',' + c]; if (t && ctl(t) !== ctl(u) && !out.includes(t)) out.push(t); }
  return out;
}
/** Whether a stands in the 3x3 square around one of u's cells, in the same camp. */
const adjacent = (u, a) => a.id !== u.id && a.owner === u.owner && ctl(a) === ctl(u) && a.lane === u.lane
  && cellsOf(a).some(([r, c]) => cellsOf(u).some(([ur, uc]) => Math.abs(r - ur) <= 1 && Math.abs(c - uc) <= 1));
/** Allies around u (the 3x3 square around each of its cells, within its camp). */
const adjacentAllies = (s, u) => s.units.filter(a => a.id !== u.id && a.owner === u.owner && ctl(a) === ctl(u) && a.lane === u.lane
  && cellsOf(a).some(([r, c]) => cellsOf(u).some(([ur, uc]) => Math.abs(r - ur) <= 1 && Math.abs(c - uc) <= 1)));

/** Units directly left or right of any of u's cells, in the same row (in cell order, as before). */
function besideUnits(s, u) {
  const mine = cellsOf(u), out = [], cands = s.units.filter(x => x.id !== u.id && x.owner === u.owner && x.lane === u.lane && ctl(x) === ctl(u));
  if (!cands.length) return out;
  for (const [r, c] of mine) for (const dc of [-1, 1]) {
    const x = cands.find(v => cellsOf(v).some(([vr, vc]) => vr === r && vc === c + dc));
    if (x && !out.includes(x)) out.push(x);
  }
  return out;
}
/** Cells directly in front of u (toward the base), in its own columns, that u does not cover itself. */
function frontCellsOf(u) {
  const own = new Set(cellsOf(u).map(x => x.join())), out = [];
  for (const [r, c] of cellsOf(u)) { const R = r + fwd(u.owner); if (inCamp(R, c) && !own.has(R + ',' + c)) out.push([R, c]); }
  return out;
}
/** Units standing directly behind u (away from the base), in its own columns. */
function unitsBehind(s, u) {
  const own = new Set(cellsOf(u).map(x => x.join())), map = occupancy(s, u.owner, u.lane), out = [];
  for (const [r, c] of cellsOf(u)) {
    const R = r - fwd(u.owner), x = map[R + ',' + c];
    if (inCamp(R, c) && !own.has(R + ',' + c) && x && !out.includes(x)) out.push(x);
  }
  return out;
}

/** Supply a unit adds to its lane at the start of each round. */
const unitIncome = u => Math.max(0, unitSupply(u) + (cardOf(u).bonus || 0) + (cardOf(u).backBonus && inBack(u) ? cardOf(u).backBonus : 0) - (u.blight ? 1 : 0));
/** Supply a lane gives its owner at the start of each round. */
function laneSupply(s, p, lane) {
  let sum = 0;
  for (const u of s.units) if (ctl(u) === p && u.lane === lane) sum += unitIncome(u);
  return sum;
}


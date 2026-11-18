/* ---------- small helpers ---------- */
const other = p => 1 - p;
const CARD_MAP = new Map(Object.entries(CARDS));   // faster than looking a key up in the big CARDS object
const cardOf = u => CARD_MAP.get(u.card);
const unitName = u => cardOf(u).name;
const unitSupply = u => cardOf(u).sup;
/** Printed strength / defence of a unit: its card's. */
const printedStr = u => cardOf(u).str;
const printedDef = u => cardOf(u).def;
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
    log: list(s.log), fx: [],
  };
}

/* ---------- geometry ---------- */
/** A shape is a card's size: 1 cell, a line of 2 or 3 (orientation 'h' or 'v'), or 4 (2x2). (r, c) is its top-left cell. */
function shapeCells(size, o) {
  if (size === 1) return [[0, 0]];
  if (size === 4) return [[0, 0], [0, 1], [1, 0], [1, 1]];
  return Array.from({ length: size }, (_, i) => (o === 'h' ? [0, i] : [i, 0]));
}
/** The orientations a shape can take: h/v for sizes 2 and 3. */
const orientations = size => (size === 2 || size === 3 ? ['h', 'v'] : ['h']);
const CELLS_CACHE = new Map();
const cellsAt = (size, r, c, o) => {
  const key = ((size * 2 + (o === 'v' ? 1 : 0)) * 64 + (r + 32)) * 64 + (c + 32);
  let cells = CELLS_CACHE.get(key);
  if (!cells) {
    cells = shapeCells(size, o).map(([dr, dc]) => Object.freeze([r + dr, c + dc]));
    Object.freeze(cells);
    CELLS_CACHE.set(key, cells);
  }
  return cells;
};
const cellsOf = u => cellsAt(cardOf(u).size, u.r, u.c, u.o);
/** Cell offsets of unit u's shape in orientation o. */
const offsetsOf = (u, o) => shapeCells(cardOf(u).size, o);
const orientationsOf = u => orientations(cardOf(u).size);
const frontRow = p => (p === 0 ? 0 : ROWS - 1);
const inFront = u => cellsOf(u).some(([r]) => r === frontRow(u.owner));
/** Rows a unit covers, worked out once per cell list (cell lists of standard shapes are shared and never change). */
const ROWS_OF = new WeakMap();
const rowsOf = u => { const cl = cellsOf(u); let r = ROWS_OF.get(cl); if (!r) { r = Object.freeze([...new Set(cl.map(x => x[0]))]); ROWS_OF.set(cl, r); } return r; };
const inCamp = (r, c) => r >= 0 && c >= 0 && r < ROWS && c < COLS;

/** The cells a shape would cover, or null if it leaves the camp. */
function regionAt(size, r, c, o) {   // size: a shape (see shapeCells)
  const cells = cellsAt(size, r, c, o);
  return cells.every(([x, y]) => inCamp(x, y)) ? cells : null;
}

/* ---------- queries ---------- */
/** Units of side p in a lane. */
const unitsIn = (s, p, lane) => s.units.filter(u => u.owner === p && u.lane === lane);
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
/** Whether a shape given as cell offsets fits at (r, c) in p's camp of `lane`. */
function fitsCells(s, p, lane, offs, r, c, ignoreId) {
  const cells = offs.map(([dr, dc]) => [r + dr, c + dc]);
  if (!cells.every(([x, y]) => inCamp(x, y))) return false;
  const map = occupancy(s, p, lane);
  return cells.every(([x, y]) => { const u = map[x + ',' + y]; return !u || u.id === ignoreId; });
}




/** Supply a unit adds to its lane at the start of each round. */
const unitIncome = u => unitSupply(u) + (cardOf(u).bonus || 0);
/** No lane holds more than this much supply for one player. */
const LANE_SUPPLY_MAX = 12;
/** Supply a lane gives its owner at the start of each round. */
function laneSupply(s, p, lane) {
  let sum = 0;
  for (const u of s.units) if (u.owner === p && u.lane === lane) sum += unitIncome(u);
  return Math.min(LANE_SUPPLY_MAX, sum);
}


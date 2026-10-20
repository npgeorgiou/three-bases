/* =====================================================================
   APP STATE
   ===================================================================== */
const settings = { mode: 'ai' };  // mode: 'ai' or 'hot' (same screen)
/** Which computer player the game uses: 'bench' (the Benchmark) or 'random'. Remembered in this browser. */
const AI_STORE = 'threeBases.v2.ai';
const aiChoice = (() => { try { return JSON.parse(localStorage.getItem(AI_STORE) || 'null') || {}; } catch (e) { return {}; } })();
if (!['bench', 'random'].includes(aiChoice.kind)) aiChoice.kind = 'bench';
function saveAiChoice() { try { localStorage.setItem(AI_STORE, JSON.stringify(aiChoice)); } catch (e) { /* not remembered */ } }
function computerRedraw(s, p) { if (aiChoice.kind === 'random') randomRedraw(s, p); else aiMulligan(s, p); }
function chooseComputerMove(s) {
  if (aiChoice.kind === 'random') return randomMove(listActions(s).map(a => ({ a }))).a;
  return chooseIfelseAction(s, BENCH_VALUES);
}
let game = null;            // current game state
let ui = {};                // current selection / interaction mode
let drag = null;            // pointer drag in progress
let busy = false, aiThinking = false;           // animations or the computer are running
let hoverCard = null, hoverLane = null, hoverUnitId = null, lastPointer = 'mouse';

function resetUi() { ui = { mode: null, hi: null, id: null, o: 'h', anchor: null, err: '', free: false, tid: null }; }
const isHuman = p => settings.mode === 'hot' || p === 0;
/** Whose view the screen shows. */
const viewer = () => (replay ? 0 : settings.mode === 'hot' ? game.cur : 0);
const myTurn = () => !!game && !replay && game.winner === null && !busy && isHuman(game.cur) && $('#cover').hidden;
const selectedUnit = () => (ui.id ? byId(game, ui.id) : null);
const handCard = i => game.players[game.cur].hand[i];
/** The follow-up choice the human player must make now, if any. */
const pend = () => (game && game.pending && isHuman(game.cur) && game.winner === null ? game.pending : null);
/** Ids of the units the pending choice can pick. */
const pendingPicks = () => new Set(pend() ? listActions(game).filter(a => a.t === 'pick').map(a => a.tid) : []);
/** The legal use of hand spell hi matching `want` (e.g. {lane}, {tid}), or null. */
function spellMatch(hi, want) {
  const k = handCard(hi);
  return spellOptions(game, game.cur, k, false).find(o => Object.keys(want).every(key => o[key] === want[key])) || null;
}
const SPELL_MODES = ['lane', 'column', 'own', 'enemy', 'any'];

/* =====================================================================
   BOARD GEOMETRY (SVG units)
   ===================================================================== */
const CELL = 64, LANE_X = [12, 226, 440], TOP_Y = 23, BAND_Y = 228, BAND_H = 44, BOTTOM_Y = 285, VIEW_H = 501;
const SIDE_PAD = 6, SUP_SIZE = 16;   // active-side panel padding around a camp; camp supply bread size (the row sits outside the panel)
const campY = owner => (owner === 1 ? TOP_Y : BOTTOM_Y);
const cellXY = (lane, owner, r, c) => [LANE_X[lane] + c * CELL, campY(owner) + r * CELL];

/** [x, y, width, height] of a unit on the board. */
function unitRect(u) {
  const corners = cellsOf(u).map(([r, c]) => cellXY(u.lane, u.owner, r, c));
  const x0 = Math.min(...corners.map(p => p[0])), y0 = Math.min(...corners.map(p => p[1]));
  return [x0, y0, Math.max(...corners.map(p => p[0])) + CELL - x0, Math.max(...corners.map(p => p[1])) + CELL - y0];
}
const cellRect = (svg, lane, owner, r, c, cls, inset = 3) => {
  const [x, y] = cellXY(lane, owner, r, c);
  return svgEl('rect', { x: x + inset, y: y + inset, width: CELL - 2 * inset, height: CELL - 2 * inset, rx: inset + 4, class: cls }, svg);
};
const crossPath = (x0, y0, x1, y1) => `M${x0} ${y0}L${x1} ${y1}M${x1} ${y0}L${x0} ${y1}`;

/**
 * Reach: what an ability touches, for highlighting. cells: [owner, lane, r, c] of the area (row, column, cells
 * beside / in front, a whole camp); ids: units it would hit, buff or pick (marked orange).
 */
function newReach() {
  const cells = new Map(), ids = new Set();
  return {
    cells, ids,
    cell(owner, lane, r, c) { if (inCamp(r, c)) cells.set([owner, lane, r, c].join(), [owner, lane, r, c]); },
    camp(owner, lane) { for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) this.cell(owner, lane, r, c); },
    rows(owner, lane, rows) { for (const r of rows) for (let c = 0; c < COLS; c++) this.cell(owner, lane, r, c); },
    unit(u) { if (u) ids.add(u.id); },
    list() { return [...cells.values()]; },
  };
}
/** What unit u's abilities reach from where it stands in state s (placing: also its Place effect and charge), read from the scopes. */
function unitReach(s, u, placing = false) {
  const R = newReach(), own = new Set(cellsOf(u).map(x => x.join()));
  for (const f of abilitiesOf(u, placing)) {
    for (const [o, l, r, c] of areaOf(s, u, f)) if (!(o === u.owner && own.has(r + ',' + c))) R.cell(o, l, r, c);
    targetsOf(s, u, f).forEach(t => R.unit(t));
  }
  return R;
}
/** What spell k (as action a) reaches: its declared area and the units it affects. */
function spellReach(s, p, k, a) {
  const R = newReach();
  for (const [o, l, r, c] of spellArea(s, p, k, a)) R.cell(o, l, r, c);
  spellTargets(s, p, k, a).forEach(u => R.unit(u));
  return R;
}
/** Pending choices: the camp they pick in. */
const PENDING_AREA = { pull: 'foe', defect: 'foe', duel: 'foe', kiss: 'foe', cinder: 'own', surgeon: 'own', embalm: 'own' };   // placing choices (place, free moves) mark their open cells instead
/** What a pending follow-up choice reaches: where its picks are, the unit it started from, and (Cinder Imp) the enemy it damages next. */
function pendingReach(s, P) {
  const R = newReach(), side = PENDING_AREA[P.k];
  if (side) for (const x of campCells(side === 'own' ? P.p : other(P.p), P.lane)) R.cell(...x);
  const src = byId(s, P.src);
  if (P.k === 'cinder' && src) targetsOf(s, src, 'place:cinder').filter(t => ctl(t) !== P.p).forEach(t => R.unit(t));
  if (P.k === 'pair') { const v = byId(s, P.vid); if (v) AREA.beside(s, v).forEach(x => R.cell(...x)); }
  return R;
}


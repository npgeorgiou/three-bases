/* =====================================================================
   APP STATE
   ===================================================================== */
const settings = { mode: 'ai' };  // mode: 'ai' or 'hot' (same screen)
/** Which computer player the game uses: 'bench' (the Benchmark), 'random', or 'ifelse' (an ifelse AI exported by the AI lab:
 *  aiChoice.ifelse = its name and values, which include how far it looks). Remembered in this browser. */
const AI_STORE = 'threeBases.v2.ai';
const aiChoice = (() => { try { return JSON.parse(localStorage.getItem(AI_STORE) || 'null') || {}; } catch (e) { return {}; } })();
const ifelseFileOk = f => !!f && f.kind === 'ifelse' && !!f.values && typeof f.values === 'object' && Number.isFinite(f.values.depth);
if (!['bench', 'random'].includes(aiChoice.kind) && !(aiChoice.kind === 'ifelse' && ifelseFileOk(aiChoice.ifelse))) aiChoice.kind = 'bench';
function saveAiChoice() { try { localStorage.setItem(AI_STORE, JSON.stringify(aiChoice)); } catch (e) { /* not remembered */ } }
function computerRedraw(s, p) { if (aiChoice.kind === 'random') randomRedraw(s, p); else aiMulligan(s, p); }
function chooseComputerMove(s) {
  if (aiChoice.kind === 'random') return randomMove(listActions(s).map(a => ({ a }))).a;
  return chooseIfelseAction(s, aiChoice.kind === 'ifelse' ? aiChoice.ifelse.values : BENCH_VALUES);
}
let game = null;            // current game state
let ui = {};                // current selection / interaction mode
let drag = null;            // pointer drag in progress
let busy = false, aiThinking = false;           // animations or the computer are running
let hoverCard = null, hoverLane = null, hoverUnitId = null, lastPointer = 'mouse';

function resetUi() { ui = { mode: null, hi: null, id: null, o: 'h', anchor: null, err: '' }; }
const isHuman = p => settings.mode === 'hot' || p === 0;
/** Whose view the screen shows. */
const viewer = () => (replay ? 0 : settings.mode === 'hot' ? game.cur : 0);
const myTurn = () => !!game && !replay && game.winner === null && !busy && isHuman(game.cur) && $('#cover').hidden;
const selectedUnit = () => (ui.id ? byId(game, ui.id) : null);
const handCard = i => game.players[game.cur].hand[i];

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

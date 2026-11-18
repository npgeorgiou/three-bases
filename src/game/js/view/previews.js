/* =====================================================================
   PREVIEWS: what the hovered action would do
   ===================================================================== */
/** Top-left anchor for a shape of `size` centred under the pointer cell `c`. */
function placeAt(c, size, o) {
  const cells = shapeCells(size, o);
  const rows = Math.max(...cells.map(x => x[0])) + 1, cols = Math.max(...cells.map(x => x[1])) + 1;
  return {
    ...c,
    r: Math.max(0, Math.min(ROWS - rows, Math.round(c.fr - rows / 2))),
    c: Math.max(0, Math.min(COLS - cols, Math.round(c.fc - cols / 2))),
  };
}

/**
 * What is being placed now (a deploy or a move): {size, test(lane, r, c, o)}, or null.
 * test says whether that spot is legal; the same test serves the pointer preview and the cells marked as open.
 */
function placingNow() {
  const p = game.cur;
  if (ui.mode === 'deploy') {
    const k = handCard(ui.hi);
    if (!k) return null;
    return { size: CARDS[k].size, owner: p, lanes: LANES, card: k, test: (lane, r, c, o) => canDeploy(game, p, ui.hi, lane, r, c, o) };
  }
  if (ui.mode === 'unit') {
    const u = selectedUnit();
    if (!u) return null;
    return { size: cardOf(u).size, owner: u.owner, lanes: [u.lane], unit: u, test: (lane, r, c, o) => lane === u.lane && !!moveTargets(game, u, o)[r + ',' + c] };
  }
  return null;
}
/**
 * Placement under the pointer: {a: anchor, o: orientation, ok, cells}. The chosen orientation is used if it fits there;
 * otherwise the unit turns to an orientation that fits (auto-rotation), so a fitting spot never shows red.
 */
function placementInfo() {
  const a0 = ui.anchor, W = placingNow();
  if (!a0 || !W || a0.owner !== W.owner || !W.lanes.includes(a0.lane)) return null;
  const u = W.unit;
  if (u) { const under = unitAt(game, W.owner, a0.lane, a0.r, a0.c); if (under && under.id === u.id && ui.o === u.o) return null; }
  const list = orientations(W.size), order = [ui.o, ...list.filter(o => o !== ui.o)];
  let first = null;
  for (const o of order) {
    if (!list.includes(o)) continue;
    const a = placeAt(a0, W.size, o), info = { a, o, ok: W.test(a0.lane, a.r, a.c, o), cells: regionAt(W.size, a.r, a.c, o) };
    if (info.ok) return info;
    if (!first) first = info;
  }
  return first;
}
/** Cells of the camps where what is being placed could go (any orientation): marked as open (green dashed). */
function openCells() {
  const W = placingNow(), out = new Map();
  if (!W) return [];
  for (const lane of W.lanes) for (const o of orientations(W.size)) for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++)
    if (W.test(lane, r, c, o)) for (const [x, y] of cellsAt(W.size, r, c, o)) {
      const t = unitAt(game, W.owner, lane, x, y);
      if (t && !(W.unit && t.id === W.unit.id)) continue;   // only free cells
      out.set([W.owner, lane, x, y].join(), [W.owner, lane, x, y]);
    }
  return [...out.values()];
}

/** The action the pointer is on right now, if it is legal: {a: action, mover?: id}. */
function hoverAction() {
  if (!myTurn()) return null;
  const a0 = ui.anchor, unitUnder = a0 ? unitAt(game, a0.owner, a0.lane, a0.r, a0.c) : null;
  if (ui.mode === 'deploy') {
    const place = placementInfo();
    if (!place || !place.ok) return null;
    const { lane, r, c: col } = place.a;
    return { a: { t: 'deploy', hi: ui.hi, lane, r, c: col, o: place.o } };
  }
  if (ui.mode === 'unit' && a0) {
    const u = selectedUnit();
    if (!u) return null;
    if (a0.owner !== u.owner) return unitUnder && canAttack(game, u, unitUnder) ? { a: { t: 'attack', id: u.id, tid: unitUnder.id } } : null;
    const place = placementInfo();
    if (!place || !place.ok) return null;
    const { r, c: col } = place.a;
    return { a: { t: 'move', id: u.id, r, c: col, o: place.o }, mover: u.id };
  }
  return null;
}

/**
 * Compare the live game with a future state t (the hovered action played on a copy, or the round-end forecast):
 * fx[id] = 'kill' | 'aff', disp[id] = unit with its new stats, loss[p][lane] = supply lost, state = t.
 */
function diffStates(t, skipId) {
  const out = { fx: {}, disp: {}, state: t };
  out.loss = [0, 1].map(p => LANES.map(l => Math.max(0, laneSupply(game, p, l) - laneSupply(t, p, l))));
  for (const u of game.units) {
    if (u.id === skipId) continue;
    const v = byId(t, u.id);
    if (!v) { out.fx[u.id] = 'kill'; continue; }
    if (strengthOf(v) !== strengthOf(u) || defenceOf(v) !== defenceOf(u)) { out.disp[u.id] = v; out.fx[u.id] = 'aff'; }
  }
  return out;
}

function simulate(h) {
  const t = cloneState(game);
  t.noFx = true;
  try { applyAction(t, h.a); } catch (e) { return null; }
  // the unit being placed or moved: a new unit takes the next id
  const placedId = h.mover ?? (h.a.t === 'deploy' ? game.nid : undefined);
  const out = diffStates(t, placedId);
  out.placed = placedId !== undefined ? byId(t, placedId) : null;
  out.placedRef = h.mover !== undefined ? byId(game, h.mover) : null;
  return out;
}

function canDeployInLane(hi, lane) {
  const k = handCard(hi), c = CARDS[k];
  if (!canPay(game, lane, c.cost)) return false;
  for (let r = 0; r < ROWS; r++) for (let col = 0; col < COLS; col++)
    for (const o of orientations(c.size)) if (fits(game, game.cur, lane, c.size, r, col, o)) return true;
  return false;
}

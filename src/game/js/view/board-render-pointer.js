/** The hand card that is selected, or else hovered. */
function activeHandCard() {
  if (!myTurn()) return null;
  const hi = ui.mode === 'deploy' ? ui.hi : ui.mode ? null : hoverCard;
  return hi !== null && hi !== undefined ? hi : null;
}
/** Lanes where the active hand card can be placed. */
function lanesForHandCard() {
  const lanes = new Set(), hi = activeHandCard();
  if (hi !== null) for (const lane of LANES) if (canDeployInLane(hi, lane)) lanes.add(lane);
  return lanes;
}

/** Where the active card can't be placed, darkened (instead of frames around the places it can). */
function darkZones(fitLanes) {
  const out = [];
  if (activeHandCard() !== null)
    for (const lane of LANES) for (const owner of [0, 1]) if (owner !== game.cur || !fitLanes.has(lane)) out.push({ lane, owner });
  return out;
}
const zoneShade = (svg, z) => svgEl('rect', { x: LANE_X[z.lane] - 4, y: campY(z.owner) - 4, width: CELL * 3 + 8, height: CELL * ROWS + 8, rx: 10, class: 'shade' }, svg);

/**
 * The legal choices of the selected unit, from the engine's list of actions (nothing per card):
 * targets (units it can attack) and kills (attacks that would kill, by playing them on a copy).
 */
function legalChoices(sel) {
  const out = { targets: new Set(), kills: new Set() };
  if (!myTurn() || !sel || ui.mode !== 'unit') return out;
  for (const a of listActions(game)) {
    if (a.t !== 'attack' || a.id !== sel.id) continue;
    out.targets.add(a.tid);
    const t = cloneState(game); t.noFx = true; applyAction(t, a);
    if (!byId(t, a.tid)) out.kills.add(a.tid);
  }
  return out;
}

/**
 * Draw the board for state B (the live game, or an animation snapshot).
 * opt: anim (snapshot), spawn (unit id), mover / path / mo (move animation), forecast (round-end state).
 */
function renderBoard(B = game, opt = {}) {
  const svg = $('#board');
  svg.innerHTML = '';
  const live = B === game && !opt.anim && !opt.forecast;
  const hover = live ? hoverAction() : null;
  const preview = opt.forecast ? diffStates(opt.forecast) : hover ? simulate(hover) : null;
  if (live) actPreview = hover ? preview : null;
  const basesFrom = opt.forecast || B;
  const fitLanes = live ? lanesForHandCard() : new Set();

  if (B.winner === null || B.winner === undefined) drawActiveSide(svg, B.cur);
  for (const lane of LANES) {
    for (const p of [1, 0]) {
      drawCampCells(svg, B, p, lane);
      drawSupplyBar(svg, B, p, lane, { preview, act: live && hover ? preview : null });
    }
    drawBase(svg, basesFrom, lane);
  }

  if (opt.path) {
    const u = B.units.find(x => x.id === opt.mover), size = cardOf(u).size;
    for (const [r, c] of opt.path.slice(1))
      for (const [x, y] of cellsAt(size, r, c, opt.mo ?? u.o)) cellRect(svg, u.lane, u.owner, x, y, 'mvpath');
  }

  // interaction overlays
  const sel = live ? selectedUnit() : null;
  const legal = live ? legalChoices(sel) : { targets: new Set(), kills: new Set() };
  // where the unit being placed or moved can go: only the cells that can take it (any orientation)
  if (live) for (const [owner, lane, r, c] of openCells()) cellRect(svg, lane, owner, r, c, 'aurazone');

  // markers, drawn above every unit so a dimmed unit never dims them: one role per unit
  const marks = new Map(), mark = (id, role) => { if (id !== undefined && id !== null && !marks.has(id)) marks.set(id, role); };
  if (sel) mark(sel.id, 'pick');
  if (preview) for (const id in preview.fx) if (preview.fx[id] === 'kill') mark(+id, 'kill');
  legal.kills.forEach(id => mark(id, 'kill'));
  legal.targets.forEach(id => mark(id, 'tgt'));
  if (preview) for (const id in preview.fx) if (preview.fx[id] === 'aff') mark(+id, 'tgt');
  // the hovered legal target
  let hovT = hover && hover.a.tid !== undefined ? hover.a.tid : undefined;
  if (hovT == null && live) {   // a marked unit under the pointer with no action hovered yet
    const u = hoverUnitId !== null ? byId(game, hoverUnitId) : ui.anchor ? unitAt(game, ui.anchor.owner, ui.anchor.lane, ui.anchor.r, ui.anchor.c) : null;
    if (u && marks.get(u.id) === 'tgt') hovT = u.id;
  }
  for (const u of B.units) {
    let cls = '';
    if (live && drag && drag.on && drag.id === u.id) cls += ' lift';
    if (opt.spawn === u.id) cls += ' spawn placed';
    if (opt.mover === u.id) cls += ' mv';
    if (live && B.pool[u.owner][u.lane] + B.players[u.owner].reserve < unitSupply(u)) cls += ' nosup';   // can't afford any action
    const shown = preview && preview.disp[u.id];
    drawUnit(svg, shown ? { ...shown, attacked: u.attacked, moved: u.moved } : u, cls, shown ? { s: strengthOf(u), d: defenceOf(u) } : null);
    if (opt.forecast && shown && defenceOf(shown) < defenceOf(u)) {        // shields lost at round end
      const [x0, y0, w] = unitRect(u), bw = Math.min(28, (Math.min(w, CELL * 2) - 8) / 3), lost = defenceOf(u) - defenceOf(shown);
      const g = svgEl('g', { class: 'hitmark' }, svg), cx = Math.min(x0 + w - 4 - bw / 2, x0 + w - 21), cy = y0 + 4 + bw + 13;
      svgEl('rect', { x: cx - 15, y: cy - 10, width: 30, height: 20, rx: 10 }, g);
      svgEl('text', { x: cx, y: cy }, g).textContent = '−' + lost;
    }
    if (preview && preview.fx[u.id] === 'kill') {
      const [x0, y0, w, h] = unitRect(u);
      svgEl('path', { d: crossPath(x0 + 10, y0 + 10, x0 + w - 10, y0 + h - 10), class: 'deathx' }, svg);
    }
  }
  // camps where the card can't be placed are darkened (above the units, below the markers)
  if (live) for (const z of darkZones(fitLanes)) zoneShade(svg, z);
  for (const [id, role] of marks) {
    const u = B.units.find(x => x.id === id);
    if (u) drawMark(svg, u, role + (id === hovT ? ' hov' : ''));
  }
  if (hovT !== undefined && !marks.has(hovT)) { const u = B.units.find(x => x.id === hovT); if (u) drawMark(svg, u, 'tgt hov'); }
  if (!live) return;
  updateCarryPreview();
  updateDrawPreview(hover, preview);
  const place = placementInfo();
  if (place && place.ok && preview && preview.placed) {
    // the real unit where it would end up, its stats coloured against its card (a move: against its current stats)
    const v = preview.placed, was = preview.placedRef;
    drawUnit(svg, v, ' pvnew', was ? { s: strengthOf(was), d: defenceOf(was) } : null);
    cursorOutline(svg, place);
  } else if (place && place.ok) cursorOutline(svg, place); else if (place && place.cells && !(ui.mode === 'unit' && sel && !hasMoves(sel))) {
    // an invalid spot: red only on its free cells, never over other units
    for (const [r, c] of place.cells) {
      const t = unitAt(game, place.a.owner, place.a.lane, r, c);
      if (!t || (sel && t.id === sel.id)) cellRect(svg, place.a.lane, place.a.owner, r, c, 'pv no');
    }
  }
}

/** Cards the hovered action would draw: shown as card backs at the end of that hand. */
function updateDrawPreview(hover, preview) {
  $$('.drawghost').forEach(x => x.remove());
  if (!hover || !preview || !preview.state) return;
  const t = preview.state, v = viewer();
  for (const [p, sel] of [[v, '#hand'], [other(v), '#oppHand']]) {
    const used = p === game.cur && hover.a.t === 'deploy' ? 1 : 0;
    const n = t.players[p].hand.length - game.players[p].hand.length + used;
    if (n <= 0) continue;
    const box = $(sel), items = [...box.children], fac = DECKS[game.players[p].deck].fac, own = sel === '#hand';
    const w = items.length ? items[0].offsetWidth : 100, step = items.length > 1 ? items[1].offsetLeft - items[0].offsetLeft : w + Math.max(22, w * 0.3);
    const startLeft = items.length ? items[items.length - 1].offsetLeft + step : box.clientWidth / 2 - w / 2;
    for (let i = 0; i < n; i++) {
      const d = document.createElement('div');
      d.className = (own ? 'drawghost back f-' : 'drawghost oback f-') + fac;
      d.innerHTML = deckArt(fac);
      d.style.left = startLeft + i * step + 'px';
      box.appendChild(d);
    }
  }
}
/** Where the pointer puts the unit: a dashed white outline that stays with the pointer. */
function cursorOutline(svg, place) {
  if (!place.cells) return;
  const xy = place.cells.map(([r, c]) => cellXY(place.a.lane, place.a.owner, r, c));
  const x0 = Math.min(...xy.map(p => p[0])), y0 = Math.min(...xy.map(p => p[1]));
  const x1 = Math.max(...xy.map(p => p[0])) + CELL, y1 = Math.max(...xy.map(p => p[1])) + CELL;
  svgEl('rect', { x: x0 + 3, y: y0 + 3, width: x1 - x0 - 6, height: y1 - y0 - 6, rx: 8, class: 'pvcur' }, svg);
}

/* ---------- pointer → board coordinates ---------- */
function toSvgPoint(x, y) {
  const svg = $('#board'), pt = svg.createSVGPoint(), m = svg.getScreenCTM();
  pt.x = x; pt.y = y;
  return m ? pt.matrixTransform(m.inverse()) : null;
}
/** Camp cell under a screen point: {lane, owner, r, c, fr, fc} (fr/fc = fractional position). */
function cellFromPoint(x, y) {
  const q = toSvgPoint(x, y);
  if (!q) return null;
  for (const lane of LANES) {
    const fc = (q.x - LANE_X[lane]) / CELL;
    if (fc < 0 || fc >= COLS) continue;
    for (const owner of [1, 0]) {
      const fr = (q.y - campY(owner)) / CELL;
      if (fr >= 0 && fr < ROWS) return { lane, owner, r: Math.floor(fr), c: Math.floor(fc), fr, fc };
    }
  }
  return null;
}
function laneFromPoint(x, y) {
  const q = toSvgPoint(x, y);
  if (!q) return null;
  return LANES.find(l => q.x >= LANE_X[l] - 12 && q.x <= LANE_X[l] + CELL * 3 + 12) ?? null;
}
const placementKey = a => (a ? [a.lane, a.owner, a.r, a.c].join() : '');


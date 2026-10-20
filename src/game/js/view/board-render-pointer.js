/** The hand card that is selected, or else hovered. */
function activeHandCard() {
  if (!myTurn()) return null;
  const hi = ['deploy', ...SPELL_MODES].includes(ui.mode) ? ui.hi : ui.mode ? null : hoverCard;
  return hi !== null && hi !== undefined ? hi : null;
}
/** Lanes where a unit card can be placed. */
function lanesForHandCard() {
  const lanes = new Set(), hi = activeHandCard();
  if (hi !== null && !CARDS[handCard(hi)].tactic) for (const lane of LANES) if (canDeployInLane(hi, lane)) lanes.add(lane);
  return lanes;
}
/** For a spell card: {lane: castable} for every lane, or null for unit cards. */
function spellLanes() {
  const hi = activeHandCard();
  if (hi === null || pend()) return null;
  const k = handCard(hi), c = CARDS[k];
  if (!c.tactic) return null;
  const opts = spellOptions(game, game.cur, k, false), out = {};
  for (const lane of LANES) out[lane] = opts.some(o => spellLane(game, o) === lane);
  return out;
}
const laneFrame = (svg, lane, cls) =>
  svgEl('rect', { x: LANE_X[lane] - 9, y: TOP_Y - 6, width: CELL * 3 + 18, height: BOTTOM_Y + ROWS * CELL - TOP_Y + 12, rx: 14, class: cls }, svg);

/**
 * Where the active card or choice can't act, darkened (instead of frames around the places it can):
 * a unit card darkens every camp it can't be placed in; a spell darkens the lanes it can't be cast on;
 * a follow-up choice darkens the other lanes.
 */
function darkZones(fitLanes, spells, P) {
  const out = [];
  if (P) {
    // the lanes the choice can act in: its picks' lanes, or the lane it places or moves in
    const used = new Set();
    for (const a of listActions(game)) {
      if (a.t === 'pick') { const t = byId(game, a.tid); if (t) used.add(t.lane); }
      else if (a.t === 'place' || a.t === 'fmove') used.add(P.lane);
    }
    if (used.size) for (const lane of LANES) if (!used.has(lane)) out.push({ lane });
    return out;
  }
  if (spells) { for (const lane of LANES) if (!spells[lane]) out.push({ lane }); return out; }
  const hi = activeHandCard();
  if (hi !== null && !CARDS[handCard(hi)].tactic)
    for (const lane of LANES) for (const owner of [0, 1]) if (owner !== game.cur || !fitLanes.has(lane)) out.push({ lane, owner });
  return out;
}
function zoneShade(svg, z) {
  if (z.owner === undefined) return svgEl('rect', { x: LANE_X[z.lane] - 9, y: TOP_Y - 6, width: CELL * 3 + 18, height: BOTTOM_Y + ROWS * CELL - TOP_Y + 12, rx: 14, class: 'shade' }, svg);
  return svgEl('rect', { x: LANE_X[z.lane] - 4, y: campY(z.owner) - 4, width: CELL * 3 + 8, height: CELL * ROWS + 8, rx: 10, class: 'shade' }, svg);
}

/**
 * The legal choices of the current selection, from the engine's list of actions (nothing per card):
 * targets (units it can attack, throw, cast on or pick), kills (attacks that would kill, by playing them on a copy),
 * cells (free cells it can move to, land on or be placed in).
 */
function legalChoices(sel) {
  const out = { targets: new Set(), kills: new Set(), cells: [] };
  const P = pend(), spellMode = ['own', 'enemy', 'any'].includes(ui.mode);
  if (!myTurn() || !(sel || P || spellMode)) return out;
  const acts = listActions(game, false), seen = new Set(), card = spellMode ? handCard(ui.hi) : null;
  const cellsFor = (owner, lane, size, r, c, o) => {
    for (const [x, y] of cellsAt(size, r, c, o)) { const k = [owner, lane, x, y].join(); if (!seen.has(k)) { seen.add(k); out.cells.push([owner, lane, x, y]); } }
  };
  for (const a of acts) {
    if (sel && ui.mode === 'unit' && a.id === sel.id) {
      if (a.t === 'attack') {
        out.targets.add(a.tid);
        const t = cloneState(game); t.noFx = true; applyAction(t, a);
        if (!byId(t, a.tid)) out.kills.add(a.tid);
      } else if (a.t === 'throw') out.targets.add(a.aid);
    } else if (sel && ui.mode === 'throw' && a.t === 'throw' && a.id === sel.id && a.aid === ui.tid) {
      const t = unitAt(game, a.owner, a.lane, a.r, a.c);
      if (t) out.targets.add(t.id); else out.cells.push([a.owner, a.lane, a.r, a.c]);
    } else if (spellMode && a.t === 'tactic' && handCard(a.hi) === card) out.targets.add(a.vid ?? a.tid);
    else if (P && a.t === 'pick') out.targets.add(a.tid);
    else if (P && a.t === 'fmove' && !sel) out.targets.add(a.id);
  }
  if (ui.mode === 'throw') out.targets.add(ui.tid);
  return out;
}

/**
 * Draw the board for state B (the live game, or an animation snapshot).
 * opt: anim (snapshot), spawn (unit id), mover / path / mo (move animation).
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
  const spells = live ? spellLanes() : null;
  if (opt.anim && animFx && animFx.lane !== null) {   // the spell being cast: its lane or column
    if (animFx.col !== null) for (let r = 0; r < ROWS; r++) cellRect(svg, animFx.lane, animFx.foe, r, animFx.col, 'colhl', 2);
    else laneFrame(svg, animFx.lane, 'lanehl');
  }

  if (opt.path) {
    const u = B.units.find(x => x.id === opt.mover), size = shapeOf(u);
    for (const [r, c] of opt.path.slice(1))
      for (const [x, y] of cellsAt(size, r, c, opt.mo ?? u.o)) cellRect(svg, opt.toLane !== undefined ? opt.toLane : u.lane, u.owner, x, y, 'mvpath');
  }

  // interaction overlays
  const sel = live ? selectedUnit() : null;
  if (live && ui.mode === 'lane' && hoverLane !== null && (!spells || spells[hoverLane])) laneFrame(svg, hoverLane, 'lanehl');
  // reach: what the hovered action, choice or unit affects (area cells green, affected units orange)
  const reach = live ? currentReach(hover, preview) : null;
  if (reach) for (const [owner, lane, r, c] of reach.list()) cellRect(svg, lane, owner, r, c, 'aurazone');
  const P = live ? pend() : null;
  // the legal choices of the current selection, straight from the engine's list of actions
  const legal = live ? legalChoices(sel) : { targets: new Set(), kills: new Set(), cells: [] };
  for (const [owner, lane, r, c] of legal.cells) cellRect(svg, lane, owner, r, c, 'reach', 2);
  // where the unit being placed or moved can go: only the cells that can take it (any orientation)
  if (live) for (const [owner, lane, r, c] of openCells()) cellRect(svg, lane, owner, r, c, 'aurazone');
  if (live && ui.mode === 'column' && ui.anchor && ui.anchor.owner !== game.cur) {
    const ok = !!spellMatch(ui.hi, { lane: ui.anchor.lane, col: ui.anchor.c });
    for (let r = 0; r < ROWS; r++) cellRect(svg, ui.anchor.lane, ui.anchor.owner, r, ui.anchor.c, ok ? 'colhl' : 'colhl no', 2);
  }

  // markers, drawn above every unit so a dimmed unit never dims them: one role per unit
  const marks = new Map(), mark = (id, role) => { if (id !== undefined && id !== null && !marks.has(id)) marks.set(id, role); };
  if (sel) mark(sel.id, 'pick');
  if (live && ui.mode === 'throw' && ui.tid) mark(ui.tid, 'pick');   // the ally picked to be thrown
  if (P && P.vid) mark(P.vid, 'pick');
  if (P && P.k === 'place' && P.tid) mark(P.tid, 'pick');
  if (opt.anim && animFx && animFx.tid !== undefined) mark(animFx.tid, 'tgt');
  if (preview) for (const id in preview.fx) if (preview.fx[id] === 'kill') mark(+id, 'kill');
  legal.kills.forEach(id => mark(id, 'kill'));
  legal.targets.forEach(id => mark(id, 'tgt'));
  if (reach) reach.ids.forEach(id => mark(id, 'tgt'));
  if (preview) for (const id in preview.fx) if (preview.fx[id] === 'aff') mark(+id, 'tgt');
  // the hovered legal target
  let hovT = hover && (hover.a.tid !== undefined ? hover.a.tid : hover.a.t === 'tactic' ? hover.a.vid
    : hover.a.t === 'throw' ? (unitAt(game, hover.a.owner, hover.a.lane, hover.a.r, hover.a.c) || {}).id : undefined);   // a throw onto a unit: that unit
  if (hovT == null && live) {   // a marked unit under the pointer with no action hovered yet (e.g. an ally the Ogre Thrower can pick)
    const u = hoverUnitId !== null ? byId(game, hoverUnitId) : ui.anchor ? unitAt(game, ui.anchor.owner, ui.anchor.lane, ui.anchor.r, ui.anchor.c) : null;
    if (u && marks.get(u.id) === 'tgt') hovT = u.id;
  }
  for (const u of B.units) {
    if (u.aloft) continue;
    let cls = '';
    if (live && drag && drag.on && drag.id === u.id) cls += ' lift';
    if (opt.spawn === u.id) cls += ' spawn placed';
    if (opt.merged === u.id) cls += ' merged';
    if (opt.mover === u.id) cls += ' mv';
    if (live && B.pool[ctl(u)][u.lane] + B.players[ctl(u)].reserve < Math.min(unitSupply(u), canMoveAgain(u) && !cardOf(u).fixed ? moveCost(u) : Infinity)) cls += ' nosup';   // can't afford any action
    const shown = preview && preview.disp[u.id];
    const ug = drawUnit(svg, shown ? { ...shown, mv: u.mv, atk: u.atk, attacked: u.attacked, moved: u.moved } : u, cls,
      shown ? { s: strengthOf(u), d: defenceOf(u) } : null);
    if (!opt.forecast) {   // a gained stat puffs on its badge once
      const st = [strengthOf(u), defenceOf(u) + Math.max(0, u.dmg || 0)], was = prevStats.get(u.id);
      if (was) [['k-str', st[0] > was[0]], ['k-def', st[1] > was[1]]].forEach(([k, up]) => { const b = up && ug.querySelector('.' + k); if (b) gainPuff(ug, b); });
      prevStats.set(u.id, st);
    }
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
  // camps or lanes where the card or choice can't act are darkened (above the units, below the markers)
  if (live) for (const z of darkZones(fitLanes, spells, P)) zoneShade(svg, z);
  for (const [id, role] of marks) {
    const u = B.units.find(x => x.id === id);
    if (u) drawMark(svg, u, role + (id === hovT ? ' hov' : ''));
  }
  if (hovT !== undefined && !marks.has(hovT)) { const u = B.units.find(x => x.id === hovT); if (u) drawMark(svg, u, 'tgt hov'); }
  // tombstones: units dead in this step whose death hasn't resolved yet
  $$('#fxLayer .tombfly').forEach(x => x.remove());
  for (const t of B.tombs || []) drawTomb(svg, B, t);
  // units the preview would add (Shades, Abominations, spawns), drawn as they would stand
  if (preview && preview.added) for (const v of preview.added) drawUnit(svg, v, ' pvnew');
  if (!live) return;
  updateCarryPreview();
  updateDrawPreview(hover, preview);
  const GP = pend();
  if (GP && GP.k === 'grave' && GP.pool && ui.gk) {
    const spot = freeSpots(game, GP.p, GP.lane, ui.gk)[0];
    if (spot) for (const [r, c] of cellsAt(CARDS[ui.gk].size, spot.r, spot.c, spot.o)) cellRect(svg, GP.lane, GP.p, r, c, 'pv ok');
  }
  const place = placementInfo();
  if (hover && hover.a.t === 'throw' && preview && preview.placed) drawUnit(svg, preview.placed, ' pvnew', { s: strengthOf(preview.placedRef), d: defenceOf(preview.placedRef) });
  else if (place && place.ok && preview && preview.placed) {
    // the real unit where it would end up, its stats coloured against its card (a move: against its current stats)
    const v = preview.placed, was = preview.placedRef;
    drawUnit(svg, v, ' pvnew', was ? { s: strengthOf(was), d: defenceOf(was) } : null);
    cursorOutline(svg, place);
  } else if (place && place.ok && preview && preview.placedDead) {
    // it dies where it ends up (e.g. struck back after its charge): drawn there with the death X
    const v = preview.placedDead, [x0, y0, w, h] = unitRect(v);
    drawUnit(svg, v, ' pvnew', preview.placedRef ? { s: strengthOf(preview.placedRef), d: defenceOf(preview.placedRef) } : null);
    svgEl('path', { d: crossPath(x0 + 10, y0 + 10, x0 + w - 10, y0 + h - 10), class: 'deathx' }, svg);
    cursorOutline(svg, place);
  } else if (place && place.ok) cursorOutline(svg, place); else if (place && place.cells && (place.ok || !(ui.mode === 'unit' && sel && !hasMoves(sel, ui.free)))) {
    // an invalid spot: red only on its free cells, never over other units
    for (const [r, c] of place.cells) {
      const t = unitAt(game, place.a.owner, place.a.lane, r, c);
      if (place.ok || !t || (sel && t.id === sel.id)) cellRect(svg, place.a.lane, place.a.owner, r, c, 'pv ' + (place.ok ? 'ok' : 'no'));
    }
  }
}

/** Cards the hovered action would draw (or bring back to a hand): shown as card backs at the end of that hand. */
function updateDrawPreview(hover, preview) {
  $$('.drawghost').forEach(x => x.remove());
  if (!hover || !preview || !preview.state) return;
  const t = preview.state, v = viewer();
  for (const [p, sel] of [[v, '#hand'], [other(v), '#oppHand']]) {
    const used = p === game.cur && (hover.a.t === 'deploy' || hover.a.t === 'tactic') ? 1 : 0;
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
/** A dead unit that hasn't left yet: its pawn dimmed under a tombstone; while its death resolves, a white cell border and a lit stone. */
function drawTomb(svg, B, t) {
  const spot = t, xy = spot.cells.map(([r, c]) => cellXY(spot.lane, spot.owner, r, c));
  const x0 = Math.min(...xy.map(p => p[0])), y0 = Math.min(...xy.map(p => p[1]));
  const w = Math.max(...xy.map(p => p[0])) + CELL - x0, h = Math.max(...xy.map(p => p[1])) + CELL - y0, size = Math.min(w, h) * 0.62;
  const taken = B.units.some(v => v.lane === spot.lane && v.owner === spot.owner && cellsOf(v).some(([r, c]) => spot.cells.some(([R, C]) => R === r && C === c)));
  if (t.u && !taken) drawUnit(svg, t.u, ' deadpawn');
  const g = svgEl('g', { class: 'tomb' + (t.res && B.resNow === t.id ? ' now' : ''), 'data-tomb': t.id }, svg);   // lit: only the death being resolved now
  if (t.res) svgEl('rect', { x: x0 + 1, y: y0 + 1, width: w - 2, height: h - 2, rx: 9, class: 'tombcell' }, g);
  if (!taken) {
    const inner = svgEl('svg', { x: x0 + (w - size) / 2, y: y0 + (h - size) / 2 + size * 0.08, width: size, height: size, viewBox: '0 0 100 100' }, g);
    inner.innerHTML = '<path class="tst" d="M24 92V40C24 18 76 18 76 40V92Z"/><path class="tsx" d="M50 36V70M38 48H62"/><path class="tsg" d="M12 92H88"/>';
  }
}
/** Where the pointer puts the unit: a dashed white outline that stays with the pointer (the preview may end elsewhere, e.g. after a Charge). */
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


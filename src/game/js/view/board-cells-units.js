/* =====================================================================
   BOARD RENDERING
   ===================================================================== */
function drawActiveSide(svg, cur) {
  // the panel wraps the camps with the same padding on every side, clear of the bases; camp supply sits just outside it
  const y = (cur === 1 ? TOP_Y : BOTTOM_Y) - SIDE_PAD, h = ROWS * CELL + 2 * SIDE_PAD;
  svgEl('rect', { x: LANE_X[0] - 14, y, width: LANE_X[2] + CELL * 3 + 28 - LANE_X[0], height: h, rx: 16, class: 'activeside' }, svg);
}

function drawCampCells(svg, B, p, lane) {
  const taken = new Set();
  for (const u of B.units) if (u.owner === p && u.lane === lane) for (const [r, c] of cellsOf(u)) taken.add(r + ',' + c);
  for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++)
    if (!taken.has(r + ',' + c)) cellRect(svg, lane, p, r, c, 'cell' + (r === frontRow(p) ? ' frontrow' : ''), 2);
  // one merged cell under each unit
  for (const u of B.units) if (u.owner === p && u.lane === lane) {
    const [x0, y0, w, h] = unitRect(u), cls = 'mcell' + (inFront(u) ? ' frontrow' : '');
    if (cellsOf(u).length !== (w / CELL) * (h / CELL)) svgEl('path', { d: shapeOutline(u, 2), class: cls }, svg);   // a non-rectangular shape
    else svgEl('rect', { x: x0 + 2, y: y0 + 2, width: w - 4, height: h - 4, rx: 6, class: cls }, svg);
  }
}

/**
 * Bread row under/over a camp: this round's supply (spent ones faded, the pending cost pulsing),
 * then next round's extra supply (empty outline), then gains from the hovered action (green),
 * with an X over supply the hovered action would destroy.
 */
/**
 * A camp's supply: this round's bread (spent ones faded), next round's extra as empty bread.
 * act: the hovered action's simulated result; the supply it would take pulses, the supply it would add shows green.
 */
function drawSupplyBar(svg, B, p, lane, { preview, act }) {
  const g = svgEl('g', { class: 'supbar' }, svg);
  const y = p === 1 ? 0 : BOTTOM_Y + ROWS * CELL + SIDE_PAD + 1;
  const total = B.poolStart[p][lane], left = B.pool[p][lane];
  const extra = Math.max(0, laneSupply(B, p, lane) - total);
  const t = act && act.state;
  const spend = t ? Math.max(0, left - t.pool[p][lane]) : 0;
  const gained = t ? Math.max(0, t.pool[p][lane] - left) + Math.max(0, laneSupply(t, p, lane) - laneSupply(B, p, lane)) : 0;
  const count = total + extra + gained;
  const size = Math.min(SUP_SIZE, (CELL * 3 - 8) / Math.max(1, count));
  const x0 = LANE_X[lane] + CELL * 1.5 - count * size / 2;
  const pending = i => i >= left - spend;
  for (let i = 0; i < count; i++) {
    const x = x0 + i * size;
    if (i < total) {
      const icon = svgBread(g, i < left ? (pending(i) ? 'pend' : 'sup') : 'spent', x, y, size);
      if (i < left) icon.setAttribute('data-left', p + '-' + lane);
    } else if (i < total + extra) {
      svgBread(g, 'next', x, y, size);
    } else svgBread(g, 'gain', x, y, size);
  }
  const lost = preview && preview.loss ? Math.min(preview.loss[p][lane], total + extra) : 0;
  for (let i = 0; i < lost; i++) {
    const x = x0 + (total + extra - 1 - i) * size;
    svgEl('path', { d: crossPath(x + 2, y + 2, x + size - 2, y + size - 2), class: 'supx' }, g);
  }
}

function drawBase(svg, B, lane) {
  // the base's colour: who holds it now; a frame set apart from it, in the same colours: who held it when the round started
  // (green = bottom side, red = top side)
  const owner = B.owner[lane], start = (B.ownerStart || [])[lane], tone = o => (o === 0 ? ' own-me' : ' own-op');
  const bx = LANE_X[lane], by = BAND_Y + 3, bw = CELL * 3, bh = BAND_H - 6;
  if (start !== null && start !== undefined) {
    svgEl('rect', { x: bx - 5, y: by - 5, width: bw + 10, height: bh + 10, rx: 16, class: 'bandout' + tone(start) }, svg);
  }
  svgEl('rect', { x: bx, y: by, width: bw, height: bh, rx: 12, class: 'band' + (owner === null ? '' : tone(owner)) }, svg);
  dotState(B, lane).forEach((d, c) => {
    const cx = LANE_X[lane] + c * CELL + CELL / 2, cy = BAND_Y + BAND_H / 2;
    svgEl('circle', { cx, cy, r: 15, class: 'dot' + (d === null ? '' : d === 'x' ? ' x' : d === 0 ? ' d-me' : ' d-op') }, svg);
    if (d === 'x') svgEl('path', { d: crossPath(cx - 7, cy - 7, cx + 7, cy + 7), class: 'dotx' }, svg);
  });
}

/** A number badge on a unit: 'str' / 'def' / 'empty' squares or a 'sup' bread; tone 'up' (green) or 'down' (red). */
const SHIELD = 'M12 1L22.5 4.5V11.5C22.5 17.5 17.8 21.3 12 23C6.2 21.3 1.5 17.5 1.5 11.5V4.5Z';
function unitBadge(g, kind, x, y, size, n, textClass, tone, shield) {
  const icon = svgEl('svg', { x, y, width: size, height: size, viewBox: '0 0 24 24', class: 'ico bdg sq k-' + kind + (tone ? ' ' + tone : '') }, g);
  if (kind === 'sup') svgEl('path', { class: 'b', d: BREAD_PLAIN }, icon);
  else if (shield) svgEl('path', { class: 'b', d: SHIELD }, icon);
  else svgEl('rect', { class: 'b', x: 1, y: 1, width: 22, height: 22, rx: 5 }, icon);
  const text = svgEl('text', { x: 12, y: kind === 'sup' ? 12.9 : 12, dy: '.36em',
    class: 'numc' + (kind === 'sup' ? '' : ' w') + ' ' + textClass, 'font-size': digits(n) > 1 ? 12 : 16 }, icon);
  text.textContent = n;
}
/** Green if a stat is above its reference, red if below, plain otherwise. */
const tone = (n, ref) => (n > ref ? 'up' : n < ref ? 'down' : '');

/** Green rings burst from a stat badge that just went up. */
function gainPuff(g, badge) {
  const x = +badge.getAttribute('x'), y = +badge.getAttribute('y'), w = +badge.getAttribute('width');
  for (let i = 0; i < 2; i++) svgEl('circle', { cx: x + w / 2, cy: y + w / 2, r: w / 2 + 1, class: 'puff gainp', style: `animation-delay:${i * 140}ms` }, g);
}
function drawSpawnBurst(g, x0, y0, w, h) {
  const cx = x0 + w / 2, cy = y0 + h / 2, r = Math.max(w, h) / 2;
  for (let i = 0; i < 3; i++) svgEl('circle', { cx, cy, r, class: 'puff', style: `animation-delay:${i * 110}ms` }, g);
  for (let i = 0; i < 10; i++) {
    const angle = i / 10 * Math.PI * 2;
    svgEl('circle', { cx, cy, r: 4, class: 'spark', style: `--dx:${Math.cos(angle) * r * 1.7}px;--dy:${Math.sin(angle) * r * 1.7}px` }, g);
  }
}

/** The outline of a unit's cells on screen, `inset` px inside their edges, convex corners rounded like a normal unit. */
function shapeOutline(u, inset = 4) {
  const pts = cellsOf(u).map(([r, c]) => cellXY(u.lane, u.owner, r, c));
  const X = Math.min(...pts.map(p => p[0])), Y = Math.min(...pts.map(p => p[1]));
  const own = new Set(pts.map(([x, y]) => ((x - X) / CELL) + ',' + ((y - Y) / CELL)));
  const next = {};   // clockwise boundary edges on the grid of cell corners, start -> end
  const add = (a, b) => { next[a.join()] = b; };
  for (const k of own) {
    const [i, j] = k.split(',').map(Number);
    if (!own.has(i + ',' + (j - 1))) add([i, j], [i + 1, j]);
    if (!own.has((i + 1) + ',' + j)) add([i + 1, j], [i + 1, j + 1]);
    if (!own.has(i + ',' + (j + 1))) add([i + 1, j + 1], [i, j + 1]);
    if (!own.has((i - 1) + ',' + j)) add([i, j + 1], [i, j]);
  }
  const start = Object.keys(next)[0].split(',').map(Number), loop = [start];
  for (let p = next[start.join()]; p.join() !== start.join() && loop.length < 400; p = next[p.join()]) loop.push(p);
  // corners only, each moved 4px inward along both edges' inward normals
  const n = loop.length, corners = [];
  for (let k = 0; k < n; k++) {
    const a = loop[(k + n - 1) % n], b = loop[k], c = loop[(k + 1) % n];
    const d1 = [b[0] - a[0], b[1] - a[1]], d2 = [c[0] - b[0], c[1] - b[1]];
    if (d1[0] === d2[0] && d1[1] === d2[1]) continue;
    const convex = d1[0] * d2[1] - d1[1] * d2[0] > 0;
    corners.push({ x: X + b[0] * CELL + inset * (-d1[1] - d2[1]), y: Y + b[1] * CELL + inset * (d1[0] + d2[0]), d1, d2, r: convex ? inset + 5 : inset });
  }
  return corners.map(({ x, y, d1, d2, r }, k) => `${k ? 'L' : 'M'}${x - d1[0] * r},${y - d1[1] * r}Q${x},${y} ${x + d2[0] * r},${y + d2[1] * r}`).join('') + 'Z';
}

/** A marker around unit u: 'tgt' (orange: a legal target or affected), 'kill' (red: would die), 'pick' (white: selected or picked), plus ' hov' when hovered. */
function drawMark(svg, u, role) {
  const d = shapeOutline(u, 3);
  svgEl('path', { d, class: 'markhalo ' + role }, svg);
  svgEl('path', { d, class: 'mark ' + role }, svg);
}

/**
 * A unit: body, art, strength | supply | defence on top, melee/ranged mark at the bottom.
 * ref: the values its stats are compared with for colour (default: the printed card; in a preview: the current values).
 */
function drawUnit(svg, u, extraClasses = '', ref = null) {
  let [x0, y0, w, h] = unitRect(u);
  const c = cardOf(u);
  const cls = ['unit', 'f-' + c.fac, !canMoveAgain(u) && 'nomove', !canAttackAgain(u) && 'noatk', isIncorp(u) && 'ghost']
    .filter(Boolean).join(' ') + extraClasses;
  const g = svgEl('g', { class: cls, 'data-id': u.id }, svg);
  if (u.sh && cellsOf(u).length !== (w / CELL) * (h / CELL)) {
    // an amorphous (non-rectangular) unit: one outlined body; badges and art in its own cell
    svgEl('path', { d: shapeOutline(u, 2), class: 'ubody' }, g);
    const own = cellsOf(u).map(([r, c]) => cellXY(u.lane, u.owner, r, c)).sort((a, b) => a[1] - b[1] || a[0] - b[0])[0];   // its top-left cell on screen
    [x0, y0, w, h] = [...own, CELL, CELL];
  } else svgEl('rect', { x: x0 + 2, y: y0 + 2, width: w - 4, height: h - 4, rx: 6, class: 'ubody' }, g);
  // Immobile: a dashed inner border
  if (kw(u, 'fixed')) svgEl('rect', { x: x0 + 7, y: y0 + 7, width: w - 14, height: h - 14, rx: 3, class: 'immo' }, g);
  const m = Math.min(w, h);
  // a unit controlled from the other side's camp: an inner ring in its controller's colour
  if (u.ctl !== undefined && u.ctl !== u.owner) svgEl('rect', { x: x0 + 1, y: y0 + 1, width: w - 2, height: h - 2, rx: 11, class: 'ctlmark ' + (u.ctl === viewer() ? 'me' : 'op') }, g);

  const badge = Math.min(28, (Math.min(w, CELL * 2) - 8) / 3);
  const art = Math.max(18, m * 0.56);
  const artEl = svgEl('svg', { x: x0 + (w - art) / 2, y: y0 + (h - art) / 2 + (h <= CELL ? badge * 0.3 : 0), width: art, height: art, viewBox: '0 0 100 100', class: 'uart' }, g);
  svgEl('path', { d: ART[c.art] }, artEl);

  const str = strengthOf(u), def = defenceOf(u);
  const refS = ref ? ref.s : printedStr(u), refD = ref ? ref.d : printedDef(u);
  if (str || c.str) unitBadge(g, 'str', x0 + 4, y0 + 4, badge, str, 'strnum', tone(str, refS));
  unitBadge(g, 'sup', x0 + w / 2 - badge / 2, y0 + 4, badge, unitSupply(u), 'supnum', tone(unitSupply(u), c.sup));
  if (def || c.def) unitBadge(g, def > 0 ? 'def' : 'empty', x0 + w - 4 - badge, y0 + 4, badge, def, 'defnum', def > 0 ? tone(def, refD) : '', isArmoured(u) && !u.armUsed);
  // state marks along the bottom-left: Plague (green), Blighted (brown), soul contract (violet)
  [kw(u, 'plague') && 'plague', u.blight && 'blight'].filter(Boolean)
    .forEach((k, i) => svgEl('circle', { cx: x0 + 12 + i * 12, cy: y0 + h - 12, r: 5, class: 'stm ' + k }, g));

  if (kw(u, 'ranged') && (c.str > 0 || str > 0)) {
    const size = Math.max(16, Math.min(22, m * 0.3)), role = kw(u, 'ranged') ? 'ranged' : 'melee';
    const icon = svgEl('svg', { x: x0 + w / 2 - size / 2, y: y0 + h - size - 5, width: size, height: size, viewBox: '0 0 24 24', class: 'role' }, g);
    svgEl('circle', { cx: 12, cy: 12, r: 11, class: 'rbg' }, icon);
    svgEl('path', { d: ROLE_GLYPH[role], class: 'rgl' }, icon);
  }
  if (extraClasses.includes('spawn')) drawSpawnBurst(g, x0, y0, w, h);
  return g;
}


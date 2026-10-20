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
 * What is being placed now (a deploy, a move, a defector's or a resurrected unit's spot): {size, test(lane, r, c, o)}, or null.
 * test says whether that spot is legal; the same test serves the pointer preview and the cells marked as open.
 */
function placingNow() {
  const p = game.cur, P = pend();
  if (P && P.k === 'place') {
    const t = P.card ? { card: P.card } : byId(game, P.tid);
    if (!t) return null;
    return { size: shapeOf(t), owner: p, lanes: [P.lane], test: (lane, r, c, o) => lane === P.lane && fitsCells(game, p, lane, shapeCells(shapeOf(t), o), r, c) };
  }
  if (ui.mode === 'deploy') {
    const k = handCard(ui.hi);
    if (!k || CARDS[k].tactic) return null;
    return { size: CARDS[k].size, owner: p, lanes: LANES, card: k, test: (lane, r, c, o) => canDeploy(game, p, ui.hi, lane, r, c, o) };
  }
  if (ui.mode === 'unit') {
    const u = selectedUnit();
    if (!u) return null;
    const lanes = cardOf(u).outrider && !ui.free ? LANES : [u.lane];
    return { size: shapeOf(u), owner: u.owner, lanes, unit: u, test: (lane, r, c, o) => !!moveTargets(game, u, o, ui.free, lane)[r + ',' + c] };
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
      if (t && !(W.unit && t.id === W.unit.id) && !(W.card && (CARDS[W.card].onto || CARDS[W.card].sacrifice))) continue;   // only free cells (or the units it may go onto)
      out.set([W.owner, lane, x, y].join(), [W.owner, lane, x, y]);
    }
  return [...out.values()];
}

/** The throw action for camp cell c in throw mode, if legal. */
function throwAt(c) {
  const u = selectedUnit(), t = byId(game, ui.tid);
  if (!c || !u || !t || !throwables(game, u).some(x => x.id === t.id)) return null;
  return throwTargets(game, u, t).some(x => x.lane === c.lane && x.owner === c.owner && x.r === c.r && x.c === c.c)
    ? { t: 'throw', id: u.id, aid: t.id, lane: c.lane, owner: c.owner, r: c.r, c: c.c } : null;
}
/** The action the pointer is on right now, if it is legal: {a: action, mover?: id, zone?: {k, lane, r, cc, o}}. */
function hoverAction() {
  if (!myTurn()) return null;
  const p = game.cur, a0 = ui.anchor, P = pend();
  const unitUnder = a0 ? unitAt(game, a0.owner, a0.lane, a0.r, a0.c) : null;
  if (P) {
    if (P.k === 'place' && P.card) {
      const place = placementInfo();
      if (!place || !place.ok) return null;
      return { a: { t: 'place', r: place.a.r, c: place.a.c, o: place.o }, zone: { k: P.card, lane: P.lane, r: place.a.r, cc: place.a.c, o: place.o } };
    }
    if (P.k === 'place') {
      const place = placementInfo(), t = byId(game, P.tid);
      if (!place || !place.ok || !t) return null;
      return { a: { t: 'place', r: place.a.r, c: place.a.c, o: place.o }, mover: t.id,
        zone: { k: t.card, lane: P.lane, r: place.a.r, cc: place.a.c, o: place.o } };
    }
    if (P.k === 'free') {
      const u = selectedUnit(), place = ui.mode === 'unit' && ui.free ? placementInfo() : null;
      if (!u || !place || !place.ok) return null;
      return { a: { t: 'fmove', id: u.id, r: place.a.r, c: place.a.c, o: place.o }, mover: u.id, zone: { k: u.card, lane: u.lane, r: place.a.r, cc: place.a.c, o: place.o } };
    }
    return unitUnder && pendingPicks().has(unitUnder.id) ? { a: { t: 'pick', tid: unitUnder.id } } : null;
  }
  if (ui.mode === 'deploy') {
    const place = placementInfo();
    if (!place || !place.ok) return null;
    const { lane, r, c: col } = place.a;
    return { a: { t: 'deploy', hi: ui.hi, lane, r, c: col, o: place.o },
      zone: { k: handCard(ui.hi), lane, r, cc: col, o: place.o } };
  }
  if (ui.mode === 'throw') {
    const a = throwAt(a0);
    return a ? { a, mover: a.aid } : null;
  }
  if (ui.mode === 'unit' && a0) {
    const u = selectedUnit();
    if (!u) return null;
    if (a0.owner !== u.owner || (unitUnder && unitUnder.id !== u.id && canAttack(game, u, unitUnder)))
      return unitUnder && canAttack(game, u, unitUnder) ? { a: { t: 'attack', id: u.id, tid: unitUnder.id } } : null;
    const place = placementInfo();
    if (!place || !place.ok) return null;
    const { lane, r, c: col } = place.a;
    const mv = lane === u.lane ? { t: 'move', id: u.id, r, c: col, o: place.o } : { t: 'move', id: u.id, lane, r, c: col, o: place.o };
    return { a: mv, mover: u.id, zone: { k: u.card, lane, r, cc: col, o: place.o } };
  }
  const spell = want => { const opt = spellMatch(ui.hi, want); return opt ? { a: { t: 'tactic', hi: ui.hi, ...opt } } : null; };
  if (ui.mode === 'lane' && hoverLane !== null) return spell({ lane: hoverLane });
  if (ui.mode === 'column' && a0 && a0.owner !== p) return spell({ lane: a0.lane, col: a0.c });
  if (ui.mode === 'own' && unitUnder && ctl(unitUnder) === p) return spell({ vid: unitUnder.id });
  if (ui.mode === 'enemy' && unitUnder && ctl(unitUnder) !== p) return spell({ tid: unitUnder.id });
  if (ui.mode === 'any' && unitUnder) return spell({ tid: unitUnder.id });
  return null;
}


/**
 * Compare the live game with a future state t (the hovered action played on a copy, or the round-end forecast):
 * fx[id] = 'kill' | 'aff', disp[id] = unit with its new stats, loss[p][lane] = supply lost, state = t.
 */
function diffStates(t, skipId) {
  applyAuras(game);
  const out = { fx: {}, disp: {}, state: t };
  out.loss = [0, 1].map(p => LANES.map(l => Math.max(0, laneSupply(game, p, l) - laneSupply(t, p, l))));
  const marks = u => JSON.stringify([kw(u, 'plague'), !!u.blight, isIncorp(u), cellsOf(u)]);
  for (const u of game.units) {
    if (u.id === skipId) continue;
    const v = byId(t, u.id);
    if (!v) { out.fx[u.id] = 'kill'; continue; }
    if (v.lane !== u.lane || v.owner !== u.owner) continue;
    const grew = v.sh && cellsOf(v).length !== cellsOf(u).length;   // a spreading or eating unit
    if (strengthOf(v) !== strengthOf(u) || defenceOf(v) !== defenceOf(u) || (marks(v) !== marks(u) && (grew || v.r === u.r && v.c === u.c))) {
      out.disp[u.id] = v;
      out.fx[u.id] = 'aff';
    }
  }
  // units that appear (Shades, Abominations, Gorvan...), except the one being placed or moved
  out.added = t.units.filter(v => !byId(game, v.id) && v.id !== skipId);
  return out;
}

/** Parts of a pending choice that happen whatever is picked, for previews (Cinder Imp: its damage to the enemy). */
const PENDING_PREVIEW = {
  cinder(t, P) { const imp = byId(t, P.src); if (imp) { damageFacing(t, imp, P.amt, 'Cinder Imp'); processDeaths(t); } },
};
function simulate(h) {
  const t = cloneState(game);
  t.noFx = true;
  try { applyAction(t, h.a); } catch (e) { return null; }
  // an action that waits for a choice: the part that doesn't depend on the choice still shows
  if (t.pending && PENDING_PREVIEW[t.pending.k]) { try { PENDING_PREVIEW[t.pending.k](t, t.pending); } catch (e) { /* preview only */ } }
  // the unit being placed or moved: a new unit takes the next id
  const placedId = h.mover ?? (h.a.t === 'deploy' || h.a.t === 'place' ? game.nid : undefined);
  const out = diffStates(t, placedId);
  out.reach = null;
  out.placed = placedId !== undefined ? byId(t, placedId) : null;
  out.placedRef = h.mover !== undefined ? byId(game, h.mover) : null;
  // the placed or moved unit dies on the way: it is still drawn where it dies, with an X
  if (placedId !== undefined && !out.placed) out.placedDead = (t.deadUnits || []).filter(v => v.id === placedId).pop() || null;
  if (h.mover !== undefined && !out.placed) out.fx[h.mover] = 'kill';   // the moved or thrown unit dies (a throw onto a unit, Akritai)
  const z = h.zone;
  if (z) {
    const placed = out.placed;
    const u = placed || { card: z.k, owner: game.cur, lane: z.lane, r: z.r, c: z.cc, o: z.o ?? ui.o, id: -1 };
    out.reach = unitReach(t, u, h.a.t === 'deploy' || h.a.t === 'place');
    // a placement that asks for a follow-up pick: the units that could be picked take part too
    if (t.pending) for (const a of listActions(t)) if (a.t === 'pick') out.reach.unit(byId(t, a.tid));
  }
  return out;
}

/** What to highlight now: the hovered action's reach, else the pending choice's, else the hovered or selected unit's. */
function currentReach(hover, preview) {
  if (hover && preview && preview.reach) return preview.reach;
  if (hover && hover.a.t === 'tactic') return spellReach(game, game.cur, handCard(hover.a.hi), hover.a);
  const P = pend();
  if (P) return pendingReach(game, P);
  if (ui.mode && ui.mode !== 'unit') return null;
  const u = (hoverUnitId && byId(game, hoverUnitId)) || selectedUnit();
  return u ? unitReach(game, u) : null;
}

function canDeployInLane(hi, lane) {
  const c = CARDS[handCard(hi)];
  if (!canPay(game, lane, c.cost) || !needsMet(game, game.cur, handCard(hi))) return false;
  for (let r = 0; r < ROWS; r++) for (let col = 0; col < COLS; col++)
    for (const o of orientations(c.size)) if (deployFits(game, game.cur, lane, handCard(hi), r, col, o)) return true;
  return false;
}


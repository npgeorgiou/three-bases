/* =====================================================================
   INPUT
   ===================================================================== */
const ROTATABLE_MODES = ['deploy', 'unit'];
const laneCell = lane => (lane === null ? null : { lane, owner: game.cur, r: 0, c: 0, fr: 0, fc: 0 });

function attackRefusal(u) {
  if (u.attacked) return 'This unit already attacked this round.';
  if (strengthOf(u) <= 0) return 'Units with no strength can\'t attack.';
  if (!canPay(game, u.lane, attackCost(u))) return `Attacking costs ${attackCost(u)} supply.`;
  return 'Out of reach: a melee unit strikes only the cells around it; from your front row that reaches the three enemy front-row cells facing it (a Pike also from your second row).';
}
function moveRefusal(u) {
  if (cardOf(u).fixed) return 'This unit can\'t move.';
  if ((u.mv || 0) >= maxMoves(u)) return 'This unit already moved this round.';
  if (!canPay(game, u.lane, moveCost(u))) return `Moving costs ${moveCost(u)} supply.`;
  return 'It doesn\'t fit there. Try another spot or rotate (R or mouse wheel).';
}
function deployRefusal(a, card) {
  if (card.onto && !deployFits(game, game.cur, a.lane, handCard(ui.hi), a.r, a.c, ui.o)) return `${card.name} must be placed onto one of your Shades.`;
  if (card.sacrifice && !deployFits(game, game.cur, a.lane, handCard(ui.hi), a.r, a.c, ui.o)) return `${card.name} must cover at least one of your units, and only yours.`;
  if (!card.onto && !card.sacrifice && !fits(game, game.cur, a.lane, card.size, a.r, a.c, ui.o)) return 'It doesn\'t fit there. Try another spot or rotate (R or mouse wheel).';
  return `Not enough supply in lane ${a.lane + 1}: ${card.name} costs ${card.cost}.`;
}
/** Why spell hi can't target that. */
function spellRefusal(k) {
  return {
    monomachia: 'Pick one of your units with an enemy in its lane.',
    synaspismos: 'Pick one of your units with an ally directly beside it.',
    bribe: 'Pick an enemy unit whose supply you can pay and that fits in your camp.',
    cull: 'Pick an enemy unit with 2 or less defence left.',
    greekfire: 'Pick a column of an enemy camp with an enemy in it.',
  }[k] || `${CARDS[k].name} can't target that, or you lack the supply.`;
}

/** Clicks while a follow-up choice is pending. */
function resolvePending(c, confirm, under) {
  const P = pend(), p = game.cur;
  if (P.k === 'place') {
    ui.anchor = c;
    if (c.owner !== p || c.lane !== P.lane) { if (confirm) ui.err = `Pick a free spot in your camp in lane ${P.lane + 1}.`; return false; }
    if (!confirm) return false;
    const place = placementInfo();
    if (place && place.ok) { act({ t: 'place', r: place.a.r, c: place.a.c, o: place.o }); return true; }
    ui.err = 'It doesn\'t fit there. Try another spot or rotate (R or mouse wheel).';
    return false;
  }
  if (P.k === 'free') {
    const movable = under && ctl(under) === p && under.lane === P.lane && under.id !== P.ex && !cardOf(under).fixed;
    const u = ui.mode === 'unit' && ui.free ? selectedUnit() : null;
    if (u && c.owner === u.owner && c.lane === P.lane && !(movable && under.id !== u.id)) {
      ui.anchor = c;
      if (!confirm) return false;
      const place = placementInfo();
      if (place && place.ok) { act({ t: 'fmove', id: u.id, r: place.a.r, c: place.a.c, o: place.o }); return true; }
      ui.err = 'It doesn\'t fit there. Try another spot or rotate (R or mouse wheel).';
      return false;
    }
    if (movable) { selectUnit(under); return true; }
    ui.err = P.ex ? 'Pick another of your units in this lane.' : `Pick one of your units in lane ${P.lane + 1}.`;
    return false;
  }
  if (under && pendingPicks().has(under.id)) { act({ t: 'pick', tid: under.id }); return true; }
  if (confirm) ui.err = pendingPrompt(game);
  return false;
}

/**
 * Act on camp cell c in the current mode. Returns true if an action ran (or a pick was made),
 * false if refused (ui.err explains why), null if the click means nothing here.
 */
function resolveCell(c, confirm) {
  if (!c) return false;
  const p = game.cur, under = unitAt(game, c.owner, c.lane, c.r, c.c);
  ui.err = '';
  if (pend()) return resolvePending(c, confirm, under);
  const castOn = (want, lane) => {
    const opt = spellMatch(ui.hi, want);
    if (opt) { act({ t: 'tactic', hi: ui.hi, ...opt }); return true; }
    ui.err = spellRefusal(handCard(ui.hi));
    return false;
  };
  switch (ui.mode) {
    case 'deploy': {
      const card = CARDS[handCard(ui.hi)];
      ui.anchor = c;
      if (c.owner !== p) { if (confirm) ui.err = 'Units go into your own camp.'; return false; }
      if (!confirm) return false;
      const place = placementInfo(), a = place ? place.a : placeAt(c, card.size, ui.o);
      if (place && place.ok) { act({ t: 'deploy', hi: ui.hi, lane: a.lane, r: a.r, c: a.c, o: place.o }); return true; }
      ui.err = deployRefusal(a, card);
      return false;
    }
    case 'unit': {
      const u = selectedUnit(), card = cardOf(u);
      if (under && throwables(game, u).some(x => x.id === under.id)) { ui.mode = 'throw'; ui.tid = under.id; return true; }
      if (under && ctl(under) !== p) {
        if (canAttack(game, u, under)) { act({ t: 'attack', id: u.id, tid: under.id }); return true; }
        if (under.lane === u.lane) { ui.err = attackRefusal(u); return false; }
      }
      if (under && ctl(under) === p && under.id !== u.id && canAttack(game, u, under)) { act({ t: 'attack', id: u.id, tid: under.id }); return true; }
      if (c.owner !== u.owner || (c.lane !== u.lane && !card.outrider) || (under && under.id === u.id && ui.o === u.o)) return null;
      ui.anchor = c;
      if (!confirm) return false;
      const place = placementInfo();
      if (place && place.ok) {
        const a = place.a;
        act(c.lane === u.lane ? { t: 'move', id: u.id, r: a.r, c: a.c, o: place.o } : { t: 'move', id: u.id, lane: c.lane, r: a.r, c: a.c, o: place.o });
        return true;
      }
      if (under) return null;
      ui.err = moveRefusal(u);
      return false;
    }
    case 'throw': {
      const u = selectedUnit(), t = byId(game, ui.tid), a = throwAt(c);
      if (a) { act(a); return true; }
      if (u && t) ui.err = `Pick a free cell or a unit in lane ${u.lane + 1}, in either camp.`;
      return false;
    }
    case 'lane': return castOn({ lane: c.lane }, c.lane);
    case 'column':
      if (c.owner === p) { ui.err = 'Pick a column of an enemy camp.'; return false; }
      return castOn({ lane: c.lane, col: c.c }, c.lane);
    case 'own':
      if (!under || ctl(under) !== p) { ui.err = 'Pick one of your units.'; return false; }
      return castOn({ vid: under.id }, under.lane);
    case 'enemy':
      if (!under || ctl(under) === p) { ui.err = 'Pick an enemy unit.'; return false; }
      return castOn({ tid: under.id }, under.lane);
    case 'any':
      if (!under) { ui.err = 'Pick a unit.'; return false; }
      return castOn({ tid: under.id }, under.lane);
  }
  return null;
}

/** Size of what is being placed or moved. */
function activeSize() {
  const P = pend();
  if (P && P.k === 'place') { const t = P.card ? { card: P.card } : byId(game, P.tid); return t ? shapeOf(t) : 1; }
  if (ui.mode === 'deploy') return CARDS[handCard(ui.hi)].size;
  const u = selectedUnit();
  return u ? shapeOf(u) : 1;
}

/** Can unit u move anywhere now (any orientation; Outrider: any lane)? */
const hasMoves = (u, free = false) => (cardOf(u).outrider && !free ? LANES : [u.lane])
  .some(l => orientationsOf(u).some(o => Object.keys(moveTargets(game, u, o, free, l)).length));
/** Can unit u do anything now: move, attack or throw? */
const canActNow = u => hasMoves(u) || game.units.some(t => canAttack(game, u, t)) || throwables(game, u).length > 0;
function selectUnit(u) { resetUi(); ui.mode = 'unit'; ui.id = u.id; ui.o = u.o; ui.free = !!(pend() && pend().k === 'free'); }

function boardClick(c, pointerType) {
  if (!myTurn() || !c) return;
  const under = unitAt(game, c.owner, c.lane, c.r, c.c);
  // touch: the first tap previews, a second tap on the same spot confirms
  const confirm = pointerType === 'mouse'
    || (!!ui.anchor && placementKey(placeAt(ui.anchor, activeSize(), ui.o)) === placementKey(placeAt(c, activeSize(), ui.o)));
  if (resolveCell(c, confirm) === null) {
    if (under && ctl(under) === game.cur && !(ui.mode === 'unit' && ui.id === under.id) && !pend()) {
      if (canActNow(under)) selectUnit(under);
      else { resetUi(); ui.err = `${unitName(under)} can't move or attack now.`; }
    } else resetUi();
  }
  if (!busy) render();
}

function selectCard(i) {
  if (!myTurn() || game.pending) return;
  if (ui.hi === i && ui.mode) { resetUi(); render(); return; }
  const c = CARDS[handCard(i)];
  resetUi();
  ui.hi = i;
  ui.mode = !c.tactic ? 'deploy' : c.tactic;
  render();
}

const canRotate = () => ROTATABLE_MODES.includes(ui.mode) || (pend() && pend().k === 'place');
function rotate() {
  const list = orientations(activeSize());
  if (list.length < 2) return;
  ui.o = list[(list.indexOf(ui.o) + 1) % list.length];
  render();
}

function cancel() {
  const choosing = game && myTurn() && pend() && !ui.mode;
  resetUi();
  drag = null;
  $('#ghost').hidden = true; dragSrc = null;
  document.body.classList.remove('dragging');
  if (choosing) { exitPending(); return; }
  if (game && !busy) render();
}

function onPointerDown(e) {
  if (e.button === 2) return;
  lastPointer = e.pointerType;
  hideTip();
  const start = { x: e.clientX, y: e.clientY, on: false };
  const cardBtn = e.target.closest('.cardbtn');
  if (cardBtn) { drag = { ...start, type: 'card', hi: +cardBtn.dataset.i }; return; }
  if (!e.target.closest('#board')) return;
  const c = cellFromPoint(e.clientX, e.clientY);
  const P = pend();
  const canPickUnit = c && myTurn() && !['deploy', ...SPELL_MODES].includes(ui.mode) && (!P || P.k === 'free');
  const u = canPickUnit ? unitAt(game, c.owner, c.lane, c.r, c.c) : null;
  const draggable = u && ctl(u) === game.cur && (P ? u.lane === P.lane && u.id !== P.ex && !cardOf(u).fixed : canActNow(u));
  drag = draggable ? { ...start, type: 'unit', id: u.id } : { ...start, type: 'board' };
}

/** The hand card being dragged (hidden in the hand while it is held), or null. */
let dragSrc = null;
/** A dragged card that wasn't played glides back into its place in the hand. */
function returnCard(hi) {
  const ghost = $('#ghost'), btn = $(`#hand .cardbtn[data-i="${hi}"]`);
  const finish = () => { ghost.hidden = true; ghost.className = ''; if (dragSrc === hi) { dragSrc = null; const b = $(`#hand .cardbtn[data-i="${hi}"]`); if (b) b.classList.remove('dragsrc'); } };
  if (ghost.hidden || !btn) { finish(); return; }
  ghost.className = '';
  const pad = parseFloat(getComputedStyle(ghost).paddingTop) || 0, to = btn.querySelector('.card').getBoundingClientRect();
  const dx = to.left - pad - parseFloat(ghost.style.left), dy = to.top - pad - parseFloat(ghost.style.top);
  const anim = ghost.animate([{ transform: 'translate(0,0)' }, { transform: `translate(${dx}px,${dy}px)` }], { duration: 180, easing: 'ease-out', fill: 'forwards' });
  const done = () => { anim.cancel(); finish(); };
  anim.finished.then(done, done);
}

function startDrag() {
  drag.on = true;
  document.body.classList.add('dragging');
  if (drag.type === 'card') {
    // the card itself is dragged from where it is: one card, held where it was grabbed
    const btn = $(`#hand .cardbtn[data-i="${drag.hi}"]`), rect = btn ? btn.querySelector('.card').getBoundingClientRect() : null;
    const keep = ui.hi === drag.hi ? ui.o : 'h';
    const ghost = $('#ghost');
    textSide = viewer(); ghost.innerHTML = cardHtml(handCard(drag.hi)); textSide = null;
    ghost.className = ''; ghost.hidden = false;
    const pad = parseFloat(getComputedStyle(ghost).paddingTop) || 0;
    drag.gx = rect ? drag.x - rect.left + pad : pad + 40; drag.gy = rect ? drag.y - rect.top + pad : pad + 40;
    ghost.style.transformOrigin = `${drag.gx}px ${drag.gy}px`;
    dragSrc = drag.hi;
    resetUi();
    selectCard(drag.hi);
    ui.o = keep;
  } else {
    const u = byId(game, drag.id), keep = ui.id === drag.id ? ui.o : u.o;
    selectUnit(u);
    ui.o = keep;
    renderSide();
  }
}

function onPointerMove(e) {
  lastPointer = e.pointerType;
  if (drag && !drag.on && (drag.type === 'card' || drag.type === 'unit') && myTurn()
    && Math.hypot(e.clientX - drag.x, e.clientY - drag.y) > 7) startDrag();
  if (drag && drag.on) {
    const ghost = $('#ghost');
    if (!ghost.hidden) {
      ghost.style.left = e.clientX - drag.gx + 'px'; ghost.style.top = e.clientY - drag.gy + 'px';
      // over a camp a unit card becomes the unit preview; over the rest of the board (or for a spell) it shrinks beside the pointer
      const onCamp = !!cellFromPoint(e.clientX, e.clientY), onBoard = !!(e.target.closest && e.target.closest('#board')) || onCamp;
      const unitCard = drag.type === 'card' && !CARDS[handCard(drag.hi)].tactic;
      ghost.classList.toggle('gone', unitCard && onCamp);
      ghost.classList.toggle('small', onBoard && !(unitCard && onCamp));
    }
    if (ui.mode === 'lane') hoverLane = laneFromPoint(e.clientX, e.clientY);
    ui.anchor = cellFromPoint(e.clientX, e.clientY);
    renderBoard();
    return;
  }
  if (busy) { hideTip(); return; }

  const onBoard = e.target.closest && e.target.closest('#board');
  if (onBoard && e.pointerType === 'mouse') {
    const c = cellFromPoint(e.clientX, e.clientY), u = c ? unitAt(game, c.owner, c.lane, c.r, c.c) : null;
    if (u && !ui.mode) showUnitTip(u, e.clientX, e.clientY); else hideTip();
    const hid = u && (!ui.mode || ui.mode === 'unit') ? u.id : null;
    if (hid !== hoverUnitId) { hoverUnitId = hid; if (!busy) renderBoard(); }
    const lane = laneFromPoint(e.clientX, e.clientY);
    if (lane !== hoverLane) { hoverLane = lane; markCardsForLane(); if (ui.mode === 'lane') renderBoard(); }
    if (myTurn() && (ui.mode || pend())) {
      const before = ui.anchor ? placementKey(placeAt(ui.anchor, activeSize(), ui.o)) : '';
      ui.anchor = c;
      if (before !== (c ? placementKey(placeAt(c, activeSize(), ui.o)) : '')) renderBoard();
    }
  } else {
    hideTip();
    if (hoverLane !== null && !onBoard) { hoverLane = null; markCardsForLane(); if (ui.mode === 'lane') renderBoard(); }
  }
  const cardBtn = e.target.closest && e.target.closest('.cardbtn'), hovered = cardBtn ? +cardBtn.dataset.i : null;
  if (hovered !== hoverCard) { hoverCard = hovered; if (!ui.mode && myTurn()) renderBoard(); }
}

function onPointerUp(e) {
  if (!drag) return;
  const d = drag;
  drag = null;
  document.body.classList.remove('dragging');
  const lane = () => laneFromPoint(e.clientX, e.clientY);
  if (d.on) {
    // a drop counts only over the board (dropping a card back on the hand puts it back)
    const overBoard = !!(e.target.closest && e.target.closest('#board')) || !!cellFromPoint(e.clientX, e.clientY);
    const c = !overBoard ? null : ui.mode === 'lane' ? laneCell(lane()) : cellFromPoint(e.clientX, e.clientY);
    let played = false;
    const held = dragSrc;
    dragSrc = null;   // if the card is played, the hand redraws without a hidden slot
    if (c && myTurn()) { const r = resolveCell(c, true); played = r === true; if (r === null) ui.anchor = null; } else ui.anchor = null;
    if (d.type === 'card' && !played) { dragSrc = held; if (!c) resetUi(); returnCard(d.hi); } else $('#ghost').hidden = true;   // dropped off the board: put back, unselected
    if (!busy) render();
    return;
  }
  $('#ghost').hidden = true;
  if (d.type === 'card') { selectCard(d.hi); return; }
  if (ui.mode === 'lane' && myTurn()) {
    const c = laneCell(lane());
    if (c) { resolveCell(c, true); if (!busy) render(); }
    return;
  }
  boardClick(cellFromPoint(e.clientX, e.clientY), e.pointerType);
}


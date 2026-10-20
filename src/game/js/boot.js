/* =====================================================================
   BOOT
   ===================================================================== */
document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('pointerdown', onPointerDown);
  document.addEventListener('pointermove', onPointerMove);
  document.addEventListener('pointerup', onPointerUp);
  document.addEventListener('pointercancel', () => { const d = drag; drag = null; document.body.classList.remove('dragging'); if (d && d.on && d.type === 'card') returnCard(d.hi); else $('#ghost').hidden = true; });
  document.addEventListener('pointerdown', () => Sound.unlock(), { once: true });
  document.addEventListener('mouseover', showKeywordTip);
  document.addEventListener('mouseover', showLogCard);
  document.addEventListener('mouseover', showPileTip);
  new MutationObserver(list => {
    for (const m of list) {
      if (m.type === 'attributes') { if (!m.target.hidden) queueFit(m.target); continue; }
      for (const n of m.addedNodes) if (n.nodeType === 1 && (n.matches('.card') || n.querySelector('.card'))) queueFit(n.parentNode || n);
    }
  }).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['hidden'] });
  addEventListener('resize', () => queueFit(document.body));
  // side panels open on hover: fit the texts of the cards they show once they are visible
  document.addEventListener('mouseover', e => { const b = e.target.closest && e.target.closest('.cardbtn, .bcard'), side = b && b.querySelector('.kwside .kwref'); if (side) queueFit(b.querySelector('.kwside')); });
  document.addEventListener('keydown', onKey);
  addEventListener('resize', () => { if (game) layoutHands(); if (!$('#infoPanel').hidden) placeInfoPanel(); });

  $('#eye').addEventListener('pointerenter', showForecast);
  $('#eye').addEventListener('pointerleave', hideForecast);
  $('#eye').addEventListener('click', () => (forecasting ? hideForecast() : showForecast()));
  $('#app').addEventListener('contextmenu', e => { e.preventDefault(); cancel(); });
  $('#board').addEventListener('wheel', e => { if (myTurn() && canRotate()) { e.preventDefault(); rotate(); } }, { passive: false });
  $('#board').addEventListener('pointerleave', () => {
    hideTip();
    if (hoverUnitId !== null) { hoverUnitId = null; if (game && !busy) renderBoard(); }
    if (!drag && ui.anchor && lastPointer === 'mouse') { ui.anchor = null; renderBoard(); }
  });
  $('#panel').addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    const handlers = { cancel, rotate };
    handlers[b.dataset.a]?.();
  });

  setupAiPick();
  setupDeckPages();
  for (const b of $$('[data-mode]')) b.addEventListener('click', () => pressToggle('mode', b.dataset.mode));
  $('#passBtn').addEventListener('click', passOrDone);
  $('#prompt').addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b || !myTurn()) return;
    if (b.dataset.p === 'done') act({ t: 'done' });
    if (b.dataset.p === 'g') act({ t: 'gpick', key: b.dataset.k });
    if (b.dataset.p === 'k') act({ t: 'kpick', f: b.dataset.f });
  });
  $('#gravePick').addEventListener('click', e => {
    const b = e.target.closest('button.gpc');
    if (b && !b.disabled && myTurn()) { ui.gk = null; act({ t: 'gpick', key: b.dataset.k }); }
  });
  $('#gravePick').addEventListener('mouseover', e => {
    const b = e.target.closest('button.gpc'), k = b && !b.disabled ? b.dataset.k : null;
    if (k !== ui.gk) { ui.gk = k; renderBoard(); }
  });
  $('#gravePick').addEventListener('mouseleave', () => { if (ui.gk) { ui.gk = null; renderBoard(); } });
  $('#infoBtn').addEventListener('click', toggleInfoPanel);
  $('#startBtn').addEventListener('click', () => { enterFullscreen(); startGame(); });
  $('#fsBtn').addEventListener('click', () => (document.fullscreenElement ? document.exitFullscreen() : enterFullscreen()));
  document.addEventListener('fullscreenchange', onFullscreenChange);
  // Withdraw: the first click arms the button, a second click within 3 seconds leaves the battle
  let quitTimer = null;
  $('#quitBtn').addEventListener('click', () => {
    const q = $('#quitBtn');
    if (!q.classList.contains('armed')) { q.classList.add('armed'); clearTimeout(quitTimer); quitTimer = setTimeout(() => q.classList.remove('armed'), 3000); return; }
    clearTimeout(quitTimer); q.classList.remove('armed');
    if (!game || replay || game.winner !== null) { $('#newBtn').click(); return; }
    // withdrawing is a loss: the other side wins
    const w = viewer();
    game.winner = other(w);
    game.endReason = `${deckName(game, w)} withdrew.`;
    showEnd();
  });
  $('#newBtn').addEventListener('click', () => { if (replay) { replay = null; $('#replayBar').hidden = true; } showPage('#setup'); renderHome(); });
  $('#replayBtn').addEventListener('click', startReplay);
  $('#rbPlay').addEventListener('click', replayPlay);
  $('#rbNext').addEventListener('click', replayStep);
  $('#rbRestart').addEventListener('click', () => { if (replay) { replay.playing = false; const go = () => (busy ? setTimeout(go, 100) : startReplay()); go(); } });
  $('#rbExit').addEventListener('click', () => { if (replay) { replay.playing = false; const go = () => (busy ? setTimeout(go, 100) : exitReplay()); go(); } });
  $('#rbSlider').addEventListener('pointerdown', () => { if (replay && replay.playing) { replay.playing = false; renderReplayBar(); } });
  $('#rbSlider').addEventListener('input', e => { if (replay) $('#rbStep').textContent = `Move ${e.target.value} / ${lastReplay.actions.length}`; });
  $('#rbSlider').addEventListener('change', e => replayJump(+e.target.value));
  $('#againBtn').addEventListener('click', () => { $('#endDlg').hidden = true; showPage('#setup'); renderHome(); });
});

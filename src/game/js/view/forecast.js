/* ---------- end-of-round forecast (the eye) ---------- */
let forecasting = false;
function showForecast() {
  if (!game || (busy && !aiThinking) || game.winner !== null) return;
  forecasting = true;
  const t = forecastRoundEnd(game), v = viewer(), o = other(v);
  const next = { ...t, starter: other(t.starter) };      // who acts first next round
  hideTip();
  renderBoard(game, { forecast: t });
  renderStacks(next);
  const line = p => `<b>${deckName(t, p)}</b> ${t.players[p].hand.length} in hand · ${basesHeld(t, p)} bases`
    + (next.starter === p ? '<span class="tagp">starts next round</span>' : '');
  $('#oppLine').innerHTML = line(o);
  $('#meLine').innerHTML = line(v);
  const result = t.winner === null ? null : t.winner === 'draw' ? 'Draw' : t.winner === 'lost' ? 'Both sides lose' : `${deckName(t, t.winner)} wins`;
  $('#status').textContent = `Preview · end of round ${t.round}: ` + (result || 'no winner yet');
  const fw = $('#fcWin');
  if (result) {                                                 // the game would end: say so over the board
    fw.innerHTML = `${result}<small>${t.endReason || ''}</small>`;
    const r = $('#board').getBoundingClientRect();
    fw.style.left = (r.left + r.width / 2) + 'px'; fw.style.top = (r.top + r.height / 2) + 'px';
    fw.hidden = false;
  }
  $('#eye').classList.add('on');
}
function hideForecast() {
  if (!forecasting) return;
  forecasting = false;
  $('#eye').classList.remove('on');
  $('#fcWin').hidden = true;
  if (game && (!busy || aiThinking)) render();
}


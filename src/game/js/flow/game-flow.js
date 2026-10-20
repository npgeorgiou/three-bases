/* =====================================================================
   GAME FLOW
   ===================================================================== */
async function act(action) {
  if (busy) return;
  const current = game;
  resetUi();
  hideTip();
  await perform(action);
  if (game === current) afterAction(action);   // a new game may have started meanwhile
}

/** Apply an action and play its animations. */
async function perform(action) {
  const current = game, round = game.round, side = game.cur;
  const played = action.t === 'tactic' && game.cur === viewer() ? $('#hand').children[action.hi] : null;
  spellOrigin = played ? (played.querySelector('.card') || played).getBoundingClientRect() : null;
  aiThinking = false;
  if (forecasting) { forecasting = false; $('#eye').classList.remove('on'); $('#fcWin').hidden = true; }
  busy = true;
  if (action.t === 'pick' && game.pending && game.pending.src && isHuman(game.cur)) await flashPick(action.tid);
  if (game !== current) return;
  const before = isHuman(game.cur) && !game.pending ? structuredClone(game) : null;
  applyAction(game, action);
  if (!replay && game.history) game.history.push(action);
  if (!game.pending || !isHuman(game.cur)) undoState = null;
  else if (before) undoState = before;
  const events = game.fx;
  game.fx = [];
  renderSide();
  renderHand();
  hideIncomingCards(events);
  if (events.length) await playEvents(events);
  if (game !== current) return;
  if (game.round === round && game.cur !== side && game.winner === null) Sound.tick();
  busy = false;
  render();
  if ($('#eye').matches(':hover')) showForecast();
}

/** Cards about to be drawn stay hidden until their draw animation lands them. */
function hideIncomingCards(events) {
  for (const [p, sel] of [[viewer(), '#hand'], [other(viewer()), '#oppHand']]) {
    const n = events.filter(e => e.draw === p || e.handIn === p).reduce((sum, e) => sum + (e.n || 1), 0);
    if (n) [...$(sel).children].slice(-n).forEach(card => { card.style.visibility = 'hidden'; });
  }
}

function afterAction(action) {
  if (game.winner !== null) { showEnd(); return; }
  if (settings.mode === 'ai' && game.cur === 1) {
    $('#status').textContent = `${deckName(game, 1)} is acting…`;
    busy = true; aiThinking = true;
    renderSide();
    if ($('#eye').matches(':hover')) showForecast();
    const current = game;
    setTimeout(async () => {       // let the last animation settle on screen, then think
      if (game !== current) return;
      const started = performance.now();
      const idle = game.test && testIdle && !game.pending;   // a test game whose opponent doesn't act
      const move = idle ? { t: 'pass' } : chooseComputerMove(game);
      await sleep(idle ? 300 : Math.max(0, 1000 - (performance.now() - started)) + (move.t === 'pass' ? 1000 : 0));
      if (game !== current) return;
      resetUi();
      await perform(move);
      if (game === current) afterAction(move);
    }, 50);
    return;
  }
  if (settings.mode === 'hot' && action && !game.pending) { showCover(game.cur); return; }
  autoPassIfStuck();
}


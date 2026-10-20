/* ---------- replay: the finished battle again, from the start, move by move ---------- */
/** A random ready deck: each faction with a ready deck is equally likely, then each of its decks. */
function randomDeck(ready) {
  const facs = [...new Set(ready.map(deckFaction).filter(Boolean))];
  if (!facs.length) return ready[Math.floor(Math.random() * ready.length)];
  const fac = facs[Math.floor(Math.random() * facs.length)], list = ready.filter(d => deckFaction(d) === fac);
  return list[Math.floor(Math.random() * list.length)];
}
const deckFaction = d => { const k = Object.keys(d.cards || {}).find(x => CARDS[x] && d.cards[x] > 0); return k ? CARDS[k].fac : null; };
let replay = null, lastReplay = null;   // replay: { i, playing } while replaying
function startReplay() {
  if (!lastReplay) return;
  $('#endDlg').hidden = true;
  replay = { i: 0, playing: false };
  game = structuredClone(lastReplay.start);
  game.fx = [];
  prevStats = new Map(); animFx = null;
  resetUi(); hideTip();
  busy = false;
  $('#replayBar').hidden = false;
  render(); renderReplayBar();
}
function renderReplayBar() {
  if (!replay) return;
  const n = lastReplay.actions.length, done = replay.i >= n, o = other(viewer());
  $('#rbStep').textContent = `Move ${replay.i} / ${n}`;
  const sl = $('#rbSlider'); sl.max = n; if (!sl.matches(':active')) sl.value = replay.i;
  $('#rbPlay').textContent = replay.playing ? 'Pause' : 'Play';
  $('#rbPlay').disabled = done && !replay.playing;
  $('#rbNext').disabled = done || replay.playing || busy;
  $('#rbHandLbl').textContent = `${deckName(game, o)}'s hand · ${game.players[o].hand.length}`;
  const counts = {};
  for (const k of game.players[o].hand) counts[k] = (counts[k] || 0) + 1;
  $('#rbHand').innerHTML = Object.keys(counts).sort(byDeckOrder).map(k => deckItemHtml(k, counts[k], false)).join('') || '<p class="empty">Empty.</p>';
}
async function replayStep() {
  if (!replay || busy || replay.i >= lastReplay.actions.length) return;
  const current = game;
  await perform(lastReplay.actions[replay.i]);
  if (!replay || game !== current) return;
  replay.i++;
  busy = false;
  renderReplayBar();
}
async function replayPlay() {
  if (!replay) return;
  replay.playing = !replay.playing;
  renderReplayBar();
  while (replay && replay.playing && replay.i < lastReplay.actions.length) {
    await replayStep();
    if (replay && replay.playing) await sleep(500);
  }
  if (replay) { replay.playing = false; renderReplayBar(); }
}
/** Jump the replay to move i (from the start, without animations). */
function replayJump(i) {
  if (!replay) return;
  replay.playing = false;
  if (busy) { setTimeout(() => replayJump(i), 100); return; }
  const g = structuredClone(lastReplay.start);
  g.fx = [];
  for (let j = 0; j < i; j++) { applyAction(g, lastReplay.actions[j]); g.fx = []; }
  game = g; replay.i = i;
  $('#fxLayer').innerHTML = ''; stagedSpell = null; animFx = null; prevStats = new Map();
  resetUi(); hideTip(); render(); renderReplayBar();
}
function exitReplay() {
  if (!replay) return;
  replay = null;
  game = lastReplay.final;
  busy = false;
  $('#replayBar').hidden = true;
  resetUi(); hideTip();
  showEnd();
}

/** The game as it was before a human action that opened a follow-up choice (Esc takes the action back). */
let undoState = null;
/** Esc during a follow-up choice: finish it if it may be skipped, otherwise take back the whole action. */
function exitPending() {
  if (listActions(game).some(a => a.t === 'done')) { act({ t: 'done' }); return; }
  if (!undoState) return;
  game = undoState;
  undoState = null;
  resetUi();
  render();
  showToast('Taken back.', 'info');
}

let autoPassTimer = null;
const onlyPassLeft = () => !game.pending && !listActions(game).some(a => a.t !== 'pass');
function autoPassIfStuck() {
  clearTimeout(autoPassTimer);
  if (!myTurn() || !onlyPassLeft()) return;
  const turn = game.turn;
  showToast('No actions left. Passing…', 'info');
  autoPassTimer = setTimeout(() => { if (myTurn() && game.turn === turn && onlyPassLeft()) act({ t: 'pass' }); }, 2000);
}

function showCover(p, onReveal) {
  $('#coverName').textContent = deckName(game, p);
  $('#cover').hidden = false;
  $('#coverBtn').onclick = () => {
    $('#cover').hidden = true;
    if (onReveal) onReveal();
    else { render(); autoPassIfStuck(); }
  };
}

function showEnd() {
  render();
  if (game.replayStart) lastReplay = { start: game.replayStart, actions: game.history.slice(), final: game };
  $('#replayBtn').hidden = !lastReplay;
  $('#endText').textContent = game.winner === 'draw' ? 'The battle ends in a draw.' : game.winner === 'lost' ? 'Both sides lose the battle.' : `${deckName(game, game.winner)} wins the battle.`
    + (game.endReason ? ' ' + game.endReason : '');
  $('#endDlg').hidden = false;
}

function startGame() {
  clearTimeout(autoPassTimer);
  replay = null;
  $('#replayBar').hidden = true;
  $('#fxLayer').innerHTML = '';
  stagedSpell = null; animFx = null; prevStats = new Map();
  const ready = deckStore.decks.filter(x => deckPlayable(x));
  const mine = deckById(deckStore.pick), theirs = deckStore.opp === 'random' ? randomDeck(ready) : deckById(deckStore.opp);
  if (!mine || !theirs || !deckPlayable(mine) || !deckPlayable(theirs)) return;
  battleDeck('side0', mine); battleDeck('side1', theirs); nameMirrorSides();
  game = newGame('side0', 'side1', testGames);
  resetUi();
  busy = true;
  for (const id of ['#setup', '#endDlg', '#cover']) $(id).hidden = true;
  render();
  if (settings.mode === 'ai') { computerRedraw(game, 1); showMulligan(0, beginBattle); }
  else showMulligan(0, () => showCover(1, () => showMulligan(1, beginBattle)));
}

function beginBattle() {
  // both redraws are done: each side learns how many cards the other redrew
  game.redrawDone = true;
  const n = p => game.players[p].redrawn.length;
  log(game, `${deckName(game, 0)} redrew ${n(0)} card${n(0) === 1 ? '' : 's'}; ${deckName(game, 1)} redrew ${n(1)} card${n(1) === 1 ? '' : 's'}.`);
  const events = game.fx;
  game.fx = [];
  game.history = [];
  const start = structuredClone(game);
  delete start.history;
  game.replayStart = start;
  render();
  busy = true;
  const current = game;
  playEvents(events).then(() => { if (game !== current) return; busy = false; render(); afterAction(); });
}

/** Starting-hand screen: each card can be redrawn once. */
function showMulligan(p, done) {
  const redrawn = new Set();
  const draw = () => {
    $('#mullCards').innerHTML = game.players[p].hand.map((k, i) => {
      const used = redrawn.has(i), full = redrawn.size >= MAX_REDRAW;
      return `<button class="mc${used ? ' done' : ''}" data-i="${i}" ${used || full ? 'disabled' : ''}>${cardHtml(k)}<span class="rd">${used ? 'Redrawn' : full ? 'Kept' : 'Click to redraw'}</span></button>`;
    }).join('');
  };
  $('#mullName').textContent = deckName(game, p);
  $('#mull').hidden = false;
  draw();
  $('#mullCards').onclick = e => {
    const b = e.target.closest('.mc');
    if (!b || b.disabled || redrawn.size >= MAX_REDRAW) return;
    const i = +b.dataset.i;
    redraw(game, p, i);
    redrawn.add(i);
    Sound.draw();
    draw();
    renderHand();
    $('#mullCards').querySelector(`[data-i="${i}"]`).classList.add('swap');
  };
  $('#mullGo').onclick = () => { $('#mull').hidden = true; render(); done(); };
}


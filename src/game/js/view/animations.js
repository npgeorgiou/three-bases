/* =====================================================================
   ANIMATIONS: replay the events the engine emitted, in order
   ===================================================================== */
const unitNode = id => $('#board').querySelector(`g.unit[data-id="${id}"]`);
const centreDelta = (from, to) => [to.left + to.width / 2 - (from.left + from.width / 2), to.top + to.height / 2 - (from.top + from.height / 2)];

/** A fixed-position element in the effects layer, covering `rect`. */
function flyer(className, html, rect) {
  const d = document.createElement('div');
  d.className = className;
  d.innerHTML = html;
  Object.assign(d.style, { left: rect.left + 'px', top: rect.top + 'px', width: rect.width + 'px', height: rect.height + 'px' });
  $('#fxLayer').appendChild(d);
  return d;
}

async function playEvents(events) {
  const current = game;
  for (const e of events) {
    if (game !== current) return;   // a new game started: drop the old animations
    if (!e.snap) continue;
    if (e.place) { renderBoard(e.snap, { spawn: e.place, anim: true }); Sound.place(); await sleep(1000); }
    else if (e.move) await animateMove(e);
    else if (e.carry) await animateCarry(e);
    else if (e.round) { renderBoard(e.snap, { anim: true }); renderStacks(e.snap); await showRoundBanner(e); }
    else if (e.draw !== undefined) await animateDraw(e);
    else if (e.capture !== undefined) { renderBoard(e.snap, { anim: true }); Sound.capture(); await sleep(700); }
    else if (e.hit) await animateHits([e]);
    else if (e.dead) await animateDeath(e);
  }
}

/** A unit killed outright: it flies to its owner's discard pile. */
async function animateDeath(e) {
  const node = unitNode(e.dead);
  if (!node) return;
  node.classList.add('hitme');
  await sleep(350);
  Sound.death();
  await flyToDiscard(node, e.dead);
}
/** A dead unit leaves its cell for its owner's discard pile. */
async function flyToDiscard(node, id) {
  const u = game.units.find(x => x.id === id) || (game.deadUnits || []).find(x => x.id === id) || null;
  const rect = node.getBoundingClientRect(), owner = Number(node.dataset.owner);
  const pile = $(owner === viewer() ? '#pileMe .stack' : '#pileOpp .stack').getBoundingClientRect();
  const card = node.dataset.card || (u && u.card);
  const d = flyer('flyunit f-' + CARDS[card].fac, cardArt(card), rect);
  node.style.visibility = 'hidden';
  await d.animate([
    { transform: 'translate(0,0) scale(1)', opacity: 0.85 },
    { transform: `translate(${pile.left - rect.left}px,${pile.top - rect.top}px) scale(${pile.width / rect.width},${pile.height / rect.height})`, opacity: 0.3 },
  ], { duration: 420, easing: 'ease-in', fill: 'forwards' }).finished;
  d.remove();
}

/* ---------- card draws, round banner, carry-over and moves ---------- */

async function animateDraw(e) {
  renderStacks(e.snap);
  const mine = e.draw === viewer();
  const deck = $(mine ? '#deckMe .stack' : '#deckOpp .stack');
  if (!deck) { await sleep(300); return; }
  const slots = incomingSlots(mine, e.n || 1);
  const fac = DECKS[e.snap.players[e.draw].deck].fac, from = deck.getBoundingClientRect();
  const flights = slots.map((slot, i) => {
    const to = (slot.querySelector('.card') || slot).getBoundingClientRect();
    const d = flyer('flycard', `<div class="back f-${fac}" style="width:${from.width}px;height:${from.height}px">${deckArt(fac)}</div>`,
      { left: from.left, top: from.top, width: from.width, height: from.height });
    setTimeout(() => Sound.draw(), i * 180);
    return d.animate([
      { transform: 'translate(0,0) scale(1)' },
      { transform: `translate(${to.left - from.left}px,${to.top - from.top}px) scale(${to.width / from.width},${to.height / from.height})` },
    ], { duration: 520, delay: i * 180, easing: 'cubic-bezier(.3,.7,.3,1)', fill: 'forwards' })
      .finished.then(() => { d.remove(); slot.style.visibility = ''; });
  });
  await Promise.all(flights);
  await sleep(150);
}

/** The hand slots still waiting for their card (hidden until it arrives), in order: each arrival fills the first ones. */
const incomingSlots = (mine, n) => [...$(mine ? '#hand' : '#oppHand').children].filter(x => x.style.visibility === 'hidden').slice(0, n);

async function showRoundBanner(e) {
  Sound.gong();
  const board = $('#board').getBoundingClientRect();
  const d = document.createElement('div');
  d.className = 'rbanner';
  d.innerHTML = `<b>Round ${e.round}</b><span>${DECKS[e.snap.players[e.starter].deck].name} acts first</span>`;
  Object.assign(d.style, { left: board.left + board.width / 2 + 'px', top: board.top + board.height / 2 + 'px' });
  $('#fxLayer').appendChild(d);
  await d.animate([{ opacity: 0, transform: 'translate(-50%,-50%) scale(.7)' }, { opacity: 1, transform: 'translate(-50%,-50%) scale(1)' }],
    { duration: 250, easing: 'ease-out', fill: 'forwards' }).finished;
  await sleep(1100);
  await d.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 250, fill: 'forwards' }).finished;
  d.remove();
}

/** Leftover bread flies into the carry-over slots; the rest fades away. */
async function animateCarry(e) {
  renderBoard(e.snap, { anim: true });
  renderStacks(e.snap);
  await sleep(250);
  const flights = [];
  let slot = e.before;
  for (const lane of LANES) {
    const breads = [...$('#board').querySelectorAll(`[data-left="${e.p}-${lane}"]`)];
    if (!breads.length) continue;
    const moved = (e.carry.find(x => x[0] === lane) || [lane, 0])[1];
    const flying = moved ? breads.slice(-moved) : [];
    for (const b of flying) {
      const target = document.querySelector(`.carry[data-p="${e.p}"] [data-slot="${slot++}"]`);
      if (!target) continue;
      const from = b.getBoundingClientRect(), to = target.getBoundingClientRect();
      const d = flyer('flyer', breadHtml('sup'), from);
      b.style.visibility = 'hidden';
      const [dx, dy] = centreDelta(from, to);
      flights.push({ d, target, dx, dy, scale: to.width / from.width });
    }
    breads.forEach(b => { if (!flying.includes(b)) b.classList.add('lost'); });
  }
  if (!flights.length) { await sleep(400); return; }
  await Promise.all(flights.map((f, i) => f.d.animate(
    [{ transform: 'translate(0,0) scale(1)' }, { transform: `translate(${f.dx}px,${f.dy}px) scale(${f.scale})` }],
    { duration: 650, delay: i * 160, easing: 'cubic-bezier(.4,0,.2,1)', fill: 'forwards' },
  ).finished.then(() => {
    f.d.remove();
    f.target.firstElementChild.classList.remove('k-empty');
    f.target.firstElementChild.classList.add('k-sup', 'fill');
  })));
  await sleep(350);
}

async function animateMove(e) {
  renderBoard(e.snap, { mover: e.move, path: e.path, mo: e.o, toLane: e.toLane, anim: true });
  await sleep(600);
  const g = unitNode(e.move);
  if (!g) return;
  const [r0, c0] = e.path[0], [r1, c1] = e.path[e.path.length - 1];
  const duration = Math.max(380, e.steps * 380);
  Sound.march(e.steps, duration);
  const su = e.snap.units.find(x => x.id === e.move);
  if (su && e.o !== undefined && e.o !== su.o) {
    // a turn (with or without a move): one motion from the old body to the new one
    const [x0, y0, w0, h0] = unitRect(su), [x1, y1, w1, h1] = unitRect({ ...su, r: r1, c: c1, o: e.o });
    Object.assign(g.style, { transformBox: 'fill-box', transformOrigin: 'center' });
    await g.animate([{ transform: 'translate(0,0) rotate(0deg)' }, { transform: `translate(${x1 + w1 / 2 - x0 - w0 / 2}px,${y1 + h1 / 2 - y0 - h0 / 2}px) rotate(90deg)` }],
      { duration: Math.max(420, duration * 0.8), easing: 'ease-in-out', fill: 'forwards' }).finished;
  } else await g.animate([{ transform: 'translate(0,0)' }, { transform: `translate(${(c1 - c0) * CELL}px,${(r1 - r0) * CELL}px)` }],
    { duration, easing: 'ease-in-out', fill: 'forwards' }).finished;
  await sleep(200);
}


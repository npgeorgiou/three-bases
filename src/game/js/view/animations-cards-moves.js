/* ---------- spells: the card flies face up to the spell slot, acts from there, then goes to the discard pile ---------- */
let stagedSpell = null, spellOrigin = null, animFx = null;   // animFx: what the spell being cast highlights
let prevStats = new Map();   // unit id -> [strength, full defence] last drawn (stat gains puff)   // spellOrigin: where the player's played card was in the hand

function cardFlipper(k, fac) {
  const d = document.createElement('div');
  d.className = 'spellcard';
  d.innerHTML = `<div class="flip"><div class="face">${cardHtml(k)}</div><div class="face backface"><div class="back f-${fac}">${deckArt(fac)}</div></div></div>`;
  $('#fxLayer').appendChild(d);
  return d;
}

async function animateSpellIn(e) {
  renderBoard(e.snap, { anim: true });
  renderStacks(e.snap);
  const fac = DECKS[e.snap.players[e.p].deck].fac, mine = e.p === viewer();
  const d = cardFlipper(e.spell, fac), w = d.offsetWidth, h = d.offsetHeight;
  const slot = $('#spellSlot').getBoundingClientRect();
  const to = { left: slot.left + slot.width / 2 - w / 2, top: slot.top + slot.height / 2 - h / 2 };
  let from;
  if (mine && spellOrigin) from = { left: spellOrigin.left, top: spellOrigin.top };
  else { const hand = $(mine ? '#hand' : '#oppHand').getBoundingClientRect(); from = { left: hand.left + hand.width / 2 - w / 2, top: mine ? hand.top : hand.top - h + 30 }; }
  Object.assign(d.style, { left: to.left + 'px', top: to.top + 'px' });
  Sound.draw();
  const flip = d.querySelector('.flip');
  await Promise.all([
    d.animate([{ transform: `translate(${from.left - to.left}px,${from.top - to.top}px) scale(.8)` }, { transform: 'translate(0,0) scale(1)' }],
      { duration: 750, easing: 'cubic-bezier(.25,.8,.3,1)', fill: 'forwards' }).finished,
    flip.animate([{ transform: `rotateY(${mine ? 0 : 180}deg)` }, { transform: 'rotateY(0deg)' }],
      { duration: 750, easing: 'ease-in-out', fill: 'forwards' }).finished,
  ]);
  d.classList.add('cast');
  stagedSpell = d;
  spellOrigin = null;
  animFx = { lane: e.fxl ?? null, col: e.fxc ?? null, tid: e.fxt ?? null, foe: other(e.p) };
  renderBoard(e.snap, { anim: true });
  await sleep(mine ? 600 : 1000);
}

async function animateSpellOut(e) {
  const d = stagedSpell;
  stagedSpell = null;
  animFx = null;
  if (!d) { renderStacks(e.snap); return; }
  await sleep(250);
  d.classList.remove('cast');
  const pile = $(e.p === viewer() ? '#pileMe .stack' : '#pileOpp .stack').getBoundingClientRect(), r = d.getBoundingClientRect();
  await d.animate([{ transform: 'translate(0,0) scale(1)' },
    { transform: `translate(${pile.left - r.left}px,${pile.top - r.top}px) scale(${pile.width / r.width},${pile.height / r.height})` }],
    { duration: 600, easing: 'cubic-bezier(.4,0,.2,1)', fill: 'forwards' }).finished;
  d.remove();
  renderBoard(e.snap, { anim: true });
  renderStacks(e.snap);
}

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

/** A card enters a hand from somewhere other than the deck: it appears at its source (the spell slot when it's created, the discard pile when it returns) and flies into its slot. */
async function animateHandIn(e) {
  renderStacks(e.snap);
  const mine = e.handIn === viewer(), slot = incomingSlots(mine, 1)[0];
  if (!slot) { await sleep(200); return; }
  const fac = DECKS[e.snap.players[e.handIn].deck].fac, d = cardFlipper(e.k, fac), w = d.offsetWidth, h = d.offsetHeight;
  if (!mine) d.querySelector('.flip').style.transform = 'rotateY(180deg)';
  const src = (e.from === 'discard' ? $(mine ? '#pileMe .stack' : '#pileOpp .stack') : $('#spellSlot')).getBoundingClientRect();
  const to = (slot.querySelector('.card') || slot).getBoundingClientRect();
  const from = { left: src.left + src.width / 2 - w / 2, top: src.top + src.height / 2 - h / 2 };
  Object.assign(d.style, { left: from.left + 'px', top: from.top + 'px' });
  Sound.draw();
  if (e.from === 'create') await d.animate([{ transform: 'scale(.2)', opacity: 0, filter: 'brightness(2)' }, { transform: 'scale(1)', opacity: 1, filter: 'brightness(1)' }],
    { duration: 380, easing: 'cubic-bezier(.2,.8,.3,1.2)', fill: 'forwards' }).finished;
  d.style.transformOrigin = '0 0';
  await d.animate([{ transform: 'translate(0,0) scale(1)' }, { transform: `translate(${to.left - from.left}px,${to.top - from.top}px) scale(${to.width / w},${to.height / h})` }],
    { duration: 520, easing: 'cubic-bezier(.3,.7,.3,1)', fill: 'forwards' }).finished;
  slot.style.visibility = '';
  d.remove();
  await sleep(120);
}

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
  await sleep(e.charge ? 260 : 600);
  const g = unitNode(e.move);
  if (!g) return;
  const [r0, c0] = e.path[0], [r1, c1] = e.path[e.path.length - 1];
  const duration = e.charge ? Math.max(200, e.steps * 170) : Math.max(380, e.steps * 380);   // a charge: fast
  Sound.march(e.steps, duration);
  const su = e.snap.units.find(x => x.id === e.move), laneDx = su && e.toLane !== undefined ? LANE_X[e.toLane] - LANE_X[su.lane] : 0;
  if (su && e.o !== undefined && e.o !== su.o) {
    // a turn (with or without a move): one motion from the old body to the new one
    const [x0, y0, w0, h0] = unitRect(su), [x1, y1, w1, h1] = unitRect({ ...su, r: r1, c: c1, o: e.o, lane: e.toLane ?? su.lane });
    Object.assign(g.style, { transformBox: 'fill-box', transformOrigin: 'center' });
    await g.animate([{ transform: 'translate(0,0) rotate(0deg)' }, { transform: `translate(${x1 + w1 / 2 - x0 - w0 / 2}px,${y1 + h1 / 2 - y0 - h0 / 2}px) rotate(90deg)` }],
      { duration: Math.max(420, duration * 0.8), easing: 'ease-in-out', fill: 'forwards' }).finished;
  } else await g.animate([{ transform: 'translate(0,0)' }, { transform: `translate(${(c1 - c0) * CELL + laneDx}px,${(r1 - r0) * CELL}px)` }],
    { duration, easing: 'ease-in-out', fill: 'forwards' }).finished;
  await sleep(200);
}


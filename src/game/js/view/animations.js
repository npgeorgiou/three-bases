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
  for (let i = 0; i < events.length; i++) {
    const e = events[i];
    if (game !== current) return;   // a new game started: drop the old animations
    // during a Mass Grave flight, what happens along it waits for the flight to get there (the flight itself never waits)
    if (e.flight) { await animateFlight(e); continue; }
    if (!e.snap) continue;
    if (e.place) { renderBoard(e.snap, { spawn: e.place, anim: true }); Sound.place(); await sleep(1000); }
    else if (e.merge) { renderBoard(e.snap, { merged: e.merge, anim: true }); await sleep(800); }
    else if (e.move) await animateMove(e);
    else if (e.carry) await animateCarry(e);
    else if (e.round) { renderBoard(e.snap, { anim: true }); renderStacks(e.snap); await showRoundBanner(e); }
    else if (e.draw !== undefined) await animateDraw(e);
    else if (e.handIn !== undefined) await animateHandIn(e);
    else if (e.capture !== undefined) { renderBoard(e.snap, { anim: true }); Sound.capture(); await sleep(700); }
    else if (e.heal) await animateHeal(e);
    else if (e.spell) await animateSpellIn(e);
    else if (e.spellEnd) await animateSpellOut(e);
    else if (e.hit && e.drain) { renderBoard(e.snap, { anim: true }); await animateDrain(e); }
    else if (e.hit) {
      // the hits of one step (same group, different units) play together
      const group = [e];
      while (i + 1 < events.length) {
        const n = events[i + 1];
        if (!n.hit || n.drain || n.grp !== e.grp || group.some(x => x.t === n.t)) break;
        group.push(n); i++;
      }
      await animateHits(group);
    }
    else if (e.grow) { renderBoard(e.snap, { anim: true }); await sleep(420); }
    else if (e.dead) await animateDeath(e);
    else if (e.resolve) await animateResolve(e);
    else if (e.resolved) await animateResolved(e);
    else if (e.toss) await animateToss(e);
    else if (e.fly) await animateFly(e);
    else if (e.exit) await animateExit(e);
  }
}

/** A Place effect's target was picked: it gets the white picked marker before the effect plays. */
async function flashPick(id) {
  renderBoard(game, { anim: true });
  const u = byId(game, id);
  if (!u) return;
  drawMark($('#board'), u, 'pick');
  Sound.draw();
  await sleep(480);
}

/** A unit killed outright (a spell, a sacrifice, Reckless): it flies to its owner's discard pile. */
async function animateDeath(e) {
  renderBoard(e.snap, { anim: true });
  const target = unitNode(e.dead);
  if (!target) return;
  target.classList.add('hitme');
  await sleep(350);
  Sound.death();
  await dropTombstones([target]);
  await sleep(120);
}
const TOMB_SVG = '<svg viewBox="0 0 100 100" aria-hidden="true"><path class="tst" d="M24 92V40C24 18 76 18 76 40V92Z"/><path class="tsx" d="M50 36V70M38 48H62"/><path class="tsg" d="M12 92H88"/></svg>';
/** Units that die: a tombstone drops onto each of them at the same moment and stays until its death resolves. */
async function dropTombstones(nodes, instant = false) {
  await Promise.all(nodes.map(node => {
    const r = node.getBoundingClientRect(), size = Math.min(r.width, r.height) * 0.62;
    const box = { left: r.left + r.width / 2 - size / 2, top: r.top + r.height / 2 - size / 2 + size * 0.08, width: size, height: size };
    const d = flyer('flyer tombfly', TOMB_SVG, box);
    node.classList.add('deadpawn');   // the dead unit stays visible, dimmed, under its tombstone
    if (instant) return Promise.resolve();   // it already dropped (Mass Grave: as the killing flier passed over)
    return d.animate([{ transform: 'translateY(-70px) scale(1.15)', opacity: 0 }, { transform: 'translateY(4px) scale(1)', opacity: 1, offset: 0.8 }, { transform: 'translateY(0) scale(1)', opacity: 1 }],
      { duration: 420, easing: 'cubic-bezier(.4,0,.8,.4)', fill: 'forwards' }).finished;
  }));
}
/** A death starts resolving: its cell gets a white border and its tombstone lights up, for as long as its chain runs. */
async function animateResolve(e) {
  renderBoard(e.snap, { anim: true });
  Sound.draw();
  await sleep(380);
}
/** A death's chain is done: the dead unit and its tombstone leave for the discard pile. */
async function animateResolved(e) {
  const t = e.tomb, spot = t;
  const rect = screenRectOf(spot.lane, spot.owner, spot.cells);
  renderBoard(e.snap, { anim: true });
  const pile = $(t.ctl === viewer() ? '#pileMe .stack' : '#pileOpp .stack').getBoundingClientRect();
  const d = flyer('flyunit f-' + CARDS[t.card].fac, cardArt(t.card), rect);
  await d.animate([
    { transform: 'translate(0,0) scale(1)', opacity: 0.85 },
    { transform: `translate(${pile.left - rect.left}px,${pile.top - rect.top}px) scale(${pile.width / rect.width},${pile.height / rect.height})`, opacity: 0.3 },
  ], { duration: 420, easing: 'ease-in', fill: 'forwards' }).finished;
  d.remove();
}
/** Mass Grave: a unit lunges at the enemy it strikes. */
async function animateFly(e) {
  renderBoard(e.snap, { anim: true });
  const g = unitNode(e.fly), t = unitNode(e.to);
  if (!g || !t) return;
  const a = g.getBoundingClientRect(), b = t.getBoundingClientRect(), [dx, dy] = centreDelta(a, b), m = g.getScreenCTM();
  const k = m ? 1 / m.a : 1;
  Object.assign(g.style, { transformBox: 'fill-box', transformOrigin: 'center' });
  await g.animate([{ transform: 'translate(0,0)' }, { transform: `translate(${dx * k * 0.8}px,${dy * k * 0.8}px)` }], { duration: 300, easing: 'ease-in', fill: 'forwards' }).finished;
}
/** A unit leaves the game (Mass Grave with no enemy left): it flies off the board over the enemy camp. */
async function animateExit(e) {
  renderBoard(e.snap, { anim: true });
  const g = unitNode(e.exit), u = e.snap.units.find(x => x.id === e.exit);
  if (!g || !u) return;
  const up = u.owner === viewer() ? -1 : 1;
  Object.assign(g.style, { transformBox: 'fill-box', transformOrigin: 'center' });
  await g.animate([{ transform: 'translate(0,0)', opacity: 1 }, { transform: `translate(0,${up * 420}px) scale(.7)`, opacity: 0 }], { duration: 650, easing: 'ease-in', fill: 'forwards' }).finished;
}

/** Restored shields: the unit glows green and "+n" rises from its defence. */
/** Drain: drops of life stream from the target into the drainer. */
async function animateDrain(e) {
  const from = unitNode(e.t), to = e.src ? unitNode(e.src) : null;
  if (!from) return;
  from.classList.add('drained');
  if (to) to.classList.add('drainer');
  Sound.hit();
  const a = from.getBoundingClientRect(), b = to ? to.getBoundingClientRect() : a;
  const ax = a.left + a.width / 2, ay = a.top + a.height / 2, bx = b.left + b.width / 2, by = b.top + b.height / 2;
  const n = Math.max(4, Math.min(10, e.str * 4)), runs = [];
  for (let i = 0; i < n; i++) {
    const d = document.createElement('div');
    d.className = 'lifedrop';
    $('#fxLayer').appendChild(d);
    const bend = (i % 2 ? 1 : -1) * (14 + (i * 7) % 22), mx = (ax + bx) / 2 + bend, my = (ay + by) / 2 - 18;
    runs.push(d.animate([
      { transform: `translate(${ax - 5}px, ${ay - 5}px) scale(.6)`, opacity: 0 },
      { transform: `translate(${ax - 5}px, ${ay - 5}px) scale(1)`, opacity: 1, offset: .12 },
      { transform: `translate(${mx - 5}px, ${my - 5}px) scale(1.15)`, opacity: 1, offset: .55 },
      { transform: `translate(${bx - 5}px, ${by - 5}px) scale(.5)`, opacity: 0 },
    ], { duration: 850, delay: i * 70, easing: 'ease-in-out', fill: 'forwards' }).finished.then(() => d.remove()));
  }
  await Promise.all(runs);
  from.classList.remove('drained');
  if (to) to.classList.remove('drainer');
}
async function animateHeal(e) {
  renderBoard(e.snap, { anim: true });
  const g = unitNode(e.heal);
  if (!g) return;
  g.classList.add('healed');
  Sound.heal();
  const anchor = (g.querySelector('.k-def') || g).getBoundingClientRect();
  const d = flyer('healnum', '+' + e.n, { left: anchor.left, top: anchor.top - 6, width: anchor.width, height: anchor.height });
  await d.animate([{ transform: 'translateY(0)', opacity: 1 }, { transform: 'translateY(-26px)', opacity: 0 }], { duration: 900, easing: 'ease-out', fill: 'forwards' }).finished;
  d.remove();
  g.classList.remove('healed');
}


/**
 * Attacker frame, target frame, red strength markers fly to the defence, then the target breaks or dies.
 * Hits of one step (a charge into two units, a blast, Pyre) play together: they take their damage at once.
 */
async function animateHits(list) {
  renderBoard(list[0].snap, { anim: true });
  const items = list.map(e => ({ e, attacker: e.src && !e.how ? unitNode(e.src) : null, target: unitNode(e.t) })).filter(x => x.target);
  if (!items.length) return;
  if (items.some(x => x.e.how === 'charge')) return animateChargeImpact(items);
  if (items.some(x => x.e.how === 'thrown' || x.e.how === 'flight')) return animateLanding(items);
  const attackers = [...new Set(items.map(x => x.attacker).filter(Boolean))];
  if (attackers.length) { attackers.forEach(g => g.classList.add('atk')); await sleep(500); }
  items.forEach(x => x.target.classList.add('hitme'));
  await sleep(attackers.length ? 250 : 350);
  $$('#fxLayer .flyer').forEach(x => x.remove());   // leftovers only; a staged spell card stays

  const hot = new Set(), flights = [];
  for (const x of items) {
    const { e, attacker, target } = x;
    const strBadge = attacker ? attacker.querySelector('.k-str') : null;
    const source = attacker ? e.snap.units.find(u => u.id === e.src) : null;
    // damage comes from where it is dealt: the unit's strength, a dead unit's cell (its Death effects), or the spell card
    const fromNode = !attacker && e.from ? (unitNode(e.from) || $('#board').querySelector(`g.tomb[data-tomb="${e.from}"]`)) : null;
    const spell = !attacker && !fromNode ? stagedSpell : null;
    const origin = strBadge || fromNode || (spell && spell.querySelector('.card'));
    const markers = strBadge && source ? Math.min(12, e.str) : origin ? Math.min(8, e.str) : 0;
    if (strBadge) hot.add(strBadge);
    if (fromNode) fromNode.classList.add('src');
    x.defBadge = target.querySelector('.k-def');
    x.targetRect = target.getBoundingClientRect();
    const aim = (x.defBadge || target).getBoundingClientRect();
    for (let i = 0; i < markers; i++) {
      const b = origin.getBoundingClientRect(), size = strBadge ? b.width : 30, off = (i - (markers - 1) / 2) * 4;
      const from = { left: b.left + b.width / 2 - size / 2 + off, top: b.top + b.height / 2 - size / 2 + off, width: size, height: size };
      const d = flyer('flyer', '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="7" fill="#E0402F" stroke="#fff" stroke-width="2"/></svg>', from);
      const [dx, dy] = centreDelta(from, aim);
      flights.push({ d, dx, dy, i });
    }
  }
  if (hot.size) { hot.forEach(b => b.classList.add('k-hot')); await sleep(300); }
  hot.forEach(b => { b.style.visibility = 'hidden'; });
  await Promise.all(flights.map(f => f.d.animate([{ transform: 'translate(0,0)' }, { transform: `translate(${f.dx}px,${f.dy}px) scale(1.15)` }],
    { duration: 380, delay: f.i * 70, easing: 'cubic-bezier(.5,0,.9,.6)', fill: 'forwards' }).finished));

  for (const { e, target, defBadge } of items) {
    const defNumber = target.querySelector('.defnum');
    if (defNumber) {
      const remaining = Math.max(0, +defNumber.textContent - e.broke);
      defNumber.textContent = remaining;
      if (remaining === 0 && defBadge) defBadge.classList.add('k-broken');
    }
    target.classList.add('shake');
    if (e.blocked) {
      const b = (defBadge || target).getBoundingClientRect();
      const d = flyer('blocknum', 'Armour', { left: b.left - 14, top: b.top - 4, width: b.width + 28, height: 20 });
      d.animate([{ transform: 'translateY(0)', opacity: 1 }, { transform: 'translateY(-22px)', opacity: 0 }], { duration: 900, easing: 'ease-out', fill: 'forwards' }).finished.then(() => d.remove());
    }
  }
  Sound.hit();
  await sleep(220);
  await Promise.all(flights.map(f => f.d.animate([{ transform: `translate(${f.dx}px,${f.dy}px)` }, { transform: 'translate(0,0)' }],
    { duration: 320, easing: 'ease-out', fill: 'forwards' }).finished));
  flights.forEach(f => f.d.remove());
  hot.forEach(b => { b.style.visibility = ''; b.classList.remove('k-hot'); });

  // the units this step kills die at the same moment: a tombstone drops on each
  const dying = items.filter(x => x.e.kill);
  if (dying.length) { Sound.death(); await dropTombstones(dying.map(x => x.target)); }
  await sleep(150);
  attackers.forEach(g => g.classList.remove('atk'));
}

/** Mass Grave: all the fliers take off together and glide straight on through the enemy camp without stopping; each vanishes
 *  where it strikes, or flies off the board; an enemy it kills gets its tombstone as that flier passes over it. */
async function animateFlight(e) {
  renderBoard(e.snap, { anim: true });
  const m = $('#board').getScreenCTM(), runs = [];
  // board y of a lane row (0-2 the top camp, 3-5 the bottom one), so crossing the base takes one cell's time too
  const yOf = R => (R < 0 ? TOP_Y - CELL * 1.5 : R > 5 ? BOTTOM_Y + ROWS * CELL + CELL * 0.5 : R <= 2 ? TOP_Y + R * CELL : BOTTOM_Y + (R - ROWS) * CELL);
  for (const f of e.flight) {
    const node = unitNode(f.id), rect = node ? node.getBoundingClientRect() : screenRectOf(f.lane, f.owner, f.cells);
    if (node) node.style.visibility = 'hidden';
    const d = flyer('flyunit flier f-' + CARDS[f.card].fac, cardArt(f.card), rect);
    const top = f.owner === 1, R0 = Math.min(...f.cells.map(([r]) => (top ? r : r + ROWS))), R1 = R0 + f.dir * f.end;
    const dy = (yOf(Math.max(-1, Math.min(6, R1))) - yOf(R0)) * (m ? m.d : 1), dur = f.end * e.ms;
    if (f.grave) setTimeout(() => { const t = unitNode(f.grave); if (t) dropTombstones([t]); Sound.death(); }, 120 + dur);
    runs.push(d.animate([
      { transform: 'translate(0,0) scale(1)', opacity: 0.95 },
      { transform: `translate(0,${dy * 0.12}px) scale(1.04)`, opacity: 0.85, offset: 0.12 },
      { transform: `translate(0,${dy}px) scale(${f.out ? 0.7 : 0.85})`, opacity: f.out ? 0 : 0.6 },
    ], { duration: dur, delay: 120, easing: 'linear', fill: 'forwards' }).finished.then(() => {
      if (f.out) { d.remove(); return; }
      return d.animate([{ opacity: 0.6 }, { opacity: 0, transform: `translate(0,${dy}px) scale(1.3)` }], { duration: 160, fill: 'forwards' }).finished.then(() => d.remove());
    }));
  }
  await Promise.all(runs);
  await sleep(500);   // the tombstones dropped during the flight settle before the strikes are counted
}
/** Defence numbers drop, the targets shake, and the units this step kills get their tombstones. */
async function landHits(items, instantStones = false) {
  for (const { e, target } of items) {
    const defNumber = target.querySelector('.defnum'), defBadge = target.querySelector('.k-def');
    if (defNumber) {
      const remaining = Math.max(0, +defNumber.textContent - e.broke);
      defNumber.textContent = remaining;
      if (remaining === 0 && defBadge) defBadge.classList.add('k-broken');
    }
    if (e.blocked) {
      const b = (defBadge || target).getBoundingClientRect();
      const d = flyer('blocknum', 'Armour', { left: b.left - 14, top: b.top - 4, width: b.width + 28, height: 20 });
      d.animate([{ transform: 'translateY(0)', opacity: 1 }, { transform: 'translateY(-22px)', opacity: 0 }], { duration: 900, easing: 'ease-out', fill: 'forwards' }).finished.then(() => d.remove());
    }
  }
  Sound.hit();
  const dying = items.filter(x => x.e.kill);
  if (dying.length) { Sound.death(); await dropTombstones(dying.map(x => x.target), instantStones); }
}
/** The board's elements of one lane, gathered in a group so the lane can shake. */
function laneGroup(lane) {
  const svg = $('#board'), g = svgEl('g', { class: 'laneshake' }), x0 = LANE_X[lane] - 16, x1 = LANE_X[lane] + CELL * 3 + 16;
  for (const el of [...svg.children]) {
    let b; try { b = el.getBBox(); } catch (err) { continue; }
    const cx = b.x + b.width / 2;
    if (b.width && cx >= x0 && cx <= x1 && b.width < x1 - x0 + 40) g.appendChild(el);
  }
  svg.appendChild(g);
  return g;
}
/** A charge: the charger rushes into the enemies ahead, knocks them back, the lane shakes front to back, and all settle. */
async function animateChargeImpact(items) {
  const e0 = items[0].e, src = e0.snap.units.find(u => u.id === e0.src), lane = src ? src.lane : 0;
  const lg = laneGroup(lane), a = unitNode(e0.src), dir = src && src.owner === viewer() ? -1 : 1;
  const m = $('#board').getScreenCTM(), k = m ? m.a : 1;   // screen px per board unit
  const reach = CELL * 0.62 * k;
  const fly = (node, kf, opt) => { if (!node) return Promise.resolve(); Object.assign(node.style, { transformBox: 'fill-box', transformOrigin: 'center' }); return node.animate(kf, { fill: 'forwards', ...opt }).finished; };
  items.forEach(x => x.target.classList.add('hitme'));
  await fly(a, [{ transform: 'translate(0,0)' }, { transform: `translate(0,${dir * reach}px) scale(1.06)` }], { duration: 150, easing: 'cubic-bezier(.6,0,1,.6)' });
  // impact: the struck units are knocked back, the lane shakes front to back
  const knock = items.map(x => fly(x.target, [{ transform: 'translate(0,0)' }, { transform: `translate(0,${dir * 12 * k}px)` }, { transform: 'translate(0,0)' }], { duration: 420, easing: 'cubic-bezier(.2,.9,.3,1)' }));
  lg.animate([{ transform: 'translateY(0)' }, { transform: `translateY(${dir * 5}px)` }, { transform: `translateY(${-dir * 4}px)` }, { transform: `translateY(${dir * 2}px)` }, { transform: 'translateY(0)' }], { duration: 360, easing: 'ease-out' });
  await landHits(items);
  await Promise.all([...knock, fly(a, [{ transform: `translate(0,${dir * reach}px) scale(1.06)` }, { transform: 'translate(0,0)' }], { duration: 260, easing: 'ease-out' })]);
  await sleep(150);
}
/** A thrown unit lands on a unit: impact, no markers. */
async function animateLanding(items) {
  for (const x of items) { const n = unitNode(x.e.src); if (n) n.style.visibility = 'hidden'; x.target.classList.add('hitme'); x.target.classList.add('shake'); }
  await landHits(items, items.some(x => x.e.how === 'flight'));
  await sleep(200);
}
/** Ogre Thrower: the ally flies in an arc from its cell to where it is thrown. */
async function animateToss(e) {
  renderBoard(e.snap, { anim: true });
  const g = unitNode(e.toss), u = e.snap.units.find(x => x.id === e.toss), thrower = unitNode(e.by);
  if (!g || !u) return;
  if (thrower) { thrower.classList.add('atk'); await sleep(300); }
  const from = g.getBoundingClientRect(), to = screenRectOf(e.to.lane, e.to.owner, [[e.to.r, e.to.c]]);
  const d = flyer('flyunit f-' + CARDS[u.card].fac, cardArt(u.card), from);
  g.style.visibility = 'hidden';
  const dx = to.left - from.left, dy = to.top - from.top, lift = -Math.max(60, Math.abs(dy) * 0.45);
  Sound.march(1, 300);
  await d.animate([
    { transform: 'translate(0,0) scale(1) rotate(0deg)' },
    { transform: `translate(${dx / 2}px,${dy / 2 + lift}px) scale(1.25) rotate(180deg)`, offset: 0.5 },
    { transform: `translate(${dx}px,${dy}px) scale(1) rotate(360deg)` },
  ], { duration: 620, easing: 'cubic-bezier(.35,.1,.5,1)', fill: 'forwards' }).finished;
  d.remove();
  if (thrower) thrower.classList.remove('atk');
}
/** Screen rectangle of some cells of a camp. */
function screenRectOf(lane, owner, cells) {
  const svg = $('#board'), m = svg.getScreenCTM(), xy = cells.map(([r, c]) => cellXY(lane, owner, r, c));
  const x0 = Math.min(...xy.map(p => p[0])), y0 = Math.min(...xy.map(p => p[1])), x1 = Math.max(...xy.map(p => p[0])) + CELL, y1 = Math.max(...xy.map(p => p[1])) + CELL;
  const pt = svg.createSVGPoint();
  pt.x = x0; pt.y = y0; const a = pt.matrixTransform(m);
  pt.x = x1; pt.y = y1; const b = pt.matrixTransform(m);
  return { left: a.x, top: a.y, width: b.x - a.x, height: b.y - a.y };
}


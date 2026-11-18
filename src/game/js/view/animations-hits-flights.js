/** An attack: attacker frame, target frame, red strength markers fly to the defence, then the target breaks or dies. */
async function animateHits(list) {
  renderBoard(list[0].snap, { anim: true });
  const items = list.map(e => ({ e, attacker: e.src ? unitNode(e.src) : null, target: unitNode(e.t) })).filter(x => x.target);
  if (!items.length) return;
  const attackers = [...new Set(items.map(x => x.attacker).filter(Boolean))];
  if (attackers.length) { attackers.forEach(g => g.classList.add('atk')); await sleep(500); }
  items.forEach(x => x.target.classList.add('hitme'));
  await sleep(attackers.length ? 250 : 350);
  $$('#fxLayer .flyer').forEach(x => x.remove());

  const hot = new Set(), flights = [];
  for (const x of items) {
    const { e, attacker, target } = x;
    const strBadge = attacker ? attacker.querySelector('.k-str') : null;
    const markers = strBadge ? Math.min(12, e.str) : 0;
    if (strBadge) hot.add(strBadge);
    x.defBadge = target.querySelector('.k-def');
    const aim = (x.defBadge || target).getBoundingClientRect();
    for (let i = 0; i < markers; i++) {
      const b = strBadge.getBoundingClientRect(), size = b.width, off = (i - (markers - 1) / 2) * 4;
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
  }
  Sound.hit();
  await sleep(220);
  await Promise.all(flights.map(f => f.d.animate([{ transform: `translate(${f.dx}px,${f.dy}px)` }, { transform: 'translate(0,0)' }],
    { duration: 320, easing: 'ease-out', fill: 'forwards' }).finished));
  flights.forEach(f => f.d.remove());
  hot.forEach(b => { b.style.visibility = ''; b.classList.remove('k-hot'); });

  // a killed target leaves for its owner's discard pile
  const dying = items.filter(x => x.e.kill);
  if (dying.length) { Sound.death(); await Promise.all(dying.map(x => flyToDiscard(x.target, x.e.t))); }
  await sleep(150);
  attackers.forEach(g => g.classList.remove('atk'));
}


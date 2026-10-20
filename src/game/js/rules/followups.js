/* ---------- follow-up choices ---------- */
/** Eligible defectors for Presbeutes: enemy 1-supply units in the lane that fit somewhere in p's camp. */
/** Enemies Monomachos can pull: they can move at least one cell forward. */
const pullable = (s, p, lane) => unitsIn(s, other(p), lane).filter(t => !kw(t, 'fixed') && fitsCells(s, t.owner, t.lane, offsetsOf(t, t.o), t.r + fwd(t.owner), t.c, t.id));
const defectors = (s, p, lane) => unitsIn(s, other(p), lane).filter(t => unitSupply(t) === 1 && spotsFor(s, p, lane, t).length);

/** Open the follow-up choice of a unit's Place ability, or resolve it at once when there is no choice. */
function startOnPlace(s, p, u) {
  const k = cardOf(u).onPlace, lane = u.lane, choose = !s.inEnd && s.cur === p && !s.pending;
  if (!choose && ['mandator', 'pull', 'defect'].includes(k)) return;   // ('letter' then strikes only itself)   // a choice nobody can make now: nothing happens
  if (!choose && k === 'cinder') { damageFacing(s, u, abilityHit(u, 1), unitName(u)); return; }
  if (k === 'mandator') s.pending = { k: 'free', p, lane, n: 1, ex: u.id, src: u.id };
  else if (k === 'pull' && pullable(s, p, lane).length) s.pending = { k: 'pull', p, lane, src: u.id };
  else if (k === 'defect' && defectors(s, p, lane).length) s.pending = { k: 'defect', p, lane, src: u.id };
  else if (k === 'letter') {
    const amt = abilityHit(u, 1);
    if (choose && s.units.some(x => x.id !== u.id && !isIncorp(x))) s.pending = { k: 'letter', p, lane, src: u.id, amt };
    else hitUnit(s, amt, u, unitName(u) + ' (itself)', null, true, true, true);
  }
  else if (k === 'cinder') {
    if (unitsIn(s, p, lane).some(x => x.id !== u.id)) s.pending = { k: 'cinder', p, lane, src: u.id, amt: abilityHit(u, 1) };
    else damageFacing(s, u, abilityHit(u, 1), unitName(u));
  }
  else exStartOnPlace(s, p, u);
}

/** The choices open in a pending follow-up (never "pass"). */
function pendingActions(s) {
  const P = s.pending, p = P.p, out = [];
  const pick = list => list.forEach(t => out.push({ t: 'pick', tid: t.id }));
  if (P.k === 'free') {
    for (const u of unitsIn(s, p, P.lane)) if (u.id !== P.ex)
      for (const o of orientationsOf(u))
        for (const m of Object.values(moveTargets(s, u, o, true))) out.push({ t: 'fmove', id: u.id, r: m.r, c: m.c, o });
    if (out.length) out.push({ t: 'done' });
  } else if (P.k === 'pull') pick(pullable(s, p, P.lane));
  else if (P.k === 'defect') pick(defectors(s, p, P.lane));
  else if (P.k === 'cinder') pick(unitsIn(s, p, P.lane).filter(x => x.id !== P.src));
  else if (P.k === 'duel') { const v = byId(s, P.vid); if (v) pick(unitsIn(s, other(p), v.lane)); }
  else if (P.k === 'pair') { const v = byId(s, P.vid); if (v) pick(besideUnits(s, v)); }
  else if (P.k === 'place') {
    const t = P.card ? { card: P.card, owner: -1 } : byId(s, P.tid);
    if (t) spotsFor(s, p, P.lane, t).forEach(x => out.push({ t: 'place', ...x }));
  }
  else if (P.k === 'grave') { graveOptions(s, p, P.mode, P.pool).forEach(k => out.push({ t: 'gpick', key: k })); if (out.length && P.mode !== 'spell') out.push({ t: 'done' }); }
  else if (P.k === 'surgeon') pick(s.units.filter(u => ctl(u) === p));
  else if (P.k === 'embalm') pick(s.units.filter(u => ctl(u) === p && !kw(u, 'revenant')));
  else if (P.k === 'letter') pick(s.units.filter(x => x.id !== P.src && !isIncorp(x)));
  else if (P.k === 'kiss') pick(s.units.filter(u => ctl(u) !== p));
  else if (P.k === 'vsrc') pick(s.units.filter(u => ctl(u) === p && movableKw(u).length));
  else if (P.k === 'vkw') { const v = byId(s, P.vid); if (v) movableKw(v).forEach(f => out.push({ t: 'kpick', f })); }
  else if (P.k === 'vdst') pick(s.units.filter(u => ctl(u) === p && u.id !== P.vid));
  return out;
}
const PENDING_STEPS = new Set(['fmove', 'pick', 'place', 'done', 'gpick', 'kpick']);
/** What the pending choice asks the player to do (for the screen). */
function pendingPrompt(s) {
  const P = s.pending;
  if (!P) return '';
  const src = P.src ? CARDS[(byId(s, P.src) || {}).card || ''] : null, name = src ? src.name : '';
  return {
    free: `${name || 'Reform Ranks'}: move ${P.n > 1 ? `up to ${P.n} of your units` : 'another of your units'} in lane ${P.lane + 1} (free). Done when finished.`,
    pull: `${name}: pick an enemy unit in lane ${P.lane + 1} to pull forward.`,
    defect: `${name}: pick an enemy 1-supply unit in lane ${P.lane + 1} to win over.`,
    cinder: `${name}: pick another of your units in lane ${P.lane + 1} to strike with 1.`,
    duel: 'Monomachia: pick the enemy to duel.',
    pair: 'Synaspismos: pick the unit directly beside it.',
    place: P.card ? `${name || CARDS[P.card].name}: pick a free spot in lane ${P.lane + 1} for ${CARDS[P.card].name} (R rotates).` : 'Pick a free spot in your camp for the defector (R rotates).',
    grave: P.mode === 'spell' ? `${name}: pick a spell to return to your hand.` : `${name || 'Requiem'}: pick a unit from your discard pile (${P.left} left)${P.mode === 'rez' ? ' to resurrect' : ' to return to your hand'}.`,
    surgeon: `${name}: pick one of your units to operate on (strike 1, then +2 strength).`,
    embalm: `${name}: pick one of your units to gain Revenant.`,
    letter: `${name}: pick the unit it strikes with ${P.amt} (it also strikes itself).`,
    kiss: 'Kiss of the Revenant: pick the enemy to deal 3 damage to.',
    vsrc: `${name}: pick the unit to take a keyword from.`,
    vkw: `${name}: pick the keyword to move.`,
    vdst: `${name}: pick the unit to receive it.`,
  }[P.k];
}


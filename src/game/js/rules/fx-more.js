/* ---------- more card effects for the seven factions of 4 Nov 2026: winding, offerings, waves, omens, marks ----------
   Triggers added: kill (my hit kills an enemy), enemyPlace (an enemy is placed in my lane), allyAttack (another ally in my
   lane attacks), targeted (one of your spells targets me), healed (my shields are restored), allySurvive (an ally in my lane
   survives damage); survive gets the attacker as "it". Ops added: tick (its round-end effects happen now; Geared allies
   touching it too), ready (it may move and attack again this round), advance (moves straight forward as far as it can),
   offer (the ally directly behind me dies; later ops with if: {offered} need it), raise (a unit card from the discard pile
   comes back), sup (lasting supply change). */
const deathsThisRound = s => (s.dR && s.dR.r === s.round ? s.dR.n : 0);
const attacksThisRound = (s, p) => (s.aR && s.aR[p] && s.aR[p].r === s.round ? s.aR[p].n : 0);
const fxCount = n => Array.from({ length: Math.max(0, n) }, () => ({}));
/** The ally of u directly behind (dir -1) or in front (dir 1) of it, in the same column. */
function fxNextInCol(s, u, dir) {
  if (!u || !byId(s, u.id)) return null;
  const rows = cellsOf(u).map(x => x[0]), step = fwd(u.owner) * dir;
  const edge = dir > 0 ? (step < 0 ? Math.min(...rows) : Math.max(...rows)) : (step < 0 ? Math.max(...rows) : Math.min(...rows));
  const r = edge + step, cols = colsOf(u);
  return fxCamp(s, u.owner, u.lane).find(x => x.id !== u.id && ctl(x) === ctl(u) && cellsOf(x).some(([xr, xc]) => xr === r && cols.includes(xc))) || null;
}
Object.assign(FX_SEL, {
  deathsR: s => fxCount(deathsThisRound(s)),
  attacksR: (s, c) => fxCount(attacksThisRound(s, c.p)),
  spellsR: (s, c) => fxCount(spellsThisRound(s, c.p)),
  handN: (s, c) => fxCount(s.players[c.p].hand.length),
  behind: (s, c) => one(fxNextInCol(s, c.u, -1)),
  ahead: (s, c) => one(fxNextInCol(s, c.u, 1)),
  itBehind: (s, c) => one(fxNextInCol(s, c.t, -1)),
  // the enemy furthest from the base in my lane (back row first, then reading order)
  deepest: (s, c) => one(FX_SEL.enemies(s, c).sort((a, b) => seatKey(b, c.p) - seatKey(a, c.p))[0]),
  hurtEnemies: (s, c) => FX_SEL.enemies(s, c).filter(isBloodied),
  marked: (s, c) => FX_SEL.enemies(s, c).filter(x => kw(x, 'marked')),
  markedAll: (s, c) => s.units.filter(x => ctl(x) !== c.p && kw(x, 'marked')),
  geared: (s, c) => FX_SEL.team(s, c).filter(x => kw(x, 'geared')),
  frontAllies: (s, c) => FX_SEL.team(s, c).filter(inFront),
  backAllies: (s, c) => FX_SEL.team(s, c).filter(x => !inFront(x)),
  shellsHand: (s, c) => fxCount(s.players[c.p].hand.filter(k => CARDS[k] && CARDS[k].shellCard).length),
  hurtTeam: (s, c) => FX_SEL.team(s, c).filter(x => (x.dmg || 0) > 0),
  discardUnits: (s, c) => fxCount(s.players[c.p].discard.filter(k => CARDS[k] && !CARDS[k].tactic).length),
  partsHand: (s, c) => fxCount(s.players[c.p].hand.filter(k => CARDS[k] && CARDS[k].part).length),
  itTwins: (s, c) => (c.t ? s.units.filter(x => ctl(x) === c.p && x.lane !== c.t.lane && baseKey(x.card) === baseKey(c.t.card)) : []),
  otherFront: (s, c) => LANES.filter(l => l !== c.lane).map(l => s.units.filter(x => ctl(x) === c.p && x.lane === l && (cardOf(x).fx || []).some(f => f.on === 'roundEnd')).sort(byReadingOrder)[0]).filter(Boolean),
  itFacing: (s, c) => one(c.t && byId(s, c.t.id) ? fxFacing(s, c.t) : null),
  hurtAll: (s, c) => s.units.filter(x => ctl(x) !== c.p && isBloodied(x)),
  deepestAll: (s, c) => LANES.filter(l => l !== c.lane).map(l => s.units.filter(x => x.lane === l && ctl(x) !== c.p).sort((a, b) => seatKey(b, c.p) - seatKey(a, c.p))[0]).filter(Boolean),
  emptyFront: (s, c) => fxCount(3 - [0, 1, 2].filter(col => unitAt(s, c.p, c.lane, frontRow(c.p), col)).length),
});
/** Conditions added: bloodied (the other unit), side / mid column, deaths this round, marked, offered, moved, hurt (me). */
function fxIfMore(s, c, w) {
  if (w.itHurt && !(c.t && isBloodied(c.t))) return false;
  if (w.itHas && !(c.t && kw(c.t, w.itHas))) return false;
  if (w.itNot && c.t && kw(c.t, w.itNot)) return false;
  if (w.hurt && !(c.u && isBloodied(c.u))) return false;
  if (w.side && !(c.u && colsOf(c.u).some(k => k !== 1))) return false;
  if (w.mid && !(c.u && colsOf(c.u).includes(1))) return false;
  if (w.deaths && deathsThisRound(s) < w.deaths) return false;
  if (w.itMarked && !(c.t && kw(c.t, 'marked'))) return false;
  if (w.offered && !c.offered) return false;
  if (w.still && c.u && (c.u.mv || 0) > 0) return false;
  if (w.attacks && attacksThisRound(s, c.p) < w.attacks) return false;
  if (w.hand && s.players[c.p].hand.length < w.hand) return false;
  return true;
}
/** Augur N: your spells deal N more damage for each unit of yours with it (in any lane). */
const fxAugur = (s, c) => (c.spell ? s.units.filter(x => ctl(x) === c.p).reduce((n, x) => n + (kw(x, 'augur') || 0), 0) : 0);
/** After u's attack is paid: the attack counter, then Onrush and other allyAttack triggers in its lane. */
function fxAttacked(s, p, u) {
  s.aR = s.aR || [null, null];
  s.aR[p] = s.aR[p] && s.aR[p].r === s.round ? { r: s.round, n: s.aR[p].n + 1 } : { r: s.round, n: 1 };
  for (const w of fxWatchers(s, p, u.lane, u.id)) if (byId(s, w.id)) fxFire(s, 'allyAttack', w, { ev: u });
}
/** Wind: units' round-end effects happen now; a wound Geared unit winds the Geared allies touching it (each once). */
function fxTick(s, list, label) {
  const done = new Set(), queue = list.slice();
  while (queue.length) {
    const t = queue.shift();
    if (!t || done.has(t.id) || !byId(s, t.id)) continue;
    done.add(t.id);
    log(s, `${unitName(t)} is wound (${label}).`);
    emit(s, { grow: [t.id] });
    fxFire(s, 'roundEnd', t, { again: true });
    fxFire(s, 'wound', t);
    processDeaths(s);
    if (byId(s, t.id) && kw(t, 'geared')) for (const g of fxCamp(s, t.owner, t.lane)) if (!done.has(g.id) && ctl(g) === ctl(t) && kw(g, 'geared') && touches(t, g)) queue.push(g);
  }
}
Object.assign(FX_OPS, {
  tick(s, c, o) { fxTick(s, fxSel(s, c, o.to), c.label); },
  ready(s, c, o) { for (const t of fxSel(s, c, o.to)) { Object.assign(t, { attacked: false, atk: 0, moved: false, mv: 0 }); log(s, `${unitName(t)} may act again this round (${c.label}).`); } },
  advance(s, c, o) { for (const t of fxSel(s, c, o.to || 'self')) if (!kw(t, 'fixed') && slide(s, t, fwd(t.owner))) { log(s, `${unitName(t)} advances.`); fxFire(s, 'move', t); } },
  offer(s, c, o) {
    const v = fxNextInCol(s, c.u, -1);
    if (!v) return;
    c.offered = true;
    kill(s, v, `offered by ${c.label}`);
    processDeaths(s);
  },
  raise(s, c, o) {
    const P = s.players[c.p], ks = P.discard.map((k, i) => [k, i]).filter(([k]) => CARDS[k] && !CARDS[k].tactic && !CARDS[k].token && (!o.max || CARDS[k].sup <= o.max));
    ks.sort((a, b) => (o.raise === 'best' ? CARDS[b[0]].sup - CARDS[a[0]].sup : b[1] - a[1]));
    for (const [k, i] of ks) {
      const spot = fxSpot(s, c.p, c.lane, k, o.at);
      if (!spot) continue;
      P.discard.splice(i, 1);
      spawn(s, c.p, k, c.lane, spot.r, spot.c, spot.o, `${CARDS[k].name} comes back from the discard pile (${c.label}).`);
      return;
    }
  },
  kill(s, c, o) { let ts = fxSel(s, c, o.to); if (o.first) ts = ts.sort((a, b) => defenceOf(a) - defenceOf(b) || byReadingOrder(a, b)).slice(0, 1); for (const t of ts) kill(s, t, c.label); },
  itStrike(s, c, o) { const u = fxAlive(s, c.t); if (!u) return; for (let i = 0; i < (o.itStrike || 1); i++) { const t = byId(s, u.id) && strikeTarget(s, u); if (t) strike(s, u, t, `${unitName(u)} (${c.label})`); } },
  omen(s, c, o) { for (const t of fxSel(s, c, o.to || 'it')) fxFire(s, 'targeted', t, { k: c.k }); },
  sup(s, c, o) { for (const t of fxSel(s, c, o.to)) { t.sup = Math.max(1, unitSupply(t) + o.sup); log(s, `${unitName(t)}: supply ${unitSupply(t)} (${c.label}).`); } },
});

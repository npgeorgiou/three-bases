/* ---------- movement and deployment ---------- */
/** A unit reached new cells of its front row: enemy Akritai facing those columns hit it. */
function arrive(s, u, before) {
  if (!byId(s, u.id)) return;
  const fresh = [...frontCols(u)].filter(c => !before.has(c));
  if (!fresh.length) return;
  for (const a of unitsIn(s, other(ctl(u)), u.lane).filter(a => a.owner !== u.owner).sort(byReadingOrder)) {
    const k = cardOf(a).spearwall;
    if (!k || !byId(s, u.id) || !byId(s, a.id)) continue;
    if (colsOf(a).some(c => fresh.includes(c))) dealDamage(s, abilityHit(a, k), u, unitName(a) + ' (spear wall)', a);
  }
}

/** Tourmarches: an ally that moves in its lane gains +1|+1 until round end. */
function moved(s, u) {
  for (const t of s.units) if (cardOf(t).tourm && targetsOf(s, t, 'tourm').includes(u)) {
    u.ts = (u.ts || 0) + 1; u.td = (u.td || 0) + 1;
    log(s, `${unitName(t)} rewards the manoeuvre: ${unitName(u)} +1|+1 until round end.`);
  }
  applyAuras(s);
}

/** Slide a unit straight along its column by `step` rows, as far as the cells are free (at most `max`). Returns rows moved. */
function slide(s, u, step, max = ROWS) {
  if (kw(u, 'fixed')) return 0;
  const offs = offsetsOf(u, u.o);
  let row = u.r, n = 0;
  for (let r = u.r + step; n < max && fitsCells(s, u.owner, u.lane, offs, r, u.c, u.id); r += step) { row = r; n++; }
  if (!n) return 0;
  const before = frontCols(u);
  moved(s, u);   // gains for moving (Tourmarches) come as it sets off
  emit(s, { move: u.id, path: [[u.r, u.c], [row, u.c]], o: u.o, steps: n, charge: s.chargeFx || undefined });
  u.r = row;
  arrive(s, u, before);
  return n;
}

/** Where a unit can move in its camp (keyed "r,c"), in orientation o. Costs its supply; `free` = no cost and no move used. */
function moveTargets(s, u, o = u.o, free = false, lane = u.lane) {
  const out = {};
  if (kw(u, 'fixed')) return out;
  if (lane !== u.lane && (free || !cardOf(u).outrider)) return out;   // Outrider: its move may go to another lane's camp
  if (!free && ((u.mv || 0) >= maxMoves(u) || !canPay(s, u.lane, moveCost(u)))) return out;
  const offs = offsetsOf(u, o), same = lane === u.lane;
  for (let r = 0; r < ROWS; r++)
    for (let c = 0; c < COLS; c++) {
      if (same && r === u.r && c === u.c && o === u.o) continue;   // where it stands now
      if (fitsCells(s, u.owner, lane, offs, r, c, same ? u.id : undefined)) out[r + ',' + c] = { r, c, lane, d: free ? 0 : moveCost(u), path: [[u.r, u.c], [r, c]] };
    }
  return out;
}

/** Spots of p's camp in `lane` where unit u (of either side) would fit. */
function spotsFor(s, p, lane, u) {
  const out = [];
  for (const o of orientationsOf(u)) for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++)
    if (fitsCells(s, p, lane, offsetsOf(u, o), r, c, u.owner === p ? u.id : undefined)) out.push({ r, c, o });
  return out;
}

/** Units of p that card k would cover at (r, c, o) in `lane` (cards placed onto units, e.g. Corpse Gnawer). */
function coveredUnits(s, p, lane, k, r, c, o) {
  const cells = regionAt(CARDS[k].size, r, c, o), map = occupancy(s, p, lane), out = [];
  for (const [x, y] of cells || []) { const u = map[x + ',' + y]; if (u && !out.includes(u)) out.push(u); }
  return out;
}
/** Whether card k can be placed at (r, c, o): on free cells, or for a card placed onto units, covering at least one unit it may cover and nothing else. */
function deployFits(s, p, lane, k, r, c, o) {
  const card = CARDS[k];
  if (!card.onto && !card.sacrifice) return fits(s, p, lane, card.size, r, c, o);
  if (!regionAt(card.size, r, c, o)) return false;
  const under = coveredUnits(s, p, lane, k, r, c, o);
  return under.length > 0 && under.every(u => ctl(u) === p && (card.sacrifice || card.onto.includes(u.card)));
}
function canDeploy(s, p, handIndex, lane, r, c, o) {
  const k = s.players[p].hand[handIndex];
  if (!k || CARDS[k].tactic || s.pending || !needsMet(s, p, k)) return false;
  return deployFits(s, p, lane, k, r, c, o) && canPay(s, lane, CARDS[k].cost);
}

/** Restore up to n lost shields of unit u (n = Infinity: all of them). */
function restoreShields(s, u, n, source) {
  const restored = Math.min(n, Math.max(0, u.dmg || 0));
  if (!restored) return;
  u.dmg -= restored;
  log(s, `${source} restores ${restored} shield${restored > 1 ? 's' : ''} of ${unitName(u)}.`);
  emit(s, { heal: u.id, n: restored });
}

/**
 * Place: unit u has just entered side p's camp (played from the hand, or defected). Its Place effects fire in order:
 * Voukinator and Warhorn bonuses from allies already in the lane, its own Place counts (Crowd Pleaser, Komes),
 * enemy Akritai facing it, Charge, and finally any Place choice (Mandator, Monomachos, Presbeutes, Cinder Imp).
 */
/** own: an extra effect of the unit itself that fires with its Place effects (a Revenant's "when it returns"). */
function placeUnit(s, p, u, line, own) {
  if (u.rising) { delete u.rising; risen(s, p, u); }   // gains are instant: Tomb Warden before anything else happens to it
  const card = cardOf(u), already = s.units.filter(x => x.lane === u.lane && x.id !== u.id), mine = already.filter(x => ctl(x) === p);
  const heralds = mine.filter(x => cardOf(x).herald).length;
  u.ps = (u.ps || 0) + heralds;
  if (mine.some(x => cardOf(x).warhorn)) { u.reck = true; u.chg = true; }
  if (card.onPlace === 'crowd') u.ps += already.length;
  if (card.onPlace === 'komes') for (const x of targetsOf(s, u, 'place:komes')) x.pd = (x.pd || 0) + 1;
  applyAuras(s);
  log(s, line);
  if (heralds) log(s, `The trumpets sound: ${unitName(u)} +${heralds} strength.`);
  if (card.onPlace === 'komes' && mine.length) log(s, `${unitName(u)} rallies the lane: +1 defence.`);
  if (card.onPlace === 'crowd' && already.length) log(s, `The crowd roars: ${unitName(u)} +${already.length} strength.`);
  emit(s, { place: u.id });
  const startCols = [...frontCols(u)];
  if ((card.charge || u.chg) && !inFront(u)) {   // placed in the front row it has no run-up: no charge
    s.chargeFx = true;
    slide(s, u, fwd(u.owner));
    s.chargeFx = false;
    processDeaths(s);
    if (byId(s, u.id)) {
      log(s, unitName(u) + ' charges.');
      const targets = targetsOf(s, u, 'charge');
      const str = strengthOf(u);   // fixed for all of the charge's hits
      if (targets.length) {
        // a 0-strength charge still counts as a hit for the charger (Reckless fires), but does nothing to the target
        if (str > 0) {
          s.fxHow = 'charge';
          try { strikeAll(s, u, targets, unitName(u) + ' (charge)', str); } finally { s.fxHow = undefined; }
        } else log(s, `${unitName(u)} hits ${targets.map(x => unitName(x)).join(' and ')} for 0.`);
        processDeaths(s);
        if (isReckless(u) && byId(s, u.id)) kill(s, u, 'reckless');
      } else log(s, unitName(u) + (inFront(u) ? ' finds no one ahead to hit.' : ' is stopped short of the front row and hits no one.'));
    }
  }
  processDeaths(s);
  if (byId(s, u.id)) { exPlace(s, p, u); processDeaths(s); }
  if (byId(s, u.id)) { startOnPlace(s, p, u); processDeaths(s); }
  if (own && byId(s, u.id)) { own(); processDeaths(s); }
  // enemy Akritai react only once its Place effects are done (after a Place choice, once it is made)
  if (!byId(s, u.id) || !startCols.length) return;
  if (s.pending) s.arrQ = [...(s.arrQ || []), { id: u.id, cols: startCols }];
  else arriveInto(s, u, startCols);
}
/** Enemy Akritai react to u's arrival in the front-row columns `cols` it was placed into (those it still stands in). */
function arriveInto(s, u, cols) {
  if (byId(s, u.id)) arrive(s, u, new Set([...frontCols(u)].filter(c => !cols.includes(c))));
}


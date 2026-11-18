/* ---------- combat ---------- */
/** Remove a unit; its card goes to its owner's discard pile. opt.silent: the hit animation already shows the death. */
function kill(s, u, why, opt = {}) {
  if (!byId(s, u.id)) return;
  if (!opt.silent) emit(s, { dead: u.id });
  if (s.noFx) s.deadUnits = [...(s.deadUnits || []), { ...u }];   // previews: where a unit died
  s.units = s.units.filter(x => x.id !== u.id);
  s.players[u.owner].discard.push(u.card);
  log(s, `${unitName(u)} (${deckName(s, u.owner)}) dies${why ? ' — ' + why : ''}.`);
}

/** Hit a unit with `str`: it loses that many shields and dies when none are left. Returns {killed, t} or null if nothing was hit. */
function hitUnit(s, str, target, source, sourceId) {
  if (!target || !byId(s, target.id) || str <= 0) return null;
  const def = defenceOf(target), dies = str >= def;
  emit(s, { hit: true, src: sourceId || null, t: target.id, str, broke: Math.min(str, def), kill: dies });
  if (dies) { kill(s, target, 'hit by ' + source, { silent: true }); return { killed: true, t: target }; }
  target.dmg = (target.dmg || 0) + str;
  log(s, `${source} hits ${unitName(target)}: ${str} shield${str > 1 ? 's' : ''} lost.`);
  return { killed: false, t: target };
}

/**
 * Reach (AGREED, October 2026). A lane's two camps form one column of 6 rows (top camp rows 0-2, bottom camp rows 3-5),
 * so the two front rows touch across the base. A melee unit reaches every cell adjacent to one of its cells (diagonals
 * included); Pike also reaches the opposite camp's front-row cells two rows ahead of it (column ±1). Ranged units reach
 * every cell of their lane. A strike (an attack with the unit's strength) only hits enemies in reach.
 */
const laneRow = (owner, r) => (owner === 1 ? r : ROWS + r);
function reachesCell(u, owner, r, c) {
  if (kw(u, 'ranged')) return true;
  const f = u.owner === 0 ? -1 : 1;   // toward the other camp, in lane rows
  const R = laneRow(owner, r), pikeRow = laneRow(other(u.owner), frontRow(other(u.owner)));
  return cellsOf(u).some(([ur, uc]) => {
    const G = laneRow(u.owner, ur);
    if (Math.abs(c - uc) > 1) return false;
    if ((G !== R || uc !== c || owner !== u.owner) && Math.abs(G - R) <= 1) return true;
    return kw(u, 'reach') && R === G + 2 * f && R === pikeRow;
  });
}
/** Whether u could strike t now by position: t is in its lane and one of t's cells is in u's reach. */
const reaches = (u, t) => !!t && t.lane === u.lane && t.id !== u.id && cellsOf(t).some(([r, c]) => reachesCell(u, t.owner, r, c));
/** Page order of the board as side p sees it (the resolution order): top to bottom, left to right on p's screen. */
/** The enemies u could strike, in resolution order. */
/** Unit u strikes t with its strength (an attack). */
const strike = (s, u, t, label) => hitUnit(s, strengthOf(u), t, label, u.id);

function canAttack(s, a, t) {
  if (!a || !t || a.id === t.id || a.attacked || a.owner !== s.cur || a.lane !== t.lane || a.owner === t.owner) return false;
  if (strengthOf(a) <= 0 || !canPay(s, a.lane, attackCost(a))) return false;
  return reaches(a, t);
}

function updateBases(s) {
  for (const lane of LANES) {
    const o = laneOwner(s, lane);
    if (o === s.owner[lane]) continue;
    log(s, o !== null ? `${deckName(s, o)} takes base ${lane + 1}.` : `${deckName(s, s.owner[lane])} loses base ${lane + 1}.`);
    s.owner[lane] = o;
    if (o !== null) emit(s, { capture: lane, p: o });
  }
}


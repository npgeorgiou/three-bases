/* The checks run by tools/fxtest.js (inside the game engine; returns the report). */
const out = []; let fails = 0;
const ok = (name, cond, got) => { out.push((cond ? 'ok   ' : 'FAIL ') + name + (cond ? '' : ' (got ' + got + ')')); if (!cond) fails++; };
function fresh() { DECKS.x = { name: 'x', fac: 'c', list: [['c_key', 30]] }; const s = newGame('x', 'x'); s.redrawDone = true; s.units = []; s.players.forEach(P => { P.hand = []; P.reserve = 5; }); s.pool = [[9, 9, 9], [9, 9, 9]]; return s; }
const put = (s, p, k, lane, r, c) => spawn(s, p, k, lane, r, c, 'h');
const fr = p => frontRow(p), bk = p => backRow(p);
{ const s = fresh(), p = s.cur, q = 1 - p; const a = put(s, p, 'c_cogsoldier', 0, fr(p), 0); put(s, p, 'c_cogsoldier', 0, fr(p), 1);
  const e = put(s, q, 'c_ticker', 0, fr(q), 0), e2 = put(s, q, 'b_spearman', 0, fr(q), 1); e.pd = 10; e2.pd = 10;
  fxTick(s, [a], 'test'); ok('Geared: winding one wound the touching one too', (e.dmg || 0) + (e2.dmg || 0) === 4, (e.dmg || 0) + (e2.dmg || 0)); }
{ const s = fresh(), p = s.cur, q = 1 - p; const v = put(s, p, 'd_victim', 0, fr(p) - fwd(p), 1); const e = put(s, q, 'b_spearman', 0, fr(q), 1); e.pd = 10;
  put(s, p, 'd_altarpriest', 0, fr(p), 1); ok('Offering: the ally behind dies and the offering effect happens', !byId(s, v.id) && e.dmg === 4, e.dmg); }
{ const s = fresh(), p = s.cur, q = 1 - p; const a = put(s, p, 'a_runner', 0, fr(p), 0), b = put(s, p, 'a_hornwarrior', 0, fr(p), 2); const e = put(s, q, 'b_spearman', 0, fr(q), 1); e.pd = 10;
  s.cur = p; applyAction(s, { t: 'attack', id: b.id, tid: e.id }); ok('Onrush: +1 strength when another ally attacks', strengthOf(a) === 2, strengthOf(a)); ok('Flanker: +2 strength in a side column of the front row', strengthOf(b) === printedStr(b) + 2, strengthOf(b)); }
{ const s = fresh(), p = s.cur, q = 1 - p; const k = put(s, p, 'b_thornknight', 0, fr(p), 1); const e = put(s, q, 'a_runner', 0, fr(q), 1); e.pd = 10; s.cur = q;
  applyAction(s, { t: 'attack', id: e.id, tid: k.id }); ok('Retaliate 2: the attacker takes 2', e.dmg === 2, e.dmg); }
{ const s = fresh(), p = s.cur; const u = put(s, p, 's_bullcalf', 0, fr(p), 1); s.players[p].hand = ['s_blessing']; s.cur = p;
  applyAction(s, listActions(s).find(a => a.t === 'tactic' && a.vid === u.id)); ok('Omen: fulfilled when a spell targets it', strengthOf(u) === 2 && defenceOf(u) === 6, strengthOf(u) + '|' + defenceOf(u)); }
{ const s = fresh(), p = s.cur; const u = put(s, p, 'o_youngoak', 0, fr(p), 1); fxFire(s, 'roundEnd', u); ok('Perennial 1: +1|+1 at round end', strengthOf(u) === printedStr(u) + 1 && defenceOf(u) === printedDef(u) + 1, strengthOf(u) + '|' + defenceOf(u)); }
{ const s = fresh(), p = s.cur, q = 1 - p; const u = put(s, p, 'l_private', 0, fr(p), 1); put(s, p, 'l_sandbag', 0, fr(p) - fwd(p), 1); applyAuras(s); ok('Entrenched: Armoured with an ally behind', isArmoured(u), isArmoured(u));
  const e = put(s, q, 'b_spearman', 0, fr(q), 1); e.pd = 10; giveKw(e, 'marked'); const g = put(s, p, 'l_lewis', 0, bk(p), 0); s.cur = p;
  applyAction(s, { t: 'attack', id: g.id, tid: e.id }); ok('Marked: strikes deal double damage', e.dmg === 2, e.dmg); }
{ const s = fresh(), p = s.cur; const u = put(s, p, 'd_drummer', 0, fr(p), 1); const v = put(s, p, 'd_victim', 0, fr(p), 0); kill(s, v, 't'); processDeaths(s); applyAuras(s); ok('Toll: +1 strength per death this round', strengthOf(u) === 1, strengthOf(u)); }
{ const s = fresh(), p = s.cur, q = 1 - p; const g = put(s, p, 'l_battery', 0, bk(p), 1); const f = put(s, q, 'b_spearman', 0, fr(q), 1), b = put(s, q, 'b_spearman', 0, bk(q), 2); f.pd = 9; b.pd = 9;
  fxFire(s, 'roundEnd', g); ok('Barrage: hits the enemy furthest from the base', !f.dmg && b.dmg === 2, (f.dmg || 0) + '/' + b.dmg); }
{ const s = fresh(), p = s.cur; const a = put(s, p, 'a_runner', 0, fr(p), 1), r = put(s, p, 'a_loinwarrior', 0, bk(p), 1); kill(s, a, 't'); processDeaths(s); ok('Reserve: moves forward when an ally dies', r.r === fr(p), r.r); }
{ const s = fresh(), p = s.cur, q = 1 - p; const a = put(s, p, 'c_cogsoldier', 0, fr(p), 1); const e = put(s, q, 'b_spearman', 0, fr(q), 1); e.pd = 10;
  fxCast(s, p, { lane: 0 }, 0, 'c_overwind'); ok('A selector written as the op\'s value is its target (Overwind winds the lane)', e.dmg === 2, e.dmg); }
{ const s = fresh(), p = s.cur, q = 1 - p; const e = put(s, q, 'b_spearman', 0, bk(q), 1); const u = put(s, p, 'o_ivy', 0, fr(p), 1);
  ok('Climbing Ivy pulls the enemy facing it, not itself', e.r === fr(q) && u.r === fr(p), e.r + '/' + u.r); }
{ const s = fresh(), p = s.cur; const a = put(s, p, 'a_runner', 0, bk(p), 1); s.players[p].hand = ['a_advance']; s.cur = p;
  applyAction(s, listActions(s).find(x => x.t === 'tactic')); ok('Close the Gap moves the back units forward', a.r === fr(p), a.r); }
return out.join('\n') + '\n' + (fails ? fails + ' failed' : 'all passed');

/* ---------- results ---------- */

function renderProgress(finished) {
  const total = state.plan ? state.plan.jobs.length : 0;
  const done = state.plan ? state.plan.jobs.filter(j => state.results.some(r => r.key === j.key)).length : 0;
  $('#barFill').style.width = total ? (100 * done / total) + '%' : finished ? '100%' : '0%';
  const failed = tour.failed ? ` · ${tour.failed} crashed (last error: ${tour.lastError})` : '';
  $('#status').textContent = (finished ? 'Finished.' : !total ? 'Not started.' : `${done} of ${total} games, ${tour.running ? 'playing' : 'paused'}`) + failed;
}

function tally() {
  const pairs = new Map(), people = new Map();
  const person = id => people.get(id) || people.set(id, { id, games: 0, wins: 0, losses: 0, draws: 0, none: 0, ms: 0, msN: 0 }).get(id);
  for (const r of state.results) {
    if (!playerById(r.a) || !playerById(r.b)) continue;
    const k = r.a + '|' + r.b, p = pairs.get(k) || pairs.set(k, { a: r.a, b: r.b, aw: 0, bw: 0, d: 0, lost: 0, none: 0 }).get(k);
    const A = person(r.a), B = person(r.b);
    A.games++; B.games++;
    if (!r.failed) { A.ms += r.ms.a; A.msN++; B.ms += r.ms.b; B.msN++; }
    if (r.winner === 'a') { p.aw++; A.wins++; B.losses++; }
    else if (r.winner === 'b') { p.bw++; B.wins++; A.losses++; }
    else if (r.winner === 'draw') { p.d++; A.draws++; B.draws++; }
    else if (r.winner === 'lost') { p.lost++; A.losses++; B.losses++; }
    else { p.none++; A.none++; B.none++; }
  }
  return { pairs: [...pairs.values()], people: [...people.values()] };
}
function sideTally() {
  const rec = () => ({ w: 0, l: 0 }), per = new Map(), overall = { first: 0, second: 0, ...Object.fromEntries(LAB_FACTIONS.map(f => [f, 0])) };
  const of = id => per.get(id) || per.set(id, { id, first: rec(), second: rec(), ...Object.fromEntries(LAB_FACTIONS.map(f => [f, rec()])) }).get(id);
  for (const r of state.results) {
    if ((r.winner !== 'a' && r.winner !== 'b') || !playerById(r.a) || !playerById(r.b)) continue;
    if (!LAB_FACTIONS.includes(r.aFaction) || !LAB_FACTIONS.includes(r.bFaction)) continue;   // played with cards the lab no longer has
    const sides = [{ id: r.a, faction: r.aFaction, first: r.aFirst, won: r.winner === 'a' }, { id: r.b, faction: r.bFaction, first: !r.aFirst, won: r.winner === 'b' }];
    for (const x of sides) { const p = of(x.id), k = x.won ? 'w' : 'l'; p[x.faction][k]++; p[x.first ? 'first' : 'second'][k]++; }
    const w = sides.find(x => x.won);
    if (r.aFaction !== r.bFaction) overall[w.faction]++;
    overall[w.first ? 'first' : 'second']++;
  }
  return { per: [...per.values()], overall };
}
const pct = (w, n) => (n ? Math.round(100 * w / n) + '%' : '–');
const wl = x => `${x.w}-${x.l} (${pct(x.w, x.w + x.l)})`;
function verdict(x, y) {
  const z = x + y === 0 ? 0 : (x - y) / Math.sqrt(x + y);
  return z >= 2 ? 2 : z >= 1 ? 1 : z <= -2 ? -2 : z <= -1 ? -1 : 0;
}
function verdictText(p) {
  const v = verdict(p.aw, p.bw);
  return v === 0 ? 'Not clear yet' : `${nameOf(v > 0 ? p.a : p.b)} is ${Math.abs(v) === 2 ? 'clearly' : 'probably'} better`;
}
function renderResults() {
  const { pairs, people } = tally(), sides = sideTally(), o = sides.overall;
  people.sort((x, y) => y.wins / Math.max(1, y.wins + y.losses) - x.wins / Math.max(1, x.wins + x.losses));
  $('#standings').innerHTML = `<tr><th>Player</th><th class="num">Games</th><th class="num">Won</th><th class="num">Lost</th><th class="num">Draw</th><th class="num">Unfinished</th><th class="num">Win rate</th><th class="num">Time per move</th></tr>`
    + (people.map(p => `<tr><td>${esc(nameOf(p.id))}</td><td class="num">${p.games}</td><td class="num">${p.wins}</td><td class="num">${p.losses}</td><td class="num">${p.draws}</td><td class="num">${p.none}</td><td class="num">${pct(p.wins, p.wins + p.losses)}</td><td class="num">${Math.round(p.ms / Math.max(1, p.msN))} ms</td></tr>`).join('') || '<tr><td>No games yet.</td></tr>');
  $('#pairs').innerHTML = `<tr><th>Player</th><th>Opponent</th><th class="num">Won</th><th class="num">Lost</th><th class="num">Draw</th><th class="num">Both lost</th><th class="num">Unfinished</th><th>Verdict</th></tr>`
    + (pairs.map(p => `<tr><td>${esc(nameOf(p.a))}</td><td>${esc(nameOf(p.b))}</td><td class="num">${p.aw}</td><td class="num">${p.bw}</td><td class="num">${p.d}</td><td class="num">${p.lost}</td><td class="num">${p.none}</td><td class="${verdict(p.aw, p.bw) ? 'better' : 'unclear'}">${esc(verdictText(p))}</td></tr>`).join('') || '<tr><td>No games yet.</td></tr>');
  $('#overall').textContent = `Games between different factions, won by: ${LAB_FACTIONS.map(f => `${LAB_FACTION_NAME[f]} ${o[f]}`).join(', ')}. All games: the first player won ${o.first}, the second player ${o.second}.`;
  $('#sides').innerHTML = `<tr><th>Player</th>${LAB_FACTIONS.map(f => `<th class="num">As ${esc(LAB_FACTION_NAME[f])}</th>`).join('')}<th class="num">Moving first</th><th class="num">Moving second</th></tr>`
    + (sides.per.map(p => `<tr><td>${esc(nameOf(p.id))}</td>${LAB_FACTIONS.map(f => `<td class="num">${wl(p[f])}</td>`).join('')}<td class="num">${wl(p.first)}</td><td class="num">${wl(p.second)}</td></tr>`).join('') || '<tr><td>No games yet.</td></tr>');
  $('#export').value = exportText(pairs, people, sides);
}
function exportText(pairs, people, sides) {
  const lines = ['Three Bases AI tournament results', '', 'Standings (won-lost-draw-unfinished, win rate, ms per move):'];
  for (const p of people) lines.push(`  ${nameOf(p.id)}: ${p.wins}-${p.losses}-${p.draws}-${p.none}, ${pct(p.wins, p.wins + p.losses)}, ${Math.round(p.ms / Math.max(1, p.msN))} ms`);
  lines.push('', 'Head to head (by matchup: X = different factions, S = same faction):');
  for (const p of pairs) {
    const by = Object.keys(MATCHUPS).map(m => {
      const rs = state.results.filter(r => r.a === p.a && r.b === p.b && r.m === m);
      return rs.length ? `${m} ${rs.filter(r => r.winner === 'a').length}-${rs.filter(r => r.winner === 'b').length}` : null;
    }).filter(Boolean).join(', ');
    lines.push(`  ${nameOf(p.a)} v ${nameOf(p.b)}: ${p.aw}-${p.bw} (draws ${p.d}, both lost ${p.lost}, unfinished ${p.none}) [${by}] ${verdictText(p)}`);
  }
  const o = sides.overall;
  lines.push('', `Games between different factions, won by: ${LAB_FACTIONS.map(f => `${LAB_FACTION_NAME[f]} ${o[f]}`).join(', ')}.`, `All games: first player won ${o.first}, second player won ${o.second}.`, 'By faction and seat (won-lost):');
  for (const p of sides.per) lines.push(`  ${nameOf(p.id)}: ${LAB_FACTIONS.map(f => `as ${LAB_FACTION_NAME[f]} ${wl(p[f])}`).join(', ')}, first ${wl(p.first)}, second ${wl(p.second)}`);
  lines.push('', 'Players:');
  for (const p of people) {
    const pl = playerById(p.id);
    if (!pl) continue;
    const extra = pl.kind === 'random' ? 'random player (picks a kind of move at random, then a move of that kind)' : pl.kind === 'net' ? `learning AI, trained on ${state.training[pl.net].games} games against itself${state.training[pl.net].teacherGames ? ` and ${state.training[pl.net].teacherGames} teacher games` : ''}`
      : pl.kind === 'bench' ? 'benchmark AI (sees the opponent\'s hand)' : pl.kind === 'ifelse' ? 'ifelse AI (sees both hands) ' + JSON.stringify(ifelseFull(pl.cfg)) : 'Strategist ' + JSON.stringify(pl.cfg || {});
    lines.push(`  ${pl.name}: ${extra}`);
  }
  lines.push('', 'Strategist defaults: ' + JSON.stringify(STRATEGIST_DEFAULTS));
  return lines.join('\n');
}
$('#copy').addEventListener('click', async () => {
  try { await navigator.clipboard.writeText($('#export').value); }
  catch (e) { $('#export').select(); document.execCommand('copy'); }
  $('#copied').textContent = 'Copied.';
  setTimeout(() => { $('#copied').textContent = ''; }, 2000);
});

/* =====================================================================
   Watching a game (played here on the page, move by move)
   ===================================================================== */

const watch = { game: null, token: 0, paused: false, names: null, nets: {} };
const W_CELL = 58, W_GAP = 18, W_LANE = 3 * W_CELL, W_LEFT = 12, W_TOP = 24, W_BASE = 50;
/** Unit and base colours by faction (the game's faction fills). */
const FAC_FILL = { c: '#2E3A46', d: '#241E22', a: '#6A3E1E', b: '#6B1E24', s: '#1E2F6E', o: '#2F4A26', l: '#474A42' };
const FACTION_FILL = new Proxy({}, { get: (_, deck) => FAC_FILL[facOfDeck(deck)] || '#555' });
for (const id of ['#wAf', '#wBf']) $(id).innerHTML = LAB_DECKS.map(d => `<option value="${d}">${esc(DECKS[d].name)}</option>`).join('');
$('#wBf').selectedIndex = 1;
const wait = ms => new Promise(r => setTimeout(r, ms));

/** Watch `sides` = [{ name, spec }, { name, spec }] play, seat 0 as factions[0]. */
async function watchGame(sides, factions) {
  const token = ++watch.token;
  watch.paused = false;
  $('#wPause').textContent = 'Pause';
  for (const x of sides) if (x.spec.kind === 'net') watch.nets[x.spec.net] = netNamed('watch:' + x.spec.net, netData[x.spec.net]);
  const s = newGame(factions[0], factions[1]);
  s.noFx = true;
  sides.forEach((x, p) => {                                                   // the starting-hand redraw, as in every lab game
    if (x.spec.kind === 'net') netRedraw(s, p, watch.nets[x.spec.net]);
    else if (x.spec.kind === 'random') randomRedraw(s, p);
    else aiMulligan(s, p);
  });
  s.redrawDone = true;
  watch.game = s; watch.names = sides.map(x => x.name); watch.last = null; watch.sides = sides;
  $('#wTitle').textContent = `${sides[0].name} (${DECKS[factions[0]].name}) v ${sides[1].name} (${DECKS[factions[1]].name})`;
  $('#wLog').innerHTML = '';
  $('#watch').hidden = false;
  drawWatch(s);
  await wait(600);
  for (let i = 0; i < ACTION_CAP && s.winner === null && s.round <= ROUND_CAP; i++) {
    while (watch.paused && token === watch.token) await wait(150);
    if (token !== watch.token) return;
    const side = s.cur, spec = sides[side].spec;
    const a = spec.kind === 'bench' ? chooseIfelseAction(s, BENCH_VALUES) : spec.kind === 'ifelse' ? chooseIfelseAction(s, spec.cfg) : spec.kind === 'strategist' ? chooseStrategistAction(s, spec.full)
      : spec.kind === 'random' ? randomMove(listActions(s).map(x => ({ a: x }))).a
      : chooseNetAction(s, watch.nets[spec.net], spec.play);
    const text = describeAction(s, a, sides[side].name), round = s.round, before = new Set(s.units.map(u => u.id + ':' + u.dmg));
    applyAction(s, a);
    watch.last = { changed: new Set(s.units.filter(u => !before.has(u.id + ':' + u.dmg)).map(u => u.id)), deployed: a.t === 'deploy' ? Math.max(...s.units.map(u => u.id)) : null };
    logWatch(`R${round}. ${text}` + (s.round !== round && s.winner === null ? ` Round ${round} ends.` : ''));
    drawWatch(s);
    await wait(Number($('#wSpeed').value) * (a.t === 'pass' ? 0.6 : 1));
  }
  if (token !== watch.token) return;
  const end = s.winner === null ? 'The game is stopped: too long.' : s.winner === 'draw' ? 'Draw.' : s.winner === 'lost' ? 'Both sides lose.'
    : `${sides[s.winner].name} wins.`;
  logWatch(end + (s.endReason ? ' ' + s.endReason : ''));
  $('#wNow').textContent = end;
}

function describeAction(s, a, who) {
  const unit = id => { const u = byId(s, id); return u ? CARDS[u.card].name : 'a unit'; };
  if (a.t === 'pass') return `${who} passes.`;
  if (a.t === 'deploy') return `${who} deploys ${CARDS[s.players[s.cur].hand[a.hi]].name} in lane ${a.lane + 1}.`;
  if (a.t === 'tactic') return `${who} casts ${CARDS[s.players[s.cur].hand[a.hi]].name}${a.lane !== undefined ? ' on lane ' + (a.lane + 1) : a.vid ? ' on ' + unit(a.vid) : ''}.`;
  if (a.t === 'attack') return `${who}: ${unit(a.id)} attacks ${unit(a.tid)}.`;
  if (a.t === 'move') return `${who} moves ${unit(a.id)}.`;
  return `${who}: ${unit(a.id)} uses ${a.t}.`;
}
function logWatch(text) {
  const li = document.createElement('li');
  li.textContent = text;
  $('#wLog').prepend(li);
  $('#wNow').textContent = text;
}

/** Draw the board: seat 1's camps on top, seat 0's at the bottom, bases in between. */
function drawWatch(s) {
  const svg = $('#wBoard'), parts = [];
  const campTop = side => (side === 1 ? W_TOP : W_TOP + 3 * W_CELL + W_BASE);
  const rowY = (side, r) => campTop(side) + (side === 1 ? r : r) * W_CELL;
  for (const lane of LANES) {
    const x0 = W_LEFT + lane * (W_LANE + W_GAP);
    parts.push(`<text class="lbl" x="${x0 + W_LANE / 2}" y="${W_TOP - 8}">Lane ${lane + 1} · supply ${s.pool[1][lane]}</text>`);
    parts.push(`<text class="lbl" x="${x0 + W_LANE / 2}" y="${W_TOP + 6 * W_CELL + W_BASE + 18}">supply ${s.pool[0][lane]}</text>`);
    for (const side of [0, 1]) for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++)
      parts.push(`<rect class="cell" x="${x0 + c * W_CELL + 1}" y="${rowY(side, r) + 1}" width="${W_CELL - 2}" height="${W_CELL - 2}" rx="6"></rect>`);
    const by = W_TOP + 3 * W_CELL + 6, d = dotState(s, lane);
    const owner = s.owner[lane];                                   // a held base gets its holder's colour as a thick border
    parts.push(`<rect class="base" x="${x0}" y="${by}" width="${W_LANE}" height="${W_BASE - 12}" rx="10" ${owner !== null ? `style="stroke:${FACTION_FILL[s.players[owner].deck]};stroke-width:5"` : ''}></rect>`);
    for (let c = 0; c < COLS; c++) {
      const fill = d[c] === 0 || d[c] === 1 ? FACTION_FILL[s.players[d[c]].deck] : 'none';
      parts.push(`<circle class="dot" cx="${x0 + c * W_CELL + W_CELL / 2}" cy="${by + (W_BASE - 12) / 2}" r="10" fill="${fill}"></circle>`);
      if (d[c] === 'x') parts.push(`<text class="lbl" x="${x0 + c * W_CELL + W_CELL / 2}" y="${by + (W_BASE - 12) / 2 + 5}">×</text>`);
    }
  }
  for (const u of s.units) {
    const cells = cellsOf(u), rs = cells.map(([r]) => r), cs = cells.map(([, c]) => c);
    const x0 = W_LEFT + u.lane * (W_LANE + W_GAP) + Math.min(...cs) * W_CELL + 4, y0 = rowY(u.owner, Math.min(...rs)) + 4;
    const w = (Math.max(...cs) - Math.min(...cs) + 1) * W_CELL - 8, h = (Math.max(...rs) - Math.min(...rs) + 1) * W_CELL - 8;
    const cls = watch.last && watch.last.deployed === u.id ? 'new' : watch.last && watch.last.changed.has(u.id) ? 'hit' : '';
    parts.push(`<g class="unit ${cls}"><rect x="${x0}" y="${y0}" width="${w}" height="${h}" rx="7" fill="${FACTION_FILL[s.players[u.owner].deck]}"></rect>
      <text x="${x0 + w / 2}" y="${y0 + h / 2 - 3}">${esc(CARDS[u.card].name.split(' ')[0].slice(0, 9))}</text>
      <text class="stats" x="${x0 + w / 2}" y="${y0 + h / 2 + 13}">${strengthOf(u)} / ${defenceOf(u)}${u.dmg ? ' −' + u.dmg : ''}</text></g>`);
  }
  svg.innerHTML = parts.join('');
  const info = side => {
    const P = s.players[side];
    return `<b>${esc(watch.names[side])}</b> <span class="t">${esc(DECKS[P.deck].name)}${s.cur === side && s.winner === null ? ' · to act' : ''}${s.passed === side ? ' · passed' : ''}</span><br>
      <span class="t">Carry-over ${P.reserve} · hand ${P.hand.length} · deck ${P.draw.length} · bases ${basesHeld(s, side)}</span>`;
  };
  $('#wTop').innerHTML = info(1);
  $('#wBottom').innerHTML = info(0);
}

$('#wPause').addEventListener('click', () => { watch.paused = !watch.paused; $('#wPause').textContent = watch.paused ? 'Resume' : 'Pause'; });
$('#wNext').addEventListener('click', () => {                       // same two players, a fresh game (decks drawn again)
  if (!watch.sides) return;
  watchGame(watch.sides, randomDecks());
});
$('#wClose').addEventListener('click', () => { watch.token++; watch.sides = null; $('#watch').hidden = true; });
$('#wGo').addEventListener('click', () => {
  const a = $('#wA').value, b = $('#wB').value;
  watchGame([{ name: nameOf(a), spec: specOf(a) }, { name: nameOf(b) + (a === b ? ' (twin)' : ''), spec: specOf(b) }], [$('#wAf').value, $('#wBf').value]);
});


/* ---------- Decks tab: running the games, card tests, the premade yardstick, the page ---------- */
const dsPilots = st => st.pilots.filter(id => id && playerById(id));
/** The next game: card tests and premade measures first, then the search. Pilot k plays both sides (decks, not AIs, are compared). */
function dsJob() {
  const st = dsState(), pilots = dsPilots(st);
  if (!pilots.length) return null;
  for (const list of [st.extra || [], st.tasks]) for (const t of list) {
    if (t.started >= st.per) continue;
    const g = t.started++, spec = specOf(pilots[Math.floor(g / 2) % pilots.length]), decks = g % 2 ? [t.b, t.a] : [t.a, t.b];
    const lists = {};
    for (const id of decks) if (st.decks[id]) lists[id] = { name: st.decks[id].name, fac: st.decks[id].fac, list: st.decks[id].list };
    return { key: `ds-${t.a}-${t.b}-${g}-${st.tries}`, t, aSeat: g % 2, specs: [spec, spec], decks, lists, seed: t.seed + Math.floor(g / 2) };
  }
  return null;
}
function dsResult(res, job) {
  const st = dsState(), t = job.t;
  const r = res.winner === job.aSeat ? 1 : res.winner === 'draw' ? 0.5 : res.winner === 1 - job.aSeat ? 0 : null;
  if (r !== null) {
    const fresh = st.cand && st.cand.replay && (t.tag === 'replay' ? st.cand.replay : t.tag === 'fresh' ? st.cand.fresh : null);
    if (fresh) fresh[r === 1 ? 0 : r === 0 ? 1 : 2]++;                  // kept apart: only these games decide
    else addResult(st, t.a, t.b, r);
  }
  recordCards(st, job, res);
  t.done++;
  if ((st.extra || []).length && st.extra.every(x => x.done >= st.per)) finishExtra(st);
  if (st.tasks.length && st.tasks.every(x => x.done >= st.per)) {
    st.tasks = [];
    stepDone(st);
    if (st.phase === 'done') stopDs();
  }
  if (++ds.unsaved >= 20) { ds.unsaved = 0; save(); }
  renderDs();
}
function startDs() {
  if (manual) { reportError('Stop the network test first: only one thing runs at a time.'); return; }
  const st = dsState();
  st.pilots = [$('#dsP1').value, $('#dsP2').value].filter(Boolean);
  st.per = Math.max(2, Math.round(Number($('#dsPer').value) / 2) * 2 || 10);
  if (!dsPilots(st).length) { reportError('Pick at least one AI to play the decks.'); return; }
  if (Object.keys(trainings).length) stopAllTraining();
  if (tour.running) pauseTournament();
  if (tune.running) pauseTune();
  if (!st.phase) startPool(st);
  for (const d of Object.values(st.decks)) labDeck(d.id, d.name, d.fac, d.list);
  for (const list of [st.extra || [], st.tasks]) for (const t of list) t.started = t.done;   // games cut off by a pause are played again
  ds.unsaved = 0;
  ds.pool = new Pool(Math.max(1, Math.min(32, Number($('#dsThreads').value) || 1)), Object.fromEntries(NETS.map(n => [n.id, playable(netData[n.id])])), dsJob, dsResult,
    (job, msg) => { if (job) job.t.started--; reportError('A deck game failed: ' + msg); });
  save(); renderDs();
}
function stopDs() { if (ds.pool) ds.pool.stop(); ds.pool = null; save(); renderDs(); }

/* ---------- card tests (with and without) and the premade yardstick ---------- */
/** The card is measured in up to 3 pool decks holding it: each deck once more with the card's copies replaced by the plain unit of its cost. */
function testCard(k) {
  const st = dsState();
  if (!st.phase) { reportError('Start the deck search first: card tests play against its pool.'); return; }
  const holders = poolIds(st).filter(id => deckOf(st, id).list.some(([x]) => x === k)).slice(0, 3);
  if (!holders.length) { reportError(`No pool deck holds ${CARDS[k].name} now.`); return; }
  st.extra = st.extra || [];
  const pairs = [];
  for (const id of holders) {
    const d = deckOf(st, id), plain = plainFor(k), list = [];
    for (const [x, n] of d.list) { const y = x === k ? plain : x, e = list.find(z => z[0] === y); if (e) e[1] += n; else list.push([y, n]); }
    const v = addDeck(st, { id: `t-${k}-${id}`, name: `${d.name} without ${CARDS[k].name}`, fac: d.fac, list, test: true, fails: 0, tried: [] });
    for (const b of poolIds(st)) if (b !== id) st.extra.push(task(v.id, b, 'test'));
    pairs.push([id, v.id]);
  }
  st.tests[k] = { pairs, result: null };
  save(); renderDs();
  if (ds.pool) ds.pool.feed();
}
function measurePremades() {
  const st = dsState();
  if (!st.phase) { reportError('Start the deck search first: the premades are measured against its pool.'); return; }
  st.extra = st.extra || [];
  st.yard = {};
  for (const p of LAB_DECKS) {
    const y = addDeck(st, { id: 'y-' + p, name: DECKS[p].name + ' (premade)', fac: DECKS[p].fac, list: DECKS[p].list, test: true, fails: 0, tried: [] });
    for (const b of poolIds(st)) st.extra.push(task(y.id, b, 'yard'));
    st.yard[p] = { id: y.id, done: false };
  }
  save(); renderDs();
  if (ds.pool) ds.pool.feed();
}
function finishExtra(st) {
  for (const [k, t] of Object.entries(st.tests)) if (!t.result) {
    const w = t.pairs.map(([id]) => rate(vsPool(st, id))), wo = t.pairs.map(([, v]) => rate(vsPool(st, v)));
    t.result = { with: w.reduce((a, b) => a + b, 0) / w.length, without: wo.reduce((a, b) => a + b, 0) / wo.length };
    dsLog(st, `${CARDS[k].name}: decks with it ${pc(t.result.with)} against the pool, with a plain unit instead ${pc(t.result.without)}.`);
  }
  for (const y of Object.values(st.yard)) y.done = true;
  st.extra = [];
}

/* ---------- the page ---------- */
function renderDs() {
  const st = dsState(), opts = sel => ['', ...players().filter(p => p.kind !== 'random').map(p => p.id)].map(id => `<option value="${id}" ${id === sel ? 'selected' : ''}>${id ? esc(nameOf(id)) : '(none)'}</option>`).join('');
  if (!$('#dsP1').dataset.done) { $('#dsP1').innerHTML = opts(st.pilots[0] || ''); $('#dsP2').innerHTML = opts(st.pilots[1] || ''); $('#dsP1').dataset.done = 1; $('#dsPer').value = st.per; }
  $('#dsStart').disabled = !!ds.pool; $('#dsPause').disabled = !ds.pool;
  $('#dsStart').textContent = st.phase && st.phase !== 'done' ? 'Resume' : 'Start';
  const all = [...(st.extra || []), ...st.tasks], left = all.reduce((n, t) => n + st.per - t.done, 0);
  $('#dsStatus').textContent = (ds.pool ? 'Running' : st.phase ? 'Paused' : 'Not started') + ' · ' +
    ({ first: 'first round: every pool deck against every other one', search: st.cand ? `trying ${st.decks[st.cand.id] ? st.decks[st.cand.id].name : ''} (${st.decks[st.cand.id] ? st.decks[st.cand.id].say : ''})` : 'search', done: 'the search is done' }[st.phase] || 'no pool yet')
    + (all.length ? ` · ${left} games left in this step` : '') + ` · ${st.tries} decks tried, ${st.entered} entered the pool`;
  // the pool, per faction, best first
  $('#dsPool').innerHTML = st.phase ? LAB_FACTIONS.map(fac => `<h3 class="tuh">${esc(LAB_FACTION_NAME[fac])}</h3><table class="tutable"><thead><tr><th>Deck</th><th>Against the pool</th><th>Games</th><th>Tries from it</th><th>In the game</th><th>Cards</th></tr></thead><tbody>${
    st.pool[fac].map(id => ({ id, t: vsPool(st, id) })).sort((a, b) => rate(b.t) - rate(a.t)).map(({ id, t }) => { const d = deckOf(st, id), x = st.decks[id];
      return `<tr><td>${esc(d.name)}</td><td>${pc(rate(t))}</td><td>${games(t)}</td><td>${x ? x.fails : 0}/${DS_DONE_AFTER} failed in a row</td><td class="dsuse">${LAB_DECKS.filter(p => facOfDeck(p) === fac).map((p, i) =>
        `<button data-use="${esc(id)}" data-slot="${p}" title="This deck becomes the game's premade deck ${i + 1} of this faction (replacing ${esc(DECKS[p].name)})">Deck ${i + 1}</button>`).join('')}</td><td class="dsl">${d.list.map(([k, n]) => `${n}× ${esc(CARDS[k].name)}`).join(', ')}</td></tr>`; }).join('')
  }</tbody></table>`).join('') : '';
  for (const b of $('#dsPool').querySelectorAll('button[data-use]')) b.addEventListener('click', () => useInGame({ [b.dataset.slot]: b.dataset.use }));
  const saved = PREMADE.filter(p => p.saved).length;
  $('#dsSaved').textContent = saved ? `The game and the lab use ${saved} of the ${PREMADE.length} premade decks from here.` : 'The game and the lab use their built-in premade decks.';
  $('#dsBuiltIn').disabled = !saved; $('#dsUseBest').disabled = !st.phase;
  const yard = Object.entries(st.yard || {});
  $('#dsYard').innerHTML = yard.length ? '<h3 class="tuh">Premades against the pool (the yardstick)</h3>' + yard.map(([p, y]) => `${esc(DECKS[p].name)}: ${y.done ? pc(rate(vsPool(st, y.id))) : 'playing…'}`).join(' · ') : '';
  $('#dsLog').innerHTML = st.log.slice(-15).reverse().map(x => `<li>${esc(x)}</li>`).join('');
  renderCardStats();
}
function renderCardStats() {
  const st = dsState(), fac = $('#dsFac').value || LAB_FACTIONS[0];
  if (!$('#dsFac').options.length) $('#dsFac').innerHTML = LAB_FACTIONS.map(f => `<option value="${f}">${esc(LAB_FACTION_NAME[f])}</option>`).join('');
  const rows = factionCards(fac).map(k => ({ k, e: st.stats[k] || [0, 0, 0, 0, 0] })).filter(r => r.e[0]);
  const partner = k => { let best = null; for (const r of rows) if (r.k !== k && r.e[2] >= ENOUGH) { const l = pairLift(st, k, r.k); if (!best || l > best.l) best = { k: r.k, l }; } return best && best.l > 1.2 ? `${CARDS[best.k].name} (×${best.l.toFixed(1)})` : ''; };
  const p = (a, b) => (b ? pc(a / b) : '–');
  $('#dsCards').innerHTML = rows.length ? `<table class="tutable"><thead><tr><th>Card</th><th>Cost</th><th>Games in a deck</th><th>Played when in the deck</th><th>Win rate when played</th><th>Win rate of its decks</th><th>Most played with</th><th>With / without</th></tr></thead><tbody>${
    rows.sort((a, b) => b.e[2] / b.e[0] - a.e[2] / a.e[0]).map(({ k, e }) => { const t = st.tests[k];
      return `<tr><td>${esc(CARDS[k].name)}${e[2] / e[0] >= 0.9 ? ' <span class="tud">always played</span>' : e[2] / e[0] < 0.2 ? ' <span class="tud">rarely played</span>' : ''}</td><td>${CARDS[k].cost ?? ''}</td><td>${e[0]}</td><td>${p(e[2], e[0])}</td><td>${p(e[3], e[2])}</td><td>${p(e[1], e[0])}</td><td>${esc(partner(k))}</td><td>${t ? (t.result ? `${pc(t.result.with)} / ${pc(t.result.without)}` : 'playing…') : `<button data-test="${k}">Test</button>`}</td></tr>`; }).join('')
  }</tbody></table>` : '<p class="note">No games played with this faction yet.</p>';
  for (const b of $('#dsCards').querySelectorAll('button[data-test]')) b.addEventListener('click', () => testCard(b.dataset.test));
}
/* ---------- decks found here become the game's premade decks (and so the decks the lab trains and plays with) ---------- */
/** slots: premade id -> pool deck id. Every pool deck keeps its own list first, so its results stay its own. */
async function useInGame(slots) {
  const st = dsState(), names = Object.entries(slots).map(([p, id]) => `${deckOf(st, id).name} → ${DECKS[p].name}`);
  if (!(await askYes('Use these decks in the game?', names.join(' · ') + '. The game, its computer opponents and every AI in the lab then play with them. The lab reloads; whatever is running pauses.', 'Use them'))) return;
  for (const id of poolIds(st)) if (!st.decks[id]) { const d = deckOf(st, id); addDeck(st, { ...d, list: d.list.map(([k, n]) => [k, n]), from: null, fails: 0, tried: [] }); }
  let cur = null;
  try { cur = JSON.parse(localStorage.getItem(PREMADE_SAVED_STORE) || 'null'); } catch (e) { cur = null; }
  const decks = (cur && cur.decks) || {};
  for (const [p, id] of Object.entries(slots)) { const d = deckOf(st, id); decks[p] = { name: d.name, cards: Object.fromEntries(d.list) }; }
  writeSaved({ stamp: String(Date.now()), decks });
}
/** Per faction, the two pool decks with the best results against the pool become its premades. */
function useBest() {
  const st = dsState(), slots = {};
  for (const fac of LAB_FACTIONS) {
    const best = st.pool[fac].slice().sort((a, b) => rate(vsPool(st, b)) - rate(vsPool(st, a)));
    LAB_DECKS.filter(p => facOfDeck(p) === fac).forEach((p, i) => { if (best[i]) slots[p] = best[i]; });
  }
  useInGame(slots);
}
async function useBuiltIn() {
  if (!(await askYes('Go back to the built-in premade decks?', 'The game, its computer opponents and every AI in the lab play the premade decks written in the game again. The lab reloads; whatever is running pauses.', 'Go back'))) return;
  const st = dsState();
  for (const id of poolIds(st)) if (!st.decks[id]) { const d = deckOf(st, id); addDeck(st, { ...d, list: d.list.map(([k, n]) => [k, n]), from: null, fails: 0, tried: [] }); }
  writeSaved(null);
}
async function writeSaved(data) {
  stopDs(); if (Object.keys(trainings).length) await stopAllTraining();   // trained networks are stored before the reload
  if (tour.running) pauseTournament(); if (tune.running) pauseTune();
  save();
  try { if (data) localStorage.setItem(PREMADE_SAVED_STORE, JSON.stringify(data)); else localStorage.removeItem(PREMADE_SAVED_STORE); }
  catch (e) { reportError('This browser did not let the lab save the decks.'); return; }
  location.reload();
}
function exportDs() {
  const st = dsState(), lines = ['Three Bases AI lab: deck search', ''];
  for (const fac of LAB_FACTIONS) {
    lines.push(LAB_FACTION_NAME[fac] + ':');
    for (const id of st.pool[fac] || []) { const d = deckOf(st, id); lines.push(`  ${d.name} (${pc(rate(vsPool(st, id)))} against the pool): ` + d.list.map(([k, n]) => `${n}x ${CARDS[k].name}`).join(', ')); }
  }
  lines.push('', 'Cards (games in a deck, played when in the deck, win rate when played, win rate of its decks):');
  for (const [k, e] of Object.entries(st.stats)) lines.push(`  ${CARDS[k].name}: ${e[0]}, ${pc(e[2] / Math.max(1, e[0]))}, ${e[2] ? pc(e[3] / e[2]) : '–'}, ${pc(e[1] / Math.max(1, e[0]))}`);
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([lines.join('\n')], { type: 'text/plain' })); a.download = 'deck search.txt';
  document.body.appendChild(a); a.click(); a.remove();
}
$('#dsStart').addEventListener('click', startDs);
$('#dsPause').addEventListener('click', stopDs);
$('#dsYardBtn').addEventListener('click', measurePremades);
$('#dsExport').addEventListener('click', exportDs);
$('#dsUseBest').addEventListener('click', useBest);
$('#dsBuiltIn').addEventListener('click', useBuiltIn);
$('#dsFac').addEventListener('change', renderCardStats);
$('#dsThreads').addEventListener('change', () => { if (ds.pool) ds.pool.resize(Math.max(1, Math.min(32, Number($('#dsThreads').value) || 1))); });
$('#dsReset').addEventListener('click', async () => {
  if (!(await askYes('Start the deck search over?', 'The pool, every deck tried and the card statistics are cleared.', 'Start over'))) return;
  stopDs(); state.ds = freshDs(); save(); renderDs();
});

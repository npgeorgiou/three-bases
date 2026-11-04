/* =====================================================================
   Tournament
   ===================================================================== */

const tour = { running: false, pool: null, queue: [], failed: 0, lastError: '' };

function renderRoster() {
  const list = $('#aiList');
  list.innerHTML = '';
  for (const p of players()) {
    const custom = state.custom.includes(p), row = document.createElement('div');
    row.className = 'ai';
    row.innerHTML = `<input type="checkbox" aria-label="Enter ${esc(p.name)}" ${state.chosen.includes(p.id) ? 'checked' : ''}>
      <div class="name">${esc(p.name)}${custom ? '<span class="tag">yours</span>' : ''}</div>
      <div class="acts">${custom ? '<button data-a="del">Delete</button>' : ''}</div>
      <div class="desc">${esc(p.desc || describe(p))}</div>`;
    row.querySelector('input').addEventListener('change', e => {
      state.chosen = e.target.checked ? [...new Set([...state.chosen, p.id])] : state.chosen.filter(x => x !== p.id);
      save();
    });
    row.querySelectorAll('[data-a]').forEach(b => b.addEventListener('click', async () => {
      if (b.dataset.a === 'del' && await askYes(`Delete ${p.name}?`, '', 'Delete')) {
        state.custom = state.custom.filter(x => x !== p);
        state.chosen = state.chosen.filter(x => x !== p.id);
        save(); renderPlayers();
      }
    }));
    list.appendChild(row);
  }
}
function describe(p) {
  const changes = S_FIELDS.filter(([k]) => p.cfg && p.cfg[k] !== undefined).map(([k]) => `${k} ${p.cfg[k]}`);
  return 'Strategist. ' + (changes.length ? 'Changes: ' + changes.join(', ') : 'Default settings.');
}
function renderPlayers() {
  if (typeof renderAgreeChoices === 'function' && $('#sA').options.length) renderAgreeChoices();
  renderRoster();
  const opts = players().map(p => `<option value="${p.id}">${esc(p.name)}</option>`).join('');
  for (const [sel, fallback] of [['#vsAi', 'bench'], ['#wA', 'net-tabula-alone'], ['#wB', 'bench']]) {
    const el = $(sel), keep = el.value || fallback;
    el.innerHTML = opts;
    el.value = playerById(keep) ? keep : fallback;
  }
}

$('#format').addEventListener('change', () => { $('#vsWrap').hidden = $('#format').value !== 'one'; });

/* ---------- schedule and running ---------- */

/** Every game to play: each pairing, each chosen matchup, seats and factions evenly swapped. */
function makeSchedule() {
  const ids = state.chosen.filter(playerById), n = Math.max(2, Math.round(Number($('#games').value) / 2) * 2), pairs = [];
  if ($('#format').value === 'one') { const vs = $('#vsAi').value; for (const id of ids) if (id !== vs) pairs.push([id, vs]); }
  else for (let i = 0; i < ids.length; i++) for (let j = i + 1; j < ids.length; j++) pairs.push([ids[i], ids[j]]);
  const jobs = [];
  for (const [a, b] of pairs) for (const m of Object.keys(MATCHUPS).filter(m => $('#m' + m).checked)) for (let g = 0; g < n; g++) {
    const aFirst = g % 2 === 0;
    jobs.push({ key: `${a}|${b}|${m}|${g}`, a, b, m, seat0: aFirst ? a : b, decks: scheduledDecks(g, MATCHUPS[m].pairs) });
  }
  return jobs;
}

function startTournament() {
  if (manual) { reportError('Stop the network test first: only one thing runs at a time.'); return; }
  if (Object.keys(trainings).length) stopAllTraining();
  if (tune.running) pauseTune();
  if (!state.plan) {
    const jobs = makeSchedule();
    if (!jobs.length) { $('#status').textContent = 'Tick at least two players (or one plus the opponent) and one matchup.'; return; }
    state.plan = { jobs };
    save();
  }
  const done = new Set(state.results.map(r => r.key));
  tour.queue = state.plan.jobs.filter(j => !done.has(j.key));
  tour.running = true; tour.failed = 0; tour.lastError = ''; notice = '';
  $('#start').disabled = true; $('#pause').disabled = false;
  const nextJob = () => {
    const job = tour.queue.shift();
    if (!job) return null;
    const other = job.seat0 === job.a ? job.b : job.a;
    return { ...job, specs: [specOf(job.seat0), specOf(other)] };
  };
  const onResult = (r, job) => {
    record(r, job);
    if (!tour.queue.length && !tour.pool.busy()) finishTournament();
  };
  // a game that crashes is tried once more; if it crashes again it is recorded as unfinished, so the tournament always completes
  const onFail = (job, message) => {
    tour.failed++; tour.lastError = message;
    if (job && (job.attempts = (job.attempts || 0) + 1) < 2) tour.queue.unshift(job);
    else if (job) record({ key: job.key, winner: 'none', rounds: 0, ms: [0, 0], failed: true }, job);
    if (tour.pool && !tour.queue.length && !tour.pool.busy()) finishTournament();
    else renderProgress();
  };
  tour.pool = new Pool(Math.max(1, Math.min(32, Number($('#threads').value) || 1)), Object.fromEntries(NETS.map(n => [n.id, playable(netData[n.id])])), nextJob, onResult, onFail);
  renderProgress();
}
function pauseTournament() {
  tour.running = false;
  if (tour.pool) tour.pool.stop();
  tour.pool = null;
  $('#start').disabled = false; $('#pause').disabled = true; $('#start').textContent = 'Resume';
  renderProgress();
}
function finishTournament() {
  tour.running = false;
  if (tour.pool) tour.pool.stop();
  tour.pool = null;
  state.plan = null;
  save();
  $('#start').disabled = false; $('#pause').disabled = true; $('#start').textContent = 'Start';
  renderProgress(true);
}
$('#start').addEventListener('click', startTournament);
$('#pause').addEventListener('click', pauseTournament);
$('#reset').addEventListener('click', async () => {
  if (!(await askYes('Clear all tournament results?', '', 'Clear'))) return;
  if (tour.running) pauseTournament();
  state.results = []; state.plan = null;
  $('#start').textContent = 'Start';
  save(); renderResults(); renderProgress();
});

function record(r, job) {
  if (!state.plan || state.results.some(x => x.key === r.key)) return;
  const aFirst = job.seat0 === job.a, seatOf = { [job.a]: aFirst ? 0 : 1, [job.b]: aFirst ? 1 : 0 };
  const winner = r.winner === 'none' || r.winner === 'draw' || r.winner === 'lost' ? r.winner : (r.winner === seatOf[job.a] ? 'a' : 'b');
  state.results.push({ key: r.key, a: job.a, b: job.b, m: job.m, winner, rounds: r.rounds,
    ms: { a: r.ms[seatOf[job.a]], b: r.ms[seatOf[job.b]] }, failed: !!r.failed, aFirst, aFaction: facOfDeck(job.decks[seatOf[job.a]]), bFaction: facOfDeck(job.decks[seatOf[job.b]]) });
  save();
  renderResults();
  renderProgress();
}


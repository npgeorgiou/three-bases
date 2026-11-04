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
/* ---------- ifelse AI: tuning all its values at once with CMA-ES ---------- */

/** Who the ifelse AI can play against: the Benchmark, the Strategist and every learning AI in the lab (playing as in its tests). */
const TUNE_OPPS = () => [['bench', 'Benchmark'], ['strategist', 'Strategist'], ...NETS.map(n => ['net:' + n.id, n.name])];
const tuneOppName = k => (TUNE_OPPS().find(([x]) => x === k) || [k, k])[1];
function tuneOppSpec(k) {
  if (k === 'bench') return { kind: 'bench' };
  if (k === 'strategist') return { kind: 'strategist', full: strategistConfig({}) };
  return { kind: 'net', net: k.slice(4), play: { replies: false, explore: 0 } };
}
/*
 * Every value lives on one common scale x (0 = its starting value), so one step size suits them all:
 * weights move by a factor (×e^x), a weight starting at 0 moves by 5·x on its own scale, shares move on the
 * logit scale (×2), whole numbers move by x times their range (rounded), a switch flips when x crosses ±0.25.
 */
const TUNE_N = IFELSE_FIELDS.length;
const logit = v => Math.log(v / (1 - v)), sigm = z => 1 / (1 + Math.exp(-z));
function tuneDecode(x) {
  const out = {};
  IFELSE_FIELDS.forEach(([k, , type, def, extra], i) => {
    const z = x[i];
    if (type === 'int') { const [lo, hi] = extra; out[k] = Math.max(lo, Math.min(hi, Math.round(def + z * (hi - lo)))); }
    else if (type === 'switch') out[k] = def - 0.5 + 2 * z > 0 ? 1 : 0;
    else if (type === 'share') out[k] = Math.max(0.01, Math.min(1, sigm(logit(Math.min(0.99, Math.max(0.01, def))) + 2 * z)));
    else out[k] = def === 0 ? 5 * (extra || 1) * z : def * Math.exp(z);
  });
  return out;
}
const SIGMA0 = 0.3, LAMBDA0 = 10;
/** CMA-ES state for n values: centre, step size, covariance, evolution paths. */
function cmaFresh(mean, lambda) {
  const n = TUNE_N, I = Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => (i === j ? 1 : 0)));
  return { mean: mean.slice(), sigma: SIGMA0, lambda, C: I.map(r => r.slice()), B: I.map(r => r.slice()), D: Array(n).fill(1),
    pc: Array(n).fill(0), ps: Array(n).fill(0), g: 0 };
}
function cmaConsts(n, lambda) {
  const mu = Math.floor(lambda / 2), raw = Array.from({ length: mu }, (_, i) => Math.log(mu + 0.5) - Math.log(i + 1));
  const sw = raw.reduce((a, b) => a + b, 0), w = raw.map(x => x / sw), mueff = 1 / w.reduce((a, b) => a + b * b, 0);
  const cc = (4 + mueff / n) / (n + 4 + 2 * mueff / n), cs = (mueff + 2) / (n + mueff + 5);
  const c1 = 2 / ((n + 1.3) ** 2 + mueff), cmu = Math.min(1 - c1, 2 * (mueff - 2 + 1 / mueff) / ((n + 2) ** 2 + mueff));
  const damps = 1 + 2 * Math.max(0, Math.sqrt((mueff - 1) / (n + 1)) - 1) + cs, chiN = Math.sqrt(n) * (1 - 1 / (4 * n) + 1 / (21 * n * n));
  return { mu, w, mueff, cc, cs, c1, cmu, damps, chiN };
}
/** Eigen-decomposition of a symmetric matrix (Jacobi rotations): C = B·diag(d)·Bᵀ. */
function eigSym(C) {
  const n = C.length, A = C.map(r => r.slice()), V = Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => (i === j ? 1 : 0)));
  for (let sweep = 0; sweep < 60; sweep++) {
    let off = 0;
    for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) off += A[p][q] * A[p][q];
    if (off < 1e-18) break;
    for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) {
      if (Math.abs(A[p][q]) < 1e-15) continue;
      const th = (A[q][q] - A[p][p]) / (2 * A[p][q]), t = Math.sign(th || 1) / (Math.abs(th) + Math.sqrt(th * th + 1));
      const c = 1 / Math.sqrt(t * t + 1), s = t * c;
      for (let k = 0; k < n; k++) { const a = A[k][p], b = A[k][q]; A[k][p] = c * a - s * b; A[k][q] = s * a + c * b; }
      for (let k = 0; k < n; k++) { const a = A[p][k], b = A[q][k]; A[p][k] = c * a - s * b; A[q][k] = s * a + c * b; }
      for (let k = 0; k < n; k++) { const a = V[k][p], b = V[k][q]; V[k][p] = c * a - s * b; V[k][q] = s * a + c * b; }
    }
  }
  return { B: V, d: A.map((r, i) => Math.max(1e-20, r[i])) };
}
const gauss = () => Math.sqrt(-2 * Math.log(1 - Math.random())) * Math.cos(2 * Math.PI * Math.random());
function cmaSample(cma) {
  const n = TUNE_N, z = Array.from({ length: n }, gauss);
  return cma.mean.map((m, i) => m + cma.sigma * cma.B[i].reduce((s, b, j) => s + b * cma.D[j] * z[j], 0));
}
/** One CMA-ES step from the generation's candidates and their win rates (higher is better). */
function cmaUpdate(cma, xs, rates) {
  const n = TUNE_N, K = cmaConsts(n, cma.lambda), order = rates.map((r, i) => i).sort((a, b) => rates[b] - rates[a]);
  const old = cma.mean.slice(), sel = order.slice(0, K.mu).map(i => xs[i]);
  cma.mean = old.map((_, j) => sel.reduce((s, x, i) => s + K.w[i] * x[j], 0));
  const yw = cma.mean.map((m, j) => (m - old[j]) / cma.sigma);
  const BtY = cma.B[0].map((_, k) => yw.reduce((s, y, j) => s + cma.B[j][k] * y, 0));                // Bᵀ·yw
  const invSqrtY = cma.B.map(row => row.reduce((s, b, k) => s + b * BtY[k] / cma.D[k], 0));         // C^-1/2·yw
  cma.ps = cma.ps.map((p, j) => (1 - K.cs) * p + Math.sqrt(K.cs * (2 - K.cs) * K.mueff) * invSqrtY[j]);
  cma.g++;
  const psn = Math.hypot(...cma.ps), hsig = psn / Math.sqrt(1 - (1 - K.cs) ** (2 * cma.g)) / K.chiN < 1.4 + 2 / (n + 1) ? 1 : 0;
  cma.pc = cma.pc.map((p, j) => (1 - K.cc) * p + hsig * Math.sqrt(K.cc * (2 - K.cc) * K.mueff) * yw[j]);
  const ys = sel.map(x => x.map((v, j) => (v - old[j]) / cma.sigma));
  for (let i = 0; i < n; i++) for (let j = 0; j <= i; j++) {
    let v = (1 - K.c1 - K.cmu) * cma.C[i][j] + K.c1 * (cma.pc[i] * cma.pc[j] + (1 - hsig) * K.cc * (2 - K.cc) * cma.C[i][j]);
    for (let k = 0; k < ys.length; k++) v += K.cmu * K.w[k] * ys[k][i] * ys[k][j];
    cma.C[i][j] = cma.C[j][i] = v;
  }
  cma.sigma = Math.min(1, cma.sigma * Math.exp((K.cs / K.damps) * (psn / K.chiN - 1)));
  const { B, d } = eigSym(cma.C);
  cma.B = B; cma.D = d.map(Math.sqrt);
}

const freshTune = (opps = ['bench']) => ({ v: 3, opps, cma: cmaFresh(Array(TUNE_N).fill(0), LAMBDA0), best: { ...IFELSE_DEFAULTS },
  gen: 0, restarts: 0, cand: null, hist: [], stall: 0, top: -1 });
function tuneState() {
  if (!state.ifelse || state.ifelse.v !== 3) state.ifelse = freshTune(state.ifelse && state.ifelse.opps);   // earlier tunings are replaced
  const st = state.ifelse;
  st.opps = (st.opps || []).filter(k => TUNE_OPPS().some(([x]) => x === k));
  if (!st.opps.length) st.opps = ['bench'];
  return st;
}
const tuneGames = () => Math.max(20, Math.round(Number($('#tuGames').value) / 2) * 2 || 300);
function newGeneration() {
  const st = tuneState(), L = st.cma.lambda;
  st.cand = { G: tuneGames(), xs: Array.from({ length: L }, () => cmaSample(st.cma)), w: Array(L).fill(0), n: Array(L).fill(0), started: Array(L).fill(0) };
}
function tuneJob() {
  const st = tuneState(), c = st.cand;
  if (!c) return null;
  let i = -1;
  c.started.forEach((s, j) => { if (s < c.G && (i < 0 || s < c.started[i])) i = j; });   // the candidate with fewest games started
  if (i < 0) return null;
  const gi = c.started[i]++, m = gi % 3 === 2 ? 'S' : 'X', seat = Math.floor(gi / 3) % 2;
  const mine = { kind: 'ifelse', cfg: ifelseFull(tuneDecode(c.xs[i])) };
  const opp = tuneOppSpec(st.opps[Math.floor(gi / 12) % st.opps.length]);   // every candidate gets the same schedule
  return { key: 'tune' + st.gen + '-' + i + '-' + gi, i, seat, gen: st.gen, specs: seat === 0 ? [mine, opp] : [opp, mine],
    decks: MATCHUPS[m].pairs[Math.floor(gi / 6) % MATCHUPS[m].pairs.length] };
}
function tuneResult(r, job) {
  const st = tuneState(), c = st.cand;
  if (!c || job.gen !== st.gen) return;
  c.w[job.i] += r.winner === job.seat ? 1 : r.winner === 'draw' ? 0.5 : 0;
  c.n[job.i]++;
  if (c.n.every(x => x >= c.G)) finishGeneration(); else renderTuneStatus();
}
function finishGeneration() {
  const st = tuneState(), c = st.cand, rates = c.w.map((w, i) => w / c.n[i]);
  cmaUpdate(st.cma, c.xs, rates);
  st.best = tuneDecode(st.cma.mean);
  const avg = rates.reduce((a, b) => a + b, 0) / rates.length, top = Math.max(...rates);
  st.hist.push({ gen: st.gen, avg, top, lambda: st.cma.lambda, sigma: st.cma.sigma });
  if (st.hist.length > 2000) st.hist.splice(0, st.hist.length - 2000);
  // stalled: no better generation average for 20 generations, or a tiny step size → restart around the centre with twice the candidates
  if (avg > st.top + 0.01) { st.top = avg; st.stall = 0; } else st.stall++;
  if (st.stall >= 20 || st.cma.sigma < 0.02) {
    st.restarts++; st.stall = 0; st.top = -1;
    st.cma = cmaFresh(st.cma.mean, Math.min(40, st.cma.lambda * 2));
    st.hist.push({ gen: st.gen, mark: `restart ${st.restarts} · ${st.cma.lambda} candidates` });
  }
  st.gen++; st.cand = null;
  if (tune.running) newGeneration();
  save(); renderTune();
}
function startTune() {
  if (manual) { reportError('Stop the network test first: only one thing runs at a time.'); return; }
  if (Object.keys(trainings).length) stopAllTraining();
  if (tour.running) pauseTournament();
  const st = tuneState();
  if (st.cand) st.cand.started = st.cand.n.slice();                           // games cut off by a pause are played again
  else newGeneration();
  tune.running = true;
  const onFail = (job, msg) => { const c = tuneState().cand; if (c && job && job.gen === tuneState().gen) c.started[job.i]--; reportError('A tuning game failed: ' + msg); };
  tune.pool = new Pool(Math.max(1, Math.min(32, Number($('#tuThreads').value) || 1)), Object.fromEntries(NETS.map(n => [n.id, playable(netData[n.id])])), tuneJob, tuneResult, onFail);
  renderTune();
}
function pauseTune() {
  tune.running = false;
  if (tune.pool) tune.pool.stop();
  tune.pool = null;
  save(); renderTune();
}
$('#tuStart').addEventListener('click', startTune);
$('#tuExport').addEventListener('click', () => {
  const st = tuneState(), values = { ...st.best };
  askName({ title: 'Export ifelse AI', note: 'Its current values, as a file the game can load. The game can also read them straight from this browser\'s lab.',
    value: `ifelse AI gen ${st.gen}`, ok: 'Export',
    check: v => /[\\/:*?"<>|]/.test(v) ? 'A name can\'t contain \\ / : * ? " < > |' : '' }).then(name => {
    if (!name) return;
    const blob = new Blob([JSON.stringify({ kind: 'ifelse', name, gen: st.gen, opponents: st.opps.map(tuneOppName), values })], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = `${name}.json`;
    document.body.appendChild(a); a.click(); a.remove();
  });
});
$('#tuPause').addEventListener('click', pauseTune);
$('#tuReset').addEventListener('click', async () => {
  if (!(await askYes('Start the ifelse AI over?', 'Its values go back to the starting values and its history is cleared.', 'Start over'))) return;
  const was = tune.running;
  if (was) pauseTune();
  state.ifelse = freshTune(tuneState().opps); save();
  if (was) startTune(); else renderTune();
});
/** A new opponent mix: the generation under way starts again; the search itself carries on. */
function setTuneOpps(opps) {
  const st = tuneState(), was = tune.running;
  if (was) pauseTune();
  st.opps = opps; st.cand = null; st.top = -1; st.stall = 0;
  const last = st.hist[st.hist.length - 1], mark = { gen: st.gen, mark: 'vs ' + opps.map(tuneOppName).join(', ') };
  if (last && last.mark) st.hist[st.hist.length - 1] = mark; else st.hist.push(mark);
  save();
  if (was) startTune(); else renderTune();
}
$('#tuThreads').addEventListener('change', () => { if (tune.pool) tune.pool.resize(Math.max(1, Math.min(32, Number($('#tuThreads').value) || 1))); });
const tpct = v => (v == null || !Number.isFinite(v) ? '–' : Math.round(v * 100) + '%');
function renderTuneStatus() {
  const st = tuneState(), c = st.cand, last = [...st.hist].reverse().find(e => !e.mark);
  const done = c ? c.n.reduce((a, b) => a + b, 0) : 0, total = c ? c.G * c.xs.length : 0;
  $('#tuStatus').textContent = (tune.running ? 'Tuning' : st.gen || c ? 'Paused' : 'Not started') +
    ` · generation ${st.gen + 1} · ${st.cma.lambda} candidates` + (c ? ` · ${done}/${total} games` : '') +
    (last ? ` · last generation: average ${tpct(last.avg)}, best candidate ${tpct(last.top)}` : '') +
    ` · step size ${st.cma.sigma.toFixed(3)}` + (st.restarts ? ` · ${st.restarts} restart${st.restarts > 1 ? 's' : ''}` : '');
}
function renderTune() {
  const st = tuneState();
  $('#tuOpps').innerHTML = '<span class="tuoppl">Opponents</span>' + TUNE_OPPS().map(([k, name]) =>
    `<label class="tuopp"><input type="checkbox" value="${k}" ${st.opps.includes(k) ? 'checked' : ''}> ${esc(name)}</label>`).join('')
    + '<span class="note">Games are shared equally among them; at least one.</span>';
  for (const b of $('#tuOpps').querySelectorAll('input')) b.addEventListener('change', () => {
    const on = [...$('#tuOpps').querySelectorAll('input:checked')].map(x => x.value);
    if (!on.length) { b.checked = true; return; }
    setTuneOpps(on);
  });
  $('#tuStart').disabled = tune.running; $('#tuPause').disabled = !tune.running;
  $('#tuStart').textContent = st.gen || st.cand ? 'Resume' : 'Start';
  renderTuneStatus();
  // the chart: per generation, the candidates' average win rate (line) and the best candidate's (dot)
  const h = st.hist, W = 1200, H = 300, l = 52, r = 16, t = 14, b = 34, pw = W - l - r, ph = H - t - b;
  const gens = h.filter(e => !e.mark), n = Math.max(1, gens.length - 1);
  const X = i => l + pw * (gens.length < 2 ? 0.5 : i / n), Y = v => t + ph * (1 - v);
  let svg = `<rect class="plot" x="${l}" y="${t}" width="${pw}" height="${ph}"></rect>`;
  for (const v of [0, 0.25, 0.5, 0.75, 1]) svg += `<line class="grid${v === 0.5 ? ' mid' : ''}" x1="${l}" x2="${W - r}" y1="${Y(v)}" y2="${Y(v)}"></line><text class="ylab" x="${l - 8}" y="${Y(v) + 5}">${v * 100}%</text>`;
  if (!gens.length) svg += `<text class="empty" x="${l + pw / 2}" y="${t + ph / 2}">No generations yet.</text>`;
  else {
    let i = 0;
    for (const e of h) {
      if (!e.mark) { i++; continue; }
      const x = X(Math.max(0, i - 0.5)), right = x > W - r - 200;
      svg += `<line class="tumark" x1="${x}" x2="${x}" y1="${t}" y2="${t + ph}"></line><text class="tumarkt" x="${right ? x - 4 : x + 4}" y="${t + 14}" text-anchor="${right ? 'end' : 'start'}">${esc(e.mark)}</text>`;
    }
    svg += `<polyline class="tubest" points="${gens.map((e, k) => `${X(k)},${Y(e.avg)}`).join(' ')}"></polyline>`;
    svg += gens.map((e, k) => `<circle class="tucand acc" cx="${X(k)}" cy="${Y(e.top)}" r="3.5"><title>Generation ${e.gen + 1}: average ${tpct(e.avg)}, best candidate ${tpct(e.top)} (${e.lambda} candidates)</title></circle>`).join('');
    svg += `<text class="xlab" x="${l}" y="${H - 10}">generation ${gens[0].gen + 1}</text><text class="xlab end" x="${W - r}" y="${H - 10}">generation ${gens[gens.length - 1].gen + 1}</text>`;
  }
  $('#tuChart').innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Win rates by generation">${svg}</svg>
    <div class="tulegend"><span class="lg best"></span>candidates' average win rate <span class="lg acc"></span>best candidate</div>`;
  const fmt = v => (Number.isInteger(v) ? String(v) : Math.abs(v) >= 10 ? v.toFixed(1) : v.toFixed(3));
  $('#tuTable').innerHTML = `<table class="tutable"><thead><tr><th>Value</th><th>Start</th><th>ifelse AI (centre)</th></tr></thead><tbody>${
    IFELSE_FIELDS.map(([k, text]) => { const d = IFELSE_DEFAULTS[k], v = st.best[k] ?? d, ch = Math.abs(v - d) > 1e-9;
      return `<tr${ch ? ' class="ch"' : ''}><td>${esc(text)}</td><td>${fmt(d)}</td><td>${fmt(v)}${ch ? ` <span class="tud">${v > d ? '▲' : '▼'}</span>` : ''}</td></tr>`; }).join('')
  }</tbody></table>`;
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


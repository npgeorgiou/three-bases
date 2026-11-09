/* ---------- ifelse AI: tuning all its values at once with CMA-ES ---------- */

/** Who the ifelse AI can play against: the Benchmark and every learning AI in the lab (playing as in its tests). */
const TUNE_OPPS = () => [['bench', 'Benchmark'], ...NETS.map(n => ['net:' + n.id, n.name])];
const tuneOppName = k => (TUNE_OPPS().find(([x]) => x === k) || [k, k])[1];
function tuneOppSpec(k, depth) {
  if (k === 'bench') return { kind: 'bench', depth };
  return { kind: 'net', net: k.slice(4), play: { replies: false, explore: 0 } };
}
/*
 * Every value lives on one common scale x (0 = its starting value), so one step size suits them all:
 * weights move by a factor (×e^x), a weight starting at 0 moves by 5·x on its own scale, shares move on the
 * logit scale (×2), whole numbers move by x times their range (rounded), a switch flips when x crosses ±0.25.
 */
const TUNE_N = IFELSE_FIELDS.length;
const logit = v => Math.log(v / (1 - v)), sigm = z => 1 / (1 + Math.exp(-z));
/** Values from the search's numbers. Widths of moves deeper than the tuning depth are never used in tuning games, so they keep their start. */
function tuneDecode(x, depth = BENCH_VALUES.depth) {
  const out = {};
  IFELSE_FIELDS.forEach(([k, , type, def, extra], i) => {
    const z = /^w\d$/.test(k) ? 0 : x[i];                              // how wide it looks is set, not tuned (wider is always slower)
    if (type === 'int') { const [lo, hi] = extra; out[k] = Math.max(lo, Math.min(hi, Math.round(def + z * (hi - lo)))); }
    else if (type === 'switch') out[k] = def - 0.5 + 2 * z > 0 ? 1 : 0;
    else if (type === 'share') out[k] = Math.max(0.01, Math.min(1, sigm(logit(Math.min(0.99, Math.max(0.01, def))) + 2 * z)));
    else out[k] = def === 0 ? 5 * (extra || 1) * z : def * Math.exp(z);
  });
  return out;
}
const SIGMA0 = 0.3, LAMBDA0 = Math.max(10, 4 + Math.floor(3 * Math.log(TUNE_N)));   // candidates per generation: CMA-ES's usual number for this many values
/*
 * The search keeps one step size per value (the diagonal form of CMA-ES, "sep-CMA-ES"): with about a hundred values the
 * full form learns which values matter roughly n/3 times slower, far too slow for a few hundred generations. Candidates
 * come in mirrored pairs (centre + step and centre − step) playing the same deals, so luck cancels out between them.
 */
function cmaFresh(mean, lambda) {
  return { mean: mean.slice(), sigma: SIGMA0, lambda: lambda + (lambda % 2), D: Array(TUNE_N).fill(1), pc: Array(TUNE_N).fill(0), ps: Array(TUNE_N).fill(0), g: 0 };
}
function cmaConsts(n, lambda) {
  const mu = Math.floor(lambda / 2), raw = Array.from({ length: mu }, (_, i) => Math.log(mu + 0.5) - Math.log(i + 1));
  const sw = raw.reduce((a, b) => a + b, 0), w = raw.map(x => x / sw), mueff = 1 / w.reduce((a, b) => a + b * b, 0);
  const cc = (4 + mueff / n) / (n + 4 + 2 * mueff / n), cs = (mueff + 2) / (n + mueff + 5), sep = (n + 2) / 3;
  const c1 = Math.min(1, sep * 2 / ((n + 1.3) ** 2 + mueff)), cmu = Math.min(1 - c1, sep * 2 * (mueff - 2 + 1 / mueff) / ((n + 2) ** 2 + mueff));
  const damps = 1 + 2 * Math.max(0, Math.sqrt((mueff - 1) / (n + 1)) - 1) + cs, chiN = Math.sqrt(n) * (1 - 1 / (4 * n) + 1 / (21 * n * n));
  return { mu, w, mueff, cc, cs, c1, cmu, damps, chiN };
}
const gauss = () => Math.sqrt(-2 * Math.log(1 - Math.random())) * Math.cos(2 * Math.PI * Math.random());
/** A generation's candidates: mirrored pairs around the centre. */
function cmaSamples(cma) {
  const xs = [];
  for (let k = 0; k < cma.lambda / 2; k++) {
    const z = Array.from({ length: TUNE_N }, gauss);
    xs.push(cma.mean.map((m, i) => m + cma.sigma * cma.D[i] * z[i]), cma.mean.map((m, i) => m - cma.sigma * cma.D[i] * z[i]));
  }
  return xs;
}
/** One step from the generation's candidates and their win rates (higher is better). */
function cmaUpdate(cma, xs, rates) {
  const n = TUNE_N, K = cmaConsts(n, cma.lambda), order = rates.map((r, i) => i).sort((a, b) => rates[b] - rates[a]);
  const old = cma.mean.slice(), sel = order.slice(0, K.mu).map(i => xs[i]);
  cma.mean = old.map((_, j) => sel.reduce((s, x, i) => s + K.w[i] * x[j], 0));
  const yw = cma.mean.map((m, j) => (m - old[j]) / cma.sigma);
  cma.ps = cma.ps.map((p, j) => (1 - K.cs) * p + Math.sqrt(K.cs * (2 - K.cs) * K.mueff) * yw[j] / cma.D[j]);
  cma.g++;
  const psn = Math.hypot(...cma.ps), hsig = psn / Math.sqrt(1 - (1 - K.cs) ** (2 * cma.g)) / K.chiN < 1.4 + 2 / (n + 1) ? 1 : 0;
  cma.pc = cma.pc.map((p, j) => (1 - K.cc) * p + hsig * Math.sqrt(K.cc * (2 - K.cc) * K.mueff) * yw[j]);
  const ys = sel.map(x => x.map((v, j) => (v - old[j]) / cma.sigma));
  cma.D = cma.D.map((d, i) => {
    let v = (1 - K.c1 - K.cmu) * d * d + K.c1 * (cma.pc[i] * cma.pc[i] + (1 - hsig) * K.cc * (2 - K.cc) * d * d);
    for (let k = 0; k < ys.length; k++) v += K.cmu * K.w[k] * ys[k][i] * ys[k][i];
    return Math.sqrt(Math.max(1e-20, v));
  });
  cma.sigma = Math.min(1, cma.sigma * Math.exp((K.cs / K.damps) * (psn / K.chiN - 1)));
}

const TUNE_NAMES = IFELSE_FIELDS.map(f => f[0]);
const freshTune = (opps = ['bench']) => ({ v: 6, mode: 'lessons', depth: 1, opps, fields: TUNE_NAMES, cma: cmaFresh(Array(TUNE_N).fill(0), LAMBDA0), best: { ...IFELSE_DEFAULTS },
  gen: 0, restarts: 0, cand: null, hist: [] });
function tuneState() {
  if (!state.ifelse || state.ifelse.v !== 6) state.ifelse = freshTune(state.ifelse && state.ifelse.opps);   // earlier tunings are replaced
  const st = state.ifelse;
  if (st.fields.join() !== TUNE_NAMES.join()) {                        // values added or removed (cards changed): the rest carry on by name
    const was = Object.fromEntries(st.fields.map((k, i) => [k, st.cma.mean[i]]));
    st.cma = cmaFresh(TUNE_NAMES.map(k => was[k] ?? 0), st.cma.lambda); st.fields = TUNE_NAMES; st.cand = null;
    st.best = tuneDecode(st.cma.mean, st.depth); st.hist.push({ gen: st.gen, mark: 'values changed' });
  }
  if (!st.mode) st.mode = 'lessons';
  st.opps = (st.opps || []).filter(k => TUNE_OPPS().some(([x]) => x === k));
  if (!st.opps.length) st.opps = ['bench'];
  return st;
}
const tuneGames = () => Math.max(20, Math.round(Number($('#tuGames').value) / 2) * 2 || 300);
$('#tuGames').addEventListener('change', () => { $('#tuGames').value = tuneGames(); });   // the box shows the number played
function newGeneration() {
  const st = tuneState(), L = st.cma.lambda;
  // the candidates, then the centre itself (the values the ifelse AI has now) and, after a move, the centre before it:
  // they play the same games (or lessons), only to be measured
  // res[candidate][deal]: its score in that game (1 win, 0.5 draw, 0 loss), null until played
  const G = st.mode === 'lessons' ? lessonBlocks() : tuneGames();      // lessons: one score per block of lessons
  const xs = [...cmaSamples(st.cma), st.cma.mean.slice(), ...(st.prevMean && st.prevMean.length === TUNE_N ? [st.prevMean.slice()] : [])];
  st.cand = { G, xs, res: xs.map(() => Array(G).fill(null)) };
  tuneRunning.clear();
}
/** The games being played now (candidate-deal), not saved: after a pause they are played again. */
const tuneRunning = new Set();
const tuneDone = c => c.res.reduce((n, r) => n + r.filter(x => x !== null).length, 0);
/** The candidate with fewest games done or running and its first deal left, marked as running; null when none is left. */
function tuneNextDeal(c) {
  let i = -1, gi = -1, fewest = Infinity;
  c.res.forEach((r, j) => {
    const free = r.findIndex((x, d) => x === null && !tuneRunning.has(j + '-' + d));
    if (free < 0) return;
    const busy = r.filter((x, d) => x !== null || tuneRunning.has(j + '-' + d)).length;
    if (busy < fewest) { fewest = busy; i = j; gi = free; }
  });
  if (i < 0) return null;
  tuneRunning.add(i + '-' + gi);
  return [i, gi];
}
function tuneJob() {
  const st = tuneState(), c = st.cand;
  if (st.mode === 'lessons') return lessonJob(st, c);
  if (!c) return null;
  const pick = tuneNextDeal(c);
  if (!pick) return null;
  const [i, gi] = pick, m = gi % 3 === 2 ? 'S' : 'X', seat = Math.floor(gi / 3) % 2;
  const mine = { kind: 'ifelse', cfg: { ...ifelseFull(tuneDecode(c.xs[i], st.depth)), depth: st.depth } };
  const opp = tuneOppSpec(st.opps[Math.floor(gi / 12) % st.opps.length], st.depth);   // every candidate gets the same schedule
  return { key: 'tune' + st.gen + '-' + i + '-' + gi, i, gi, seat, gen: st.gen, specs: seat === 0 ? [mine, opp] : [opp, mine],
    seed: st.gen * 100003 + gi,                                                // game gi deals the same cards for every candidate
    decks: MATCHUPS[m].pairs[(st.gen * Math.ceil(c.G / 6) + Math.floor(gi / 6)) % MATCHUPS[m].pairs.length] };   // later generations go on through the pairs
}
function tuneResult(r, job) {
  if (job.lesson) return lessonResult(r, job);
  tuneScore(job, r.winner === job.seat ? 1 : r.winner === 'draw' ? 0.5 : 0);
}
/** A candidate's score for one deal (a game, or a block of lessons); the generation ends when the scores are in. */
function tuneScore(job, score) {
  const st = tuneState(), c = st.cand;
  if (!c || job.gen !== st.gen) return;
  tuneRunning.delete(job.i + '-' + job.gi);
  c.res[job.i][job.gi] = score;
  // every game started, half the cores or more idle, and the unfinished games in at most 5% of the deals: the generation
  // ends without those deals (dropped for every candidate alike, so all still played the same deals) instead of the
  // cores waiting for a few long games (games only: blocks of lessons are short)
  const left = c.G * c.res.length - tuneDone(c), cores = tune.pool ? tune.pool.size : 1;
  const open = c.res[0].filter((_, d) => c.res.some(r => r[d] === null)).length;
  if (left === 0 || (st.mode !== 'lessons' && left === tuneRunning.size && left <= Math.max(1, Math.floor(cores / 2)) && open <= Math.max(1, Math.floor(c.G * 0.05)))) finishGeneration();
  else renderTuneStatus();
}
function finishGeneration() {
  const st = tuneState(), c = st.cand, L = st.cma.lambda, gen = st.gen;
  const deals = c.res[0].map((_, d) => d).filter(d => c.res.every(r => r[d] !== null));   // the deals every candidate finished
  const all = c.res.map(r => deals.reduce((a, d) => a + r[d], 0) / Math.max(1, deals.length)), rates = all.slice(0, L), centre = all[L], prev = all[L + 1];
  if (tuneRunning.size && tune.pool) tune.pool.cancel(job => job.gen === gen);   // the dropped games stop at once
  tuneRunning.clear();
  // the last move made the centre worse (the centre before it scored more in the same games or lessons): back to it, smaller steps.
  // Else the centre moves only when the better half of the candidates beat it; else it stays and the steps get smaller.
  const back = prev != null && prev > centre;
  const half = rates.slice().sort((a, b) => b - a).slice(0, Math.floor(L / 2)), better = !back && half.reduce((a, b) => a + b, 0) / half.length > centre;
  if (back) { st.cma.mean = c.xs[L + 1].slice(); st.cma.sigma *= 0.9; st.prevMean = null; }
  else if (better) { st.prevMean = st.cma.mean.slice(); cmaUpdate(st.cma, c.xs.slice(0, L), rates); }
  else { st.cma.sigma *= 0.9; st.prevMean = null; }
  st.best = tuneDecode(st.cma.mean, st.depth);
  const avg = rates.reduce((a, b) => a + b, 0) / rates.length, top = Math.max(...rates);
  st.hist.push({ gen: st.gen, avg, top, centre, prev, back, kept: !better && !back, lambda: L, sigma: st.cma.sigma, deals: deals.length });
  if (st.hist.length > 2000) st.hist.splice(0, st.hist.length - 2000);
  // settled (a tiny step size) → restart around the centre with twice the candidates. A generation average that stops
  // rising is not a reason: with a few hundred games per candidate it stalls by luck, and a restart throws away the step sizes learned.
  if (st.cma.sigma < 0.02) {
    st.restarts++;
    st.cma = cmaFresh(st.cma.mean, Math.min(40, st.cma.lambda * 2));
    st.hist.push({ gen: st.gen, mark: `restart ${st.restarts} · ${st.cma.lambda} candidates` });
  }
  st.gen++; st.cand = null;
  if (st.mode === 'lessons') lessonsAfterRound(st);
  else if (tune.running) newGeneration();
  save(); renderTune();
}
function startTune() {
  if (manual) { reportError('Stop the network test first: only one thing runs at a time.'); return; }
  if (Object.keys(trainings).length) stopAllTraining();
  if (tour.running) pauseTournament();
  const st = tuneState();
  tuneRunning.clear(); strengthRunning.clear();                             // games cut off by a pause are played again
  if ((!st.cand || !st.cand.res) && st.mode !== 'lessons') newGeneration();   // lessons: the first job starts the round
  tune.running = true;
  const onFail = (job, msg) => {
    if (job && job.lesson === 'strength') strengthRunning.delete(job.k);
    else if (job && job.gen === tuneState().gen) tuneRunning.delete(job.i + '-' + job.gi);
    reportError('A tuning game failed: ' + msg);
  };
  tune.pool = new Pool(Math.max(1, Math.min(32, Number($('#tuThreads').value) || 1)), Object.fromEntries(NETS.map(n => [n.id, playable(netData[n.id])])), tuneJob, tuneResult, onFail);
  if (st.mode === 'lessons' && st.cand) tune.pool.setInit([{ type: 'lessons', lessons: LESSONS.list }]);
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
$('#tuDepth').addEventListener('change', () => setTuneDepth(Number($('#tuDepth').value)));
$('#tuMode').addEventListener('change', () => {
  const st = tuneState();
  if (tune.running) pauseTune();
  st.mode = $('#tuMode').value; st.cand = null; tuneRunning.clear(); st.hist.push({ gen: st.gen, mark: st.mode === 'lessons' ? 'lessons' : 'games' });
  save(); renderTune();
});
$('#tuLessons').addEventListener('change', () => {
  const st = tuneState();
  if (tune.running) pauseTune();
  st.lessonN = Math.max(100, Math.round(Number($('#tuLessons').value) || 1000)); st.cand = null; save(); renderTune();
});

/** A new tuning depth: the generation under way starts again; the search itself carries on. */
function setTuneDepth(d) {
  const st = tuneState(), was = tune.running;
  if (st.depth === d) return;
  if (was) pauseTune();
  st.depth = d; st.cand = null; st.best = tuneDecode(st.cma.mean, d);
  st.hist.push({ gen: st.gen, mark: 'depth ' + d });
  save();
  if (was) startTune(); else renderTune();
}

/* ---------- "Make this the Benchmark": a check match against the game's Benchmark at the tuning depth ---------- */
const check = { pool: null, run: null };
/** The values the game would get: the centre, looking as far ahead as the game's Benchmark (the check match plays them at the tuning depth). */
const checkValues = () => { const v = { ...ifelseFull(tuneState().best), depth: BENCH_VALUES.depth }; return Object.fromEntries(Object.keys(v).filter(k => k in BENCH_VALUES || k in IFELSE_DEFAULTS || k === 'depth').map(k => [k, v[k]])); };
function renderCheck() {
  const r = check.run || (tuneState().lastCheck || null);
  $('#tuCheck').textContent = check.pool ? 'Stop the check' : 'Make this the Benchmark';
  if (!r) { $('#tuCheckStatus').textContent = 'The centre plays the Benchmark, both at the tuning depth; only a clear win gives a file for the game.'; return; }
  const n = r.w + r.l + r.d, v = verdict(r.w, r.l);
  $('#tuCheckStatus').textContent = `${check.pool ? 'Checking' : 'Last check'} (generation ${r.gen + 1}): ${n}/${r.N} games, won ${r.w}, lost ${r.l}, drawn ${r.d}`
    + (n ? ` (${tpct((r.w + r.d / 2) / n)})` : '') + (n === r.N || !check.pool ? ` · ${v === 2 ? 'clearly better than the Benchmark: file downloaded' : v === 1 ? 'probably better, not clearly: no file' : v <= -1 ? 'worse than the Benchmark: no file' : 'not clearly better: no file'}` : '');
}
function checkJob() {
  const r = check.run;
  if (!r || r.started >= r.N) return null;
  const j = r.started++, seat = j % 2, mine = { kind: 'ifelse', cfg: { ...r.values, depth: r.depth } }, opp = { kind: 'bench', depth: r.depth };
  return { key: 'check' + j, j, seat, specs: seat === 0 ? [mine, opp] : [opp, mine], decks: scheduledDecks(j), seed: 7000003 + Math.floor(j / 2) };
}
function checkResult(res, job) {
  const r = check.run;
  if (!r) return;
  if (res.winner === job.seat) r.w++; else if (res.winner === 'draw') r.d++; else r.l++;
  if (r.w + r.l + r.d >= r.N) finishCheck(); else renderCheck();
}
function finishCheck() {
  const r = check.run;
  stopCheck();
  tuneState().lastCheck = r; save();
  if (verdict(r.w, r.l) === 2) {
    const name = `Benchmark from ifelse gen ${r.gen + 1}`;
    const blob = new Blob([JSON.stringify({ kind: 'benchmark', name, values: r.values, check: { games: r.N, won: r.w, lost: r.l, drawn: r.d } }, null, 1)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = `${name}.json`;
    document.body.appendChild(a); a.click(); a.remove();
  }
  renderCheck();
}
function stopCheck() { if (check.pool) check.pool.stop(); check.pool = null; }
$('#tuCheck').addEventListener('click', () => {
  if (check.pool) { stopCheck(); check.run = null; renderCheck(); return; }
  if (manual) { reportError('Stop the network test first: only one thing runs at a time.'); return; }
  if (tune.running) pauseTune();
  if (Object.keys(trainings).length) stopAllTraining();
  if (tour.running) pauseTournament();
  const N = Math.max(20, Math.round(Number($('#tuCheckN').value) / 2) * 2 || 200);
  check.run = { gen: tuneState().gen, N, started: 0, w: 0, l: 0, d: 0, values: checkValues(), depth: tuneState().depth };
  check.pool = new Pool(Math.max(1, Math.min(32, Number($('#tuThreads').value) || 1)), Object.fromEntries(NETS.map(n => [n.id, playable(netData[n.id])])), checkJob, checkResult,
    (job, msg) => { if (check.run) check.run.started--; reportError('A check game failed: ' + msg); });
  renderCheck();
});
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
  st.opps = opps; st.cand = null;
  const last = st.hist[st.hist.length - 1], mark = { gen: st.gen, mark: 'vs ' + opps.map(tuneOppName).join(', ') };
  if (last && last.mark) st.hist[st.hist.length - 1] = mark; else st.hist.push(mark);
  save();
  if (was) startTune(); else renderTune();
}
$('#tuThreads').addEventListener('change', () => { if (tune.pool) tune.pool.resize(Math.max(1, Math.min(32, Number($('#tuThreads').value) || 1))); });
const tpct = v => (v == null || !Number.isFinite(v) ? '–' : Math.round(v * 100) + '%');
function renderTuneStatus() {
  const st = tuneState(), c = st.cand, last = [...st.hist].reverse().find(e => !e.mark);
  const done = c && c.res ? tuneDone(c) : 0, total = c && c.res ? c.G * c.res.length : 0;
  const lessons = st.mode === 'lessons', making = lessons && LESSONS.need > 0;
  $('#tuStatus').textContent = (tune.running ? (making ? 'Making lessons' : 'Tuning') : st.gen || c ? 'Paused' : 'Not started') +
    (lessons ? ` · ${LESSONS.list.length} lessons` + (LESSONS.need ? `, making ${LESSONS.need} new` : '') + (st.strength ? `, games against the opponents ${st.strength.res.filter(x => x !== null).length}/${STRENGTH_GAMES}` : '') : '') +
    ` · generation ${st.gen + 1} · ${st.cma.lambda} candidates` + (c ? ` · ${done}/${total} ${lessons ? 'blocks of lessons' : 'games'}` : '') +
    (last ? ` · last generation: the ifelse AI ${tpct(last.centre)}, candidates' average ${tpct(last.avg)}, best candidate ${tpct(last.top)}` : '') +
    ` · step size ${st.cma.sigma.toFixed(3)}` + (st.restarts ? ` · ${st.restarts} restart${st.restarts > 1 ? 's' : ''}` : '');
}
function renderTune() {
  const st = tuneState();
  $('#tuOpps').innerHTML = '<span class="tuoppl">Opponents</span>' + TUNE_OPPS().map(([k, name]) =>
    `<label class="tuopp"><input type="checkbox" value="${k}" ${st.opps.includes(k) ? 'checked' : ''}> ${esc(name)}</label>`).join('')
    + `<span class="note">${st.mode === 'lessons' ? 'They play the centre in the games that make lessons and in the games every 10th round, shared equally' : 'Games are shared equally among them'}; at least one.</span>`;
  for (const b of $('#tuOpps').querySelectorAll('input')) b.addEventListener('change', () => {
    const on = [...$('#tuOpps').querySelectorAll('input:checked')].map(x => x.value);
    if (!on.length) { b.checked = true; return; }
    setTuneOpps(on);
  });
  $('#tuStart').disabled = tune.running; $('#tuPause').disabled = !tune.running;
  $('#tuDepth').value = String(st.depth);
  $('#tuMode').value = st.mode; $('#tuLessons').value = lessonTarget();
  for (const el of document.querySelectorAll('.tugames')) el.hidden = st.mode === 'lessons';
  for (const el of document.querySelectorAll('.tulessons')) el.hidden = st.mode !== 'lessons';
  renderCheck();
  $('#tuStart').textContent = st.gen || st.cand ? 'Resume' : 'Start';
  renderTuneStatus();
  // the chart: per generation, the candidates' average win rate (line) and the best candidate's (dot)
  const h = st.hist, W = 1200, H = 300, l = 60, r = 44, t = 14, b = 34, pw = W - l - r, ph = H - t - b;
  const gens = h.filter(e => !e.mark), n = Math.max(1, gens.length - 1);
  // lessons: grades differ by fractions of a point, so the left scale zooms to them; games won against the Benchmark
  // use their own 0-100% scale on the right
  const lessonsMode = st.mode === 'lessons', vals = gens.flatMap(e => [e.avg, e.top, e.centre]).filter(Number.isFinite);
  let lo = 0, hi = 1;
  if (lessonsMode && vals.length) { const a = Math.min(...vals), b = Math.max(...vals), pad = Math.max(0.002, (b - a) * 0.15); lo = Math.max(0, a - pad); hi = Math.min(1, b + pad); }
  const X = i => l + pw * (gens.length < 2 ? 0.5 : i / n), Y = v => t + ph * (1 - (v - lo) / (hi - lo)), YB = v => t + ph * (1 - v);
  let svg = `<rect class="plot" x="${l}" y="${t}" width="${pw}" height="${ph}"></rect>`;
  const dec = hi - lo < 0.02 ? 2 : hi - lo < 0.2 ? 1 : 0;
  for (let k = 0; k <= 4; k++) { const v = lo + (hi - lo) * k / 4; svg += `<line class="grid${!lessonsMode && k === 2 ? ' mid' : ''}" x1="${l}" x2="${W - r}" y1="${Y(v)}" y2="${Y(v)}"></line><text class="ylab" x="${l - 8}" y="${Y(v) + 5}">${(v * 100).toFixed(dec)}%</text>`; }
  if (lessonsMode && gens.some(e => e.bench != null)) for (const v of [0, 0.5, 1]) svg += `<text class="ylab benchlab" x="${W - r + 4}" y="${YB(v) + 5}">${v * 100}%</text>`;
  if (!gens.length) svg += `<text class="empty" x="${l + pw / 2}" y="${t + ph / 2}">No generations yet.</text>`;
  else {
    let i = 0;
    for (const e of h) {
      if (!e.mark) { i++; continue; }
      const x = X(Math.max(0, i - 0.5)), right = x > W - r - 200;
      svg += `<line class="tumark" x1="${x}" x2="${x}" y1="${t}" y2="${t + ph}"></line><text class="tumarkt" x="${right ? x - 4 : x + 4}" y="${t + 14}" text-anchor="${right ? 'end' : 'start'}">${esc(e.mark)}</text>`;
    }
    svg += `<polyline class="tuavg" points="${gens.map((e, k) => `${X(k)},${Y(e.avg)}`).join(' ')}"></polyline>`;
    const cen = gens.map((e, k) => (e.centre == null ? null : `${X(k)},${Y(e.centre)}`)).filter(Boolean);
    if (cen.length) svg += `<polyline class="tubest" points="${cen.join(' ')}"></polyline>`;
    svg += gens.map((e, k) => (e.bench == null ? '' : `<rect class="tubench" x="${X(k) - 5}" y="${YB(e.bench) - 5}" width="10" height="10"><title>Generation ${e.gen + 1}: the ifelse AI won ${tpct(e.bench)} of ${STRENGTH_GAMES} games against the opponents ticked (looking 1 move ahead)</title></rect>`)).join('');
    svg += gens.map((e, k) => `<circle class="tucand acc" cx="${X(k)}" cy="${Y(e.top)}" r="3.5"><title>Generation ${e.gen + 1}: ifelse AI ${tpct(e.centre)}${e.back ? ` (the centre before scored ${tpct(e.prev)}: went back to it)` : e.kept ? ' (better half not better: centre kept)' : ''}, candidates' average ${tpct(e.avg)}, best candidate ${tpct(e.top)} (${e.lambda} candidates${e.deals ? `, ${e.deals} games each` : ''})</title></circle>`).join('');
    svg += `<text class="xlab" x="${l}" y="${H - 10}">generation ${gens[0].gen + 1}</text><text class="xlab end" x="${W - r}" y="${H - 10}">generation ${gens[gens.length - 1].gen + 1}</text>`;
  }
  $('#tuChart').innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Win rates by generation">${svg}</svg>
    <div class="tulegend"><span class="lg best"></span>the ifelse AI itself (the centre) <span class="lg avg"></span>candidates' average <span class="lg acc"></span>best candidate${st.mode === 'lessons' ? ' <span class="lg bench"></span>games won against the opponents ticked (every 10th round, right scale)' : ''}</div>`;
  const fmt = v => (Number.isInteger(v) ? String(v) : Math.abs(v) >= 10 ? v.toFixed(1) : v.toFixed(3));
  $('#tuTable').innerHTML = `<table class="tutable"><thead><tr><th>Value</th><th>Start</th><th>ifelse AI (centre)</th></tr></thead><tbody>${
    IFELSE_FIELDS.map(([k, text]) => { const d = IFELSE_DEFAULTS[k], v = st.best[k] ?? d, ch = Math.abs(v - d) > 1e-9;
      return `<tr${ch ? ' class="ch"' : ''}><td>${esc(text)}</td><td>${fmt(d)}</td><td>${fmt(v)}${ch ? ` <span class="tud ${v > d ? 'up' : 'down'}">${v > d ? '▲' : '▼'}</span>` : ''}</td></tr>`; }).join('')
  }</tbody></table>`;
}


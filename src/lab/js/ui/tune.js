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
    const z = /^w\d$/.test(k) && Number(k.slice(1)) > depth ? 0 : x[i];
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

const freshTune = (opps = ['bench']) => ({ v: 5, depth: 1, opps, cma: cmaFresh(Array(TUNE_N).fill(0), LAMBDA0), best: { ...IFELSE_DEFAULTS },
  gen: 0, restarts: 0, cand: null, hist: [] });
function tuneState() {
  const old = state.ifelse;
  if (old && old.v === 4 && old.cma && old.cma.mean && old.cma.mean.length === TUNE_N) {   // a tuning of the full form: its centre carries on
    state.ifelse = { ...freshTune(old.opps), depth: old.depth, gen: old.gen, restarts: old.restarts, best: old.best, lastCheck: old.lastCheck,
      cma: cmaFresh(old.cma.mean, LAMBDA0), hist: [...(old.hist || []), { gen: old.gen, mark: 'one step size per value' }] };
  }
  if (!state.ifelse || state.ifelse.v !== 5) state.ifelse = freshTune(state.ifelse && state.ifelse.opps);   // earlier tunings are replaced
  const st = state.ifelse;
  st.opps = (st.opps || []).filter(k => TUNE_OPPS().some(([x]) => x === k));
  if (!st.opps.length) st.opps = ['bench'];
  return st;
}
const tuneGames = () => Math.max(20, Math.round(Number($('#tuGames').value) / 2) * 2 || 300);
function newGeneration() {
  const st = tuneState(), L = st.cma.lambda;
  // the candidates, then the centre itself (the values the ifelse AI has now): it plays the same games, only to be measured
  st.cand = { G: tuneGames(), xs: [...cmaSamples(st.cma), st.cma.mean.slice()], w: Array(L + 1).fill(0), n: Array(L + 1).fill(0), started: Array(L + 1).fill(0) };
}
function tuneJob() {
  const st = tuneState(), c = st.cand;
  if (!c) return null;
  let i = -1;
  c.started.forEach((s, j) => { if (s < c.G && (i < 0 || s < c.started[i])) i = j; });   // the candidate with fewest games started
  if (i < 0) return null;
  const gi = c.started[i]++, m = gi % 3 === 2 ? 'S' : 'X', seat = Math.floor(gi / 3) % 2;
  const mine = { kind: 'ifelse', cfg: { ...ifelseFull(tuneDecode(c.xs[i], st.depth)), depth: st.depth } };
  const opp = tuneOppSpec(st.opps[Math.floor(gi / 12) % st.opps.length], st.depth);   // every candidate gets the same schedule
  return { key: 'tune' + st.gen + '-' + i + '-' + gi, i, seat, gen: st.gen, specs: seat === 0 ? [mine, opp] : [opp, mine],
    seed: st.gen * 100003 + gi,                                                // game gi deals the same cards for every candidate
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
  const st = tuneState(), c = st.cand, all = c.w.map((w, i) => w / c.n[i]), L = st.cma.lambda, rates = all.slice(0, L), centre = all[L];
  cmaUpdate(st.cma, c.xs.slice(0, L), rates);
  st.best = tuneDecode(st.cma.mean, st.depth);
  const avg = rates.reduce((a, b) => a + b, 0) / rates.length, top = Math.max(...rates);
  st.hist.push({ gen: st.gen, avg, top, centre, lambda: L, sigma: st.cma.sigma });
  if (st.hist.length > 2000) st.hist.splice(0, st.hist.length - 2000);
  // settled (a tiny step size) → restart around the centre with twice the candidates. A generation average that stops
  // rising is not a reason: with a few hundred games per candidate it stalls by luck, and a restart throws away the step sizes learned.
  if (st.cma.sigma < 0.02) {
    st.restarts++;
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
$('#tuDepth').addEventListener('change', () => setTuneDepth(Number($('#tuDepth').value)));
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
  const done = c ? c.n.reduce((a, b) => a + b, 0) : 0, total = c ? c.G * c.xs.length : 0;
  $('#tuStatus').textContent = (tune.running ? 'Tuning' : st.gen || c ? 'Paused' : 'Not started') +
    ` · generation ${st.gen + 1} · ${st.cma.lambda} candidates` + (c ? ` · ${done}/${total} games` : '') +
    (last ? ` · last generation: the ifelse AI ${tpct(last.centre)}, candidates' average ${tpct(last.avg)}, best candidate ${tpct(last.top)}` : '') +
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
  $('#tuDepth').value = String(st.depth);
  renderCheck();
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
    svg += `<polyline class="tuavg" points="${gens.map((e, k) => `${X(k)},${Y(e.avg)}`).join(' ')}"></polyline>`;
    const cen = gens.map((e, k) => (e.centre == null ? null : `${X(k)},${Y(e.centre)}`)).filter(Boolean);
    if (cen.length) svg += `<polyline class="tubest" points="${cen.join(' ')}"></polyline>`;
    svg += gens.map((e, k) => `<circle class="tucand acc" cx="${X(k)}" cy="${Y(e.top)}" r="3.5"><title>Generation ${e.gen + 1}: ifelse AI ${tpct(e.centre)}, candidates' average ${tpct(e.avg)}, best candidate ${tpct(e.top)} (${e.lambda} candidates)</title></circle>`).join('');
    svg += `<text class="xlab" x="${l}" y="${H - 10}">generation ${gens[0].gen + 1}</text><text class="xlab end" x="${W - r}" y="${H - 10}">generation ${gens[gens.length - 1].gen + 1}</text>`;
  }
  $('#tuChart').innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Win rates by generation">${svg}</svg>
    <div class="tulegend"><span class="lg best"></span>the ifelse AI itself (the centre) <span class="lg avg"></span>candidates' average <span class="lg acc"></span>best candidate</div>`;
  const fmt = v => (Number.isInteger(v) ? String(v) : Math.abs(v) >= 10 ? v.toFixed(1) : v.toFixed(3));
  $('#tuTable').innerHTML = `<table class="tutable"><thead><tr><th>Value</th><th>Start</th><th>ifelse AI (centre)</th></tr></thead><tbody>${
    IFELSE_FIELDS.map(([k, text]) => { const d = IFELSE_DEFAULTS[k], v = st.best[k] ?? d, ch = Math.abs(v - d) > 1e-9;
      return `<tr${ch ? ' class="ch"' : ''}><td>${esc(text)}</td><td>${fmt(d)}</td><td>${fmt(v)}${ch ? ` <span class="tud">${v > d ? '▲' : '▼'}</span>` : ''}</td></tr>`; }).join('')
  }</tbody></table>`;
}


/* ---------- "Test now": 100 games against the Benchmark with the network as it is ---------- */

function testNow(id) {
  if (manual && manual.id === id) { finishManual(); return; }                   // the button turns into "Stop test"
  if (Object.keys(trainings).length || tour.running || manual) { reportError('Pause training or the tournament first: only one thing runs at a time.'); return; }
  const rec = state.training[id], m = manual = { id, opp: testOppSpec(), vs: testOppName(), total: 100, queued: 0, done: 0, won: 0, lost: 0, drawn: 0, fails: 0, pool: null };

  notice = '';
  const nextJob = () => {
    if (manual !== m || m.queued >= m.total) return null;
    const g = m.queued++, netSide = g % 2, specs = [];
    specs[netSide] = { kind: 'net', net: 'manual', play: { replies: false, explore: 0 } };   // playing alone, like every test
    specs[1 - netSide] = m.opp;
    return { key: 'manual' + g, kind: 'test', netSide, specs, decks: scheduledDecks(g), seed: 9000001 + Math.floor(g / 2) };
  };
  const onResult = (r, job) => {
    if (manual !== m) return;
    m.fails = 0; m.done++;
    if (r.winner === job.netSide) m.won++; else if (r.winner === 'draw') m.drawn++; else m.lost++;
    if (m.done >= m.total) { rec.tests.push({ games: rec.games + rec.teacherGames, won: m.won, lost: m.lost, drawn: m.drawn, n: m.total, mode: 'alone', manual: true, vs: m.vs }); finishManual(); return; }
    renderTrainingSoon();
  };
  const onFail = (job, message) => {
    if (manual !== m) return;
    rec.failed = (rec.failed || 0) + 1; rec.lastError = message;
    if (job) m.queued--;                                                         // replaced by a new game
    if (++m.fails >= 10) { reportError('Test stopped: 10 background games in a row failed. Last error: ' + message); finishManual(); return; }
    renderTrainingSoon();
  };
  m.pool = new Pool(trainingSettings().threads, { manual: netData[id], ...(netData.testopp ? { testopp: playable(netData.testopp) } : {}) }, nextJob, onResult, onFail);
  renderTraining();
}
function finishManual() {
  if (!manual) return;
  manual.pool.stop();
  manual = null;
  save();
  renderTraining();
}

/* ---------- training page ---------- */

/** All tests of one network as a framed chart: win rate against the Benchmark by games played against itself. */
/**
 * One chart per AI: win rate in the tests against the Benchmark (solid lines) and how well each network
 * predicts the winner of new games (dashed lines), all in percent. Moving the pointer over it shows a vertical
 * line and every value at that point.
 */
function chart(n, r, firstTestAt) {
  const variants = SIZE_VARIANTS(n), tests = r.tests;
  const rate = testRate;
  const own = tests.filter(t => !t.net), series = [], hidden = new Set((state.chartHidden || {})[n.id] || []);
  const pts = list => list.map(t => ({ x: t.games, y: rate(t), big: t.n >= 100, counts: testCounts(t),
    note: `${t.won}–${t.lost}${t.drawn ? ', ' + t.drawn + ' drawn' : ''} in ${t.n || 20} games${t.manual ? ' (Test now)' : ''}` }));
  series.push({ label: 'wins, playing alone', cls: 'c0', group: 'Vanilla', pts: pts(own.filter(t => t.mode === 'alone')) });
  for (const v of variants) series.push({ label: `${v.label}: wins`, cls: v.cls, group: v.label, pts: pts(tests.filter(t => t.net === v.key)) });
  const log = r.predLog || [];
  const pred = key => log.filter(e => e[key] !== null && e[key] !== undefined).map(e => ({ x: e.games, y: e[key], note: 'of positions in new games' }));
  series.push({ label: 'Vanilla: predicts the winner', cls: 'c0 dash', group: 'Vanilla', pts: pred('main') });
  for (const v of variants) series.push({ label: `${v.label} (${v.hidden.join(', ')} nodes): predicts`, cls: v.cls + ' dash', group: v.label, pts: pred(v.key) });
  // the main network's step size, on the right axis (0 to the start step): known from the moment it was first recorded
  LR_AXIS = Math.max(LR_START, ...(r.lrLog || []).map(e => e.r));
  const rlog = (r.lrLog || []).map((e, i) => ({ ...e, i })).sort((p, q) => p.g - q.g || p.i - q.i)
    .filter((e, i, a) => i + 1 === a.length || a[i + 1].g !== e.g);                  // in order of games; the last change at each count wins
  const rateAt = g => { let v = null; for (const e of rlog) if (e.g <= g) v = e.r; return v; };
  series.push({ label: 'step size (right axis)', cls: 'rate', rateLine: true,
    pts: rlog.length ? own.filter(q => !q.manual && rateAt(q.games) !== null).map(q => ({ x: q.games, y: rateAt(q.games) / LR_AXIS, txt: fmtRate(rateAt(q.games)), note: '' })) : [] });

  const W = 1200, H = 360, left = 58, right = 84, top = 16, bottom = 44, pw = W - left - right, ph = H - top - bottom;
  const y = v => top + ph * (1 - Math.max(0, Math.min(1, v)));
  let body = `<rect class="plot" x="${left}" y="${top}" width="${pw}" height="${ph}"></rect>`;
  for (const v of [0, 0.25, 0.5, 0.75, 1])
    body += `<line class="grid${v === 0.5 ? ' mid' : ''}" x1="${left}" x2="${W - right}" y1="${y(v)}" y2="${y(v)}"></line><text class="ylab" x="${left - 8}" y="${y(v) + 5}">${Math.round(v * 100)}%</text>`;
  // the right axis: only the values the step size can take (halvings from the top, down to the floor);
  // every one gets a tick, and a label where it does not crowd the one below it (the floor is always labelled)
  { let lastY = Infinity;
    const ticks = []; for (let r = LR_AXIS; r >= LR_FLOOR * 0.9999; r /= 2) ticks.unshift(r);   // bottom up, so the floor is labelled
    for (const r of ticks) {
      const yy = y(r / LR_AXIS);
      body += `<line class="tick rate" x1="${W - right}" x2="${W - right + 5}" y1="${yy}" y2="${yy}"></line>`;
      if (lastY - yy >= 14) { body += `<text class="ylab rate" x="${W - right + 8}" y="${yy + 5}">${r.toPrecision(2).replace(/0+$/, '')}</text>`; lastY = yy; }
    } }
  const shown = series.filter(sr => sr.pts.length), all = shown.flatMap(sr => sr.pts);
  // each win-rate line gets its two weighted averages (over the tests that count); they show and hide with it
  for (const sr of shown) {
    sr.group = sr.group || sr.label;
    if (sr.cls.includes('dash') || sr.rateLine) continue;
    const e = emaLine(sr.pts.filter(p => p.counts).sort((a, b) => a.x - b.x));
    sr.fast = e.map(q => ({ x: q.x, y: q.fast, note: '' }));
    sr.slow = e.map(q => ({ x: q.x, y: q.slow, note: '' }));
  }
  const visible = shown.filter(sr => !hidden.has(sr.group));
  const periods = r.periods || [], KINDS = PERIOD_KINDS();
  let maxG = 1, shaded = [];
  if (!all.length) {
    body += `<text class="none" x="${left + pw / 2}" y="${top + ph / 2 - 6}">No tests yet.</text><text class="none" x="${left + pw / 2}" y="${top + ph / 2 + 16}">The first comes after ${firstTestAt} games.</text>`;
  } else {
    maxG = Math.max(1, ...all.map(p => p.x));
    const x = g => left + pw * g / maxG;
    // training periods, shaded behind everything: each lasts until the next one starts (or the chart's end)
    periods.forEach((pd, i) => {
      const a = Math.min(pd.g, maxG), b = Math.min(i + 1 < periods.length ? periods[i + 1].g : maxG, maxG);
      if (b <= a || !KINDS[pd.kind]) return;
      body += `<rect class="period" x="${x(a).toFixed(1)}" y="${top}" width="${(x(b) - x(a)).toFixed(1)}" height="${ph}" fill="${KINDS[pd.kind][1]}"></rect>`;
      if (!shaded.includes(pd.kind)) shaded.push(pd.kind);
    });
    // where the test opponent changed: a dashed line, labelled with the new one
    let prevVs = null;
    for (const q of r.tests.filter(q => !q.net && !q.manual)) {
      const vs = q.vs || 'the Benchmark';
      if (prevVs !== null && vs !== prevVs && q.games <= maxG) {
        const xx = x(q.games), right = xx > left + pw - 180;
        body += `<line class="vsmark" x1="${xx.toFixed(1)}" x2="${xx.toFixed(1)}" y1="${top}" y2="${top + ph}"></line><text class="vsmarkt" x="${(right ? xx - 4 : xx + 4).toFixed(1)}" y="${top + 13}" text-anchor="${right ? 'end' : 'start'}">tests vs ${esc(vs)}</text>`;
      }
      prevVs = vs;
    }
    const raw = maxG / 6, mag = Math.pow(10, Math.floor(Math.log10(raw))), step = mag * ([1, 2, 5, 10].find(f => f * mag >= raw) || 10);
    for (let g = 0; g <= maxG; g += step) body += `<text class="xlab" x="${x(g)}" y="${top + ph + 18}">${g}</text>`;   // round-number ticks
    body += `<text class="xttl" x="${left + pw / 2}" y="${H - 6}">${r.teacherGames > 0 ? 'games played (library and its own)' : 'games played'}</text>`;
    const line = (p, cls) => `<polyline class="${cls}" points="${p.map(q => x(q.x).toFixed(1) + ',' + y(q.y).toFixed(1)).join(' ')}"></polyline>`;
    for (const sr of visible) if (sr.slow && sr.slow.length > 1) body += line(sr.slow, `ema slow ${sr.cls}`);   // wide and faint, underneath
    for (const sr of visible) {
      if (sr.rateLine) {                                                      // a step line: flat until the step changes, then a jump
        const e = rlog.filter(q => q.g <= maxG), p = [];
        e.forEach((q, i) => { p.push({ x: q.g, y: q.r / LR_AXIS }); p.push({ x: i + 1 < e.length ? e[i + 1].g : maxG, y: q.r / LR_AXIS }); });
        if (p.length > 1) body += line(p, 'line rate');
        continue;
      }
      const p = sr.pts.slice().sort((a, b) => a.x - b.x);
      body += line(p, `line ${sr.cls}`);
      if (!sr.cls.includes('dash')) for (const q of p)
        body += `<circle class="dot ${sr.cls}${q.big ? ' big' : ''}" cx="${x(q.x).toFixed(1)}" cy="${y(q.y).toFixed(1)}" r="${q.big ? 3.5 : 2.5}"></circle>`;
    }
    for (const sr of visible) if (sr.fast && sr.fast.length > 1) body += line(sr.fast, `ema fast ${sr.cls}`);   // dotted, on top
    body += `<line class="cursor" x1="0" x2="0" y1="${top}" y2="${top + ph}" visibility="hidden"></line>`;
  }
  const groups = [...new Set(shown.map(sr => sr.group))].map(g => { const m = shown.filter(sr => sr.group === g);
    return { g, cls: (m.find(sr => !sr.cls.includes('dash')) || m[0]).cls.replace(' dash', ''), label: m.length > 1 || m[0].group !== m[0].label ? g : m[0].label, many: m.length > 1, avg: m.some(sr => sr.fast) }; });
  const legend = `<p class="legend">${groups.map(G => { const off = hidden.has(G.g);
      return `<span class="li tog${off ? ' off' : ''}" data-g="${esc(G.g)}" role="button" tabindex="0" aria-pressed="${!off}" title="${off ? 'Show' : 'Hide'} ${G.many ? 'these lines' : 'this line'}${G.avg ? ' and the averages' : ''}"><span class="sw ${G.cls}"></span>${G.label}</span>`; }).join('')}</p>`
    + (shaded.length ? `<p class="legend periods">Background, training against: ${shaded.map(k => `<span class="li"><span class="pb" style="background:${KINDS[k][1]}"></span>${KINDS[k][0]}</span>`).join('')}</p>` : '');
  const data = esc(JSON.stringify({ W, H, left, pw, top, ph, maxG, periods: periods.map(p => ({ g: p.g, name: KINDS[p.kind] ? KINDS[p.kind][0] : p.kind })), series: visible.filter(sr => !sr.rateLine).flatMap(sr => [{ label: sr.label, cls: sr.cls, pts: sr.pts },
    ...(sr.fast ? [{ label: sr.label + ' · 9-test average', cls: 'fast ' + sr.cls, pts: sr.fast }, { label: sr.label + ' · 18-test average', cls: 'slow ' + sr.cls, pts: sr.slow }] : [])]) }));
  return `<div class="chartbox"><div class="chartwrap"><svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Win rate in the tests and prediction score over training" data-chart="${data}">${body}</svg><div class="tip" hidden></div></div>${legend}</div>`;
}
/** The pointer over a chart: a vertical line at the nearest test, and a box with every value there. */
const chartHover = {};                         // net id -> the pointer's last position over its chart
function hookChart(svg) {
  const d = JSON.parse(svg.dataset.chart), tip = svg.parentElement.querySelector('.tip'), cursor = svg.querySelector('.cursor');
  const id = svg.closest('.netcard').dataset.id;
  for (const li of svg.closest('.chartbox').querySelectorAll('.legend .li.tog')) {   // a label shows or hides its lines
    const flip = () => {
      const all = state.chartHidden || (state.chartHidden = {}), set = new Set(all[id] || []);
      if (set.has(li.dataset.g)) set.delete(li.dataset.g); else set.add(li.dataset.g);
      all[id] = [...set]; save();
      refreshChart(id);
    };
    li.addEventListener('click', flip);
    li.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); flip(); } });
  }
  if (!cursor) return;
  const xs = [...new Set(d.series.flatMap(sr => sr.pts.map(p => p.x)))].sort((a, b) => a - b);
  const show = clientX => {
    if (!xs.length) return;
    const box = svg.getBoundingClientRect(), sx = (clientX - box.left) * d.W / box.width;
    const g = (sx - d.left) / d.pw * d.maxG, near = xs.reduce((a, b) => (Math.abs(b - g) < Math.abs(a - g) ? b : a), xs[0]);
    const cx = d.left + d.pw * near / d.maxG;
    cursor.setAttribute('x1', cx); cursor.setAttribute('x2', cx); cursor.setAttribute('visibility', 'visible');
    const rows = d.series.map(sr => { const p = sr.pts.find(q => q.x === near); return p ? `<div class="row"><span class="sw ${sr.cls}"></span><span>${sr.label}</span><b>${p.txt || Math.round(p.y * 100) + '%'}</b><span class="muted">${p.note || ''}</span></div>` : ''; }).join('');
    const pd = [...d.periods].reverse().find(p => p.g <= near);
    tip.innerHTML = `<div class="head">after ${near} games${pd ? ` · training against ${pd.name}` : ''}</div><div class="rows">${rows}</div>`;
    tip.hidden = false;
    const px = cx / d.W * box.width, right = px > box.width / 2;
    tip.style.left = right ? '' : (px + 14) + 'px';
    tip.style.right = right ? (box.width - px + 14) + 'px' : '';
    tip.style.top = '8px';
  };
  svg.addEventListener('mousemove', ev => { chartHover[id] = ev.clientX; show(ev.clientX); });
  svg.addEventListener('mouseleave', () => { delete chartHover[id]; cursor.setAttribute('visibility', 'hidden'); tip.hidden = true; });
  if (chartHover[id] !== undefined) show(chartHover[id]);
}

let renderPending = false;
function renderTrainingSoon() {
  if (renderPending) return;
  renderPending = true;
  setTimeout(() => { renderPending = false; updateTrainingStats(); }, 1000);
}

/** Size check on (at any time): its two networks start as grown copies of the AI's network as it is now, at its
 *  current step size. Off: they and their results are removed. A running training restarts around the change. */
async function setSizeCheck(id, on) {
  const n = NETS.find(x => x.id === id), rec = state.training[id];
  if (!on && !(await askYes('Turn the size check off?', 'Its two networks and their results are removed.', 'Turn off'))) { renderTraining(); return; }
  const was = !!trainings[id];
  if (was) await stopTraining(id);                                               // the learners hold the networks: stop, change, go on
  if (on) {
    for (const v of SIZE_VARIANTS(n)) { netData[copyId(id, v.key)] = net3Grow(netData[id], v.hidden); saveNet(copyId(id, v.key)); }
    const lr = JSON.parse(JSON.stringify(lrOf(rec)));
    rec.size = { on: true, from: rec.games + rec.teacherGames, nets: Object.fromEntries(SIZE_VARIANTS(n).map(v => [v.key, { acc: null, fit: null, lr: { ...lr } }])) };
  } else {
    rec.size = { on: false };
    rec.tests = rec.tests.filter(t => !t.net);
    for (const e of rec.predLog || []) for (const v of SIZE_VARIANTS(n)) delete e[v.key];
    for (const v of SIZE_VARIANTS(n)) { delete netData[copyId(id, v.key)]; deleteNet(copyId(id, v.key)); }
  }
  save();
  if (was) startTraining(id); else renderTraining();
}


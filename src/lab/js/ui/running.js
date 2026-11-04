/* =====================================================================
   Running games in the background
   ===================================================================== */

const MAX_PENDING = 12000;   // positions waiting to be learned from; above this, new training games wait for the learners

/**
 * A pool of game workers. Each takes one job at a time from `nextJob` and hands the result to `onResult`;
 * a game that crashes is handed to `onFail` (never silently dropped), so callers can replace it.
 */
class Pool {
  constructor(size, nets, nextJob, onResult, onFail) {
    this.nextJob = nextJob; this.onResult = onResult; this.onFail = onFail; this.workers = []; this.stopped = false;
    this.nets = nets; this.size = 0;
    this.resize(size);
  }
  addWorker() {
    const w = newWorker();
    w.postMessage({ type: 'nets', nets: this.nets });
    const after = () => { if (w.retiring) this.drop(w); if (!this.stopped) this.feed(); };
    w.onmessage = e => {
      const job = w.job;
      w.job = null;
      if (!this.stopped && job) this.onResult(e.data, job);         // a result with no job waiting for it is ignored
      after();
    };
    w.onerror = e => {
      e.preventDefault();
      const job = w.job;
      w.job = null;
      if (!this.stopped) this.onFail(job, e.message || 'unknown error');
      after();
    };
    this.workers.push(w);
  }
  drop(w) { w.terminate(); this.workers = this.workers.filter(x => x !== w); }
  /** Change the number of game workers. Idle ones are removed at once; busy ones finish their game first. */
  resize(n) {
    this.size = n;
    const live = () => this.workers.filter(w => !w.retiring);
    while (live().length < n) this.addWorker();
    while (live().length > n) {
      const l = live(), w = l.find(x => !x.job) || l[l.length - 1];
      w.retiring = true;
      if (!w.job) this.drop(w);
    }
    this.feed();
  }
  feed() {
    for (const w of this.workers) {
      if (w.job || w.retiring || this.stopped) continue;
      const job = this.nextJob();
      if (!job) continue;
      w.job = job;
      w.postMessage({ type: 'game', key: job.key, specs: job.specs, decks: job.decks, record: !!job.record,
        roundCap: ROUND_CAP, actionCap: ACTION_CAP, search: job.search || 0,
        replay: job.replay });
    }
  }
  busy() { return this.workers.some(w => w.job); }
  setNets(nets) { this.nets = nets; for (const w of this.workers) w.postMessage({ type: 'nets', nets }); }
  stop() { this.stopped = true; for (const w of this.workers) w.terminate(); this.workers = []; }
}

/** The last message for the person, kept so it survives redraws of the cards. */
let notice = '';
function reportError(text) {
  notice = text;
  const el = $('#tStatus');
  if (el) el.textContent = text;
  const st = $('#status');
  if (!$('#tourPage').hidden && st) st.textContent = text;
}

/** A random matchup and seating: [faction of seat 0, faction of seat 1]. */

/* =====================================================================
   Training. Both networks can train at the same time. "Games at once" is the total number of cores in
   use: it is split evenly between the networks currently training (rebalanced whenever one starts or
   stops), and each network divides its share between learners and game workers. That split moves on
   its own: when positions pile up faster than the learners can learn from them, a game worker becomes
   a learner; when the learners run short of positions, a learner becomes a game worker again.
   ===================================================================== */

const trainings = {};        // net id -> { learners (id -> { w, pending, dropped, leaving }), share, want, pool, phase, testing, pending, fails, cfg, lastSave, nextJob, onResult, onFail } or absent
const stoppingIds = {};      // net id -> promise, while its stop is finishing (the last weights are on their way)
let manual = null;           // a "Test now" run: { id, pool, total, queued, done, won, lost, drawn, fails }

function trainingSettings() {
  const num = (sel, fallback) => { const v = Number($(sel).value); return Number.isFinite(v) ? v : fallback; };
  return {
    threads: Math.max(1, Math.min(32, num('#tThreads', 1))),
    explore: Math.max(0, Math.min(0.5, num('#tExplore', 5) / 100)),
    uses: Math.max(1, Math.min(50, Math.round(num('#tUses', 8)))),
    evalEvery: Math.max(100, num('#tEvalEvery', 1000)),
    evalGames: Math.max(2, Math.round(num('#tEvalGames', 100) / 2) * 2),
  };
}

/** Give every currently training network an equal share of "Games at once" (at least one learner and one game each). */
function rebalancePools() {
  const ids = Object.keys(trainings);
  if (!ids.length) return;
  const share = Math.max(2, Math.floor(trainingSettings().threads / ids.length));
  for (const id of ids) { trainings[id].share = share; syncLearners(trainings[id]); }
}

/** How full the learners' queues are: 1 means new games wait. */
const loadOf = x => x.pending / MAX_PENDING;
/** As loadOf, also counting what the games still being played will bring (by the recent average per game), so the
 *  queues stop short of their limits instead of overshooting them by a whole round of games. */
const loadAhead = t => {
  const ap = t.avgPos === undefined ? 60 : t.avgPos;                            // before any result: a cautious guess
  return (t.pending + (t.inflight || 0) * ap) / MAX_PENDING;
};
// each learner's hard ceiling, as in the learner code: during a test the learners' lessons are gathered into as
// few learners as can hold them, never into one that would have to throw lessons away
const LEARNER_MAX_POS = 60000;
const LEARNER_MORE = 0.75;                 // queues this full: the learners can't keep up
const LEARNER_FEWER = 1500 / MAX_PENDING;  // queues this empty: the learners are running short
const LEARNER_PAUSE = 3000;                // ms to wait after a change before the next, so the queue can react
const activeLearners = t => Object.values(t.learners).filter(l => !l.leaving).length;

/** Bring the number of learners to t.want (kept within the share) and give the rest of the share to games. */
function syncLearners(t) {
  t.want = Math.max(1, Math.min(t.share - 1, t.want));
  while (activeLearners(t) > t.want) removeLearner(t);
  const games = t.share - t.want;
  if (t.pool) t.pool.resize(games);
  else t.pool = new Pool(games, poolNets(t.id), t.nextJob, t.onResult, t.onFail);
  while (activeLearners(t) < t.want) addLearner(t);
}
/** A new learner joins the lead: it talks to it directly and gets its share of new positions from now on. */
function addLearner(t) {
  const id = t.nextLearner++, w = newWorker(), ch = new MessageChannel();
  const l = t.learners[id] = { id, w, pending: 0, dropped: 0, leaving: false };
  w.postMessage({ type: 'trainStart', data: trainNets(t.id), uses: t.cfg.uses, mirror: $('#tMirror').checked, rates: stepSizes(t.id).map(lr => lr.rate), lead: false, port: ch.port2 }, [ch.port2]);
  t.learners[0].w.postMessage({ type: 'join', id, port: ch.port1 }, [ch.port1]);
  hookLearner(t, l);
  // so the new learner has work at once, the fullest learner hands it half of its waiting lessons
  const fullest = Object.values(t.learners).filter(x => x !== l && !x.leaving).sort((a, b) => loadOf(b) - loadOf(a))[0];
  if (fullest) { fullest.splitTo = id; fullest.w.postMessage({ type: 'split' }); }
}
/** A learner (never the lead) leaves: its waiting positions are handed to the others first. */
function removeLearner(t) {
  const l = Object.values(t.learners).filter(x => x.id !== 0 && !x.leaving).sort((a, b) => loadOf(a) - loadOf(b))[0];
  if (!l) return;
  l.leaving = true;
  t.learners[0].w.postMessage({ type: 'leave', id: l.id });
}
/** Where new positions go: the staying learner with the fewest waiting. */
function emptiestLearner(t) {
  return Object.values(t.learners).filter(l => !l.leaving).sort((a, b) => loadOf(a) - loadOf(b))[0];
}
function hookLearner(t, l) {
  const rec = state.training[t.id];
  l.w.onerror = e => { e.preventDefault(); reportError('Training failed: ' + (e.message || 'unknown error')); stopTraining(t.id); };
  l.w.onmessage = e => {
    const m = e.data;
    if (trainings[t.id] !== t) return;
    if (m.type === 'status') {
      // what it holds, plus what was sent to it but is still waiting in its message queue (it reads messages only
      // between learning steps); without these the page would think it had room and send it more than it can hold
      l.pending = m.pending + Math.max(0, (l.sentV || 0) - (m.recvV || 0));
      l.dropped = m.dropped;
      const all = Object.values(t.learners);
      t.pending = all.reduce((a, x) => a + x.pending, 0);
      rec.dropped = all.reduce((a, x) => a + (x.dropped || 0), 0);
      if (l.id === 0) {
        t.learned = m.learned; rec.steps = rec.stepsBefore + m.steps - t.stepStart; rec.loss = m.loss; if (m.fit !== null) rec.fit = m.fit;
        if (sizeOn(t.id) && m.fits) SIZE_VARIANTS(NETS.find(n => n.id === t.id)).forEach((v, i) => { if (m.fits[i + 1] !== null && m.fits[i + 1] !== undefined) rec.size.nets[v.key].fit = m.fits[i + 1]; });
      }
      if (t.pool) t.pool.feed();
      renderTrainingSoon();
    } else if (m.type === 'exam') {                                   // one running score for all learners' exams
      const hits = m.stages.reduce((a, x) => a + x[0], 0), tries = m.stages.reduce((a, x) => a + x[1], 0);
      t.accuracy = blend(t.accuracy, hits, tries);
      rec.accuracy = t.accuracy;
      m.stages.forEach(([h, n], i) => { t.stages.net[i] = blend(t.stages.net[i], h, n); });
      rec.stages = t.stages;
      if (sizeOn(t.id) && m.each) SIZE_VARIANTS(NETS.find(n => n.id === t.id)).forEach((v, i) => {
        const x = rec.size.nets[v.key], e = m.each[i + 1];
        if (e && e[1]) x.acc = blend(x.acc, e[0], e[1]);
      });
    } else if (m.type === 'weights') {
      storeNets(t.id, m.datas || [m.data]);
      t.pool.setNets(poolNets(t.id));
      if (Date.now() - t.lastSave > 20000) { t.lastSave = Date.now(); saveNets(t.id); save(); }
    } else if (m.type === 'handover') {                               // a leaving learner's positions go to another
      const to = (m.split && t.learners[l.splitTo] && !t.learners[l.splitTo].leaving) ? t.learners[l.splitTo] : emptiestLearner(t), bufs = d => Object.values(d).map(a => a.buffer);
      to.pending += m.v.left.length;
      to.sentV = (to.sentV || 0) + m.v.left.length;
      to.w.postMessage({ type: 'handover', v: m.v }, bufs(m.v));
      if (!m.split && !l.byeSent) { l.byeSent = true; l.w.postMessage({ type: 'bye' }); }
      if (m.split) l.pending -= m.v.left.length;
    } else if (m.type === 'gone') {                                   // everything it held has been passed on
      l.w.terminate();
      delete t.learners[l.id];
      renderTrainingSoon();
    }
  };
}
/** A running score (the same weighting as before: each new answer counts 0.5%), updated with `hits` of `tries`. */
function blend(score, hits, tries) {
  if (!tries) return score;
  const f = Math.pow(0.995, tries), rate = hits / tries;
  return score === null || score === undefined ? rate : f * score + (1 - f) * rate;
}

/**
 * Each AI's training opponent, chosen on its card. 'self' (the default) keeps its usual games; the others replace
 * the second player in its games against itself: the Benchmark, the Strategist, another AI's
 * network (playing alone), or a mix (for each game, at random: itself, the Benchmark, the Strategist or one of the
 * other AIs). Learning from the teacher-game library is not affected.
 */
const OPPONENTS = () => [['self', 'itself'], ['bench', 'the Benchmark'], ['strategist', 'the Strategist'], ['ifelse', 'the ifelse AI'],
  ...NETS.map(n => ['net:' + n.id, n.name]), ['mix', 'a mix']];
/**
 * The test opponent, the same for every AI: the Benchmark (default), the Strategist, or a network loaded from a file and
 * kept frozen (stored as netData.testopp), so results stay comparable from test to test. Each test records whom it was against.
 */
const testOpp = () => state.testOpp || { kind: 'bench' };
const testOppName = () => { const o = testOpp(); return o.kind === 'strategist' ? 'the Strategist' : o.kind === 'net' ? o.name : 'the Benchmark'; };
function testOppSpec() {
  const o = testOpp();
  if (o.kind === 'strategist') return { kind: 'strategist', full: strategistConfig({}) };
  if (o.kind === 'net' && netData.testopp) return { kind: 'net', net: 'testopp', play: { replies: false, explore: 0 } };
  return { kind: 'bench' };
}
function renderTestOpp() {
  const o = testOpp();
  $('#tTestOpp').innerHTML = `<option value="bench">the Benchmark</option><option value="strategist">the Strategist</option>`
    + (o.kind === 'net' ? `<option value="net">${esc(o.name)} (frozen network)</option>` : '') + `<option value="file">a network file…</option>`;
  $('#tTestOpp').value = o.kind;
}
/** A new test opponent: every AI's step-size judging pauses for 9 tests, as after an opponent change. */
function setTestOpp(o) {
  state.testOpp = o;
  for (const n of NETS) restartComparison(n.id);
  save(); refreshPools(); renderTestOpp(); renderTraining();
}
$('#tTestOpp').addEventListener('change', () => {
  const v = $('#tTestOpp').value;
  if (v === 'file') { renderTestOpp(); $('#tTestFile').click(); return; }
  if (v === 'bench' || v === 'strategist') setTestOpp({ kind: v });
});
$('#tTestFile').addEventListener('change', async () => {
  const f = $('#tTestFile').files[0];
  $('#tTestFile').value = '';
  if (!f) return;
  try {
    const file = JSON.parse(await f.text()), data = file.network || file;
    if (!net3Valid(data, F3.hidden)) throw new Error('bad');
    netData.testopp = { enc: data.enc, arch: data.arch, weights: data.weights };
    saveNet('testopp');
    setTestOpp({ kind: 'net', name: file.name || f.name.replace(/\.json$/i, '') });
  } catch (e) { reportError('That file is not a network from this version of the AI lab.'); }
});
/** Who can be in an AI's mix: itself, the Benchmark, the Strategist and every other learning AI. */
const mixChoices = id => ['self', 'bench', 'strategist', 'ifelse', ...NETS.filter(n => n.id !== id).map(n => 'net:' + n.id)];
/** Who is in it: the members chosen in its mix panel (still existing), or everyone when none were chosen. */
function mixOf(id) {
  const all = mixChoices(id), chosen = state.training[id].mix;
  const kept = Array.isArray(chosen) ? all.filter(k => chosen.includes(k)) : [];
  return kept.length ? kept : all;
}
function opponentSpec(id, self) {
  let o = state.training[id].opponent || 'self';
  if (o === 'mix') { const pool = mixOf(id); o = pool[Math.floor(Math.random() * pool.length)]; }
  if (o === 'self' || o === 'net:' + id) return null;
  if (o === 'bench') return { kind: 'bench' };
  if (o === 'strategist') return { kind: 'strategist', full: strategistConfig({}) };
  if (o === 'ifelse') return { kind: 'ifelse', cfg: ifelseFull(state.ifelse && state.ifelse.v === 3 ? state.ifelse.best : {}) };   // its current tuned values
  if (o.startsWith('net:')) return { kind: 'net', net: 'opp:' + o.slice(4), play: { replies: false, explore: 0 } };
  return null;
}
/**
 * Step size: judged on the win rate in the scheduled tests against the Benchmark (playing alone), through two
 * weighted averages as in MACD: a fast one (9 tests) and a slow one (18 tests); each new test weighs 2/(N+1).
 * Judging starts once 18 tests count. When the fast average has not been more than 1 point above the slow one
 * for 3 counted tests in a row, the step size halves; then 9 counted tests pass before judging again.
 * It never goes below a floor of about 0.00003. Every scheduled test counts; "Test now" tests do not count.
 * Two manual modes replace this rule while they run (judging resumes 9 tests after they end):
 *   boost: the step goes to 0.00025, then halves at each test until it reaches the floor;
 *   cycle: the step halves at each test down to the floor, then doubles at each test up to 0.00025, and so on
 *          (a full cycle every 6 tests), starting at 0.00025 at the next test.
 */
const EMA_FAST = 9, EMA_SLOW = 18, EMA_MARGIN = 0.01, EMA_CONFIRM = 3, EMA_WAIT = 9;
const LR_START = 0.0005, LR_FLOOR = 0.001 / 32, LR_PEAK = 0.00025;
let LR_AXIS = LR_START;                    // the chart's step axis: top at the start step (raised for a record that went higher)
/** The starting step of the AI a record belongs to (its own, or one of its size-check networks): 0.0005 unless set. */
const startOf = rec => {
  for (const n of NETS) { const r = state.training[n.id]; if (r && (r === rec || (r.size && r.size.nets && Object.values(r.size.nets).includes(rec)))) return n.start || LR_START; }
  return LR_START;
};
const lrOf = rec => {
  if (!rec.lr) rec.lr = { rate: startOf(rec), halvings: 0, below: 0, wait: 0, mode: null, dir: 'down', aligned: false };
  if (rec.lr.below === undefined) {                                             // saved under the prediction-score rule: step size kept
    const { rate, halvings } = rec.lr;
    rec.lr = { rate, halvings: halvings || 0, below: 0, wait: 0 };
  }
  if (rec.lr.mode === undefined) Object.assign(rec.lr, { mode: null, dir: 'down', aligned: false });
  return rec.lr;
};
/** The main network's step size over training, for the chart: a new entry whenever it changes. */
function logRate(id) {
  const rec = state.training[id], lr = lrOf(rec), g = rec.games + rec.teacherGames, log = rec.lrLog || (rec.lrLog = []);
  const last = log[log.length - 1];
  if (last && Math.abs(last.r - lr.rate) < 1e-12) return;
  if (last && last.g === g) last.r = lr.rate; else log.push({ g, r: lr.rate });
}
/** Boost and cycle, at each scheduled test (when it starts). */
function stepSchedule(id) {
  let changed = false;
  for (const lr of stepSizes(id)) {
    if (lr.mode === 'boost') {
      lr.rate = Math.max(LR_FLOOR, lr.rate / 2);
      if (lr.rate <= LR_FLOOR * 1.0001) { lr.mode = null; lr.wait = EMA_WAIT; lr.below = 0; }   // over: the usual rule, after its wait
      changed = true;
    } else if (lr.mode === 'cycle') {
      if (!lr.aligned && lr.atTest) { lr.rate = LR_PEAK; lr.dir = 'down'; lr.aligned = true; delete lr.atTest; changed = true; continue; }   // started at this test
      if (lr.dir === 'down') { lr.rate = Math.max(LR_FLOOR, lr.rate / 2); if (lr.rate <= LR_FLOOR * 1.0001) lr.dir = 'up'; }
      else { lr.rate = Math.min(LR_PEAK, lr.rate * 2); if (lr.rate >= LR_PEAK * 0.9999) lr.dir = 'down'; }
      changed = true;
    }
  }
  if (changed) { sendRates(id); logRate(id); setTimeout(renderTraining, 0); }
}
const fmtRate = v => v.toPrecision(2);
const testRate = t => t.won / Math.max(1, t.won + t.lost + t.drawn);
/** Whether a test counts for the averages. */
const testCounts = t => !t.manual;
/** The two weighted averages along a list of {x, y} points (in order of games). */
function emaLine(points) {
  const af = 2 / (EMA_FAST + 1), as = 2 / (EMA_SLOW + 1), out = [];
  let fast = null, slow = null;
  for (const p of points) {
    fast = fast === null ? p.y : fast + af * (p.y - fast);
    slow = slow === null ? p.y : slow + as * (p.y - slow);
    out.push({ x: p.x, fast, slow });
  }
  return out;
}
const stepSizes = id => [lrOf(state.training[id]), ...(sizeOn(id) ? SIZE_VARIANTS(NETS.find(n => n.id === id)).map(v => lrOf(state.training[id].size.nets[v.key])) : [])];
function sendRates(id) { const t = trainings[id]; if (t) t.learners[0].w.postMessage({ type: 'rate', rates: stepSizes(id).map(lr => lr.rate) }); }
/**
 * One network's step size after a new scheduled test: list is that network's tests playing alone, the new one last.
 */
function judgeStepSize(id, lr, list) {
  const last = list[list.length - 1];
  if (!last || !testCounts(last)) return;
  if (lr.mode) return;                                                         // boost or cycle in charge
  if (lr.wait > 0) { lr.wait--; lr.below = 0; return; }
  const pts = list.filter(t => testCounts(t)).sort((a, b) => a.games - b.games).map(t => ({ x: t.games, y: testRate(t) }));
  if (pts.length < EMA_SLOW) return;
  const z = emaLine(pts).pop();
  if (z.fast > z.slow + EMA_MARGIN) { lr.below = 0; return; }
  if (++lr.below >= EMA_CONFIRM && lr.rate > LR_FLOOR * 1.0001) {
    lr.rate = Math.max(LR_FLOOR, lr.rate / 2); lr.halvings++; lr.below = 0; lr.wait = EMA_WAIT;
    sendRates(id); logRate(id);
    setTimeout(renderTraining, 0);                                            // the settings show the new step size
  }
}
/** Judging pauses for 9 counted tests (the step sizes stay): used when the training opponent changes. */
function restartComparison(id) { for (const lr of stepSizes(id)) { lr.below = 0; lr.wait = EMA_WAIT; } }


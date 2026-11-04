/**
 * Training periods, for the chart's background: whenever what an AI trains against changes, the lab notes the
 * game count and the new kind (the teacher-game library during a library session, otherwise its training opponent). Each period is shaded in its own colour.
 */
const PERIOD_KINDS = () => ({ library: ['the teacher-game library', '#4f7f5a'], self: ['itself', '#6f9fd8'], bench: ['the Benchmark', '#d86f6f'],
  random: ['the Random player', '#9b9b9b'], mix: ['a mix', '#b07fd8'], ifelse: ['the ifelse AI', '#4fa3c7'],
  'net:tabula': ['Tabula rasa', '#5fb8a8'],
  ...Object.fromEntries(NETS.filter(n => n.id !== 'tabula').map((n, i) => ['net:' + n.id, [n.name, ['#7fa8d8', '#d8a07f'][i % 2]]])) });
function periodKind(id) {
  const rec = state.training[id];
  return rec.libSession ? 'library' : rec.opponent || 'self';
}
function logPeriod(id) {
  const rec = state.training[id], log = rec.periods || (rec.periods = []), g = rec.games + rec.teacherGames, kind = periodKind(id);
  const last = log[log.length - 1];
  if (last && last.kind === kind) return;
  if (last && last.g === g) { last.kind = kind; if (log.length > 1 && log[log.length - 2].kind === kind) log.pop(); }
  else log.push({ g, kind });
  save();
}

/** "Search in training" (replaced "own later judgement"): in its games against itself or its training opponent the AI
 *  chooses each move with a 4-move look-ahead (its 4 best moves, each against every reply of a guessed opponent hand,
 *  scored by its network; the move whose worst reply is best), and that value becomes part of the position's target.
 *  Off by default. */
const searchOn = (rec, n) => !!rec.searchOn;
const searchShare = rec => Math.max(0, Math.min(1, rec.searchShare === undefined ? 0.5 : Number(rec.searchShare)));
const searchOf = id => { const rec = state.training[id], n = NETS.find(x => x.id === id); return searchOn(rec, n) ? searchShare(rec) : 0; };
const TRAIN_SEARCH_WIDTH = 4;
const searchNote = (on, w) => on
  ? `Its moves: its 4 best, each against every reply (guessed hand). Targets: ${Math.round(100 * (1 - w))}% the real result, ${Math.round(100 * w)}% the search's value. Slower games.`
  : 'Off: it plays its best-scored move; targets are the real result only.';

/**
 * How each AI has trained so far and what came of it, in one file for examining the training methods: the lab-wide
 * settings and rule constants, then per AI (and per size-check network) its settings, its whole training record,
 * and every Benchmark test with the two weighted averages the lab computed at that test. Left out: network weights,
 * the tournament, what is running right now, error messages and internal bookkeeping.
 */
function exportLab() {
  const shape = d => (d ? { format: d.enc, hidden: d.arch && d.arch.hidden, printedValues: d.arch && d.arch.props.length,
    learningSteps: d.step || 0 } : null);
  const SKIP = new Set(['failed', 'lastError', 'libCursor', 'libOwn', 'libSession', 'stepsBefore', 'tests', 'size']);
  const record = r => Object.fromEntries(Object.entries(r).filter(([k]) => !SKIP.has(k)));
  // one network's tests, in order of games, each counted test with the lab's 9- and 18-test averages at that point
  const testsOf = list => {
    const sorted = list.slice().sort((a, b) => a.games - b.games), counted = sorted.filter(t => testCounts(t));
    const ema = emaLine(counted.map(t => ({ x: t.games, y: testRate(t) })));
    return sorted.map(t => { const i = counted.indexOf(t);
      return { ...t, winRate: testRate(t), ...(i >= 0 ? { averageFast: ema[i].fast, averageSlow: ema[i].slow } : { counted: false }) }; });
  };
  const ts = trainingSettings();
  const data = {
    exported: new Date().toISOString(),
    lab: { networkFormat: 3, networkVersion: F3.version, cellSummary: F3.CO, cellInputs: F3.CS + F3.props.length + 7, handSlots: F3.HS,
      mainInputs: F3.NCELL * F3.CO + F3.HS * F3.props.length + F3.NREST, hidden: F3.hidden },
    settings: { explore: ts.explore, uses: ts.uses, testEvery: ts.evalEvery, testGames: ts.evalGames, mirror: $('#tMirror').checked },
    ifelse: state.ifelse || null,
    stepSizeRule: { start: LR_START, floor: LR_FLOOR, peak: LR_PEAK, averageFast: EMA_FAST, averageSlow: EMA_SLOW, margin: EMA_MARGIN, confirm: EMA_CONFIRM, wait: EMA_WAIT },
    ais: NETS.map(n => {
      const r = state.training[n.id];
      return { id: n.id, name: n.name, description: n.desc,
        settings: { startStep: n.start || LR_START, opponent: r.opponent || 'self', ...(r.opponent === 'mix' ? { mix: mixOf(n.id) } : {}), searchInTraining: searchOf(n.id) },
        network: shape(netData[n.id]),
        record: { ...record(r), stepSize: lrOf(r) },
        tests: testsOf(r.tests.filter(t => !t.net)),
        sizeCheck: sizeOn(n.id) ? SIZE_VARIANTS(n).map(v => ({ key: v.key, label: v.label, hidden: v.hidden, network: shape(netData[copyId(n.id, v.key)]),
          ...r.size.nets[v.key], stepSize: lrOf(r.size.nets[v.key]), tests: testsOf(r.tests.filter(t => t.net === v.key)) })) : null };
    }),
  };
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 1)], { type: 'application/json' }));
  a.download = `three-bases-lab-export-${new Date().toISOString().slice(0, 16).replace(/[:T]/g, '-')}.json`;
  a.click();
}

/** Every second: measure how many lessons per second the learners get through, and move one core between
 * learning and games if the queues show it is needed. */
ticks.push(() => {
  const now = Date.now();
  for (const t of Object.values(trainings)) {
    const learned = t.learned || 0, hist = t.speedLog || (t.speedLog = []);
    hist.push([now, learned]);
    while (hist.length > 4) hist.shift();
    t.speed = hist.length > 1 ? (learned - hist[0][1]) / ((now - hist[0][0]) / 1000) : 0;
    if (t.testing || now - t.lastChange < LEARNER_PAUSE) continue;       // no changes while a test is running
    const n = activeLearners(t), load = loadOf(t);
    if (load >= LEARNER_MORE && n < t.share - 1) t.want = n + 1;
    else if (load < LEARNER_FEWER && n > 1) t.want = n - 1;
    else continue;
    t.lastChange = now;
    syncLearners(t);
    renderTrainingSoon();
  }
});

function startTraining(id) {
  if (trainings[id]) return;                                                   // already training
  if (tune.running) pauseTune();                                               // one thing at a time: the tuning waits
  if (!netsReady) { reportError('Still reading the saved networks. Try again in a moment.'); return; }
  if (!LIB.ready) { libLoadedP.then(() => startTraining(id)); return; }       // the library is read first, so its numbering is settled
  if (stoppingIds[id]) { stoppingIds[id].then(() => startTraining(id)); return; }
  if (tour.running || manual) { reportError('Pause the tournament or the test first: only one thing runs at a time.'); return; }
  logRate(id);                                                                 // the chart's step-size line starts (or continues) here
  const cfg = trainingSettings(), rec = state.training[id];
  rec.stepsBefore = rec.steps;
  const stepStart = (netData[id] && netData[id].step) || 0;         // the network's own step count, saved with it
  const net = NETS.find(n => n.id === id);
  /** A training game of `self` against the chosen opponent (seats at random): the two players' specs. */
  const versus = self => {
    const opp = opponentSpec(id, self);
    if (!opp) return [self, self];
    const seat = Math.random() < 0.5 ? 0 : 1, specs = [];
    specs[seat] = self; specs[1 - seat] = opp;
    return specs;
  };
  const t = trainings[id] = { get cfg() { return trainingSettings(); }, id, learners: {}, nextLearner: 1, want: 2, share: 2, lastChange: Date.now(), accuracy: null, stages: { net: [null, null, null], bench: [null, null, null] }, pool: null, testing: null, lastSave: Date.now(), cfg,
    pending: 0, libQueued: 0, fails: 0, stepStart };
  notice = '';
  const lead = t.learners[0] = { id: 0, w: newWorker(), pending: 0, dropped: 0, leaving: false };   // runs the learning steps
  lead.w.postMessage({ type: 'trainStart', data: trainNets(id), uses: cfg.uses, mirror: $('#tMirror').checked, rates: stepSizes(id).map(lr => lr.rate), lead: true });
  hookLearner(t, lead);

  let k = 0;
  // how a test game (against the test opponent, not learned from) has the network play: alone
  const TEST_PLAY = { alone: { replies: false, explore: 0 } };
  const startTest = at => {
    stepSchedule(id);                                                          // boost / cycle move on at each test
    const modes = ['alone'], todo = [];                                        // every AI is tested playing alone
    if (sizeOn(id)) for (const v of SIZE_VARIANTS(net)) modes.push('alone@' + v.key);
    // prediction scores at this moment (its own network, and the size check's), drawn on the chart with the tests
    (rec.predLog || (rec.predLog = [])).push({ games: at, main: t.accuracy === null ? rec.accuracy : t.accuracy,
      ...(sizeOn(id) ? Object.fromEntries(SIZE_VARIANTS(net).map(v => [v.key, rec.size.nets[v.key].acc])) : {}) });
    for (const mode of modes) for (let j = 0; j < t.cfg.evalGames; j++) todo.push({ mode, j });
    t.testing = { opp: testOppSpec(), vs: testOppName(), todo, done: 0, total: todo.length, perMode: t.cfg.evalGames, atGames: at, score: Object.fromEntries(modes.map(m => [m, { won: 0, lost: 0, drawn: 0 }])) };
    // during the test, all cores but one play the test games; the learners come back afterwards
    t.beforeTest = activeLearners(t);
    { const ap = t.avgPos === undefined ? 60 : t.avgPos, fly = t.inflight || 0;   // and room for the games still being played
      t.want = Math.max(1, Math.ceil((t.pending + fly * ap) / (LEARNER_MAX_POS * 0.8))); }
    syncLearners(t);
  };
  t.nextJob = () => {
    if (trainings[id] !== t) return null;
    if (t.testing && t.testing.todo.length) {
      const item = t.testing.todo.shift(), netSide = item.j % 2, specs = [];
      const [how, copy] = item.mode.split('@');
      specs[netSide] = { kind: 'net', net: copy ? 'train~' + copy : 'train', play: TEST_PLAY[how] };
      specs[1 - netSide] = t.testing.opp;
      return { key: 'test' + id + item.mode + item.j + '-' + k++, kind: 'test', item, netSide, specs, decks: scheduledDecks(item.j), seed: 9000001 + Math.floor(item.j / 2) };
    }
    if (loadAhead(t) >= 1) return null;                                        // the learners are behind: wait for them
    if (rec.libSession) {                                                      // learning from the shared library of teacher games
      if (rec.teacherGames + t.libQueued < rec.libSession.until) {
        const li = libNext(rec);
        if (li !== null) {
          t.libQueued++;
          return { key: 'lib' + id + k++, kind: 'library', replay: LIB.games[li], decks: randomDecks(),
            specs: [{ kind: 'bench' }, { kind: 'bench' }], record: true };
        }
        rec.libSession.until = rec.teacherGames + t.libQueued;                // the library ran out: the session ends early
      }
      if (t.libQueued > 0) return null;                                        // its last games are still being learned
      rec.libSession = null; logPeriod(id); save(); setTimeout(renderTraining, 0);   // over: back to its usual training
    }
    const self = { kind: 'net', net: 'train', play: { replies: searchOf(id) > 0, width: TRAIN_SEARCH_WIDTH, explore: t.cfg.explore } };   // itself, or the chosen opponent
    return { key: 'self' + id + k++, kind: 'self', specs: versus(self), decks: randomDecks(), record: true, search: searchOf(id) };
  };

  { const pick = t.nextJob;                                                  // count the training games being played
    t.nextJob = () => { const j = pick(); if (j && j.kind !== 'test') t.inflight = (t.inflight || 0) + 1; return j; }; }
  t.onResult = (r, job) => {
    if (trainings[id] !== t) return;
    t.fails = 0;
    if (job.kind !== 'test') {
      t.inflight = Math.max(0, (t.inflight || 0) - 1);
      const np = r.D ? r.D.length : 0;                                         // the recent average a game brings
      t.avgPos = t.avgPos === undefined ? np : 0.9 * t.avgPos + 0.1 * np;
    }
    if (job.kind === 'library') {
      t.libQueued--; rec.teacherGames++;
      const o = rec.outcomes || (rec.outcomes = { won: 0, draw: 0, lost: 0, none: 0 });
      o[r.winner === 0 || r.winner === 1 ? 'won' : r.winner]++;
      if ((rec.teacherGames + rec.games) % t.cfg.evalEvery === 0 && !t.testing) startTest(rec.teacherGames + rec.games);
      if (rec.libSession && rec.teacherGames >= rec.libSession.until && t.libQueued === 0) {   // done: back to its usual training
        rec.libSession = null; logPeriod(id); save(); setTimeout(renderTraining, 0);
      }
    }
    if (r.X) {
      const n = r.D.length;
      rec.positions += n;
      const to = emptiestLearner(t);                                          // to the learner with the emptiest queue
      to.pending += n; t.pending += n;
      to.sentV = (to.sentV || 0) + n;
      if (r.bench) { r.bench.forEach(([h, c], i) => { t.stages.bench[i] = blend(t.stages.bench[i], h, c); }); rec.stages = t.stages; }
      to.w.postMessage({ type: 'data', X: r.X, K: r.K, Y: r.Y, D: r.D, E: r.E }, [r.X, r.K, r.Y, r.D, r.E].map(a => a.buffer));
    }
    if (job.kind === 'self') {
      const o = rec.outcomes || (rec.outcomes = { won: 0, draw: 0, lost: 0, none: 0 });
      o[r.winner === 0 || r.winner === 1 ? 'won' : r.winner]++;
      rec.games++;
      const played = rec.teacherGames + rec.games;                             // every AI counts all its training games
      if (played % t.cfg.evalEvery === 0 && !t.testing) startTest(played);
    }
    if (job.kind === 'test') {
      const x = t.testing, sc = x.score[job.item.mode];
      x.done++;
      if (r.winner === job.netSide) sc.won++; else if (r.winner === 'draw') sc.drawn++; else sc.lost++;
      if (x.done >= x.total) {
        for (const [key, v] of Object.entries(x.score)) {
          const [mode, copy] = key.split('@');
          const tagged = copy ? { mode, net: copy } : { mode };
          rec.tests.push({ games: x.atGames, won: v.won, lost: v.lost, drawn: v.drawn, n: x.perMode, vs: x.vs, ...tagged });
        }
        judgeStepSize(id, lrOf(rec), rec.tests.filter(q => !q.net && q.mode === 'alone'));   // the step sizes, on the win rates
        if (sizeOn(id)) for (const v of SIZE_VARIANTS(net)) judgeStepSize(id, lrOf(rec.size.nets[v.key]), rec.tests.filter(q => q.net === v.key && q.mode === 'alone'));
        t.testing = null; save();
        t.want = t.beforeTest || t.want;                                       // the learners come back
        t.lastChange = Date.now();
        syncLearners(t);
      }
    }
    renderTrainingSoon();
  };

  /** A game crashed: count it, remember why, and let a replacement be issued so no counter can get stuck. */
  t.onFail = (job, message) => {
    if (trainings[id] !== t) return;
    if (job && job.kind !== 'test') t.inflight = Math.max(0, (t.inflight || 0) - 1);
    rec.failed = (rec.failed || 0) + 1; rec.lastError = message;
    if (job && job.kind === 'library') t.libQueued--;
    if (job && job.kind === 'test') t.testing.todo.push(job.item);            // played again
    if (++t.fails >= 10) { reportError('Training stopped: 10 background games in a row failed. Last error: ' + message); stopTraining(id); return; }
    renderTrainingSoon();
  };

  logPeriod(id);        // the chart's background: what it trains against from here on
  rebalancePools();     // sets this network's share (and resizes any other active one), its learners and its games
  renderTraining();
}

/** Stop one network's training. Its lead learner sends its final weights first, then everything is saved. */
function stopTraining(id) {
  if (!trainings[id]) return stoppingIds[id];
  const t = trainings[id], rec = state.training[id];
  delete trainings[id];
  t.pool.stop();
  const p = stoppingIds[id] = new Promise(resolve => {
    const done = final => {
      clearTimeout(timer);
      if (final) { storeNets(id, final.datas || [final.data]); rec.steps = (rec.stepsBefore || 0) + final.steps - (t.stepStart || 0); rec.loss = final.loss; }
      Object.values(t.learners).forEach(l => l.w.terminate());
      saveNets(id); save();
      delete stoppingIds[id];
      rebalancePools();     // the network(s) still training reclaim the freed share
      renderTraining();
      resolve();
    };
    const timer = setTimeout(() => done(null), 3000);
    Object.values(t.learners).forEach(l => { l.w.onmessage = null; l.w.postMessage({ type: 'stop' }); });
    t.learners[0].w.onmessage = e => { if (e.data.type === 'final') done(e.data); };
  });
  renderTraining();
  return p;
}
/** Stop every network currently training; resolves once all are saved. */
function stopAllTraining() { return Promise.all(Object.keys(trainings).map(stopTraining)); }


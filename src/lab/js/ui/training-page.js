/**
 * The AI boards. Each has a header, then two clearly separate halves: settings on the left (fixed width, so
 * nothing moves when a value needs more room), the action buttons in one row above progress and statistics on the
 * right, and the chart across the full width below. While training runs only the statistics, the header's status and the
 * chart refresh (once a second); the settings are rebuilt only when something about them changes, so an open
 * dropdown or a number being typed is never interrupted.
 */
function cardStats(n) {
  const r = state.training[n.id], t = trainings[n.id], active = !!t, testingNow = manual && manual.id === n.id;
  const own = r.tests.filter(x => !x.net), last = [...own].reverse().find(x => x.mode === 'alone'), testing = active && t.testing;
  const rate = x => Math.round(100 * x.won / Math.max(1, x.won + x.lost + x.drawn)) + '%';
  const o = r.outcomes, f = (label, value, cls = '') => `<div class="fact"><dt>${label}</dt><dd${cls ? ` class="${cls}"` : ''}>${value}</dd></div>`;
  const pc = v => (v === null || v === undefined ? '–' : Math.round(v * 100) + '%');
  const pn = v => (v === null || v === undefined ? '–' : String(Math.round(v * 100)));   // a percentage without its sign
  const none = '<span class="muted">–</span>', idle = '<span class="muted">not training</span>';
  // every AI shows the same rows in the same places: what does not apply shows a dash
  const left = [
    f('Own training games', r.games),
    f('Library games learned from', r.teacherGames > 0 ? `${r.teacherGames} <span class="muted">(library ${LIB.games.length})</span>` : none),
    f('How training games ended', o ? `${o.won} won | ${o.lost} pass | ${o.draw} draw | ${o.none} stop` : none),
    f('Positions collected', r.positions),
  ];
  const right = [
    f('Predicts the winner', `${pc(r.accuracy)} new positions · ${pc(r.fit)} lessons`),
    f('By game stage', r.stages && r.stages.net.some(v => v !== null) ? ('%: ' + ['E', 'M', 'L'].map((name, i) => `${name} ${pn(r.stages.net[i])} <span class="muted">(${pn(r.stages.bench[i])})</span>`).join(' | ')) : none),
    f('Learning steps', r.steps),
    f('Cores', active ? `${activeLearners(t)} learning · ${t.pool ? t.pool.size : 0} playing games` : idle),
    f('Learning speed', active ? `${Math.round(t.speed || 0)} lessons per second` : idle),
    f('Waiting to be learned from', active ? `${t.pending}${loadOf(t) >= 1 ? ' (new games wait)' : ''}` : idle),
  ];
  const alerts = [
    r.failed ? f('Failed games', `${r.failed} crashed and were replaced. Last error: ${esc(r.lastError || 'unknown')}`, 'bad') : '',
    r.dropped ? f('Positions dropped', `${r.dropped} (the learners were overloaded)`, 'bad') : '',
  ].join('');
  return `<dl class="facts">${left.join('')}</dl><dl class="facts">${right.join('')}</dl>${alerts ? `<dl class="facts alerts">${alerts}</dl>` : ''}`;
}
/** The training-opponent dropdown: a list like a select; hovering (or focusing) "a mix" opens its panel beside it. */
const oppLabel = (id, v) => (OPPONENTS().find(([k]) => k === v) || [v, v])[1];
function oppControl(n) {
  const id = n.id, cur = state.training[id].opponent || 'self', mix = mixOf(id), all = mixChoices(id);
  const opts = OPPONENTS().filter(([v]) => v !== 'net:' + id);
  const sum = mix.length === all.length ? 'all' : `${mix.length} of ${all.length}`;
  return `<div class="oppdd" data-id="${id}">
    <button type="button" class="oppbtn" aria-haspopup="listbox" aria-expanded="false" aria-label="Training opponent">
      <span class="oppcur">${esc(cur === 'mix' ? `a mix (${sum})` : oppLabel(id, cur))}</span><span class="caret" aria-hidden="true"></span></button>
    <div class="oppmenu" role="listbox" tabindex="-1" hidden>${opts.map(([v, label]) => `<div class="oppopt${v === 'mix' ? ' mixopt' : ''}" role="option" data-v="${v}" aria-selected="${v === cur}">
      <span>${esc(label)}</span>${v === 'mix' ? `<span class="mixsum">${sum}</span><span class="more" aria-hidden="true">›</span>` : ''}</div>`).join('')}</div>
    <div class="mixpanel" role="group" aria-label="Who is in the mix" hidden>
      <div class="mixhead">In the mix</div>
      <div class="mixnote">Each training game picks one of these at random.</div>
      ${all.map(k => `<label class="mixrow"><input type="checkbox" data-k="${k}" ${mix.includes(k) ? 'checked' : ''}> ${esc(oppLabel(id, k))}</label>`).join('')}
      <div class="mixfoot"><button type="button" class="small" data-mix="all">All</button><span class="mixnote">From the next game on.</span></div>
    </div>
  </div>`;
}
let oppOpen = null;           // { id, panel }: the opponent dropdown that is open, kept open through a redraw
/** Sets an AI's training opponent (and its mix), from the next game on. */
function setOpponent(id, v, mix) {
  const rec = state.training[id], before = JSON.stringify([rec.opponent || 'self', rec.opponent === 'mix' ? mixOf(id) : null]);
  rec.opponent = v;
  if (mix) rec.mix = mix.length === mixChoices(id).length ? null : mix;   // everyone: also whoever is added later
  if (JSON.stringify([v, v === 'mix' ? mixOf(id) : null]) === before) { save(); return; }
  restartComparison(id);                                                   // other games: judging the step size pauses for 9 tests
  logPeriod(id);
  save();
  if (trainings[id] && trainings[id].pool) trainings[id].pool.setNets(poolNets(id));   // its game workers get that opponent now
}
function hookOppControl(dd) {
  const id = dd.dataset.id, btn = dd.querySelector('.oppbtn'), menu = dd.querySelector('.oppmenu'), panel = dd.querySelector('.mixpanel');
  const opts = [...menu.querySelectorAll('.oppopt')], mixRow = menu.querySelector('.mixopt');
  const place = () => {                                                    // the panel beside the menu, at the mix row; flipped left if there is no room
    panel.style.top = (menu.offsetTop + mixRow.offsetTop - 8) + 'px';
    const r = menu.getBoundingClientRect(), w = panel.offsetWidth || 260;
    panel.style.left = (r.right + 6 + w > window.innerWidth - 8 ? menu.offsetLeft - w - 6 : menu.offsetLeft + menu.offsetWidth + 6) + 'px';
  };
  const showPanel = on => { panel.hidden = !on; mixRow.classList.toggle('open', on); if (on) place(); if (oppOpen) oppOpen.panel = on; };
  const open = (panelToo = false) => {
    for (const other of document.querySelectorAll('.oppdd.open')) if (other !== dd) other.closeDd();
    dd.classList.add('open'); menu.hidden = false; btn.setAttribute('aria-expanded', 'true');
    oppOpen = { id, panel: false };
    showPanel(panelToo);
    (menu.querySelector('[aria-selected="true"]') || opts[0]).classList.add('hot');
  };
  const close = () => { dd.classList.remove('open'); menu.hidden = true; panel.hidden = true; btn.setAttribute('aria-expanded', 'false'); opts.forEach(o => o.classList.remove('hot', 'open')); if (oppOpen && oppOpen.id === id) oppOpen = null; };
  dd.closeDd = close;
  const pick = v => { close(); setOpponent(id, v); renderTraining(); };
  btn.addEventListener('click', () => (menu.hidden ? open() : close()));
  for (const o of opts) {
    o.addEventListener('mouseenter', () => { opts.forEach(x => x.classList.remove('hot')); o.classList.add('hot'); showPanel(o === mixRow); });
    o.addEventListener('click', e => {
      if (o === mixRow && e.target.closest('.more')) { showPanel(panel.hidden); return; }   // the arrow only opens the panel (for touch)
      pick(o.dataset.v);
    });
  }
  const boxes = [...panel.querySelectorAll('input[data-k]')];
  const changed = () => {
    const mix = boxes.filter(b => b.checked).map(b => b.dataset.k);
    setOpponent(id, 'mix', mix);                                           // editing the mix chooses it
    renderTraining();
  };
  for (const b of boxes) b.addEventListener('change', () => {
    if (!boxes.some(x => x.checked)) { b.checked = true; return; }          // at least one
    if (oppOpen) oppOpen.focus = b.dataset.k;
    changed();
  });
  panel.querySelector('[data-mix="all"]').addEventListener('click', () => { boxes.forEach(b => { b.checked = true; }); if (oppOpen) oppOpen.focus = 'all'; changed(); });
  dd.addEventListener('keydown', e => {
    if (menu.hidden) { if (e.key === 'ArrowDown' || e.key === 'Enter' || e.key === ' ') { if (e.target === btn) { e.preventDefault(); open(); menu.focus(); } } return; }
    if (e.key === 'Escape') { e.preventDefault(); close(); btn.focus(); return; }
    if (e.target.matches('input, button.small')) return;                   // inside the panel: the usual keys
    const i = opts.findIndex(o => o.classList.contains('hot'));
    const go = k => { opts.forEach(x => x.classList.remove('hot')); opts[k].classList.add('hot'); opts[k].scrollIntoView({ block: 'nearest' }); showPanel(opts[k] === mixRow); };
    if (e.key === 'ArrowDown') { e.preventDefault(); go(Math.min(opts.length - 1, i + 1)); }
    if (e.key === 'ArrowUp') { e.preventDefault(); go(Math.max(0, i - 1)); }
    if (e.key === 'ArrowRight' && opts[i] === mixRow) { e.preventDefault(); showPanel(true); boxes[0].focus(); }
    if (e.key === 'ArrowLeft' && !panel.hidden) { e.preventDefault(); menu.focus(); }
    if (e.key === 'Enter' && i >= 0) { e.preventDefault(); pick(opts[i].dataset.v); }
  });
  if (oppOpen && oppOpen.id === id) {                                      // it was open before this redraw
    const { panel: p, focus: f } = oppOpen;
    open(p);
    const el = f === 'all' ? panel.querySelector('[data-mix="all"]') : f ? panel.querySelector(`input[data-k="${f}"]`) : null;
    if (el) { el.focus({ preventScroll: true }); oppOpen.focus = f; }
  }
}
document.addEventListener('pointerdown', e => { for (const dd of document.querySelectorAll('.oppdd.open')) if (!dd.contains(e.target)) dd.closeDd(); });
function cardConfig(n) {
  const r = state.training[n.id], t = trainings[n.id], active = !!t, testingNow = manual && manual.id === n.id;
  const row = (label, control, note = '') => `<div class="cfg"><div class="lbl">${label}</div><div class="ctl">${control}</div>${note !== null ? `<div class="cnote">${note}</div>` : ''}</div>`;
  const w = searchShare(r), on = searchOn(r, n);
  return [
    row('Training opponent', oppControl(n),
      'From the next game on.'),
    row('Search in training', `<label class="inline"><input type="checkbox" data-a="searchOn" data-id="${n.id}" ${on ? 'checked' : ''}> on</label>
      <label class="inline">share <input type="number" data-a="searchShare" data-id="${n.id}" min="0" max="1" step="0.05" value="${w}" ${on ? '' : 'disabled'} aria-label="Share of the search's value in the targets"></label>`,
      searchNote(on, w)),
    row('Step size', `<span class="stepctl"><span class="val">${lrOf(r).mode === 'cycle' ? '' : fmtRate(lrOf(r).rate)}</span>${lrOf(r).mode === 'cycle' ? '' : ` <button class="small" data-a="lrreset" data-id="${n.id}" title="Back to ${fmtRate(n.start || LR_START)}">Reset</button> <button class="small" data-a="lrboost" data-id="${n.id}" title="0.00025, then halved at each test down to the floor"${lrOf(r).mode === 'boost' ? ' disabled' : ''}>Boost</button>`}
      <button class="small cyc${lrOf(r).mode === 'cycle' ? ' on' : ''}" data-a="lrcycle" data-id="${n.id}" aria-pressed="${lrOf(r).mode === 'cycle'}" title="${lrOf(r).mode === 'cycle' ? 'Stop the cycle' : 'Cycle the step between about 0.00003 and 0.00025'}">${lrOf(r).mode === 'cycle' ? `Cycle ${fmtRate(lrOf(r).rate)} ${!lrOf(r).aligned ? '·' : lrOf(r).dir === 'down' ? '↓' : '↑'}` : 'Cycle'}</button></span>`,
      lrOf(r).mode === 'boost' ? 'Boosted: halves at each test until it reaches the floor (about 0.00003); then the usual rule resumes after 9 tests.'
        : lrOf(r).mode === 'cycle' ? (!lrOf(r).aligned ? 'Cycle on: starts at 0.00025 at the next test.' : 'Cycle on: halves at each test down to about 0.00003, then doubles up to 0.00025 (6 tests per cycle). Click to stop; the step stays, and the usual rule resumes after 9 tests.')
        : `Halves by itself when test wins stop rising: the 9-test average has not been more than 1 point above the 18-test average for 3 tests in a row; never below about 0.00003${lrOf(r).wait ? `. Judging again in ${lrOf(r).wait} tests` : ''}.`),
    row('Size check', `<label class="inline"><input type="checkbox" data-a="size" data-id="${n.id}" ${sizeOn(n.id) && !lessonsOn(n.id) ? 'checked' : ''}> on</label>`,
      'More nodes and Extra layer learn the same lessons alongside it, starting as copies of its network as it is when switched on.'),
    row('Lessons check', `<label class="inline"><input type="checkbox" data-a="lessons" data-id="${n.id}" ${lessonsOn(n.id) ? 'checked' : ''}> on</label>`,
      'Two copies of its network as it is when switched on learn from the same games, but each lesson is 15% and 45% the copy\'s own win chance one move later, instead of the AI\'s 30%. Replaces the size check while on.'),
  ].join('');
}
/** The action buttons, in one row at the top of the right half. */
function cardActions(n) {
  const t = trainings[n.id], active = !!t, testingNow = manual && manual.id === n.id;
  return `<div class="actions">
      <button class="${active ? '' : 'go'}" data-a="train" data-id="${n.id}">${active ? 'Pause training' : 'Train'}</button>
      <button data-a="test" data-id="${n.id}">${testingNow ? 'Stop test' : 'Test now (100 games)'}</button>
      <button data-a="watch" data-id="${n.id}">Watch a game</button>
      <select data-a="wvs" data-id="${n.id}" aria-label="Opponent to watch it play">
        <option value="self">against itself</option><option value="bench">against the Benchmark</option><option value="random">against the Random player</option>
      </select>
      <button data-a="download" data-id="${n.id}" title="The network with its whole training record (chart, tests, settings), to continue training later">Export training</button>
      <button data-a="netonly" data-id="${n.id}" title="The network only, without its training record; you name it (suggested: the AI and its latest win rate against the Benchmark)">Export network</button>
      <button data-a="load" data-id="${n.id}">Load network file</button>
      <button data-a="lib" data-id="${n.id}" class="${state.training[n.id].libSession ? 'libon' : ''}" aria-pressed="${!!state.training[n.id].libSession}" ${state.training[n.id].libSession || libSessionSize(state.training[n.id], trainingSettings().evalEvery) ? '' : 'disabled'} title="${state.training[n.id].libSession ? (state.training[n.id].libSession.stopping ? 'Stopping at the end of this test interval; click to learn the whole session after all' : 'Stop at the end of the current test interval') : "Learn from the shared library's teacher games it has not learned from yet, in whole test intervals; then back to its usual training"}">${state.training[n.id].libSession ? `Library: ${state.training[n.id].teacherGames} of ${state.training[n.id].libSession.until}${state.training[n.id].libSession.stopping ? ' · stopping' : ''}` : `Learn from library (${libSessionSize(state.training[n.id], trainingSettings().evalEvery)})`}</button>
      <button data-a="reset" data-id="${n.id}">Start over</button>
      ${n.added ? `<button data-a="remove" data-id="${n.id}" title="Delete this trainer, its network and its training record">Remove</button>` : ''}
    </div>`;
}
const cardPhase = n => {
  const t = trainings[n.id], test = t && t.testing ? ` · testing ${t.testing.done}/${t.testing.total}` : manual && manual.id === n.id ? ` · testing ${manual.done}/${manual.total}` : '';
  if (!t) return test ? test.slice(3) : '';
  return (state.training[n.id].libSession ? 'learning from the teacher-game library' : 'training') + (Object.keys(trainings).length > 1 ? ' · sharing cores' : '') + test;
};
/** Refresh only what changes while training: the left half, the header's status and the chart. */
function updateTrainingStats() {
  const set = trainingSettings();
  for (const n of NETS) {
    const card = $('#netCards').querySelector(`.netcard[data-id="${n.id}"]`);
    if (!card) continue;
    card.querySelector('[data-slot="facts"]').innerHTML = cardStats(n);
    const ph = card.querySelector('[data-slot="phase"]'), p = cardPhase(n);
    ph.textContent = p; ph.hidden = !p;
    card.querySelector('[data-slot="chart"]').innerHTML = chart(n, state.training[n.id], set.evalEvery);
    const svg = card.querySelector('svg[data-chart]');
    if (svg) hookChart(svg);
  }
}
/** Redraw one AI's chart right away (after a label was clicked). */
function refreshChart(id) {
  const n = NETS.find(x => x.id === id), card = $('#netCards').querySelector(`.netcard[data-id="${id}"]`);
  if (!n || !card) return;
  card.querySelector('[data-slot="chart"]').innerHTML = chart(n, state.training[id], trainingSettings().evalEvery);
  const svg = card.querySelector('svg[data-chart]');
  if (svg) hookChart(svg);
  const li = card.querySelector('.legend .li.tog:focus-visible');
  if (li) li.focus();
}
function renderTraining() {
  $('#netCards').innerHTML = NETS.map(n => `<div class="netcard" data-id="${n.id}">
      <div class="cardhead"><h3>${esc(n.name)} <span class="phase" data-slot="phase" hidden></span></h3><p class="note">${esc(n.desc)}</p></div>
      <div class="cardbody">
        <section class="config" aria-label="Settings"><h4>Settings</h4>${cardConfig(n)}</section>
        <section class="stats" aria-label="Progress">${cardActions(n)}<h4>Progress</h4><div class="factcols" data-slot="facts"></div></section>
      </div>
      <div data-slot="chart"></div>
    </div>`).join('') + '<button class="addtrainer" data-a="add" title="A plain trainer that learns like Tabula rasa: load a network file into it, or train it from nothing">+ New trainer</button><p class="sub" id="tStatus"></p>';
  updateTrainingStats();
  $('#tStatus').textContent = notice;
  for (const b of $('#netCards').querySelectorAll('button[data-a]')) b.addEventListener('click', () => trainAction(b.dataset.a, b.dataset.id));
  for (const dd of $('#netCards').querySelectorAll('.oppdd')) hookOppControl(dd);
  for (const inp of $('#netCards').querySelectorAll('input[data-a="searchOn"]')) {
    inp.addEventListener('change', () => {                                     // from the next game on
      const id = inp.dataset.id, rec = state.training[id];
      rec.searchOn = inp.checked; save();
      const card = inp.closest('.config');                                     // just this row: nothing else moves
      card.querySelector('input[data-a="searchShare"]').disabled = !inp.checked;
      inp.closest('.cfg').querySelector('.cnote').textContent = searchNote(inp.checked, searchShare(rec));
    });
  }
  for (const inp of $('#netCards').querySelectorAll('input[data-a="searchShare"]')) {
    inp.addEventListener('change', () => {
      const id = inp.dataset.id, w = searchShare({ searchShare: inp.value });
      state.training[id].searchShare = w; inp.value = w; save();
      inp.closest('.cfg').querySelector('.cnote').textContent = searchNote(true, w);
    });
  }

  wireSizeChecks($('#netCards'));


  for (const sel of $('#netCards').querySelectorAll('select[data-a="wvs"]')) {
    sel.value = watchChoice[sel.dataset.id] || 'self';
    sel.addEventListener('change', () => { watchChoice[sel.dataset.id] = sel.value; });
  }
}
const watchChoice = {};

/**
 * A small naming dialog: resolves with the trimmed name, or null when cancelled. check(name) returns an error
 * text to show (the dialog stays open) or nothing.
 */
function askName({ title, note, value, ok, check, input = true }) {
  const dlg = $('#nameDlg'), inp = $('#ndName'), err = $('#ndErr');
  inp.hidden = !input;
  $('#ndTitle').textContent = title; $('#ndNote').textContent = note || ''; $('#ndOk').textContent = ok;
  inp.value = value || ''; err.textContent = '';
  return new Promise(resolve => {
    const done = v => { dlg.onsubmit = null; $('#ndCancel').onclick = null; dlg.oncancel = null; inp.oninput = null; if (dlg.open) dlg.close(); resolve(v); };
    dlg.onsubmit = e => {
      e.preventDefault();
      if (!input) { done(true); return; }
      const v = inp.value.trim().replace(/\s+/g, ' '), bad = !v ? 'Give it a name.' : check && check(v);
      if (bad) { err.textContent = bad; inp.focus(); return; }
      done(v);
    };
    $('#ndCancel').onclick = () => done(null);
    dlg.oncancel = e => { e.preventDefault(); done(null); };                   // Esc
    inp.oninput = () => { err.textContent = ''; };
    dlg.showModal();
    if (input) { inp.focus(); inp.select(); } else $('#ndOk').focus();
  });
}
/** A yes/no question in the same dialog (the browser's own confirm box can be blocked where the lab is embedded). */
const askYes = (title, note, ok) => askName({ title, note, ok, input: false }).then(v => v === true);
/** Every AI training now gets the networks it may meet: a mix may draw on the others. */
function refreshPools() { for (const t of Object.values(trainings)) if (t.pool) t.pool.setNets(poolNets(t.id)); }
/** "+ New trainer": a plain trainer, learning like Tabula rasa, starting from nothing. */
async function addTrainer() {
  const num = (state.trainerSeq || 0) + 1;
  const name = await askName({ title: 'New trainer', note: 'A plain trainer that learns like Tabula rasa. Load a network file into it, or train it from nothing.',
    value: 'Trainer ' + num, ok: 'Add trainer',
    check: v => NETS.some(n => n.name.toLowerCase() === v.toLowerCase()) ? 'Another AI already has that name.' : '' });
  if (!name) return;
  state.trainerSeq = num;
  const x = { id: 'trainer' + num, name }, n = trainerNet(x);
  state.trainers.push(x); NETS.push(n); PRESETS.push(...netPresets(n));
  state.training[n.id] = freshRecord();
  netData[n.id] = net3ToData(net3Create()); netFound[n.id] = true;
  saveNet(n.id); save();
  refreshPools(); renderTraining(); renderPlayers();
  const card = $('#netCards').querySelector(`.netcard[data-id="${n.id}"]`);
  if (card) { card.scrollIntoView({ behavior: 'smooth', block: 'start' }); card.classList.add('fresh'); }
}
/** Deletes an added trainer with its network and record; the built-in AIs can't be removed. */
async function removeTrainer(id) {
  const n = NETS.find(x => x.id === id);
  if (!n || !n.added) return;
  if (tour.running) { reportError('Wait until the tournament has finished before removing a trainer.'); return; }
  if (!(await askYes(`Remove ${n.name}?`, 'Its network, its training record and everything it has learned are deleted.', 'Remove'))) return;
  if (manual && manual.id === id) finishManual();
  if (trainings[id]) await stopTraining(id);
  NETS.splice(NETS.indexOf(n), 1);
  for (let i = PRESETS.length - 1; i >= 0; i--) if (PRESETS[i].kind === 'net' && PRESETS[i].net === id) PRESETS.splice(i, 1);
  state.trainers = state.trainers.filter(x => x.id !== id);
  delete state.training[id];
  delete watchChoice[id];
  forgetNet(id);
  dropNetRefs(id);
  save(); refreshPools(); renderTraining(); renderPlayers();
}

async function trainAction(action, id) {
  if (action === 'add') { addTrainer(); return; }
  if (action === 'remove') { removeTrainer(id); return; }
  const n = NETS.find(x => x.id === id);
  if (action === 'train') { if (trainings[id]) stopTraining(id); else startTraining(id); }
  if (action === 'test') testNow(id);
  if (action === 'lrreset') {                                                  // step sizes back to the AI's start, halvings from scratch
    const rec = state.training[id];
    rec.lr = null;
    if (sizeOn(id)) for (const v of SIZE_VARIANTS(NETS.find(n => n.id === id))) rec.size.nets[v.key].lr = null;
    if (rec.tests.length) for (const lr of stepSizes(id)) lr.wait = EMA_WAIT;   // the averages still hold the old step's results
    sendRates(id); logRate(id);
    save(); renderTraining();
  }
  if (action === 'lib') {                                                      // a library session, then back to the usual training
    const rec = state.training[id], size = libSessionSize(rec, trainingSettings().evalEvery);
    if (rec.libSession) {                                                      // a toggle
      const ls = rec.libSession, t = trainings[id], q = t ? t.libQueued || 0 : 0, every = trainingSettings().evalEvery;
      if (ls.stopping) { ls.until = ls.full; delete ls.stopping; delete ls.full; }   // on again: the whole session
      else {                                                                   // off: finish the current test interval, then stop
        const played = rec.games + rec.teacherGames + q, rest = (every - played % every) % every;
        ls.full = ls.until; ls.stopping = true;
        ls.until = Math.min(ls.until, rec.teacherGames + q + rest);
        if (!t && ls.until <= rec.teacherGames) { rec.libSession = null; logPeriod(id); }
      }
      save(); renderTraining(); return;
    }
    if (!size) return;
    rec.libSession = { until: rec.teacherGames + size };
    logPeriod(id); save();
    if (!trainings[id]) startTraining(id); else renderTraining();
  }
  if (action === 'lrboost') {                                                  // 0.00025, then halved at each test down to the floor
    for (const lr of stepSizes(id)) Object.assign(lr, { rate: LR_PEAK, mode: 'boost', below: 0 });
    sendRates(id); logRate(id);
    save(); renderTraining();
  }
  if (action === 'lrcycle') {                                                  // a toggle
    const on = lrOf(state.training[id]).mode !== 'cycle';
    for (const lr of stepSizes(id)) {
      if (on) Object.assign(lr, { mode: 'cycle', below: 0, aligned: false, dir: 'down', atTest: true });   // the step changes at a test, never in between
      else { Object.assign(lr, { mode: null, wait: EMA_WAIT, below: 0 }); delete lr.atTest; }   // the step stays; the usual rule after its wait
    }
    save(); renderTraining();
  }
  if (action === 'watch') {
    const vs = watchChoice[id] || 'self', f = randomDecks();
    const me = { name: n.name, spec: { kind: 'net', net: id, play: { replies: false, explore: 0 } } };   // playing alone, as in its tests
    const them = vs === 'self' ? { name: n.name + ' (its twin)', spec: me.spec } : { name: nameOf(vs), spec: specOf(vs) };
    watchGame([me, them], f);
  }
  if (action === 'download') {
    const blob = new Blob([JSON.stringify({ name: n.name, id, training: state.training[id], network: netData[id] })], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = `three-bases-${id}-${state.training[id].games}-games.json`;
    document.body.appendChild(a); a.click(); a.remove();
  }
  if (action === 'netonly') {                                                  // the network alone, named by its latest scheduled test
    const last = state.training[id].tests.filter(q => !q.net && q.mode === 'alone' && !q.manual).pop();
    const rate = last ? `${Math.round(testRate(last) * 100)}%` : 'untested';
    const data = netData[id];                                                  // the network as it is now, not after the dialog
    askName({ title: 'Export network', note: `The network alone, without its training record. The name is used for the file and is shown when the network is loaded.`,
      value: `${n.name} ${rate}`, ok: 'Export',
      check: v => /[\\/:*?"<>|]/.test(v) ? 'A name can\'t contain \\ / : * ? " < > |' : '' }).then(name => {
      if (!name) return;
      const blob = new Blob([JSON.stringify({ name, id, network: data })], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = `${name}.json`;
      document.body.appendChild(a); a.click(); a.remove();
    });
  }
  if (action === 'load') {
    const input = document.createElement('input');
    input.type = 'file'; input.accept = '.json,application/json';
    input.onchange = async () => {
      try {
        const f = JSON.parse(await input.files[0].text());
        if (!usable(f.network, n)) throw new Error('that network was made for a different version of the game, or for another of the networks');
        if (trainings[id]) await stopTraining(id);
        netData[id] = f.network;
        if (f.training) state.training[id] = { ...freshRecord(), ...f.training };
        saveNet(id); save(); renderTraining();
      } catch (e) { reportError('Could not load that file: ' + e.message); }
    };
    input.click();
  }
  if (action === 'reset' && await askYes(`Start ${n.name} over?`, 'It goes back to knowing nothing. Everything it has learned is lost.', 'Start over')) {
    if (manual && manual.id === id) finishManual();
    const go = () => {
      const keepSize = sizeOn(id);
      netData[id] = net3ToData(net3Create());
      state.training[id] = freshRecord();
      saveNet(id); save();
      if (keepSize) setSizeCheck(id, true);                                   // the size check starts over too
      renderTraining();
    };
    if (trainings[id]) stopTraining(id).then(go); else go();
  }
}


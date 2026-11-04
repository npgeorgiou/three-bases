/* =====================================================================
   Tabs and start-up
   ===================================================================== */

function showTab(which) {
  for (const [tab, page, k] of [['#tabTrain', '#trainPage', 'train'], ['#tabTour', '#tourPage', 'tour'], ['#tabTune', '#tunePage', 'tune'], ['#tabDecks', '#decksPage', 'decks']]) {
    $(tab).setAttribute('aria-selected', which === k); $(page).hidden = which !== k;
  }
  if (which === 'tune') renderTune();
  if (which === 'decks') renderDs();
}
$('#tabTrain').addEventListener('click', () => showTab('train'));
$('#tabTour').addEventListener('click', () => showTab('tour'));
$('#tabTune').addEventListener('click', () => showTab('tune'));
$('#tabDecks').addEventListener('click', () => showTab('decks'));
$('#dsThreads').value = CORES;
$('#tuThreads').value = CORES;
$('#tThreads').value = CORES;
$('#threads').value = CORES;
$('#exportLab').addEventListener('click', exportLab);
/** The top settings are saved with the rest and restored on the next visit. */
renderTestOpp();
const SETTING_INPUTS = ['#tThreads', '#tExplore', '#tUses', '#tEvalEvery', '#tEvalGames', '#tMirror'];
if (!state.testGames100) { if (state.settings) delete state.settings['#tEvalGames']; state.testGames100 = true; save(); }   // once: test games go to the new default, 100
for (const sel of SETTING_INPUTS) {
  const el = $(sel), saved = (state.settings || {})[sel];
  if (saved !== undefined) { if (el.type === 'checkbox') el.checked = saved; else el.value = saved; }
  el.addEventListener('change', () => {
    state.settings = state.settings || {};
    state.settings[sel] = el.type === 'checkbox' ? el.checked : el.value;
    save();
    if (sel === '#tMirror') for (const t of Object.values(trainings)) for (const l of Object.values(t.learners)) l.w.postMessage({ type: 'mirror', on: el.checked });
    if (sel === '#tUses') for (const t of Object.values(trainings)) for (const l of Object.values(t.learners)) l.w.postMessage({ type: 'uses', uses: trainingSettings().uses });
    if (sel === '#tThreads') rebalancePools();                                   // the new total is shared out at once
  });
}
window.addEventListener('beforeunload', () => { for (const id of Object.keys(trainings)) saveNets(id); if (Object.keys(trainings).length) save(); });
for (const old of ['scholar', 'apprentice', 'wanderer']) dropNetRefs(old);   // removed AIs: out of the tournament's entries, training opponents and mixes
for (const r of Object.values(state.training)) if (Array.isArray(r.mix)) r.mix = r.mix.filter(k => !k.startsWith('net:') || NETS.some(n => 'net:' + n.id === k));
save();
state.chosen = state.chosen.filter(p => !NETS.some(n => p === 'net-' + n.id));   // the removed reply-check players
renderTraining();
renderPlayers();
renderResults();
if (state.plan) { $('#start').textContent = 'Resume'; renderProgress(); }

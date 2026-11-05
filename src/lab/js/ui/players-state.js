/* =====================================================================
   AI lab: training the learning networks, tournaments between AIs, and watching games.
   Games run in background workers; each training network also uses one or more learner workers, taken from "Games at once".
   ===================================================================== */

const $ = sel => document.querySelector(sel);
const esc = t => String(t).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const STORE = 'threeBases.lab.v1', NET_STORE = id => `threeBases.lab.v1.net.${id}`;
const ROUND_CAP = 40, ACTION_CAP = 500;          // a game still running then ends unfinished (a loss for both)
const CORES = Math.max(1, (navigator.hardwareConcurrency || 2) - 1);

/** Trainers added with "+ New trainer": plain ones that learn like Tabula rasa. Read early, as NETS needs them. */
const trainerNet = x => ({ id: x.id, name: x.name, added: true,
  desc: 'An added trainer. Starts knowing nothing, or from a network file you load, and learns only from its own training games (against itself, or the opponent chosen below): every position is labelled with who went on to win.' });
const savedTrainers = (() => {
  try { const s = JSON.parse(localStorage.getItem(STORE) || 'null'); return s && Array.isArray(s.trainers) ? s.trainers : []; }
  catch (e) { return []; }
})();
/** The learning networks: the three built-in AIs, then the added trainers. */
const NETS = [
  { id: 'tabula', name: 'Tabula rasa',
    desc: 'Starts knowing nothing and learns only from its own training games (against itself, or the opponent chosen below): every position is labelled with who went on to win.' },
  ...savedTrainers.map(trainerNet),
];

/** The three ways a learning AI can be entered as a player. */
const netPresets = n => [                      // (the reply-check version was removed)
    { id: 'net-' + n.id + '-alone', name: n.name + ' · alone', kind: 'net', net: n.id, play: { replies: false, explore: 0 },
      desc: 'Learning AI, playing as in its tests: the network scores the board after each of its moves and it plays the best. Guesses the opponent\'s hand. ' + n.desc },
    { id: 'net-' + n.id + '-search', name: n.name + ' · Benchmark search', kind: 'net', net: n.id, play: { search: true },
      desc: 'Learning AI inside the earlier Benchmark\'s look-ahead: the same search and the same view of the opponent\'s hand, but the network scores every position. ' + n.desc },
];
/** The players. */
const PRESETS = [
  { id: 'bench', name: 'Benchmark', kind: 'bench', desc: 'The game\'s AI. Sees the opponent\'s hand.' },
  { id: 'random', name: 'Random player', kind: 'random', desc: 'A baseline. Picks a kind of move at random (deploy, move, attack, spell or pass), then a move of that kind.' },
  { id: 'ifelse', name: 'ifelse AI', kind: 'ifelse', desc: 'Sees both hands and searches the real position; every judgement is a weighted term, with the values found by its tuning (the starting values until it finds better).',
    get cfg() { return (state.ifelse && state.ifelse.v === 4 && state.ifelse.best) || {}; } },
  ...NETS.flatMap(netPresets),
];

/* ---------- saved state ---------- */

const freshRecord = () => ({ games: 0, teacherGames: 0, positions: 0, steps: 0, loss: null, accuracy: null, tests: [], failed: 0, lastError: '' });
/**
 * One open lab at a time: two tabs would overwrite each other's saved progress. An open lab writes a heartbeat
 * every 2 seconds (a background tab only about once a minute); a second one that finds a heartbeat from the
 * last 90 seconds refuses to run. Closing or reloading the lab removes its heartbeat at once.
 */
const LAB_ALIVE = 'threeBases.lab.alive', labTab = Math.random().toString(36).slice(2);
let refused = false;
try {
  const alive = JSON.parse(localStorage.getItem(LAB_ALIVE) || 'null');
  if (alive && alive.id !== labTab && Date.now() - alive.t < 90000) refused = true;   // browsers slow a background tab's timers to about once a minute
} catch (e) { /* no heartbeat */ }
if (refused) {
  document.body.innerHTML = '<div class="refused"><h1>The lab is already open</h1><p>It is running in another tab or window of this browser. Two open labs would overwrite each other\'s saved progress, so this one stays closed. Close the other one first, then reload this page.</p></div>';
  throw new Error('The lab is already open in another tab.');
}
const beat = () => { try { localStorage.setItem(LAB_ALIVE, JSON.stringify({ id: labTab, t: Date.now() })); } catch (e) { /* storage full */ } };
beat();
/**
 * A background tab's own timers are slowed to about once a minute by the browser, but messages from a worker
 * keep arriving on time. This tiny worker ticks every second; the page uses it to move cores between learning
 * and games, and for its heartbeat.
 */
const ticks = [];
try {
  const tickWorker = new Worker(URL.createObjectURL(new Blob(['setInterval(() => postMessage(0), 1000);'], { type: 'text/javascript' })));
  tickWorker.onmessage = () => { for (const f of ticks) f(); };
} catch (e) { setInterval(() => { for (const f of ticks) f(); }, 1000); }
let beatCount = 0;
ticks.push(() => { if (++beatCount % 2 === 0) beat(); });
window.addEventListener('pagehide', () => { try { const a = JSON.parse(localStorage.getItem(LAB_ALIVE) || 'null'); if (a && a.id === labTab) localStorage.removeItem(LAB_ALIVE); } catch (e) { /* ignore */ } });

let state = load();
for (const n of NETS) if (!state.training[n.id]) state.training[n.id] = freshRecord();   // a network added since the last visit
if (!Array.isArray(state.trainers)) state.trainers = [];
function load() {
  try {
    const s = JSON.parse(localStorage.getItem(STORE) || 'null');
    if (s && s.results && s.training) return s;
  } catch (e) { /* nothing saved, or unreadable */ }
  return {
    chosen: ['bench', 'ifelse'], results: [], plan: null,
    training: Object.fromEntries(NETS.map(n => [n.id, freshRecord()])),
  };
}
function save() {
  try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (e) { /* storage full or blocked: keep going */ }
}
/**
 * Networks' weights, kept apart from the rest because they are large. They are saved in the browser's database
 * (IndexedDB), which has room for bigger networks; networks saved earlier in the smaller browser storage are
 * still read, and moved over the next time they are saved. Training waits until the database has been read.
 */
const netData = {};
const usable = (data, n) => {                                   // a network of this AI's input format and its standard size
  try { return net3Valid(data, F3.hidden); }
  catch (e) { return false; }
};
/**
 * The size check: two extra networks, More nodes and Extra layer, trained on exactly the same lessons as the
 * AI's own network, to see whether a different size would learn better. It can only be switched on before the
 * AI's first game (or right after "Start over"), so all three networks start from nothing together and compare
 * fairly. Each has its own step size and halving schedule, judged on its own test results.
 */
const SIZE_VARIANTS = n => {
  const h = F3.hidden, rec = state.training[n.id];
  // the lessons check: same-size copies whose lessons take another share from their own value of the next position
  if (rec && rec.size && rec.size.kind === 'lessons') return [
    { key: 'next15', label: 'Next move 15%', hidden: h.slice(), next: 0.15, cls: 'c2' },
    { key: 'next45', label: 'Next move 45%', hidden: h.slice(), next: 0.45, cls: 'c3' },
  ];
  return [
    { key: 'big', label: 'More nodes', hidden: h.map(x => 2 * x), cls: 'c2' },
    { key: 'deep', label: 'Extra layer', hidden: [...h, Math.max(4, h[h.length - 1] / 2)], cls: 'c3' },
  ];
};
const sizeOn = id => !!(state.training[id].size && state.training[id].size.on);
const lessonsOn = id => sizeOn(id) && state.training[id].size.kind === 'lessons';
/** Every AI's lessons are 30% its own win chance one move later (the lessons check of 5 Nov 2026 found it best). */
const NEXT_SHARE = 0.3;
/** Per trained network, its game-worker name and its share learned from the next position (the size check's learn the AI's). */
const nextShares = id => [{ net: 'train', share: NEXT_SHARE },
  ...(lessonsOn(id) ? SIZE_VARIANTS(NETS.find(n => n.id === id)).map(v => ({ net: 'train~' + v.key, share: v.next })) : [])];
const copyId = (id, key) => id + '~' + key;
/** The networks a training run learns: the AI's own, then the size check's (if on). */
const trainNets = id => [netData[id], ...(sizeOn(id) ? SIZE_VARIANTS(NETS.find(n => n.id === id)).map(v => netData[copyId(id, v.key)]) : [])];
/** The networks the game workers need: 'train', and 'train~big' and 'train~deep' for the size check's test games. */
const playable = d => (d ? { enc: d.enc, arch: d.arch, weights: d.weights } : d);   // no learning momentum: games don't need it
const poolNets = id => {
  const out = { train: playable(netData[id]) }, o = state.training[id].opponent || 'self';
  const mix = o === 'mix' ? mixOf(id) : [];
  for (const n of NETS) if (n.id !== id && (mix.includes('net:' + n.id) || o === 'net:' + n.id)) out['opp:' + n.id] = playable(netData[n.id]);   // opponents in use
  if (sizeOn(id)) for (const v of SIZE_VARIANTS(NETS.find(n => n.id === id))) out['train~' + v.key] = playable(netData[copyId(id, v.key)]);
  if (netData.testopp) out.testopp = playable(netData.testopp);              // a frozen test opponent
  return out;
};
for (const n of NETS) {
  try { netData[n.id] = JSON.parse(localStorage.getItem(NET_STORE(n.id)) || 'null'); } catch (e) { netData[n.id] = null; }
  if (netData[n.id] && !usable(netData[n.id], n)) netData[n.id] = null;   // made for another version
  if (!netData[n.id]) netData[n.id] = net3ToData(net3Create());
}
let netsReady = false;
const netFound = {};                          // net id -> a usable saved network was found
for (const n of NETS) { let d = null; try { d = JSON.parse(localStorage.getItem(NET_STORE(n.id)) || 'null'); } catch (e) { d = null; } if (d && usable(d, n)) netFound[n.id] = true; }
const netDb = new Promise(resolve => {
  try {
    const req = indexedDB.open('threeBases.lab.nets', 1);
    req.onupgradeneeded = () => req.result.createObjectStore('nets');
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => resolve(null);
  } catch (e) { resolve(null); }
});
netDb.then(db => {
  if (!db) { netsReady = true; renderTestOpp(); renderTraining(); return; }
  const tx = db.transaction('nets', 'readonly'), store = tx.objectStore('nets');
  const tq = store.get('testopp');
  tq.onsuccess = () => { if (tq.result && net3Valid(tq.result, F3.hidden)) netData.testopp = tq.result; };
  for (const n of NETS) {
    const req = store.get(n.id);
    req.onsuccess = () => { if (req.result && usable(req.result, n)) { netData[n.id] = req.result; netFound[n.id] = true; } };
    for (const v of SIZE_VARIANTS(n)) {                                 // the size check's networks
      const r2 = store.get(copyId(n.id, v.key));
      r2.onsuccess = () => { if (r2.result && net3Valid(r2.result, v.hidden)) netData[copyId(n.id, v.key)] = r2.result; };
    }
  }
  tx.oncomplete = tx.onerror = () => {
    for (const n of NETS) if (!netFound[n.id] && state.training[n.id].games + state.training[n.id].teacherGames > 0) {
      state.training[n.id] = freshRecord();                                // its saved network was of an older kind: it starts over
      save();
    }
    for (const n of NETS) if (sizeOn(n.id) && SIZE_VARIANTS(n).some(v => !netData[copyId(n.id, v.key)])) state.training[n.id].size.on = false;   // missing: check off
    if (testOpp().kind === 'net' && !netData.testopp) state.testOpp = { kind: 'bench' };   // its network is gone: back to the Benchmark
    netsReady = true; renderTestOpp(); renderTraining();
  };
});
/**
 * The shared library of teacher games (games played earlier between coded AIs). Each game is kept as the board after
 * the starting-hand redraws plus the list of moves played; after the redraws the rules involve no chance, so
 * replaying the moves gives exactly the same game, at a tiny fraction of the cost of the two players thinking.
 * Every AI that learns from teacher games takes the library's games
 * in order and only has new ones played when it has used them all; those are added for the others. Kept in the
 * browser's database; "Start over" goes back to the library's first game.
 */
const LIB = { games: [], ready: false };
let libLoaded = null; const libLoadedP = new Promise(r => { libLoaded = r; });
const libDb = new Promise(resolve => {
  try {
    const req = indexedDB.open('threeBases.lab.teacherGames', 1);
    req.onupgradeneeded = () => req.result.createObjectStore('games', { autoIncrement: true });
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => resolve(null);
  } catch (e) { resolve(null); }
});
libDb.then(db => {
  if (!db) { LIB.ready = true; libLoaded(); return; }
  const req = db.transaction('games', 'readonly').objectStore('games').getAll();
  req.onsuccess = () => { LIB.games = (req.result || []).filter(g => g && g.init && g.actions && g.v === LIB_VERSION); LIB.ready = true; libLoaded(); renderTrainingSoon(); };
  req.onerror = () => { LIB.ready = true; libLoaded(); };
});
const LIB_VERSION = 2;   // library games are kept only for the cards they were played with
/** How many library games this AI has not learned from yet. */
const libUnused = rec => Math.max(0, LIB.games.length - (rec.libCursor || 0));
/** A library session takes whole test intervals of games, so tests keep falling where they did. */
const libSessionSize = (rec, every) => Math.floor(libUnused(rec) / every) * every;
/** The next library game this AI has not learned from yet (its place), or null when it has used them all. */
function libNext(rec) {
  if (!LIB.ready) return null;
  const c = rec.libCursor || 0;
  if (c >= LIB.games.length) return null;
  rec.libCursor = c + 1;
  return c;
}
function deleteNet(id) {
  netDb.then(db => { if (db) db.transaction('nets', 'readwrite').objectStore('nets').delete(id); });
}
function saveNet(id) {
  const data = netData[id];
  netDb.then(db => {
    const old = () => { try { localStorage.setItem(NET_STORE(id), JSON.stringify(data)); } catch (e) { /* too large for this browser's storage */ } };
    if (!db) { old(); return; }
    const tx = db.transaction('nets', 'readwrite');
    tx.objectStore('nets').put(data, id);
    tx.oncomplete = () => { try { localStorage.removeItem(NET_STORE(id)); } catch (e) { /* nothing to free */ } };
    tx.onerror = old;
  });
}

/** The learners' networks, in trainNets order, back into netData. */
function storeNets(id, datas) {
  netData[id] = datas[0];
  if (sizeOn(id) && datas.length > 1) SIZE_VARIANTS(NETS.find(n => n.id === id)).forEach((v, i) => { if (datas[i + 1]) netData[copyId(id, v.key)] = datas[i + 1]; });
}
function saveNets(id) {
  saveNet(id);
  if (sizeOn(id)) for (const v of SIZE_VARIANTS(NETS.find(n => n.id === id))) saveNet(copyId(id, v.key));
}
/** A network the lab no longer has (with its size-check copies) leaves both stores. */
function forgetNet(id) {
  for (const k of [id, copyId(id, 'big'), copyId(id, 'deep')]) {
    delete netData[k]; deleteNet(k);
    try { localStorage.removeItem(NET_STORE(k)); } catch (e) { /* nothing to free */ }
  }
}
/** Nothing may still point at a removed network: it leaves the tournament's entries, and an AI training against it
 *  trains against itself from the next game on. */
function dropNetRefs(id) {
  state.chosen = state.chosen.filter(p => p !== 'net-' + id && !p.startsWith('net-' + id + '-'));
  for (const n of NETS) {
    const r = state.training[n.id];
    if (r && r.opponent === 'net:' + id) { r.opponent = 'self'; logPeriod(n.id); }
  }
}
/* Leftovers of earlier versions: AIs that were removed (Scholar, Apprentice, Wanderer) lose their progress and networks, and
   setting fields no longer used are dropped from every record. */
for (const old of ['scholar', 'apprentice', 'wanderer']) if (state.training[old]) { delete state.training[old]; forgetNet(old); }
for (const r of Object.values(state.training)) for (const f of ['td', 'tdOn', 'teacher', 'learnFrom', 'choiceLessons', 'choice', 'closs', 'watchLib', 'libOwn', 'libReplayed', 'decay', 'round', 'roundStart', 'fullFrom', 'noRandomStreak', 'batchMoves', 'batchRandom']) delete r[f];
/* Any other key of the lab's own in this browser that the lab no longer uses (older networks, older formats) goes;
   the games' keys (threeBases.game…, threeBases.v2…) are left alone. */
try {
  const keep = new Set([STORE, LAB_ALIVE, ...NETS.flatMap(n => [n.id, copyId(n.id, 'big'), copyId(n.id, 'deep')].map(NET_STORE)), NET_STORE('testopp')]);
  for (let i = localStorage.length - 1; i >= 0; i--) {
    const k = localStorage.key(i);
    if (k && k.startsWith('threeBases.lab') && !keep.has(k)) localStorage.removeItem(k);
  }
} catch (e) { /* storage unavailable */ }
netDb.then(db => {                                     // the same for the network database
  if (!db) return;
  const ids = new Set([...NETS.flatMap(n => [n.id, copyId(n.id, 'big'), copyId(n.id, 'deep')]), 'testopp']);
  const tx = db.transaction('nets', 'readwrite'), store = tx.objectStore('nets'), req = store.getAllKeys();
  req.onsuccess = () => { for (const k of req.result) if (!ids.has(k)) store.delete(k); };
});

const tune = { running: false, pool: null, k: 0 };          // the ifelse AI's tuning, while it runs
const players = () => PRESETS;
const playerById = id => players().find(p => p.id === id);
const nameOf = id => (playerById(id) || { name: id }).name;

/** What a worker (or the page) needs to play as this player. */
function specOf(id) {
  const p = playerById(id);
  if (p.kind === 'bench') return { kind: 'bench' };
  if (p.kind === 'random') return { kind: 'random' };
  if (p.kind === 'net') return { kind: 'net', net: p.net, play: p.play };
  return { kind: 'ifelse', cfg: ifelseFull(p.cfg) };
}


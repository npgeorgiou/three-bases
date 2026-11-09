/* =====================================================================
   ifelse tuning by LESSONS (ifelse-lessons.js). A round: if lessons are wanted, games are played to make them (the
   centre's numbers against the opponents ticked, seats in turn; only the centre's own turns become lessons); then every try (and the centre) is graded on every lesson, in blocks of LESSON_BLOCK lessons, one
   block per job; its score is 1 minus its average loss; CMA-ES moves the centre as with games. After each round a
   quarter of the lessons, the oldest, are remade with the new centre; every 10th round the centre plays 100 games
   against the opponents ticked (looking 1 move ahead), shown on the chart. Lessons are kept in the browser's database.
   ===================================================================== */
const LESSON_BLOCK = 50, LESSON_RENEW = 0.25, STRENGTH_EVERY = 10, STRENGTH_GAMES = 100;
/** list: the lessons, oldest first; need: new ones still wanted before the next round; spare: new ones that came in
 *  after enough were made (they wait for the next round's renewal, so the lessons never change during a round). */
const LESSONS = { list: [], cards: '', need: 0, spare: [], seed: 0 };
/** The cards' stamp: lessons made with other cards (stats, texts) are thrown away. */
const lessonCards = () => { let h = 2166136261; const t = JSON.stringify(Object.entries(CARDS).map(([k, c]) => [k, c.sup, c.str, c.def, c.text])); for (let i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h.toString(36); };
const lessonDb = new Promise(resolve => {
  try {
    const req = indexedDB.open('threeBases.lab.lessons', 2);
    req.onupgradeneeded = () => { if (!req.result.objectStoreNames.contains('lessons')) req.result.createObjectStore('lessons'); };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => resolve(null);
  } catch (e) { resolve(null); }
});
lessonDb.then(db => {
  if (!db) return;
  const req = db.transaction('lessons', 'readonly').objectStore('lessons').get('set');
  req.onsuccess = () => { const v = req.result; if (v && v.cards === lessonCards() && v.list.every(l => l.result != null)) Object.assign(LESSONS, { list: v.list.map(lessonOnly), cards: v.cards, need: v.need || 0, spare: (v.spare || []).map(lessonOnly), seed: v.seed || 0 }); renderTuneStatus(); };
});
/** A lesson as kept: the position, the side to move and the result (anything else saved with it is dropped). */
const lessonOnly = l => ({ s: l.s, side: l.side, result: l.result });
function saveLessons() {
  lessonDb.then(db => { if (db) db.transaction('lessons', 'readwrite').objectStore('lessons').put({ list: LESSONS.list, cards: LESSONS.cards, need: LESSONS.need, spare: LESSONS.spare, seed: LESSONS.seed }, 'set'); });
}
const lessonTarget = () => tuneState().lessonN || 1000;               // how many lessons each try is graded on (kept with the tuning)
/** Lessons are ready when there are enough, all made with these cards, and none are still wanted for this round. */
function lessonsReady() {
  if (LESSONS.cards !== lessonCards()) { LESSONS.list = []; LESSONS.spare = []; LESSONS.cards = lessonCards(); }
  if (LESSONS.list.length < lessonTarget() && LESSONS.need < lessonTarget() - LESSONS.list.length) LESSONS.need = lessonTarget() - LESSONS.list.length;
  return LESSONS.need === 0;
}
const lessonBlocks = () => Math.ceil(lessonTarget() / LESSON_BLOCK);
/** After a round: a quarter of the lessons are remade with the new centre; every 10th round the centre plays the Benchmark. */
function lessonsAfterRound(st) {
  LESSONS.need = Math.max(LESSONS.need, Math.ceil(lessonTarget() * LESSON_RENEW));
  addLessons(LESSONS.spare.splice(0, LESSONS.need));                  // the spare ones from the last making count first
  if (st.gen % STRENGTH_EVERY === 0) st.strength = { gen: st.gen - 1, values: { ...st.best }, res: Array(STRENGTH_GAMES).fill(null) };
  saveLessons();
}
/** Games against the Benchmark being played now (not saved: after a pause they are played again). */
const strengthRunning = new Set();
/** The next job: a game against the Benchmark when one is due, a game to make lessons from while lessons are wanted, else a block of lessons for a try. */
function lessonJob(st, c) {
  const g = st.strength;
  if (g) {
    const k = g.res.findIndex((x, i) => x === null && !strengthRunning.has(i));
    if (k >= 0) {
      strengthRunning.add(k);
      const seat = k % 2, mine = { kind: 'ifelse', cfg: { ...ifelseFull(g.values), depth: 1 } }, opp = tuneOppSpec(st.opps[Math.floor(k / 2) % st.opps.length], 1);
      return { key: 'strength-' + g.gen + '-' + k, lesson: 'strength', k, seat, specs: seat === 0 ? [mine, opp] : [opp, mine],
        seed: 900001 + g.gen * 1000 + k, decks: DECK_PAIRS[(g.gen * 7 + Math.floor(k / 2)) % DECK_PAIRS.length] };
    }
  }
  if (!lessonsReady()) {                                              // every free core plays a game to make lessons
    const seed = 7001 + LESSONS.seed++;
    const opp = tuneOppSpec(st.opps[seed % st.opps.length], 1), seat = Math.floor(seed / st.opps.length) % 2;   // the ticked opponents and seats in turn
    return { key: 'lesson-make-' + seed, lesson: 'make', msg: { type: 'lessonMake', seed, opp, seat, cfg: ifelseFull(st.best), actionCap: ACTION_CAP, roundCap: ROUND_CAP, decks: DECK_PAIRS[seed % DECK_PAIRS.length] } };
  }
  if (!c) { newGeneration(); c = st.cand; if (tune.pool) tune.pool.setInit([{ type: 'lessons', lessons: LESSONS.list }]); }
  const pick = tuneNextDeal(c);
  if (!pick) return null;
  const [i, gi] = pick;
  return { key: 'lesson' + st.gen + '-' + i + '-' + gi, lesson: 'grade', i, gi, gen: st.gen,
    msg: { type: 'lessonGrade', cfg: ifelseFull(tuneDecode(c.xs[i], 1)), from: gi * LESSON_BLOCK, to: (gi + 1) * LESSON_BLOCK } };
}
/** All lessons thrown away (Start over): new ones are made at the next start, with the starting values. */
function clearLessons() { LESSONS.list = []; LESSONS.spare = []; LESSONS.need = 0; saveLessons(); renderTuneStatus(); }
/** New lessons go in at the end; the oldest go when there are more than wanted. */
function addLessons(ls) {
  if (!ls.length) return;
  LESSONS.list.push(...ls);
  if (LESSONS.list.length > lessonTarget()) LESSONS.list.splice(0, LESSONS.list.length - lessonTarget());
  LESSONS.need = Math.max(0, LESSONS.need - ls.length);
}
function lessonResult(r, job) {
  const st = tuneState();
  if (job.lesson === 'strength') {
    const g = st.strength;
    strengthRunning.delete(job.k);
    if (!g || job.key !== 'strength-' + g.gen + '-' + job.k) return;
    g.res[job.k] = r.winner === job.seat ? 1 : r.winner === 'draw' ? 0.5 : 0;
    if (g.res.every(x => x !== null)) {
      const e = st.hist.find(x => !x.mark && x.gen === g.gen);
      if (e) e.bench = g.res.reduce((a, b) => a + b, 0) / g.res.length;
      st.strength = null; save(); renderTune();
    }
    return;
  }
  if (job.lesson === 'make') {
    const take = r.lessons.slice(0, LESSONS.need);
    LESSONS.spare.push(...r.lessons.slice(take.length));
    if (LESSONS.spare.length > lessonTarget()) LESSONS.spare.splice(0, LESSONS.spare.length - lessonTarget());
    addLessons(take);
    if (LESSONS.need === 0) saveLessons();
    renderTuneStatus();
    return;
  }
  tuneScore(job, r.n ? 1 - r.sum / r.n : 0);
}

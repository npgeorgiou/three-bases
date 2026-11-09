/* =====================================================================
   ifelse tuning by LESSONS (ifelse-lessons.js). A round: if lessons are wanted, games are played to make them (the
   centre's numbers against the opponents ticked, seats in turn; every one of the centre's own turns becomes a lesson);
   then every try (and the centre) is graded on every lesson of the kept games, in blocks of LESSON_BLOCK lessons, one
   block per job; its score is 1 minus its average loss; CMA-ES moves the centre as with games. After each round a
   quarter of the games, the oldest, are replaced by new ones played with the new centre; every 5th round the centre
   plays 100 games against the opponents ticked (looking 1 move ahead), shown on the chart. Lessons are kept in the
   browser's database.
   ===================================================================== */
const LESSON_BLOCK = 50, LESSON_RENEW = 0.25, STRENGTH_EVERY = 5, STRENGTH_GAMES = 100;
/** games: each kept game's lessons, oldest game first; list: all their lessons in one list (what the workers grade);
 *  need: new games still wanted before the next round; spare: new games that came in after enough were played (they
 *  wait for the next round's renewal, so the lessons never change during a round). */
const LESSONS = { games: [], list: [], cards: '', need: 0, spare: [], seed: 0 };
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
  const store = db.transaction('lessons', 'readwrite').objectStore('lessons'), req = store.get('games');
  store.delete('set');                                                // lessons kept without their games can't be counted by game
  req.onsuccess = () => { const v = req.result; if (v && v.cards === lessonCards()) { Object.assign(LESSONS, { games: v.games, cards: v.cards, need: v.need || 0, spare: v.spare || [], seed: v.seed || 0 }); LESSONS.list = LESSONS.games.flat(); } renderTuneStatus(); };
});
function saveLessons() {
  lessonDb.then(db => { if (db) db.transaction('lessons', 'readwrite').objectStore('lessons').put({ games: LESSONS.games, cards: LESSONS.cards, need: LESSONS.need, spare: LESSONS.spare, seed: LESSONS.seed }, 'games'); });
}
const lessonTarget = () => tuneState().lessonGames || 200;            // how many games' lessons each try is graded on (kept with the tuning)
/** Lessons are ready when enough games are kept, all played with these cards, and none are still wanted for this round. */
function lessonsReady() {
  if (LESSONS.cards !== lessonCards()) { LESSONS.games = []; LESSONS.list = []; LESSONS.spare = []; LESSONS.cards = lessonCards(); }
  if (LESSONS.games.length < lessonTarget() && LESSONS.need < lessonTarget() - LESSONS.games.length) LESSONS.need = lessonTarget() - LESSONS.games.length;
  return LESSONS.need === 0;
}
const lessonBlocks = () => Math.max(1, Math.ceil(LESSONS.list.length / LESSON_BLOCK));
/** After a round: a quarter of the games are replaced by new ones with the new centre; every 5th round the centre plays the opponents. */
function lessonsAfterRound(st) {
  LESSONS.need = Math.max(LESSONS.need, Math.ceil(lessonTarget() * LESSON_RENEW));
  addGames(LESSONS.spare.splice(0, LESSONS.need));                    // the spare games from the last making count first
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
function clearLessons() { LESSONS.games = []; LESSONS.list = []; LESSONS.spare = []; LESSONS.need = 0; saveLessons(); renderTuneStatus(); }
/** New games go in at the end; the oldest go when there are more than wanted. */
function addGames(gs) {
  if (!gs.length) return;
  LESSONS.games.push(...gs);
  if (LESSONS.games.length > lessonTarget()) LESSONS.games.splice(0, LESSONS.games.length - lessonTarget());
  LESSONS.list = LESSONS.games.flat();
  LESSONS.need = Math.max(0, LESSONS.need - gs.length);
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
    if (!r.lessons.length) return;                                    // unfinished game: no winner, it doesn't count
    if (LESSONS.need > 0) addGames([r.lessons]);
    else { LESSONS.spare.push(r.lessons); if (LESSONS.spare.length > lessonTarget()) LESSONS.spare.splice(0, LESSONS.spare.length - lessonTarget()); }
    if (LESSONS.need === 0) saveLessons();
    renderTuneStatus();
    return;
  }
  tuneScore(job, r.n ? 1 - r.sum / r.n : 0);
}

/* =====================================================================
   ifelse tuning by LESSONS (ifelse-lessons.js). A round: if lessons are wanted, games are played to make them (the
   centre's numbers against the opponents ticked, seats in turn; every one of the centre's own turns becomes a lesson);
   then every try (and the centre) is graded on every lesson of the kept games, in blocks of LESSON_BLOCK lessons, one
   block per job; its score is 1 minus its average loss; CMA-ES moves the centre as with games. After each round all
   games are thrown away and new ones are played with the new centre; every 5th round the centre
   plays 100 games against the opponents ticked (looking 1 move ahead), shown on the chart. Lessons are kept in the
   browser's database.
   ===================================================================== */
const LESSON_BLOCK = 50, STRENGTH_EVERY = 5, STRENGTH_GAMES = 100;
/** games: each game's lessons; list: all their lessons in one list (what the workers grade). */
const LESSONS = { games: [], list: [], cards: '', seed: 0 };
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
  req.onsuccess = () => { const v = req.result; if (v && v.cards === lessonCards()) { Object.assign(LESSONS, { games: v.games, cards: v.cards, seed: v.seed || 0 }); LESSONS.list = LESSONS.games.flat(); } renderTuneStatus(); };
});
function saveLessons() {
  lessonDb.then(db => { if (db) db.transaction('lessons', 'readwrite').objectStore('lessons').put({ games: LESSONS.games, cards: LESSONS.cards, seed: LESSONS.seed }, 'games'); });
}
const lessonTarget = () => tuneState().lessonGames || 200;            // how many games' lessons each try is graded on (kept with the tuning)
/** Games still to play before this round's grading. */
const lessonNeed = () => Math.max(0, lessonTarget() - LESSONS.games.length);
/** Lessons are ready when enough games are played, all with these cards. */
function lessonsReady() {
  if (LESSONS.cards !== lessonCards()) { LESSONS.games = []; LESSONS.list = []; LESSONS.cards = lessonCards(); }
  return lessonNeed() === 0;
}
const lessonBlocks = () => Math.max(1, Math.ceil(LESSONS.list.length / LESSON_BLOCK));
/** After a round: all games are thrown away and new ones are played with the new centre; every 5th round the centre plays the opponents. */
function lessonsAfterRound(st) {
  LESSONS.games = []; LESSONS.list = [];
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
    return { key: 'lesson-make-' + seed, lesson: 'make', gen: st.gen, msg: { type: 'lessonMake', seed, opp, seat, cfg: ifelseFull(st.best), actionCap: ACTION_CAP, roundCap: ROUND_CAP, decks: DECK_PAIRS[seed % DECK_PAIRS.length] } };
  }
  if (!c) { newGeneration(); c = st.cand; if (tune.pool) tune.pool.setInit([{ type: 'lessons', lessons: LESSONS.list }]); }
  const pick = tuneNextDeal(c);
  if (!pick) return null;
  const [i, gi] = pick;
  return { key: 'lesson' + st.gen + '-' + i + '-' + gi, lesson: 'grade', i, gi, gen: st.gen,
    msg: { type: 'lessonGrade', cfg: ifelseFull(tuneDecode(c.xs[i], 1)), from: gi * LESSON_BLOCK, to: (gi + 1) * LESSON_BLOCK } };
}
/** All lessons thrown away (Start over): new ones are made at the next start, with the starting values. */
function clearLessons() { LESSONS.games = []; LESSONS.list = []; saveLessons(); renderTuneStatus(); }
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
    // unfinished games (no winner), games from an earlier round and games beyond the number wanted don't count
    if (!r.lessons.length || job.gen !== st.gen || !lessonNeed()) return;
    LESSONS.games.push(r.lessons); LESSONS.list.push(...r.lessons);
    if (!lessonNeed()) saveLessons();
    renderTuneStatus();
    return;
  }
  tuneScore(job, r.n ? 1 - r.sum / r.n : 0);
}

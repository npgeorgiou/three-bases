/* =====================================================================
   ifelse tuning by FORESIGHT LESSONS (ifelse-lessons.js): first the lessons are made (positions from games, every move
   valued by the teacher at depth 3), then each generation every candidate, at depth 1, chooses a move in every lesson;
   its score is 1 minus its average loss. Candidates are graded in blocks of LESSON_BLOCK lessons, one block per job.
   The lessons are kept in the browser's database with the teacher's values and the cards they were made with.
   ===================================================================== */
const LESSON_BLOCK = 50, LESSON_EVERY = 7, LESSON_PER_GAME = 12;
const LESSONS = { list: [], teacher: null, cards: '', making: false, seed: 0 };
/** The cards' stamp: lessons made with other cards (stats, texts) are thrown away. */
const lessonCards = () => { let h = 2166136261; const t = JSON.stringify(Object.entries(CARDS).map(([k, c]) => [k, c.sup, c.str, c.def, c.text])); for (let i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h.toString(36); };
const lessonDb = new Promise(resolve => {
  try {
    const req = indexedDB.open('threeBases.lab.lessons', 1);
    req.onupgradeneeded = () => req.result.createObjectStore('lessons');
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => resolve(null);
  } catch (e) { resolve(null); }
});
lessonDb.then(db => {
  if (!db) return;
  const req = db.transaction('lessons', 'readonly').objectStore('lessons').get('set');
  req.onsuccess = () => { const v = req.result; if (v && v.cards === lessonCards()) Object.assign(LESSONS, { list: v.list, teacher: v.teacher, cards: v.cards }); renderTuneStatus(); };
});
function saveLessons() {
  lessonDb.then(db => { if (db) db.transaction('lessons', 'readwrite').objectStore('lessons').put({ list: LESSONS.list, teacher: LESSONS.teacher, cards: LESSONS.cards }, 'set'); });
}
const lessonTarget = () => tuneState().lessonN || 1000;               // how many lessons each candidate is graded on (kept with the tuning)
const lessonsReady = () => LESSONS.list.length >= lessonTarget() && LESSONS.cards === lessonCards();
const lessonBlocks = () => Math.ceil(lessonTarget() / LESSON_BLOCK);
/** Throw the lessons away; the next start makes new ones with the ifelse AI as it is now as the teacher. */
function newLessons() { LESSONS.list = []; LESSONS.teacher = null; saveLessons(); }
/** The next job: a game to make lessons from while there are too few, else a block of lessons for a candidate. */
function lessonJob(st, c) {
  if (!lessonsReady()) {
    if (!LESSONS.teacher || LESSONS.cards !== lessonCards()) { LESSONS.list = []; LESSONS.teacher = lessonTeacher(ifelseFull(st.best)); LESSONS.cards = lessonCards(); }
    const seed = 7001 + LESSONS.seed++;
    return { key: 'lesson-make-' + seed, lesson: 'make', msg: { type: 'lessonMake', seed, teacher: LESSONS.teacher, every: LESSON_EVERY,
      most: LESSON_PER_GAME, actionCap: ACTION_CAP, roundCap: ROUND_CAP, decks: DECK_PAIRS[seed % DECK_PAIRS.length] } };
  }
  if (!c) return null;
  const pick = tuneNextDeal(c);
  if (!pick) return null;
  const [i, gi] = pick;
  return { key: 'lesson' + st.gen + '-' + i + '-' + gi, lesson: 'grade', i, gi, gen: st.gen,
    msg: { type: 'lessonGrade', cfg: ifelseFull(tuneDecode(c.xs[i], 1)), from: gi * LESSON_BLOCK, to: (gi + 1) * LESSON_BLOCK } };
}
function lessonResult(r, job) {
  const st = tuneState();
  if (job.lesson === 'make') {
    if (lessonsReady()) return;
    LESSONS.list.push(...r.lessons);
    if (lessonsReady()) {
      LESSONS.list.length = lessonTarget(); saveLessons();
      if (tune.pool) tune.pool.setInit([{ type: 'lessons', lessons: LESSONS.list }]);
      if (!st.cand) newGeneration();
    }
    renderTuneStatus();
    return;
  }
  tuneScore(job, r.n ? 1 - r.sum / r.n : 0);
}

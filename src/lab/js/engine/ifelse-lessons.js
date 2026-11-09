/* =====================================================================
   FORESIGHT LESSONS: positions from real games where every legal move has a value from the deep search (the teacher,
   depth 3). The ifelse AI at depth 1 (the student) chooses a move in each; its loss in a lesson is how far its move's
   teacher value falls below the teacher's best move, capped (LESSON_CAP points = a full loss). Tuning the values to
   lose less teaches the depth-1 score to foresee what depth 3 sees, without playing whole games.
   ===================================================================== */
const LESSON_CAP = 200;                                               // about 3 dots: a move this much worse counts as fully wrong
/** The teacher: the values it was made from at depth 3, 10 own moves and 10 replies, then the 3 best next moves. */
const lessonTeacher = values => ({ ...values, depth: 3, w2: 10, w3: 3, rootRound: 1 });
/** One lesson from a position: every legal move with its teacher value (the full search below each, no move cut). */
function makeLesson(s, teacherCfg) {
  const c = ifelseConfig(teacherCfg), me = s.cur, root = cloneState(s);
  root.noFx = true; root.stopAtRoundEnd = true;
  let goals = null;
  if (c.goals) { goals = []; goals[me] = ifelseGoalsFor(root, me, null, c); goals[other(me)] = ifelseGoalsFor(root, other(me), null, c); }
  const moves = [];
  for (const a of listActions(root)) {
    const t = cloneState(root);
    applyAction(t, a);
    const o = { a, t };
    moves.push([JSON.stringify(a), ifelseSearch(t, me, 2, 2, goals, c) + rootPref(root, o, me, c)]);
  }
  const s0 = cloneState(s); s0.noFx = true;
  return { s: s0, moves };
}
/** The student's loss in a lesson: 0 for the teacher's best move, up to 1 for a move LESSON_CAP points worse or more. */
function lessonLoss(lesson, studentCfg) {
  const s = cloneState(lesson.s), key = JSON.stringify(chooseIfelseAction(s, { ...studentCfg, depth: 1 }));
  let best = -Infinity, mine = null;
  for (const [k, v] of lesson.moves) { if (v > best) best = v; if (k === key) mine = v; }
  if (mine === null) return 1;                                        // a move the teacher did not list (should not happen)
  return Math.min(LESSON_CAP, best - mine) / LESSON_CAP;
}
/** Runs fn with the dice fixed by seed (the same deals and chances every time). */
function withSeed(seed, fn) {
  const real = Math.random;
  let z = seed >>> 0;
  Math.random = () => { z = (z + 0x6D2B79F5) >>> 0; let t = Math.imul(z ^ (z >>> 15), z | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  try { return fn(); } finally { Math.random = real; }
}
/** Lessons from one seeded game: the teacher's values play both sides at depth 1; every `every` moves (from a start
 *  set by the seed) the position becomes a lesson, if it has two or more moves that the teacher values differently. */
function lessonsFromGame(msg) {
  return withSeed(msg.seed, () => {
    const s = newGame(msg.decks[0], msg.decks[1]);
    s.noFx = true;
    for (const p of [0, 1]) aiMulligan(s, p);
    s.redrawDone = true;
    const out = [], play = { ...msg.teacher, depth: 1 };
    for (let i = 0; i < msg.actionCap && s.winner === null && s.round <= msg.roundCap && out.length < msg.most; i++) {
      if ((i + msg.seed) % msg.every === 0) {
        const l = makeLesson(s, msg.teacher), vs = l.moves.map(m => m[1]);
        if (vs.length > 1 && Math.max(...vs) > Math.min(...vs)) out.push(l);
      }
      applyAction(s, chooseIfelseAction(s, play));
    }
    return out;
  });
}
/** A student's summed loss over lessons [from, to), each graded with its own fixed dice. */
function gradeLessons(lessons, cfg, from, to) {
  let sum = 0, n = 0;
  for (let i = from; i < Math.min(to, lessons.length); i++) { sum += withSeed(1000 + i, () => lessonLoss(lessons[i], cfg)); n++; }
  return { sum, n };
}

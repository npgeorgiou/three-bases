/* =====================================================================
   LESSONS: positions from real games and who went on to win. A try is graded in each lesson only on how well its
   score of the position predicts the winner (Texel tuning): its chance that the side to move wins, from the score
   after the round end is played out, against the real result (squared error).
   ===================================================================== */
const LESSON_SCALE = 200;                                            // score → chance scale
/** One lesson from a position: the position and the side to move; the result is added when the game ends. */
function makeLesson(s) {
  const s0 = cloneState(s); s0.noFx = true;
  return { s: s0, side: s.cur, result: null };
}
/** A try's loss in a lesson (0 best, 1 worst): how far its chance for the side to move is from the real result. */
function lessonLoss(lesson, studentCfg) {
  const t = cloneState(lesson.s); t.noFx = true; t.stopAtRoundEnd = true;
  const chance = 1 / (1 + Math.exp(-ifelseEnd(t, lesson.side, null, ifelseConfig({ ...studentCfg, depth: 1 })) / LESSON_SCALE));
  return (chance - lesson.result) ** 2;
}
/** Runs fn with the dice fixed by seed (the same deals and chances every time). */
function withSeed(seed, fn) {
  const real = Math.random;
  let z = seed >>> 0;
  Math.random = () => { z = (z + 0x6D2B79F5) >>> 0; let t = Math.imul(z ^ (z >>> 15), z | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  try { return fn(); } finally { Math.random = real; }
}
/** Lessons from one seeded game played to its end: the centre's numbers, looking 1 move ahead, play seat msg.seat
 *  against msg.opp (picked by `oppMove`); the position before every one of the centre's own moves becomes a lesson;
 *  at the end each lesson gets the centre's result. */
function lessonsFromGame(msg, oppMove) {
  return withSeed(msg.seed, () => {
    const s = newGame(msg.decks[0], msg.decks[1]);
    s.noFx = true;
    for (const p of [0, 1]) aiMulligan(s, p);
    s.redrawDone = true;
    const out = [], play = { ...msg.cfg, depth: 1 };
    for (let i = 0; i < msg.actionCap && s.winner === null && s.round <= msg.roundCap; i++) {
      if (s.cur !== msg.seat) { applyAction(s, oppMove(msg.opp, s)); continue; }
      out.push(makeLesson(s));
      applyAction(s, chooseIfelseAction(s, play));
    }
    if (s.winner !== 0 && s.winner !== 1 && s.winner !== 'draw') return [];   // unfinished game: no winner to learn from
    for (const l of out) l.result = s.winner === 'draw' ? 0.5 : s.winner === l.side ? 1 : 0;
    return out;
  });
}
/** A student's summed loss over lessons [from, to), each graded with its own fixed dice. */
function gradeLessons(lessons, cfg, from, to) {
  let sum = 0, n = 0;
  for (let i = from; i < Math.min(to, lessons.length); i++) { sum += withSeed(1000 + i, () => lessonLoss(lessons[i], cfg)); n++; }
  return { sum, n };
}

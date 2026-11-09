/* =====================================================================
   LESSONS: positions from real games, each with every legal move valued by the ifelse AI looking 3 moves ahead (with
   the centre's numbers when the lesson was made) and who went on to win. A try is graded in each lesson on two things,
   half each: its move looking 1 move ahead (0 for the 3-ahead best move, up to 1 for a move LESSON_CAP points worse or
   more), and how well its score of the position predicts the winner (its chance that the side to move wins, from the
   score after the round end is played out, against the real result: squared error).
   ===================================================================== */
const LESSON_CAP = 200, LESSON_SCALE = 200;                           // about 3 dots: a move this much worse counts as fully wrong; score → chance scale
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
  return { s: s0, moves, side: me, result: null };
}
/** A try's loss in a lesson (0 best, 1 worst): half its move looking 1 ahead, half how well it predicts the winner. */
function lessonLoss(lesson, studentCfg) {
  const cfg = { ...studentCfg, depth: 1 }, s = cloneState(lesson.s), key = JSON.stringify(chooseIfelseAction(s, cfg));
  let best = -Infinity, mine = null;
  for (const [k, v] of lesson.moves) { if (v > best) best = v; if (k === key) mine = v; }
  const move = mine === null ? 1 : Math.min(LESSON_CAP, best - mine) / LESSON_CAP;   // mine null: a move not listed (should not happen)
  const t = cloneState(lesson.s); t.noFx = true; t.stopAtRoundEnd = true;
  const chance = 1 / (1 + Math.exp(-ifelseEnd(t, lesson.side, null, ifelseConfig(cfg)) / LESSON_SCALE));
  return (move + (chance - lesson.result) ** 2) / 2;
}
/** Runs fn with the dice fixed by seed (the same deals and chances every time). */
function withSeed(seed, fn) {
  const real = Math.random;
  let z = seed >>> 0;
  Math.random = () => { z = (z + 0x6D2B79F5) >>> 0; let t = Math.imul(z ^ (z >>> 15), z | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  try { return fn(); } finally { Math.random = real; }
}
/** Lessons from one seeded game played to its end: the centre's numbers play both sides looking 1 move ahead; every
 *  `every` moves (from a start set by the seed) the position becomes a lesson, if it has two or more moves valued
 *  differently, at most `most`; at the end each lesson gets the result for its side to move. */
function lessonsFromGame(msg) {
  return withSeed(msg.seed, () => {
    const s = newGame(msg.decks[0], msg.decks[1]);
    s.noFx = true;
    for (const p of [0, 1]) aiMulligan(s, p);
    s.redrawDone = true;
    const out = [], play = { ...msg.teacher, depth: 1 };
    for (let i = 0; i < msg.actionCap && s.winner === null && s.round <= msg.roundCap; i++) {
      if ((i + msg.seed) % msg.every === 0 && out.length < msg.most) {
        const l = makeLesson(s, msg.teacher), vs = l.moves.map(m => m[1]);
        if (vs.length > 1 && Math.max(...vs) > Math.min(...vs)) out.push(l);
      }
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

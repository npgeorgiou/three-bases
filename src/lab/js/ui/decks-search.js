/* =====================================================================
   Decks tab: AI-made decks (the deck search) and card statistics.
   The pool: 6 decks per faction (its 2 premades and 4 random decks of 10 cards x3). First every pool deck plays every
   other one; then, faction by faction, a new deck is made from the faction's best unfinished deck by swapping one
   card's copies (or changing a copy count), chosen from the card statistics, and plays every pool deck. If it looks at
   least probably better than the faction's weakest deck, both play a fresh set of the same games (same opponents,
   seats and deals; scores picked out as lowest or highest are partly luck, fresh games remove that). The new deck
   replaces the weakest only if it is clearly better in those games. A deck is finished when 30 decks made from it in a
   row failed; the search ends when every pool deck is finished. Every game records which cards each side played.
   ===================================================================== */
const DS_PER_FACTION = 6, DS_RANDOM = 4, DS_RANDOM_CARDS = 10, DS_DONE_AFTER = 30;
const ds = { pool: null };                                          // the running games (not saved)
const freshDs = () => ({ v: 1, per: 10, pilots: [], decks: {}, pool: {}, h2h: {}, tasks: [], phase: null, cand: null, turn: 0, tries: 0,
  entered: 0, log: [], stats: {}, pairs: {}, tests: {}, yard: {} });
function dsState() {
  if (!state.ds || state.ds.v !== 1) state.ds = freshDs();
  return state.ds;
}
const dsRand = n => Math.floor(Math.random() * n);
const deckSize = list => list.reduce((n, [, c]) => n + c, 0);

/* ---------- head-to-head results and scores ---------- */
const h2hKey = (a, b) => a + '|' + b;
function addResult(st, a, b, r) {                                  // r from a's view: 1 won, 0.5 drawn, 0 lost
  for (const [x, y, v] of [[a, b, r], [b, a, 1 - r]]) {
    const e = st.h2h[h2hKey(x, y)] || (st.h2h[h2hKey(x, y)] = [0, 0, 0]);
    e[v === 1 ? 0 : v === 0 ? 1 : 2]++;
  }
}
const poolIds = st => Object.values(st.pool).flat();
/** A deck's results against the current pool (itself left out): [won, lost, drawn]. */
function vsPool(st, id, pool = poolIds(st)) {
  const t = [0, 0, 0];
  for (const b of pool) if (b !== id) { const e = st.h2h[h2hKey(id, b)]; if (e) { t[0] += e[0]; t[1] += e[1]; t[2] += e[2]; } }
  return t;
}
const rate = t => (t[0] + t[2] / 2) / Math.max(1, t[0] + t[1] + t[2]);
const games = t => t[0] + t[1] + t[2];
/** How sure it is that win rate a is above win rate b: z of the difference (2 or more: clearly; 1 or more: probably). */
function zOf(a, b) {
  const na = games(a), nb = games(b);
  if (!na || !nb) return 0;
  const pa = rate(a), pb = rate(b), p = (pa * na + pb * nb) / (na + nb), se = Math.sqrt(Math.max(1e-9, p * (1 - p) * (1 / na + 1 / nb)));
  return (pa - pb) / se;
}

/* ---------- card statistics ---------- */
/** Per card: [games in a deck, of them won, games it was played, of them won, times played]. */
function recordCards(st, job, res) {
  for (const side of [0, 1]) {
    const d = deckOf(st, job.decks[side]), won = res.winner === side ? 1 : res.winner === 'draw' ? 0.5 : 0;
    if (!d) continue;
    const played = (res.played && res.played[side]) || [], set = new Set(played.filter(k => !k.startsWith('lab_')));
    for (const [k] of d.list) {
      if (k.startsWith('lab_')) continue;
      const e = st.stats[k] || (st.stats[k] = [0, 0, 0, 0, 0]);
      e[0]++; e[1] += won;
      if (set.has(k)) { e[2]++; e[3] += won; }
    }
    for (const k of played) if (st.stats[k]) st.stats[k][4]++;
    const ps = [...set].sort();
    for (let i = 0; i < ps.length; i++) for (let j = i + 1; j < ps.length; j++) st.pairs[ps[i] + '|' + ps[j]] = (st.pairs[ps[i] + '|' + ps[j]] || 0) + 1;
  }
}
const ENOUGH = 8;                                                   // games played before a card's numbers guide swaps
/** A card's worth from the statistics (win rate when played, less for cards rarely played), or null with too little data. */
function cardValue(st, k) {
  const e = st.stats[k];
  if (!e || e[2] < ENOUGH) return null;
  const wr = (e[3] + 1) / (e[2] + 2), playRate = e[2] / Math.max(1, e[0]);
  return wr - Math.max(0, 0.25 - playRate);
}
/** How much more often two cards are played in the same game than chance would give (1 = as chance). */
function pairLift(st, a, b) {
  const ea = st.stats[a], eb = st.stats[b], both = st.pairs[a < b ? a + '|' + b : b + '|' + a] || 0;
  if (!ea || !eb || !ea[2] || !eb[2]) return 1;
  const n = Math.max(ea[0], eb[0]);
  return (both / n) / ((ea[2] / ea[0]) * (eb[2] / eb[0]));
}

/* ---------- decks ---------- */
const deckOf = (st, id) => st.decks[id] || (DECKS[id] ? { id, name: DECKS[id].name, fac: DECKS[id].fac, list: DECKS[id].list } : null);
function addDeck(st, d) { st.decks[d.id] = d; labDeck(d.id, d.name, d.fac, d.list); return d; }
function randomDeck(st, fac, n) {
  const cards = shuffle(factionCards(fac)).slice(0, DS_RANDOM_CARDS);
  return addDeck(st, { id: `r-${fac}-${n}`, name: `${LAB_FACTION_NAME[fac]} random ${n}`, fac, list: cards.map(k => [k, 3]), from: null, fails: 0, tried: [] });
}
/** A new deck from a parent: one card's copies swapped, or (one time in five) one copy more or less. Chosen from the
 *  statistics like a player would: out goes the card that adds least, in comes first a card of about the same cost,
 *  preferring cards often played with the deck's best cards; with no statistics yet, chosen at random. */
function childOf(st, parent) {
  const fac = parent.fac, have = new Set(parent.list.map(([k]) => k)), list = parent.list.map(([k, n]) => [k, n]), size = deckSize(list);
  const guided = st.phase === 'search', val = k => cardValue(st, k) ?? 0.5;
  const ranked = list.map(([k]) => k).sort((a, b) => (guided ? val(a) - val(b) : Math.random() - 0.5));
  let change = null;
  if (Math.random() < 0.2) {                                         // a copy count
    const weak = ranked.find(k => list.find(x => x[0] === k)[1] > 1), strong = [...ranked].reverse().find(k => list.find(x => x[0] === k)[1] < 3);
    if (size > 30 && weak && !parent.tried.includes('-' + weak)) change = { tag: '-' + weak, apply: () => { list.find(x => x[0] === weak)[1]--; }, say: `one ${CARDS[weak].name} less` };
    else if (size < 40 && strong && !parent.tried.includes('+' + strong)) change = { tag: '+' + strong, apply: () => { list.find(x => x[0] === strong)[1]++; }, say: `one ${CARDS[strong].name} more` };
  }
  if (!change) {
    const best = [...ranked].reverse().slice(0, 3), cost = k => CARDS[k].cost ?? CARDS[k].sup ?? 0;
    for (const out of ranked) {
      const options = factionCards(fac).filter(k => !have.has(k) && !parent.tried.includes(out + '>' + k));
      if (!options.length) continue;
      const score = k => (cardValue(st, k) ?? 0.55) + 0.05 * best.reduce((n, b) => n + Math.min(3, pairLift(st, k, b)) - 1, 0);
      const pick = guided ? options.sort((a, b) => (Math.abs(cost(a) - cost(out)) > 1) - (Math.abs(cost(b) - cost(out)) > 1) || score(b) - score(a))[0]
        : options[dsRand(options.length)];
      const n = list.find(x => x[0] === out)[1];
      change = { tag: out + '>' + pick, apply: () => { const i = list.findIndex(x => x[0] === out); list[i] = [pick, n]; }, say: `${n}× ${CARDS[out].name} out, ${n}× ${CARDS[pick].name} in` };
      break;
    }
  }
  if (!change) return null;
  parent.tried.push(change.tag); change.apply();
  st.tries++;
  return addDeck(st, { id: `d-${st.tries}`, name: `${LAB_FACTION_NAME[fac]} deck ${st.tries}`, fac, list: list.filter(([, n]) => n > 0), from: parent.id, say: change.say, fails: 0, tried: [] });
}

/* ---------- the schedule: tasks of games between two decks ---------- */
const task = (a, b, tag, seed = 31000) => ({ a, b, tag, seed, started: 0, done: 0 });
function startPool(st) {
  for (const fac of LAB_FACTIONS) {
    st.pool[fac] = LAB_DECKS.filter(d => DECKS[d].fac === fac).map(d => d);
    for (let i = 1; i <= DS_RANDOM; i++) st.pool[fac].push(randomDeck(st, fac, i).id);
  }
  const ids = poolIds(st);
  for (let i = 0; i < ids.length; i++) for (let j = i + 1; j < ids.length; j++) st.tasks.push(task(ids[i], ids[j], 'first'));
  st.phase = 'first';
  dsLog(st, `Pool made: ${ids.length} decks; first round: every deck plays every other one ${st.per} times.`);
}
function dsLog(st, text) { st.log.push(text); if (st.log.length > 200) st.log.splice(0, st.log.length - 200); }
function testAgainstPool(st, id, tag) { for (const b of poolIds(st)) if (b !== id) st.tasks.push(task(id, b, tag)); }
/** The next deck to try: factions in turn, from the faction's best unfinished deck. */
function nextCandidate(st) {
  for (let k = 0; k < LAB_FACTIONS.length; k++) {
    const fac = LAB_FACTIONS[(st.turn + k) % LAB_FACTIONS.length];
    const open = st.pool[fac].map(id => deckOf(st, id)).filter(d => st.decks[d.id] ? st.decks[d.id].fails < DS_DONE_AFTER : true);
    for (const d of open.sort((a, b) => rate(vsPool(st, b.id)) - rate(vsPool(st, a.id)))) {
      const parent = st.decks[d.id] || addDeck(st, { ...d, list: d.list.map(([x, n]) => [x, n]), from: null, fails: 0, tried: [] });
      const child = childOf(st, parent);
      if (!child) { parent.fails = DS_DONE_AFTER; continue; }
      st.turn = (st.turn + k + 1) % LAB_FACTIONS.length;
      st.cand = { id: child.id, fac, parent: parent.id, round: 1 };
      testAgainstPool(st, child.id, 'cand');
      return true;
    }
  }
  return false;
}
/** All games of the current step are done: decide, then plan the next step. */
function stepDone(st) {
  if (st.phase === 'first') { st.phase = 'search'; dsLog(st, 'First round done; the search starts.'); }
  else if (st.phase === 'search' && st.cand) {
    const c = st.cand, facPool = st.pool[c.fac], d = st.decks[c.id], parent = st.decks[c.parent];
    if (!c.weakest) c.weakest = facPool.slice().sort((a, b) => rate(vsPool(st, a)) - rate(vsPool(st, b)))[0];
    const others = poolIds(st).filter(x => x !== c.weakest), mine = vsPool(st, c.id, others), wname = deckOf(st, c.weakest).name;
    const z = c.replay ? zOf(c.fresh, c.replay) : zOf(mine, vsPool(st, c.weakest));
    const shown = c.replay ? `${pc(rate(c.fresh))} in fresh games where ${wname} scored ${pc(rate(c.replay))}` : `${pc(rate(mine))} against the pool, ${wname} ${pc(rate(vsPool(st, c.weakest)))}`;
    if (!c.replay && z >= 1) {                                       // looks better: both play a fresh set of the same games
      c.replay = [0, 0, 0]; c.fresh = [0, 0, 0];
      for (const b of others) { st.tasks.push(task(c.weakest, b, 'replay', 61000)); st.tasks.push(task(c.id, b, 'fresh', 61000)); }
      dsLog(st, `${d.name}: ${shown}: probably better; both play a fresh set of the same games.`);
      return;
    }
    if (c.replay && z >= 2) {
      facPool[facPool.indexOf(c.weakest)] = c.id; st.entered++; parent.fails = 0;
      dsLog(st, `${d.name} (${d.say}, from ${parent.name}): ${shown}: clearly better, it replaces ${wname}.`);
    } else {
      parent.fails++;
      dsLog(st, `${d.name} (${d.say}): ${shown}: not clearly better; dropped (${parent.name}: ${parent.fails}/${DS_DONE_AFTER} in a row).`);
      for (const k of Object.keys(st.h2h)) if (k.startsWith(c.id + '|') || k.endsWith('|' + c.id)) delete st.h2h[k];
      delete st.decks[c.id];
    }
    st.cand = null;
  }
  if (st.phase === 'search' && !nextCandidate(st)) { st.phase = 'done'; dsLog(st, 'Every pool deck is finished: the search is done.'); }
}
const pc = v => Math.round(100 * v) + '%';

/* ---------- the lab's decks: the game's premade decks, each a deck of its own ---------- */
const LAB_FACTION_NAME = Object.fromEntries(Object.values(DECKS).map(d => [d.fac, d.name]));
for (const d of PREMADE) DECKS[d.id] = { name: d.name, fac: CARDS[Object.keys(d.cards)[0]].fac, list: Object.entries(d.cards) };
const LAB_DECKS = PREMADE.map(d => d.id);
const LAB_FACTIONS = [...new Set(LAB_DECKS.map(d => DECKS[d].fac))];
const facOfDeck = d => DECKS[d].fac;
/** Every ordered pair of premade decks, in a fixed mixed order (so the first few dozen cover many factions). */
const DECK_PAIRS = (() => {
  const all = [];
  for (const a of LAB_DECKS) for (const b of LAB_DECKS) all.push([a, b]);
  let seed = 12345;
  const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
  for (let i = all.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [all[i], all[j]] = [all[j], all[i]]; }
  return all;
})();
/** Tournament matchups: decks of different factions, or of the same faction. */
const MATCHUPS = {
  X: { label: 'Different factions', pairs: DECK_PAIRS.filter(([a, b]) => facOfDeck(a) !== facOfDeck(b)) },
  S: { label: 'Same faction', pairs: DECK_PAIRS.filter(([a, b]) => facOfDeck(a) === facOfDeck(b)) },
};
/** The decks of the i-th game of a fixed schedule (i and i+1 share decks, so both seats get them). */
const scheduledDecks = (i, pairs = DECK_PAIRS) => pairs[Math.floor(i / 2) % pairs.length];
const randomDecks = () => DECK_PAIRS[Math.floor(Math.random() * DECK_PAIRS.length)];

/** Lab-only plain units, one per cost: size 1, no keywords or effects, strength + defence = the design budget for that
 *  cost (tools/design_gate.py: 0, 3, 5, 7, 8, 10, then twice the cost). A card measured "with and without" is replaced by
 *  the plain unit of its cost; these never enter a real deck. */
const PLAIN_BUDGET = n => [0, 3, 5, 7, 8, 10][n] ?? 2 * n;
for (let n = 0; n <= 12; n++) {
  const b = PLAIN_BUDGET(n);
  CARDS['lab_plain' + n] = { name: `Plain unit (${n})`, fac: 'lab', size: 1, sup: n, cost: n, str: Math.floor(b / 2), def: Math.ceil(b / 2), art: 'helm', text: 'A plain unit for card tests.' };
}
const plainFor = key => 'lab_plain' + Math.min(12, Math.max(0, Math.round(CARDS[key].cost || CARDS[key].sup || 0)));
/** The cards a deck of this faction may hold: its own, no tokens, no lab cards. */
const factionCards = fac => Object.keys(CARDS).filter(k => CARDS[k].fac === fac && !CARDS[k].token).sort();
/** Makes a deck known under a key (lab decks are sent to the workers with each game). */
const labDeck = (key, name, fac, list) => (DECKS[key] = { name, fac, list: list.map(([k, n]) => [k, n]) });


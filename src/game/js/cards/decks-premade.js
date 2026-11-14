const DECKS = {};
/** Premade decks: each built around one side of its faction. */
const PREMADE_VERSION = 8;   // raising it replaces the premade decks stored in a browser with these lists
const PREMADE = [];

/** Decks saved from the AI lab ("Use in the game"), up to 4 per faction (p-<faction>1 to p-<faction>4), take the place of
 *  the premade lists in this browser, the 3rd and 4th as premades of their own: the game, the scenarios and the lab read
 *  the same store. The lab's workers have no browser store and get the saved decks with their program. */
const PREMADE_PER_FACTION = 4;
const PREMADE_SAVED_STORE = 'threeBases.savedPremades';
const PREMADE_SAVED = (() => {
  try {
    if (typeof localStorage !== 'undefined') return JSON.parse(localStorage.getItem(PREMADE_SAVED_STORE) || 'null');
    return (typeof self !== 'undefined' && self.PREMADE_SAVED_DATA) || null;
  } catch (e) { return null; }
})();
if (PREMADE_SAVED && PREMADE_SAVED.decks) for (const fac of Object.values(DECKS).map(d => d.fac)) for (let i = 1; i <= PREMADE_PER_FACTION; i++) {
  const id = `p-${fac}${i}`, s = PREMADE_SAVED.decks[id];
  if (!s || !s.cards) continue;
  const cards = Object.fromEntries(Object.entries(s.cards).filter(([k, n]) => CARDS[k] && !CARDS[k].token && CARDS[k].fac === fac && n > 0));
  const n = Object.values(cards).reduce((a, b) => a + b, 0);
  if (n < 30 || n > 40 || Object.values(cards).some(x => x > 3)) continue;
  const d = PREMADE.find(x => x.id === id);
  if (d) { d.cards = cards; d.name = s.name || d.name; d.saved = true; continue; }
  const after = PREMADE.map(x => x.id).filter(x => x.startsWith('p-' + fac)).pop();   // next to the faction's other premades
  PREMADE.splice(after ? PREMADE.findIndex(x => x.id === after) + 1 : PREMADE.length, 0, { id, name: s.name || id, cards, saved: true });
}

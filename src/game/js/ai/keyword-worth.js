/* =====================================================================
   KEYWORD WORTH: what each keyword on a unit is worth to the ifelse AI, by how much it is working right now
   (Geared counts the Geared allies touching it, Bodyguard the allies it protects ...). One line per keyword; the
   AI lab makes one tunable value per line whose keyword is in the game's cards (kw_<field>, start 0), so a keyword
   added to or removed from the cards needs only its line here. tools/ifelse_speed.js lists keywords on unit cards
   that have neither a line here nor a line in KW_NOT_VALUED.
   ===================================================================== */
/** Where a rule looks: the unit, its side and lane, as card effects see them (fxIf conditions, fxSel targets). */
const kwCtx = u => ({ p: ctl(u), u, lane: u.lane });
const kwCount = to => (s, u) => fxSel(s, kwCtx(u), to).length;
const kwWhen = cond => (s, u) => (fxIf(s, kwCtx(u), cond) ? 1 : 0);
/** "Always": the keyword counts the same wherever the unit stands. */
const KW_ALWAYS = () => 1;
const kwSecondRow = u => rowsOf(u).includes(u.owner === 0 ? 1 : ROWS - 2);
/** [card field, keyword, how much it works now (a number; 1 = always), and optionally the card's number when it is not
 *  the field (e.g. an effect on a trigger)]. Its worth: the value x the card's number x how much it works now. */
const KW_RULES = [
  ['ranged', 'Ranged', KW_ALWAYS],
  ['fixed', 'Immobile', KW_ALWAYS],
  ['lightfooted', 'Lightfooted', KW_ALWAYS],
  ['reach', 'Pike', (s, u) => (kwSecondRow(u) ? 1 : 0)],                       // attacks the enemy front row from the second row
  ['wall', 'Shield wall', (s, u) => targetsOf(s, u, 'wall').length],          // Shield wall units directly beside it
  ['reckless', 'Reckless', KW_ALWAYS],
  ['armoured', 'Armoured', (s, u) => (u.armUsed ? 0 : 1)],                     // its block is still unused this round
  ['push', 'Push', KW_ALWAYS],
  ['outrider', 'Outrider', KW_ALWAYS],
  ['guard', 'Bodyguard', (s, u) => adjacentAllies(s, u).length],              // the allies it protects
  ['riposte', 'Riposte', KW_ALWAYS],
  ['flurry', 'Flurry', KW_ALWAYS],
  ['geared', 'Geared', kwCount('adj:geared')],                                // Geared allies touching it
  ['salvage', 'Salvage', KW_ALWAYS],
  ['toll', 'Toll', KW_ALWAYS],
  ['obsidian', 'Obsidian', KW_ALWAYS],
  ['onrush', 'Onrush', kwCount('allies')],                                    // other allies in its lane whose attacks pump it
  ['flanker', 'Flanker', kwWhen({ front: 1, side: 1 })],                       // in a side column of the front row
  ['reserve', 'Reserve', kwWhen({ back: 1 })],                                 // outside the front row, so it can still move up
  ['harden', 'Harden', KW_ALWAYS],
  ['retaliate', 'Retaliate', KW_ALWAYS],
  ['vigil', 'Vigil', KW_ALWAYS],
  ['perennial', 'Perennial', KW_ALWAYS],
  ['seeds', 'Seeds', KW_ALWAYS],
  ['roots', 'Roots', kwCount('facing')],                                       // an enemy in its column to hit
  ['barrage', 'Barrage', kwCount('deepest')],                                  // an enemy in its lane to hit
  ['entrench', 'Entrenched', kwWhen({ front: 1, min: ['behind', 1] })],        // in the front row with an ally behind
  ['augur', 'Augur', KW_ALWAYS],
  ['omen', 'Omen', KW_ALWAYS, k => ((k.fx || []).some(e => e.on === 'targeted') ? 1 : 0)],   // an effect when one of your spells targets it
  ['marked', 'Marked', KW_ALWAYS],                                                // given by enemy cards: strikes on it deal double
];
/** The card's number for a rule: its own way, or the field (gained keywords count, moved-away ones don't). */
const kwAmount = (u, rule) => (rule[3] ? rule[3](cardOf(u)) : Number(kw(u, rule[0])) || 0);
/** Whether a rule's keyword is in the game: on a unit card, or named on any card (a spell that gives it). */
const kwInGame = rule => Object.values(CARDS).some(k => (k.sup && !k.token && (rule[3] ? rule[3](k) : k[rule[0]])) || (k.text || '').includes('|' + rule[1] + ']]') || (k.text || '').includes('[[' + rule[1] + ']]'));
/** Words in [[ ]] on unit cards that get no keyword value, and why. */
const KW_NOT_VALUED = { Charge: 'happens on placement, which the search plays itself', Wound: 'happens on placement, which the search plays itself',
  Offering: 'happens on placement, which the search plays itself', Wind: 'an effect, played by the search', Strike: 'a rule word',
  Supply: "part of a unit's worth", 'Carry-over': 'its own value', Bloodied: 'a state its defence already shows', Shield: 'its defence already shows it' };
/** The worth of a unit's keywords (gained ones count, moved-away ones don't); only keywords with a value set are looked at.
 *  Per card, the keywords that apply and their fixed part are worked out once (units with gained or moved keywords each time). */
function kwWorth(s, u, c) {
  let m = c._kwr;                                                     // kept on the values object, hidden from copies and exports
  if (!m) { m = { rules: KW_RULES.filter(r => c['kw_' + r[0]]), byCard: new Map() }; Object.defineProperty(c, '_kwr', { value: m }); }
  if (!m.rules.length) return 0;
  const own = !(u.kw || u.off);
  let k = own ? m.byCard.get(u.card) : null;
  if (!k) {
    k = { fixed: 0, works: [] };
    for (const r of m.rules) {
      const v = c['kw_' + r[0]] * kwAmount(u, r);
      if (!v) continue;
      if (r[2] === KW_ALWAYS) k.fixed += v; else k.works.push([v, r[2]]);
    }
    if (own) m.byCard.set(u.card, k);
  }
  let n = k.fixed;
  for (const [v, works] of k.works) n += v * works(s, u);
  return n;
}

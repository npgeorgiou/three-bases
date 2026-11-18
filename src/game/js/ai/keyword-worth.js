/* =====================================================================
   KEYWORD WORTH: what each keyword on a unit is worth to the ifelse AI, by how much it is working right now
   (Pike counts only from the second row). One line per keyword; the
   AI lab makes one tunable value per line whose keyword is in the game's cards (kw_<field>, start 0), so a keyword
   added to or removed from the cards needs only its line here. tools/ifelse_speed.js lists keywords on unit cards
   that have neither a line here nor a line in KW_NOT_VALUED.
   ===================================================================== */
/** "Always": the keyword counts the same wherever the unit stands. */
const KW_ALWAYS = () => 1;
const kwSecondRow = u => rowsOf(u).includes(u.owner === 0 ? 1 : ROWS - 2);
/** [card field, keyword, how much it works now (a number; 1 = always), and optionally the card's number when it is not
 *  the field (e.g. an effect on a trigger)]. Its worth: the value x the card's number x how much it works now. */
const KW_RULES = [
  ['ranged', 'Ranged', KW_ALWAYS],
  ['fixed', 'Immobile', KW_ALWAYS],
  ['reach', 'Pike', (s, u) => (kwSecondRow(u) ? 1 : 0)],                       // attacks the enemy front row from the second row
];
/** The card's number for a rule: its own way, or the field. */
const kwAmount = (u, rule) => (rule[3] ? rule[3](cardOf(u)) : Number(kw(u, rule[0])) || 0);
/** Whether a rule's keyword is in the game: on a unit card, or named on any card (a spell that gives it). */
const kwInGame = rule => Object.values(CARDS).some(k => (k.sup && !k.token && (rule[3] ? rule[3](k) : k[rule[0]])) || (k.text || '').includes('|' + rule[1] + ']]') || (k.text || '').includes('[[' + rule[1] + ']]'));
/** Words in [[ ]] on unit cards that get no keyword value, and why. */
const KW_NOT_VALUED = { Strike: 'a rule word', Supply: "part of a unit's worth", 'Carry-over': 'its own value' };
/** The worth of a unit's keywords; only keywords with a value set are looked at.
 *  Per card, the keywords that apply and their fixed part are worked out once. */
function kwWorth(s, u, c) {
  let m = c._kwr;                                                     // kept on the values object, hidden from copies and exports
  if (!m) { m = { rules: KW_RULES.filter(r => c['kw_' + r[0]]), byCard: new Map() }; Object.defineProperty(c, '_kwr', { value: m }); }
  if (!m.rules.length) return 0;
  let k = m.byCard.get(u.card);
  if (!k) {
    k = { fixed: 0, works: [] };
    for (const r of m.rules) {
      const v = c['kw_' + r[0]] * kwAmount(u, r);
      if (!v) continue;
      if (r[2] === KW_ALWAYS) k.fixed += v; else k.works.push([v, r[2]]);
    }
    m.byCard.set(u.card, k);
  }
  let n = k.fixed;
  for (const [v, works] of k.works) n += v * works(s, u);
  return n;
}

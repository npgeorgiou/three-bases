/* =====================================================================
   CARD DATA (card revamp, v2)
   Units: sup = supply given each round = deploy cost = cost of each move or attack.
   Budget (supply to stats): strength + defence of a vanilla unit by supply: 1:3, 2:5, 3:7, 4:8, 5:10, then 2 per supply
   (6:12 … 10:20); minus size (line of 2: 1, line of 3: 2, 2x2: 3); stats take their share, the ability the rest.
   Areas are always the unit's own row(s), column(s), or the whole camp; "in front" / "behind" face the enemy camp.
   Card text: [[Keyword]] or [[shown text|Keyword]] shows a hover explanation.
   Unit flags: bonus (Supply +n), backBonus (+n supply in back row), moves, wall (Shield wall), reach (Pike), ranged,
   onPlace ('mandator' | 'pull' | 'komes' | 'defect' | 'crowd' | 'cinder'), herald, warhorn, eotAdjHeal, eotLaneHealAll,
   charge, spearwall, frontBuff, veteran, fixed, rowAura {s,d}, drumHit, armoured, reckless, keg, pain, grubber, push,
   deathHit, bleed, skull, carrion, splash, overrun, sorcerer, eotSelf, skirm, pack, adjAura {s,d}, guard, guardGrow, outrider,
   hitsOwn, frenzy, eotShoot, eotShootStr, eotSapper, eotBurn, eotRegen, desert, deathDraw, deathAdjHeal, deathReturn.
   Spells: tactic = 'lane' | 'column' | 'own' | 'enemy' | 'any'; costLabel for variable costs.
   ===================================================================== */
const CARDS = {

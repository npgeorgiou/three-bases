# Deck read: Duelyst (29 Oct 2026, v38 build; PROCESS step 2.9)

All 10 guide decks (decks.tsv) read line by line as a player, before any fix. Each wrong or missing line, then the
families they fall into. Every family is fixed once, by a rule for every game.

## Wrong or missing lines, deck by deck
| deck | from | to | what is wrong |
|---|---|---|---|
| all ten | every unit | Dagona, Unseven, Grimes, Juggernaut, Vorpal Reaver, Desolator, Aymara Healer, Battle Panddo, Arclyte Regalia | "your units die / take damage (by the game's rule: units counterattack)": a counterattack hits the attacker, an enemy |
| all ten | every unit | Letigress, White Asp, Spectral Blade | "your units attack / are killed (by fighting)": these wait for the General attacking or destroying, not any unit |
| Argeon Mechaz0r | Lifestream, Holy Immolation, Mirrorrim, Argeon BBS | Argeon Highmayne | "targets can heal / copies it / +2": the General is no minion and is never in the deck |
| Vaath Dying Wish | Kujata, Flash Reincarnation, Fractal Replication, Cascading Rebirth | Vaath the Immortal | "cheaper / copies / kills it": same, the General is no minion |
| Kaleos Trial, Dawn's Eye, Riftwalker, Lilithe | Mist Dragon Seal, Darkfire Sacrifice, Afterblaze, Primus Fist ... | the General | same |
| Vaath Dying Wish | Vaath the Immortal | Lavaslasher | "more power: it hits harder": Vaath's spell gives the General +1 Attack, not Lavaslasher |
| Vaath Dying Wish | Flash Reincarnation | Unseven | "your units get Dying Wish": Flash gives the player an ability, no keyword |
| Vaath Dying Wish | - | Unseven -> Dagona, Grimes | missing: Unseven summons a Dying Wish minion from the hand |
| Kaleos Trial, Lilithe | EMP | Dagona, Vorpal Reaver, Desolator | "your units die": EMP destroys artifacts, no minion dies |
| Kaleos Trial | Scroll Bandit | Battle Panddo, Dagona | "your units take damage / die": Backstab's extra damage hits the enemy attacked |
| Kaleos Trial | Inquisitor Kron, Dagona | Hideatsu the Ebon Ox | "your units enter play": the Trial counts minions summoned from the action bar; tokens do not count; every minion card of the deck does |
| Kaleos Trial | Kaleos Xaan, Mist Dragon Seal, Juxtaposition | Scroll Bandit | missing: teleporting it behind an enemy is what Backstab needs |
| Shidai Artifacts | Mask of Shadows, Saberspine Seal, Bangle, Cyclone Mask, Crescent Spear | Shidai Stormblossom | missing: artifacts and spells that give the General Attack, Backstab, Celerity, Ranged make the General hit harder |
| Shidai Artifacts | Flicker, Mist Walking | Mask of Shadows | missing: teleporting the General behind an enemy is what the General's Backstab needs |
| Cassyva Replace | Aethermaster | White Widow, Wings of Paradise, Inquisitor Kron | missing: an extra replace each turn sets off "whenever you replace a card" |
| Cassyva Replace | Theobule | White Widow, Wings, Kron | right, but said "waits shuffled": say "cards are replaced" |
| Cassyva Replace | Wings of Paradise | Primus Fist | "your units move": Primus Fist buffs a minion next to where it is summoned; moving is no help |
| Lilithe Darkfire | Lilithe BBS, Inkling Surge, Vorpal Reaver | Phantasm | "enemy units enter play": my Wraithlings are mine; Phantasm waits for the opponent's summons |
| Lilithe Darkfire | Grasp of Agony | Vorpal Reaver, Desolator, Spectral Blade | "your units die / are killed": Grasp damages the enemies around the dying enemy minion |
| Argeon Mechaz0r | Argeon BBS, Oakenheart | Martyrdom | "stats changed": Martyrdom heals by the destroyed minion's Health; +Attack adds nothing |
| Argeon Mechaz0r, Riftwalker | Lifestream | spells, the General | "draws it from the deck": Lifestream draws a copy of the minion it healed |
| Riftwalker | Sunstrike | Lifestream, Trinity Oath, other spells | "targets can heal it": spells are never on the board |
| Argeon Mechaz0r | MECHAZ0R pieces | each other | missing: each piece progresses the build 20%; five together deploy MECHAZ0R! |
| Faie Blood Taura | Flameblood Warlock | Blood Taura | missing: damage to my General makes Blood Taura cheaper (its cost is the General's Health); the record had it the other way (healing) |
| Riftwalker | Afterblaze | Windblade Adept, Silverguard Knight, Solpiercer | missing: "if that minion has Zeal" asks for the Zeal minions |
| Dawn's Eye, Riftwalker | (General moves) | Zeal minions | missing need: Zeal is where the General stands; moving the General or the minion changes it |
| Faie Blood Taura | Spirit of the Wild targets | units on the enemy side | Infiltrate and "on the enemy side" needs: moving the unit is what they need (none was written) |
| Shidai Artifacts | Shidai's Bloodbound Spell | Spellsword | a stub: Spellsword is one of Murasame, Kiyomori, Tanahashi, Kotetsu |

Second read, after the merge with Faeria's v39 code (same 10 decks):
| deck | from | to | what is wrong |
|---|---|---|---|
| Vaath Dying Wish | Juggernaut | Lavaslasher, Vaath | "more power: it hits harder": Grow makes only Juggernaut stronger |
| Cassyva Replace, Kaleos Trial | Aethermaster | the General | "targets can can it": an extra replace is the player's, no help to the General card |
| Cassyva Replace | every unit, Healing Mystic | Abhorrent Unbirth | "your units die / are healed": Unbirth destroys my minions itself |
| Lilithe Darkfire | Phantasm, Darkfire Sacrifice | Wraithling | "+1 Attack / cheaper": Wraithlings are summoned onto the board, never in the action bar |
| Cassyva Replace, Ciphyron Build | Healing Mystic | the General, units | missing: "restore 2 Health to anything" heals my General or a minion |
| Lilithe Darkfire | Lilithe BBS, Inkling Surge, Vorpal Reaver | Inkling Surge | missing: "if you have another Wraithling" asks for the Wraithling makers |

## Families (one rule each, every game)
1. **pick actor kept no kind or side** (counterattack rule, Scroll Bandit, every "the attacker"): the actor of the event is
   who it is. refs.py: a target picked "actor" takes the kind and side of its ability's event actor.
2. **A leader card is no unit** (the General is the player's life): category `leader` for a card that is its player (Duelyst
   Generals); network KIND_CAT player -> leader; the fight rules apply to leaders as the player; a unit target never matches
   a leader. Runeterra and Monster Train champions stay `hero` (units).
3. **What is done to the player helps only the leader**: power and keywords given to my player help my leader card fight
   ("more power: it hits harder" to the General), never my units.
4. **A keyword given to a target: "it" in the keyword's record is no holder** (flat.py applied_to replaced "it" with the
   holder: Backstab's extra damage landed on the attacker). Only "self" is the holder; "it" stays the keyword's target.
5. **Destroying an artifact kills no unit**: kill on equipment makes leaves_play only.
6. **An ability given to the player is no keyword given** (Flash Reincarnation "gives Dying Wish").
7. **A summon is on its owner's side** when the text names no side.
8. **"Summoned from your action bar" is played** (one form: BRIEF Duelyst says Opening Gambit = played): normalize N24 turns
   summoned + state from_hand into played; the Trial then counts the deck's minion cards.
9. **Positions that need moving**: what a unit's own keyword needs about where it stands (Backstab behind an enemy, Zeal near
   my General, Infiltrate on the enemy side) is its need; a position measured from the player (my General) counts as a
   board thing; "on" a space (same_space, no "of") is where the card stands. Moving the unit or the General feeds them.
10. **Where a new card enters needs no moving**: an effect on entering ("give a nearby minion +2 Attack") is placement.
11. **Replacing cards**: "you may replace an additional card" makes cards be replaced; wording "cards are replaced".
12. **A copy of it is that card** (Lifestream): a draw or summon of "a copy of it" takes only cards the first effect can pick.
13. **Board targets are on the board**: a target of kind any is a unit or a player, never a spell or artifact card.
14. **A stat used as an amount wants that stat**: +Attack does not feed "restore that minion's Health".
15. **A cost equal to a stat wants less of it** (Blood Taura: cheaper when my General is hurt).
16. **Asked-for keywords in conditions**: "if that minion has Zeal" asks for Zeal cards.
17. **MECHAZ0R build**: the keyword's record counts progress; every piece helps the others complete MECHAZ0R!.
18. **Grasp of Agony's "enemies"** are the caster's enemies (the dying minion's allies); Spellsword is one of four swords.
19. **A gain on itself helps no other card** (Juggernaut's Grow): power and health makers are counted row by row; a card whose
    stat gains are all on itself is no maker for others.
20. **What the player may do with cards is no help to its leader card** ("you may replace an additional card").
21. **What an ability kills and then uses is its own** (Abhorrent Unbirth): a death need is dropped when the same ability makes
    those deaths.
22. **Cards only summoned onto the board are never in the hand**: effects on cards in hand and cost changes skip them.
23. **Help to "anything" chosen on the board** reaches units and the leader card (games with leader cards).
24. **A named card asked for in play** ("if you have another Wraithling"): the cards that make it feed the condition; not a
    condition on the deck or discard ("if Krog is in your deck, draw him" fetches him).

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
| Faie Blood Taura | White Asp | Blazing Spines | "makes the walls it names": the spell names only the walls it summons itself |

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
    condition on the deck or discard ("if Krog is in your deck, draw him" fetches him). A card naming what it makes itself in
    its own effects (Blazing Spines' walls "can attack") asks for no other maker of it.

## Kaptain's check (30 Oct 2026, v42): families (PROCESS "Kaptain's check of the Duelyst networks")
Lines before -> after my v42 change, measured with the network code before and after (before the merge with Faeria's v41):
Runeterra 597 gone / 15 new, Stormbound 18 / 4, Monster Train 2 / 0, Faeria 53 / 3, Inscryption 19 / 1; every gone and new
reason group read.

## F1 Help read as a need
Kaptain: Mechs -> Oakenheart "is a Mech it asks for"; Golems -> Golem Metallurgist; Build cards -> Timekeeper.
Root cause: network.py lines_of took every effect's target filter as an ask (type, name); refs.py state_rows took a keyword
filter of any effect as a keyword need, and help triggers ("the first Golem you summon costs 1 less") as waits.
Same error elsewhere: Runeterra 129 "is a Lurker it asks for" + 38 "makes a Lurker" (Lurk grants Lurkers +1|+0: now a help
line); Stormbound 11 "is a Dragon it asks for" to Spare Dragonling; Faeria 14 Rakoan asks, Ancient Beastmaster, Drakkar
Skycaptain counts; Monster Train: none wrong (Shardtail Queen kills her Imps, Deranged Brute makes Rage stronger: real wants).
Fix: an effect that helps what it names (helps_it, HELP_ACTS) is no ask, no keyword need, and its trigger's own cards are no
"card it counts"; a card that makes an effect stronger (increase_effect) still wants it.

## F2 What every unit does by the rules
Kaptain: Aethermaster, Kron, Replicant, Letigress ... -> Punish "by fighting": all units can attack.
Root cause: network.py lines_of linked every unit through the game's fight and counterattack rules, and HELPS gave power as
help to "an enemy is damaged".
Same error elsewhere: Runeterra 79 "your units attack (by fighting)", 62 "enemy units take damage", 57 "your units die", 26
"the enemy player takes damage", 20 "any units strike", 37 "more damage"; Faeria 9 "harvests (by the rule)" to Wavecrash
Colossus, 10 "your units die (by fighting)"; Inscryption 19 "Bones from deaths".
Fix: a rule line stays only from a card whose own ability makes it fight more (Celerity, Frenzy, Overwhelm, "this fights"),
for a need naming the leader, or for a level-up count (Kaptain's n53); power helps damage needs only for level-ups.

## F3 A stat of what the player picks to harm
Kaptain: Lifestream, Holy Immolation -> Martyrdom "does what it waits for".
Root cause: refs.py (amount_stat conditions) and network.py (more health / more power) wanted the stat of "it" also when
"it" is any minion the player picks to destroy.
Same error elsewhere: Faeria The Emperor's Command -> Feed the Forest; none else found.
Fix: a stat of a chosen or random target of a harmful act on either side wants nothing; help picks keep the want.

## F4 Stat gains by stat and by target
Found reading again: Roar -> Martyrdom "more health"; Abhorrent Unbirth -> Letigress "hits harder"; Juggernaut -> others.
Root cause: having() counted any stat change as both stats and any target.
Same error elsewhere: Runeterra 41 "more power: it hits harder" (Ballistic Bot's Augment on itself, Glare's Gloom, spells
like Final Spark); Stormbound Spare Dragonling's gift to non-Dragons; level forms lost their types (Pyke (level 2)).
Fix: gains per stat (strength is both) and per target filter; a level form keeps its card's types.

## F5 Makers of a made card that is drawn
Kaptain: Lilithe, Vorpal Reaver -> Inkling Surge "enables".
Root cause: the named-card rule linked makers straight to the asker though the made card was a node.
Same error elsewhere: Runeterra 11 "makes a Celestial", 5 "makes the Poison Puffcap", 5 "makes the Chime"; Monster Train 2
(Morselmaker, Shardtail Queen); Stormbound Qordia's Nest.
Fix: when the made card is drawn, makers put it into play and it enables the asker; "another" in a condition still asks.

## F6 Keywords and acts that help were "can aim at it"
Kaptain: Cyclone Mask -> the General not linked (only a faint "can aim at it").
Root cause: BUFFS lacked ranged, flanking, haste, taunt, placement_rules; helps_it lacked ready, countdown_advance,
damage_reduction.
Same error elsewhere: Runeterra 3 countdown lines; Faeria Spirit-like readies; Duelyst Spirit of the Wild, Timekeeper.
Fix: those keywords and acts are help ("helps").

## F7 Moves and positions
Kaptain: Azurite Lion (Celerity) not linked to Holy Immolation.
Root cause: Duelyst Celerity caused no moves; a position measured from my unit ("enemies around it") made a moves need only
for the enemies; a card moving itself had no kind (so the Lion moved "your leader").
Same error elsewhere: Stormbound Tode the Elevated -> Toxic Sacrifice now "your units move"; none wrong found elsewhere.
Fix: Celerity causes moves; positions measured from my unit (its own "around this one", or "around it" of my first target)
need my units moved; a card's own moves keep its kind.

## F8 The General's spell
Kaptain: each General's spell should be a node.
Root cause: the General's record held a copy of its signature card's effects.
Same error elsewhere: none (Runeterra champion spells are cards already).
Fix: the spell is its own card (fixes/duelyst/v41.py; supplement_duelyst.py names it in the General's text), drawn with the
deck: General -> spell "casts its own spell".

## F9 Protection triggers and tokens
Found reading again: Tempest -> Arclyte Regalia "waits"; Dispirited Prisoner -> Hideatsu "counts when played"; Abyssal Scar
-> the General "gives it an ability".
Root cause: a trigger that only prevents damage was a wait; tokens summoned on the board counted as played; a delayed ability
the player gets was help to the leader card.
Same error elsewhere: none found in the other games' gone and new lines.
Fix: protection triggers wait for nothing; board-only tokens are never played or drawn; give_ability on the player is no help.

## Kaptain's second check (30 Oct 2026, v46): families F10-F15
Lines before -> after (dump_lines.py, network code before and after; links are now one per pair): Runeterra 6104 -> 4286
(pairs 4376 -> 4286), Stormbound 891 -> 699, Faeria 538 -> 407, Duelyst 515 -> 436, Monster Train 102 -> 75, Inscryption
162 -> 146 (no pairs gone outside Runeterra). Every gone pair read: 47 Invoke Celestial asks, 34 rule lines, 5 heals on itself
or the Nexus, 1 Otterpus ask (now "creates").

## F10 Heals inside "makes stronger"
Root cause: network.py help_kind put "can heal it" under stronger.
Same error elsewhere: every heal line of every game (Duelyst 82, Runeterra and Faeria heal spells).
Fix: its own kind "heals" (page colour and legend).

## F11 Help to itself or to the player read as help to units
Root cause: having() counted a card that acts anywhere on my side plus a heal or protection concept; healing itself and the
Nexus (Cosmic Youngling) became "more health: survives damage" for Braum.
Same error elsewhere: Runeterra Spectral Surveyor (Lifesteal heals the Nexus), Radiant Guardian (Tough on itself), 5 pairs.
Fix: effects on itself, or heals, stats and keywords on the player, help no unit; Rally on the player still gives another
attack (Blood in the Water, Sion Returned keep their lines). Case n38 rewritten by Kaptain's word.

## F12 What a card makes read as what it asks for
Root cause: lines_of took the filter of a making keyword's action ("Invoke a Celestial", "Manifest an Otterpus") as an
ask; refs.py took a keyword in a create or summon filter ("create a follower with Challenger") as a keyword need.
Same error elsewhere: Runeterra 47 "makes a Celestial it asks for" (Behold the Infinite -> Supercool Starchart), 1 Otterpus
ask; keyword needs from making filters: Runeterra 20, Duelyst 7, Faeria 1.
Fix: such filters describe the made card: no ask, no need; a making keyword that names a card puts it into play (Trinket Trade
-> Otterpus "creates"). Case n70.

## F13 Trap lines said "activates traps"
Root cause: the active verb for trap_activated named the opponent's act as the planter's.
Same error elsewhere: every trap planter in Runeterra (Teemo, Peddlers, Poison Dart, Chime -> Proximity Puffcap).
Fix: "plants traps that go off later"; the trap card itself "is a trap that goes off". Case n71.

## F14 Two links between the same two cards
Root cause: one need read by two rules (lines_of asks read played/summoned/drawn triggers that played_lines reads;
need_lines counted played spells that played_lines reads), the same fact said twice (a stat gain and "more power"; a cost cut
and "pays for it"; a rule line beside the card's own ability; "through" lines repeating what the maker does itself or going
through two made cards), and each different need drew its own arrow.
Same error elsewhere: all games (line counts above): Faeria Windstorm Colossus, Stormbound Shaped Stone, Runeterra Sejuani.
Fix: one rule per need; no second saying of the same fact; one link per pair whose kind is the first reason in a fixed order
(puts, levels into, levels, enables, waits, moves, clears, heals, keyword, stronger, cheaper, ...), every reason listed.

## F15 "You" exempted rule lines in games without leaders
Root cause: v42's leader exemption (a need naming the leader keeps rule lines) took the player as the leader in every game.
Same error elsewhere: Runeterra 17 "damages the enemy player (by fighting)" (Fortune Croaker -> Sejuani (level 2)).
Fix: the exemption only in games with leader cards.

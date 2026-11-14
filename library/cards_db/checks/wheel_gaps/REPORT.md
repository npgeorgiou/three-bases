# Wheel gaps (todo item 13), 14 Nov 2026. Nothing rebuilt: cards.sqlite is still the old one; the next rebuild (run.py / check_all.py) and axes.py show the effect.

## 1. Faeria Green: my unit fights a chosen enemy
- Cause: script. The rows were right (act start_attack, `to` = chosen enemy unit, concept attack_now), but nothing counted a strike/fight on an enemy as damage on an enemy; axes.py reads only `on_side='enemy'` damage rows.
- Existing concept: none fits (on_fight is a trigger, attack_now only says "attacks now", forced_attack is making an enemy attack). Runeterra's "strike each other" cards use the same rows (act strike, `to` enemy).
- NEW concept `fight_enemy` (concept_tree.txt, parent hurts_enemy): "A card makes my unit strike or fight enemy units now, so they take its damage and may die"; not this: own normal attack (on_attack), making an enemy attack (forced_attack), damage the text names (damage).
- Rule: flat.py RULES, `fight_enemy` = act strike/start_attack, origin own, `to` an enemy unit (or unit_or_structure), not "nearest", the actor not on the enemy side, not a keyword card. Read on the stored rows (read-only SQL): 64 cards: Faeria 3 (Deepwood Stalker, Frog-Tosser, Hunt Down), Duelyst 2 (Bloodsworn Gambler, Lavaslasher), Stormbound 1 (Lunatic Lunas), Runeterra 58 (Single Combat, Concerted Strike, Condemn, Brutal Skirmish, Fish Fight, Judgment, ... all `strike`/`start_attack` cards with an enemy `to`).
- axes.py: new list DAMAGE_BY_CONCEPT = ('fight_enemy',) joins the cards counted as damage on an enemy (unit text -> textdmg, spell -> spelldmg). No card names in axes.py. I chose textdmg/spelldmg, not kills: a fight is damage, it does not always kill.
- Files: flat.py, ../concept_tree.txt, BRIEF.md (rule 30 line), axes.py (list + query + check line).
- Check line: CHECKS ('faeria','Green','textdmg',0.3) (was 0.129; my estimate with 2 unit cards is about 0.4; Hunt Down is a spell and Faeria has no spelldmg value). Unsure: the 0.3 is an estimate, not run.

## 2. Into the Breach: weapon damage not on enemies
- Cause: data. Weapon text names a tile / unit_or_structure, so the reader stored no side (and the game says friendly fire is on).
- Fix: fixes/into_the_breach/v89.py (run once, safe twice): in weapon cards (category ability), damage on chosen / all / nearest / highest units or structures with no side gets side enemy ("it" follows, self/actor recoil left alone). 61 weapon cards, 141 effects changed (batch_003: 21 cards, batch_004: 40 cards). Cards: Titan Fist, Burst Beam, Electric Whip, Vice Fist, Flame Thrower, Hydraulic Legs, Explosive Vents, Mercury Fist, Prime Spear, Sidewinder Fist, Rocket Fist, Titanite Blade, Vortex Fist, Thermal Discharger, Hydraulic Lifter, Fissure Fist, Prism Laser, Refractor Laser, Spring-Loaded Legs, The Big One, Taurus Cannon, Aerial Bombs, Ramming Engines, Janus Cannon, Unstable Cannon, Astra Bombs, Heavy Rocket, Rail Cannon, Shock Cannon, Shrapnel Cannon, AP Cannon, Ricochet Rocket, Reverse Thrusters, Quick-Fire Rockets, EM Railgun, Fracturing Shells, Guided Missile, Artemis Artillery, Rocket Artillery, Rock Accelerator, Cluster Artillery, Vulcan Artillery, Aegon Mortar, Gemini Missiles, Heavy Artillery, Micro-Artillery, Raining Death, Arachnoid Injector, Smoldering Shells, Tri-Rocket, Cascading Resonator, Rebounding Volley, Seismic Capacitor, Enrage Shot, Targeted Strike, Grid Assault, Bombing Run, Grid Charger, Ramming Speed, Needle Shot, Explosive Goo (list from the old database, 61).
- Unsure: this is the game rule "weapons are aimed at Vek", not a word of the card text (friendly fire stays possible). Vek (monster/boss) attacks have the same missing side (47 monsters, 12 bosses): NOT changed, they are no wheel faction; ask Kaptain.
- Files: fixes/into_the_breach/v89.py, axes.py. Check lines: CHECKS ('into_the_breach','Ranged','textdmg',0.5) and HAS ('into_the_breach','textdmg') (the radius had no value: fewer than 10 cards).

- CHANGED by the main chat (14 Nov 2026): v89 is withdrawn and the records are as before. Marking weapon damage as "enemy" broke case ntb18 (Janus Cannon hits its own frozen Cryo-Launcher to free it: friendly fire is a real play) and said more than the card text. Instead axes.py counts Into the Breach weapon damage with no side as damage on enemies (DAMAGE_NO_SIDE_GAMES).

## 3. Monster Train, Umbra: Cave In
- Cause: data. "Descend friendly and enemy units" was one effect with no side (side none = either), so it is not marked as on enemies.
- Fix: fixes/monster_train/v88.py (all games' texts searched for "friendly and enemy" wording; only Monster Train has it): the effect is split into a mine and an enemy effect. 2 cards: Cave In, Inferno ("Deal 100 damage to friendly and enemy units"; same cause). Other Monster Train cards that move units say "a unit" (either side by the text): left as they are; Siren's Song, Steel Pulleyclaw, Crypt Builder already have side enemy.
- Monster Train is NOT_MEASURED in axes.py: no check line.

## 4. Monster Train, Hellhorned: Imp-in-a-Box
- Cause: none found in the data. The stored rows already give generate_cards (act create, zone hand); every Monster Train card with "add/put/create ... to your hand/deck" in its text has generate_cards. Nothing changed. The todo item was probably older than the Monster Train import. (Monster Train is NOT_MEASURED.)

## 5. Monster Train, Awoken: Sting, Bramble Lash
- Cause: none in the data. Both have a damage row on `all enemy unit` (front of lane), concept damage, so axes.py's rule already makes them spelldmg. Only other miss over all Monster Train spells with "Deal ... damage ... enemy" text: Inferno ("friendly and enemy units"), fixed by v88 (gap 3). Monster Train is NOT_MEASURED, so no value shows. Nothing else changed.

## 6. Runeterra, Demacia: Judgment
- Cause: script. flat.py's aoe_damage / multi_target_attack rules read only act damage; a strike by my unit on enemies (act strike, `to` enemies) had neither.
- Rule (flat.py RULES, same condition as gap 1): `to_pick='all'` gives aoe_damage (Judgment, Garen's Judgment: "strikes all battling enemies"). By the concept tree "all" is aoe_damage, not multi_target_attack (that is two separately named targets); both are in the `many` radius for Runeterra. Two separate named targets give multi_target_attack: Boomerang Blade (strongest and weakest), Fish Fight. Random targets (Frenzied Feast, Jaull-fish) stay random_target; "2 allies strike one enemy" (Concerted Strike) is neither.
- Files: flat.py, axes.py. Check line: CHECKS ('runeterra','Demacia','many',0.1) (was 0.06; estimated about 0.16, not run).
- Fish Fight's text was not read: unsure it belongs to multi_target_attack.

## Not run
run.py, check_all.py, links.py, axes.py. After a rebuild: `python3 axes.py` must print no CHECK FAILED; the new rules touch network lines (fight_enemy, aoe_damage on strikes): dump_lines before/after must be read.

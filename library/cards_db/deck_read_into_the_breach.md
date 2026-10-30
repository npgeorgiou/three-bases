# Into the Breach: what was wrong, and the deck reads

## Before the fix (30 Oct 2026, one pass after the first build)
Read: text audit (62), word check (100 flags), proposals (32), second reading (30 cards, 24 differ), link audit (16).
Families F1-F6 were fixed by fixes/into_the_breach/v48.py, names.tsv and patterns.tsv strips, then one rebuild.

Judged and kept:
- Word check: the Massive reminder, "all other damage (Push, Blocking, Fire, etc.) is unaffected" and "fire a projectile"
  are stripped (S-TB1 to S-TB3); 64 flags left were wiki prose or said another way: verdicts.tsv.
- Text audit: 60 flags are wiki prose in Vek texts (spawn limits, looks) or said another way: audit_text_explained.tsv.
- Second reading: the first reading writes a weapon's use as event attacks, the second as activated; the first is used
  for every weapon (a weapon is the mech's attack). Ally Immune and Building Immune upgrades: the first reading's form
  (cant strikes, to my units or my landmarks) is used by all 20 such upgrades. The other differences are the same meaning.
- Proposals left unsure, one text each: grid_defense_chance (Civilian Building), picked_up (Marked tile), splash_damage_victim
  (Cascading Resonator), gain_xp (Ralph Karlsson), reactor_core (Mafan), disable_keyword (A.C.I.D.), ignores_armor
  (Explosive Decay), direct (Energy Shield), moves (Flying); second_in_line and arachnoid_attack are one weapon each (the
  weapon and the mech that carries it share the text).
- Link audit: Spore, Alpha Spore, Alpha Blob, Blob Leader, Boulder, Unstable Boulder, Freeze Mine, Strange Pod and Strange
  Object are named by Vek or tiles but have no entry in the source (RESULTS.md); Emerging and High Tide are each one tile
  with two library pages (terrain and modifier, same text).

## F1 Damage that changes along the line or with hits
Cards: Burst Beam, Laser Mech, Rail Cannon, Prism Laser, Refractor Laser, Reverse Thrusters, Thruster Mech, Laser-Bot,
Laser-Mech, Boom Laser ("Damage: 3-1", "0 - 2", "2 damage reduced by range").
Root cause: BRIEF "Game words: Into the Breach" told readers to write min and max "as the first number written" and mark
unsure; min and max are lower and upper limits in vocab, so "3-1" became min 3, max 1.
Same error elsewhere: only this game writes damage as "N-M"; Stormbound's "4-5" already uses x range.
Fix: every damage with min and max becomes amount `{"x": "range", "items": [low, high]}` (v48.py F1); BRIEF says so.

## F2 Flip its attack direction
Cards: Aegis Mech, Spartan Shield, Confuse Shot, Mass Confusion.
Root cause: no value for turning an enemy's announced attack; readers made a keyword_action "Flip attack direction".
Same error elsewhere: no other game announces enemy attacks ahead; no other game uses that keyword.
Fix: act redirect_attack (vocab v48, no concept yet: Claude's suggestion for Kaptain's check); BRIEF says so.

## F3 Range upgrades with no reach written
Cards: Explosive Warp, Shield Placer, Smoke Bombs ("+2 Range" with no base range); Thruster Mech, Reverse Thrusters
("max distance and damage by 1").
Root cause: the other range upgrades write the new reach (can attack, distance le N); these texts give only the change,
so readers wrote increase_effect amount 1, unsure; the damage half was left out.
Same error elsewhere: upgrades are this game's only; the range upgrades with a written reach were right.
Fix: increase_effect params range N (new param); the "and damage by N" upgrades also get the damage (v48.py F3).

## F4 Damage by its origin
Cards: Natural Armor, A.C.I.D., Corroding A.C.I.D., Force Amp, Stabilizers.
Root cause: no state for weapon damage, bumps or blocking emerging Vek; readers left the condition out or wrote "damaged".
Same error elsewhere: Runeterra's combat damage already uses origin combat; other games name no damage source.
Fix: states weapon, bump, blocking_emerging; event damaged with COND it_matches origin (v48.py F4); BRIEF says so.

## F5 Tiles that turn into Lava
Cards: Lava Flow, Tentacles.
Root cause: no terrain lava; readers used damage_space (Duelyst's harmful space), which the source does not say.
Same error elsewhere: no other game has lava.
Fix: terrain lava (vocab v48); v48.py F5.

## F6 Other games' keywords written on moves
Cards: 103 pushes, 14 pulls, 7 charges, 5 dashes, 5 jumps, 4 tosses, 2 teleports, 2 flips; Leaper's Jump; Smoke Bombs.
Root cause: readers named the move with a keyword of Stormbound or Faeria (Push, Pull, Charge, Dash, Teleport) or a made-up
one; Into the Breach has no such keywords.
Same error elsewhere: Inscryption and Duelyst had the same and drop them in names.tsv; Faeria's and Stormbound's are their own.
Fix: names.tsv drops them for into_the_breach (the move stays; act move gives forced_movement or movement); Leaper's
"Jump" is can move; Flying written on a move is dropped from it (v48.py F6). "Reset Turn" and "flip target" have no
value: Isaac Jones and Seismic Capacitor stay unsure.

## Deck read (30 Oct 2026, all 20 squads, after the v48 rebuild; 107 lines)
Read with deck_lines.py, both cards' texts side by side. Nothing below is fixed yet: each family gets its rule, a
cases/network.tsv row and a rebuild in the next step. Lines a player would keep: Bombling Mech -> Walking Bomb and Arachnoid
Mech -> Arachnoid (summons), Meteor Mech -> Flame Mech (Fire for Flame Thrower's "damage units already on Fire"), Pulse,
Slide and Hook Mech giving Energy Shield to an ally, Flame Mech -> the other mechs (Fire Immunity).

## F7 Every pusher "enables" every weapon (95 lines, 18 of 20 squads)
Lines: "makes units move", "makes enemy units move", "makes your units move", "moves it for its effect" between nearly all
pairs (Combat Mech -> Cannon Mech, Artillery Mech -> Combat Mech ...).
Root cause: refs.py state_rows: a target picked by position ("in a line from self", "adjacent to self") is a need for moves,
and from my own unit a need for moving it (Kaptain's Duelyst rule 7: Holy Immolation, Bonereaper). Every Into the Breach
weapon aims from its mech and nearly every weapon pushes, so every pair links.
Same error elsewhere: to be measured with dump_lines.py --find "move" in every game before any change.
Fix: none. Kaptain (30 Oct 2026): "things that move stuff benefit things that depend on stuff's position"; pushing an enemy
into another mech's line of fire is help. These lines stay; the family is decided, not an error.
Kaptain (30 Oct 2026, after the F8-F12 fix): "makes enemy units move" did not say why. Every such line, in every game, now
says both halves: "moves units; what it does depends on where they stand (in a line from it or next to its target)"
(network.py moves_said, merge_places: one reason per pair, every place joined). Only the words changed, no line.
Reading every line again after that showed three more errors of the same family, fixed in every game: a card that only
moves itself (Ice Mech's Flying, Thruster Mech, Tode the Elevated) puts no enemy where another card hits (gone: Ice Mech ->
Mirror Mech, Thruster Mech -> Control Mech, Tode -> Ubass); a swap moves the unit swapped with too (refs.py: Swap Mech ->
Flame, Laser, Ice, Meteor, Boulder Mech stay; new Hearth-Sister -> Warbird in Duelyst); a card that picks any space
(Chromatic Cold) does not care where units stand.
Kaptain (30 Oct 2026): the labels were hard to understand. The move labels and Viscera Nanobots' label now name both cards
("Combat Mech moves units, and Artillery Mech acts on units in a line from it"; "Nano Mech heals Leap Mech when Leap Mech
kills"); the page shows each reason of a line on its own row.

## F8 "is a unit_or_structure it asks for" (49 lines; Stormbound 3 lines, Tode the Elevated)
Lines: Combat Mech -> Artillery Mech, Walking Bomb -> Pierce Mech ...
Root cause: network.py need_lines reads a position measured from another thing ("the tile beyond the pushed unit", of kind
unit_or_structure) as a need for a card of that kind on my side; it skips kind unit (always there) but not unit_or_structure.
Same error elsewhere: Stormbound, 13 lines to Tode the Elevated (all decks); no other game writes that kind in a position.
Fix: need_lines treats unit_or_structure like unit there. Gone: 49 Into the Breach lines, 13 Stormbound lines to
Tode the Elevated (all decks). Case ntb1.

## F9 "is a Mech it asks for" towards a passive that helps all Mechs (6 lines)
Lines: Swap Mech -> Flame Mech, Meteor Mech -> Flame Mech (Flame Shielding), Thruster and Control Mech -> Smog Mech
(Nanofilter Mending), Dispersal and Quick-Fire Mech -> Napalm Mech (Heat Engines).
Root cause: network.py type line takes the passive's target type (Mech) as something it asks for; Kaptain's rule (30 Oct): a
passive that helps cards points from it to them, and those cards do not enable it. The help line (Flame Mech -> Swap Mech)
is right.
Same error elsewhere: Slay the Spire 49 lines ("is an Attack it asks for" to Strength cards); none in other games.
Fix: the type lines skip an effect that helps my cards: removing a status that is no buff (Fire, Smoke) and what a
helping keyword the card gives does (Fire Immunity, Boost). A keyword's concept now comes from the game's own vocab entry
first (into_the_breach:Boost is a buff; another game's Boost is not). Same error in Slay the Spire: 49 "is an Attack it asks
for" lines to Strength cards are gone (NEXT_CHAT family 1); the help lines it wants are still missing there. Case ntb2.

## F10 Viscera Nanobots: wrong side and wrong direction (2 lines; 2 missing)
Lines: Leap Mech -> Nano Mech, Unstable Mech -> Nano Mech "triggers: kills your units". Viscera Nanobots heals any Mech that
deals a killing blow: the lines should be Nano Mech -> Leap Mech and Nano Mech -> Unstable Mech, "heals it when it kills".
Root cause: a damage target with no side is read as my units, and the trigger's actor (a Mech) is not used to point the
help at the killer.
Same error elsewhere: Runeterra 3 new lines (LeBlanc level 2 counts damage you deal); Duelyst 1 (Spectral Blade).
Fix: refs.py: on "killed" and "damaged" with no object, the actor is who does it, the victim is not said (also
LeBlanc level 2 "each time you deal 15+ damage": damage dealers now feed it). network.py: a trigger that only helps the
unit that did it (doer_help_abilities) waits for nothing; a help line goes from the card to the deck's cards of that kind
that do it (doer_help_lines): Nano Mech -> Leap Mech and Unstable Mech "heals it when it kills". Case ntb3.

## F11 Vek Hormones set off by my own damage (2 lines)
Lines: Judo Mech -> Gravity Mech, Siege Mech -> Gravity Mech "triggers: damages enemy units or players". Vek Hormones adds
damage only when an enemy damages another enemy; the record says actor side enemy.
Root cause: the line matches the event's object (enemy units) and does not check its actor.
Same error elsewhere: no other game's lines changed.
Fix: a trigger's actor side is kept; an enemy actor is fitted only by cards that make an enemy strike, attack or
turn its attack. Cases ntb4, ntb6.

## F12 Statuses on tiles do not reach cards that ask for units with them (missing lines)
Missing: Thruster Mech -> Smog Mech (Reverse Thrusters leaves Smoke; Nanofilter Mending repairs Mechs standing on Smoke),
Defense Mech -> Laser Mech and Charge Mech (Shield Projector shields tiles).
Root cause: give_keyword on kind position (tiles) is not read as giving it to the unit on that tile.
Same error elsewhere: no other game's lines changed (Monster Train's one tile keyword feeds nothing in its decks).
Fix: a keyword given to a tile reaches the unit on it (lines_of and aimed_rows read kind position as
unit_or_structure). New: Thruster Mech -> Smog Mech (Smoke), Defense Mech -> Laser Mech and Charge Mech (Energy Shield),
Jet Mech -> Rocket Mech (Smoke for Storm Generator). Case ntb5.

## After the fix (30 Oct 2026, one rebuild)
Into the Breach 107 -> 99 lines; Stormbound 696 -> 683; Slay the Spire 451 -> 410; Runeterra +3 (LeBlanc level 2); Duelyst
+1 (Lilithe -> Spectral Blade); other differences are only the order of reasons. Cases pass in every game (Stormbound 141
of 145, the known csb09-csb13). ntb6 (Aegis Mech -> Gravity Mech: Spartan Shield turns an enemy attack onto enemies, Vek Hormones) keeps the F11 exception tested.

## Check of 20 cards (30 Oct 2026, Claude; CHECK_20_into_the_breach.md, ids in CHECK_20_into_the_breach_ids.txt)
Each card's rows read against its text: Centipede Leader, Quick-Fire Mech, Hook Mech, Emerging, Alpha Hornet, Spring-Loaded
Legs, Alpha Bouncer, Raining Death, Alpha Beetle, Techno-Scarab, Tentacles, Meteor Mech, Alpha Scarab, Mine-Mech, Cannon Mech,
Alpha Mosquito, Repulse, Burrower, Ramming Speed, Lily Reed. 15 right; 4 errors (F13-F16), fixed by fixes/into_the_breach/v51.py.
The guide-deck explanations (ask.py into_the_breach analyze, all 20 squads) showed three more (F17-F19).
Kept: Emerging writes "a Vek emerges" and "a unit blocking it takes 1 damage" side by side (the text does not say the
blocked Vek stays down); Flying keeps "not given A.C.I.D." although the wiki text says both "not affected by A.C.I.D. tiles"
and "not immune to A.C.I.D. pools" (marked unsure).

## F13 Flying stands on mountains and enemy units
Cards: Flying (keyword), so every flying unit (Alpha Hornet, Alpha Mosquito, Jet Mech, Swap Mech ...).
Root cause: the text "can be positioned at any terrain tile, except mountains and other units. Mountains and unfriendly units
can be overflown" was read as two more places to move onto; flying over is no place to stop.
Same error elsewhere: no other game writes a can-move onto mountains or onto enemy units (flat_do query, every game).
Fix: v51.py drops the can-move rows onto mountains and enemy units when the text says so. Case mtb1.

## F14 "Shield adjacent ally or Building" picks one
Cards: Repulse, Pulse Mech (Shield Friendly).
Root cause: "Shield adjacent ally or Building" has no choice word; it shields every adjacent ally and building.
Same error elsewhere: no other card of any game has a chosen help next to it with no choice word and "adjacent ally" in its text.
Fix: v51.py makes it pick all. Pulse Mech -> Jet Mech and Rocket Mech now say "gives it Energy Shield". Case ntb7.

## F15 Burrowers hit any 3 tiles around them
Cards: Burrower, Alpha Burrower ("Slam against 3 tiles in a row"; wiki: "a 3-tile wide area in front of them").
Root cause: "in a row" was read as 3 chosen tiles around it; it is the tile in front and its two sides.
Same error elsewhere: Hornet Leader's "three tiles in a row" is ahead of it, as its text says; no other game.
Fix: v51.py: damage to all on the tile in front and its sides. Case mtb2.

## F16 "Increases area hit by 1 tile" read as wider pushes
Cards: Explosive Goo, Techno-Scarab.
Root cause: no value for a bigger hit area; readers wrote pushes within 2 tiles, which the text does not say.
Same error elsewhere: only this game words an upgrade that way.
Fix: param area (vocab v51): increase_effect params area 1. Case mtb3.

## F17 Swap Mech "waits for your units getting Webbed"
Cards: Swap Mech, Teleporter ("if you are webbed and swap places with another unit, the other unit will become webbed").
Root cause: a condition that the card has a status it passes on was read as a status it wants (ask.py analyze: weak spot).
Same error elsewhere: none in other games (flat_ref query).
Fix: refs.py drops a "has status X" need when the same ability gives X to another. Squads with Swap Mech have no weak spot now.

## F18 The deck explanation missed Smoke on tiles (F12 in ask.py analyze)
Cards: Jet Mech, Thruster Mech and every weapon that puts a status on a tile.
Root cause: F12 was fixed in network.py only; ask.py analyze reads flat_ref, where a keyword given to a tile had kind position.
Same error elsewhere: Monster Train's one tile keyword (Molluscmage) now reaches units too; no deck line changed.
Fix: refs.py writes a keyword given to a tile as given to the unit or structure on it (one rule for both); network.py's
own copy removed. Rusting Hulks: "Enemy units get Smoke: made by Jet Mech. Use it: Rocket Mech". Case dtb01.

## F19 The deck explanation fed Vek Hormones with my own damage (F11 in ask.py analyze)
Cards: Gravity Mech (Vek Hormones) in Steel Judoka.
Root cause: F11 was fixed in network.py only; deck_analysis did not check who must do it.
Same error elsewhere: no other game's deck explanation changed (cases pass).
Fix: deck_analysis.py: a trigger whose doer is an enemy is fed only by cards that make enemies act. Steel Judoka no longer
says "Enemy units take damage: made by Judo Mech, Siege Mech. Use it: Gravity Mech".

## F20 The squads had no weapons (Kaptain, 30 Oct 2026: "In this game you can equip mechs with extra weapons")
Cards: every squad in decks.tsv; every mech.
Root cause: a squad was written as its 3 mechs, each mech's record carrying its starting weapon and passive; the weapons and
passives that are cards of their own (Titan Fist, Storm Generator) and the extra weapons a run equips were never in a deck.
Same error elsewhere: no other game has cards carried by another card in a deck.
Fix: fixes/into_the_breach/v52.py: a mech's record keeps only its own keywords (Flying, Massive, Natural Armor); its weapon
and passive rows stay on the weapon and passive cards. decks.tsv lists each mech with its starting weapon and passive; 6 new
decks from players' runs and guides add their extra weapons (Sevastromo's Unfair runs: Rift Walkers, Rusting Hulks,
Hazardous Mechs, Zenith Guard; CelJaded: Force Amp with Rift Walkers and Secret Squad). Quick-Fire Artillery (Zenith run)
is not in the source and is left out. The lines are now between weapons ("Titan Fist moves units, and Artemis Artillery acts
on units in a line from it"); a mech is a dot whose lines are what is given to it (Energy Shield, Fire Immunity). Case ntb10;
cases ntb1-ntb7 rewritten on the weapons.
The weapon and passive wording in a mech's text is stripped for the word check and the text audit (pattern S-TB4; audit_text.py
now skips every game's strip wordings, which changed no other game's count).

## F21 A weapon is no Mech, so "any Mech that kills" found no killer
Cards: Viscera Nanobots (heals a Mech that kills) with every weapon.
Root cause: once weapons are cards, the one who kills is the weapon card, which is no Mech; the line went missing.
Same error elsewhere: no other game has carried cards (network.CARRIED lists Into the Breach weapons only).
Fix: network.py as_doer: a weapon acts as the mech that carries it; the label says "the mech with Hydraulic Legs".
deck_analysis.py: a mech whose weapons are in the deck is no "no clear role". Case ntb3.

## F22 Force Amp fed by any damage
Cards: Force Amp ("All Vek take +1 damage from Bumps and blocking emerging Vek").
Root cause: its trigger is damage to enemies with a condition on the damage's origin (bump); the line read only "damaged",
so every weapon that damages fed it, and Storm Generator's Smoke too.
Same error elsewhere: no other game has bump damage; Runeterra's "origin not combat" is untouched (its lines are the same).
Fix: network.py: a need for damage only from bumps is fed by the cards that push enemy units ("Titan Fist pushes enemy
units into things (bump damage)"). Cases ntb8, ntb9.

## F23 The deck explanation missed shields on tiles and damage the player aims
Cards: Shield Projector ("no clear role"), Guided Missile, every weapon that damages a target of no side.
Root cause: deck_analysis counted support only on my side and control only on enemies; Into the Breach weapons aim at any
tile, and a shield is given to a tile.
Same error elsewhere: no other game's deck explanation case changed.
Fix: deck_analysis.py: help of a support kind on a target of no side is support; harm on a target the player picks with no
side is control (as refs.py's HARM rule).

## F24 The mechs were linked to nothing, and builds broke the loadout rule (Kaptain, 30 Oct 2026)
Cards: every mech; the builds of F20.
Root cause: after F20 a mech kept only its keywords, so most mechs had no line; and the builds were taken as card lists, not
as which mech carries what. Kaptain: a mech has 2 weapon slots (a passive takes one); its starting weapon and one more,
never two extra.
Same error elsewhere: no other game has carried cards.
Fix: decks list each mech, then what it carries; network.py draws "Combat Mech carries Titan Fist" (kind carries, first in
KIND_ORDER; network_page.py colours it). Builds checked against the rule: Hazardous Mechs' run (Nano Mech would hold
Teleporter, Frost Beam and Viscera Nanobots, and Force Amp's mech is not said) and the two CelJaded Force Amp builds (no mech
said) are dropped; in the Rusting Hulks run Force Amp goes on Jet Mech, the only free slot. Cases ntb11; ntb8 moved to the
Rusting Hulks run. The rule is in BRIEF "Game words: Into the Breach" and library/games/into_the_breach.md.

## Claude's builds (30 Oct 2026; Kaptain: "put something that makes sense")
Most official squads leave one slot free per mech, and players post their loadouts as pictures, not text. At Kaptain's word
Claude filled the second slot of every mech in the 14 squads and the 6 custom squads (decks.tsv: the squad's row lists both
weapons of each mech; its source says which are Claude's; the 3 players' runs stay as they were played): weapons of the
mech's class or Any class, chosen for what the squad does, from guides where they name one (Cluster Artillery on the Boulder
Mech, Vek Hormones moved to the Siege Mech, Viscera Nanobots moved to the Unstable Mech, Frost Beam on the Nano Mech, Rail
Cannon and Control Shot in Arachnophiles), else Claude's choice; each row's source says why. Every build is checked: 2
items per mech at most, class or Any. Reading their networks found F25 and F26.

## F25 Smoke Pellets' Ally Immune read as removing Smoke
Cards: Smoke Pellets ("Ally Immune: No longer applies Smoke on self or allies").
Root cause: "no longer applies" was read as remove_keyword on my units, so it looked like it clears Smoke off my mechs.
Same error elsewhere: no other text in any game says "no longer applies".
Fix: fixes/into_the_breach/v53.py: cant given_keyword Smoke on my units there (as Smoke Immunity); the label says "keeps
Smoke off it" (network.py, every game's "can't be given"). Case ntb13.

## F26 Confuse Shot did not feed Vek Hormones
Cards: Confuse Shot, Mass Confusion, Aegis Mech's Spartan Shield (redirect_attack) with Vek Hormones.
Root cause: redirect_attack had no causes in vocab, so a turned Vek attack hit nothing in the records; only Spartan Shield,
which also deals damage itself, reached Vek Hormones.
Same error elsewhere: only Into the Breach has redirect_attack.
Fix: vocab: redirect_attack causes damaged, survives_damage, dies, killed. Case ntb12.

## F27 Holes, water and lava did not count (Kaptain, 30 Oct 2026: "Flood Drill makes a Hole, so of course it synergizes")
Cards: Flood Drill (holes and water), Seismic Capacitor and Fissure Fist (cracked ground, a hole once hit), and every weapon
that pushes, pulls or tosses Vek.
Root cause: the game's rule that a ground unit pushed into a Chasm is destroyed, and that most Vek drown in Water and Lava
(library/games/into_the_breach.md, wiki Tiles), was in the rules notes but in no record or line rule.
Same error elsewhere: Faeria makes oceans, where nothing dies; no other game has deadly ground.
Fix: network.DEADLY_GROUND (Into the Breach: chasm, water, lava, cracked ground): a card that makes it enables every card
that pushes enemy units ("Flood Drill makes holes, and Titan Fist pushes enemy units: a ground unit pushed into a hole
dies"); ask.py analyze says "Holes and water that kill pushed Vek". Case ntb14.

## F28 A.C.I.D. made no weapon stronger
Cards: A.C.I.D. Projector, Arachnoid Injector, every weapon that damages a picked target.
Root cause: the rule for statuses that make damage bigger (Slay the Spire's Vulnerable) read only "increase_effect"; A.C.I.D.
is written as extra damage equal to the hit; and a status put on a target of no side, or damage to one, was not seen as aimed
at enemies.
Same error elsewhere: none (cases and lines of every other game unchanged).
Fix: network.status_damage_givers also reads "damage self, amount = the hit"; a status or damage on a picked target of no
side is aimed at enemies (refs.py's HARM rule); bump damage is no weapon damage, so Force Amp gets no A.C.I.D. line. Cases
ntb15, ntb16.

## F29 Help to "Mechs on Fire" reached no mech
Cards: Heat Engines (Mechs standing on Fire get Boost), Nanofilter Mending (Mechs on Smoke are repaired).
Root cause: a filter "with keyword Fire" was matched against printed keywords; no mech has Fire printed, it is a status
given in play.
Same error elsewhere: none changed (the rule is kept to statuses no card prints, of the status kinds: damage over time, can't
attack, can't act, can't move, weaker, a bonus for one attack, shield).
Fix: network.matches: such a status filter fits any unit. Heat Engines -> Dispersal, Quick-Fire and Napalm Mech "gives it Boost".

## F30 A frozen mech is freed by a hit
Cards: Cryo-Launcher (freezes the Ice Mech too), every weapon that can hit my units.
Root cause: Frozen ends when the unit is damaged (its keyword record), so a hit on my frozen mech is help; no line said it.
Guides: Mirror Mech's Janus Cannon thaws the Ice Mech.
Same error elsewhere: only Into the Breach puts a bad status on its own unit that a hit removes.
Fix: network.py: a card that puts on itself a bad status that damage removes is helped by cards that can hit my units ("Janus
Cannon can hit the mech with Cryo-Launcher while it is Frozen: the hit frees it") and by cards that shield my units.


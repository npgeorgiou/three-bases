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

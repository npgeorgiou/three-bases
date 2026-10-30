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

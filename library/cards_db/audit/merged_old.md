# Merged causes (old check) - 16 files: f1-f4 (Faeria), r1-r7 (Runeterra), s1-s2 (Slay the Spire), u1-u3 (Duelyst)
Format per cause: wrong thinking | rule broken | games | files | examples.
File reference "f1 c4" = cause 4 in causes_f1.md.

## A. Movement and reach

1. Wrong thinking: a card's own move keyword (Flying, Jump, Dash, Charge, Aquatic) moves my other units forward, so the other card reaches enemy ground / enemy well.
   Rule: L20, L2 (also L7 for Luduan "this harvests"). Games: Faeria. Files: f1 c1, f2 c1, f3 c1, f4 c8 (duplicates).
   - Ghost Dragon -> Lost Explorer: moves: moves my units or land forward: they reach enemy ground
   - Windborne Emissary -> Luduan: moves: moves my units or land forward: they reach enemy ground
   - Airbot -> Imperial Trooper: moves into place: moves my units or land forward: they reach enemy ground

2. Wrong thinking: a card that moves nothing (land maker, land destroyer, turns land to lake, reactivates, moves only itself) is read as a mover.
   Rule: L1 (f1 also L20, L2). Games: Faeria, Duelyst. Files: f1 c1, f2 c3, f3 c1, u3 c9.
   - Wood Elemental -> Wavecrash Colossus: moves: moves my units or land forward: they reach enemy ground
   - Meteor -> Luduan: moves: moves my units or land forward: they reach enemy ground
   - Spirit of the Wild -> Avalanche: enables: Spirit of the Wild moves units, and Avalanche acts on units base's starting side or on your leader

3. Wrong thinking: any teleport triggers Corrupt / reaches enemy ground, even a teleport to my own land.
   Rule: L1. Games: Faeria. Files: f2 c4.
   - Desert Twister -> Baldurion, Evil Archsmith: waits: moves it for its effect
   - Sagami Grovecaller -> Monstrous Hydra: waits: moves it for its effect
   - Sagami Grovecaller -> Sapphire Yak: moves: moves my units or land forward: they reach enemy ground

4. Wrong thinking: "it can enter where it needs to be" is given to cards whose need is only where they are summoned (Gift read once at summon), or about themselves (own land, act next to self), or ask a kind the mover is not.
   Rule: L2, L1, L20. Games: Faeria. Files: f1 c2, f2 c2, f3 c2.
   - Barrensky Vulture -> Triton Tactician: moves: moves my units or land forward: it can enter where it needs to be
   - Spear of the Guardians -> Topaz Yak: moves: moves my units or land forward: it can enter where it needs to be
   - Syland Horsemaster -> Bomb Slinger: moves into place: moves my units or land forward: it can enter where it needs to be

5. Wrong thinking: a unit's own movement keyword (Celerity, Flying, Dash, Jump) or help to any creature means "A moves your units, and B acts on units next to/around it", so it pairs with every positional card.
   Rule: L20, L1, L14 (f2 also Secret of Strength / Triton Banquet = help to any creature). Games: Faeria, Duelyst. Files: f1 c3, f2 c6, f3 c1 (Boar/Kodama part), u1 c9, u2 c8, u3 c9.
   - Demonic Salmon -> Tiki Adventurer: type: Demonic Salmon moves your units, and Tiki Adventurer acts on units next to it
   - Dragonlark -> Vigilator: type: Dragonlark moves your units, and Vigilator acts on units around it
   - Azurite Lion -> Roar: enables: Azurite Lion moves your units, and Roar acts on units around your leader or base

6. Wrong thinking: a card that moves, teleports or gives Celerity only to the General is linked as moving the minion that needs to be moved behind an enemy / reactivated.
   Rule: L7. Games: Duelyst. Files: u1 c9 (second half), u2 c7.
   - Mist Walking -> Gore Horn: type: Mist Walking moves Gore Horn, and Gore Horn acts on units behind its target
   - Silhouette Tracer -> Mizuchi: type: Silhouette Tracer moves Mizuchi, and Mizuchi acts on units behind its target
   - Bombard -> Penumbraxx: waits: makes it attack for its effect

7. Wrong thinking: moving a unit lets its Combat effect go off ("moves it where it must be" to Combat cards).
   Rule: L2, L4. Games: Faeria. Files: f2 c9 (f3 unsure raises the same).
   - Windborne Champion -> King's Guard: moves: moves it where it must be
   - Spirit Spice -> Krog, the Ogre King: moves: moves it where it must be
   - Cloud Machine -> Herald of War: moves: moves it where it must be

8. Wrong thinking: a need about the enemy god is fed by any creature that reaches or attacks the god (own Flying/Charge reach, any attack, any damage to the opponent); some lines point the wrong way (Defender wants to be attacked; War Yak/Exalted Ogre read Life).
   Rule: L2, L1, L20, L9, L18. Games: Faeria. Files: f1 c4, f2 c7.
   - Seed of Paradise -> Defender of the Homeland: moves: moves it within reach of the enemy player
   - Demon Wing -> Zealous Crusader: moves: moves it within reach of the enemy player
   - Volcanic Colossus -> Oradrim Sagittarius: waits: makes your units hit the enemy player (by fighting)

9. Wrong thinking: a transform (Frogify, The World's Tear) that removes B's text is linked as helping that text (new form has Jump/Flying).
   Rule: L1. Games: Faeria. Files: f2 c8.
   - Frogify -> Oradrim Monk: moves: moves it within reach of the enemy player
   - The World's Tear -> Krog, the Ogre King: moves: moves it where it must be
   - Frogify -> Tax Collector: moves: moves it where it must be

10. Wrong thinking: "transforms" is equated with "built" (Cloudcaller/Disciple of Yggdra/Eternity Painter feed Rescue-RX/Architect-T2K5/Manakite Drifter).
    Rule: L10, L1. Games: Duelyst. Files: u1 c13.
    - Cloudcaller -> Rescue-RX: waits: transforms it for its effect
    - Disciple of Yggdra -> Architect-T2K5: waits: transforms cards
    - Eternity Painter -> Manakite Drifter: waits: transforms cards (for the ability it gives)

11. Wrong thinking: a card that hits Flying creatures (Destructive Volley) is fed by my own Flying cards.
    Rule: L9. Games: Faeria. Files: f1 c12.
    - Astral Weapon -> Destructive Volley: type: has Flying
    - Seed of Paradise -> Destructive Volley: type: makes units get Flying

12. Wrong thinking: a neutral card gets "turns a land into the colour it needs".
    Rule: L22. Games: Faeria. Files: f1 c13.
    - Fire Elemental -> Path to Paradise: type: turns a land into the colour it needs: helps pay its land cost
    - Ring of Dominion -> Path to Paradise: type: turns a land into the colour it needs: helps pay its land cost, and can take that land from the enemy

## B. Fighting, Nexus damage, credit

13. Wrong thinking: a unit's own fight keyword (Elusive, Overwhelm, Fearsome, Impact, Scout, Quick Attack) means it "damages the enemy player" / "helps it hit the enemy player" for every Plunder card and every Nexus-damage champion; also Plunder is checked when played, so helping the Plunder card later does nothing; many B are spells.
    Rule: L20, L2. Games: Runeterra. Files: r1 c2, r2 c1, r3 c14, r4 c1, r7 c3.
    - Alpha Wildclaw -> Snowy Razorclaw: damages the enemy player
    - Abyssal Eye -> Dashing Dandy: damages the enemy player
    - Necrotic Nestling -> Teenydactyl: type: helps it hit the enemy player

14. Wrong thinking: fighting itself (any unit can attack/block, counterattack, Frenzy, Blast, "attack again") is counted as making units die / strike / hit the Nexus / attack, so every unit is a source.
    Rule: L1, L2, L9, L18. Games: Runeterra, Duelyst. Files: r1 c1, u1 c3, u2 c11, u3 c5 (Dispirited Prisoner part).
    - Ye Been Warned <- Affectionate Poro: makes enemy units die (by fighting)
    - Faie Bloodwing -> Resonance Scythe: waits: kills enemy units (by fighting)
    - Piercing Mantis -> Gate to the Undervault: waits: makes units die

15. Wrong thinking: A makes B and B acts on C, but A is credited with what B does.
    Rule: L3. Games: Runeterra. Files: r5 c9, r6 c8, r7 c4.
    - Aurelion Sol -> Braum: more health or protection: survives damage (levels it up)
    - Captain Farron -> Swain (level 2): triggers: damages the enemy player; also helps it hit the enemy player
    - Tybaulk -> Snip Snip Snip!: makes stronger: its damage gets 1 more; also more power

## C. Help (stats, keywords, heals, damage)

16. Wrong thinking: help or a tutor aimed at a kind/group (Flying, Jump, Combat, yak, 5+ Life, 1 cost, Yordle, Elite, Fae, Fearsome, tribe, Lurker, Vespyr) is linked to every card of that kind, though the receiving text does not use it.
    Rule: L14 (also L15, L18, L1b). Games: Faeria, Runeterra, Duelyst. Files: f1 c8, f3 c3, f4 c2, f4 c3, r1 c3, r2 c3, r3 c1, r6 c4, u3 c1 (f2 unsure).
    - Drakkar Skycaptain -> Airbot: makes stronger: gives it more power and health when it comes
    - Yordle Captain -> Aatrox: gives it more power and health when it comes
    - Oakenheart -> Replicant: makes stronger: gives it more power and health

17. Wrong thinking: every heal, power boost, keyword or damage protection for "your General" is linked to every General card, whose only text is a Bloodbound Spell; Generals are in every deck.
    Rule: L14, L18, L20 (also L1, L13, L16). Games: Duelyst. Files: u1 c1, u2 c5, u3 c2, u3 c3.
    - Aer Pridebeak -> Argeon Highmayne: heals: can heal it
    - Dawn's Eye -> Argeon Highmayne: stronger: can give it more power
    - Cyclone Mask -> Shidai Stormblossom: gives keyword: can give it Ranged

18. Wrong thinking: a heal is linked to Provoke minions, though L18 lets only "more health" reach Taunt units.
    Rule: L14, L18. Games: Duelyst. Files: u1 c8 (u2 unsure, u3 unsure).
    - Lux Ignis -> Fireblazer: heals: can heal it
    - Sundrop Elixir -> Fireblazer: heals: can heal it
    - Healing Mystic -> Lady Locke: heals: can heal it

19. Wrong thinking: generic power/health is linked to a card whose text does not read its own stats, reads only the damage it deals/a fixed amount, or reads another card's stats (the General, equipment, a Tentacle).
    Rule: L18 (also L7). Games: Faeria, Runeterra, Duelyst. Files: f1 c7, r1 c7, r5 c8, u1 c7, u2 c6, u2 c12 (hits-several / splash part).
    - Path to Paradise -> Enslaved Priest: stronger: more power: its text uses the damage it deals when it comes
    - Adept Weaponsmith -> The Tuskraider: more power
    - Mirkblood Devourer -> Drogon: stronger: more power

20. Wrong thinking: all health/stat help links to a card that reads only Power (and its own stats are not read).
    Rule: L15, L18. Games: Runeterra. Files: r2 c5.
    - Tiny Shield -> Xolaani the Bloodweaver: can give it more health
    - Galio -> Xolaani the Bloodweaver: gives it more health
    - Bayou Brunch -> Xolaani the Bloodweaver: turns the Health it grows into Health

21. Wrong thinking: a stat boost on the board is linked to a card that already read its stats (Gift fight already happened, Play/summon effect already went off, card in hand vs played one, fight on summon).
    Rule: L18 (also L4, L14). Games: Faeria, Runeterra, Duelyst. Files: f1 c7 (Animated Banquet), f2 c13, r4 c3, u2 c12 (Lavaslasher).
    - Spirit Spice -> Barrensky Vermin: stronger: can give it more power and health
    - Rising Spell Force -> Banana Blaster: stronger: more power
    - Blood Rage -> Lavaslasher: stronger: can give it more power and health

22. Wrong thinking: a giver is linked as giving help it cannot give to B (narrow kind such as Ephemeral/1 cost, itself, enemies, only certain target, other card).
    Rule: L4, L8, L14, L9. Games: Runeterra. Files: r1 c8, r4 c4.
    - Here to Help -> Gangplank: more power: its text uses the damage it deals
    - Soul Shepherd -> Vi: stronger: more power
    - Ornn (level 2) -> Wrought Colossus: stronger: more health / more power

23. Wrong thinking: a stat change is linked to a card it cannot reach (structures Doomgate/Faeria Tree) or goes the wrong way (lowering Life where the card needs it to rise; a 6/6 stops Seedling).
    Rule: L8, L21. Games: Faeria. Files: f1 c6, f4 c4.
    - Tower of Curses -> Doomgate, Door to Oblivion: type: changes its stats for its effect
    - Aurora, Myth Maker -> Faeria Tree: type: changes its stats for its effect
    - The Emperor's Command -> Faeria Tree: enables: changes its stats for its effect

24. Wrong thinking: "spells deal 1 extra damage" / "double all damage" / "your damage boost" is linked to every spell or damage card (also to spells that deal no damage, to Last Breath/death effects, to champions that do not read damage).
    Rule: L18 (gives_lines: more damage alone is never a use; also L21, L4). Games: Runeterra, Duelyst. Files: r1 c4, r2 c4, r4 c6, r5 c20, r6 c1, r7 c1, u1 c15, u3 c4.
    - Powder Keg -> Advanced Intel: makes its effect bigger
    - Crescent Spear -> Phoenix Fire: stronger: makes its effect bigger
    - The Dreadway -> Decimate: makes stronger: doubles its damage

25. Wrong thinking: a boost/non-damage card (Tybaulk, Might, The Dreadway) is read as dealing damage or killing itself.
    Rule: L1, L3 (r7: L1/L4/L18). Games: Runeterra. Files: r6 c2, r7 c2.
    - Tybaulk -> The Harrowing: enables: makes your units die: The Harrowing brings them back
    - Might -> Scorched Earth: enables: more damage
    - The Dreadway -> Scorched Earth: enables: damages enemy units or players: Scorched Earth kills them

26. Wrong thinking: removing enemy Block, keeping Block (Barricade), or more Block per Dexterity is linked to every Attack/Block card though none reads it.
    Rule: L14, L18. Games: Slay the Spire. Files: s2 c3, s2 c4, s2 c7.
    - Melter -> Hyperbeam: makes stronger: removes their Block: its damage gets through
    - Barricade -> Defend (Ironclad): makes stronger: keeps the Block it gives
    - Kunai -> Reinforced Body: makes stronger: makes the Block it gives bigger

27. Wrong thinking: any stat change counts as Gwen's "gains Power from Hallowed" trigger or Bard's "increased total stats" (Frostbite, Gloom, Tybaulk +1|+0, self-buff keywords); Gwen is also read as giving/using any stat change.
    Rule: L15, L14, L4. Games: Runeterra. Files: r3 c2, r4 c5, r5 c7, r6 c3.
    - Rimetusk Shaman -> Gwen (level 2): waits: changes units' stats (for the ability it gives)
    - Bayou Brunch -> Gwen: changes your units' stats
    - Tybaulk -> Gwen: triggers: changes your units' stats; also makes stronger: gives it more power

28. Wrong thinking: any stat change is linked to Out Of The Way, which only makes "this round" buffs permanent.
    Rule: none stated. Games: Runeterra. Files: r3 c3.
    - Starhound Pack -> Out Of The Way: type: changes your units' stats: Out Of The Way lets them do more
    - Grotesque Gift -> Out Of The Way: type: changes your units' stats: Out Of The Way lets them do more

29. Wrong thinking: an enemy debuff (Gloom) is read as "changes your units' stats" for champion level-ups.
    Rule: L9. Games: Runeterra. Files: r3 c4.
    - Grotesque Gift -> Aurelion Sol: levels: changes your units' stats (levels it up)
    - Grotesque Gift -> Bard: levels: changes your units' stats (levels it up)
    - Grotesque Gift -> Galio: levels: changes your units' stats (levels it up)

30. Wrong thinking: "grant keywords" / any keyword or status is matched to every card that counts, waits for or levels from one specific keyword/status (Trap, Plant, Curse, Stunned/Recalled, Block, Daybreak).
    Rule: L14, L16, L4. Games: Runeterra, Slay the Spire. Files: r2 c2, r2 c7 (Legion General part), r3 c7, r5 c6, s1 c4.
    - Papercraft Dragon (created) -> Teemo: makes units get Plant (levels it up)
    - Acceleration Gate -> Caitlyn: makes units get Trap (levels it up)
    - Clockwork Souvenir -> Wave of the Hand: waits: makes units get a keyword or status (for the ability it gives)

## D. Draw, play, copy, make

31. Wrong thinking: draw/tutor/put by kind (or a single random draw) is linked to every card of that kind / every "when you draw X" card.
    Rule: L1b (also L14, L15, L21). Games: Faeria, Runeterra, Slay the Spire. Files: f1 c8, r1 c5, r7 c6, s1 c11, s1 c13.
    - Iona's Smile -> Astral Weapon: puts: draws it from the deck
    - Realm Warp -> Aatrox: draws it and keeps it
    - Gremlin Horn -> Fire Breathing: waits: makes you draw cards

32. Wrong thinking: "create X if you don't have one / if you don't already have one" is read as "wants an empty hand".
    Rule: L5, L21, L1. Games: Runeterra. Files: r1 c6, r2 c7 (Catalogue part), r5 c1.
    - Realm Warp -> Aatrox: waits: empties your hand
    - Spinning Axe -> Gnar: empties your hand
    - Catalogue of Regrets -> Vayne / Veigar / Senna / Aphelios: empties your hand

33. Wrong thinking: any card that makes cards, plays the top card, or is played feeds a card that reacts to "any card played" / "play N cards" / Orange Pellets (every type).
    Rule: L1 (also L19, L1b). Games: Runeterra, Slay the Spire. Files: r5 c3, r5 c4, r2 c8, s1 c1, s1 c9, s1 c10.
    - Annie -> Breakneck Husk: makes more cards to play
    - Beta -> After Image+: waits: makes more cards to play
    - Havoc -> Corruption: waits: is played

34. Wrong thinking: a copy or card put into the deck/hand/play (Nautilus, Dual Wield, Pack Attack, Radiant Standard, Mirror Meld) is a line, though it is by kind or the receiver has no summon/death effect (an Opening Gambit also does not go off from the deck).
    Rule: L19 (also L17). Games: Runeterra, Slay the Spire, Duelyst. Files: r3 c9, r3 c10, r5 c11, s1 c7, u1 c6.
    - Nautilus -> Bull Elnuk: puts: copies it
    - Dual Wield -> Body Slam: puts: copies it
    - Radiant Standard -> Futureshaker: puts: puts it into play from the deck

35. Wrong thinking: a summoner/"puts your units into play" feeds a level-up or summon payoff that asks for a specific kind (Tech, multi-region, Mech, Vespyr, 1 or less Attack, action bar) or a stat filter, though the summoned card is not that kind.
    Rule: L20 (also L1b, L17). Games: Faeria, Runeterra, Duelyst. Files: f1 c10, r2 c6, u1 c5, u2 c10, u3 c8.
    - Mother of All Yaks -> Hate Seed: cheaper: puts your units into play
    - Island Navigator -> Heimerdinger: puts your units into play (levels it up)
    - Firestarter -> Hideatsu the Ebon Ox: waits: puts your units into play

36. Wrong thinking: "creates cards" / "fills your hand" is linked where the receiving text does not count made cards, wants a pick, wants another kind, or the cards go to the enemy.
    Rule: L1, L9, L19, L20, L10, L14, L21. Games: Faeria, Runeterra, Slay the Spire, Duelyst. Files: f1 c9, r5 c2, r7 c5, s1 c12, u1 c11 (Alcuin/Blue Conjurer part).
    - Amai Mapdealer -> Gemshell Tortoise: type: creates cards
    - Ashe -> Cunning Kitten: creates cards
    - Alcuin Fugitive -> Hideatsu the Ebon Ox: type: creates cards: more different cards to play

37. Wrong thinking: waiting for a card added to the deck (Eggs, Ceramic Fish, Darkstone Periapt, Omamori, Master Reality) is fed by cards made in combat or potions, and by the wrong kind.
    Rule: L13, L20. Games: Slay the Spire. Files: s1 c2.
    - Jack of All Trades -> Molten Egg: waits: creates cards
    - Hello World -> Omamori: waits: creates cards
    - Attack Potion -> Darkstone Periapt: waits: creates cards

38. Wrong thinking: a condition in the text (spell filter, "in combat", cost 0, "3 or less Attack", targets a friendly minion) is not checked.
    Rule: L21 (f1: L11; u3: "read like a player"). Games: Duelyst, Runeterra, Faeria. Files: u1 c11, u3 c6, r4 c7, f1 c5 (Blood Obelisk part).
    - Accumulonimbus -> The Scientist: waits: is a spell whose playing sets off its effect
    - Plasma Storm -> Dagona: triggers: kills it for its death effect
    - Nagakabouros' Tantrum -> Lux (level 2): waits: is a spell whose playing sets off its effect

## E. Kills, deaths, sides, drawbacks

39. Wrong thinking: opponent-side triggers (Sentinel cards, Night Watcher, "your opponent casts") are fed by my own spells and summons.
    Rule: L9 (also L5, L21). Games: Duelyst. Files: u1 c4, u2 c1, u2 c2.
    - Lurking Fear -> Xerroloth: waits: is a spell whose playing sets off its effect
    - Firestarter -> Night Watcher: waits: puts units into play
    - Gloomchaser -> Bound Tormentor: waits: puts units into play

40. Wrong thinking: kills/damage on one side feed a need on the other (enemy-only kills feed my Dying Wish; friendly-only kills feed "enemy dies"; Annie's enemy damage feeds my-unit death effects).
    Rule: L9, L11. Games: Duelyst, Runeterra. Files: u1 c14, u2 c3, u3 c7, r5 c18.
    - Deathmark -> Ironclad: waits: kills it for its death effect
    - Darkfire Sacrifice -> Grasp of Agony: waits: makes units die (for the ability it gives)
    - Annie -> Blades of the Fallen: makes units die (for the ability it gives)

41. Wrong thinking: damage to the General is read as damage to the minion.
    Rule: L7. Games: Duelyst. Files: u1 c2.
    - Flameblood Warlock -> Lantern Fox: waits: damages it for its effect
    - Elucidator -> Juggernaut: waits: damages it for its effect
    - Dark Nemesis -> Deathstrike Seal: waits: damages units or players (for the ability it gives)

42. Wrong thinking: a plain hit on one target, removal, or ordinary attack damage feeds my own Last Words/death effect or "whenever an enemy dies".
    Rule: L11 (also L9, L21, L2). Games: Faeria, Slay the Spire, Duelyst. Files: f2 c11, s1 c6, u3 c5.
    - Flame Burst -> Imperial Guard: waits: kills it for its death effect
    - Anger, Bash, Bite, Claw, Clothesline, Dash, Dagger Throw -> Gremlin Horn: waits: makes enemy units die
    - Daemonic Lure -> Grasp of Agony: triggers: makes units die (for the ability it gives)

43. Wrong thinking: text that kills nothing, or kills something else (a well, a deck, a landmark; Snecko Skull; Earthfire Shaker counting only its own Gift), is read as a kill.
    Rule: L1, L3, L11, L9, L10. Games: Faeria, Slay the Spire, Runeterra. Files: f1 c5, f2 c10, s2 c5, r7 c9.
    - Solem -> Annoying Gnat: waits: kills it for its death effect
    - Void Guardian -> Village Elder: waits: kills it for its death effect
    - Snecko Skull -> Corpse Explosion: triggers: makes enemy units die

44. Wrong thinking: a drawback (Last Words that helps the opponent, a status card that only hurts, a Play that curses itself, damage that helps the enemy) is linked as a need.
    Rule: L5 (f1 Hunted Outlaw; u2 also L9). Games: Faeria, Slay the Spire, Runeterra, Duelyst. Files: f1 c5, f2 c12, s2 c2, r3 c13, u2 c4.
    - Doom Scythe -> Hunted Outlaw: waits: kills it for its death effect
    - Overclock -> Burn: puts it into play: creates
    - Riftwalker -> Haruspex: waits: damages it for its effect

45. Wrong thinking: text that does not exist is read as self-death, a keyword giver, or a given ability.
    Rule: L1. Games: Faeria. Files: f1 c11, f4 c5.
    - Baeru, the First Wave -> Bone Collector: waits: dies by its own effect
    - Seed of Paradise -> Imperial Engineer: type: makes your units get Production
    - Grappling Hook -> Imperial Engineer: enables: makes your units get Production

46. Wrong thinking: what every turn or every unit does (own summon, self-summon, turn end) is read as a trigger.
    Rule: L1. Games: Faeria, Runeterra. Files: f1 c14, r7 c8.
    - Doomsday -> Compass of Gagana: waits: makes this happen: your turn ends
    - Jarvan IV -> Fleetfeather Tracker: triggers: puts your units into play

## F. Wording, direction, duplicates

47. Wrong thinking: the same reason is said two or three times for one pair (type + waits, triggers + helps it level up, movement rules joined).
    Rule: L10 (also L18). Games: all four. Files: f2 c5, f4 c8, r4 c2, r5 c13, r6 c6, s1 c8, s2 c6, u1 c17, u2 c14, u3 c10 (last part).
    - Celestial Tower -> Imperial Drakerider: triggers: moves it for its effect; also moves into place: moves my units or land forward: they reach enemy ground; also moves into place: moves it where it must be
    - Thunderclap -> Champion Belt: type: makes enemy units get Vulnerable / waits: makes enemy units get Vulnerable
    - Chassis of MECHAZ0R -> Echo Deliverant: waits: is a Mech whose summoning sets off its effect, AND waits: puts your units into play

48. Wrong thinking: the reason words do not match what the card does (wrong kind: triggers vs makes cheaper, summon vs plant, heal vs repair, stat word vs movement, replace vs shuffle, landmark vs units).
    Rule: L10 (also L8, L12, L13). Games: all four. Files: f3 c5, f4 c7, r5 c16, r5 c23, r6 c7, r7 c9, u1 c12 (Replace wording), u1 c18, u3 c10, s1 c5 (words "units"), u2 c14.
    - Mirror Phantasm -> Windstorm Archer: clears the way: clears its line of fire
    - Topaz Yak -> Mother of All Yaks: triggers: is a yak it counts when dies
    - Manasoul Student -> Annie: helps it level up: is played (levels it up)

49. Wrong thinking: "puts it into play" is said for a card only put into hand, draw pile or discard pile.
    Rule: L10. Games: Slay the Spire. Files: s2 c1.
    - Blade Dance -> Shiv: puts it into play: creates
    - Scrape -> Claw: puts it into play: draws it and keeps it
    - All for One -> Overclock: puts it into play: brings it back to your hand

50. Wrong thinking: the link direction is wrong (helper said to need what it helps; A named by B instead of B by A).
    Rule: L6, L14 (r5: none stated). Games: Faeria, Runeterra. Files: f3 c4, r5 c14, f1 c4 (Defender), u2 c12 (Scion's Third Wish -> Duskweaver note).
    - Ninja Toad -> Triton Trainer: enables: has Jump
    - Battle Toads -> Triton Trainer: enables: makes your units get Jump
    - Warlord's Palace -> Akshan: is the A it names

51. Wrong thinking: reasons that do not match B's text at all (Catalogue discard, Lee Sin -> Legion General, Ambush "hit the enemy player", Arena Bookie -> Samira).
    Rule: L1, L7, L10. Games: Runeterra. Files: r2 c7.
    - Catalogue of Regrets -> Ancient Warmonger: makes you discard cards
    - Lee Sin -> Legion General: has Barrier
    - Arena Bookie -> Samira (level 2): empties your hand

## G. Single-game cards and misreadings

52. Out-of-combat healing (rest sites, shops, pickups) feeds Magic Flower, and the player is called "units".
    Rule: L13, L12. Games: Slay the Spire. Files: s1 c5.
    - Eternal Feather -> Magic Flower: waits: heals your units
    - Meal Ticket -> Magic Flower: waits: heals your units
    - Lee's Waffle -> Magic Flower: waits: heals your units

53. A card's own Exhaust keyword feeds Sentinel ("If THIS card is Exhausted").
    Rule: L7. Games: Slay the Spire. Files: s1 c3.
    - Slimed -> Sentinel: waits: exhausts cards
    - Reaper -> Sentinel: waits: exhausts cards
    - Exhume -> Sentinel: waits: exhausts cards

54. Kalista (level 2) read wrongly (bond as need for damage, revive linked to champions, revived attacker as another attack).
    Rule: L7, L4, L20. Games: Runeterra. Files: r1 c9.
    - Kalista (level 2) <- Absorb Soul: damages units or players (for the ability it gives)
    - Kalista (level 2) -> Ahri (level 2): makes it attack for its effect
    - Kalista (level 2) -> Quinn: another attack

55. Moving an ally to the deck (Bone Skewer top, Sugary Snare bottom) is read as moving toward the Nexus.
    Rule: L4. Games: Runeterra. Files: r1 c10.
    - Bone Skewer -> Darius: levels: moves it within reach of the enemy player (levels it up)
    - Sugary Snare -> Snowy Razorclaw: moves it within reach of the enemy player
    - Bone Skewer -> Dashing Dandy: moves it within reach of the enemy player

56. Wrong doer: Challenger choosing a blocker is read as making enemy units block for Annie/Captive Greyback/Ziggs/Taliyah blocker-hit cards.
    Rule: L7. Games: Runeterra. Files: r3 c5, r2 c7 (Lee Sin -> Threaded Volley).
    - Laurent Protege -> Obeyed Order: type: makes enemy units block: Obeyed Order damages them
    - Trifarian Gloryseeker -> Threaded Volley: type: makes enemy units block: Threaded Volley damages them
    - Lee Sin -> Threaded Volley: makes enemy units block: B damages them

57. Challenger is read as targeting (for Ezreal).
    Rule: L15. Games: Runeterra. Files: r3 c6 (r5 unsure Braum -> Ezreal).
    - Laurent Protege -> Ezreal: levels: targets enemy cards (levels it up)
    - Fiora (level 2) -> Ezreal: levels: targets enemy cards (levels it up)
    - Trifarian Gloryseeker -> Ezreal: levels: targets enemy cards (levels it up)

58. A faction/tribe/cost/stat filter is treated as narrower than a deck ("another Noxus ally", 1 cost ally, higher Attack than Life).
    Rule: L14, L17, L21. Games: Runeterra, Faeria. Files: r3 c8, r5 c12, f4 c6.
    - Reckless Trifarian -> Trifarian Hopeful: type: is a unit it asks for
    - Kinkou Wayfinder -> Annie: puts it into play from the deck
    - Demon Wrangler -> Firebringer: triggers: puts your units into play

59. Grandmaster at Arms (an Origin, a deckbuilding rule) is counted as a played spell and Jax "casts" it.
    Rule: none stated. Games: Runeterra. Files: r3 c11.
    - Grandmaster at Arms -> Annie: levels: is a spell it needs played for its count (levels it up)
    - Grandmaster at Arms -> The Prefect: waits: is a spell whose playing sets off its effect
    - Jax -> Grandmaster at Arms: puts: casts its skill

60. A unit summoned for the opponent is linked as mine.
    Rule: L9. Games: Runeterra. Files: r3 c12.
    - Stalking Wolf -> Snow Hare: puts: summons

61. Flashbomb Trap (planted in the enemy deck) is read as hitting my side.
    Rule: L9, L7. Games: Runeterra. Files: r5 c5 (r2 unsure).
    - Caitlyn -> Kalista: through Flashbomb Trap: makes your units die (levels it up)
    - Caitlyn -> Vladimir: through Flashbomb Trap: damages your units without killing them (levels it up)
    - Caitlyn -> Braum: through Flashbomb Trap: damages it without killing it, for its effect (levels it up)

62. "Mecha Yordle" is read as "Yordle" (Gnar is not a Mecha).
    Rule: none stated. Games: Runeterra. Files: r5 c10.
    - Gnar -> Skrappy's Partsapalooza: is a Mecha whose summoning sets off its effect
    - Gnar -> Rumble (level 2): is a Yordle it asks for
    - Rumble (level 2) -> Gnar: makes it cheaper

63. Akshan only advances Warlord's Palace but is linked to every Countdown landmark.
    Rule: L1. Games: Runeterra. Files: r5 c15.
    - Akshan -> Dragon Roost: finishes countdowns
    - Akshan -> Buried Armory: finishes countdowns

64. Buried Sun Disc is linked as levelling or waking champions (it only counts Ascended level-ups).
    Rule: none stated. Games: Runeterra. Files: r5 c17.
    - Buried Sun Disc -> Akshan: makes champions level up (it levels up from what it then does)
    - Buried Sun Disc -> Annie: makes champions level up

65. Twisted Catalyzer (boosts only "your Darkness") is linked to Annie and Gwen.
    Rule: none stated. Games: Runeterra. Files: r5 c19.
    - Annie -> Twisted Catalyzer: damages units or players (for the ability it gives)
    - Gwen -> Twisted Catalyzer: damages units or players (for the ability it gives)

66. Strike spells are said to set off an Attack effect (a strike is not an attack).
    Rule: none stated. Games: Runeterra. Files: r5 c21.
    - Bone Skewer -> Gwen: makes it attack or strike again: its own effect goes off

67. Twilit Protector's Nightfall buff to Nightfall allies is linked to Aphelios (Nightfall on Nightfall gives no line; Aphelios does not read Power).
    Rule: L15. Games: Runeterra. Files: r5 c22.
    - Twilit Protector -> Aphelios: gives it more power

68. Level-up lines filed under "type" instead of "levels".
    Rule: none stated. Games: Runeterra. Files: r5 c23.
    - Gifts From Beyond -> Aphelios: makes a Moon Weapon it asks for
    - Spiderling -> Elise: is a Spider it asks for

69. Ashe's "changes enemy units' stats" list includes Husks, which grant stats to my own ally.
    Rule: none stated. Games: Runeterra. Files: r5 c24.
    - Breakneck Husk -> Ashe: changes enemy units' stats (levels it up)
    - Ashe -> Gwen (level 2): changes units' stats (for the ability it gives)

70. Station Archivist (discards nothing) is said to make you discard cards for cards that need themselves discarded.
    Rule: L1, L7. Games: Runeterra. Files: r7 c7.
    - Station Archivist -> Fallen Rider: triggers: makes you discard cards
    - Station Archivist -> Flame Chompers!: triggers: makes you discard cards

71. Revival cards linked against their own limits (Zurael only last-turn enemy kills, Blood Echoes only own kills, Obelysk/Kujata kill nothing).
    Rule: L20, L21. Games: Duelyst. Files: u2 c9.
    - Darkfire Sacrifice -> Zurael, the Lifegiver: type: makes your units die: Zurael, the Lifegiver brings them back
    - Abhorrent Unbirth -> Blood Echoes: type: makes your units die: Blood Echoes brings them back
    - Simulacra Obelysk -> Keeper of the Vale: type: makes your units die

72. Internal follow-ups, placeholders and AI helpers are treated as cards a player owns/plays.
    Rule: L9. Games: Duelyst. Files: u2 c13.
    - Teleport (follow-up, FollowupTeleportMyGeneralBehindEnemy) -> Chakri Avatar: waits: is a spell whose playing sets off its effect
    - Spell Damge -> Soul Grimwar: waits: makes units die (for the ability it gives)
    - Cascading Rebirth (follow-up) -> Sellsoul: waits: kills it for its death effect

73. "Another friendly minion" is read as the card itself (Oropsisaur).
    Rule: L7. Games: Duelyst. Files: u1 c10.
    - Owlbeast Sage -> Oropsisaur: waits: more health or protection: survives damage
    - Healing Mystic -> Oropsisaur: waits: more health or protection: survives damage
    - Mirkblood Devourer -> Oropsisaur: waits: more health or protection: survives damage

74. Any card that adds cards to hand links to Theobule as "fills your hand" (it only replaces; replace is worded "shuffles cards into the deck").
    Rule: L21 (and L10 for wording). Games: Duelyst. Files: u1 c12 (u3 c10 wording, u3 unsure Replicant).
    - Aegis Barrier -> Theobule: waits: fills your hand
    - Spelljammer -> Theobule: waits: fills your hand
    - Aethermaster -> White Widow: triggers: shuffles cards into the deck

75. Repairing artifacts is read as healing.
    Rule: L10. Games: Duelyst. Files: u1 c16.
    - Dawn's Eye -> Lightchaser: waits: heals units
    - Dawn's Eye -> Gold Vitriol: heals: can heal it
    - Dawn's Eye -> Excelsious: type: heals units

76. Stats on a move spell are linked as extra help where only the move matters.
    Rule: L18. Games: Duelyst. Files: u3 c11.
    - Mist Dragon Seal -> Bonereaper: ...; also makes stronger: can give it more power and health

## H. Missed lines (a line that should exist)

77. Missing: Treasure Map makers (Amai Mapdealer, Aryana, Compass of Gagana, Gagana Treasure Seeker, Message in a Bottle) to cards that count Treasure Maps (Ancient Gargoyle, Triton Stargazer, Fugoro).
    Rule: L17 (f4). Games: Faeria. Files: f1 c15, f3 c6, f4 c9, f1 unsure.
    - (no line exists) Amai Mapdealer -> Ancient Gargoyle: puts Treasure Maps in your deck: it counts them
    - (no line exists) Amai Mapdealer -> Triton Stargazer
    - (no line exists) Message in a Bottle -> Triton Stargazer

78. Missing: Gift of Steel -> Grim Guard (+3/+3 to a Taunt Combat creature); lines exist in other decks.
    Rule: L18. Games: Faeria. Files: f3 c6.
    - (no line exists) Gift of Steel -> Grim Guard

79. Missing: Gagana, Rainbow Birdship / Magnus / Aurora's Dream -> Illusion of Grandeur (cost 0/1 creature), and "triggers" wording.
    Rule: none stated. Games: Faeria. Files: f3 c6.
    - (no line exists) Gagana, Rainbow Birdship -> Illusion of Grandeur

80. Missing: cards of a kind (events, Flying creatures) have no line to cards waiting for that kind to be drawn.
    Rule: L1b (case nfa09). Games: Faeria. Files: f4 c1.
    - (no line exists) Flame Burst -> Flamesilk Faerie
    - (no line exists) Soul Drain -> Sunsilk Faerie
    - (no line exists) Airbot -> Drakkar Skycaptain

81. Missing: cards that make a card "by description" (Crystal Spice discovers 7+ cost cards; Yak Attack summons Angry Yaks) have no line to the card that counts/asks for it.
    Rule: L17. Games: Faeria. Files: f4 c9.
    - (no line exists) Crystal Spice -> Gabrian Archon
    - (no line exists) Yak Attack -> Topaz Yak

82. Missing: a need to stand on enemy land (Triton Adventurer "if this is on an enemy land") is not seen.
    Rule: none stated (cases nfa21, nfa27). Games: Faeria. Files: f4 c10.
    - (no line exists) Oradrim Fanatic -> Triton Adventurer

83. Missing: champion spells ("X's Spell ... Create an X in your deck") get no lines (made champion and own effects).
    Rule: none stated. Games: Runeterra. Files: r3 c15.
    - (no line exists) Vex's Glare -> Vex
    - (no line exists) Xerath's Rite of the Arcane -> Xerath
    - (no line exists) Jax's Counter Strike -> Jax

84. Missing: a transform into a named card is not seen as "puts it into play".
    Rule: none stated. Games: Runeterra. Files: r3 c16.
    - (no line exists) Pyke -> Death From Below
    - (no line exists) The Darkin Halberd -> Taarosh
    - (no line exists) Avenging Vastaya's Ambush -> Avenging Vastaya

85. Missing: Ephemeral revives (Taarosh) are not seen.
    Rule: L3 (example shape). Games: Runeterra. Files: r3 c17.
    - (no line exists) Taarosh -> Moonlit Glenkeeper
    - (no line exists) Taarosh -> Fallen Sands General

86. Missing: World Runes are not a kind the database knows.
    Rule: none stated. Games: Runeterra. Files: r3 c18.
    - (no line exists) Shard of Hope -> Ryze
    - (no line exists) Delve Into The Past -> each Shard

87. Missing: Overwhelm given to a card that needs to hit the Nexus.
    Rule: L20. Games: Runeterra. Files: r3 c19.
    - (no line exists) Heavy Blade Fragment -> Chempunk Pickpocket
    - (no line exists) Wildclaw Stance -> Pakaa Cub

88. Missing: Puffcap planters -> Teemo / Teemo (level 2).
    Rule: none stated. Games: Runeterra. Files: r6 M1.
    - (no line exists) Puffcap Peddler -> Teemo
    - (no line exists) Poison Dart -> Teemo (level 2)

89. Missing: traps/boons and their planters -> Mister Thrift.
    Rule: none stated. Games: Runeterra. Files: r6 M2.
    - (no line exists) Poison Puffcap -> Mister Thrift
    - (no line exists) Volatile Bloom -> Mister Thrift

90. Missing: other Lurkers' Lurk -> Rek'Sai (it reads its own power).
    Rule: L15 (exception). Games: Runeterra. Files: r6 M3.
    - (no line exists) Xerxa'Reth, The Undertitan -> Rek'Sai (Lurk +1|+0)

91. Missing: Bone Skewer -> Lurk cards (Rek'Sai, Pyke, Xerxa'Reth).
    Rule: none stated. Games: Runeterra. Files: r6 M4.
    - (no line exists) Bone Skewer -> Rek'Sai
    - (no line exists) Bone Skewer -> Pyke

92. Missing: Pen Nib counts Attacks played but gets no count lines (like Nunchaku).
    Rule: none stated. Games: Slay the Spire. Files: s2 c8.
    - (no line exists) Shiv -> Pen Nib
    - (no line exists) Claw -> Pen Nib
    - (no line exists) Beam Cell -> Pen Nib

93. Missing: Stun cards -> Cryoblade ("double damage to Stunned enemies"); Omniseer -> Verdant Fulmination.
    Rule: none stated. Games: Duelyst. Files: u1 (Missed lines).
    - (no line exists) Icy -> Cryoblade
    - (no line exists) Permafrost -> Cryoblade
    - (no line exists) Omniseer -> Verdant Fulmination

94. Missing: Fractal Replication -> Dying Wish cards (Unseven, Grimes, Dagona).
    Rule: L19. Games: Duelyst. Files: u3 c12.
    - (no line exists) Fractal Replication -> Unseven
    - (no line exists) Fractal Replication -> Dagona

95. Missing: return to the action bar of Opening Gambit cards (Hailstone Prison -> Hearth-Sister; Sandswirl Reader -> Azure Herald / Healing Mystic).
    Rule: L14. Games: Duelyst. Files: u3 c12.
    - (no line exists) Hailstone Prison -> Hearth-Sister
    - (no line exists) Sandswirl Reader -> Azure Herald
    - (no line exists) Sandswirl Reader -> Healing Mystic

## Unsure items raised by more than one file
- Removal -> Ranged Attack "clears its line of fire": is a ranged attack blocked by units in between? (f1, f3)
- Land colour (L22) lines to all cards of a colour, and Seed/Wild Growth/Baeru -> coloured cards: count huge, colours unchecked. (f2, f3)
- Plain single-target removal/damage on my own Last Words / sacrifice target (Soul Drain -> Deathwish Ghoul, Ravenous Flock -> Ceaseless Sentry, Mystic Shot -> Blade Squire, Sump Fumes -> Last Breath allies): L11 or a real sacrifice? (f3, r4, r6, r7)
- Plain draw cards -> cards that wait for one kind of draw (Sunsilk Faerie, Flight of the Mantas, Ancient Herald, Gabrian Commander, Janna, Cloak Clasp): L1b generic? (f3, f4, r5, s1)
- Cost-match filters ("play a 2 cost card", Insightful Investigator, Tri-beam Improbulator) and "pays for it" with a low EXPENSIVE threshold (energy to 2+ cost): generic by L21? (r3, r5, s1, s2, r1)
- Mecha vs Yordle (Rumble (level 2), Arena Kingpin, Wizened Wizard, Gnar -> Heimerdinger): tribe not shown in the printed text. (r2, r3, r5)
- Random help (Dragon Dedicant / Smokescaled Host reduce a random card; Snecko Oil, Madness, Mummified Hand): is random cost change aimed help? (r3, s1)
- Heal (not more health) to Provoke/Taunt units: does healing count under L18? (u1, u2, u3)
- Whether spells are a minority for L1b (308 of 1036 cards in Duelyst), so "is a spell whose playing..." lines stay. (u1, u3)
- Kills/damage of any friendly or enemy minion feeding Deathwatch/revivers (Death Knell, Corpse Combustion, Bonereaper -> Deathwatch cards): generic by L21? (u1, u2)
- Does Scout / Challenger / Tough count as a second attack, targeting, or a damage reduction (Samira -> Ardent Tracker, King Jarvan III -> Gwen, Braum -> Ezreal, The Scargrounds -> Braum)? (r2, r3, r5, r7)
- "Is played" from Prank and Stance Swap: do they play another card? (r1, r2; r7 Prank -> Curious Shellfolk)
- A tribe/kind narrow enough for aimed help (Arcanyst via Kindling/Owlbeast Sage, Infiltrate via Wind Sister Maia, Golem, 5+ Life creatures)? L14. (f1, u1, u2, u3)
- Movement/keyword given to Combat cards depends on Faeria's Combat trigger. (f2, f3)
- Copies of Flashbomb Trap/trap planting: whose side the trap lands on. (r2, r5)
- Cards that fill hand "Chemtech Drake <- fills your hand" / hand-size readers (Cloak Clasp, Spirit Shield): too generic under L21. (r1, s1)

## Must-stay lines (exact, up to 15)
- Clockwork Yak -> Topaz Yak: type: is a yak it asks for
- Syland Horsemaster -> Lost Explorer: waits: moves it for its effect
- Celestial Tower -> Oradrim Monk: moves: moves it within reach of the enemy player
- Fragmenter -> Hate Seed: cheaper: puts your units into play
- Architect -> Doomgate, Door to Oblivion: stronger: can give it more health
- Illusion of Grandeur -> Gabrian Commander: triggers: is a card whose drawing sets off its effect
- Chemtech Drake -> Jagged Butcher: damages the enemy player
- Fae Guide -> Fizz (level 2): can give it Elusive
- Mischievous Marai -> Kennen: puts your units into play (levels it up)
- Laurent Protege -> Baccai Witherclaw: waits: makes this happen: challenges
- Cithria the Bold -> Bitsy Lizard: type: helps it hit the enemy player
- Corruption -> Feel No Pain: triggers: exhausts cards
- Shuriken -> Heavy Blade: type: gives you Strength
- Unseven -> Dagona: puts it into play: puts it into play from the hand
- Bonereaper -> Deathstrike Seal: waits: damages units or players (for the ability it gives)

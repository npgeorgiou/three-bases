# Case tests: runeterra

Made by `cases/run.py runeterra`.
**174 of 193 cases pass.**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| m01 | rewards an ally dying (event) | 6 | 6 | 100% | 10 | yes |
| m02 | cares whether allies died (condition) | 13 | 13 | 100% | 22 | yes |
| m03 | triggers when you play a spell | 31 | 31 | 100% | 8 | yes |
| m04 | triggers when you summon an ally | 40 | 40 | 100% | 11 | yes |
| m05 | kills own units | 34 | 34 | 100% | 20 | yes |
| m06 | stuns | 68 | 65 | 96% | 10 | yes |
| m07 | frostbites (power to 0) | 21 | 21 | 100% | 2 | yes |
| m08 | recalls units | 58 | 54 | 93% | 58 | NO |
| m09 | draws cards | 178 | 175 | 98% | 22 | yes |
| m10 | creates cards | 413 | 412 | 100% | 146 | yes |
| m11 | damages the enemy Nexus | 89 | 87 | 98% | 232 | yes |
| m12 | heals | 62 | 60 | 97% | 71 | yes |
| m13 | discards | 37 | 36 | 97% | 105 | yes |
| m14 | obliterates | 43 | 43 | 100% | 22 | yes |
| m15 | levels up (champion level-up condition) | 107 | 106 | 99% | 4 | yes |
| m16 | grants lasting stats | 215 | 215 | 100% | 215 | yes |
| m17 | gives Barrier (damage prevention) | 29 | 29 | 100% | 2 | yes |
| m18 | Nexus Strike triggers | 32 | 32 | 100% | 1 | yes |
| m19 | Last Breath (dies) triggers | 47 | 46 | 98% | 17 | yes |
| m20 | Round Start triggers | 113 | 113 | 100% | 2 | yes |
| m21 | Round End triggers | 31 | 31 | 100% | 185 | yes |
| m22 | Attack triggers | 96 | 95 | 99% | 245 | yes |
| m23 | Overwhelm units deal excess damage | 104 | 104 | 100% | 34 | yes |
| m24 | Elusive units can't be blocked by most units | 76 | 76 | 100% | 253 | yes |
| m25 | Ephemeral units die at round end | 23 | 23 | 100% | 43 | yes |
| m26 | Plunder: needs damage to the enemy Nexus this round | 33 | 33 | 100% | 11 | yes |
| m27 | Countdown landmarks | 26 | 26 | 100% | 6 | yes |
| m28 | refills or gains mana | 29 | 26 | 90% | 36 | NO |
| m29 | Toss (obliterate own deck) | 13 | 13 | 100% | 4 | yes |
| m30 | Rally (attack token) | 25 | 25 | 100% | 18 | yes |
| m31 | Predict | 20 | 20 | 100% | 62 | yes |
| m32 | reduces costs | 125 | 123 | 98% | 54 | yes |
| m33 | copies cards or spells | 112 | 83 | 74% | 8 | NO |
| m34 | Behold (have a card) | 18 | 16 | 89% | 100 | NO |
| m35 | Daybreak / Nightfall | 42 | 42 | 100% | 1 | yes |
| m36 | can't block | 8 | 8 | 100% | 321 | yes |
| m37 | summons units | 273 | 248 | 91% | 133 | NO |
| m38 | revives | 23 | 22 | 96% | 7 | yes |
| m39 | silences | 11 | 11 | 100% | 37 | yes |
| m40 | shuffles cards into a deck | 21 | 7 | 33% | 11 | NO |

Missed cards (first 8 per failing case):

- m08 recalls units: Fae Bladetwirler, Tail-Cloak Matriarch, Yasuo, Yasuo (level 2)
- m28 refills or gains mana: Jack, Jack (level 2), Perfidious Promoter
- m33 copies cards or spells: Black Rose Spy, Bladebound Berserker, Curious Changelings, Entrapment, Entrapment (created), Entrapment (created), Eternal Dancers, Frozen Tomb
- m34 Behold (have a card): Targonian Tellstones, Zoe (level 2)
- m37 summons units: Adaptatron 3000, Altar to Unity, Ardent Tracker, Battlesmith, Chamber of Renewal, Deathgrasp Cultist, Dragon Prince Grinzo, Portal Scholar
- m40 shuffles cards into a deck: Careful Preparation, Coup de Grace, Nautilus, Nautilus' Riptide, Pick a Card, Rek'Sai, Riptide, Salty Spinner

## Combos (the enabler must set off the payoff)

| case | enabler | payoff | why | found as | pass |
|---|---|---|---|---|---|
| c01 | Hecarim | Shark Chariot | attacking with Ephemeral allies revives the Chariot | event: start_attack -> attacks (via Hecarim (level 2)) | yes |
| c02 | Thresh | Kalista | revive the strongest dead champion | condition: damage -> dies (via Thresh's The Box) | yes |
| c03 | Ezreal | Mystic Shot | Nexus Strike creates Mystic Shot | makes | yes |
| c04 | Elise | Frenzied Skitterer | spider tribal | event: summon -> summoned (via Elise's Crawling Sensation) | yes |
| c05 | Get Excited! | Jinx | discarding empties the hand for Jinx's level up | - | NO |
| c06 | Thresh (level 2) | Kalista (level 2) | summon a champion attacking; Kalista's attack payoff | event: start_attack -> attacks | yes |
| c07 | Vladimir | Legion Veteran | Vladimir damages allies; Veteran buffs allies that survive damage | event: damage -> survives_damage | yes |
| c08 | Puffcap Peddler | Teemo | Peddler plants Puffcaps; Teemo levels on Puffcaps planted | makes | yes |
| c09 | Atrocity | Lucian | Atrocity kills an ally; Lucian levels on allies dying | condition: kill -> dies | yes |
| c10 | Spectral Rider | Soul Shepherd | an Ephemeral ally is summoned; Shepherd buffs it | is: playing Spectral Rider is a summoned the payoff waits for | yes |
| c11 | Twin Disciplines | Lee Sin | playing a spell gives Lee Sin Challenger | is: playing Twin Disciplines is a played the payoff waits for | yes |
| c12 | Brittle Steel | Ashe | Frostbite sets enemy Power to 0; Ashe levels on that | condition: stat_set -> stat_changed | yes |
| c13 | Gnar | Pokey Stick | Strike creates Pokey Stick | makes | yes |
| c14 | Pokey Stick | Swain (level 2) | non-combat damage to the enemy Nexus stuns | event: damage -> nexus_damaged | yes |
| c15 | Coin | Jack | refilling mana heals Jack | event: mana_gain -> mana_refilled | yes |
| c16 | Culling Strike | Kindred | killing a unit lets Kindred mark | event: kill -> killed | yes |
| c17 | Draven | Spinning Axe | Draven creates Spinning Axes | makes | yes |
| c18 | Vladimir | Braum | damaging Braum makes him survive damage and summon a Poro | event: damage -> survives_damage | yes |
| c19 | Shadow Assassin | Twisted Fate | drawing cards levels Twisted Fate | condition: draw -> drawn | yes |
| c20 | Mystic Shot | Annie | playing Fast spells levels Annie | is: counted as a played spell | yes |
| c21 | Aurelion Sol | The Scourge | Invoked Celestial cards grow The Scourge | - | NO |
| c22 | Noxian Fervor | Legion Veteran | damaging an ally that survives | event: damage -> survives_damage | yes |
| c23 | Mystic Shot | Lux | playing spells levels Lux | event: damage -> damaged | yes |

## Region identity (signature, splash, archetype)

| case | region | kind | mechanic | need | found | pass |
|---|---|---|---|---|---|---|
| r01 | Shadow Isles | archetype (Claude) | rewards allies dying | 4 | 10 | yes |
| r02 | Shadow Isles | archetype (Claude) | Last Breath | 10 | 21 | yes |
| r03 | Shadow Isles | archetype (Claude) | Ephemeral | 8 | 33 | yes |
| r04 | Shadow Isles | archetype (Claude) | revive | 3 | 20 | yes |
| r05 | Noxus | archetype (Claude) | damages the enemy Nexus | 8 | 69 | yes |
| r06 | Noxus | archetype (Claude) | Overwhelm | 8 | 37 | yes |
| r07 | Noxus | archetype (Claude) | kills own units / self-damage | 2 | 2 | yes |
| r08 | Demacia | archetype (Claude) | grants lasting stats | 10 | 53 | yes |
| r09 | Demacia | archetype (Claude) | gives Barrier | 4 | 12 | yes |
| r10 | Freljord | archetype (Claude) | Frostbite | 8 | 22 | yes |
| r11 | Freljord | archetype (Claude) | heals | 5 | 25 | yes |
| r12 | Ionia | archetype (Claude) | Elusive | 8 | 42 | yes |
| r13 | Ionia | archetype (Claude) | recall | 8 | 51 | yes |
| r14 | Ionia | archetype (Claude) | stun | 5 | 13 | yes |
| r15 | Piltover & Zaun | archetype (Claude) | discard | 8 | 31 | yes |
| r16 | Piltover & Zaun | archetype (Claude) | creates cards | 20 | 70 | yes |
| r17 | Bilgewater | archetype (Claude) | Plunder | 10 | 20 | yes |
| r18 | Bilgewater | archetype (Claude) | Toss | 3 | 6 | yes |
| r19 | Bilgewater | archetype (Claude) | damages the enemy Nexus | 8 | 37 | yes |
| r20 | Targon | archetype (Claude) | Daybreak/Nightfall | 8 | 30 | yes |
| r21 | Targon | archetype (Claude) | Invoke / pick cards | 2 | 26 | yes |
| r22 | Shurima | archetype (Claude) | Countdown | 8 | 14 | yes |
| r23 | Bandle City | archetype (Claude) | creates cards | 15 | 72 | yes |
| r25 | Bandle City | signature (library tags) | trap_secret | 6 | 26 | yes |
| r26 | Bandle City | signature (library tags) | discard | 6 | 22 | yes |
| r27 | Bandle City | signature (library tags) | on_attack | 36 | 86 | yes |
| r28 | Bandle City | signature (library tags) | transform | 8 | 12 | yes |
| r29 | Bandle City | splash (library tags) | stat_gain | 2 | 68 | yes |
| r30 | Bandle City | splash (library tags) | on_spell | 2 | 6 | yes |
| r31 | Bandle City | splash (library tags) | resource_gain | 4 | 8 | yes |
| r32 | Bandle City | splash (library tags) | turn_start | 10 | 18 | yes |
| r33 | Bilgewater | signature (library tags) | resource_gain | 11 | 20 | yes |
| r34 | Bilgewater | splash (library tags) | on_spell | 3 | 10 | yes |
| r35 | Bilgewater | signature (library tags) | draw | 16 | 36 | yes |
| r36 | Bilgewater | signature (library tags) | turn_end | 11 | 29 | yes |
| r37 | Bilgewater | signature (library tags) | damage | 17 | 54 | yes |
| r38 | Bilgewater | splash (library tags) | heal | 4 | 11 | yes |
| r39 | Bilgewater | splash (library tags) | turn_start | 10 | 18 | yes |
| r40 | Bilgewater | splash (library tags) | summon | 19 | 43 | yes |
| r41 | Demacia | signature (library tags) | damage_reduction | 10 | 17 | yes |
| r42 | Demacia | signature (library tags) | stat_gain | 7 | 74 | yes |
| r43 | Demacia | signature (library tags) | multi_attack | 4 | 3 | NO |
| r44 | Demacia | splash (library tags) | merge_attach | 6 | 11 | yes |
| r45 | Demacia | splash (library tags) | on_ally_play | 6 | 43 | yes |
| r46 | Demacia | signature (library tags) | on_kill | 25 | 13 | NO |
| r47 | Demacia | splash (library tags) | banish | 2 | 9 | yes |
| r48 | Demacia | splash (library tags) | on_attack | 12 | 65 | yes |
| r49 | Freljord | signature (library tags) | on_damaged | 4 | 8 | yes |
| r50 | Freljord | signature (library tags) | excess_damage | 18 | 32 | yes |
| r51 | Freljord | signature (library tags) | damage_reduction | 4 | 9 | yes |
| r52 | Freljord | signature (library tags) | banish | 4 | 9 | yes |
| r53 | Freljord | splash (library tags) | heal | 4 | 25 | yes |
| r54 | Freljord | splash (library tags) | resource_gain | 5 | 10 | yes |
| r55 | Freljord | splash (library tags) | death_trigger | 6 | 8 | yes |
| r56 | Freljord | splash (library tags) | delayed | 3 | 5 | yes |
| r57 | Ionia | signature (library tags) | swap | 2 | 6 | yes |
| r58 | Ionia | signature (library tags) | return_to_hand | 26 | 51 | yes |
| r59 | Ionia | signature (library tags) | attack_now | 5 | 15 | yes |
| r60 | Ionia | signature (library tags) | disable | 14 | 13 | NO |
| r61 | Ionia | splash (library tags) | turn_end | 8 | 33 | yes |
| r62 | Ionia | splash (library tags) | cost_reduction | 6 | 23 | yes |
| r63 | Ionia | splash (library tags) | resource_gain | 4 | 8 | yes |
| r64 | Ionia | splash (library tags) | summon | 18 | 31 | yes |
| r65 | Noxus | signature (library tags) | excess_damage | 18 | 37 | yes |
| r66 | Noxus | signature (library tags) | disable | 10 | 21 | yes |
| r67 | Noxus | signature (library tags) | discard | 4 | 16 | yes |
| r68 | Noxus | signature (library tags) | damage | 18 | 68 | yes |
| r69 | Noxus | splash (library tags) | first_strike | 7 | 16 | yes |
| r70 | Noxus | splash (library tags) | cost_reduction | 5 | 12 | yes |
| r71 | Noxus | splash (library tags) | on_attack | 12 | 87 | yes |
| r72 | Noxus | splash (library tags) | on_play | 26 | 123 | yes |
| r73 | Piltover & Zaun | signature (library tags) | trap_secret | 6 | 17 | yes |
| r74 | Piltover & Zaun | signature (library tags) | discard | 6 | 31 | yes |
| r75 | Piltover & Zaun | signature (library tags) | cost_reduction | 12 | 39 | yes |
| r76 | Piltover & Zaun | signature (library tags) | on_spell | 4 | 28 | yes |
| r77 | Piltover & Zaun | splash (library tags) | resource_gain | 4 | 10 | yes |
| r78 | Piltover & Zaun | splash (library tags) | damage | 14 | 55 | yes |
| r79 | Piltover & Zaun | splash (library tags) | generate_cards | 20 | 54 | yes |
| r80 | Piltover & Zaun | splash (library tags) | transform | 4 | 9 | yes |
| r81 | Shadow Isles | signature (library tags) | revive | 11 | 20 | yes |
| r82 | Shadow Isles | signature (library tags) | destroy | 29 | 86 | yes |
| r83 | Shadow Isles | signature (library tags) | death_trigger | 14 | 50 | yes |
| r84 | Shadow Isles | signature (library tags) | summon | 34 | 43 | yes |
| r85 | Shadow Isles | splash (library tags) | attack_now | 2 | 11 | yes |
| r86 | Shadow Isles | splash (library tags) | on_kill | 26 | 11 | NO |
| r87 | Shadow Isles | splash (library tags) | cant_attack | 6 | 61 | yes |
| r88 | Shadow Isles | splash (library tags) | merge_attach | 4 | 6 | yes |
| r89 | Shurima | signature (library tags) | variety_payoff | 4 | 3 | NO |
| r90 | Shurima | signature (library tags) | delayed | 12 | 15 | yes |
| r91 | Shurima | signature (library tags) | counter_spell | 2 | 20 | yes |
| r92 | Shurima | signature (library tags) | selection | 6 | 27 | yes |
| r93 | Shurima | splash (library tags) | attack_now | 4 | 14 | yes |
| r94 | Shurima | splash (library tags) | excess_damage | 11 | 22 | yes |
| r95 | Shurima | splash (library tags) | copy | 8 | 13 | yes |
| r96 | Shurima | splash (library tags) | on_ally_play | 6 | 50 | yes |
| r97 | Targon | signature (library tags) | silence | 2 | 6 | yes |
| r98 | Targon | signature (library tags) | selection | 8 | 28 | yes |
| r99 | Targon | signature (library tags) | heal | 9 | 30 | yes |
| r100 | Targon | signature (library tags) | disable | 15 | 27 | yes |
| r101 | Targon | splash (library tags) | delayed | 4 | 7 | yes |
| r102 | Targon | splash (library tags) | cost_reduction | 6 | 22 | yes |
| r103 | Targon | splash (library tags) | on_kill | 28 | 13 | NO |
| r104 | Targon | splash (library tags) | discard | 2 | 8 | yes |
| r105 | Bandle City | archetype (library) | scaling | 34 | 14 | NO |
| r106 | Bandle City | archetype (library) | chaos | 28 | 63 | yes |
| r107 | Bandle City | archetype (library) | trickery | 6 | 26 | yes |
| r108 | Bandle City | archetype (library) | transformation | 16 | 28 | yes |
| r109 | Bilgewater | archetype (library) | chaos | 30 | 54 | yes |
| r110 | Bilgewater | archetype (library) | ramp | 17 | 37 | yes |
| r111 | Bilgewater | archetype (library) | graveyard | 4 | 28 | yes |
| r112 | Demacia | archetype (library) | scaling | 21 | 12 | NO |
| r113 | Demacia | archetype (library) | fortress | 22 | 30 | yes |
| r114 | Freljord | archetype (library) | sustain | 14 | 25 | yes |
| r115 | Freljord | archetype (library) | transformation | 11 | 16 | yes |
| r116 | Ionia | archetype (library) | positional | 8 | 0 | NO |
| r117 | Ionia | archetype (library) | control | 38 | 87 | yes |
| r118 | Ionia | archetype (library) | ramp | 14 | 32 | yes |
| r119 | Ionia | archetype (library) | card_advantage | 30 | 31 | yes |
| r120 | Piltover & Zaun | archetype (library) | chaos | 24 | 58 | yes |
| r121 | Piltover & Zaun | archetype (library) | trickery | 6 | 17 | yes |
| r122 | Piltover & Zaun | archetype (library) | ramp | 18 | 47 | yes |
| r123 | Piltover & Zaun | archetype (library) | spellslinger | 14 | 44 | yes |
| r124 | Shadow Isles | archetype (library) | sacrifice | 47 | 50 | yes |
| r125 | Shadow Isles | archetype (library) | graveyard | 14 | 21 | yes |
| r126 | Shadow Isles | archetype (library) | sustain | 17 | 34 | yes |
| r127 | Shadow Isles | archetype (library) | swarm | 36 | 65 | yes |
| r128 | Shurima | archetype (library) | trickery | 5 | 0 | NO |
| r129 | Shurima | archetype (library) | swarm | 30 | 85 | yes |
| r130 | Targon | archetype (library) | spellslinger | 18 | 7 | NO |
| r131 | Targon | archetype (library) | card_advantage | 15 | 43 | yes |

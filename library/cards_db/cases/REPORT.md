# Case tests: runeterra

Made by `cases/run.py runeterra`.
**248 of 248 cases pass.**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| m01 | rewards an ally dying (event) | 6 | 6 | 100% | 10 | yes |
| m02 | cares whether allies died (condition) | 13 | 13 | 100% | 20 | yes |
| m03 | triggers when you play a spell | 32 | 32 | 100% | 9 | yes |
| m04 | triggers when you summon an ally | 41 | 41 | 100% | 12 | yes |
| m05 | kills own units | 35 | 35 | 100% | 20 | yes |
| m06 | stuns | 72 | 69 | 96% | 11 | yes |
| m07 | frostbites (power to 0) | 22 | 22 | 100% | 1 | yes |
| m08 | recalls units or cares about recalling | 60 | 60 | 100% | 77 | yes |
| m09 | draws cards | 190 | 187 | 98% | 24 | yes |
| m10 | creates cards | 435 | 434 | 100% | 187 | yes |
| m11 | damages the enemy Nexus | 94 | 92 | 98% | 267 | yes |
| m12 | heals | 67 | 65 | 97% | 74 | yes |
| m13 | discards | 40 | 39 | 98% | 108 | yes |
| m14 | obliterates | 43 | 43 | 100% | 21 | yes |
| m15 | levels up (champion level-up condition) | 119 | 118 | 99% | 4 | yes |
| m16 | grants lasting stats | 233 | 233 | 100% | 231 | yes |
| m17 | gives Barrier (damage prevention) | 31 | 31 | 100% | 2 | yes |
| m18 | Nexus Strike triggers | 32 | 32 | 100% | 1 | yes |
| m19 | Last Breath (dies) triggers | 47 | 46 | 98% | 18 | yes |
| m20 | Round Start triggers | 118 | 118 | 100% | 0 | yes |
| m21 | Round End triggers | 31 | 31 | 100% | 191 | yes |
| m22 | Attack triggers | 102 | 101 | 99% | 242 | yes |
| m23 | Overwhelm units deal excess damage | 111 | 111 | 100% | 35 | yes |
| m24 | Elusive units can't be blocked by most units | 80 | 80 | 100% | 269 | yes |
| m25 | Ephemeral units die at round end | 25 | 25 | 100% | 43 | yes |
| m26 | Plunder: needs damage to the enemy Nexus this round | 33 | 33 | 100% | 11 | yes |
| m27 | Countdown landmarks | 26 | 26 | 100% | 5 | yes |
| m28 | refills/gains mana or cares about refilling | 33 | 33 | 100% | 37 | yes |
| m29 | Toss (obliterate own deck) | 13 | 13 | 100% | 3 | yes |
| m30 | Rally (attack token) | 25 | 25 | 100% | 19 | yes |
| m31 | Predict | 20 | 20 | 100% | 62 | yes |
| m32 | reduces costs | 129 | 129 | 100% | 54 | yes |
| m33 | copies cards or spells (incl. becoming an exact copy) | 100 | 98 | 98% | 70 | yes |
| m34 | Behold (have a card) | 16 | 16 | 100% | 101 | yes |
| m35 | Daybreak / Nightfall | 43 | 43 | 100% | 1 | yes |
| m36 | can't block | 8 | 8 | 100% | 341 | yes |
| m37 | summons units or cares about summoning | 279 | 279 | 100% | 190 | yes |
| m38 | revives | 23 | 22 | 96% | 8 | yes |
| m39 | silences | 11 | 11 | 100% | 43 | yes |
| m40 | shuffles cards into a deck | 20 | 20 | 100% | 225 | yes |
| m41 | triggers when you draw | 7 | 7 | 100% | 13 | yes |
| m42 | When I'm summoned triggers | 286 | 286 | 100% | 30 | yes |
| m43 | Strike triggers | 36 | 36 | 100% | 260 | yes |
| m44 | gives Challenger | 25 | 25 | 100% | 10 | yes |
| m45 | gives Elusive | 16 | 16 | 100% | 8 | yes |
| m46 | gives Vulnerable | 35 | 35 | 100% | 2 | yes |
| m47 | Lifesteal units heal their Nexus | 17 | 17 | 100% | 37 | yes |
| m48 | Regeneration units heal fully | 16 | 16 | 100% | 5 | yes |
| m49 | Tough units take less damage | 30 | 30 | 100% | 10 | yes |
| m50 | Fearsome units evade weak blockers | 87 | 87 | 100% | 138 | yes |
| m51 | Quick Attack strikes first | 88 | 88 | 100% | 20 | yes |
| m52 | SpellShield negates enemy spells | 27 | 27 | 100% | 37 | yes |
| m53 | Spirit / Gloom / Impact stacking keywords | 37 | 37 | 100% | 49 | yes |
| m54 | damage equal to a stat or count | 9 | 9 | 100% | 40 | yes |
| m55 | effects scaling with a count (for each) | 89 | 87 | 98% | 625 | yes |
| m56 | temporary buffs this round | 130 | 130 | 100% | 44 | yes |
| m57 | Invoke (does it or cares about it) | 19 | 19 | 100% | 0 | yes |
| m58 | Manifest | 32 | 32 | 100% | 0 | yes |
| m59 | Plants traps or Puffcaps | 39 | 39 | 100% | 11 | yes |
| m60 | Imbue (when a spell resolves) | 20 | 20 | 100% | 22 | yes |
| m61 | Spawn | 15 | 15 | 100% | 0 | yes |
| m62 | Equipment attaches | 56 | 56 | 100% | 42 | yes |
| m63 | Augment grows on created cards | 10 | 10 | 100% | 2 | yes |
| m64 | Formidable strikes with Health | 8 | 8 | 100% | 2 | yes |
| m65 | Reputation | 13 | 13 | 100% | 149 | yes |
| m66 | Allegiance | 10 | 10 | 100% | 18 | yes |
| m67 | Enlightened | 15 | 15 | 100% | 1 | yes |
| m68 | Empowered | 10 | 10 | 100% | 4 | yes |
| m69 | Fury grows on kills | 27 | 27 | 100% | 8 | yes |
| m70 | transforms | 58 | 58 | 100% | 23 | yes |
| m71 | Capture | 18 | 18 | 100% | 4 | yes |
| m72 | Deathless / cheat death | 3 | 3 | 100% | 4 | yes |
| m73 | Nab | 4 | 4 | 100% | 0 | yes |
| m74 | Flow | 13 | 13 | 100% | 0 | yes |
| m75 | Support | 34 | 34 | 100% | 1 | yes |
| m76 | Attune refills spell mana | 25 | 25 | 100% | 21 | yes |
| m77 | Scout attacks again | 16 | 16 | 100% | 13 | yes |
| m78 | Fleeting cards are discarded at round end | 45 | 45 | 100% | 0 | yes |
| m79 | Advance (Countdowns) | 23 | 23 | 100% | 0 | yes |
| m80 | counters spells | 12 | 12 | 100% | 52 | yes |
| m81 | benefits from allies dying, any way (trigger, condition, count, dead allies picked) | 41 | 41 | 100% | 86 | yes |

## Combos (the enabler must set off the payoff)

| case | enabler | payoff | why | found as | pass |
|---|---|---|---|---|---|
| c01 | Hecarim | Shark Chariot | attacking with Ephemeral allies revives the Chariot | event: start_attack -> attacks | yes |
| c03 | Ezreal | Mystic Shot | Nexus Strike creates Mystic Shot | makes | yes |
| c04 | Elise | Frenzied Skitterer | spider tribal | event: summon -> summoned | yes |
| c05 | Get Excited! | Jinx | discarding empties the hand for Jinx's level up | zone: hand | yes |
| c06 | Thresh (level 2) | Kalista (level 2) | summon a champion attacking; Kalista's attack payoff | event: start_attack -> attacks | yes |
| c07 | Vladimir | Legion Veteran | Vladimir damages allies; Veteran buffs allies that survive damage | event: damage -> survives_damage | yes |
| c08 | Puffcap Peddler | Teemo | Peddler plants Puffcaps; Teemo levels on Puffcaps planted | makes | yes |
| c09 | Atrocity | Lucian | Atrocity kills an ally; Lucian levels on allies dying | condition: damage -> dies | yes |
| c10 | Spectral Rider | Soul Shepherd | an Ephemeral ally is summoned; Shepherd buffs it | is: playing Spectral Rider is a summoned the payoff waits for | yes |
| c11 | Twin Disciplines | Lee Sin | playing a spell gives Lee Sin Challenger | is: playing Twin Disciplines is a played the payoff waits for | yes |
| c12 | Brittle Steel | Ashe | Frostbite sets enemy Power to 0; Ashe levels on that | condition: stat_set -> stat_changed | yes |
| c13 | Gnar | Pokey Stick | Strike creates Pokey Stick | makes | yes |
| c14 | Pokey Stick | Swain (level 2) | non-combat damage to the enemy Nexus stuns | event: damage -> nexus_damaged | yes |
| c15 | Coin | Jack | refilling mana heals Jack | event: mana_gain -> mana_refilled | yes |
| c16 | Culling Strike | Kindred | killing a unit lets Kindred mark | event: kill -> killed | yes |
| c17 | Draven | Spinning Axe | Draven creates Spinning Axes | makes | yes |
| c18 | Vladimir | Braum | damaging Braum makes him survive damage and summon a Poro | condition: damage -> survives_damage | yes |
| c19 | Shadow Assassin | Twisted Fate | drawing cards levels Twisted Fate | condition: draw -> drawn | yes |
| c20 | Mystic Shot | Annie | playing Fast spells levels Annie | is: counted as a played spell | yes |
| c21 | Aurelion Sol | The Scourge | Invoked Celestial cards grow The Scourge | type: Celestial | yes |
| c22 | Noxian Fervor | Legion Veteran | damaging an ally that survives | event: damage -> survives_damage | yes |
| c23 | Mystic Shot | Lux | playing spells levels Lux | event: damage -> damaged | yes |
| c24 | Shadow Assassin | Astute Academic | drawing a card buffs the Academic | event: draw -> drawn | yes |
| c25 | Ritual of Renewal | Chief Mechanist Zevi | drawing a card makes Zevi copy it | event: draw -> drawn | yes |
| c26 | Recall | Ahri (level 2) | recalling an ally reduces its cost | event: return_to_hand -> recalled | yes |
| c27 | Decisive Maneuver | Yasuo | stunning an enemy makes Yasuo deal 2 to it | event: stun -> given_keyword | yes |
| c28 | Arachnoid Sentry | Fae Bladetwirler | stunning a unit buffs the Bladetwirler | event: stun -> given_keyword | yes |
| c29 | Ritual of Renewal | Star Shepherd | healing a damaged ally buffs the Shepherd | event: heal -> healed | yes |
| c30 | Health Potion | Stargazer | healing a damaged ally gives it Elusive | event: heal -> healed | yes |
| c31 | Spectral Rider | Shadow Apprentice | summoning an Ephemeral ally buffs the Apprentice | is: playing Spectral Rider is a summoned the payoff waits for | yes |
| c32 | Riposte | Greenglade Caretaker | an ally getting Barrier buffs the Caretaker | event: give_keyword -> given_keyword | yes |
| c33 | Spirit's Refuge | Shen (level 2) | an ally getting Barrier gets +3|+0 from Shen | event: give_keyword -> given_keyword | yes |
| c34 | Shunpo | Windswept Hillock | gaining the attack token stuns the strongest enemy | event: gain_attack_token -> attack_token_gained | yes |
| c35 | Tianna Crownguard | Riven | gaining the attack token makes Riven Reforge | event: gain_attack_token -> attack_token_gained | yes |
| c36 | Glimpse Beyond | Kalista | killing an ally counts toward Kalista's level up | condition: kill -> dies | yes |
| c37 | Ravenous Butcher | Lucian | killing an ally counts toward Lucian's level up | condition: kill -> dies | yes |
| c38 | Mushroom Cloud | Teemo | planting Puffcaps counts toward Teemo's level up | makes | yes |
| c39 | Harsh Winds | Ashe | Frostbite sets Power to 0 for Ashe's level up | condition: stat_set -> stat_changed | yes |
| c40 | Staggering Strikes | Yasuo (level 2) | stunning an enemy makes Yasuo strike it | event: stun -> given_keyword | yes |
| c41 | Skyward Strikes | Yasuo | recalling enemies makes Yasuo deal 2 | event: return_to_hand -> recalled | yes |

## Region identity (signature, splash, archetype)

| case | region | kind | mechanic | need | found | pass |
|---|---|---|---|---|---|---|
| r01 | Shadow Isles | archetype (Claude) | rewards allies dying | 4 | 11 | yes |
| r02 | Shadow Isles | archetype (Claude) | Last Breath | 10 | 21 | yes |
| r03 | Shadow Isles | archetype (Claude) | Ephemeral | 8 | 34 | yes |
| r04 | Shadow Isles | archetype (Claude) | revive | 3 | 20 | yes |
| r05 | Noxus | archetype (Claude) | damages the enemy Nexus | 8 | 71 | yes |
| r06 | Noxus | archetype (Claude) | Overwhelm | 8 | 37 | yes |
| r07 | Noxus | archetype (Claude) | kills own units / self-damage | 2 | 2 | yes |
| r08 | Demacia | archetype (Claude) | grants lasting stats | 10 | 53 | yes |
| r09 | Demacia | archetype (Claude) | gives Barrier | 4 | 12 | yes |
| r10 | Freljord | archetype (Claude) | Frostbite | 8 | 22 | yes |
| r11 | Freljord | archetype (Claude) | heals | 5 | 25 | yes |
| r12 | Ionia | archetype (Claude) | Elusive | 8 | 42 | yes |
| r13 | Ionia | archetype (Claude) | recall | 8 | 52 | yes |
| r14 | Ionia | archetype (Claude) | stun | 5 | 14 | yes |
| r15 | Piltover & Zaun | archetype (Claude) | discard | 8 | 31 | yes |
| r16 | Piltover & Zaun | archetype (Claude) | creates cards | 20 | 87 | yes |
| r17 | Bilgewater | archetype (Claude) | Plunder | 10 | 20 | yes |
| r18 | Bilgewater | archetype (Claude) | Toss | 3 | 6 | yes |
| r19 | Bilgewater | archetype (Claude) | damages the enemy Nexus | 8 | 39 | yes |
| r20 | Targon | archetype (Claude) | Daybreak/Nightfall | 8 | 31 | yes |
| r21 | Targon | archetype (Claude) | Invoke / pick cards | 2 | 26 | yes |
| r22 | Shurima | archetype (Claude) | Countdown | 8 | 14 | yes |
| r23 | Bandle City | archetype (Claude) | creates cards | 15 | 87 | yes |
| r25 | Bandle City | signature (library tags) | trap_secret | 6 | 26 | yes |
| r26 | Bandle City | signature (library tags) | discard | 6 | 20 | yes |
| r27 | Bandle City | signature (library tags) | on_attack | 36 | 90 | yes |
| r28 | Bandle City | signature (library tags) | transform | 8 | 15 | yes |
| r29 | Bandle City | splash (library tags) | stat_gain | 2 | 75 | yes |
| r30 | Bandle City | splash (library tags) | on_spell | 2 | 6 | yes |
| r31 | Bandle City | splash (library tags) | resource_gain | 4 | 8 | yes |
| r32 | Bandle City | splash (library tags) | turn_start | 10 | 18 | yes |
| r33 | Bilgewater | signature (library tags) | resource_gain | 11 | 24 | yes |
| r34 | Bilgewater | splash (library tags) | on_spell | 3 | 11 | yes |
| r35 | Bilgewater | signature (library tags) | draw | 16 | 36 | yes |
| r36 | Bilgewater | signature (library tags) | turn_end | 11 | 29 | yes |
| r37 | Bilgewater | signature (library tags) | damage | 17 | 56 | yes |
| r38 | Bilgewater | splash (library tags) | heal | 4 | 11 | yes |
| r39 | Bilgewater | splash (library tags) | turn_start | 10 | 18 | yes |
| r40 | Bilgewater | splash (library tags) | summon | 19 | 43 | yes |
| r41 | Demacia | signature (library tags) | damage_reduction | 10 | 19 | yes |
| r42 | Demacia | signature (library tags) | stat_gain | 7 | 75 | yes |
| r43 | Demacia | signature (library tags) | multi_attack | 4 | 17 | yes |
| r44 | Demacia | splash (library tags) | merge_attach | 6 | 13 | yes |
| r45 | Demacia | splash (library tags) | on_ally_play | 6 | 43 | yes |
| r47 | Demacia | splash (library tags) | banish | 2 | 9 | yes |
| r48 | Demacia | splash (library tags) | on_attack | 12 | 62 | yes |
| r49 | Freljord | signature (library tags) | on_damaged | 4 | 9 | yes |
| r50 | Freljord | signature (library tags) | excess_damage | 18 | 35 | yes |
| r51 | Freljord | signature (library tags) | damage_reduction | 4 | 9 | yes |
| r52 | Freljord | signature (library tags) | banish | 4 | 9 | yes |
| r53 | Freljord | splash (library tags) | heal | 4 | 25 | yes |
| r54 | Freljord | splash (library tags) | resource_gain | 5 | 10 | yes |
| r55 | Freljord | splash (library tags) | death_trigger | 6 | 8 | yes |
| r56 | Freljord | splash (library tags) | delayed | 3 | 10 | yes |
| r57 | Ionia | signature (library tags) | swap | 2 | 6 | yes |
| r58 | Ionia | signature (library tags) | return_to_hand | 26 | 52 | yes |
| r59 | Ionia | signature (library tags) | attack_now | 5 | 20 | yes |
| r60 | Ionia | signature (library tags) | disable | 14 | 22 | yes |
| r61 | Ionia | splash (library tags) | turn_end | 8 | 32 | yes |
| r62 | Ionia | splash (library tags) | cost_reduction | 6 | 23 | yes |
| r63 | Ionia | splash (library tags) | resource_gain | 4 | 8 | yes |
| r64 | Ionia | splash (library tags) | summon | 18 | 31 | yes |
| r65 | Noxus | signature (library tags) | excess_damage | 18 | 37 | yes |
| r66 | Noxus | signature (library tags) | disable | 10 | 21 | yes |
| r67 | Noxus | signature (library tags) | discard | 4 | 16 | yes |
| r68 | Noxus | signature (library tags) | damage | 18 | 68 | yes |
| r69 | Noxus | splash (library tags) | first_strike | 7 | 16 | yes |
| r70 | Noxus | splash (library tags) | cost_reduction | 5 | 12 | yes |
| r71 | Noxus | splash (library tags) | on_attack | 12 | 88 | yes |
| r72 | Noxus | splash (library tags) | on_play | 26 | 126 | yes |
| r73 | Piltover & Zaun | signature (library tags) | trap_secret | 6 | 17 | yes |
| r74 | Piltover & Zaun | signature (library tags) | discard | 6 | 31 | yes |
| r75 | Piltover & Zaun | signature (library tags) | cost_reduction | 12 | 38 | yes |
| r76 | Piltover & Zaun | signature (library tags) | on_spell | 4 | 28 | yes |
| r77 | Piltover & Zaun | splash (library tags) | resource_gain | 4 | 10 | yes |
| r78 | Piltover & Zaun | splash (library tags) | damage | 14 | 57 | yes |
| r79 | Piltover & Zaun | splash (library tags) | generate_cards | 20 | 70 | yes |
| r80 | Piltover & Zaun | splash (library tags) | transform | 4 | 9 | yes |
| r81 | Shadow Isles | signature (library tags) | revive | 11 | 21 | yes |
| r82 | Shadow Isles | signature (library tags) | destroy | 29 | 88 | yes |
| r83 | Shadow Isles | signature (library tags) | death_trigger | 14 | 50 | yes |
| r84 | Shadow Isles | signature (library tags) | summon | 34 | 45 | yes |
| r85 | Shadow Isles | splash (library tags) | attack_now | 2 | 14 | yes |
| r87 | Shadow Isles | splash (library tags) | cant_attack | 6 | 65 | yes |
| r88 | Shadow Isles | splash (library tags) | merge_attach | 4 | 7 | yes |
| r89 | Shurima | signature (library tags) | variety_payoff | 4 | 11 | yes |
| r90 | Shurima | signature (library tags) | delayed | 12 | 26 | yes |
| r91 | Shurima | signature (library tags) | counter_spell | 2 | 20 | yes |
| r92 | Shurima | signature (library tags) | selection | 6 | 30 | yes |
| r93 | Shurima | splash (library tags) | attack_now | 4 | 18 | yes |
| r94 | Shurima | splash (library tags) | excess_damage | 11 | 22 | yes |
| r95 | Shurima | splash (library tags) | copy | 8 | 13 | yes |
| r96 | Shurima | splash (library tags) | on_ally_play | 6 | 50 | yes |
| r97 | Targon | signature (library tags) | silence | 2 | 6 | yes |
| r98 | Targon | signature (library tags) | selection | 8 | 29 | yes |
| r99 | Targon | signature (library tags) | heal | 9 | 30 | yes |
| r100 | Targon | signature (library tags) | disable | 15 | 28 | yes |
| r101 | Targon | splash (library tags) | delayed | 4 | 7 | yes |
| r102 | Targon | splash (library tags) | cost_reduction | 6 | 22 | yes |
| r104 | Targon | splash (library tags) | discard | 2 | 8 | yes |
| r105 | Bandle City | archetype (library) | scaling | 34 | 86 | yes |
| r106 | Bandle City | archetype (library) | chaos | 28 | 87 | yes |
| r107 | Bandle City | archetype (library) | trickery | 6 | 26 | yes |
| r108 | Bandle City | archetype (library) | transformation | 16 | 34 | yes |
| r109 | Bilgewater | archetype (library) | chaos | 30 | 73 | yes |
| r110 | Bilgewater | archetype (library) | ramp | 17 | 40 | yes |
| r111 | Bilgewater | archetype (library) | graveyard | 4 | 39 | yes |
| r112 | Demacia | archetype (library) | scaling | 21 | 38 | yes |
| r113 | Demacia | archetype (library) | fortress | 22 | 51 | yes |
| r114 | Freljord | archetype (library) | sustain | 14 | 25 | yes |
| r115 | Freljord | archetype (library) | transformation | 11 | 22 | yes |
| r116 | Ionia | archetype (library) | positional | 8 | 12 | yes |
| r117 | Ionia | archetype (library) | control | 38 | 90 | yes |
| r118 | Ionia | archetype (library) | ramp | 14 | 33 | yes |
| r119 | Ionia | archetype (library) | card_advantage | 30 | 42 | yes |
| r120 | Piltover & Zaun | archetype (library) | chaos | 24 | 81 | yes |
| r121 | Piltover & Zaun | archetype (library) | trickery | 6 | 17 | yes |
| r122 | Piltover & Zaun | archetype (library) | ramp | 18 | 46 | yes |
| r123 | Piltover & Zaun | archetype (library) | spellslinger | 14 | 45 | yes |
| r124 | Shadow Isles | archetype (library) | sacrifice | 47 | 108 | yes |
| r125 | Shadow Isles | archetype (library) | graveyard | 14 | 31 | yes |
| r126 | Shadow Isles | archetype (library) | sustain | 17 | 38 | yes |
| r127 | Shadow Isles | archetype (library) | swarm | 36 | 71 | yes |
| r128 | Shurima | archetype (library) | trickery | 5 | 7 | yes |
| r129 | Shurima | archetype (library) | swarm | 30 | 88 | yes |
| r130 | Targon | archetype (library) | spellslinger | 18 | 39 | yes |
| r131 | Targon | archetype (library) | card_advantage | 15 | 44 | yes |

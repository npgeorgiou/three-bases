# Case tests: runeterra

Made by `cases/run.py runeterra`.
**354 of 354 cases pass.**

**Cases whose reason no line says any more (rewrite them): n56, n285**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| m01 | rewards an ally dying (event) | 6 | 6 | 100% | 10 | yes |
| m02 | cares whether allies died (condition) | 13 | 13 | 100% | 21 | yes |
| m03 | triggers when you play a spell | 32 | 32 | 100% | 9 | yes |
| m04 | triggers when you summon an ally | 41 | 41 | 100% | 13 | yes |
| m05 | kills own units | 35 | 35 | 100% | 44 | yes |
| m06 | stuns | 72 | 69 | 96% | 11 | yes |
| m07 | frostbites (power to 0) | 22 | 22 | 100% | 1 | yes |
| m08 | recalls units or cares about recalling | 59 | 59 | 100% | 77 | yes |
| m09 | draws cards | 190 | 187 | 98% | 24 | yes |
| m10 | creates cards | 437 | 436 | 100% | 188 | yes |
| m11 | damages the enemy Nexus | 94 | 92 | 98% | 272 | yes |
| m12 | heals | 68 | 66 | 97% | 74 | yes |
| m13 | discards | 40 | 39 | 98% | 108 | yes |
| m14 | obliterates | 43 | 43 | 100% | 21 | yes |
| m15 | levels up (champion level-up condition) | 119 | 118 | 99% | 4 | yes |
| m16 | grants lasting stats | 234 | 234 | 100% | 233 | yes |
| m17 | gives Barrier (damage prevention) | 31 | 31 | 100% | 2 | yes |
| m18 | Nexus Strike triggers | 32 | 32 | 100% | 1 | yes |
| m19 | Last Breath (dies) triggers | 47 | 46 | 98% | 18 | yes |
| m20 | Round Start triggers | 119 | 119 | 100% | 0 | yes |
| m21 | Round End triggers | 32 | 32 | 100% | 191 | yes |
| m22 | Attack triggers | 106 | 105 | 99% | 244 | yes |
| m23 | Overwhelm units deal excess damage | 114 | 114 | 100% | 35 | yes |
| m24 | Elusive units can't be blocked by most units | 81 | 81 | 100% | 269 | yes |
| m25 | Ephemeral units die at round end | 25 | 25 | 100% | 43 | yes |
| m26 | Plunder: needs damage to the enemy Nexus this round | 33 | 33 | 100% | 11 | yes |
| m27 | Countdown landmarks | 26 | 26 | 100% | 5 | yes |
| m28 | refills/gains mana or cares about refilling | 33 | 33 | 100% | 37 | yes |
| m29 | Toss (obliterate own deck) | 13 | 13 | 100% | 3 | yes |
| m30 | Rally (attack token) | 25 | 25 | 100% | 19 | yes |
| m31 | Predict | 20 | 20 | 100% | 62 | yes |
| m32 | reduces costs | 130 | 130 | 100% | 54 | yes |
| m33 | copies cards or spells (incl. becoming an exact copy) | 100 | 98 | 98% | 72 | yes |
| m34 | Behold (have a card) | 16 | 16 | 100% | 108 | yes |
| m35 | Daybreak / Nightfall | 43 | 43 | 100% | 1 | yes |
| m36 | can't block | 8 | 8 | 100% | 342 | yes |
| m37 | summons units or cares about summoning | 280 | 280 | 100% | 192 | yes |
| m38 | revives | 23 | 22 | 96% | 8 | yes |
| m39 | silences | 11 | 11 | 100% | 42 | yes |
| m40 | shuffles cards into a deck | 20 | 20 | 100% | 227 | yes |
| m41 | triggers when you draw | 7 | 7 | 100% | 13 | yes |
| m42 | When I'm summoned triggers | 288 | 288 | 100% | 30 | yes |
| m43 | Strike triggers | 37 | 37 | 100% | 262 | yes |
| m44 | gives Challenger | 25 | 25 | 100% | 45 | yes |
| m45 | gives Elusive | 16 | 16 | 100% | 8 | yes |
| m46 | gives Vulnerable | 35 | 35 | 100% | 2 | yes |
| m47 | Lifesteal units heal their Nexus | 17 | 17 | 100% | 37 | yes |
| m48 | Regeneration units heal fully | 16 | 16 | 100% | 8 | yes |
| m49 | Tough units take less damage | 30 | 30 | 100% | 10 | yes |
| m50 | Fearsome units evade weak blockers | 87 | 87 | 100% | 140 | yes |
| m51 | Quick Attack strikes first | 90 | 90 | 100% | 20 | yes |
| m52 | SpellShield negates enemy spells | 28 | 28 | 100% | 37 | yes |
| m53 | Spirit / Gloom / Impact stacking keywords | 37 | 37 | 100% | 56 | yes |
| m54 | damage equal to a stat or count | 9 | 9 | 100% | 41 | yes |
| m55 | effects scaling with a count (for each) | 90 | 88 | 98% | 638 | yes |
| m56 | temporary buffs this round | 131 | 131 | 100% | 44 | yes |
| m57 | Invoke (does it or cares about it) | 19 | 19 | 100% | 0 | yes |
| m58 | Manifest | 32 | 32 | 100% | 0 | yes |
| m59 | Plants traps or Puffcaps | 40 | 40 | 100% | 11 | yes |
| m60 | Imbue (when a spell resolves) | 20 | 20 | 100% | 22 | yes |
| m61 | Spawn | 15 | 15 | 100% | 0 | yes |
| m62 | Equipment attaches | 56 | 56 | 100% | 45 | yes |
| m63 | Augment grows on created cards | 10 | 10 | 100% | 2 | yes |
| m64 | Formidable strikes with Health | 8 | 8 | 100% | 2 | yes |
| m65 | Reputation | 13 | 13 | 100% | 149 | yes |
| m66 | Allegiance | 10 | 10 | 100% | 18 | yes |
| m67 | Enlightened | 15 | 15 | 100% | 1 | yes |
| m68 | Empowered | 10 | 10 | 100% | 4 | yes |
| m69 | Fury grows on kills | 28 | 28 | 100% | 8 | yes |
| m70 | transforms | 60 | 60 | 100% | 23 | yes |
| m71 | Capture | 18 | 18 | 100% | 4 | yes |
| m72 | Deathless / cheat death | 3 | 3 | 100% | 23 | yes |
| m73 | Nab | 4 | 4 | 100% | 0 | yes |
| m74 | Flow | 13 | 13 | 100% | 0 | yes |
| m75 | Support | 34 | 34 | 100% | 1 | yes |
| m76 | Attune refills spell mana | 25 | 25 | 100% | 21 | yes |
| m77 | Scout attacks again | 16 | 16 | 100% | 25 | yes |
| m78 | Fleeting cards are discarded at round end | 45 | 45 | 100% | 0 | yes |
| m79 | Advance (Countdowns) | 23 | 23 | 100% | 0 | yes |
| m80 | counters spells | 12 | 12 | 100% | 53 | yes |
| m81 | benefits from allies dying, any way (trigger, condition, count, dead allies picked) | 42 | 41 | 98% | 85 | yes |
| mx01 | a trigger on another unit dying is other_death_trigger | 6 | 6 | 100% | 38 | yes |
| mx02 | moving enemy units is forced_movement | 0 | 0 | 100% | 8 | yes |
| mx03 | a plain draw is one form: zone deck_top, no pick top | 141 | 138 | 98% | 73 | yes |
| mx10 | damage to the enemy player is Nexus damage (kinds kept, v30) | 60 | 60 | 100% | 1358 | yes |
| mx11 | moving or pushing units makes units move (positions change, v30) | 0 | 0 | 100% | 17 | yes |
| mx12 | a unit that moves (onto a space) is the event's object, never its actor (N16, Sentry, v36, v38) | 0 | 0 | 100% | 0 | yes |
| mx13 | can't be targeted by spells: the cant is on the spells, the protected unit is "to" (N19, v37) | 0 | 0 | 100% | 51 | yes |
| mx14 | a dead unit put into play is revive, never summon from the discard (N20, v37) | 0 | 0 | 100% | 30 | yes |
| mx15 | a trigger that holds only "this turn" is an ability given to the player for this turn (v37, Duelyst) | 0 | 0 | 100% | 21 | yes |
| mx13 | an effect on the creature opposing it is about lanes (concept lanes from same_lane, v38) | 0 | 0 | 100% | 0 | yes |
| mx14 | a strike on the spaces beside the opposing one reaches other lanes (cross_lane, v38) | 0 | 0 | 100% | 0 | yes |
| mx15 | within a circuit is a formation (link_formation, v38) | 0 | 0 | 100% | 0 | yes |
| mx16 | more or faster base resource (base_resource_gain, v38) | 0 | 0 | 100% | 67 | yes |

## Combos (the enabler must set off the payoff)

| case | enabler | payoff | why | found as | pass |
|---|---|---|---|---|---|
| c01 | Hecarim | Shark Chariot | attacking with Ephemeral allies revives the Chariot | event: kill -> dies (via Spectral Rider) | yes |
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
| r13 | Ionia | archetype (Claude) | recall | 8 | 51 | yes |
| r14 | Ionia | archetype (Claude) | stun | 5 | 14 | yes |
| r15 | Piltover & Zaun | archetype (Claude) | discard | 8 | 31 | yes |
| r16 | Piltover & Zaun | archetype (Claude) | creates cards | 20 | 87 | yes |
| r17 | Bilgewater | archetype (Claude) | Plunder | 10 | 20 | yes |
| r18 | Bilgewater | archetype (Claude) | Toss | 3 | 6 | yes |
| r19 | Bilgewater | archetype (Claude) | damages the enemy Nexus | 8 | 40 | yes |
| r20 | Targon | archetype (Claude) | Daybreak/Nightfall | 8 | 31 | yes |
| r21 | Targon | archetype (Claude) | Invoke / pick cards | 2 | 26 | yes |
| r22 | Shurima | archetype (Claude) | Countdown | 8 | 14 | yes |
| r23 | Bandle City | archetype (Claude) | creates cards | 15 | 87 | yes |
| r25 | Bandle City | signature (library tags) | trap_secret | 6 | 26 | yes |
| r26 | Bandle City | signature (library tags) | discard | 6 | 20 | yes |
| r27 | Bandle City | signature (library tags) | on_attack | 36 | 90 | yes |
| r28 | Bandle City | signature (library tags) | transform | 8 | 14 | yes |
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
| r41 | Demacia | signature (library tags) | damage_reduction | 10 | 38 | yes |
| r42 | Demacia | signature (library tags) | stat_gain | 7 | 75 | yes |
| r43 | Demacia | signature (library tags) | multi_attack | 4 | 21 | yes |
| r44 | Demacia | splash (library tags) | merge_attach | 6 | 13 | yes |
| r45 | Demacia | splash (library tags) | on_ally_play | 6 | 43 | yes |
| r47 | Demacia | splash (library tags) | banish | 2 | 9 | yes |
| r48 | Demacia | splash (library tags) | on_attack | 12 | 62 | yes |
| r49 | Freljord | signature (library tags) | on_damaged | 4 | 9 | yes |
| r50 | Freljord | signature (library tags) | excess_damage | 18 | 35 | yes |
| r51 | Freljord | signature (library tags) | damage_reduction | 4 | 10 | yes |
| r52 | Freljord | signature (library tags) | banish | 4 | 9 | yes |
| r53 | Freljord | splash (library tags) | heal | 4 | 25 | yes |
| r54 | Freljord | splash (library tags) | resource_gain | 5 | 10 | yes |
| r55 | Freljord | splash (library tags) | death_trigger | 6 | 7 | yes |
| r56 | Freljord | splash (library tags) | delayed | 3 | 10 | yes |
| r57 | Ionia | signature (library tags) | swap | 2 | 6 | yes |
| r58 | Ionia | signature (library tags) | return_to_hand | 26 | 42 | yes |
| r59 | Ionia | signature (library tags) | attack_now | 5 | 19 | yes |
| r60 | Ionia | signature (library tags) | disable | 14 | 16 | yes |
| r61 | Ionia | splash (library tags) | turn_end | 8 | 32 | yes |
| r62 | Ionia | splash (library tags) | cost_reduction | 6 | 23 | yes |
| r63 | Ionia | splash (library tags) | resource_gain | 4 | 8 | yes |
| r64 | Ionia | splash (library tags) | summon | 18 | 32 | yes |
| r65 | Noxus | signature (library tags) | excess_damage | 18 | 37 | yes |
| r66 | Noxus | signature (library tags) | disable | 10 | 18 | yes |
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
| r83 | Shadow Isles | signature (library tags) | death_trigger | 14 | 28 | yes |
| r84 | Shadow Isles | signature (library tags) | summon | 34 | 45 | yes |
| r85 | Shadow Isles | splash (library tags) | attack_now | 2 | 14 | yes |
| r87 | Shadow Isles | splash (library tags) | cant_attack | 6 | 65 | yes |
| r88 | Shadow Isles | splash (library tags) | merge_attach | 4 | 7 | yes |
| r89 | Shurima | signature (library tags) | variety_payoff | 4 | 11 | yes |
| r90 | Shurima | signature (library tags) | delayed | 12 | 26 | yes |
| r91 | Shurima | signature (library tags) | counter_spell | 2 | 5 | yes |
| r92 | Shurima | signature (library tags) | selection | 6 | 30 | yes |
| r93 | Shurima | splash (library tags) | attack_now | 4 | 18 | yes |
| r94 | Shurima | splash (library tags) | excess_damage | 11 | 22 | yes |
| r95 | Shurima | splash (library tags) | copy | 8 | 13 | yes |
| r96 | Shurima | splash (library tags) | on_ally_play | 6 | 50 | yes |
| r97 | Targon | signature (library tags) | silence | 2 | 5 | yes |
| r98 | Targon | signature (library tags) | selection | 8 | 29 | yes |
| r99 | Targon | signature (library tags) | heal | 9 | 30 | yes |
| r100 | Targon | signature (library tags) | disable | 15 | 28 | yes |
| r101 | Targon | splash (library tags) | delayed | 4 | 7 | yes |
| r102 | Targon | splash (library tags) | cost_reduction | 6 | 22 | yes |
| r104 | Targon | splash (library tags) | discard | 2 | 8 | yes |
| r105 | Bandle City | archetype (library) | scaling | 34 | 87 | yes |
| r106 | Bandle City | archetype (library) | chaos | 28 | 87 | yes |
| r107 | Bandle City | archetype (library) | trickery | 6 | 26 | yes |
| r108 | Bandle City | archetype (library) | transformation | 16 | 34 | yes |
| r109 | Bilgewater | archetype (library) | chaos | 30 | 73 | yes |
| r110 | Bilgewater | archetype (library) | ramp | 17 | 40 | yes |
| r111 | Bilgewater | archetype (library) | graveyard | 4 | 39 | yes |
| r112 | Demacia | archetype (library) | scaling | 21 | 44 | yes |
| r113 | Demacia | archetype (library) | fortress | 22 | 54 | yes |
| r114 | Freljord | archetype (library) | sustain | 14 | 27 | yes |
| r115 | Freljord | archetype (library) | transformation | 11 | 22 | yes |
| r116 | Ionia | archetype (library) | positional | 8 | 12 | yes |
| r117 | Ionia | archetype (library) | control | 38 | 88 | yes |
| r118 | Ionia | archetype (library) | ramp | 14 | 33 | yes |
| r119 | Ionia | archetype (library) | card_advantage | 30 | 42 | yes |
| r120 | Piltover & Zaun | archetype (library) | chaos | 24 | 81 | yes |
| r121 | Piltover & Zaun | archetype (library) | trickery | 6 | 17 | yes |
| r122 | Piltover & Zaun | archetype (library) | ramp | 18 | 46 | yes |
| r123 | Piltover & Zaun | archetype (library) | spellslinger | 14 | 45 | yes |
| r124 | Shadow Isles | archetype (library) | sacrifice | 47 | 102 | yes |
| r125 | Shadow Isles | archetype (library) | graveyard | 14 | 31 | yes |
| r126 | Shadow Isles | archetype (library) | sustain | 17 | 41 | yes |
| r127 | Shadow Isles | archetype (library) | swarm | 36 | 71 | yes |
| r128 | Shurima | archetype (library) | trickery | 5 | 8 | yes |
| r129 | Shurima | archetype (library) | swarm | 30 | 88 | yes |
| r130 | Targon | archetype (library) | spellslinger | 18 | 39 | yes |
| r131 | Targon | archetype (library) | card_advantage | 15 | 44 | yes |

## Guide decks (the explanation must say what the guide says)

| case | deck | must say | missing | pass |
|---|---|---|---|---|

## Deck networks (a line must be there, or must not)

| case | deck | from | to | expect | found | pass |
|---|---|---|---|---|---|---|
| n01 | Braum Zoe | Falling Star | Braum | none  | - | yes |
| n02 | Annie Gwen | * | Ravenbloom Conservatory | line  | type: is a card it counts when played; type: is played | yes |
| n03 | Caitlyn Teemo | Puffcap Peddler | Caitlyn | line  | levels: plants traps that go off later (levels it up) | yes |
| n04 | Caitlyn Teemo | * | Caitlyn (level 2) | line  | levelsinto: levels into; stronger: more power: it hits harder; type: is a trap t | yes |
| n05 | Caitlyn Teemo | * | Teemo (level 2) | line  | levelsinto: levels into; stronger: more power: it hits harder | yes |
| n06 | Caitlyn Teemo | Ava Achiever | Poison Puffcap | line  | puts: plants; also makes stronger: makes its effect bigger | yes |
| n07 | Caitlyn Teemo | * | Corina, Mastermind | line  | repeats: makes the Trap it gives stronger; stronger: can give it +1|+1; stronger | yes |
| n08 | Bard Norra | Cosmic Binding | Chime | line  | puts: plants | yes |
| n09 | Bard Norra | Chime | Bard | line  | levels: changes your units' stats (levels it up); also makes stronger: can give  | yes |
| n10 | Bard Norra | Bard | Bard (level 2) | line  | levelsinto: levels into | yes |
| n11 | Bard Norra | Norra (level 2) | Mysterious Portal | line  | puts: plants; also changes how it works: gives it an ability | yes |
| n12 | Darius Gnar | * | Darius | line  | levels: damages the enemy player (levels it up); levels: damages the enemy playe | yes |
| n13 | Ashe LeBlanc | * | LeBlanc | line  | levels: damages units or players (levels it up); puts: copies it; stronger: can  | yes |
| n14 | Ashe LeBlanc | * | LeBlanc (level 2) | line  | levelsinto: levels into; puts: copies it; stronger: can give it +0|+2; stronger: | yes |
| n15 | Ashe LeBlanc | Ashe | LeBlanc | none  | - | yes |
| n16 | Ashe LeBlanc | * | Bloody Business | line  | type: helps my units strike more | yes |
| n26 | Annie Gwen | Gwen (level 2) | Gwen | none  | - | yes |
| n27 | Annie Gwen | Molten Shield | Annie | line  | levels: is a card it counts when played (levels it up) | yes |
| n28 | Annie Gwen | Tybaulk | Withering Wail | line  | stronger: its damage gets 1 more | yes |
| n29 | Caitlyn Teemo | Advanced Intel | Teemo | none  | - | yes |
| n30 | Caitlyn Teemo | Pie Toss | Bursting Backpack | none  | - | yes |
| n31 | Bard Norra | Cosmic Binding | Bard | line  | levels: through Chime: changes your units' stats (levels it up) | yes |
| n32 | Bard Norra | Byrd, The Bellringer | Bard | line  | levels: through Chime: changes your units' stats (levels it up) | yes |
| n33 | Darius Gnar | Yadulski Snowdog | Darius | line  | stronger: can give it +1|+1 | yes |
| n34 | Darius Gnar | Brothers' Bond | Darius | line  | stronger: can give it +2|+0 | yes |
| n35 | Darius Gnar | Darius | Mega Gnar (level 2) | none  | - | yes |
| n36 | Ashe LeBlanc | Avarosan Hearthguard | Trifarian Gloryseeker | line  | stronger: gives it +1|+1 | yes |
| n37 | Ashe LeBlanc | Incisive Tactician | Ashe | line  | levels: makes it attack for its effect (it levels up from what it then does) | yes |
| n38 | Braum Zoe | Cosmic Youngling | Braum | none  | - | yes |
| n39 | Braum Zoe | Targonian Tellstones | Zoe | line  | levels: creates cards: more different cards to play (levels it up); also trigger | yes |
| n43 | Annie Gwen | Tybaulk | Torment | line  | stronger: its damage gets 1 more | yes |
| n44 | Annie Gwen | Tybaulk | Vile Feast | line  | stronger: its damage gets 1 more | yes |
| n45 | Annie Gwen | Tybaulk | Armed Acquisitioner | line  | stronger: gives it +1|+0 | yes |
| n46 | Annie Gwen | Tybaulk | Annie | none its damage | stronger: gives it +1|+0 | yes |
| n48 | Braum Zoe | Sunburst | Braum | none  | - | yes |
| n49 | Janna Nilah | Windborne Mariner | Janna | line  | levels: changes card costs (levels it up) | yes |
| n50 | Janna Nilah | Ruined Rex | Janna | none  | - | yes |
| n52 | Ping City | Make it Rain | Gangplank | line  | levels: damages the enemy player (levels it up) | yes |
| n53 | Ping City | Jagged Butcher | Gangplank | none  | - | yes |
| n54 | Ping City | Powder Keg | Gangplank | none by fighting | - | yes |
| n55 | Ashe LeBlanc | Incisive Tactician | Yadulski Snowdog | line  | waits: makes it attack for its effect | yes |
| n56 | Braum Zoe | Spirits Unleashed | Braum | none rules: | levels: damages it without killing it, for its effect (levels it up); also more  | yes |
| n58 | Swain Ziggs | Bomber Twins | Ziggs | line  | type: makes a landmark or structure it counts | yes |
| n59 | Swain Ziggs | Conchologist | Swain | none  | - | yes |
| n60 | Lurkers | Aspiring Chronomancer | Pyke | none  | - | yes |
| n61 | Soraka Tahm Kench | An Acquired Taste | Tahm Kench | line  | levels: uses Capture (levels it up) | yes |
| n62 | Aphelios Zoe | Duskpetal Dust | Pale Cascade | line  | cheaper: makes it cheaper when it comes | yes |
| n70 | Braum Zoe | Behold the Infinite | Supercool Starchart | none  | - | yes |
| n71 | Caitlyn Teemo | Poison Dart | Caitlyn | line plants traps | levels: plants traps that go off later (levels it up) | yes |
| n242 | Hecarim Zed | Dragon Ambush | Zed | none  | - | yes |
| n243 | Hecarim Zed | Hecarim | Zed | none  | - | yes |
| n244 | Hecarim Zed | Zed | Ghastly Band | none  | - | yes |
| n245 | Hecarim Zed | Mark of the Isles | Hecarim | line makes your units Ephemeral | levels: makes your units Ephemeral (levels it up); also makes stronger: can give | yes |
| n246 | Elu Thresh | Thresh | Hecarim | none  | - | yes |
| n247 | Hecarim Zed | Soul Cleave | Undying Revenge | line brings them back | type: makes your units die: Undying Revenge brings them back | yes |
| n248 | Hecarim Zed | Glimpse Beyond | The Iron Conquest | none brings them back | - | yes |
| n249 | Hecarim Zed | Dragon Ambush | Dragonling | line summons | puts: summons | yes |
| n250 | Hecarim Zed | Hecarim | Shark Chariot | line  | waits: makes your units attack | yes |
| n251 | Hecarim Zed | Shark Chariot | Zed | none makes it attack | - | yes |
| n252 | Hecarim Zed | Redeemed Prodigy | Shark Chariot | line  | waits: makes your units attack | yes |
| n253 | Lux Jayce | Thermogenic Beam | Lux | line (levels it up) | levels: has a variable cost: pays it alone (levels it up) | yes |
| n254 | Lux Jayce | For Demacia! | Lux | line (levels it up) | levels: costs 6: pays it alone (levels it up); also makes stronger: can give it  | yes |
| n255 | Rally Elusives, aka Zed Poppy | Living Shadow | Zed | none (levels it up) | - | yes |
| n256 | Rally Elusives, aka Zed Poppy | Sharpsight | Zed | none (levels it up) | stronger: can give it +1|+2 | yes |
| n257 | Rally Elusives, aka Zed Poppy | For Demacia! | Zed | none (levels it up) | stronger: can give it +3|+3 | yes |
| n258 | Rally Elusives, aka Zed Poppy | Twin Disciplines | Zed | none (levels it up) | stronger: can give it +3|+0; also can give it +0|+3 | yes |
| n259 | Rally Elusives, aka Zed Poppy | Poppy | Zed | none (levels it up) | stronger: gives it +1|+1 | yes |
| n260 | Rally Elusives, aka Zed Poppy | Young Witch | Zed | none (levels it up) | stronger: more power | yes |
| n261 | Rally Elusives, aka Zed Poppy | Ghost | Zed | line (levels it up) | levels: helps it hit the enemy player (levels it up); also gives keyword: can gi | yes |
| n262 | Rally Elusives, aka Zed Poppy | Relentless Pursuit | Poppy | line another attack | levels: another attack (levels it up); also makes it attack for its effect (leve | yes |
| n263 | Rally Elusives, aka Zed Poppy | Brightsteel Protector | Poppy | none (levels it up) | keyword: can give it Barrier | yes |
| n264 | Rally Elusives, aka Zed Poppy | Zed | Poppy | none (levels it up) | - | yes |
| n265 | Braum Zoe | Targonian Tellstones | Braum | none (levels it up) | - | yes |
| n266 | Braum Zoe | Blessing of Targon | Braum | line (levels it up) | levels: more health or protection: survives damage (levels it up); also triggers | yes |
| n267 | Braum Zoe | Esmus, Breath of the World | Zoe | none different cards | waits: makes your units hit the enemy player; also makes stronger: more power: i | yes |
| n268 | Annie Gwen | Ravenbloom Conservatory | Gwen | none (levels it up) | - | yes |
| n269 | Annie Gwen | Tybaulk | Gwen | none (levels it up) | waits: changes your units' stats; also makes stronger: gives it +1|+0 | yes |
| n270 | Janna Nilah | Vikrash the Exuberant | Janna | none (levels it up) | - | yes |
| n271 | Janna Nilah | Nilah | Janna | none (levels it up) | - | yes |
| n272 | Janna Nilah | Slipstream | Janna | none (levels it up) | waits: makes you draw cards | yes |
| n273 | Janna Nilah | Pool Shark | Janna | none enables | waits: makes you draw cards | yes |
| n274 | Janna Nilah | Windborne Mariner | Janna | line (levels it up) | levels: changes card costs (levels it up) | yes |
| n275 | Janna Nilah | Sunken Temple | Janna | line changes card costs | levels: changes card costs (levels it up); also triggers: makes you draw cards | yes |
| n276 | Janna Nilah | Janna | Nilah | line (levels it up) | levels: makes you draw cards (levels it up); also makes cheaper: makes it cheape | yes |
| n277 | Bard Norra | Byrd, The Bellringer | Norra | none (levels it up) | - | yes |
| n278 | Bard Norra | Portalpalooza | Norra | line Mysterious Portal | levels: through Mysterious Portal: puts your units into play (levels it up) | yes |
| n279 | Bard Norra | Cosmic Binding | Bard | line (levels it up) | levels: through Chime: changes your units' stats (levels it up) | yes |
| n280 | Unstoppable Yasuo | Concussive Palm | Malphite | none (levels it up) | - | yes |
| n281 | Swain Ziggs | Captain Farron | Swain | none (levels it up) | - | yes |
| n282 | Elu Thresh | Hecarim | Thresh | none (levels it up) | - | yes |
| n283 | Akshan Riven | Blade of the Exile | Akshan | none strike | stronger: can give it +2|+0 | yes |
| n284 | Hecarim Zed | Zed | Hecarim | line (levels it up) | levels: makes units attack (levels it up) | yes |
| n285 | Draven Viktor | Chump Whump | Get Excited! | none cards to discard | - | yes |

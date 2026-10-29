# Case tests: monster_train

Made by `cases/run.py monster_train`.
**143 of 143 cases pass.**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| mt01 | Summon triggers | 13 | 13 | 100% | 180 | yes |
| mt02 | Strike triggers | 9 | 9 | 100% | 7 | yes |
| mt03 | Revenge triggers | 7 | 7 | 100% | 32 | yes |
| mt04 | Slay triggers | 14 | 14 | 100% | 0 | yes |
| mt05 | Extinguish triggers | 11 | 11 | 100% | 4 | yes |
| mt06 | Harvest triggers | 5 | 5 | 100% | 0 | yes |
| mt07 | Incant triggers | 10 | 10 | 100% | 0 | yes |
| mt08 | Rally triggers | 1 | 1 | 100% | 0 | yes |
| mt09 | Rejuvenate triggers | 4 | 4 | 100% | 0 | yes |
| mt10 | Resolve triggers | 8 | 8 | 100% | 15 | yes |
| mt11 | Action triggers | 2 | 2 | 100% | 0 | yes |
| mt12 | End of Turn triggers | 1 | 1 | 100% | 18 | yes |
| mt13 | Gorge triggers | 7 | 7 | 100% | 0 | yes |
| mt14 | Eaten triggers | 7 | 7 | 100% | 0 | yes |
| mt15 | Hunger triggers | 1 | 1 | 100% | 1 | yes |
| mt16 | Etch triggers | 4 | 4 | 100% | 0 | yes |
| mt17 | Inspire triggers | 4 | 4 | 100% | 0 | yes |
| mt18 | Reserve triggers | 6 | 6 | 100% | 0 | yes |
| mt19 | Hatch triggers | 3 | 3 | 100% | 12 | yes |
| mt20 | extra draw next turn | 6 | 6 | 100% | 43 | yes |
| mt21 | deals damage | 53 | 52 | 98% | 32 | yes |
| mt22 | restores health | 14 | 14 | 100% | 6 | yes |
| mt23 | kills | 5 | 5 | 100% | 21 | yes |
| mt24 | draws cards | 12 | 12 | 100% | 8 | yes |
| mt25 | discards | 6 | 6 | 100% | 0 | yes |
| mt26 | gains Ember | 15 | 15 | 100% | 23 | yes |
| mt27 | gains gold | 4 | 4 | 100% | 0 | yes |
| mt28 | changes floor capacity | 6 | 6 | 100% | 0 | yes |
| mt29 | adds cards to hand | 14 | 14 | 100% | 12 | yes |
| mt30 | damages its own Pyre | 5 | 5 | 100% | 0 | yes |
| mt31 | X cost amounts | 17 | 17 | 100% | 1 | yes |
| mt32 | hits the front enemy unit | 21 | 21 | 100% | 4 | yes |
| mt33 | on this floor | 14 | 14 | 100% | 52 | yes |
| mt34 | consumed cards matter | 6 | 6 | 100% | 4 | yes |
| mt35 | permanent changes | 7 | 7 | 100% | 11 | yes |
| mt36 | moves units | 4 | 4 | 100% | 9 | yes |
| mt37 | doubles amounts | 4 | 4 | 100% | 15 | yes |
| mt38 | Armor (gives, has or uses it) | 20 | 20 | 100% | 0 | yes |
| mt39 | Rage (gives, has or uses it) | 16 | 16 | 100% | 0 | yes |
| mt40 | Multistrike (gives, has or uses it) | 13 | 13 | 100% | 0 | yes |
| mt41 | Burnout (gives, has or uses it) | 12 | 12 | 100% | 5 | yes |
| mt42 | Frostbite (gives, has or uses it) | 11 | 11 | 100% | 0 | yes |
| mt43 | Sap (gives, has or uses it) | 4 | 4 | 100% | 0 | yes |
| mt44 | Dazed (gives, has or uses it) | 8 | 8 | 100% | 0 | yes |
| mt45 | Spikes (gives, has or uses it) | 9 | 9 | 100% | 0 | yes |
| mt46 | Regen (gives, has or uses it) | 4 | 4 | 100% | 0 | yes |
| mt47 | Damage Shield (gives, has or uses it) | 8 | 8 | 100% | 0 | yes |
| mt48 | Lifesteal (gives, has or uses it) | 4 | 4 | 100% | 0 | yes |
| mt49 | Stealth (gives, has or uses it) | 3 | 3 | 100% | 0 | yes |
| mt50 | Spell Weakness (gives, has or uses it) | 4 | 4 | 100% | 0 | yes |
| mt51 | Melee Weakness (gives, has or uses it) | 2 | 2 | 100% | 0 | yes |
| mt52 | Reap (gives, has or uses it) | 8 | 8 | 100% | 0 | yes |
| mt53 | Emberdrain (gives, has or uses it) | 5 | 5 | 100% | 0 | yes |
| mt54 | Rooted (gives, has or uses it) | 2 | 2 | 100% | 0 | yes |
| mt55 | Quick (gives, has or uses it) | 4 | 4 | 100% | 0 | yes |
| mt56 | Sweep (gives, has or uses it) | 7 | 7 | 100% | 0 | yes |
| mt57 | Trample (gives, has or uses it) | 4 | 4 | 100% | 0 | yes |
| mt58 | Endless (gives, has or uses it) | 3 | 3 | 100% | 0 | yes |
| mt59 | Consume (gives, has or uses it) | 60 | 59 | 98% | 0 | yes |
| mt60 | Purge (gives, has or uses it) | 11 | 11 | 100% | 0 | yes |
| mt61 | Piercing (gives, has or uses it) | 5 | 5 | 100% | 0 | yes |
| mt62 | Attuned (gives, has or uses it) | 6 | 6 | 100% | 0 | yes |
| mt63 | Permafrost (gives, has or uses it) | 3 | 3 | 100% | 0 | yes |
| mt64 | Frozen (gives, has or uses it) | 2 | 2 | 100% | 2 | yes |
| mt65 | Offering (gives, has or uses it) | 3 | 3 | 100% | 0 | yes |
| mt66 | Extract (gives, has or uses it) | 10 | 10 | 100% | 0 | yes |
| mt67 | Infused (gives, has or uses it) | 2 | 2 | 100% | 0 | yes |
| mt68 | Pyrebound (gives, has or uses it) | 2 | 2 | 100% | 0 | yes |
| mt69 | Reform (gives, has or uses it) | 6 | 6 | 100% | 0 | yes |
| mt70 | Ascend (gives, has or uses it) | 4 | 4 | 100% | 0 | yes |
| mt71 | Descend (gives, has or uses it) | 4 | 4 | 100% | 0 | yes |
| mt72 | Cultivate (gives, has or uses it) | 2 | 2 | 100% | 0 | yes |
| mt73 | Sacrifice (gives, has or uses it) | 3 | 3 | 100% | 0 | yes |
| mt74 | Magic Power (gives, has or uses it) | 3 | 3 | 100% | 6 | yes |
| mt75 | Shell (gives, has or uses it) | 5 | 5 | 100% | 0 | yes |
| mt76 | Fragile (gives, has or uses it) | 1 | 1 | 100% | 0 | yes |
| mt77 | Unplayable (gives, has or uses it) | 2 | 2 | 100% | 0 | yes |
| mx01 | a trigger on another unit dying is other_death_trigger | 5 | 5 | 100% | 3 | yes |
| mx02 | moving enemy units is forced_movement | 3 | 3 | 100% | 10 | yes |
| mx03 | a plain draw is one form: zone deck_top, no pick top | 10 | 10 | 100% | 10 | yes |
| mx10 | damage to the enemy player is Nexus damage (kinds kept, v30) | 0 | 0 | 100% | 16 | yes |
| mx11 | moving or pushing units makes units move (positions change, v30) | 0 | 0 | 100% | 13 | yes |

## Combos (the enabler must set off the payoff)

| case | enabler | payoff | why | found as | pass |
|---|---|---|---|---|---|
| cmt17 | Crystalline Seeds | Hoarfrost Effigy | Frostbite to gather and double | keyword: Frostbite | yes |
| cmt18 | Titanstooth | Hoarfrost Effigy | Frostbite to gather and double | keyword: Frostbite | yes |
| cmt28 | Cannibalize | Penumbra | Morsels for Penumbra to Gorge on | type: Morsel | yes |
| cmt29 | Morselmaker | Penumbra | Morsels for Penumbra | type: Morsel | yes |
| cmt36 | Molded | Rector Flicker | returns the fallen Flicker by Reform | event: kill -> dies | yes |
| cmt37 | Crushing Demise | Rector Flicker | deaths feed the Accumulator Harvest | event: kill -> dies | yes |
| cmt45 | Titan Sentry | Hoarfrost Effigy | Frostbite build: Frostbite to gather and double | keyword: Frostbite | yes |
| cmt46 | Glacial Seal | Hoarfrost Effigy | Frostbite build: Frostbite to gather and double | keyword: Frostbite | yes |
| cmt47 | Imp-in-a-Box | Imp-olate | Imp build: more Imps in the deck, more damage | type: Imp | yes |
| cmt48 | Queen's Impling | Transcendimp | Imp build: Summon effects to repeat | trigger keyword: Summon | yes |
| cmt49 | Impish Scholar | Transcendimp | Imp build: Summon effects to repeat | trigger keyword: Summon | yes |
| cmt50 | Making of a Morsel | Penumbra | Morsel build: a Morsel Miner for Penumbra to eat | type: Morsel | yes |
| cmt51 | Morsel Miner | Penumbra | Morsel build: Penumbra eats it for its bonus | type: Morsel | yes |
| cmt52 | Rootseeds | Siren of the Sea | Stygian + Awoken: cheap Awoken spells set off Incant | is: playing Rootseeds is a played the payoff waits for | yes |
| cmt53 | Steel Enhancer | Guard of the Unnamed | Stygian + Awoken: cheap Awoken spells set off Incant | is: playing Steel Enhancer is a played the payoff waits for | yes |
| cmt54 | Molded | Queen's Impling | Hellhorned + Melting Remnant: Reform brings Imps back to replay their Summon | replay: back in hand, played again | yes |
| cmt55 | Furnace Tap | Tethys Titansbane | Tethys + Umbra: Multistrike makes more Strikes that apply Frostbite | event: start_attack -> attacks | yes |
| cmt56 | Ritual of Battle | Deranged Brute | Hellhorned rage: Rage on friendly units hits harder | state: given_keyword | yes |
| cmt57 | Dark Deal | Deranged Brute | Hellhorned rage: Rage on friendly units hits harder | state: given_keyword | yes |
| cmt58 | Railbeater | Battering Ram | Hellhorned armor: Armor turns into damage | keyword: Armor | yes |
| cmt59 | Welder Helper | Battering Ram | Hellhorned armor: Armor turns into damage | keyword: Armor | yes |
| cmt60 | Imp-in-a-Box | Imp-pressive | Hellhorned Imps: an Imp to sacrifice | target: type Imp | yes |
| cmt61 | Imp-in-a-Box | Imp-portant Work | Hellhorned Imps: an Imp to sacrifice | target: type Imp | yes |

## Region identity (signature, splash, archetype)

| case | region | kind | mechanic | need | found | pass |
|---|---|---|---|---|---|---|
| rmt01 | Hellhorned | signature (library) | Multistrike | 2 | 3 | yes |
| rmt02 | Hellhorned | signature (library) | Rage | 8 | 11 | yes |
| rmt03 | Hellhorned | signature (library) | Imps | 8 | 14 | yes |
| rmt04 | Hellhorned | archetype (Claude) | Armor | 8 | 13 | yes |
| rmt05 | Hellhorned | archetype (Claude) | Summon triggers | 6 | 31 | yes |
| rmt06 | Awoken | signature (library) | Sweep | 3 | 3 | yes |
| rmt07 | Awoken | archetype (Claude) | Spikes | 6 | 8 | yes |
| rmt08 | Awoken | archetype (Claude) | healing | 6 | 11 | yes |
| rmt09 | Awoken | archetype (Claude) | Rejuvenate | 3 | 4 | yes |
| rmt10 | Awoken | archetype (Claude) | extra draw next turn | 5 | 11 | yes |
| rmt11 | Stygian Guard | signature (library) | Frostbite | 7 | 11 | yes |
| rmt12 | Stygian Guard | archetype (library) | spells: Incant | 5 | 9 | yes |
| rmt13 | Stygian Guard | archetype (Claude) | discard and Offering | 4 | 9 | yes |
| rmt14 | Stygian Guard | archetype (Claude) | Spell Weakness | 3 | 4 | yes |
| rmt15 | Umbra | signature (library) | eating Morsels for their buffs | 5 | 14 | yes |
| rmt16 | Umbra | signature (library) | units fed to other units | 4 | 16 | yes |
| rmt17 | Umbra | archetype (Claude) | Morsels | 10 | 25 | yes |
| rmt18 | Umbra | archetype (Claude) | Damage Shield | 4 | 7 | yes |
| rmt19 | Umbra | archetype (Claude) | Emberdrain | 3 | 4 | yes |
| rmt20 | Melting Remnant | signature (library) | death abilities | 6 | 15 | yes |
| rmt21 | Melting Remnant | signature (library) | Reform | 4 | 6 | yes |
| rmt22 | Melting Remnant | signature (library) | Burnout | 6 | 17 | yes |
| rmt23 | Melting Remnant | signature (library) | Harvest | 3 | 5 | yes |
| rmt24 | Wurmkin | signature (library) | Echo powers cards | 8 | 22 | yes |
| rmt25 | Wurmkin | archetype (Claude) | Extract | 6 | 10 | yes |
| rmt26 | Wurmkin | archetype (Claude) | Consume | 10 | 15 | yes |
| rmt27 | Wurmkin | archetype (Claude) | Reap | 5 | 8 | yes |
| rmt28 | Wurmkin | archetype (Claude) | Eggs and Shell | 3 | 5 | yes |

## Guide decks (the explanation must say what the guide says)

| case | deck | must say | missing | pass |
|---|---|---|---|---|
| dmt01 | Imp build (Shardtail Queen) | Imp cards;Transcendimp makes these cards' effects happen again: Impish Scholar, Queen's Impling | - | yes |
| dmt02 | Frostbite build (Tethys) | get frostbite: made by Crystalline Seeds, Glacial Seal, Tethys Titansbane, Titan Sentry, Titanstooth. Use it: Hoarfrost Effigy | - | yes |
| dmt03 | Morsel build (Penumbra) | Morsel cards;Eats: made by Morsel Miner. Use it: Penumbra | - | yes |
| dmt04 | Burnout and Reform build (Rector Flicker) | Your units die: made by Crushing Demise, Molded. Use it: Rector Flicker | - | yes |
| dmt05 | Stygian and Awoken spells (Solgard) | Spells you play: Awoken's Rail Spike, Glimmer, Razorsharp Edge, Rootseeds, Steel Enhancer. Set off: Solgard the Martyr | - | yes |
| dmt06 | Hellhorned rage | get rage: made by;Use it: Deranged Brute | - | yes |
| dmt07 | Hellhorned armor | get armor: made by;Use it: Battering Ram | - | yes |

## Deck networks (a line must be there, or must not)

| case | deck | from | to | expect | found | pass |
|---|---|---|---|---|---|---|
| n40 | Imp build (Shardtail Queen) | Queen's Impling | Transcendimp | none repeats | - | yes |
| n41 | Frostbite build (Tethys) | Crystalline Seeds | Tethys Titansbane | none  | - | yes |
| n42 | Frostbite build (Tethys) | Tethys Titansbane | Titan Sentry | none Frostbite | - | yes |

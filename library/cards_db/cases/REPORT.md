# Case tests: monster_train

Made by `cases/run.py monster_train`.
**149 of 149 cases pass.**


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
| mt10 | Resolve triggers | 8 | 8 | 100% | 8 | yes |
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

## Combos (the enabler must set off the payoff)

| case | enabler | payoff | why | found as | pass |
|---|---|---|---|---|---|
| cmt01 | Fledgling Imp | Deranged Brute | Rage on friendly units hits harder with the Brute | target: keyword Rage | yes |
| cmt02 | Rage Serum | Last Stand | Rage to double | keyword: Rage | yes |
| cmt03 | Ritual of Battle | Last Stand | Rage to double | keyword: Rage | yes |
| cmt04 | Fortify | Battering Ram | Armor turns into damage | keyword: Armor | yes |
| cmt05 | Steelworker | Battering Ram | Armor turns into damage | keyword: Armor | yes |
| cmt06 | Alloy of the Ancients | Reinforce | Armor to double | keyword: Armor | yes |
| cmt07 | Welder Helper | Apex Imp | Armor added gives the Apex Imp Rage | keyword: Armor | yes |
| cmt08 | Fledgling Imp | Imp-portant Work | an Imp to sacrifice | target: type Imp | yes |
| cmt09 | Molting Imp | Transcendimp | Summon effects to repeat | trigger keyword: Summon | yes |
| cmt10 | Queen's Impling | Consumer of Crowns | Imps in play make it cheaper | type: Imp | yes |
| cmt11 | Pyre Shards | Bramble Lash | Spikes turn into damage | keyword: Spikes | yes |
| cmt12 | Sharpen | Shard Channeler | Spikes deal more per stack | target: keyword Spikes | yes |
| cmt13 | Restore | Thorned Hollow | healing triggers Rejuvenate | event: heal -> healed | yes |
| cmt14 | Glimmer | Steelsinger | healing triggers Rejuvenate | event: heal -> healed | yes |
| cmt15 | Engraft | Awoken Hollow | healing triggers Rejuvenate | event: heal -> healed | yes |
| cmt16 | Sting | Siren of the Sea | spells trigger Incant | is: playing Sting is a played the payoff waits for | yes |
| cmt17 | Crystalline Seeds | Hoarfrost Effigy | Frostbite to gather and double | keyword: Frostbite | yes |
| cmt18 | Titanstooth | Hoarfrost Effigy | Frostbite to gather and double | keyword: Frostbite | yes |
| cmt19 | Molluscmage | Ice and Pyre | Magic Power counts five times with Attuned | target: keyword Magic Power | yes |
| cmt20 | Harness the Titan | Ice and Pyre | Magic Power counts five times with Attuned | target: keyword Magic Power | yes |
| cmt21 | Offering Token | Crypt Builder | discarding plays the Offering | event: discard -> discarded | yes |
| cmt22 | Drain | Titanstooth | a random discard can hit the Offering | event: discard -> discarded | yes |
| cmt23 | Deep Offering | Guardian's Amulet | discarding the hand plays the Offering | event: discard -> discarded | yes |
| cmt24 | Frenzied Swarm | Crypt Builder | discarding the hand plays the Offering | event: discard -> discarded | yes |
| cmt25 | Rubble Morsel | Overgorger | a Morsel to eat grows it | type: Morsel | yes |
| cmt26 | Packed Morsels | Crucible Warden | Morsels to eat give Damage Shield | type: Morsel | yes |
| cmt27 | Morselmaker | Morsel-Made | Morsels with Eaten for Hunger | is: playing Morselmaker is a summoned the payoff waits for | yes |
| cmt28 | Cannibalize | Penumbra | Morsels for Penumbra to Gorge on | type: Morsel | yes |
| cmt29 | Morselmaker | Penumbra | Morsels for Penumbra | type: Morsel | yes |
| cmt30 | Dreg | Hallowed Drippings | a Burnout unit to extend | event: countdown_advance -> countdown_done | yes |
| cmt31 | Wicklash | Paraffin Enforcer | Burnout units gain Rage | target: keyword Burnout | yes |
| cmt32 | Entombed Explosive | Intent on Death | an Extinguish ability to trigger | trigger keyword: Extinguish | yes |
| cmt33 | Devourer of Death | Intent on Death | an Extinguish ability to trigger | trigger keyword: Extinguish | yes |
| cmt34 | Crushing Demise | Wickless Baron | a death on the floor triggers Harvest | event: kill -> dies | yes |
| cmt35 | Crushing Demise | Memento Mori | friendly deaths raise the damage | condition: kill -> dies | yes |
| cmt36 | Molded | Rector Flicker | returns the fallen Flicker by Reform | event: kill -> dies | yes |
| cmt37 | Crushing Demise | Rector Flicker | deaths feed the Accumulator Harvest | event: kill -> dies | yes |
| cmt38 | Bounding Echoes | Keeper of Echoes | Infused cards add Echo for Inspire | event: mana_gain -> resource_gained | yes |
| cmt39 | Returned Soul | Shardsoul Carver | an Infused card adds Echo for Inspire | event: mana_gain -> resource_gained | yes |
| cmt40 | Unearthed Remains | Echo Break | Echo raises the damage | count: lane_resource | yes |
| cmt41 | Soul Siphon | Ancient Resonance | Echo raises the damage | count: lane_resource | yes |
| cmt42 | Accelerated Incubation | Bog Chrysalis | removing Shell hatches the Egg | acts on its keyword: Shell | yes |
| cmt43 | Rage Serum | First of Kin | a Consumed card triggers Etch | event: exhaust -> exhausted | yes |
| cmt44 | Dante's Candle | Dante the Deceptive | Blight cards give Multistrike | type: Blight | yes |

## Region identity (signature, splash, archetype)

| case | region | kind | mechanic | need | found | pass |
|---|---|---|---|---|---|---|
| rmt01 | Hellhorned | signature (library) | Multistrike | 2 | 3 | yes |
| rmt02 | Hellhorned | signature (library) | Rage | 8 | 11 | yes |
| rmt03 | Hellhorned | signature (library) | Imps | 8 | 14 | yes |
| rmt04 | Hellhorned | archetype (Claude) | Armor | 8 | 12 | yes |
| rmt05 | Hellhorned | archetype (Claude) | Summon triggers | 6 | 31 | yes |
| rmt06 | Awoken | signature (library) | Sweep | 3 | 3 | yes |
| rmt07 | Awoken | archetype (Claude) | Spikes | 6 | 7 | yes |
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
| rmt22 | Melting Remnant | signature (library) | Burnout | 6 | 16 | yes |
| rmt23 | Melting Remnant | signature (library) | Harvest | 3 | 5 | yes |
| rmt24 | Wurmkin | signature (library) | Echo powers cards | 8 | 22 | yes |
| rmt25 | Wurmkin | archetype (Claude) | Extract | 6 | 10 | yes |
| rmt26 | Wurmkin | archetype (Claude) | Consume | 10 | 15 | yes |
| rmt27 | Wurmkin | archetype (Claude) | Reap | 5 | 8 | yes |
| rmt28 | Wurmkin | archetype (Claude) | Eggs and Shell | 3 | 5 | yes |

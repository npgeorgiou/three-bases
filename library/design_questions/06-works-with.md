# What works well with this mechanic? (damage over time)

`ask.py all feeds damage_over_time`

```
on_kill: monster_train 308 pairs, e.g. Olde Magic -> Little Fade; stormbound 6 pairs, e.g. Acid Greenhorns -> Spellbinder Zhevana; sts1 78 pairs, e.g. Catalyst -> Hand of Greed
on_damaged: into_the_breach 384 pairs, e.g. Thermal Discharger -> Fire; stormbound 68 pairs, e.g. Toxic Sacrifice -> Greenwood Ancients
other_death_trigger: monster_train 125 pairs, e.g. Olde Magic -> Big Sludge; sts1 37 pairs, e.g. Deadly Poison -> The Specimen
shop_gold: monster_train 74 pairs, e.g. Spike of the Stygian -> Olde Magic; sts1 27 pairs, e.g. Catalyst -> Hand of Greed
immunity: into_the_breach 164 pairs, e.g. Forest Tile -> Critical Shields; monster_train 7 pairs, e.g. Titanstooth -> Solgard the Martyr
death_trigger: into_the_breach 20 pairs, e.g. Forest Tile -> Marked tile; stormbound 81 pairs, e.g. Acid Greenhorns -> Green Prototypes
base_resource_gain: into_the_breach 10 pairs, e.g. Forest Tile -> Mafan; sts1 164 pairs, e.g. Catalyst -> Gremlin Horn
area_templates: stormbound 4 pairs, e.g. Acid Greenhorns -> Temple of Life
shield: into_the_breach 160 pairs, e.g. Forest Tile -> Critical Shields
damage: sts1 296 pairs, e.g. Deadly Poison -> The Specimen
friendly_fire: into_the_breach 131 pairs, e.g. Thermal Discharger -> Fire
turn_start: stormbound 33 pairs, e.g. Acid Greenhorns -> Function Wilds; sts1 259 pairs, e.g. Deadly Poison -> The Specimen
```

`ask.py all together damage_over_time`

```
turn_start: into_the_breach 12 cards, monster_train 2 cards, stormbound 6 cards, sts1 13 cards
damage: into_the_breach 11 cards, monster_train 22 cards, stormbound 6 cards, sts1 13 cards
ping: into_the_breach 11 cards, stormbound 6 cards
aoe_damage: into_the_breach 5 cards, monster_train 15 cards, stormbound 2 cards, sts1 4 cards
terrain: into_the_breach 11 cards
turn_end: monster_train 22 cards
other_death_trigger: sts1 2 cards
count_payoff: monster_train 22 cards, sts1 13 cards
on_lifegain: into_the_breach 12 cards
lanes: into_the_breach 2 cards, monster_train 16 cards
positional: into_the_breach 12 cards, monster_train 17 cards, stormbound 3 cards
friendly_fire: into_the_breach 3 cards, stormbound 2 cards
```

# What works well with this mechanic? (damage over time)

`ask.py all feeds damage_over_time`

```
on_kill: monster_train 294 pairs, e.g. Glugsider -> Hornbreaker Prince; stormbound 6 pairs, e.g. Toxic Sacrifice -> Spellbinder Zhevana; sts1 78 pairs, e.g. Noxious Fumes -> Hand of Greed
turn_start: into_the_breach 111 pairs, e.g. Thermal Discharger -> Fire; stormbound 31 pairs, e.g. Acid Greenhorns -> Function Wilds; sts1 259 pairs, e.g. Noxious Fumes -> The Specimen
other_death_trigger: monster_train 120 pairs, e.g. Kinhost Vessel -> Memories of the Melted; sts1 37 pairs, e.g. Noxious Fumes -> The Specimen
on_damaged: into_the_breach 398 pairs, e.g. Thermal Discharger -> Fire; stormbound 68 pairs, e.g. Toxic Sacrifice -> Earthfathers
shop_gold: monster_train 63 pairs, e.g. Kinhost Vessel -> Paraffin Thug; sts1 27 pairs, e.g. Noxious Fumes -> Hand of Greed
aoe_damage: into_the_breach 143 pairs, e.g. Thermal Discharger -> Fire; sts1 33 pairs, e.g. Noxious Fumes -> Corpse Explosion
generate_cards: into_the_breach 10 pairs, e.g. Forest Tile -> Marked tile; monster_train 59 pairs, e.g. Titanstooth -> Shardtail Queen
death_trigger: into_the_breach 20 pairs, e.g. Forest Tile -> Ice Tile; stormbound 81 pairs, e.g. Acid Greenhorns -> Green Prototypes
base_resource_gain: into_the_breach 10 pairs, e.g. Forest Tile -> Mafan; sts1 164 pairs, e.g. Noxious Fumes -> Gremlin Horn
area_templates: stormbound 4 pairs, e.g. Acid Greenhorns -> Temple of Life
damage: sts1 296 pairs, e.g. Noxious Fumes -> The Specimen
copy: monster_train 32 pairs, e.g. Echowright -> Morselmaster; stormbound 8 pairs, e.g. Acid Greenhorns -> Temple of Life
```

`ask.py all together damage_over_time`

```
turn_start: into_the_breach 12 cards, stormbound 6 cards, sts1 13 cards
damage: into_the_breach 11 cards, monster_train 21 cards, stormbound 6 cards, sts1 13 cards
ping: into_the_breach 11 cards, stormbound 6 cards
aoe_damage: into_the_breach 5 cards, monster_train 15 cards, stormbound 2 cards, sts1 4 cards
terrain: into_the_breach 11 cards
turn_end: monster_train 21 cards
other_death_trigger: sts1 2 cards
count_payoff: monster_train 21 cards, sts1 13 cards
on_lifegain: into_the_breach 12 cards
immunity: into_the_breach 2 cards
lanes: into_the_breach 2 cards, monster_train 15 cards
positional: into_the_breach 12 cards, monster_train 16 cards, stormbound 3 cards
```

# What works well with this mechanic? (damage over time)

`ask.py all feeds damage_over_time`

```
on_kill: monster_train 294 pairs, e.g. Glugsider -> Hornbreaker Prince; stormbound 6 pairs, e.g. Copperskin Ranger -> Spellbinder Zhevana; sts1 78 pairs, e.g. Catalyst -> Feed
other_death_trigger: monster_train 120 pairs, e.g. Glugsider -> Wickless Baron; sts1 37 pairs, e.g. Catalyst -> The Specimen
on_damaged: into_the_breach 396 pairs, e.g. Thermal Discharger -> Fire; stormbound 68 pairs, e.g. Toxic Sacrifice -> Lunatic Lunas
shop_gold: monster_train 63 pairs, e.g. Glugsider -> Paraffin Thug; sts1 27 pairs, e.g. Catalyst -> Golden Idol
immunity: into_the_breach 165 pairs, e.g. Forest Tile -> Critical Shields; monster_train 6 pairs, e.g. Spike of the Stygian -> Solgard the Martyr
generate_cards: into_the_breach 10 pairs, e.g. Forest Tile -> Marked tile; monster_train 59 pairs, e.g. Titanstooth -> Wyldenten
death_trigger: into_the_breach 20 pairs, e.g. Forest Tile -> Ice Tile; stormbound 81 pairs, e.g. Acid Greenhorns -> Green Prototypes
base_resource_gain: into_the_breach 10 pairs, e.g. Forest Tile -> Mafan; sts1 164 pairs, e.g. Catalyst -> Gremlin Horn
area_templates: stormbound 4 pairs, e.g. Acid Greenhorns -> Temple of Life
turn_start: stormbound 31 pairs, e.g. Acid Greenhorns -> Big Sisters of Growth; sts1 259 pairs, e.g. Catalyst -> The Specimen
shield: into_the_breach 161 pairs, e.g. Forest Tile -> Critical Shields
damage: sts1 296 pairs, e.g. Catalyst -> The Specimen
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
lanes: into_the_breach 2 cards, monster_train 15 cards
positional: into_the_breach 12 cards, monster_train 16 cards, stormbound 3 cards
attack_now: monster_train 7 cards
```

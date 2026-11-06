# What works well with this mechanic? (damage over time)

`ask.py all feeds damage_over_time`

```
on_kill: gwent 1948 pairs, e.g. Oakcritters -> Nature's Rebuke; monster_train 308 pairs, e.g. Olde Magic -> Little Fade; stormbound 6 pairs, e.g. Toxic Sacrifice -> Spellbinder Zhevana; sts1 78 pairs, e.g. Catalyst+ -> Hand of Greed
lifesteal: gwent 47 pairs, e.g. Svalblod Butcher -> Regis: Reborn; stormbound 16 pairs, e.g. Acid Greenhorns -> Plague Monarchs
other_death_trigger: gwent 422 pairs, e.g. Savage Bear -> Blood Money; monster_train 125 pairs, e.g. Olde Magic -> Big Sludge; sts1 37 pairs, e.g. Envenom -> The Specimen
on_damaged: into_the_breach 384 pairs, e.g. Thermal Discharger -> Fire; stormbound 68 pairs, e.g. Toxic Sacrifice -> Greenwood Ancients
shop_gold: monster_train 74 pairs, e.g. Spike of the Stygian -> Olde Magic; sts1 27 pairs, e.g. Catalyst+ -> Hand of Greed
immunity: into_the_breach 164 pairs, e.g. Forest Tile -> Critical Shields; monster_train 7 pairs, e.g. Titanstooth -> Solgard the Martyr
death_trigger: into_the_breach 20 pairs, e.g. Forest Tile -> Ice Tile; stormbound 81 pairs, e.g. Acid Greenhorns -> Green Prototypes
base_resource_gain: into_the_breach 10 pairs, e.g. Forest Tile -> Mafan; sts1 164 pairs, e.g. Catalyst+ -> Gremlin Horn
damage: gwent 5167 pairs, e.g. Savage Bear -> Blood Money; sts1 296 pairs, e.g. The Specimen -> Sadistic Nature
area_templates: stormbound 4 pairs, e.g. Acid Greenhorns -> Temple of Life
turn_start: gwent 1041 pairs, e.g. Making a Bomb -> Madoc; stormbound 33 pairs, e.g. Acid Greenhorns -> Big Sisters of Growth; sts1 259 pairs, e.g. Envenom -> The Specimen
shield: into_the_breach 160 pairs, e.g. Forest Tile -> Critical Shields
```

`ask.py all together damage_over_time`

```
ping: gwent 46 cards, into_the_breach 11 cards, stormbound 6 cards
turn_start: gwent 2 cards, into_the_breach 12 cards, monster_train 2 cards, stormbound 6 cards, sts1 13 cards
damage: gwent 46 cards, into_the_breach 11 cards, monster_train 22 cards, stormbound 6 cards, sts1 13 cards
turn_end: gwent 46 cards, monster_train 22 cards
aoe_damage: into_the_breach 5 cards, monster_train 15 cards, stormbound 2 cards, sts1 4 cards
terrain: into_the_breach 11 cards
other_death_trigger: sts1 2 cards
count_payoff: gwent 8 cards, monster_train 22 cards, sts1 13 cards
on_lifegain: into_the_breach 12 cards
positional: gwent 20 cards, into_the_breach 12 cards, monster_train 17 cards, stormbound 3 cards
lanes: into_the_breach 2 cards, monster_train 16 cards
friendly_fire: into_the_breach 3 cards, stormbound 2 cards
```

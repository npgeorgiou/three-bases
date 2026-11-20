# Cards whose rows say "can <event>" (the card may do something normally forbidden)

## event=summoned game=faeria side=- who=self to=position
- **Khalim's Skyguard** (faeria). Text: "Flying Can be summoned adjacent to friendly creatures."
  Rows: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN always DO can self to position [position is bordering] (event=summoned) for while
- **Twinsoul Spirit** (faeria). Text: "Flying Can be summoned adjacent to friendly creatures. Gift - Summon another Twinsoul Spirit."
  Rows: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN always DO can self to position [position is bordering] (event=summoned) for while | WHEN played of self DO summon <Twinsoul Spirit>

## event=None game=runeterra side=mine who=all to=-
- **Out Of The Way** (runeterra). Text: "For the rest of the game, allied "this round" buffs (except Barrier) are permanent. Draw 1."
  Rows: WHEN played of self DO can all mine unit [state is buffed] [keyword not Barrier] for permanent THEN draw mine card in deck_top (amount=1)

## event=moves game=marvel_snap side=- who=all to=-
- **Jean Grey School** (marvel_snap). Text: "On turn 5, cards here are Moveable."
  Rows: WHEN always IF event_count round_start eq 5 this_game DO can all unit in board [position is same_lane] (event=moves) for while
- **Incursion Event** (marvel_snap). Text: "On Reveal: Replace this location with a new one. Next turn, all cards here are Moveable."
  Rows: KW: On Reveal | WHEN played of self DO set_terrain position [position is same_lane] to random position THEN can all unit in board [position is same_lane] (event=moves) for next_round

## event=moves game=marvel_snap side=- who=all to=position
- **New York** (marvel_snap). Text: "On turn 6, cards are Moveable to here."
  Rows: WHEN always IF event_count round_start eq 6 this_game DO can all unit in board to position [position is same_lane] (event=moves) for while
- **Cloak** (marvel_snap). Text: "On Reveal: Next turn, all cards are Moveable to this location."
  Rows: KW: On Reveal | WHEN played of self DO can all unit in board to position [position is same_lane] (event=moves) for next_round

## event=None game=runeterra side=mine who=- to=-
- **Restored Sun Disc** (runeterra). Text: "Keywords: Landmark. Immediately draw 1 of each of your Ascended allies. For the rest of the game, your level 2 Ascended allies are level 3."
  Rows: KW: Landmark | WHEN played of self DO draw mine card in deck [type is Ascended] (amount=distinct card of (mine card in deck [type is Ascended])) | WHEN always DO can mine unit [type is Ascended] for while

## event=None game=duelyst side=- who=self to=-
- **Grandmaster Z'ir** (duelyst). Text: "When your General dies, Grandmaster Z'ir becomes your General."
  Rows: WHEN dies of mine player DO become_leader self

## event=played game=duelyst side=- who=self to=-
- **Grand Strategos** (duelyst). Text: "Trial: Summon 12 minions with 1 or less Attack. Destiny: Promote other friendly minions at the end of your turn."
  Rows: WHEN always IF event_count summoned of mine unit [power le 1] ge 12 this_game DO can self (event=played) for permanent | WHEN turn_end by mine player DO transform all mine unit in board [card not Grand Strategos] to random unit [region is Lyonar Kingdoms] [cost eq sum (stat cost of (it) + 1)]
- **Hideatsu the Ebon Ox** (duelyst). Text: "Trial: Summon 7 minions from your action bar with different costs. Destiny: Summon friendly minions to deal their cost as damage to an enemy."
  Rows: WHEN always IF amount distinct cost of (played of mine unit) this_game ge 7 DO can self (event=played) for permanent | WHEN summoned of mine unit DO damage chosen enemy any (amount=stat cost of (it))

## event=None game=duelyst side=enemy who=it to=-
- **Soulstealer** (duelyst). Text: "Whenever the enemy General plays a minion, it becomes their new General. Whenever Soulstealer dies, he inhabits the body of one of his minions."
  Rows: WHEN played by enemy player of enemy unit DO become_leader it | WHEN dies of self DO transform self to chosen mine unit in board

## event=attacks game=into_the_breach side=- who=self to=position
- **Flame Thrower** (into_the_breach). Text: "Push target tile and light tiles on Fire. Damage units already on Fire. (Starts with 1 range.) Damage: 2. Power: Free. Upgrades: +1 Range (1 Reactor Core): Extends flamethrower range by 1 tile; +1 Range (3 Reactor Cores): Extends flamethrower range by 1 tile."
  Rows: WHEN attacks by self DO damage all unit_or_structure [position is straight_line] [distance le 1] [keyword is Fire] (amount=2) THEN move chosen unit_or_structure [position is straight_line] [distance le 1] to position [position is bordering] THEN give_keyword all position [position is straight_line] [distance le 1] <Fire> for permanent | WHEN attacks by self IF upgraded 1 DO can self to position [position is straight_line] [distance le 2] (event=attacks) for while | WHEN attacks by self IF upgraded 2 DO can self to position [position is straight_line] [distance le 3] (event=attacks) for while
- **Prime Spear** (into_the_breach). Text: "Stab multiple tiles and push the furthest hit tile. (Starts with 2-tile range.) Damage: 2. Power: 1 Reactor Core. Upgrades: A.C.I.D. Tip (1 Reactor Core): Adds A.C.I.D. to the furthest hit enemy; +1 Range (2 Reactor Cores): Increases the maximum number of hit tiles by 1."
  Rows: WHEN attacks by self DO damage all unit_or_structure [position is straight_line] [distance le 2] (amount=2) THEN move highest unit_or_structure by distance [position is straight_line] [distance le 2] to position [position is bordering] | WHEN attacks by self IF upgraded 1 DO give_keyword highest enemy unit by distance [position is straight_line] [distance le 2] <A.C.I.D.> for permanent | WHEN attacks by self IF upgraded 2 DO can self to position [position is straight_line] [distance le 3] (event=attacks) for while

## event=attacks game=into_the_breach side=- who=self to=-
- **Push Beam** (into_the_breach). Text: "Pushes all units in a line. Single-use. Power: Free. Upgrades: Unlimited Use (1 Reactor Core): Removes use restriction in battles."
  Rows: WHEN attacks by self [once_per_game] DO move all unit [position is straight_line] to position [position is bordering] | WHEN attacks by self IF upgraded 1 DO can self (event=attacks) for while
- **Wind Torrent** (into_the_breach). Text: "Push all units in a single direction. Single-use. Power: Free. Upgrades: Unlimited Uses (1 Reactor Core): Removes use restriction in battles."
  Rows: WHEN attacks by self [once_per_game] DO move all unit to position [position is bordering] | WHEN attacks by self IF upgraded 1 DO can self (event=attacks) for while

## event=played game=sts1 side=mine who=all to=-
- **Blue Candle** (sts1). Text: "Unplayable Curse cards can now be played. Whenever you play a Curse, lose 1 HP and Exhaust it."
  Rows: WHEN always DO can all mine card [type is Curse] [keyword is Unplayable] (event=played) for while | WHEN played of mine spell [type is Curse] DO damage mine player (amount=1) THEN exhaust it
- **Medical Kit** (sts1). Text: "Unplayable Status cards can now be played. Whenever you play a Status card, Exhaust it."
  Rows: WHEN always DO can all mine card [type is Status] (event=played) for permanent | WHEN played of mine spell [type is Status] DO exhaust it
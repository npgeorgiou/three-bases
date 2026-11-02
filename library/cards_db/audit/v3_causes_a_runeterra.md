# Runeterra whole-game check: causes

## Causes (7)

1. A made card is linked to a need that filters by kind, but the made card is not that kind (L20, L17).
   Wrong thinking: "creates cards -> more different cards to play". Angel makes Coins; The World Ender counts only Darkin played.
   - Angel -> The World Ender
     The World Ender: ... distinct card of (played by mine player of any [type is Darkin] [card not Aatrox]) ...

2. A draw or put-into-hand line goes to a level-2 form, which can never be drawn (L9: lines link only cards a player can own).
   Wrong thinking: "draws it and keeps it" applied to a card that only exists by levelling up.
   - Realm Warp -> Elder Dragon (level 2)
     Elder Dragon (level 2): KW: Fury   (no text; also cannot be in a deck)

3. An effect on enemies feeds a need about my own cards (L9).
   Wrong thinking: "makes you discard cards" for a card that makes the ENEMY discard.
   - Early Bird -> Noble Rebel
     Early Bird: ... DO discard highest_cost enemy card in hand
     Noble Rebel: ... event_count discarded by mine player ge 3 ...

4. A card with no text of its own (only the Equipment keyword) is given an act it does not do (L1, L15: a keyword's inner working is not the card's act).
   Wrong thinking: "Bone Club makes cards leave play". Its rows only say Equipment; it makes nothing leave play.
   - Bone Club -> Quick Quill (created)
     Bone Club: KW: Equipment
     Quick Quill (created): ... WHEN leaves_play of attached_to DO keyword_action self <Recall>
   (The other Equipment "targets" lines are in the unsure list.)

5. Plain stat help (more power/health) goes to a card whose text does not read stats (L14, L18).
   Wrong thinking: "stronger" is a need. Neither target reads power or health, has Taunt, or waits to survive damage.
   - Battlesmith -> Cithria of Cloudfield   (Cithria: no rows)
   - Bayou Brunch -> Barkbeast
     Barkbeast: WHEN dies of mine unit in board [once_per_game] DO stat_change self (power=2, health=2) for permanent
     (also: Bayou Brunch captures the unit, it does not make it die, and the reason says "Health it grows into Health", which Barkbeast does not use)

6. The Countdown keyword's own working is read as one landmark feeding another (L15).
   Stormcarved Spire's "WHEN countdown_done" has the same shape as Buried Armory's, which is clearly its own countdown. Another landmark's countdown does not finish Spire's.
   - Buried Armory -> Stormcarved Spire
     Buried Armory: KW: Landmark, Countdown | WHEN countdown_done DO create in hand <Treasure of the Sands>
     Stormcarved Spire: KW: Landmark, Countdown | WHEN countdown_done DO copy it mine unit in attached in board

7. Board-position thinking from other games is used in Runeterra (L4: a help must do the very thing needed).
   Wrong thinking: "moves it within reach of the enemy player". Swapping two allies' places does not get any unit past blockers or to the Nexus.
   - Syncopation -> Acorn, the Hextechnician
     Syncopation: WHEN played of self DO swap 2 chosen mine unit in board
     Acorn: KW: Elusive | WHEN strikes_nexus by self ...

## Unsure
- Equipment attach read as "targeting my unit" (needs the Equipment entry rows): Bone Club -> Retired Reckoner; Bone Club -> Morgana; Corrupted Form -> Pantheon (level 2); Corrupted Form -> Arrel the Tracker; Corrupted Form -> Arbiter of the Peak; Corrupted Form -> Grappling Hook. If attach is not a target, all are wrong (same cause as 4).
- Bouncer & Bolt (Challenger, Impact) -> Ye Been Warned / Ezreal "targets enemy cards": Challenger forces a block and does not target; depends on what Impact does.
- Absorb Soul only Drains 4 (damage) from my own unit; it kills only if health is 4 or less (L11: plain damage is no kill). Affects Absorb Soul -> Chronoshift, Scuttlegeist, Scribe of Sorrows, Burgeoning Sentinel.
- Arrel the Tracker -> Twisted Catalyzer: Catalyzer's trigger is its own strike; the ability it gives is not shown, so Arrel's strike may not feed it.
- Greathorn Companion (Scout only) -> Bitsy Lizard "damages the enemy player": Scout adds an attack (L2 allows) but the card itself has no text that reaches the Nexus.
- Crystal Ibex -> Acorn: Overwhelm given to a unit that already has Elusive adds little.
- Arachnoid Horror -> Insightful Investigator: Investigator needs a cost 2 card; cost of Horror not shown.
- Ghastly Band (Hallowed, Ephemeral) -> Kindred "helps my units kill": nothing in the rows helps kill.
- Double Trouble -> Vanguard Squire: Double Trouble summons random cost 1 followers; Squire needs an Elite (L20); not shown they are.
- Darkwater Scourge -> Crawling Sensation: Ephemeral dies at round end, after which "this round" no longer allows playing the spell.
- Accelerated Purrsuit -> Passage Unearned: Passage Unearned obliterates ALL summoned units, so my own summon is a drawback, not a need (L5, L9).
- Seraphine (level 2) -> Ancient Malediction: repeat needs a created cost 2 or less spell; Malediction's cost and origin not shown.

## Clearly right
- Inspiring Marshal -> Dragonling (Lifesteal gets something back from the extra damage, L18)
- The Dreadway -> Dragonling (doubles damage; Lifesteal reads it, L18)
- Avalanche -> Thrall Bulwark (damage by my spell is what its negate waits for)
- Affectionate Poro -> Molten Shield (Challenger makes a blocking enemy that Shield hits)
- Angel -> Curious Shellfolk (Shellfolk waits for created cards; Angel creates 3 Coins)
- Also right: Senna (level 2) -> Avalanche (Fast for damage spells); Allay (created) -> Legion General (counts keywords given)

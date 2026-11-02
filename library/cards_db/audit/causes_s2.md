# sts1 deck check: causes (d_sts1.txt)

Read: lines 1-1950; not read: none.

## Cause 1: "puts it into play" said for a card only put into hand, deck or discard (L10)
Wrong thinking: making, drawing or returning a card is said as "puts it into play". In Slay the Spire these cards go to hand, draw pile or discard pile and are not played. The reason words should say where the card goes.
- Blade Dance -> Shiv: puts it into play: creates
- Pray -> Insight: puts it into play: creates (shuffled into the draw pile)
- Scrape -> Claw: puts it into play: draws it and keeps it
- All for One -> Overclock: puts it into play: brings it back to your hand
About 28 lines (every "creates", "draws it and keeps it", "brings it back to your hand" line).

## Cause 2: making a drawback card is a line to it (L5)
Wrong thinking: a card that adds a status card that only hurts me "helps" that card. Burn and Void need nothing; being made is their drawback.
- Overclock -> Burn: puts it into play: creates
- TURBO -> Void: puts it into play: creates
2 lines.

## Cause 3: removing enemy Block is linked to every Attack (L14, L18)
Wrong thinking: Melter's "Remove all Block" helps any card that deals damage. None of the receiving cards reads Block or unblocked damage; this is more damage, the game's goal.
- Melter -> Hyperbeam: makes stronger: removes their Block: its damage gets through
- Melter -> Go for the Eyes: makes stronger: removes their Block: its damage gets through
- Melter -> Streamline: makes stronger: removes their Block: its damage gets through
- Melter -> Claw: makes stronger: removes their Block: its damage gets through
5 lines.

## Cause 4: Barricade linked to every card that only gives Block (L14, L18)
Wrong thinking: keeping Block helps every Block card. Defend, Shrug It Off or Anchor only give Block; their text does not use kept Block. Barricade's real partners read the Block total (Body Slam, Entrench).
- Barricade -> Defend (Ironclad): makes stronger: keeps the Block it gives
- Barricade -> Shrug It Off: makes stronger: keeps the Block it gives
- Barricade -> Anchor: makes stronger: keeps the Block it gives
- Barricade -> Feel No Pain: makes stronger: keeps the Block it gives
About 11 lines.

## Cause 5: Snecko Skull said to kill enemies (L3, wrong reason)
Wrong thinking: Snecko Skull adds 1 Poison only when another card applies Poison; it kills nothing alone. To a poison card the right reason is "makes the Poison it gives bigger" (as Snecko Skull -> Bouncing Flask); to The Specimen there is no line of its own.
- Snecko Skull -> Corpse Explosion: triggers: makes enemy units die
- Snecko Skull -> The Specimen: triggers: makes enemy units die
About 4 lines (2 per poison deck).

## Cause 6: one reason said twice in one line (L10)
Wrong thinking: the same act is listed as two kinds of reason. A Power made by Creative AI is also called "a spell"; the right kind is Power and it should be said once.
- Creative AI -> Heatsinks: triggers: is a Power whose playing sets off its effect; also makes a spell whose playing sets off its effect
- Creative AI -> Force Field: enables: makes a spell it needs played for its count; also makes cheaper: is a Power it needs played for its count
- Crescendo -> Rushdown: enables: gives you Wrath; also triggers: gives you Wrath
About 6 lines.

## Cause 7: Dexterity to a card that gives Block several times (L18)
Wrong thinking: a card that gives Block X times gets more from Dexterity. This is the Block twin of "hits several times" (Twin Strike), which L18 says makes no line.
- Kunai -> Reinforced Body: makes stronger: makes the Block it gives bigger
1 line.

## Cause 8 (missing): Pen Nib counts Attacks played but gets no count lines
Pen Nib "Every 10th Attack you play" is a count of Attacks, like Nunchaku ("Every time you play 10 Attacks"), which gets a line from every Attack. Pen Nib gets none in the Shiv and Claw decks (no partner at lines 658 and 1696).
- Missing: Shiv -> Pen Nib, Claw -> Pen Nib, Beam Cell -> Pen Nib (same reason as Shiv -> Nunchaku / Claw -> Nunchaku)
About 10-15 missing lines.

## Unsure
- "Pays for it" uses EXPENSIVE 2 for sts1, so any energy card links to every 2+ cost card (Miracle -> Worship, Charge Battery -> Hyperbeam, Sunder -> Glacier). This may be the "half the cards pass" filter of L21.
- Dropkick -> Corruption / Barricade / Dark Embrace: Dropkick gains energy only if the enemy is Vulnerable, and no card in that deck gives Vulnerable.
- Meteor Strike -> Echo Form etc. "pays for it": the energy comes from the Plasma it channels, not from Meteor Strike's own text.
- Block givers -> Body Slam / Entrench ("gives you Block"): giving Block may be something a quarter of the cards do (L21), as with damage and "whenever damage is dealt".
- Teardrop Locket -> Flurry of Blows / Mental Fortress: starting combat in Calm may not count as changing Stance.
- Watcher Divinity deck: no Mantra card (Worship, Devotion, Prostrate, Pray) links to anything that reads Mantra or Divinity. This may be right, because no card there reads Mantra.

## Must-stay examples (correct)
- Corruption -> Feel No Pain: triggers: exhausts cards
- Inflame -> Heavy Blade: enables: gives you Strength
- Barricade -> Entrench: makes stronger: keeps your Block: it counts more of it
- Burst -> Catalyst: makes stronger: plays it again: its doubling doubles again
- Tempest -> Thunder Strike: enables: uses Lightning

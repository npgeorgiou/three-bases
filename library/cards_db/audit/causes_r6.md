# runeterra, deck check part 1: causes found (r6)

Read: lines 1-1079; not read: lines 1080-3867

I checked the decks Braum Zoe, Annie Gwen, Caitlyn Teemo and Pyke Rek'Sai in full. I read Bard Norra only up to the start of Bard's lines, at line 1079.

## Causes (wrong or extra lines)

### 1. Tybaulk's "spells deal 1 extra damage" is linked to every damage spell (L18)
Wrong thinking: more damage on a spell is treated as a use of the spell's text. L18 says more damage is generic. These spells only deal damage; none of them reads the damage.
- Tybaulk -> Withering Wail: makes stronger: its damage gets 1 more
- Tybaulk -> Decimate: makes stronger: its damage gets 1 more
- Tybaulk -> Magic Embers: makes stronger: its damage gets 1 more
- Tybaulk -> Molten Shield (created): makes stronger: its damage gets 1 more
Count: about 12 lines (all 9 "its damage gets 1 more" lines, plus the same reason inside the Pyroclastic Arrival, Ravenous Flock and Snip Snip Snip! lines).

### 2. Tybaulk is treated as if it damages or kills units itself (L1, L3)
Wrong thinking: Tybaulk's damage boost is read as Tybaulk dealing damage or killing. Tybaulk's text kills nothing and damages nothing. It only grants +1|+0 and boosts spells.
- Tybaulk -> The Harrowing: enables: makes your units die: The Harrowing brings them back
- Tybaulk -> Ceaseless Sentry: triggers: kills it for its death effect
- Tybaulk -> Scorched Earth: enables: damages enemy units or players: Scorched Earth kills them
- Tybaulk -> Ravenous Flock: enables: damages enemy units or players
Count: 5 lines (the 4 above, plus the same "enables" reason in Tybaulk -> Pyroclastic Arrival).

### 3. Any stat change is counted as a "gains Power from Hallowed" trigger or as a stat increase (L15, L4)
Wrong thinking: any change to a unit's stats is taken to set off Gwen's "When another ally gains Power from Hallowed", or to count for Bard's "increased total stats". Both are wrong:
- Tybaulk's +1|+0 does not come from Hallowed.
- Glare's Gloom gives -1|-1, which lowers stats.
- L4: Tybaulk does not level Gwen.

Examples:
- Tybaulk -> Gwen: triggers: changes your units' stats; also makes stronger: gives it more power
- Glare -> Gwen: triggers: changes your units' stats
- Glare -> Gwen (level 2): triggers: changes units' stats (for the ability it gives); also changes your units' stats
- Glare -> Bard: helps it level up: changes your units' stats (levels it up)

Count: 5 lines. In Tybaulk -> Gwen (level 2), only the "triggers" part is wrong; the "more power" part may stay, because Gwen (level 2) reads its own Power.

### 4. Rek'Sai's "Grant Lurker allies +1|+0" is linked to every Lurker (L14, L18, L4)
Wrong thinking: power aimed at a card kind (Lurker allies) is linked to every card of that kind. None of these cards' texts reads power:
- Overwhelm, Fearsome and Quick Attack make no line (L18).
- Pyke's level-up damage is not helped by more power (L4).

Only Xerxa'Reth uses power ("8+ Power"), so only that line is right.
- Rek'Sai -> Jaull-fish: makes stronger: gives it more power
- Rek'Sai -> Xer'sai Dunebreaker: makes stronger: gives it more power
- Rek'Sai (level 2) -> Pyke: makes stronger: gives it more power
- Rek'Sai (level 2) -> Sharkling: makes stronger: gives it more power

Count: 18 lines.

### 5. Every Lurker is linked to Frenzied Feast's "Each Lurker ally strikes" (L14, L1b)
Wrong thinking: a strike aimed at a card kind is taken as a need for that kind. L14 says a strike given to a kind links only to cards whose own text uses a strike ("Strike:", or a "when I kill" effect such as Pyke (level 2)'s). In a Lurk deck, Lurker is no narrower than the deck. Bloodbait and Call the Pack only create Lurkers, so their lines also fall under L1b.
- Sharkling -> Frenzied Feast: enables: is a Lurker it asks for
- Xer'sai Caller -> Frenzied Feast: enables: is a Lurker it asks for
- Call the Pack -> Frenzied Feast: enables: makes a Lurker it asks for
- Xerxa'Reth, The Undertitan -> Frenzied Feast: enables: is a Lurker it asks for

Count: about 13 lines. Pyke (level 2) -> Frenzied Feast may stay ("When I kill an enemy, I strike"), and Jaull-fish's "casts its skill" stays.

### 6. One reason is said twice: "helps it level up" plus "triggers" for the same thing (L10)
Wrong thinking: when a card both levels up from a thing and reacts to it, the reason is printed once per kind. L10 says one reason is said once, by its strongest kind.
- Revna, the Lorekeeper -> Braum: helps it level up: more health or protection: survives damage (levels it up); also triggers: more health or protection: survives damage
- Spirits Unleashed -> Braum: helps it level up: damages it without killing it, for its effect (levels it up); also more health or protection: survives damage (levels it up); also triggers: damages it without killing it, for its effect; also triggers: more health or protection: survives damage
- Blood in the Water -> Rek'Sai: helps it level up: another attack (levels it up); also makes it attack for its effect (levels it up); also triggers: makes it attack for its effect

Count: about 9 lines (all of Braum's inbound buff lines, and Blood in the Water -> Rek'Sai).

### 7. Wrong reason words (L10)
Wrong thinking: the reason names the wrong act. Some examples:
- Manasoul Student's reason says "is played", but the real reason is that it plays Magic Embers, a Skill that the other card counts.
- Volatile Bloom does not make a trap stronger; it activates the traps Corina plants.
- Stat help is not said in the L18 families. "+1|+1" is printed as "more health; also more power" or as "more power" only.

Examples:
- Manasoul Student -> Annie: helps it level up: is played (levels it up)
- Manasoul Student -> Ravenbloom Conservatory: enables: is played
- Volatile Bloom -> Corina, Mastermind: repeats its effects: makes the Trap it gives stronger
- Mihira, Aspect of Justice -> Revna, the Lorekeeper: makes stronger: more health; also more power
- Esmus, Breath of the World -> Mihira, Aspect of Justice: enables: changes its stats for its effect; also makes stronger: more power

Count: about 12 lines.

### 8. Tybaulk -> Snip Snip Snip! through Gwen's power (L3)
Wrong thinking: Tybaulk raises Gwen's power, and Snip Snip Snip! reads Gwen's power. That is A acts on B, B feeds C, so A gets no line to C.
- Tybaulk -> Snip Snip Snip!: makes stronger: its damage gets 1 more; also more power

Count: 1 line.

## Missing lines

### M1. Puffcap planters are not linked to Teemo's level-up or to Teemo (level 2)
- Teemo levels up from "You've planted 15+ Poison Puffcaps".
- Teemo (level 2) doubles the Puffcaps in the enemy deck.

These cards plant Puffcaps but have no line to either Teemo: Puffcap Peddler, Mushroom Cloud, Poison Dart, Ava Achiever, Bursting Backpack. Teemo (level 2) has only 2 partners. About 10 lines are missing.

### M2. Traps, boons and their planters are not linked to Mister Thrift
Mister Thrift says "When one or more of your traps or boons activate". Its only partner is Corina. These are missing:
- Poison Puffcap, Flashbomb Trap and Chime (they activate).
- Volatile Bloom, Mushroom Cloud and the other planters.

Living Library and Proximity Puffcap, which wait for the same thing, do get these lines. About 6 or more lines are missing in Caitlyn Teemo.

### M3. Other Lurkers' Lurk is not linked to Rek'Sai
Rek'Sai levels up from "I've attacked with 10+ Power", so its own text reads its power. That is the same exception L15 makes for Xerxa'Reth, which does get these lines. The Lurk keyword grants Lurker allies +1|+0, but no Lurker -> Rek'Sai line exists. About 10 lines are missing.

### M4. Bone Skewer is not linked to Lurk cards
Bone Skewer says "An ally strikes an enemy, then moves to the top of your deck". Lurk works only "while I'm on top of your deck", so Bone Skewer sets up Lurk for:
- Rek'Sai
- Pyke, whose Lurk transforms it into Death From Below
- Xerxa'Reth and the other Lurk units

Bone Skewer has no partner at all. About 10 lines are missing.

## Unsure
- Sunburst -> Braum (level 2) "damages it without killing it": I am not sure aiming a 6-damage removal spell at your own Braum is a deck choice.
- Ravenous Flock, Scorched Earth, Disintegrate -> Ceaseless Sentry "kills it for its death effect": these are plain removal spells on one unit, used here on my own unit. L14 keeps a sacrifice, but these may not be sacrifice cards.
- Proximity Puffcap -> Junk Construct "kills it for its death effect": the same doubt as the line above.
- The Harrowing -> Ceaseless Sentry "kills it": the kill comes only from the Ephemeral it grants. The reason may be right, but it is worded as a kill.
- Braum / Braum (level 2) -> Zoe (level 2) "puts your units into play": the summon effect is one Zoe (level 2) gives to the Nexus. I am not sure it counts as Zoe's own text.
- Annie and Ravenbloom Conservatory count "Fast spells, Slow spells, or Skills". The database texts show no spell speed (no Fast or Slow keyword on Decimate, Vile Feast, Glimpse Beyond and others), so these spells may be missing lines to Annie, Ravenbloom Conservatory and Manasoul Student. I could not check their speed from the data.

## Correct lines (must stay, usable as tests)
- Braum -> Mighty Poro: puts it into play: summons
- Glimpse Beyond -> Ceaseless Sentry: triggers: kills it for its death effect
- Molten Shield (created) -> Ravenous Flock: enables: makes enemy units get Stun
- Blood in the Water -> Xerxa'Reth, The Undertitan: triggers: makes it attack for its effect (the Rally part)
- Esmus, Breath of the World -> Chime: puts it into play: plants

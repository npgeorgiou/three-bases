# Runeterra deck check, part r7: causes

Read: lines 3868-5067; not read: lines 5068-7602

## Causes (sure from both card texts)

1. **Damage boosts linked to every damage card (and to cards that deal no damage).** "Your spells deal 1 more / double damage" is more damage, which is generic. Breaks L18 (and LINKS_PLAN gives_lines: more damage alone is never a use). Lines to Scorched Earth (kills, deals no damage) and Paralyzing Bite (Stun only) have no use at all.
   - Powder Keg -> Death's Hand: makes stronger: makes its effect bigger
   - Powder Keg -> Scorched Earth: makes stronger: makes its effect bigger
   - Powder Keg -> Paralyzing Bite: makes stronger: makes its effect bigger
   - The Dreadway -> Decimate: makes stronger: doubles its damage
   - Count: about 15 (Powder Keg 10 "makes its effect bigger", The Dreadway 5 "doubles its damage").

2. **A card that deals no damage by its text is said to "damage enemy units" or "more damage" for a kill-a-damaged-unit card.** Might only gives +3|+0 and Overwhelm; The Dreadway only doubles damage. Breaks L1 / L4 / L18.
   - Might -> Scorched Earth: enables: more damage
   - The Dreadway -> Scorched Earth: enables: damages enemy units or players: Scorched Earth kills them
   - The Dreadway -> Ravenous Flock: enables: damages enemy units or players; also makes stronger: doubles its damage
   - Count: about 3.

3. **"Helps it hit the enemy player" said for the giver's OWN keyword, or for a card with no such keyword.** Farron's Overwhelm and Zap Sprayfin's Elusive work for themselves (L20); The Leviathan has neither. It must only be said when A gives Overwhelm/Elusive to B.
   - Captain Farron -> Monster Harpoon: enables: helps it hit the enemy player; also makes cheaper: damages the enemy player
   - Captain Farron -> Jagged Butcher: enables: damages the enemy player; also helps it hit the enemy player
   - The Leviathan -> Swain (level 2): triggers: damages the enemy player; also helps it hit the enemy player
   - Zap Sprayfin -> Darius: helps it level up: damages the enemy player (levels it up); also helps it hit the enemy player (levels it up)
   - Count: about 11 (the "also helps it hit the enemy player" reasons in Swain Ziggs, Gangplank TF, Hand of Pirates).

4. **Captain Farron gets the damage that its created Decimates do.** Farron makes Decimate; only Decimate damages the Nexus with non-combat damage. Breaks L3 (A makes B, B acts on C: no A -> C line). Worst for Swain (level 2), which needs non-combat Nexus damage.
   - Captain Farron -> Swain (level 2): triggers: damages the enemy player; also helps it hit the enemy player
   - Captain Farron -> Gangplank: helps it level up: damages the enemy player (levels it up); also helps it hit the enemy player (levels it up)
   - Count: about 5.

5. **"Creates cards" fed to Curious Shellfolk, which waits for a PICK from random options.** Shellfolk triggers only on Manifest-style picks (Conchologist, Trinket Trade, Loping Telescope). Plain create by name is no pick. Reason does not match the text (L10/L14).
   - Lux -> Curious Shellfolk: triggers: creates cards
   - Lecturing Yordle -> Curious Shellfolk: triggers: creates cards
   - Vanguard Sergeant -> Curious Shellfolk: triggers: creates cards
   - Poison Dart -> Curious Shellfolk: triggers: creates cards
   - Count: about 6 (Lux, Lux level 2, Lecturing Yordle, Otterpus, Vanguard Sergeant, Poison Dart).

6. **Draw by kind treated as drawing a named card.** Zap Sprayfin draws "a spell that costs 3 or less": any cheap spell. Breaks L1b / L21.
   - Zap Sprayfin -> Ravenous Flock: puts it into play: draws it from the deck
   - Zap Sprayfin -> Death's Hand: puts it into play: draws it from the deck
   - Zap Sprayfin -> Scorched Earth: puts it into play: draws it from the deck
   - Count: about 3.

7. **"Makes you discard cards" for Station Archivist, which discards nothing.** It creates a Fleeting copy of a spell and puts the top 5 back. Fallen Rider and Flame Chompers! need THEMSELVES discarded. Reason does not match either text (L1/L7).
   - Station Archivist -> Fallen Rider: triggers: makes you discard cards
   - Station Archivist -> Lost Soul: triggers: makes you discard cards
   - Station Archivist -> Flame Chompers!: triggers: makes you discard cards
   - Station Archivist -> Survival Skills: triggers: makes you discard cards
   - Count: about 4.

8. **A champion summoning itself counted as "puts your units into play".** Jarvan IV only summons himself, which every unit does when it comes in. Breaks L1.
   - Jarvan IV -> Fleetfeather Tracker: triggers: puts your units into play
   - Jarvan IV (level 2) -> Fleetfeather Tracker: triggers: puts your units into play
   - Count: 2.

9. **Wrong reason words: destroying a landmark said as "makes your units die".** Scorched Earth destroys a landmark for Ziggs's level up; the line should say that (L10).
   - Scorched Earth -> Ziggs: helps it level up: makes your units die (levels it up)
   - Count: 1.

## Unsure
- Jarvan IV / Jarvan IV (level 2) -> Penitent Squire "is an Elite it asks for": Jarvan's subtype is not in his text. A champion is probably not an Elite.
- Poppy / Cithria the Bold / Twin Disciplines -> Radiant Guardian "gives it more power (and health)": Guardian's only reading of power is a conditional Lifesteal. Probably no line under L14/L18.
- Single-target damage (Vladimir, Gouge, Basilisk Bloodseeker, Pokey Stick, Poison Dart) seems to have no line to Scorched Earth / Ravenous Flock ("a damaged unit"), yet these cards clearly work together. Possibly missing.
- Arachnoid Sentry (Stun an enemy) -> Ravenous Flock: maybe missing. Its 2 partners were not printed.
- Mystic Shot / Get Excited! -> Blade Squire "kills it for its death effect": a plain hit on one target. L11 may cover own deaths too.
- The Scargrounds (Tough) -> Braum "survives damage (levels it up)": Tough lowers the total damage that Braum's "10+ total damage" counts. Possibly a wrong direction.
- Prank -> Curious Shellfolk: Prank picks 1 of 2 cards and has no line. Missing if those are random options.

## Must-stay (correct)
- Basilisk Bloodseeker -> Gouge: puts it into play: casts its skill
- Hexplosive Minefield -> Ravenous Flock: enables: makes enemy units get Stun
- Blighted Ravine -> Scorched Earth: enables: damages enemy units or players: Scorched Earth kills them
- Vladimir -> Braum: helps it level up: damages it without killing it, for its effect (levels it up); also triggers: damages it without killing it, for its effect
- Conchologist -> Curious Shellfolk: triggers: creates cards

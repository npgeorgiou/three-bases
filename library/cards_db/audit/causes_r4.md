# Runeterra part g: causes found (r4)

Read: lines 3222-4247; not read: lines 4248-6561

Not checked: groups "stronger: more health" (from 4244 on), "waits: puts your units into play", "levels: is a spell it needs played for its count", "stronger: can give it more power and health", "type: changes its stats for its effect", "waits: makes it attack", "cheaper: pays for it", "waits: survives damage", "type: creates cards", "waits: brings it back", "waits: returns it to hand", "cheaper: damages the enemy player", "waits: damages the enemy player", "waits: makes more cards to play".

## Causes

### 1. A unit's own fight keyword is said to help B hit the Nexus (L20)
Wrong thinking: A has Fearsome, Overwhelm or Elusive, so the code says A "helps B hit the enemy player". A's keyword works only for A. On top, most B here are Plunder cards: Plunder checks Nexus damage done before B is played, so helping B hit can never feed its Plunder. Many B are spells, which never hit.
- Necrotic Nestling -> Teenydactyl: type: helps it hit the enemy player (Nestling has only Fearsome)
- Mihira, Aspect Ascendant -> Spoils of War: type: helps it hit the enemy player (Spoils is a spell)
- Overgrown Snapvine -> Bitsy Lizard: type: helps it hit the enemy player
- Smooth Soloist -> Spotted Toad: type: helps it hit the enemy player
- Supercharge -> Riptide Rex: type: helps it hit the enemy player (Overwhelm given after Rex is played does nothing for its Plunder)
Rough count: about 70 of the ~100 lines read in "type: damages the enemy player" and "type: helps it hit the enemy player". The "type: damages the enemy player" reason from such A may stay (A's own keyword gets A to the Nexus, which B's Plunder or Round End check reads); only the "helps it hit" reason is wrong.

### 2. One reason said twice (L10, L18)
Wrong thinking: each sub-reason is printed as its own line instead of the strongest one once. Stat help is split into "more power" + "more health" instead of the one family "gives it more power and health"; "type: changes its stats for its effect" is printed next to "stronger: more power"; "type" and "waits" both print "kills it for its death effect".
- Professor von Yipp -> Stubborn Husk: stronger: gives it more power and health when it comes / more health / more power
- Trumpetecher -> Scattered Husk: stronger: more health + stronger: more power
- Enraged Husk -> Vi: type: changes its stats for its effect / stronger: more power / stronger: does what it waits for or counts (stat changed) when it comes
- Master Bingwen, the Sieve -> The Undying: type: kills it for its death effect + waits: kills it for its death effect
Rough count: about 30 of the 50 pairs in "stronger: more power"; also most pairs in causes 1.

### 3. Stat help after the moment B reads its stats (L4, L14)
Wrong thinking: B reads its own power only once, in a Play or "when I'm summoned" effect, but A buffs an ally already in play (or B reads a card in hand while A buffs a played one), so the buff comes too late or hits the wrong card.
- Rising Spell Force -> Banana Blaster: stronger: more power (Blaster's Play already went off)
- Blinded Mystic -> Navori Highwayman: stronger: more health / more power (Highwayman's summon effect already went off)
- Stubborn Husk -> Revitalizing Roar: stronger: more power (Husk buffs the ally being played; Roar reads a unit still in hand)
Rough count: 3-5 of the lines read.

### 4. Help that A does not give to B at all (L14, L9)
Wrong thinking: a buff to a narrow kind, to A itself, or to enemies is linked to a B outside that kind.
- Soul Shepherd -> Vi: stronger: more power (Shepherd buffs Ephemeral allies only; Vi is not Ephemeral)
- Ornn (level 2) -> Wrought Colossus: stronger: more health / more power (Ornn equips and forges only himself)
- Wrought Colossus -> Illaoi: stronger: more power (Colossus gives Illaoi nothing; Illaoi reads a Tentacle's Power)
- The Emperor's Army -> Wrought Colossus: stronger: more power (Colossus reads the equipment's stats, not its own)
- Yasuo (level 2) -> Yeti Yearling: waits: kills it for its death effect (Yasuo strikes only enemies)
Rough count: about 6 of the lines read.

### 5. Wrong reason words for what B waits for (L10, L15)
Wrong thinking: B waits for one exact thing, the line gives a different thing.
- Quick Quill (created) -> Gwen (level 2): waits: changes your units' stats (Gwen waits for Power from Hallowed only)
- Soul Shepherd -> Vi: type: changes its stats for its effect (Vi's effect waits for cards played, not a stat change)
- Path of Destruction -> Caustic Cask: waits: kills it for its death effect (Path destroys a landmark; Caustic Cask is a unit)
Rough count: about 5.

### 6. Generic damage boost feeds a death effect (L18, L21)
Wrong thinking: "spells deal 1 extra damage" kills nothing by itself, yet links to Last Breath cards and landmarks.
- Funsmith -> Shark Chariot: waits: kills it for its death effect
- The Syren -> Sarcophagus: waits: kills it for its death effect
Rough count: 2 of 50 read in that group.

### 7. A 0-cost spell feeds a mana count (L17)
- Nagakabouros' Tantrum -> Lux (level 2): waits: is a spell whose playing sets off its effect (Tantrum costs 0, adds no mana to "6+ mana of spells")
Rough count: 1.

## Unsure
- Spirit grants (Celestial Blessing, Jarro Lightfeather, Aberrant Mageseeker, Inspiring Light, Sprite Flock) linked as "more power" to Winged Messenger, Divine Clerk, Vi, Husks, Mask Mother: I do not know if Spirit adds stats or what Empowered counts.
- Lux (level 2) from 3-5 cost spells (Scorched Earth, Search Warrant, Eradication): fine if "6+ mana of spells" adds up over several spells, as L17 suggests.
- Hothead / The Darkin Spear (created) -> Glacial Fell / Seal In Steel: buffs a card in the deck; it may reach play later.
- Bloodcursed Harpy from kill-an-ally cards (The Second Death, Gentlemen's Duel): Harpy has no death effect, only a save from death; it may still be a real combo.
- Sump Fumes, Knock 'Em Down -> Last Breath allies: a plain hit on one unit used to kill my own ally.
- Fading Memories -> Sacrificial Scholar: an Ephemeral copy in hand (L19 generic?) that later dies.
- Geode Mechaforcer -> Quick Quill (created) and Iron Legion -> Nagakabouros' Tentacle: not clear the help reaches B.
- "6+ cost spell" group (Unstable Voltician, Mageseeker Investigator, Albus Ferros...): I did not check every A's cost; Dragon Dedicant -> Ravenbloom Conservatory may be a unit.

## Must-stay (checked against both texts)
- Cithria the Bold -> Bitsy Lizard: type: helps it hit the enemy player (gives other attacking allies Fearsome)
- Zenith Blade -> Spotted Toad: type: helps it hit the enemy player (gives an ally Overwhelm)
- Cosmic Rays -> The Forge Of Tomorrow: waits: is a spell whose playing sets off its effect (8-cost spell)
- Hextech Transmogulator -> Jayce (level 2): waits: is a spell whose playing sets off its effect (6-cost spell)
- Death's Grasp -> Blue Sentinel: waits: kills it for its death effect

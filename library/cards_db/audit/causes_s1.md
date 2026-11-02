# sts1 line check: causes

Read: lines 1-1500; not read: lines 1501-3305

Sections a-f read fully. Section g read up to the middle of "waits: is a Skill whose playing sets off its effect". The rest of g (from line 1501) is not checked.

## Causes (sure, from both card texts)

### 1. "Whenever you play a card" gets a line from cards that make cards (L1)
Wrong thinking: a card that makes more cards feeds a card that reacts to any card played. L1 names After Image as no line. It even links unplayable or non-card makers (Wounds, Dazed, potions, relics).
- Beta -> After Image+: waits: makes more cards to play
- Jack of All Trades -> A Thousand Cuts: waits: makes more cards to play
- Mark of Pain -> Ink Bottle: waits: makes more cards to play
- Reckless Charge -> Pain: waits: makes more cards to play
- Cauldron -> Pain: waits: makes more cards to play
Count: about 430 lines (the whole reason, 432). Also the same reason into Orange Pellets (70) and Dead Branch -> After Image / A Thousand Cuts / Pain / Panache / Ink Bottle / Choke.

### 2. Waiting for a card added to the deck is fed by cards made in combat (L13, L20)
Wrong thinking: "add a card to your deck" (Eggs, Ceramic Fish) and "obtain a Curse" (Darkstone Periapt, Omamori) are read as "creates a card". Cards put into hand or draw pile in combat, and potions, are not added to the deck; the made card is often the wrong kind (not a Curse, not a Skill).
- Jack of All Trades -> Molten Egg: waits: creates cards
- Cauldron -> Molten Egg: waits: creates cards
- Hello World -> Omamori: waits: creates cards
- Attack Potion -> Darkstone Periapt: waits: creates cards
- Cursed Key -> Toxic Egg: waits: creates cards
Same cause for Master Reality ("created during combat") fed by out-of-combat or potion makers: Cauldron, Entropic Brew, Calling Bell, Orrery -> Master Reality.
Count: most of the 289 "creates cards" lines; correct ones are only deck adders (Dream Catcher, Orrery -> Eggs/Fish) and Curse givers (Cursed Key, Calling Bell -> Darkstone Periapt/Omamori).

### 3. A card's own Exhaust keyword feeds Sentinel (L7)
Wrong thinking: Sentinel says "If THIS card is Exhausted"; a card that exhausts itself does nothing for Sentinel. Only cards that exhaust other cards (Purity, Fiend Fire, Second Wind, Sever Soul, True Grit, Burning Pact, Corruption) help it.
- Slimed -> Sentinel: waits: exhausts cards
- Reaper -> Sentinel: waits: exhausts cards
- Intimidate -> Sentinel: waits: exhausts cards
- Exhume -> Sentinel: waits: exhausts cards
Count: about 80-100 lines (every self-Exhaust card to Sentinel).

### 4. Any status on the player feeds Wave of the Hand (L4, L14)
Wrong thinking: "makes units get a keyword or status" matches Wave of the Hand, which waits only for Block. Strength, Dexterity, Artifact, Intangible are not Block.
- Clockwork Souvenir -> Wave of the Hand: waits: makes units get a keyword or status (for the ability it gives)
- Ghost in a Jar -> Wave of the Hand: waits: makes units get a keyword or status (for the ability it gives)
- Shuriken -> Wave of the Hand: waits: makes units get a keyword or status (for the ability it gives)
- Kunai -> Wave of the Hand: waits: makes units get a keyword or status (for the ability it gives)
Count: probably 50+ (every status giver); Block givers to Wave of the Hand are right but said three times (cause 8).

### 5. Out-of-combat healing feeds Magic Flower, and the words say "units" (L13, L12)
Wrong thinking: Magic Flower boosts healing during combat only; heals at Rest Sites, shops or pickup get nothing. Also the player is no card: the words must be "heals you".
- Eternal Feather -> Magic Flower: waits: heals your units
- Meal Ticket -> Magic Flower: waits: heals your units
- Regal Pillow -> Magic Flower: waits: heals your units
- Lee's Waffle -> Magic Flower: waits: heals your units
Count: about 5-10 wrong; in-combat ones (Blood Vial, Pantograph, Lizard Tail) are right but have wrong words.

### 6. A plain hit on one target feeds "whenever an enemy dies" (L11, L21)
- Anger, Bash, Bite, Claw, Clothesline, Dash, Dagger Throw -> Gremlin Horn: waits: makes enemy units die
Count: most of the 105 lines into Gremlin Horn, and the same into The Specimen and Corpse Explosion if those get single-target hits.

### 7. Copy into hand is a line (L19)
- Dual Wield -> Body Slam: puts: copies it
- Dual Wield -> Twin Strike: puts: copies it
- Dual Wield+ -> Corruption: puts: copies it
Count: every Attack and Power from Dual Wield / Dual Wield+ (about 200+).

### 8. One reason said twice or three times (L10)
Wrong thinking: "type" and "waits" both fire for the same need.
- Captain's Wheel -> Wave of the Hand: type: gives you Block / waits: gives you Block / waits: makes units get a keyword or status
- Thunderclap -> Champion Belt: type: makes enemy units get Vulnerable / waits: makes enemy units get Vulnerable
- Mayhem -> Rebound: waits: is played (for the ability it gives) / waits: is played
- Every Attack -> Kunai, Shuriken, Ornamental Fan, Nunchaku, Letter Opener: "type: ... for its count" and "waits: ... sets off its effect"
Count: about 900 extra reasons (121 x 5 Attack counters, 202 Letter Opener, plus the Wave of the Hand and Champion Belt pairs).

### 9. "Play the top card" feeds every play counter as "is played" (L1)
Wrong thinking: Havoc, Mayhem, Distilled Chaos, Omniscience, Unraveling play a random or chosen card; that is a play like any other, not an Attack or Skill the counter needs.
- Havoc -> Corruption: waits: is played
- Distilled Chaos, Havoc -> Kunai: type: is played / waits: is played (lines 78-79)
Count: about 50 (5 cards x every counter, said twice).

### 10. Orange Pellets links from every card type (L1)
Wrong thinking: Power, Attack and Skill together are almost all playable cards, so every card counts. 416 partners.
- Bash -> Orange Pellets (from line 16), Defend (Ironclad) -> Orange Pellets (from 15), Demon Form -> Orange Pellets (from 18)
Count: about 400.

### 11. Draw of one random card feeds "when you draw X" (L1b)
- Gremlin Horn -> Fire Breathing: waits: makes you draw cards
- Gremlin Horn -> Evolve: waits: makes you draw cards
- Dark Embrace -> Fire Breathing: waits: makes you draw cards
Count: about 10-30.

### 12. Made card is the wrong kind for the need (L20)
- Metamorphosis -> Escape Plan: waits: is a Skill whose drawing sets off its effect (Metamorphosis makes Attacks)
- Burn -> Static Discharge: waits: makes you lose HP (Static Discharge needs unblocked attack damage)
- Pain -> Static Discharge: waits: makes you lose HP
Count: about 10.

### 13. Power card by kind feeds Frozen Egg (L1b)
- Live Forever -> Frozen Egg: type: is a Power it asks for
- Hello World -> Frozen Egg: type: is a Power it asks for
Count: about 70 (every Power).

## Unsure
- Energy -> "cheaper: pays for it" (3238 lines, 30.7%): most targets cost 2 (Dash, Uppercut, Heavy Blade). L21 names "costs 2 or more" as generic. If EXPENSIVE is 2 in sts1, it is too low. Also wording "more mana" should be "more energy".
- Snecko Oil, Madness, Mummified Hand -> any card "cheaper": random cost changes are aimed help to any card (L14); Snecko Oil can also raise costs.
- Sentinel -> Sever Soul: cheaper: the real use is the other way (Sever Soul exhausts Sentinel for energy); reason words may be wrong.
- Skill counters (Letter Opener, Corruption, 202 Skills): Kaptain kept Attack counts (Kunai, Rage); Skills are a bigger share, maybe generic.
- Capacitor -> Doom and Gloom, Potion Of Capacity -> Recursion "more slots": orb slots help any channeler; may be generic.
- Bullseye -> Doom and Gloom "Lock-On: its damage is bigger": Lock-On boosts orb damage, not the card's hit; may be L18.
- Kunai/Duality -> Reinforced Body "makes the Block it gives bigger": only Reinforced Body gets it, not other Block cards; inconsistent.
- Melter -> Letter Opener / Charon's Ashes: removing Block is a damage boost, maybe L18.
- Draw cards -> Cloak Clasp / Spirit Shield "fills your hand" (114): draw is generic by L1b, but B reads hand size.
- Paper Phrog (no lines seen in part e) may miss lines from Vulnerable appliers (Bash, Thunderclap, Trip); not verified.

## Must-stay (correct) examples
- All for One -> Secret Weapon+: puts: brings it back to your hand
- Unload -> Tactician: waits: makes you discard cards
- Worship+ -> Establishment+: waits: makes this happen: kept in hand
- Shuriken -> Heavy Blade: type: gives you Strength
- Dream Catcher -> Molten Egg: waits: creates cards

# Causes, runeterra deck check p2_1 (Sivir Akshan, Poppy Ziggs, Gangplank Sejuani, Bandle Tree)

## Causes (8)

1. Rally (a free extra attack) is linked to a card that waits for an attack, but not to a card that waits for a strike.
   Rule: L2/L4/L16 (an added attack makes its own effect go off). Golden Aegis (gain_attack_token) gets a line to Sivir (level 2) ("enables: another attack"), and Cataclysm gets one to Akshan ("triggers: does what it waits for (strikes)"). Akshan's rows wait for "strikes by self", so a second attack is a second Palace/Hoard step, but Golden Aegis has no line to Akshan or Akshan (level 2).
   - `Golden Aegis (3 partners)`: lines only to Sivir (level 2), Warlord's Hoard, Warlord's Palace
   - `Cataclysm -> Akshan: triggers: does what it waits for or counts (strikes)` (present, so Golden Aegis -> Akshan is missing)
   - `Cataclysm -> Akshan (level 2): triggers: does what it waits for or counts (strikes)`

2. Sivir (level 2) copies the keywords of attacking allies, but no keyword-giver links to it.
   Rule: L14 (a card that uses keywords gets the line from cards that give keywords), L20. Sivir (level 2) has only 3 partners (Cataclysm, Golden Aegis, her level 1); Lucky Find (Fearsome), Brightsteel Protector (Barrier), Golden Aegis (Barrier) and The Absolver's Return (Overwhelm) give a keyword to a chosen unit that then attacks, and Sivir copies it.
   - `Sivir (level 2): ... WHEN always IF have self [state is attacking] is DO copy_keywords all mine unit in board [state is attacking] to self`
   - `Lucky Find (3 partners)`: Warlord's Hoard, Warlord's Palace, Vekauran Bruiser, no Sivir (level 2)
   - `Brightsteel Protector (2 partners)`: only Warlord's Hoard and Warlord's Palace

3. Reason text names the wrong kind (L8): Akshan's Warlord's Palace and Hoard are landmarks, the line says units.
   - `Akshan -> Shaped Stone: enables: puts your units into play` (Shaped Stone counts "summoned of mine landmark")
   - `Akshan (level 2) -> Shaped Stone: enables: puts your units into play`
   Should read "puts your landmarks into play".

4. A unit-only hit is credited with killing a landmark (L8 kind, L16).
   Noxian Fervor's rows damage "chosen mine unit" and "chosen unit"; Scrappy Bomb is a Landmark. Imperial Demolitionist and Poison Dart get no such line, so it is also inconsistent.
   - `Noxian Fervor -> Scrappy Bomb: triggers: kills it for its death effect`

5. A line doubles a drawback: damage that hurts my own units is no help (L5).
   Fortune Croaker's damage is a cost for the draw (self and a chosen mine unit). The Dreadway's "damage it again" makes the cost bigger. Contrast the kept lines where The Dreadway doubles damage to the enemy (Kaptain: "The Dreadway -> Decimate is a combo").
   - `The Dreadway -> Fortune Croaker: makes stronger: doubles its damage`

6. A draw by kind and cost only is given a named-card line (L1b, L21).
   Zap Sprayfin draws "random spell, cost le 3": any cheap spell can be drawn, so this is no line to Make it Rain or Warning Shot.
   - `Zap Sprayfin -> Make it Rain: puts it into play: draws it from the deck`
   - `Zap Sprayfin -> Warning Shot: puts it into play: draws it from the deck`
   (Contrast The Dreadway -> Gangplank: a named draw, right.)

7. A fight keyword of the helper is counted as help to the partner, and one fact is said twice (L20, L10).
   Elusive or Overwhelm works for the card that has it. "helps it hit the enemy player" is put on partners that never hit (Black Market Merchant, Jagged Butcher, Monster Harpoon only need Nexus damage dealt), and the same fact appears twice in one line.
   - `Zap Sprayfin -> Black Market Merchant: enables: damages the enemy player; also helps it hit the enemy player`
   - `Gangplank (level 2) -> Monster Harpoon: enables: helps it hit the enemy player; also makes cheaper: damages the enemy player`
   - `The Dreadway -> Gangplank: ... helps it level up: damages the enemy player (levels it up); also helps it level up: helps it hit the enemy player (levels it up); ...`
   - `Zap Sprayfin -> Sejuani: helps it level up: damages the enemy player (levels it up); also helps it hit the enemy player (levels it up)`

8. A summon by description gets no line to the cards whose "when I'm summoned" it sets off (L17).
   Feel The Rush summons 2 random champions of mine; Gangplank and Gangplank (level 2) each "WHEN summoned DO summon Powder Keg". Feel The Rush has 1 partner (Powder Keg only).
   - `Feel The Rush (1 partners)`: only `Powder Keg -> Feel The Rush`
   - `Gangplank: KW: Overwhelm | WHEN summoned of self DO summon in board <Powder Keg>`

## Unsure
- Sivir (level 1) counts damage by my player (ge 30). The Absolver's Return -> Sivir ("more damage") is a line, but For Demacia!, The Absolver, Shaped Stone (power boosts) get none. Either all power boosts link (L18 "reads the damage") or the Return only for its Overwhelm.
- Cataclysm and Golden Aegis (extra attack) -> Sivir (level 1): not shown; an extra attack is extra damage for the count.
- Shaped Stone, The Absolver, The Absolver's Return, Concerted Strike target "chosen mine unit" like Brightsteel Protector and Lucky Find, which link to Warlord's Palace/Hoard ("triggers: targets your cards"); those lines are not visible in the output (Vekauran Vagabond -> Shaped Stone, summoning the Palace, also not visible).
- Relic of Power (summon Sandstone Charger) and Warlord's Palace -> Relic of Power (creates), analogous to Warlord's Hoard -> Sentinel's Hoard and Waking Sands -> Sandstone Charger: not visible.
- Vanguard Sergeant (creates For Demacia!) and For Demacia!: each shows 2 partners but one printed line; the creation line Sergeant -> For Demacia! (like Treasure Seeker -> Waking Sands) is not printed.
- Poppy and Poppy (level 2) show 1 partner each in both decks but no line printed (Ziggs -> Ziggs (level 2) is printed).
- Rows of Ziggs and Legion Saboteur show a direct effect, no creating or casting of Short Fuse / Sabotage, yet `Ziggs -> Short Fuse` and `Legion Saboteur -> Sabotage` say "casts its skill".
- The Bandle Tree (1 partner, only Buster Shot) needs 10 regions among my units; Bandle City Mayor and Loping Telescope manifest multi-region followers and have no line to it.
- Group Shot counts units (4 or more); House Spider (summons Spiderling) and Chum the Waters (summons Longtooth) have no line to it (House Spider has 1 partner).
- Marai Warden (no partner) summons a random cost-1 follower; a line to Dreadway Deckhand depends on its cost, which the rows do not show.
- Ravenous Flock -> Fizz says both "helps it level up" and "triggers" for one fact (a spell played), but they come from two different abilities of Fizz.

## Clearly right
- `Warlord's Hoard -> Sentinel's Hoard: puts it into play: creates`
- `Concerted Strike -> Akshan: helps it level up: makes it strike for its effect`
- `Vekauran Vagabond -> Akshan: helps it level up: finishes countdowns (levels it up)`
- `The Dreadway -> Crackshot Corsair: makes stronger: doubles its damage`
- `Yordle Grifter -> Black Market Merchant: triggers: makes you draw cards`

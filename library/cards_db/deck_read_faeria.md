# Faeria deck networks: every wrong or missing line, grouped into families (29 Oct 2026)

Kaptain's check of v38 (24 points) plus Claude's own reading of the 12 decks. Each family is fixed once, for every game.

## F1 Labels read backwards or say the wrong thing (page)
- "is a card it needs in play or in the deck" (kind type) reads as if the arrow's start needed the end; the arrow goes from
  the card that is or makes the thing to the card that uses it (Recruiter -> Champion, spells -> Windstorm Colossus, big
  creatures -> Ancient Boar, Manta Rider -> Windborne Emissary). Label becomes "enables" (Kaptain).
- "makes it stronger" (kind boosts) is used for cheaper, reaching places, more health: label becomes "helps"; the hover says
  how (Blue Jump Wavecrash Colossus; Bargain Krog's Dinner -> Krog).

## F2 Help aimed at one chosen or random card shown only as a faint "can aim at it"
- Oakling (+5/+5 to a random green creature in hand) -> every green creature; Khalim's Training (a creature +1/+0, Flying,
  Charge 2) -> every creature; Syland Horsemaster (another friendly creature Charge 3) -> every creature; Bold Bargainer,
  Ogre Dance (a card in hand costs 7 less) -> every card costing 7+. Rule: help my side aims at a chosen or random card is a
  "helps" line to every card it can hit, weight shared.

## F3 Paying for big cards
- Red Devil (gain 5 faeria), Krog (Combat: a card costs 7 less) -> the deck's expensive cards. Rule: gaining mana and cost
  cuts help the cards that cost the most in that game (top quarter of the game's costs).

## F4 Where cards enter and how the board grows (Faeria rules: land next to your creatures, summon on your own land)
- Charge / Jump / Flying units, move spells (Flash Wind, Oradrim Fanatic, Windborne Champion), land movers (Sunken Tower,
  Shifting Tide), unit makers (Battle Toads) extend where I can build and summon. They help cards whose entry needs a place:
  Bomb Slinger (adjacent enemy), Axe Grinder / Mystic Beast (adjacent to an enemy well), Mistral Guide (units summoned next
  to it), Blazing Salamander, Daring Adventurer; and creatures needing a land colour (Oasis Explorer and every coloured
  creature: a moved lake lets a blue creature enter there). Game rules for Faeria: a unit lets me build land next to it; a
  creature enters on my own empty land of its colour.

## F5 Ranged needs a clear straight line
- Flame Thrower, Hilltop Archer (Red Archers): damage, removal and moving of enemy units clears the line; effects that move
  my ranged unit do not stop its attack. Ranged keyword entry: the nearest enemy in a straight line.

## F6 Needs that are no needs
- Krog's Dinner "When you summon Krog, destroy this": an ability that only removes the card itself waits for nothing.
- Shaytan Monstrosity "when a friendly creature dies": Soul Drain and Last Nightmare (aimed at a chosen creature of either
  side) are no friendly deaths; one plays them on enemies. Every creature of mine can die fighting: they enable it (weak).
- Wavecrash Colossus: every unit with Charge/Jump/Flying "reaches enemy wells" was noise (Gabrian Archon -> Colossus).

## F7 Page
- Node labels: show cost and Attack|Life; keywords shown twice; far nodes; decks listed twice (decks.tsv and
  cases/decks.tsv); a game, then a deck, instead of one long list.

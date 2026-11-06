# Gwent (standalone)

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: digital card game (CD Projekt Red, standalone Gwent 2018-2023, the game kept running community-balanced).
- Match: best of 3 rounds. In a round players alternate playing one card or passing; when both pass, the higher total power wins the round.
- Board: each side has two rows (melee and ranged) of up to 9 units each.
- Cards: no mana. Hands are drawn at the start (10 cards, with mulligans), and only a few more cards come in rounds 2 and 3, so card advantage and when to pass are central.
- Deckbuilding: at least 25 cards, limited by provisions; a leader ability per deck.
- Keywords: Deploy, Order, Zeal, Charge, Cooldown, Boost, Damage, Armor, Lock, Spying, Bonded, Deathwise, Thrive, Consume, Harmony, Bloodthirst, Berserk, Fee, Tribute, Coin.
- Specific: points (power) are both the units' health and the score.

## Sources and notes

Sources:
[1] https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html (factions in the current game)
[2] https://www.keengamer.com/articles/guides/what-is-the-best-faction-in-gwent/ (October 2020)
[3] https://www.pockettactics.com/gwent-the-witcher-card-game/decks
[4] https://www.bluestacks.com/blog/game-guides/gwent/gwt-top-5-best-decks-en.html (February 2025)

The library holds the current card texts (v14.8). Guides from the 2017-18 beta (playgwent archetype guide of April 2018,
the faction-evolution article of July 2018, PC Gamer's Nilfgaard article with Letho + Fake Ciri and Vattier + Mangonel)
describe cards whose texts were rewritten in Homecoming; they are not used..
Neutral is not a faction.

## The game's rules (from sources)
Sources: [R1] https://gwent.fandom.com/wiki/Rules (fetched 5 Nov 2026; patch notes up to 19 Dec 2017); [R2]
https://gamepretty.com/cdpr-witcher-card-game-gwent-homecoming-revealed-returning-to-witcher-3-style/ (Homecoming, the
rules the 14.8 cards are written for); [K] the keyword entries of the gwent.one 14.8 export (in the library).
- A match is won by winning two rounds (battles) [R1]. On a turn a player plays a card, uses the leader ability, or passes;
  a player who passed plays no more cards that round; when both have passed the round ends and the higher total power
  wins it [R1]. A tie: both lose the round [R1].
- The board: each player has two rows, melee and ranged [R1][R2], of at most 9 units each [R2]. A unit's power adds to its
  side's total (the score) [R1]; damage lowers power and a unit at 0 power goes to the graveyard [R1]. Armor takes damage
  first and does not count toward the score [K].
- At the end of a round every unit on the battlefield goes to the graveyard [R1], except units with Resilience [K].
- Cards: 10 at the start, 3 more at the start of rounds 2 and 3; at most 10 in hand, cards drawn beyond it are discarded
  [R1]. Mulligans before the match and at the start of later rounds [R1][R2].
- Deck: at least 25 cards within the provision limit, which the leader ability sets; cards of the leader's faction or
  Neutral; bronze cards two copies, gold cards one [R1]. The leader ability is not a card on the board; it is used as a turn
  [R1][R2]. The winner of a round starts the next one [R1].
- Order abilities cannot be used the turn the card is placed (Zeal allows it) [K]. Coins: at most 9, halved (rounded down)
  between rounds [K].

## Factions

### Northern Realms
*Claude:* Human kingdoms: armor, boosts, Order and Charge engines.
Known for: boosting friendly units, Formation abilities that give Zeal or Boost in the right row [1]; self-boosting, Order
abilities, big numbers [2].
Weak at: tall removal [2].

### Nilfgaard
*Claude:* Empire: Lock, Spying, poison, reveal and taking enemy cards.
Known for: locking units, spying on enemy hands, stealing or forcing enemy units onto its side, Spies on the opponent's board
that benefit it, playing cards from the opponent's deck [1]; locks and poisons, reactive [2]; diplomacy and subterfuge [3].
Archetypes: control and counterplay [1].

### Monsters
*Claude:* Beasts and vampires: Thrive, Consume, Deathblow and Dominance.
Known for: Consume (devouring weaker units), Deathwish [1]; benefiting from the highest value on board, weather, and death;
growing tall, Thrive, Deathwish [2]; consuming its own kind [3].
Archetypes: swarm and devour [1]; swarming the board [2].

### Scoia'tael
*Claude:* Elves and dwarves: moving units, Harmony, traps and tempo.
Known for: traps, ambush, ranged attacks, playing cards straight from the deck [1]; traps, Harmony, mobility, many small
damage instances [2][3].
Archetypes: hit-and-run with traps [1]; guerrilla [2].

### Skellige
*Claude:* Islanders: Bloodthirst, Berserk, self-damage and the graveyard.
Known for: Berserk below a power threshold, damaging itself or allies for bonuses, reviving from the graveyard [1]; damaging
units many ways, Berserk [2]; power from wounds and death [3].
Archetypes: damage synergy and resurrection [1]; aggression [3].

### Syndicate
*Claude:* Criminal guilds: coins (Profit, Fee, Tribute) and Crime cards.
Known for: coins, a second currency spent on effects [1][2].
Archetypes: economy, hoarding for one big play or steady spending [1].

## Combos
- Koshchey + Caranthir Ar-Feiniel: a large amount of points [4]
- Joachim de Wett + Coup de Grâce: strong plays always available [4]
- Iris von Everec + Iris' Companions: thinning for a strong Round 3 hand [4]
- Sove + Tyr, Prince Anseis + Radovid: Judgment, Mutagenerator + Temple of Melitele + Inspired Zeal: names do not match one library card; no case [4]

## Deck pairs
Card pairs the deck guides (playgwent.com, `content` field of each deck in ../cards_db/decks.tsv) name, as
`deck | A | B | the guide's words` (A does it for B). `cards_db/deck_pairs.py gwent` turns each into a `line` row of
cases/network.tsv. Guides with no named pair (video links only) give none.

```pairs
Nature's Gift: Devotion Symbiosis Good Version | Mahakam Pass | Naiad Fledgling | buff can protect vulnerable engines (Naiad Fledglings)
Nature's Gift: Devotion Symbiosis Good Version | Mahakam Pass | Naiad Pondkeeper | set up a treant for Naiad Pondkeeper
Mobilization: NR Devotion Undead Army | Kerack Marine | Kaedweni Revenant | they can also protect your Revenant
Mobilization: NR Devotion Undead Army | Poor Fucking Infantry | Kaedweni Revenant | PFIs are good Revenant food
Mobilization: NR Devotion Undead Army | Forbidden Magic | Kaedweni Revenant | Forbidden Magic is to get more Revenant
Mobilization: NR Devotion Undead Army | Redanian Secret Service | Drakenborg | amazing synergy with Drakenborg
Mobilization: NR Devotion Undead Army | Redanian Secret Service | Kaedweni Revenant | good Revenant food
Mobilization: NR Devotion Undead Army | Princess Adda | Redanian Secret Service | Adda gains Immunity on Deploy, so she will summon a Secret Service
Mobilization: NR Devotion Undead Army | Drakenborg | Vincent Meis | Drakenborg targets
Mobilization: NR Devotion Undead Army | Drakenborg | Margarita Laux-Antille | Drakenborg targets
Mobilization: NR Devotion Undead Army | Drakenborg | Botchling | Drakenborg targets
Mobilization: NR Devotion Undead Army | Drakenborg | Bloody Baron | Drakenborg targets
Mobilization: NR Devotion Undead Army | Kaedweni Revenant | Vincent Meis | with Revenant on board Vincent kills any unboosted unit
Mobilization: NR Devotion Undead Army | Redanian Archer | Vincent Meis | with Archer on board Vincent kills any unboosted unit
Mobilization: NR Devotion Undead Army | Voymir | Kaedweni Revenant | boost all Revenants on board
Mobilization: NR Devotion Undead Army | Voymir | Redanian Archer | reactivate the Redanian Archer engines
Mobilization: NR Devotion Undead Army | Sabrina Glevissig | Kaedweni Revenant | another Revenant food
Mobilization: NR Devotion Undead Army | Philippa: Blind Fury | Kaedweni Revenant | a Revenant food
Mobilization: NR Devotion Undead Army | Botchling | Princess Adda | every time Botchling transforms, it boosts Adda by 5
Mobilization: NR Devotion Undead Army | Vernon Roche | Kaedweni Revenant | also a Revenant food
Shieldwall: Roegner Ale Damsel | Ale of the Ancestors | Knight-Errant | speed up Knight Errant grace
Shieldwall: Roegner Ale Damsel | Ale of the Ancestors | Prince Anséis | enhance Prince Anseis removal
Pincer Maneuver: Kimbolt's Temple Siege | Temple of Melitele: Congregation | Prince Anséis | play Temple and buff Anseis
White Frost: White Frost-EZ pro rank | Eredin Bréacc Glas | Caranthir: Golden Child | Eredin into constant frost brings Golden Child to 32 power
Arachas Swarm: Tatterwing - 1 prov left for good luck | Ge'els | Lara Dorren | with Ge'els you can replay Lara
Enslave: Damage Enslave With Enforcers (+10 -1) | Battle Stations! | Impera Enforcers | play Enforcers with Battle Preparation in one turn
Enslave: Damage Enslave With Enforcers (+10 -1) | Fercart | Impera Enforcers | Stefan Skellen played with Fercart on board procs Enforcers 4 times
Enslave: Damage Enslave With Enforcers (+10 -1) | Stefan Skellen | Impera Enforcers | Stefan Skellen with Fercart procs Enforcers 4 times
Enslave: Damage Enslave With Enforcers (+10 -1) | Buhurt | Fercart | Fercart can protect self with Buhurt
Enslave: Damage Enslave With Enforcers (+10 -1) | Joachim de Wett | Coup de Grâce | Joachim + Coup combo
Tactical Decision: OP GN HyperThin | Doadrick Leumaerts | Albrich | Doadrick will cycle Albrich in round 3
Tactical Decision: OP GN HyperThin | Maxii van Dekkar | Albrich | Maxii will also proc Albrich
Tactical Decision: OP GN HyperThin | Strays of Spalla | Albrich | Strays can be used to proc Albrich
Tactical Decision: OP GN HyperThin | Summoning Circle | Imperial Golem | select golem with summoning circle
Tactical Decision: OP GN HyperThin | Doadrick Leumaerts | Snowdrop | use Doadrick to get value off Snowdrop
Blood Money: Classical Bounty with Tamara, Drill | Vivaldi Bank | Conjurer's Candle | Vivaldi's Bank is essential for Conjurer's Candle
Blood Money: Classical Bounty with Tamara, Drill | Royal Decree | Tamara Strenger | Royal Decree can be used to find Tamara Strenger
Onslaught: Pirates attack - Endless Voyage | Vabjorn | Raiding Fleet | use Vabjorn to play Raiding Fleet
Onslaught: Pirates attack - Endless Voyage | Vabjorn | Abordage | use Vabjorn to play Abordage
Rage of the Sea: Fulmar rain ft. Otkell and Melusine | Melusine | Messenger of the Sea | go Melusine round 1, with Messenger of the Sea
Rage of the Sea: Fulmar rain ft. Otkell and Melusine | Torrential Rain | Messenger of the Sea | play rain and messenger as required
Patricidal Fury: RnR Seagulls Sove Compass | Seagull | Ragh Nar Roog | for Clear Skies some swarm; Seagulls come handy
Patricidal Fury: RnR Seagulls Sove Compass | Hammond | Ragh Nar Roog | max value from Cataclysm: Hammond moves an enemy unit
```

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name: name|expected concept|wording on the cards. Checked with coverage.py --mechanics (not yet run).
# Sources (21 Oct 2026): bluestacks.com Gwent decks guide and top-5 decks (Feb 2025), keengamer.com best faction (Oct 2020),
# pockettactics.com Gwent decks. Beta-era guides are not used (texts rewritten in Homecoming).
boost|stat_gain|\bboosts?\b
zeal|haste|\bzeal\b
formation|rows|\bformation\b
order|activated|\border\b
lock|silence|\blocks?\b
spying|donate|\bspying\b
poison|deathtouch|\bpoison\b
consume|sacrifice|\bconsumes?\b
deathwish|death_trigger|\bdeathwish\b
thrive|permanent_growth|\bthrive\b
berserk|condition_life|\bberserk\b
damage itself or allies|friendly_fire|\bdamage (itself|a (friendly|allied) unit)\b
resurrect|revive|\bresurrects?\b
trap|trap_secret|\btrap\b
ambush|stealth|\bambush\b
harmony|variety_payoff|\bharmony\b
coins|coin_economy|\bcoins?\b
hoard|resource_banking|\bhoard\b
weather|row_effects|\b(frost|fog|rain|storm|hazards?)\b
move units|movement|\bmoves?\b
play from the opponent's deck|cast_from_zone|\bopponent's deck\b
reveal|information|\breveals?\b
# term: Spying units are played on the opponent's side of the board but benefit their owner (bluestacks decks guide).
# term: Formation: an ability that gives Zeal or Boost when the unit is played in the right row (bluestacks decks guide).
# term: Berserk: activates when the unit's power drops below a threshold (bluestacks decks guide).
# term: Syndicate coins: a second currency earned and spent on effects (bluestacks; keengamer).
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Northern Realms	stat_gain	boosting friendly units	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Northern Realms	haste	Zeal	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Northern Realms	activated	Order abilities	https://www.keengamer.com/articles/guides/what-is-the-best-faction-in-gwent/
signature	Nilfgaard	silence	locking units	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Nilfgaard	information	spying on enemy hands	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Nilfgaard	steal	stealing enemy units	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Nilfgaard	donate	Spies on the opponent's board	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Nilfgaard	cast_from_zone	playing cards from the opponent's deck	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Monster	sacrifice	Consume devours weaker units	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Monster	death_trigger	Deathwish	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Monster	stat_condition	highest value on board	https://www.keengamer.com/articles/guides/what-is-the-best-faction-in-gwent/
signature	Monster	row_effects	weather	https://www.keengamer.com/articles/guides/what-is-the-best-faction-in-gwent/
signature	Scoiatael	trap_secret	traps	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Scoiatael	ranged	ranged attacks	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Scoiatael	movement	mobility	https://www.keengamer.com/articles/guides/what-is-the-best-faction-in-gwent/
signature	Scoiatael	ping	many small damage instances	https://www.keengamer.com/articles/guides/what-is-the-best-faction-in-gwent/
signature	Scoiatael	tutor	playing cards straight from the deck	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Skellige	condition_life	Berserk	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Skellige	friendly_fire	damaging itself or allies for bonuses	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Skellige	revive	reviving from the graveyard	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
signature	Skellige	damage	damaging units many ways	https://www.keengamer.com/articles/guides/what-is-the-best-faction-in-gwent/
signature	Syndicate	coin_economy	coins spent on effects	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
archetype	Nilfgaard	control	control and counterplay	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
archetype	Nilfgaard	disruption	limiting the opponent's options	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
archetype	Monster	swarm	swarm and devour	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
archetype	Monster	sacrifice	consume and Deathwish	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
archetype	Scoiatael	trickery	traps and ambush	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
archetype	Skellige	graveyard	resurrection	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
archetype	Skellige	aggro_tempo	aggression	https://www.pockettactics.com/gwent-the-witcher-card-game/decks
archetype	Syndicate	ramp	coin economy	https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html
combo	Koshchey	Caranthir Ar-Feiniel	a large amount of points	https://www.bluestacks.com/blog/game-guides/gwent/gwt-top-5-best-decks-en.html
combo	Joachim de Wett	Coup de Grâce	strong plays always available	https://www.bluestacks.com/blog/game-guides/gwent/gwt-top-5-best-decks-en.html
combo	Iris von Everec	Iris' Companions	thinning for Round 3	https://www.bluestacks.com/blog/game-guides/gwent/gwt-top-5-best-decks-en.html
```

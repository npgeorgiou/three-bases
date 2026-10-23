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

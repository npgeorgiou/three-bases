# Process lessons: what each import and review taught, for every game

Part of PROCESS.md (split 30 Oct 2026 at 600 lines). Each section is one import or one review by Kaptain; every rule in it
holds for every game. Read the sections whose kind of game is close to yours before step 2.9 (decks and networks).

## Links the deck networks showed missing (29 Oct 2026; Kaptain's check of 9 decks; fixed in every game)
The records were right card by card, but the links between cards were not: a network is only as good as the rule that
joins "A makes X" to "B waits for X". What went wrong, how it was missed, and the rule now:
1. **The kind of thing hit was dropped.** `damage` causes dies, survives_damage and nexus_damaged whatever it hits, so a
   unit damaging its own base "made units die" (Reckless Rushers -> Green Prototypes) and Falling Star (an enemy unit)
   "damaged the Nexus". Missed because every case asked "who makes X", never "who must NOT". Rule: refs.py keeps unit-only
   and player-only happenings to their kinds; network.py joins only kinds that fit (kinds_fit).
2. **"Me" was lost in conditions.** "I've survived 10+ damage" (Braum) stored its event object without the pick, so it
   read as any unit surviving; "when I level up" (LeBlanc) took Ashe levelling up. Rule: flat_if keeps ev_obj_pick and
   attr; a need about the card itself is fed only by what is done to my units; two cards each about themselves never link.
   When the query layer flattens a record, every field that changes the meaning (pick, side, kind, attr, with) is kept.
   "It" keeps the side of the target before it ("give a random enemy +2, then give it Vitalize": the enemy), or a buff
   to an enemy reads as a buff to anyone (Green Prototypes -> Booming Professors).
3. **Planted and placed cards were no cards.** Chime, Poison Puffcap, Flashbomb Trap, Mysterious Portal are planted by a
   keyword action with a card; the network only followed summon/create. Rule: an effect that names a card puts that card
   in (keyword_action included); a planted card going off is trap_activated (normalize N15; "activated" is a player using
   something). Bard levels from Cosmic Binding's Chimes; Caitlyn from every trap planter.
4. **Readers narrowed a class to one card.** "5+ of your traps have been activated" was read as card Flashbomb Trap, so
   Poison Puffcaps did not count; "Trap" as a name family missed Puffcaps. Rule (BRIEF 23): "your traps / boons / spells /
   Imps" is the keyword, category or type filter, never one card or a name family. Fixed by rule (fixes/runeterra/v30.py).
5. **Keyword records were not the card's needs.** Plunder, Reputation, Nightfall, Deep ... are conditions in the keyword's
   record; the network took only a card's own rows. Rule: a keyword condition the card uses is the card's need.
6. **Things a card tests or picks by had no maker.** A stat tested ("the enemy Nexus has half its Health": Darius), a
   position picked by ("the enemy in front", "bordering enemies": Booming Professors, Chaotic Pupil), units that can't be
   blocked (they hit the Nexus), units that strike (they deal damage), moves, challenges, captures, Predict, Countdown: no
   act said it caused them. Rule: refs.py feeds a tested stat from what changes it and a position filter from moves; vocab
   `causes` was completed (move, swap, challenge, capture, Predict, Countdown, Trap, Boon, Elusive, Overwhelm). Every new
   event, state or test needs its makers before a game is done; audit_links.py lists those nothing makes.
7. **Groups of cards acted on were ignored.** Doctor Mia repeats structures, Ava Achiever doubles traps, Teemo 2 copies
   Puffcaps, Norra 2 changes Portals: only Attack/Support repeats were followed. Rule: repeat, increase_effect, copy and
   give_ability on a named group link to every card of the group, on either side when the group is named (traps on enemy
   cards are still mine).
8. **Cards that are what another waits for, and kinds of card another needs.** A spell is what "Fast spells, Slow spells or
   Skills you've played" counts (Ravenbloom Conservatory); a structure is what "units surrounding a friendly structure"
   needs (Fortification Tonic). Rule: played_lines and need_lines match the card itself against the filter.
9. **Helping is a link too.** Power buffs and Elusive, Overwhelm, Quick Attack, Challenger given to my units help every card
   that counts damage my side deals (Darius, LeBlanc, Reputation): weak "makes its damage bigger" lines.
10. **33 Runeterra keywords had no vocab concept row** (Plunder, Countdown, Last Breath ... ; Runeterra predates rule 2 of
   "Writing data the same way"), so concept questions missed them. Mapped from Riot's glossary (Claude's, for Kaptain's
   check); audit_links.py lists any keyword without one.
How it was missed: every test asked whether the query finds the cards that do X; none asked whether two cards of a real
deck are joined, or must not be. Read the networks of guide decks (step 2.9) before calling a game done.
Second check (Kaptain, 29 Oct 2026), fixed in every game: a champion linked to its own level-up form (one card in play);
spells and skills not counted for "N spells or Skills played" (a skill is an ability card the unit casts: it is put in the
network, kind spell takes it when the filter says Skill); "help" that is no event was missing (more health helps a card
that must survive damage; more power helps a card that counts damage dealt or Nexus hits, and Challenger and Overwhelm
units; Elusive or Overwhelm given helps cards that count hits on the enemy player; creating cards helps "N different cards
played"; a planter helps what its planted card levels); a card whose own trigger makes what its level-up counts (Ashe:
Attack -> Frostbite -> level) levels from anything that sets the trigger off (Rally); an ability given to the player that
adds to what happened (Tybaulk: "your spells and Skills deal 1 extra damage") makes those cards stronger, other given
abilities are fed like the card's own; "I strike / I kill" is about the card, not the unit it hits; "it" first refers to
what the event happened to; a "non-X" filter narrows nothing; what a card creates by description ("2 random Imps") is no
need for that type; the combo search (connections.py) is no source of network lines (its weak reasons, "counts card",
"target: type", were noise); a count of a keyword used names the card when the text does ("planted 15+ Poison Puffcaps").

Found by reading guide decks card by card, 29 Oct 2026 (v34, fixed for all games): a count of what happens to my cards of a kind
("destroyed 4+ allied landmarks") is fed by cards of that kind and cards that make one by description (Bomber Twins ->
Ziggs); "non-combat damage" is not fed by units fighting (Swain); a need that names who does it ("allied Pykes have dealt")
is fed only by that doer or a card that makes such a unit fight; "used a keyword" (Capture) matches makers of that keyword
(An Acquired Taste -> Tahm Kench); an ability that helps the card that comes ("the next card with Nightfall costs 1 less",
"when you summon an Elite, grant it +1|+1") makes every card of that kind stronger; what a card does to itself only feeds a
need its own kind fits (Heliotroopers poisoning itself is no Dragon for Sunbeam Serpents); "last card in hand" is helped by
discarding, "cards in hand" by drawing and creating (First Mutineer -> Northsea Dogs).

More found 29 Oct 2026 (v33, all games): an effect that adds to what my cards of a kind just did ("your spells and Skills
deal 1 extra damage", "double all damage dealt by your spells") helps every card of that kind in the deck that does it, also
through a keyword it uses (Drain) and through Skills; it waits for nothing itself (Tybaulk, Funsmith, The Dreadway); "it"
there is what was hit only while no earlier effect named a new target (Azir's summoned Sand Soldier is not the attacker);
a lasting change to all my cards of a kind, or to them in hand and deck ("grant allies everywhere +1|+0", "friendly units
in front get 2 strength each turn") helps each of them; a boost to a status ("Rage on friendly units adds +3 Attack")
helps the cards that give it; damage as big as a card's health is no "survives damage" help (Sunburst 6, Braum 6); a
card made by description ("2 random Imps") is a card of that type for what asks for the type; a counted card with a state
("8 cost reduced cards played") is fed only by cards that put it in that state; "spells and Skills" in a text includes
Skills in every target the phrase names (fixes/runeterra/v33.py); a level-up form's power and health are its stats field.

## A card list that looked whole (Inscryption, 29 Oct 2026; checked in every game)
1. **The library's entries were not the game's cards.** Its 164 Inscryption units came from the wiki, but cards with the same
   text had been merged (Hawk, Raven, Sparrow, Mothman into Bat; Skeleton into Revenant), cards without sigils were dropped
   (Wolf, Coyote, Grizzly, Stoat, Opossum), and a page's tabs were stored under the tab's label (Left, Right, Normal, Base
   Form). The starter decks named cards the database did not have. Rule: before the readers, every card of every guide deck
   must be a card of the game; audit_links.py check 5 lists deck cards that are not. When the source is not whole, the
   supplement holds every card and source.py FULL replaces the library's categories for that game.
2. **A wiki page can hold several cards.** Empty Vessel's page has a second box (the three Gem Vessels), Trees a second box
   (Act III trees): take every card box of a page, not the first, and every tab of a box. Read every field of the source's
   card, not only the text: Inscryption's box field special_behaviours names code that changes play (Ouroboros grows each
   time it dies, Cat becomes Undead Cat, Strange Frog leaves a Leaping Trap); without it the Ouroboros decks had no plan.
   Their effects come from the wiki page Special Card Behaviours and are now in the cards' text (case ni09).
3. **Keywords belong in the Keywords field.** Written as "Sigils: Airborne." every card needed a reader and inherited nothing;
   as "Keywords: Airborne." 222 of 285 cards need no reading and take their sigils' records. A game whose cards list keywords
   (sigils, traits that the game defines) writes them in the Keywords field.
4. **Keyword records were never audited.** audit_text.py read card texts only ("a keyword's text is the glossary"); in
   Inscryption every card is its sigils, so a misread sigil is every card's error. It now reads keyword entries too (the
   rulebook line when the entry has one; trigger and condition keywords say it by their form). It found errors in other
   games' keyword records: Runeterra SpellShield and Flow lacked Skills (v33's rule ran on card batches only, now on
   keywords too), Spawn's "For each Spawn" lacked its repetition (fixes/runeterra/v36.py).
5. **Readers used another game's words.** Hefty and Rampager moves were written with keyword Push (a Stormbound keyword),
   and "in the way" with in_front / behind (a column's words on Inscryption's row of spaces). Names: a keyword that is no
   keyword of the game is dropped from the effect, the effect stays (normalize N6); the row's neighbours are sides.
6. **One happening, two forms, found by the second reading.** "Moves" had the moving unit as actor in Sentry: normalize N16
   (the moving unit is the object) and case mx12.
7. **Costs were no needs.** A Zombie (2 Bones) had no line from the Gravedigger that makes Bones, a Hawk (2 Blood) none from
   the Squirrel sacrificed for it: the network never read a card's cost. Now a game rule can name a cost word
   (`"cost_has": "Bones"`, read/<game>/game_rules.jsonl): its conditions become the needs of every card whose cost names it
   (refs.py, network.py "pays its cost"); a resource kind (Bones, gems) is fed by gaining it, and a coloured resource only by
   its colour (a Green Mox cost by a Green gem: network.colour_fit). Cases ni01-ni05. Doing it found a shared bug: load.py had
   lost every card's cost and spell speed (both sat inside a comment since v35); the card table now also keeps the cost text.
8. **Giving up my own unit had three forms** (kill on my unit in Faeria, Monster Train's Sacrifice record, nothing in
   Inscryption): one act sacrifice (causes sacrificed and dies), normalize N17 for card records.
9. **Help through the card that is paid for.** Worthy Sacrifice ("counts as 3 Blood") and Morsel act on the card they are
   sacrificed for (pick actor of event sacrificed): network.actor_help_lines gives them a line to every card of the deck that
   needs that happening (M3atB0t makes Urayuli cheaper, case ni06). An ability that spends a resource ("Activate: pay 1
   Bone") needs it like a cost does (refs.py; Bone Lord's Horn -> Tomb Robber, ni07). A cost of 0 ("0 Blood") is no need (ni08).
10. **A keyword entry without its definition.** The library kept only the wiki's pointer line for Ants and Ant ("This
   article is about the variable stat..."), so the readers wrote nothing and no Ant counted the others. The definitions now
   come from the wiki pages (supplement), audit_links.py check 6 lists any such entry, case ni11. Where a new card is put
   ("Pelt Lice in adjacent slots") needs no units to move (refs.py PLACES, ni12).
11. **The deck explainer and the combo search did not know the game's rules.** "Gravedigger: no clear role" and "Adder waits
   for sacrifices, nothing in the deck does it": ask.py analyze now reads cost needs and counts what the rules make (any
   unit can be sacrificed, a Skeleton's death gives a Bone), deck cases di01-di04; connections.py goes one step through a
   rule about the owner's own cards (Necromancer's second deaths give Bones for Tomb Robber, combo cases ci07-ci08).
12. **Keyword records are not normalized by run.py** (it normalizes card batches only). A game whose cards are mostly their
   keywords (Inscryption) applies the normalize rules to keywords.jsonl in its fix script (fixes/inscryption/v36.py:
   names, moves object, sacrifice form).
13. **Board games, positions (29 Oct 2026, v38-v39; for every positional game).** Read every sigil that names a place and
   write it in BRIEF "The board" forms; check the place, not only the act: a strike into an empty opposing space hits the
   opponent (strike to the player, link or); "moves towards them" = sides of them; "rotate one space" = bordering; a space
   struck on my side is side mine (Burrower). The concepts follow from the forms for every game (flat.py): same_lane ->
   lanes, in_circuit -> link_formation, a strike on the sides of the opposing space -> cross_lane. Lines say where help
   works: an aimed line with a position filter ends "(when next to it)". A circuit needs two conduit cards (wiki Circuits),
   so "within a circuit" also counts two Conduit Cards of mine.
14. **Who benefits from a place: three network gaps (v39, every game).** A keyword's effect on other cards (Leader: "creatures
   adjacent gain 1 Power") made no line, only the card's own text did: aimed lines now read has_keyword rows too (ni15). A
   card that names another card in a filter ("if a Chime or Bell Tentacle is attacked") made no line from that card: it
   now says "is the Bell Tentacle it names" (ni16). A trigger on an enemy attacking my unit took the side of the unit
   attacked, so my own attacks fed it "by fighting": attacks, strikes, fights and challenges take the doer's side (refs.py
   DONE_BY, ni17). A network case's deck column may be a card list when no deck has the cards.
16. **Room and full sides (v40, every positional game).** The Moon "replaces all spaces on its side with itself": a unit's
   room is stat size (Monster Train's unit capacity), here the count of its side's spaces; "board full" = no empty space
   on that side (BRIEF "The board", Room). Size changes are concept board_limit.
17. **Decks that were not full.** Inscryption's decks were starters (4-7 cards) and players' cores without counts; Kaptain
   saw too few cards and lines. Only 5 full 20-card decks exist as text (Steam threads); step 2.9 now says what a full
   deck is and that starters do not count.
18. **A cost rule makes every unit a payer** (v42, Kaptain's Faeria point seen in Inscryption): "any unit can be sacrificed"
   and "any death gives a Bone" linked every creature to every Blood and Bones card. By the rules alone only a unit that
   costs nothing to play is played to be spent (Squirrel, Skeleton); others pay by their own text. A card that wants to die
   keeps its line from the cards that sacrifice it (Ouroboros). deck_read_inscryption.md F9-F10.
19. **Card states named as states** (v42): a deck says "Child 13", the source's first tab is "Dormant"; the state a card is
   played in keeps the card's name. Search for decks under every name a guide uses (Son1a = S0N1A, Fish Bot = Fishbot).
20. **The rules pay for nothing** (Kaptain's review, 30 Oct 2026): a game whose costs are paid with units (Inscryption Blood,
   Bones) must not link every unit to every card with that cost. Lines are combos between card texts only.
21. **A source's fields are not all card text**: Inscryption's wiki "traits" are code markers; read the source's page that
   explains a field (wiki Traits) before putting it in the text.
22. **What Inscryption taught (for the next game; 30 Oct 2026).** About the game: read the wiki's mechanics pages, not only
   card pages (Traits, Special Card Behaviours, Card Battle, Circuits, the cost pages, Kaycee's Mod tips); a roguelike's
   decks are built during a run, so real decks are rare as text: search guides that say which cards to add to a starter
   (the wiki's tips page) and players' end-of-run lists (Steam threads); expect thin networks when most cards only act on
   themselves, and say so with numbers (share of cards acting on other cards) instead of adding lines. About the work:
   Kaptain reviews the page, so look at it as he does before reporting (a line whose reason no card text shows is wrong);
   ask whether a rule-made line is a combo before writing one; the review method ("Fixing a review") found in one pass
   what three of my own rounds had missed; keep only decks that test something (decks_dropped_<game>.tsv for the rest).
15. **More or faster base resource** (Kaptain 29 Oct 2026: not linked to costs, but findable): concept base_resource_gain
   (mana, spell mana, Ember, faeria, Energy; a second resource such as Bones or gems stays resource_gain), `ask.py
   <game> factions base_resource_gain` gives each faction's share, and ask.py analyze names the ramp cards. Cases mx16, ri08.

## Importing Duelyst (29 Oct 2026; checked in every game)
1. **The game file's rules were written from memory.** duelyst.md "The game" (Claude's summary) said a unit on a mana
   spring gains the mana and minions are summoned next to a friendly unit; the game's own tutorial and tips say the player
   gains it and summoning is around any friendly unit. Runeterra's, Monster Train's, Faeria's and Inscryption's game rules
   cited the same kind of summary. Rule: game rules cite the game's own rules with their source (step 0.10); audit_links
   check 8 lists a game whose game_rules.jsonl cites a "The game" section written from memory (Runeterra, Monster Train and
   Faeria now cite Riot's round FAQ, a beginner's guide and Wikipedia's Gameplay section; Inscryption cites the wiki's
   Card Battle, cost and Circuits pages and Wikipedia).
2. **One name, two cards.** The open-sourced data has Tempest and its Bloodbound Spell copy, the tutorial's Argeon Highmayne,
   Cascading Rebirth's follow-up, 14 Build structures called Building: a deck or a text naming one got either. Rule: the
   collectible card keeps the name, the others are "<name> (<kind>)" (supplement_duelyst.py names()); audit_links check 7
   lists names two cards of a game share.
3. **Decks from deck codes.** Duelyst deck pages give a base64 code of card ids; the ids are the game's own (cardsLookup).
   Codes from Duelyst II pages decode to ids the original game lacks: such a deck is another version of the game, not a
   source. Codes and decoded decks are kept (supplement/duelyst_deck_codes.tsv) so the decks can be checked again.
4. **A card kind ending in "Spell" is no type.** build_input.types_of drops subtypes ending in " spell" (Runeterra's spell
   speeds), so "Bloodbound Spell" as a type was refused by check.py. A kind of card that cards filter by and that has a
   keyword entry goes in the Keywords field (the General's spells carry "Keywords: Bloodbound Spell.").
5. **Keywords written as lines.** "Provoke\nCelerity\n..." became "Keywords: Provoke, Celerity." for 178 cards (rule of
   "A card list that looked whole" 3): line breaks in the source must be kept until the Keywords field is cut.

## Duelyst deck read: leaders and the board (29 Oct 2026, v40; deck_read_duelyst.md; checked in every game)
1. **A leader card is its player.** A Duelyst General is a card on the board and the player's life: category `leader`
   (network KIND_CAT player). Help given to "your General" reaches only the leader card; a unit target never matches it;
   the General attacks, strikes and kills as its player (game rules: applies_to unit, leader). Champions stay `hero`.
2. **Who did it keeps its kind and side.** A target picked "actor" (the attacker, a counterattack) takes its event actor's
   kind and side; "it" in an ability on my own attack is the enemy attacked; "it" in a given keyword's record is never the
   holder (Backstab's damage landed on the attacker). Cases ndu01, ndu10.
3. **Positions a card needs are needs for moves.** Backstab (behind an enemy), Zeal (near my General), Infiltrate (enemy
   side): moving the unit or the General feeds them; where a card enters needs no moves (placement). Use the BRIEF "The board"
   positions; concept rules flanking, adjacency (with diagonal), lanes (with center_column), area_templates (corners,
   starting side). Cases du31-du34, ndu07, ndu12.
4. **Help must reach the card it can hit.** A gain on itself helps no other card; a player's extra card handling is no help
   to its leader; effects on the hand or on costs skip tokens only summoned on the board; "anything" chosen on the board is a
   unit or the leader; spells and artifacts are never board targets. Cases ndu04, ndu05, ndu17, ndu23-ndu28.
5. **What a card makes itself it does not wait for** (Abhorrent Unbirth's deaths, Krog's Dinner); a named card asked for in
   play is fed by the cards that make it (Inkling Surge and Wraithlings), not a card naming what it makes itself (Blazing Spines). Cases ndu25, ndu29, ndu30, nfa24.
6. **Card counts by where the card comes from.** "Summoned from your action bar" is played (N24): tokens do not count.
   Stats used as amounts want that stat; a cost equal to a stat wants less of it (Blood Taura). Cases ndu11, ndu18.

## Kaptain's check of the Duelyst networks (30 Oct 2026, v42; fixed by rule in every game; cases ndu31-ndu47)
1. **Help is no need.** An effect that helps the cards it names (Oakenheart: Mechs +1/+1; Golem Metallurgist: Golems
   cheaper; Timekeeper: buildings progress) is a help line from it; those cards' type or keyword is no ask or need of it, and
   the cards are no "card it counts". A card that makes an effect stronger does want it (Deranged Brute wants Rage).
2. **The rules are no combo.** Every unit attacks, is struck back, harvests and gives Bones by the rules: such a line is
   dropped (Punish waits for a damaged enemy: any attacker does that), unless the card's own ability makes it fight more
   (Celerity, Frenzy, Overwhelm, "this fights"), the need names the leader ("whenever your General attacks"), or it is a
   level-up count (n53). Power is no help to "an enemy is damaged" except for a level-up count.
3. **What the player picks to harm, on either side, is the biggest there is**: "destroy ANY minion, restore its Health"
   wants no Health (Martyrdom); a chosen help still wants the stat (Gabrian Enchantment).
4. **Stat gains by stat and by target**: +2 Attack is no Health (Roar); the Abomination's gains reach only it; Juggernaut's
   Grow only itself; strength is both stats. A level-up form keeps its card's types (Pyke (level 2) is a Lurker).
5. **A made card that is drawn takes its own lines**: its makers put it into play, it enables the card that asks for it
   (Lilithe -> Wraithling -> Inkling Surge); no line from the makers straight to that card. A card naming what it makes itself
   ("walls that can attack") asks for no other maker; "if you have another Wraithling" does.
6. **Keywords that make my unit better are help** (Ranged, Backstab, Rush, Provoke, Airdrop), and so are readying,
   speeding a countdown and damage prevention.
7. **Moves**: a unit's own movement keyword (Celerity) moves it; a position measured from my unit (Holy Immolation "enemies
   around it", Bonereaper "around this one") needs my units moved; a card moving itself moves as what it is (the Lion is no
   General: no line to Zeal).
8. **A leader's spell is its own card** (Duelyst: the General's signature card, fixes/duelyst/v41.py): drawn with the deck,
   "casts its own spell"; the General's text names it.
9. **A protection trigger waits for nothing** ("the first time your General takes damage, prevent 2"). A trigger that helps
   what set it off still waits for more of those events from other cards (Janna's discount on draws, Mirkblood on summons).

## One link per pair, one rule per need (30 Oct 2026, v46; deck_read_duelyst.md F10-F15)
1. Two cards have one link. Its kind is the first of its reasons in a fixed order (network.py KIND_ORDER); every reason is
   listed. A second arrow between the same two cards is a bug in a rule, not something to hide.
2. Each need is read by one rule: triggers and counts of played, summoned or drawn cards only by played_lines; types and names
   only by the type rule. A fact is said once: a stat gain is not said again as "more power", a cost cut not again as
   "pays for it", a rule line not beside the card's own ability doing the same.
3. A filter of what a card makes (create, summon, Invoke, Manifest) describes the made card: no ask, no keyword need.
4. Help on the card itself or on the player (heals, stats, keywords) helps no unit; extra attacks given to the player do.

## Link kinds and what this chat learned (30 Oct 2026, v47; Duelyst chat)
Link kinds (Kaptain): "triggers" = B reacts to what A does (a death effect, "when an ally dies", "when this is hit"; refs role
trigger); "enables" = B needs a thing to be there or counts things ("5+ spells played", "if you have another Wraithling");
the help kinds (heals, makes stronger, makes cheaper, gives keyword, moves into place, clears the way); puts it into play;
helps it level up. One link per pair (PROCESS_LESSONS "One link per pair, one rule per need").
Learned:
1. Take `dump_lines.py` before any change and read the gone and new PAIRS after it, not only the reasons: merging reasons
   hides real losses (a player-kind exclusion silently cut Rally's "another attack" lines).
2. Every new exclusion: ask what else shares the attribute you exclude by (target kind player = Nexus heals, but also Rally).
3. A rule made for one game's model (a leader card) must be gated by that model (`leader_game`), or it opens every game.
4. When Kaptain's new word contradicts an old case, rewrite the case with the date and his word; never keep both.
5. Kaptain's words on the page are the vocabulary: say what a card does ("plants traps that go off later"), never the
   opponent's act as the card's.
6. Kaptain reviews links, but names the cause by example: "kitchen dirty, bathroom dirty". For each point, list every other
   rule that could make the same kind of mistake (a filter read as an ask, a fact said twice, a need read by two rules) and check
   them all before reporting.

## Importing Faeria: the board (29 Oct 2026; checked in every game)
Faeria is played on a hex board that players build; Kaptain uses the library to study positional play, so its board words
were made the shared form for every game with spaces (BRIEF "The board"). What went wrong and the rule now:
1. **The library's texts were not the source's texts.** Its Faeria entries kept export markup ("Choose one: {green.|...")
   and wrote two land icons as "lake lake"; 19 cards were missing. Rule: render the game's own export and compare every text,
   not only the card codes (supplement_faeria.py writes the cards whose text differs). A supplement entry now replaces the
   library entry with the same bare code too (source.py), which also removed Runeterra's duplicate Dragon's Rage.
2. **One board happening, two forms.** "Moves onto enemy land" had the space as object and the mover as actor, "moves" the
   mover as object; "summon adjacent to friendly creatures" was aimed at units, Wind Gate's at spaces; "on or adjacent" was
   one target (Meteor) or two effects (Firestorm); "in its place" had no "of". Rule: BRIEF "The board" (one form each),
   fixes/faeria/v35.py, cases nfa03, nfa04, fa36-fa43.
3. **Board words had no values.** Readers wrote stand-in keywords (Empty, Refill, Extra turn, Destroy) and proposals
   (straight_line). Now: terrain (field and attr), set_terrain, harvest / harvests, moves_onto, same_space, straight_line,
   distance, empty_resource, refill_resource, extra_turn, end_turn, state empty; audit_links lists any stand-in keyword.
4. **Board concepts were never derived.** flat.py RULES now give terrain, territory_trigger, placement_rules, zone_control,
   control_reward, area_templates, adjacency in triggers and positional for ground and distance (cases fa36-fa42).
5. **Who benefits from moves and places.** Movement keywords cause moves and moves_onto (every game's movement keywords).
   network HELPS: what moves another of my units, or gives it a movement keyword, helps a card that must reach enemy land,
   an enemy well, a fight or the enemy player (row by row: the moved unit must be able to be that card; a unit's own Dash
   helps only itself); units that move well help "my units harvest enemy wells". Placement ("summon creatures next to this")
   helps a card whose entry asks for a place. A card counting my lands of a ground is fed by cards making that ground
   (network.terrain_fit: a lake maker feeds "special lands", not "forests"). A place chosen by the player ("on or adjacent
   to a chosen space") and where a card enters need no units to move. Cases nfa12-nfa15.
6. **Needs without a direction.** "Gain faeria equal to its Life" was fed by damage and by a debuff to the god; a threshold
   ("when you would take lethal damage") wanted more Life. Rule: a stat used as an amount or tested high is fed by stat changes
   and healing, never damage; a stat used as a threshold is no need (refs.py); an unnamed stat holder is a unit (nfa06).
7. **The network never read card costs**: "a card with base cost 7 or more" matched every card in every game (cards_of had
   no cost). Fixed for all games (nfa07, nfa08). A big cost cut to a random card in hand aims at cards costing at least that
   much (nfa11).
8. **Tutors.** A draw that names what it draws is from the deck (normalize N23, all games); it links to those cards in the
   deck, never to a card the deck only makes; a keyword on a card drawn or played ("draw a Flying creature") is the card's
   own, not one given in play (nfa05, nfa09, nfa16, nfa17). Triggers on drawing a kind of card are fed by the deck's cards of
   that kind (played_lines also reads drawn).
9. **"It" lost what it was.** "Transform another Rakoan ..., give it Flying" made any unit fly. Rule: "it" keeps the previous
   target's filters, and after a summon of a named card it is that card (flat.py); a need about the card itself is fed only
   by effects that can be that card (network lines_of and HELPS; nfa03).
11. **The deck explainer (ask.py analyze) had the network's old faults**: it joined a god healed with "units healed" (no
   kinds), let a unit moving itself feed another's Corrupt, took the rules' kills of enemies as friendly deaths (every unit
   "made" Soul Eater's deaths), counted cards that make a type by description as caring about it (no Rakoan plan), and had
   no role for paying for big cards. Rule: the explainer joins makers and needs by the same tests as network.py (kinds,
   sides of the rules' rows, "about itself", who the maker acts on); role "Pays for big cards". Deck cases dfa01-dfa05.
10. **Trigger labels written "Name -".** Faeria's "Corrupt - ..." was not the card's keyword (load.py read only "Name:"), so
   "whenever a creature triggers a Corrupt ability" had no makers (fa43).

## Kaptain's check of the Faeria networks (29 Oct 2026; 24 points, fixed for every game; deck_read_faeria.md)
1. **Labels read backwards.** Arrows go from the card that provides to the card that uses it; "is a card it needs" read as
   if the start needed the end. Kinds and page names (30 Oct, agreed): "does what it waits for" (a trigger or a counted
   event), "enables" (a thing that must be there), makes cheaper / makes stronger / gives keyword / moves into place /
   clears the way (help, by how). Reasons are the first card's active verb ("kills it for its death effect").
2. **Help aimed at one chosen or random card was a faint "can aim at it".** A buff, a movement keyword, a cost cut or a
   heal aimed at a card of a kind (Oakling's random green creature, Horsemaster's Charge, Khalim's Training on "a creature"
   of either side) is "helps" to each card it can hit, weight shared (network.helps_it; cases nfa19, nfa20, nfa30).
3. **Paying for big cards.** Mana gain and cost cuts help the game's top tenth of costs when they pay a third of the cost,
   and only the cards a cut names (nfa23, nfa33, nfa39).
4. **The board grows from my units (Faeria game rules: land next to my creatures, summon on my own land).** Whatever moves my
   units or land forward (move effects, movement keywords given or owned, land movers, units made with movement keywords)
   helps cards whose entry asks for a place measured from themselves (Bomb Slinger, Axe Grinder) and cards that need my
   units deep in enemy ground (enemy wells, enemy land); what moves a card helps "units summoned next to this" (Mistral
   Guide). Read only when the game's own rules say the board grows next to units (nfa21, nfa26-nfa28).
5. **A straight line of fire** (a keyword whose strike hits the nearest enemy in a straight line: Faeria Ranged) is helped by
   removing or moving enemy units and by moving the shooter by an effect (nfa22).
6. **Needs that are none.** An ability that only destroys its own card waits for nothing (Krog's Dinner, nfa24); harm aimed
   at "a creature" of either side is no friendly death for death counters (nfa25) but is aimed at my own unit whose own
   death effect it sets off (nfa40); "if Krog has died" kept its card filter. Wrong and removed 30 Oct: "units are struck
   back when they fight, so they can die" (Claude's own addition; it linked every creature to Soul Eater).
7. **A code line lost in a comment.** A scripted replacement left aimed_rows' filter inside a comment for a whole session.
   Rule: after any scripted edit of shared code, read `git diff` of that file before rebuilding.
8. Page: cost and Attack|Life on every card, keywords once, a deck drop-down per game, decks listed once, nodes pulled closer.

## Importing Into the Breach: lessons for every game (30 Oct 2026, v48-v53; deck_read_into_the_breach.md F1-F30)
- **Understand the game before building anything.** Kaptain: "the first step was to understand the game". Read the game's
  rules, its tiles and statuses, and three guides on how players win, and write the game's own combos into
  `library/tools/games/<game>.md` "Combos" before the deck read. Then ask of every card: what does a player use it with?
- **Cards that ride on other cards** (weapons on mechs; the same holds for equipment or attachments in other games): a card
  carried by a unit is a card of its own in the deck; the unit keeps only what it is (its keywords); network.CARRIED makes
  the carried card act as its unit ("the mech with Hydraulic Legs" kills, for Viscera Nanobots); a "carries" line joins
  them, so no unit is left without lines.
- **Full decks may not exist as text** (Into the Breach and Monster Train: players post screenshots). Take the real ones
  that exist (a run report naming each item), then, only at Kaptain's word, fill the rest with builds that make sense,
  marked as Claude's in the source column with the reason per item, and checked by script against the deck limits. Say
  plainly which decks are real and which are Claude's.
- **A status a unit only gets in play** (Fire, Smoke, A.C.I.D. on a mech) is no printed keyword: filters on it match any unit
  (network.printed_kws, STATUS_TREES); otherwise help to "Mechs on Fire" reaches no card.
- **Damage by origin matters** (Force Amp adds to bumps only; A.C.I.D. doubles weapon damage only): a line must check where
  the damage comes from, not only that damage happens.
- **Harm aimed at a target of no side** (most Into the Breach weapons: "a tile", "the target") goes to enemies, as refs.py's
  HARM rule says; every rule that counts enemy damage or debuffs must read it so (status_damage_givers, deck_analysis roles).
- **Self-harm the game lets you undo** (the Ice Mech freezes itself; a hit frees it) links the cards that can undo it.
- **Words in a card's prose decide its reading when the short text is unclear** ("3 tiles in a row": the Burrower's prose says
  a 3-wide area in front, the Hornet Leader's three tiles ahead). Never give two cards the same reading only because their
  short texts match; never give the same text two readings.
- **Ask the deck explanation too** (`ask.py <game> analyze` on every deck) after a network fix: it reads the records with its
  own rules (deck_analysis.py), and every network fix about sides, statuses or tiles must be made there as well (F18, F19,
  F23, F27).
- **cases/decks.tsv overrides decks.tsv** for a deck of the same name (dump_lines, cases and the page take the last row):
  change both when a deck changes.
- **Reporting:** when Kaptain asks "are we done", answer against step 5 ("Done when") item by item, and finish every open
  step before saying goodbye; "the next chat will do it" is not done.

## Importing Slay the Spire: lessons for every game (30 Oct 2026, v49-v53; deck_read_sts1.md F1-F20)
A deckbuilder with no board and no units of mine: cards, relics, potions, statuses on the player and the enemies, Orbs.
1. **What a status does belongs to the card that gives it.** Strength makes Attacks bigger: Flex -> every Attack; Vulnerable
   on enemies: Bash -> every damage card; Focus: Defragment -> the Orb cards. A helper is never drawn as needing what it helps.
2. **What a card puts in play acts through it.** "Channel 1 Lightning": the card deals Lightning's damage (flat.py expands the
   keyword an action puts in play, as it does for a keyword given). Without it, every question over damage, Block or energy
   missed the Orb cards. Check this for any game where cards put tokens, statuses or objects in play that act later.
3. **The player is the only unit of mine.** Say "gives you Strength", "makes you lose HP", never "your units". A game with
   no units of mine is found from its card kinds (network has_units).
4. **A kind that every playable card is, is no filter.** Every Slay the Spire card is a spell: "whenever you play a card" is
   every card and draws no link from each card; cards that make more cards to play (Blade Dance) feed it instead.
5. **Costs:** X costs are no number (the source wrote them as -1); cards with no number never match a cost filter; energy
   helps X cards ("a bigger X"); a status that sets costs (Confused) and an Orb's energy (Plasma) pay for big cards. What is
   expensive is set per game (network.EXPENSIVE).
6. **Read the game's own limits** from the wiki before drawing a status line: Dexterity adds only to Block a card gives when
   played; Vulnerable to attack damage, not Orbs; Lock-On to Orb damage only.
7. **Starting items belong to every deck of the character** (deck_analysis.starters: rarity starter, the deck's main
   region), unless a card says it replaces them. A missing character can come from the text of what replaces it.
8. **Drawbacks, limits and picks are no needs:** Void's energy loss, FTL's "fewer than 3 cards", Ethereal's "still in
   hand", Bottled Flame's choice of an Attack already in the deck (a tutor: "picks it from the deck").
9. **Counts:** a reaction ("every 3rd Attack") triggers, a count it needs enables, a cost that drops per X is "makes
   cheaper"; one reason is said once per line.
10. **Readers drop filters and scopes;** fix them by text rules (fixes/sts1/v50-v52): "affects this card" is self, "cost X
   cards" keeps its filter, "Stance" and "Orb" are the keywords whose texts say so.
11. **Guide decks are thin** (core cards, no full end-of-run deck exists as text): thin networks there are true, not errors;
   say so to Kaptain with the deck, before he asks.

## Who must do it (30 Oct 2026, v56; Kaptain on Zed and Hecarim, fixed for every game)
Wrong thinking: "a need's happening is enough; who must do it does not matter". Zed levels from his own or his Living Shadows'
Nexus strikes, Hecarim from Ephemeral attackers, Pyke from allied Pykes' damage: the who-filter was ignored in help lines,
in "makes units fight" lines, in deck plans and in combos. Fixed once in shared rules: `who_fits` (a keyword state such as
Ephemeral only on cards that print it), `can_aim_at` (the card, what it acts on, or with SEND_ACTS what it makes act, can be
that card: Dragon Ambush sends only Dragonlings; Rally sends any), `state_giver_lines` (Mark of the Isles makes an ally
Ephemeral: it feeds Hecarim), deck_analysis plan lines keyed by who ("Your Ephemeral units attack"), connections.may_be
("when I attack" is no Dragonling attacking). Also: "first each round" / "once per round" triggers (Hallowed, Lurk) get no
"another attack" lines; "name has" filters now read stored name parts (allied Pykes, Duelyst Eggs and Obelysks were never matched).
Same day: a card that acts on what something left (Undying Revenge revives a dead ally, Scorched Earth kills a damaged unit) had
its line drawn as one card among all that care about deaths: weight 0.009, reason "makes your units die". Now such a line says
what the card does to them ("makes your units die: Undying Revenge brings them back") and weighs as a direct combo (0.25).

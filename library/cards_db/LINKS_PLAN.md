# Lines between cards: how they are made, the planned line table

Read START_DATABASE.md and LINE_RULES.md first. Work in `library/cards_db/`.

`links.py` stores every line network.py draws between two cards that can share a deck (deck_analysis.can_share) in
`links.sqlite` (not in git; `links.py <game>` rebuilds it in seconds, Runeterra about 9 minutes, all games about 2 minutes).
Kaptain's design questions ("a faction that attacks again and again") are answered from these lines, so they must be right.

## How lines are made (network.py; read before changing it)
`network(c, game, ids)` joins, for the cards of one deck, the lines of these functions, then cleans them:
- `lines_of()`: what A's text makes happen that B's text waits for, counts or levels from ("kills it for its death effect",
  "damages the enemy player (levels it up)"); A makes or puts B into play; types B asks for; positional lines (A moves units, B
  acts by place, `moves_said()`; ground that kills what is pushed onto it, `DEADLY_GROUND`); revive or summon by kind to cards
  with a summon effect (L17).
- `aimed()` with `aimed_rows()`: A's effect aimed at my cards of a kind. Help (stats, keywords, heal, cost) and every other act
  on a card (strike, return, copy, damage) link only where `use_of()` (`uses_help()`) finds that B's own text or keywords use
  it, and the line says why (L14, L16). A keyword's effect on cards with the same keyword gives no line (L15).
- `boost_lines()` with `HELPS` (need event, sides, helping concepts, words) and `KW_NEEDS`: help that fills a need written on B
  (Overwhelm or Elusive to "hit the Nexus", health to "survive damage", more power where B's keywords use power: `HIT_KW`; a stat
  B's text reads; paying for expensive cards: `EXPENSIVE`).
- `played_lines()`, `need_lines()`: B counts or asks for cards of a kind ("6+ cost spells played", "6+ mana of spells", "if you
  have a landmark"): the cards of that kind (only a minority kind, L1b, L21) and cards that make one (`made_cards()`).
- `object_help_lines()` ("when you summon an ally, grant it +1|+1") and `gives_lines()` ("your spells deal 1 more damage"):
  filtered by `use_of()`; more damage alone is never a use (L18).
- `state_giver_lines()`: a keyword given to my units that B's need asks for (Mark of the Isles -> Hecarim). `actor_help_lines()`:
  what happens to A acts on its actor (Worthy Sacrifice -> the cards that need sacrifices). `stat_reader_lines()`: a stat raised
  by another stat, fed by units that grow that stat (Gabrian Enchantment, Oak Father). `doer_help_lines()`: help to the card
  that does it ("heals it when it kills"). `self_harm_lines()`: harm the player aims at my own unit whose own effect fires on it
  (Falcon Dive -> a Last Words unit with 1 Life). `spent_lines()`: a count of mana spent on a kind, fed by a card that alone pays
  that much (Lux).
- Clean-up in `network()`: a need a card shares with the skill it casts is said once, on the skill; a champion and its forms
  keep only "levels into"; A makes B, B acts on C gives A no line to C, except what levels a champion through a planted card
  (L3); "draws it from the deck" is dropped for a card the deck only makes; a form that is grown or levelled into gets no cost
  help; finds from the deck are shared over the deck's cards of that kind; `CARRIED` (a mech carries its weapons);
  `help_kind()` names a help's kind from its reason's first words.
- `one_link()` joins a pair's reasons into one line, its kind the first of `KIND_ORDER`, every reason said once; a bare "can aim
  at it" is never shown (L16). A reason uses {A} and {B}; network() fills in the names.
Every reason's code line is noted in `SITE` (class `Out`): `pair.py <game> "A" "B"` shows a pair's reasons with their lines,
and links.sqlite stores the line as `link.site`. To change a line:
1. Find the code line with pair.py and the rows of both cards (`flat_ref`, `flat_do`); fix the rule there, never a card name.
2. A rule for every game: no game gets line code of its own. A new keyword joins through its concept (vocab.tsv): reactions
   through `TRIGGER_KW`, evasion through `KW_NEEDS`/`HELPS`, help through `use_of()`. A new kind of help gets its use written in
   `use_of()`, never a line to every card. Per game numbers only in `EXPENSIVE`, `CARRIED`, `DEADLY_GROUND` and the like, each
   with its source.
3. Then START_DATABASE.md "Fixing errors" 6-7 (dump diff, cases) and `check_all.py --no-load`.

## Step 3. The line check after importing a game
Moved to START_DATABASE.md "The line check" (one start file for every change to the database).

## Open (seen, not fixed)
- Into the Breach: pilots have no lines. Kaptain (31 Oct 2026): a pilot is like an item a mech carries; it can move to any mech,
  and a mech can have none. So a pilot's effect on its mech can link to the weapons a mech carries (Bethany Jones' starting
  Shield keeps Cryo-Launcher's freeze off; Isaac Jones' extra Reset Turn feeds Adam).
- Into the Breach: Repair Field counts any heal as a repair; Gana acts once at deploy, yet weapons get lines that move units
  next to it; Targeted Strike "summons" Air Strike (a map hazard; decks only).
- Runeterra has Molten Shield twice (a plain and a "(created)" entry).
- Faeria (asked Kaptain): Shifting Tide -> Oasis Explorer (moving a land does not change land counts by the text); Gabrian
  Archon has Charge 2, so it "moves into place" for Wavecrash Colossus like the Jump frogs of Battle Toads.
- Slay the Spire: Through Violence (made by Reach Heaven) is not in the library; add it to supplement_sts1.py when a source is
  reachable (wiki.gg and fandom were not, 30 Oct 2026).
- Inscryption: The Moon's "pull small creatures into its orbit" states no place; written as Squirrels moving bordering (unsure).

## Next: the line table for design questions
### Step 4. Missing concepts (show Kaptain first; change nothing before his OK)
Propose each with 3 example cards per game that has it:
- `cost_increase_self`: my own cards cost more (a drawback; QUESTION_BANK K4). Today cost_increase means only the opponent's.
- `copy_enemy`: a copy of an enemy's card or unit (K5). Today copy does not say whose.
- `steal_card`: taking a card from the enemy's hand or deck (K5). Today steal mixes units, cards and resources.
- attack_now split in three (K10): `free_attack` (Rally, "start a free attack"), `strike_now` (Single Combat: two units strike,
  no attack), `summon_attacking` (Zed's Living Shadow).
- `cost_cut_big`: a cost cut aimed at expensive cards (K1: Bold Bargainer's "costs 7 less", Age of Dragons' "cost 0").
- One "expensive" per game: network.EXPENSIVE and the concept high_cost (top 10% of costs) disagree; propose EXPENSIVE for both.
A new concept: a line in library/concept_tree.txt and a shape rule in flat.py RULES (read the existing ones first), a rebuild,
then read what it found in every game. Report each concept, its cards per game, what looked wrong.

### Step 5. Questions over the table
Add to ask.py (`c.execute("attach database 'links.sqlite' as L")`; ask.py has `under(concept, x)`):
- `ask.py <games> links <concept A> <concept B>`: lines from cards with A (flat_concept, under) to cards with B: per game the
  number of lines, the 5 most used phrases each with one example pair, and the 3 factions where both ends are most common
  (ranked by the faction's share of cards with the concept divided by the game's share).
- `ask.py <games> partners-count <concept>`: per game, how many cards link to cards with the concept, and the median number of
  partners of a card with it.
- `ask.py <games> plan <question id>`: reads the question's parts from QUESTION_BANK.md and runs each part (`compare`,
  factions), each pair of parts (`links`, both ways), cards that do two parts (`both`), and pairs of parts with no line in any
  game (new ground). Plain text, grouped by part and pair.
Report the output of `plan K1` and `plan K10`, the first 40 lines each.

### Step 6. Answer Kaptain's test questions (QUESTION_BANK.md K1-K12)
Run `plan` for each, then write each answer in the shape of factions/START_DESIGN-4-asking.md "What Kaptain wants". Read each like a designer:
an answer that reads like a card list, or a part that found nothing, is a fault of the data or the question; fix its cause
(steps 3-5). Show Kaptain three answers first (K1, K8, K10).

### Step 7. Docs
Update START_DATABASE.md (State, Open work) and factions/START_DESIGN-4-asking.md ("How to build an answer" starts with `plan`). Remove
finished steps here.

## Do not
- Change line rules to make the table smaller (links.sqlite stays out of git), store text per line, or store lines between
  cards that cannot share a deck.
- Change concepts or vocab without Kaptain's OK.

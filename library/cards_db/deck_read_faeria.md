# Faeria deck networks: every wrong or missing line, by cause (29-30 Oct 2026)

Kaptain's two checks (24 points on 29 Oct, 10 points on 30 Oct) and Claude's reading of the 12 decks. Each family names the
rule that made the wrong line, what the same rule did elsewhere (all six games, counted by `/tmp` dumps of every deck network
before and after: 9567 lines before, see CHANGES.md v41), and the rule that replaced it. `review_check.py` fails a family that
lacks one of the three.

## F1 The kind of a line came from the code path, not from the card's text
Kaptain 22, 30 Oct 1, 3, 6: spells -> Windstorm Colossus were both "enables" and "does what it waits for"; Manta Rider ->
Windborne Emissary both; "helps" covered cheaper, stronger, keywords, moving and clearing alike.
- Root cause: network.py lines_of wrote every need as "waits" whatever its role (trigger, counted event, thing that must be
  there); need_lines wrote counted events ("each event you've played") as "type" too, so one phrase gave two kinds; every
  help was "boosts".
- Same error elsewhere: 399 lines in other games were "waits" for a thing that must be there (Runeterra 293, Stormbound 54,
  Duelyst 28, Monster Train 12; Faeria 13); every help line of every game was one kind.
- Fix: the kind comes from the need: a trigger or a counted event is "does what it waits for"; a thing that must be there
  (role state: "while you control another flying creature", "a damaged enemy") is "enables"; help says how: makes cheaper,
  makes stronger, gives keyword, moves into place, clears the way (network.py help_kind); help that makes a need happen
  more (more power for "when you hit the enemy player") is "does what it waits for". Names agreed by Kaptain 30 Oct.

## F2 Reasons written as passive happenings, with card names
Kaptain 30 Oct 6, 7: "your units die" for Lord of the Wastes -> Village Elder; labels carried both card names.
- Root cause: the reason was the need's description (deck_analysis.SAY), never what the first card does.
- Same error elsewhere: every waits line of every game.
- Fix: network.py ACT and ACT_SELF: the first card's active verb ("makes your units die", "kills it for its death effect",
  "has Flying", "dies by its own effect"); the page shows only the reason and the kind.

## F3 Lines from what every unit does by the rules
Kaptain 23, 30 Oct 5: every creature -> Soul Eater and Shaytan Monstrosity ("your units die (by fighting)"); 15:
Gabrian Archon and every unit -> Wavecrash Colossus ("by the game's rule: units harvest").
- Root cause: game-rule rows (refs.py, origin game) feed every need they fit; Claude added a rule of its own (fighters are
  struck back: damaged, dies) that made it worse.
- Same error elsewhere: Runeterra 89 lines (The Harrowing, Jarvan IV, Star Spring, The Scargrounds fed "by fighting" by
  every unit); Faeria 17; Duelyst 0 after its own fixes. Kept, as Kaptain asked earlier: my units attacking and hitting the
  enemy player by the rules (Gangplank, Darius). Not changed, for the Inscryption chat: every creature -> every Blood or
  Bones card by the cost rules (252 lines) is the same pattern.
- Fix: the rules' harm to my own units (dies, damaged, survives damage, killed, sacrificed) feeds nothing, except a cost the
  rules pay; a rule that needs a place (harvest a well next to the unit) feeds nothing either (what moves units there helps);
  the struck-back rule is gone. Cards that do kill my units feed them (Lord of the Wastes, Demon Wrangler, Wind Soldier,
  Seed of Paradise; Ruunin dies, comes back and dies again).

## F4 Harm aimed at "a creature" of either side
Kaptain 23: Soul Drain -> Shaytan Monstrosity; 30 Oct 10: Falcon Dive -> units with Last Words missing.
- Root cause: refs.py first read either side as mine, then (23) Claude made all of it enemy.
- Same error elsewhere: every either-side damage, kill or sacrifice in every game; new lines: Runeterra 17 (Mystic Shot ->
  Blade Squire, Get Excited! -> Twinblade Revenant), Duelyst 4, Monster Train 1, Faeria 3.
- Fix: such harm counts as aimed at enemies for cards that count friendly deaths, and is aimed at my own unit when that
  unit's own effect fires on it, only if it can kill it (damage at least its Life) for a death effect (network.py
  self_harm_lines). Shield keywords that fire on damage (Barrier, Forcefield) are no effect anyone damages a unit for.

## F5 A number taken from a stat read as something waited for
Kaptain 30 Oct 4: Gift of Steel, Triton Banquet, Seifer -> Gabrian Enchantment "does what it waits for".
- Root cause: refs.py turned "Attack becomes equal to its Life" (amount_stat) into a need for stat changes and healing.
- Same error elsewhere: Shaytan Monstrosity, Windborne Emissary -> Shaytan; Duelyst Martyrdom and Abhorrent Unbirth (5).
- Fix: an amount from a stat waits for nothing; what raises that stat "makes stronger" (boost_lines more health, more power).

## F6 Filters dropped by a general rule
Kaptain 30 Oct 8: Krog's Dinner "pays for" every expensive card; 20c-d: "if Krog has died" read as any death.
- Root cause: rules that read effects (payers, stat help) took the act and dropped the effect's target filter.
- Same error elsewhere: Stormbound Spare Dragonling (+ to a Dragon) helped non-Dragons survive (3 lines); every rule in
  boost_lines checked (movement rows already kept theirs).
- Fix: a cost cut or help that names whom it lands on (card, type, name, keyword, region) reaches only those (network.py
  pays, lands_on).

## F7 Paying for big cards: too loose, then too narrow
Kaptain 2, 14, 20a-b, 30 Oct 2: Underground Boss and Brigand (gain 2 in a fight) -> Bomb Slinger; first no line from cost cuts.
- Root cause: v38 had no rule; v39 linked any gain to the game's top quarter of costs (5 and up in Faeria).
- Same error elsewhere: 85 Runeterra and 26 Stormbound lines from small gains to mid-cost cards; 41 in Faeria.
- Fix: a gain or cut helps the game's top tenth of costs (Faeria 7+) when it pays at least a third of the cost.

## F8 Help aimed at one chosen or random card only as a faint "can aim at it"
Kaptain 5, 8, 21: Oakling, Syland Horsemaster, Khalim's Training.
- Root cause: aimed help was drawn as "targets" only.
- Same error elsewhere: every game's chosen or random buffs (v39 helps_it).
- Fix: help my side aims at one card is a help line (makes stronger, gives keyword, ...) to each card it can hit.

## F9 Positions: where cards enter, how the board grows, lines of fire
Kaptain 9, 10, 11, 16, 19, 24: Axe Grinder, Bomb Slinger, Battle Toads, Sunken Tower, Flame Thrower, Mistral Guide.
- Root cause: the game's own rules (land next to my units, summon on my own land, Ranged hits the nearest in a straight line)
  were not researched before reading.
- Same error elsewhere: any positional game; the rules are data (read/<game>/game_rules.jsonl), so only games that write
  such rules get these lines (Faeria now; Duelyst and Inscryption write their own).
- Fix: Faeria game rules; network.py board growth, line of fire, movement help read them (v39).

## F10 Needs that are no needs
Kaptain 20d, 23: Krog -> Krog's Dinner; Wavecrash Colossus "reached" by every mobile unit.
- Root cause: an ability that only destroys itself was read as waiting; a position need was fed by every unit (F3).
- Same error elsewhere: cleanup abilities in all games (v39); position rules (F3).
- Fix: cleanup abilities wait for nothing (refs.py); F3.

## F11 Draw from my deck weighed over the game
Kaptain 30 Oct 9: the green arrow Time of Legends -> Eredon was there but hard to see.
- Root cause: a tutor's line was split over every legend in Faeria (51), so it was drawn thin.
- Same error elsewhere: every "draw a <kind>" in every game.
- Fix: it is split over the deck's cards of that kind (network.py network).

## F12 Page
Kaptain 7, 12, 13, 17, 18, 30 Oct 7.
- Root cause: page code, not data.
- Same error elsewhere: one page for all games.
- Fix: cost and Attack|Life on nodes; keywords and decks once; a game and a deck drop-down; centre pull; links hover and
  click like nodes, with both ends lit; link labels only the reason and kind.

## F13 Tests that could not fail
Claude, 30 Oct: nfa29 ("Archon must not move the Colossus into place") passed on an old wording after F1-F2.
- Root cause: a must-not case matches a reason text; when the wording changes it passes whatever the network says.
- Same error elsewhere: Runeterra n15, Duelyst ndu25, Inscryption ni10, ni12, ni17, Faeria nfa03, nfa04, nfa06, nfa12.
- Fix: cases/run.py lists must-not cases whose reason no deck of the game says; rewrite them or confirm the lines are gone.

## Open
- Kaptain 4: Shifting Tide -> Oasis Explorer: moving a land does not change land counts by the text (asked).
- Gabrian Archon has Charge 2, so it "moves into place" for Wavecrash Colossus like the Jump frogs of Battle Toads (asked).

## Deck check, 30 Oct 2026 (v54; 30 decks from Kaptain's list added, 42 in all)
- Names cut short by the page, matched to the card by the part that was kept: Crystal Spirit -> Crystal Spice, Flight of the
  Mask -> Flight of the Mantas, Gagana, Rainbow Birds -> Gagana, Rainbow Birdship, Oversky Township -> Oversky Towship,
  Radiance, Scourge of the Sky -> Radiance, Scourge of Oversky, Sorocco, Fiery Beast -> Sorocco, First Mate (the only Sorocco).
  "[NO DLC] Voice of Hunger Combo/Control" is the deck already listed as Voice of Hunger Control: not added twice.
- F-own-life: Radiance, Imperial Airship (costs your Life) drew "moves it within reach of the enemy player" and "helps it hit
  the enemy player" from every mover and attack buff: the help rule took damage to MY player as a hit on the enemy. Fixed in
  network.py (HELPS loop: nexus_damaged on my side is never helped by attacks or moves), every game; 9 lines gone, all
  Radiance's; case n241.

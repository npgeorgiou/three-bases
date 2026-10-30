# Inscryption: deck read (29 Oct 2026, v38 code)

All 19 decks of decks.tsv read card by card as a player (lines of `ask.py inscryption network`, both directions, and
`ask.py inscryption analyze`), plus every Inscryption record that uses a board position, a move or a strike. Every wrong or
missing line is listed first; the families below say how each is fixed once, for every game where the rule is shared.

## What is right (no change)
- Blood: every unit of a deck can be sacrificed for a Blood card ("sacrificed (pays its cost)"), Worthy Sacrifice cards
  (Black Goat, M3atB0t, Pharaoh's Pets) make Blood cards cheaper, a 0-Blood Pelt needs nothing.
- Bones: every card that perishes gives a Bone to Bones cards and to Bone-spending sigils (Disentomb, Enlarge); Gravedigger,
  Sporedigger, Dire Wolf Pup (Bone Digger) and Raccoon (Scavenger) give Bones of their own.
- Mox: each Mox pays only its own colour (Sapphire -> Blue Mage, Ruby -> Mage Knight, Emerald -> Junior Sage); Gem Dependant
  cards (Mage Pupil, Mage Knight, Skelemagus) need any Mox card.
- Ants count each other (Ant Queen, Worker Ant, Flying Ant); Ant Queen creates Worker Ants; Warren creates Rabbits; Tomb
  Robber creates Skeletons; Mantis God sacrificing Ouroboros grows it; Wolf Cub, Dire Wolf Pup and Curious Egg grow into
  their forms.
- Act II Technology and Kaycee's Free Reptiles have no lines: their cards have no text that links them (Energy costs are
  not linked, Kaptain 29 Oct 2026; free cards are only sacrifice fodder for Blood cards the decks do not hold).

## Wrong or missing, by deck
| deck | from | to | what is wrong |
|---|---|---|---|
| Act III starter | Double Gunner, Sniper Bot | (explainer) | "no clear role": they strike enemy units across lanes; the control role does not count strikes |
| Act III starter, One True God, Eggs (Hydra) | Double Gunner, Mantis God, Hydra | the opponent | a strike into an empty opposing space hits the opponent (Card Battle, Omni Strike); Bifurcated / Trifurcated Strike, Sniper and Double Strike strike only units |
| Bones wall (Burntcookies1) | Headless Horseman, Kingfisher | | Double Strike-like and Airborne fine; Dire Wolf's Double Strike is written as Runeterra's Double Attack (strike first and together), not "strike an extra time" |
| Act II Magick starter | Emerald Mox, Ruby Mox | (explainer) | "Supports your units": their Act III Gemified bonus has no target in the deck (no Gemified card); a support needs a card it can act on |
| Kaycee's Eggs | Squirrel, Pelts | Curious Egg | Curious Egg hatches when the deck has every tribe and Power and Health 1 to 5 (Finical Hatchling); the record has no condition (unsure), so no card of the deck is shown helping it |
| Kaycee's Free Reptiles | Tadpole | Bullfrog | Tadpole grows into a Bullfrog (wiki Fledgling); the link is missing (the grown form is on another page) |
| any deck with conduits (none of the 19; checked on Buff Conduit, Tough Cell, Splinter Cell) | Buff Conduit, Energy Conduit, Factory Conduit | Tough Cell, Splinter Cell, Kind Cell | a powered card needs two conduit cards to be in a circuit; no line from conduits to powered cards |

## Wrong board data in the records (positional)
| sigil | what is wrong | the shared form (BRIEF "The board") |
|---|---|---|
| Bifurcated Strike, Trifurcated Strike, Trifurcated When Powered, Sniper | an empty struck space hits the opponent: no strike to the player | strike to the unit, or (link or) to the enemy player |
| Double Strike | act double_strike (Runeterra Double Attack) | a second strike on the opposing space, or the opponent |
| Clinger | "moves towards them" written as onto their space (same_space), unsure | move "to" sides of it |
| Loose Tail | "moves to the right" with no space, unsure | move "to" sides |
| Hefty | the cards in its way are not pushed | a second move on the units on its sides |
| Sentry | "moves into the space opposing" written as moves | moves_onto, the mover as object, same_space of the opposing space |
| (concepts) | same_lane ("the opposing creature") gives no lanes concept; in_circuit no link_formation; strikes on the spaces left and right of the opposing one no cross_lane | flat.py RULES for every game |
| (network wording) | "Leader makes it stronger" does not say "when next to it"; who benefits from a position is not said | aimed lines name the position of their filter |

## Families (by cause; the first eight v38-v39, F9-F12 v41)

## F1 Strikes into empty spaces did not reach the opponent
Root cause: readers wrote Bifurcated, Trifurcated (When Powered) and Sniper as strikes on units only; Double Strike as Runeterra's double_strike.
Same error elsewhere: no other game strikes spaces (Stormbound, Faeria and Duelyst attack units or the base directly); 5 sigils here.
Fix: fixes/inscryption/v38.py: a strike to the enemy player, link or; Double Strike a second strike. Case mi21.

## F2 Board places written in a column's or another game's words
Root cause: readers wrote "towards them", "to the right", "in the way", "into the space opposing" with same_space, Push, in_front.
Same error elsewhere: Faeria and Duelyst write the BRIEF "The board" forms (v38); Stormbound's columns are right there.
Fix: v38.py and v39.py by text: sides, bordering, moves_onto with the mover as object; Burrower's space mine. Cases mx12, mi22, mi23.

## F3 A deck condition left unsure
Root cause: Finical Hatchling's "every tribe and Power and Health 1 to 5 in the deck" had no reading.
Same error elsewhere: no other game has a deck-content condition of that shape (checked: no "in your deck" count of every value).
Fix: v38.py: ten counts and six tribe counts in the deck.

## F4 Card data the source split over pages
Root cause: the wiki puts a grown form on another page (Tadpole -> Bullfrog) and circuits on a category page.
Same error elsewhere: Runeterra level forms and Duelyst follow-ups come from the same card's data; no split pages there.
Fix: supplement_inscryption.py: FLEDGLING_TO, Conduit Card type; "within a circuit" counts two Conduit Cards (v38.py).

## F5 Position filters made no concept
Root cause: flat.py RULES had no rule for same_lane, in_circuit and strikes on the sides of the opposing space.
Same error elsewhere: Duelyst and Faeria positions now map too (checked with cases/run.py on every game: all pass).
Fix: flat.py lanes, link_formation, cross_lane for every game.

## F6 The explainer did not count strikes or check a support's target
Root cause: deck_analysis.py control role ignored strikes; support roles kept rows whose target needs a keyword the deck lacks.
Same error elsewhere: Runeterra and Stormbound supports with keyword targets were also listed; all games' deck cases still pass.
Fix: deck_analysis.py, for every game.

## F7 Lines did not say where help works
Root cause: network.py aimed lines dropped the position filter in their wording.
Same error elsewhere: every positional game (Faeria, Duelyst, Stormbound) had the same wording.
Fix: network.py where(): "(when next to it)", "(opposite it)".

## F8 Keyword effects on others, named cards and the attacker's side
Root cause: aimed lines read only a card's own rows; a card named in a filter made no line; an "attacks" trigger took the attacked unit's side.
Same error elsewhere: has_keyword aims: Runeterra 76, Monster Train 22, Duelyst 1 rows; named cards in every game; enemy attackers: Duelyst 2 triggers.
Fix: network.py aimed_rows reads has_keyword; named lines; refs.py DONE_BY. Cases ni15, ni16, mi25.

## F9 Every unit linked to every Blood and Bones card by the rules
Root cause: network.py lines_of joined the cost rules' needs (Blood, Bones, Bones spent by Enlarge) to the rules' makers on every unit: any unit can be sacrificed and any death gives a Bone (Wolf -> Great Kraken, Urayuli -> Bone Heap).
Same error elsewhere: cost rules exist only in Inscryption (game_rule.cost_has); dump_lines diff: Inscryption 371 -> 168 lines (106 sacrifice, 75 Bones cost, 23 Bones spend gone), every other game 0 changed. The same pattern Kaptain rejected in Faeria (rules' harm) was fixed there in v41.
Fix: a cost or resource need is fed by the rules only from a unit that costs nothing to play (Squirrel, Skeleton, Rabbit, Bone Heap, Pelts: played to be spent); other units only by their own text (Worthy Sacrifice, Bone Digger). Claude's rule; checked on all 31 Inscryption decks. Cases ni19, ni20, ni21.

## F10 A card that wants to die lost its line from the cards that sacrifice it
Root cause: v41 dropped the rules' harm to my own units (Faeria), which also removed "a Blood card lets you sacrifice Ouroboros" (Ouroboros grows each time it dies).
Same error elsewhere: only cost rules that sacrifice (Inscryption Blood) and a card whose own trigger is its own death: Ouroboros, Ourobot, Cat; no other game has a cost rule.
Fix: network.py: the rules' harm still feeds nothing, except a cost rule's sacrifice feeding a card's trigger on its own death ("can sacrifice it for its cost (sets off its death effect)"). Case ni18.

## F11 Decks named cards the database stored under a state's name
Root cause: supplement_inscryption.py named every state tab "<card> (<tab>)", so "Child 13", "Swapbot", "GR1ZZ", "S0N1A", "QU177" were no cards; parse_deck needed exact spacing ("Fish Bot" for Fishbot).
Same error elsewhere: Runeterra champions keep their name ("Kalista", level form "(level 2)"); Duelyst collectible cards keep the name (v37 rule); spacing variants: none in other games' decks.
Fix: the first tab that is the state a card is played in (Dormant, Defense, Base Form) keeps the card's name, its id kept; parse_deck accepts a name with other spaces, every game.

## F12 Decks that were not full
Root cause: Claude took starter decks and players' core cards as decks without counting copies (step 2.9 did not say what a full deck is).
Same error elsewhere: Monster Train has only guides' core cards (HANDOFF says so); Runeterra, Stormbound, Faeria and Duelyst decks are full lists or deck codes.
Fix: PROCESS 2.9 and HANDOFF: a full deck has its copies and the game's deck size; starters and cores are marked. Inscryption: 7 decks with their 20-card counts, 10 core decks from a guide added (marked core).

## F13 Lines from what every unit does by the rules (Kaptain's review, 30 Oct 2026, points 2, 3, 4, 5)
Root cause: network.py lines_of joined the cost rules (Blood: any unit can be sacrificed; Bones: every death gives a Bone) to every card that costs Blood or Bones; F9 only narrowed it to free units, and F10 kept every Blood card -> Ouroboros. A player sees no card text behind "Skeleton -> Revenant", "Bone Heap -> Pharaoh's Pets", "Rabbit -> Hawk", "Mole Man -> Ouroboros".
Same error elsewhere: cost rules exist only in Inscryption; other games' rule lines were removed by Kaptain's rule in v41/v42 (Faeria, Duelyst). dump_lines diff: Inscryption 279 -> 136 lines (82 sacrifice, 46 Bones, 12 Ouroboros); no other game changed by it.
Fix: what the rules let every unit do pays for nothing; only a card that pays by its own text keeps a line (Gravedigger and Bone Lord's Horn give Bones, Black Goat counts as 3 Blood, Mealworm gives its stats). Cases ni02, ni03, ni09, ni18, ni19 now say no line.

## F14 A unit's own fighting harm aimed at my units
Root cause: refs.py took "it" in "when this damages another creature, that creature perishes" (Touch of Death) as a creature of either side, so Adder "killed Ouroboros for its death effect"; units only damage the cards they fight, which are enemies.
Same error elsewhere: the rule already held for attacks and strikes ("Backstab: deals extra damage to it"); now also for damaged and fights, every game (dump: no other game's line changed).
Fix: refs.py: "it" in an ability on my own attack, strike, damage or fight is an enemy.

## F15 Cost help to forms that are never played
Root cause: network.py dropped "(pays its cost)" lines to grown forms but not "makes it cheaper" ones (Black Goat -> Pupa, Mothman).
Same error elsewhere: Runeterra level-2 champions got "makes it cheaper when it comes" (5 lines: Curious Shellfolk -> Lux (level 2), Janna -> Nilah (level 2)); a level form is never cast.
Fix: no cost or cheaper line to a form a card grows or levels into.

## F16 Code markers shown as card text (point 4: Stoat "DeathCardNonOption")
Root cause: supplement_inscryption.py copied the wiki box's traits field whole; the wiki page Traits (rev 13178) says traits are markers for other code, and most act outside battle (Campfire survivors, the Bone Lord's boons, Leshy's trials, the Deathcard maker, stitches in Act II).
Same error elsewhere: no other game has a traits field (the other sources give keywords and text only).
Fix: only traits that act in battle stay (Ant, Gem, Giant, Terrain, Uncuttable, the Obols' sentences, Chime Keeper, Limited Lives); 16 cards' texts changed; Satisfies Ring Trial is no keyword any more.

## F17 Keywords twice in a card (point 1)
Root cause: network_page.py showed the keyword list and then the text, which for Inscryption starts with "Keywords: ...".
Same error elsewhere: any game whose text holds a "Keywords:" sentence (Inscryption only today).
Fix: the page and deck_lines.py drop that sentence; the keywords stay in their own row above the text.

## F18 Weak decks shown as decks (Kaptain's review, 30 Oct 2026)
Root cause: starter decks (where a run begins: 3-5 cards) and lists of 2-3 different cards were kept as test decks; most of their cards' sigils act on the card itself, so they showed 0-1 lines.
Same error elsewhere: Monster Train has guides' core cards only (RESULTS.md); the other games' decks are full lists with many links.
Fix: decks with fewer than 3 lines or fewer than half their cards linked moved to decks_dropped_inscryption.tsv (network_page.py skips them, cases keep their card lists); 3 decks built as the wiki's Kaycee's Mod tips page says added; Larva renamed Strange Larva (its wiki page name), id kept.

## Check of 20 cards (by Claude: Kaptain does not know the game)
Each card's rows compared with its text and the wiki. Right: Spilled Blood, Sprinter, Blue and Green Mox, Gem Guardian,
Brittle, Airborne, M!rror r0rriM, Bifurcated and Trifurcated Strike (now with the strike to the opponent), Fecundity,
Sentry, Guardian, Hoggy Bank, Fish Hook, Hammer, Mighty Leap, Omni Strike, Uncuttable, Special Dagger, Magickal Bleach
("my cards" is Leshy speaking: enemy units), Ourobot.
| card | what was wrong | fix |
|---|---|---|
| Mole (Burrower) | the empty struck space had no side | side mine (v39.py, mi22) |
| Wiseclock | "rotate one space clockwise": the move had no place | to a bordering space (v39.py, mi23) |
| The Moon, The Limoncello | "replaces all spaces on its side with itself" had no row | stat_set size = its side's spaces (BRIEF Room; v39.py, mi24) |
| The Moon (Tidal Lock) | "pull small creatures into its orbit": the place is not stated; written as Squirrels moving bordering | open (unsure) |

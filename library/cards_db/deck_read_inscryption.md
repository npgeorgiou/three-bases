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

## Families and fixes (each once)
1. Strikes into empty spaces reach the opponent (records, fixes/inscryption/v38.py): Bifurcated, Trifurcated, Trifurcated
   When Powered, Sniper get a strike to the enemy player (link or); Double Strike becomes a second strike. Case mi21.
2. Board forms (records, v38.py): Clinger, Loose Tail, Hefty, Sentry as in the table.
3. Deck conditions (records, v38.py): Finical Hatchling's ten counts (Power 1-5, Health 1-5) and six tribes in the deck.
4. Card data (supplement_inscryption.py): Tadpole -> Bullfrog (wiki Fledgling page); conduit cards get the type Conduit
   (wiki Category:Conduit Sigils) and "within a circuit" also needs two Conduit cards of mine (wiki Circuits).
5. Shared concepts (flat.py): lanes from same_lane, link_formation from in_circuit, cross_lane from a target on the sides of
   an opposing space; checked in every game (cases/run.py).
6. Shared explainer (deck_analysis.py): a strike at enemy units is control; a support whose target needs a keyword no card
   of the deck has or is given is no support.
7. Shared network wording (network.py aimed): a line from an effect with a position filter says where ("next to it",
   "opposite it", "in its circuit").
8. Shared network (network.py, refs.py; v39): a keyword's effect on other cards makes aimed lines (Alpha's Leader -> Wolf,
   ni15); a card named in a filter gets a line from that card (Bell Tentacle -> Daus, ni16); an enemy attacking my unit is
   not fed by my attacks (ni17).

## Check of 20 cards (CHECK_20_inscryption.md, by Claude: Kaptain does not know the game)
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

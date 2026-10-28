# Draft: a deck (or a whole game) as a network of cards

Status: idea for the next chat, agreed by nobody yet. Builds on deck_analysis.py and mechanics.py.

## The idea
Every card is a node. A line (edge) goes from card A to card B when A gives B what B needs. The network is built by code
from the stored rows only, the same way for every game; lines only join cards of one game. Then scripts measure the network:
which cards hold the deck together, which chains run through it, which cards hang loose.

## Nodes
- Every card in the deck. A champion and its level-up form are two nodes joined by a "levels into" line (so what Senna
  does after levelling, turning slow spells fast, is in the network).
- Cards the deck's cards make or summon (tokens, created spells) are nodes too, marked "made by the deck".
- Each node keeps its role tags from the rows: maker (makes something others use), user (waits for, counts or picks by
  something), both; plus its concepts (removal, buff, draw ...).

## Edges (A -> B), each with a type and a weight
1. makes -> waits for: A makes a happening B waits for, counts or tests (A kills an ally, B acts when allies die).
2. makes -> levels up: as 1, but B's use is a level-up condition (stronger: it changes the card).
3. puts into play: A summons, creates or plays B (Strength in Numbers -> Legion Marauder).
4. repeats: A makes B's effects happen again (Telsi -> every Attack card).
5. changes the rules for: A changes how B works (Senna level 2 makes slow spells fast -> every slow spell in the deck;
   cost changes -> the cards they make cheaper; "can't be blocked" -> the attackers).
6. targets: A's effect is aimed at units like B (a buff spell on your unit -> your units; removal -> nothing in your deck).
7. type: A has or makes a type B asks for (Satyrs -> Swarmcallers).
Weight: rarer is stronger (1 / how many cards in the game use the same thing), level-up and repeat lines count double,
"targets" lines count half (any unit will do).

## What the scripts answer
- Central cards: most lines in and out (degree), and cards most chains pass through (betweenness). These are the cards
  the deck can't lose.
- Chains: every path of 2 to 4 lines, strongest first, written as "Spirit Leech -> kills an ally -> The Undying -> comes
  back -> Lucian levels up". This is the "foo -> bar -> baz" the guides describe.
- Groups: clusters of cards tightly linked to each other (a death group, a buff group); one group = one plan.
- Loose cards: no lines, or lines only one way; cards whose needs nothing in the deck makes.
- How the deck works overall: share of cards with at least one line; how many groups; whether the groups connect.
- The same on a whole game or a faction: its central cards and strongest chains (good for "what does Shadow Isles do").

## Built from what exists
- Edges 1, 2, 3, 4, 7 exist in deck_analysis.py and mechanics.edges; they become one function `network(game, cards)`
  returning nodes and typed, weighted edges.
- Edge 5 needs the rows of rule-changing effects (cost_change, can, cant, give_keyword on a category of card) matched to
  the cards they change; Senna level 2's row must say "spells in hand become fast" in a queryable way (check the record).
- Level-up forms: card_link "levels into" joins them.
- Measures: plain Python (degree, betweenness by breadth-first search, paths by depth-first search up to length 4,
  groups by connected parts of the strong lines). No new library needed.
- Output: `ask.py <game> network "<cards>"` prints central cards, top chains, groups and loose cards in plain words;
  `--json` writes the network for a picture later.

## Check before calling it done
Run it on the four Runeterra deck guides from 28 Oct 2026 (Lucian/Senna, Nilah/Janna, Marauder/Fiora, Telsi/Volibear)
and one Stormbound deck: each guide's own description must be found (Lucian/Senna: kill your own units, Last Breath value,
Senna's fast spells; Telsi: attack effects twice), and Kaptain judges the output.

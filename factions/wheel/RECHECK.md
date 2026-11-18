# Recheck of the wheel's steps 3 and 6 (Kaptain's go, 17 Nov 2026): fix everything

A chat that picks this up reads `HANDOFF.md`, then this file, and goes on from the first stage not marked done. Each
stage ends with a commit and a push, and its line here marked done with what it left.

## What was found
- Library: concepts of the "hurts the enemy" branch also count rows on my own units. destroy: 202 cards on mine, 100
  on the enemy; damage: 128 on mine; banish: 110 on mine. So links like "destroy -> counts deaths" (17x chance) are
  my units dying, not removal. Step 1's split by whom missed them.
- Archetypes: Aggro, Tempo, Pillowfort and Hatebears have under two engine parts (no network). Stompy repeats Ramp
  (real Stompy is aggro: cheap units big for their cost, plus bonuses). Concepts in parts that don't do the part's job
  (rule_change in Prison's "binds only the enemy", donate in Theft's "use what I took", banish and deck_condition in
  Dredge, heal in Defenders' "high defence", generate_cards in Toolbox's "fetch", hand_size in Madness's "discard",
  ping and card_presence_condition in Combo's "gains each time"). One concept in two parts of one archetype.
- Edges: some count links about hitting the player (no player health here); some exist only in decks (no card pair);
  many rest on a few cards (Puzzling Signposts in 32 edges).
- Research (mtg.wiki, Card Kingdom, Draftsim, StarCityGames, Rosewater): removing or sending back an enemy unit cuts
  his lane's supply, so removal feeds my units holding the base (an engine in Aggro, Tempo, Midrange, Hatebears);
  Hatebears' pair is "his cards cost more" + "my units come in free"; Prison's is "a lock on both" + "my cards ignore
  it"; Pillowfort's is "enemies must attack this" + "the attacker pays"; Clone's best target is a Place effect and an
  enemy unit; Go-Wide's many units also give supply; Turbo-Fog needs units already on the bases.

## Stages
1. **Library: split by side** every concept of the hurts_enemy branch whose rows also act on my own units (found by
   script, not only the three above), by `START_DATABASE.md`'s fix rules, with test cases. State: in progress. `flat.py` derive maps my own unit killed or banished to sacrifice (itself:
   self_destruct), damaged or weakened to friendly_fire, my player damaged to life_payment, my cards lost to drawback;
   a row on the card itself with no side ("destroy me", "deal 2 to me") is my side too. Cases w12-w16 in
   `cases/wheel.tsv`; cases/links.tsv lk152-lk372 now name the new concepts. destroy, damage and banish keep only rows on
   the enemy or with no side (a target the player picks). State: **done**. All cases pass (check_all, links, wheel);
   the deck lines are the same before and after (only concept names changed); concept_tree.txt says it for each. Lines dumped before (`checks/side_split/before.tsv`); the rebuilt database is
   tried on a copy (`checks/side_split/cards_new.sqlite`) before it replaces cards.sqlite.
2. **Rebuild** `check_all.py` (about 14 min), `links.py` (about 6), `mechanics_wheel.py links --concepts`, step 2's
   `concept_catch.py`. New concepts go on a radius in `work/radii.tsv` by step 4's rule (Kaptain sees them). State: **done**. No new concept (the rows went to sacrifice, self_destruct,
   friendly_fire, life_payment, drawback), so the radii are unchanged; concepts.tsv, concept_links.tsv, radius_links.tsv,
   axes.tsv and wheel-axes.html rebuilt. destroy -> counts deaths fell from 17 to 11 times chance: the rest are cards
   that kill any unit, mine or his (Reckoning), which are both.
3. **Archetypes redone** (`archetypes.tsv`, `archetypes.md`) by step 3's rules, with the findings above. State: drafted in
   `work/archetypes_make.py` (106 parts, every archetype with 2+ engine parts, no concept twice in one archetype); run it
   after stage 2, then check every engine pair's edges. State: **done**, waiting for Kaptain (stage 5).
4. **Map redone** (`archetype_map.py`): edges whose link text is about hitting the player, and deck-only edges, are
   marked; the cards behind most edges are counted. State: **done**: 719 edges after stage 6.
5. **Kaptain's OK** on the redone archetypes and the map. State: waiting (the page for it is made by script from
   `archetypes.tsv` and `work/archetype_map.tsv`, with the probes' results).
6. **Probes and fixes** (Kaptain's go, 18 Nov 2026; 300 card reads at most, 183 used, all in `factions/read-cards.tsv`).
   State: **done**. A script counted, for the thin archetypes and every engine concept pair with no link, the cards
   of each game with both and the links between them; helpers read 90 real card pairs and 41 single cards (text next to rows,
   `library/cards_db/checks/wheel_probe/`). Fixed for every card, with cases (START_DATABASE.md "State"): "can" rows by
   what they allow (rule_change keeps only rules on both players: 669 cards -> 7, so it is out of the usable concepts,
   off the radii "strikes more" and "position and combos" and out of Prison's "lock on both"); Taunt or Challenger given
   makes my unit take hits; Taunt given to a unit whose damage kills; a keyword given to a space (Rain) is on the space
   too; a card moved only inside a pile puts no unit anywhere; Runeterra Flow counts spells; 21 misread cards. A map
   edge is weak "about the player" only when more than half its card links are. Still thin, because the 10 games hold
   few such cards: Pillowfort (2 edges), Prison (2), Extra Turns (2), Discard / 8-Rack (0). Not fixed: 89 cards with
   "instead" whose rows show no OR or IF (not read).
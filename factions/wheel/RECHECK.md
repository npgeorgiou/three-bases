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
   script, not only the three above), by `START_DATABASE.md`'s fix rules, with test cases. State:
2. **Rebuild** `check_all.py` (about 14 min), `links.py` (about 6), `mechanics_wheel.py links --concepts`, step 2's
   `concept_catch.py`. New concepts go on a radius in `work/radii.tsv` by step 4's rule (Kaptain sees them). State:
3. **Archetypes redone** (`archetypes.tsv`, `archetypes.md`) by step 3's rules, with the findings above. State:
4. **Map redone** (`archetype_map.py`): edges whose link text is about hitting the player, and deck-only edges, are
   marked; the cards behind most edges are counted. State:
5. **Kaptain's OK** on the redone archetypes and the map. State:

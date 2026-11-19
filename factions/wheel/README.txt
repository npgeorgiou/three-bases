THE WHEEL'S FILES (factions/START_DESIGN-1-wheel.md has the steps; HANDOFF.md says which step is next)
HANDOFF.md      where the wheel stands, step by step, and Kaptain's standing decisions
PIPELINE.md     the commands of every step and what each makes
archetypes_kaptain.txt  Kaptain's list of deck archetypes
deck_archetypes.tsv  the deck archetypes' parts and the concepts that can do each (step 8); deck_archetypes.md the same in plain words
archetypes.md   archetypes.tsv in plain words, for Kaptain (work/archetypes_plain.py)
archetypes.tsv  the faction archetypes from real factions: their parts (engine or brick) and the concepts that can do each (step 3)
work/radii.tsv  every usable concept and the radius it goes on, with the part of it that counts there (step 4)
work/           suspects.tsv, suspect_verdicts.tsv, concept_games.py (-> concept_games.tsv, --all -> concept_games_all.tsv)
                (step 1: concepts counted only in some games, their verdicts, per concept and game where its rows act);
                links_same.py (checks that two links.sqlite files hold the same links); concept_catch.py and
                concept_verdicts.tsv (step 2: the kinds, with reasons); faction_archetypes.py (step 3); archetype_map.py and archetype_map_template.html (step 6); factions.py and concept_list.py (step 7); make_stop1.py (step 10)
Made by the steps: work/concepts.tsv and work/concepts.md (2), work/faction_archetypes.tsv and .md (3), library/cards_db/axes.tsv, wheel/radius_links.tsv and
factions/wheel-axes.html (4), library/cards_db/wheel/concept_links.tsv (5), work/archetype_map.tsv, work/archetype_gaps.tsv and factions/wheel-archetypes.html (6), work/factions.tsv, work/lists/ and work/answer_concepts.tsv (7), combos.tsv (8), plans.tsv and keywords.tsv (9), answers.tsv and STOP1*.md (10).

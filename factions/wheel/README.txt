THE WHEEL'S FILES (factions/START_DESIGN-1-wheel.md has the steps; HANDOFF.md says which step is next)
HANDOFF.md      where the wheel stands, step by step, and Kaptain's standing decisions
PIPELINE.md     the commands of every step and what each makes
archetypes_kaptain.txt  Kaptain's list of archetypes (the source of step 3)
archetypes.tsv  the archetypes that can exist in this game: their parts (engine or brick) and the concepts that can do each (step 3)
work/radii.tsv  every usable concept and the radius it goes on, with the part of it that counts there (step 4)
work/           suspects.tsv, suspect_verdicts.tsv, concept_games.py (-> concept_games.tsv, --all -> concept_games_all.tsv)
                (step 1: concepts counted only in some games, their verdicts, per concept and game where its rows act);
                links_same.py (checks that two links.sqlite files hold the same links); concept_catch.py and
                concept_verdicts.tsv (step 2: the kinds, with reasons); archetype_map.py (step 6); factions.py and concept_list.py (step 7); make_stop1.py (step 10)
Made by the steps: work/concepts.tsv and work/concepts.md (2), library/cards_db/axes.tsv, wheel/radius_links.tsv and
factions/wheel-axes.html (4), library/cards_db/wheel/concept_links.tsv (5), work/archetype_map.tsv and factions/wheel-archetypes.html (6), work/factions.tsv and work/lists/ (7), themes.tsv and tools.tsv (8), combos.tsv (9), answers.tsv and STOP1*.md (10).

THE ROSTER'S FILES (factions/START_DESIGN-1-roster.md has the steps; HANDOFF.md says which step is next)
HANDOFF.md      where the roster stands, step by step, and Kaptain's standing decisions
PIPELINE.md     the commands of every step and what each makes
archetypes_kaptain.txt  Kaptain's list of deck archetypes (a reference only)
deck_archetypes.tsv  the deck archetypes' parts and the concepts that can do each (a reference only); deck_archetypes.md the same in plain words
work/           suspects.tsv, concept_games.py, tag_check.py, tag_read_input.py, tag_read_sum.py, tag_split.py
                (step 1: concepts counted only in some games, per concept and game where its rows act, the tag check);
                concept_catch.py and concept_verdicts.tsv (step 2: the kinds, with reasons);
                deck_scores.py (step 3: the real decks' scores);
                make_faction.py (one faction from concepts Kaptain gives, the way step 6 makes them; made/: its outputs);
                roster_map.py and roster_map_template.html (step 5: the map page);
                kernel_factions.py (step 6: the factions from what they do), concept_list.py (step 6: each faction's list),
                answer_concepts.tsv (the ways of each answer, agreed)
Made by the steps: work/concepts.tsv and work/concepts.md (2), work/deck_scores.json (3), library/cards_db/roster/concept_links.tsv (4),
factions/roster-map.html (5),
work/kernel_factions.md, work/kernel_factions.tsv and work/lists/ (6), combos.tsv (7), plans.tsv and keywords.tsv (8), answers.tsv and STOP1*.md (9).

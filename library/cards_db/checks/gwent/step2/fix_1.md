# Gwent step 2, fixer 1 (WRONG ROWS families 1-6)

## Family 1: Create without what is created
Scripts: fixes/gwent/v78.py (first pass, 33 rows in 9 files; one record can sit in two files), fixes/gwent/v79.py (second pass, re-reads flagged cards with the better reader). Radeyah: `summon` of the Neutral stratagem became `create`.
Cards changed: all cards whose text says Create and had `keyword_action Create` (25 cards, 33 rows as some are in two files, 2 with two Creates).
Checked: Eventide Plunder, Braathens, Filavandrel aén Fidháil, Henry var Attre, Radeyah: new create rows print next to their text and say what the text says. Finder (text has Create, no `act create`): 0 hits.
Status: FIXED. Open details (cards keep `unsure: create`): Elf and Onion Soup ("of the same color" not written), Henry var Attre / Rosa-type second row "their starting deck" has no side, 813683 ("and boost it by 2 instead" is not part of the filter). Radeyah's create row also keeps its `to` (this row).

## Family 2: Discard
Script: fixes/gwent/v80.py. Cards changed: 2 (Eist Tuirseach, Bjorn Stormursson; 1 row each, 2 files lines counted as per record). Both now `keyword_action Discard` with on/params/link kept; no `act discard` left. Second run: 0 changes.
Status: FIXED.

## Family 3: time window
STUCK: family 3: no rule by design (three different shapes) and the state value `applied_this_turn` needs Kaptain's decision (families.md). Not changed.

## Family 4: adjacent
STUCK: family 4: the with-value `adjacent_group` needs Kaptain's OK before use. Armorer's Workshop not changed.

## Family 5: ignoring Armor
Script: fixes/gwent/v81.py. Cards changed: 1 (Piercing Missile, the record in second_001.jsonl; the one in batch_004.jsonl already had it). Its damage row now has `ignore_armor: 1`. Finder: 0 hits (keyword entries Bleeding, Insanity in keywords.jsonl are glossary and skipped by design).
Status: FIXED.

## Family 6: unstated amount
STUCK: family 6: needs five new value forms that Kaptain decides (families.md). Not changed.

# Gwent step 2, fixer 4 (script fixes/gwent/v83.py)

1. FIXED. Cause: v78 REG wrote region value "Monsters"; vocab (v72) has "Monster". Only Eventide-type record 756623 (batch_002) held it. v83 turns every region value Monsters into Monster.
2. FIXED. Madame Luiza (756863, batch_003): the cost_set sits in a given ability (event keyword_used of Tribute, limit next_time) that has lasts this_round (limit is not allowed on the effect itself).
3. NOT A RECORD PROBLEM. Records already hold the keyword: Caranthir 757394 (event_total with keyword Frost, from v82) and Braathens 757137 (Create filter with keyword Disloyal, from v78). Cases gw22 and gw30 fail because the flat tables were not rebuilt (load.py not run by me). Every other card whose text names Frost or Disloyal holds the keyword ref too. Needs load.py then cases/run.py.
4. FIXED. vocab.tsv Gwent meaning added to Charge (Order uses; only Charge: X cards gain Charges), Poison (two instances destroy the unit), Ambush (played face down, flips when condition met), Resilience (adds: then the status is removed; Boost and Armor not carried over). The other 12 Gwent keywords already carry a Gwent meaning. Concept column of Charge (movement) and Poison (damage_over_time) not changed: they do not fit Gwent (see keyword_defs.md), a concept is Kaptain's to change.
5. FIXED. families.md RIGHT: 12 gwent lines added to audit_text_explained.tsv. Sigi Reuven verdict (V16 record_right) added to patterns/verdicts.tsv. pattern_check.py gwent now: 0 flags (Eventide Plunder and Braathens flags gone since the Create rows hold Fee and Disloyal; Sigi judged).

check.py gwent: batch_002 and batch_003 0 problems.

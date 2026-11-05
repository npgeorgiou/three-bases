FIXED: Wave's "all cards cost a maximum of 4" was not read as a cost cut, so it made no line; a cost cap now makes cards costing more cheaper. Files: network.py (helps_it and the aimed rows near the cost cut), cases/network.tsv. Cases: n514, n515, n516.
- pair.py: Wave -> Death and Wave -> Hulk now "makes it cheaper"; Wave -> Ant Man stays none.
- Any card in any game with a cost_change that has a max= number (cap) and no cost= now gives "makes it cheaper" lines to cards costing more than the cap.
- Cases were not run against the whole table (no check_all).

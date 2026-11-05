FIXED: A stat set to another unit's stat (Snowy Razorclaw, Zed) was treated like a fixed set (Agent Venom) and made no buff line; only sets to a fixed number now count as no buff. Files: network.py, cases/network.tsv. Cases: n539, n540, n541.
- Touches any card whose only stat act is a set to a read stat (params "=stat") in any game: now links to buffed/stat-change waiters.
- Fixed-number sets (Agent Venom) unchanged.
- Checked by pair.py: both Runeterra examples now give a line, Agent Venom -> Wolverine stays NONE.

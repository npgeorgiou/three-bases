FIXED: A card that only sets stats (Agent Venom: power 3) is no buff and feeds no stat-change need (Wolverine, Elder Dragon, Gilgamesh). Files: network.py, cases/network.tsv. Cases: n451-n454.
- Applies to every game: cards whose only stat acts are stat_set on my side lose stat_changed lines to condition/state needs.
- A set to a high value that meets a power threshold would also lose its line (none seen).

FIXED: Moving units made a line to any card that hits units "next to it" (Seismic Capacitor), though its text waits for no move; now only lines or a target's side keep it (C8 only; C9 other sites, Sigrdrifa's Rite -> Rage of the Sea still open). Files: network.py, cases/network.tsv. Cases: n683, n684.
- Change: network.py moves_said call site skips when the only place is "next to it" and the target is not the card itself.
- Hydraulic Lifter/Titan Fist -> Seismic Capacitor now NONE; Titan Fist -> Artemis Artillery stays (Kaptain ntb10); Maxii -> Albrich stays.
- Other games with "acts on units next to it" only (faeria, stormbound, gwent, ~346 table lines) lose that reason; "behind/around/in a line" kept.
- C9: Drakenborg -> Redanian Secret Service already right; Sigrdrifa's Rite -> Rage of the Sea, Mobilization/Witches' Sabbath lines differ (revive and site 1862), not touched.

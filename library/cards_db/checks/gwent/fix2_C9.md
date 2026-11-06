FIXED: Gwent keyword-only "played self" rows and the multi-activation "can act again (times=listed)" were counted as summon effects, so revive/summon/copy lines hit cards with none. Files: network.py (entry set, two lines), cases/network.tsv. Cases: n685, n686, n687.
- Rage of the Sea, Redanian Secret Service and Lyrian Arbalest lose "its summon effect goes off"; Drakenborg -> Vincent Meis (real Zeal) stays.
- Still wrong, not this cause: "is a card whose playing sets off its effect" for Mobilization -> Lyrian Arbalest and Witches' Sabbath -> Arachas Swarm (network.py ~1867, a played-trigger by keyword/type matching); Drakenborg -> Redanian "given keyword" line is another site.
- Other Gwent cards with a "can act again" ability lose a false summon-effect line; other games unchanged unless a keyword-only played row exists.
- n686 deck name taken from the Mobilization deck; Witches' Sabbath case not added (deck unknown).

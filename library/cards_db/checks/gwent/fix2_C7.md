FIXED: a card put into play by kind from deck or hand linked to every card matching the filter; now only to cards with a played/summoned effect (L17). Files: network.py (tutors loop, one line), cases/network.tsv. Cases: n681, n682.
- Knight-Errant and Redanian Knight lines gone (pair.py); Ge'els -> Lara Dorren (n645) stays.
- Cintrian Knight keeps "puts it into play": its data has a played-self effect (damage), so the line is by the rule; the sheet's claim that it has none disagrees with its rows.
- Drone (Arachas Behemoth "summons") comes from the named-card put site (~724), not the tutor site: not fixed. C8 (into_the_breach) and C9 (revive/copy site) are other sites: not covered.
- Other games: any game with summon/play_card from deck/hand by kind now needs the target to have a play/summon effect.

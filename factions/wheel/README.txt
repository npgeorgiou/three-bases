THE WHEEL CHAT'S FILES (START_DESIGN-1-wheel.md), 14 Nov 2026. Made by library/cards_db/mechanics_wheel.py.
PIPELINE.md     steps 1-5.1: how each result was made, what was script and what judgment, how to redo it
RESULTS-1-5.md  the results of steps 1-5.1: radius pairs, the 20 shapes, the order, the 48 mechanics
HANDOFF.md      for the next wheel chat: what the first try found, why the guide changed, what to reuse
mechanics.tsv   48 mechanics, one line each, "I do X -> I gain from X", the library concepts that catch its cards, SMALL marks
STOP1.md        Stop 1 in plain words (made by work/make_stop1.py)
table.tsv       Stop 1: the 20 factions (archetype, radii, owned, shared, blind spot, the five answers;
                answers and archetypes are Claude's draft); made by work/make_table.py
partners.tsv    Stop 1: per pair of factions the best read combo (KEEP/WEAK, a strong library number), played sequence, source
apart.tsv       Stop 1: mechanic pairs real factions keep apart (apart.py), per faction pair and inside one faction
arguments.tsv   joins with no strong library number, argued from this game's rules (Claude's)
tools/wheel_table_check.py checks all of these (step 9)
library/cards_db/wheel/measured.tsv:  per mechanic its cards in the library, games with 10+, the biggest real faction's count (with the cards
                that make it happen; 30+ wanted), the real factions with the highest share, the radii it serves
library/cards_db/wheel/links.tsv:  per pair of mechanics, how much more often than chance the library links their cards (cards) and how
                much more decks heavy in one hold the other (decks); 1 = chance

Step 1, how the pool was cut (an agent read 8 cards per mechanic; its verdicts are kept in each line's concepts):
- Too small (under 30 in the biggest real faction), dropped: kill outright 27, stops 28, lanes 27, cells 22, junk and hand
  12, attach 20. Merged: revive + recycle; fight + forced attacks; ping + area; weaken + silence + transform; cheaper + in
  hand; pick + copy; onattack + strikes twice or first; overkill + strength 5+; guard + can't be targeted; movement + push.
- Copies of the seven factions, dropped: units die -> others grow (Sunfeeders' Toll), hit and survive -> act (Hospice
  Harden, Retaliate), heal (Hospice), units react to spells (Star Priests), round start (the library catches player turns,
  1 of 8 right). Reworded so they don't copy: sacrifice is a trade (an enemy dies), never a gain (Offering); tokens come
  from Place or Death, never round-end seeding (Rootkin Seeds); ping never at round end (Long Guns Barrage).
- Dropped as against this board: hidden reactions (traps are instant answers on the enemy's turn).
- Concepts narrowed where the agent found wrong catches (adjacency 1 of 8 right before, guard 1, discard 1, weaken 1).
work/           the second try's files (step 2 verdicts, shapes, owners, combo verdicts, scripts); HANDOFF.md top says where it stopped

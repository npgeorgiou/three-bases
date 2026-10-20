# Rebuild differences: stored library vs a rebuild with the same tools (21 Oct 2026)

A rebuild differs from the stored library by 5,079 tags in 129 groups (concept, role, gained or lost). The 20 biggest groups
hold 90%. Samples (10-12 per group, seed 7) judged against `concept_tree_v3.txt`; verdict on the rebuild's side.

| group | size | verdict | why |
|---|---|---|---|
| buff does lost / stat_gain does new | 1,238 / 1,203 | rebuild right | +1/+1 counters and +N stats are stat_gain, the narrower concept under buff |
| buff counters lost / stat_gain counters new | 333 / 347 | rebuild right | "ignores cover" counters a defence bonus; same tag in the narrower concept |
| buff does new | 230 | rebuild right | Shadowverse evolve: the tree's upgrade rule keeps buff for units that evolve |
| debuff does lost / stat_loss does new | 226 / 209 | rebuild right | -N stats are stat_loss; 40k "subtract 1 from the hit roll" on its own damaged profile is no debuff of an enemy |
| disable does new | 185 | rebuild half wrong, fixed | "this creature doesn't untap" is a drawback; tapping lands is mana denial (patterns/mtg.txt narrowed) |
| damage benefits new | 142 | rebuild right | engine rule: cards that trigger when damaged benefit from damage |
| draw does new | 118 | rebuild right | "put N of them into your hand" is draw and selection (Kaptain, 21 Oct); 8 "skip your draw step" cards left to check |
| high_cost benefits lost | 32 | open | data-rule cost tags of newly loaded games; check role in the one-chain step |
| on_attack does new | 52 | rebuild right | Shadowverse Clash triggers when it attacks |
| on_play does new | 48 | rebuild right | Star Wars Unlimited Ambush, Shielded, Support act when played |
| haste does lost (Lorcana) | 21 | rebuild right | "chosen character gains Rush" gives haste: role grants (fixes/f03) |

Found on the way: general patterns (game NULL in concept_patterns, e.g. disable "doesn't untap", the draw patterns) live only in
the database, in no file. The build adds tags across builds and removes them only when a pattern line disappears, so the stored
tags depend on the history of the pattern files. Both are for the one-chain step.

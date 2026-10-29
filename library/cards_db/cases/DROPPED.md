# Cases dropped, with the reason

- Demacia, Shadow Isles, Targon "on_kill" (library tags): the old tags are wrong for these regions. Cards tagged on_kill there
  include Rally, Summon a Dauntless Vanguard, Fully heal an ally, Fish Fight: none of them triggers on a kill (checked 28 Oct 2026).
- c02 Thresh -> Kalista (from the library's combos.tsv, "revive the strongest dead champion"): the texts give no link.
  Thresh (level 1) only levels up on seeing units die and kills nothing of yours; the revive is Kalista (level 2)'s own
  ability; the real pair is Thresh (level 2) -> Kalista (level 2), which is case c06 and passes. An earlier run passed c02
  only through a loose connection (Thresh's The Box damaging enemies counted toward Kalista's allied deaths), fixed since.
- csb39 Summon Militia -> Kindred's Grace, csb41 Brothers in Arms -> Kindred's Grace (Claude's pairs from the texts):
  Kindred's Grace gives strength to units sharing the target's type, whatever the type; Knights are not named, so the
  pair has no link of its own beyond "more units of one type". The records hold it correctly (state shares_subtype_with_it).
- cfa04 Gabrian Enchantment -> Oak Father, cfa11 Oakling -> Deepwood Stalker, cfa16 Gift of Steel -> Hilltop Archer (Faeria
  guides): stat help, not one card setting off another; the combo search finds only that. The two in guide decks are network
  cases nfa01, nfa02 ("boosts" lines); Enchantment + Oak Father is in no deck found.
- cfa12 Gabrian Commander -> Triton Trainer (Blue Jump guide, "a strong turn-two play"): no link in the texts; the Trainer
  buffs the next Jump creature and the Commander has no Jump (Aquatic, Charge 2). Tempo advice, not a combo.

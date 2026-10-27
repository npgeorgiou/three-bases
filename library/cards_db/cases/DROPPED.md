# Cases dropped, with the reason

- Demacia, Shadow Isles, Targon "on_kill" (library tags): the old tags are wrong for these regions. Cards tagged on_kill there
  include Rally, Summon a Dauntless Vanguard, Fully heal an ally, Fish Fight: none of them triggers on a kill (checked 28 Oct 2026).
- c02 Thresh -> Kalista (from the library's combos.tsv, "revive the strongest dead champion"): the texts give no link.
  Thresh (level 1) only levels up on seeing units die and kills nothing of yours; the revive is Kalista (level 2)'s own
  ability; the real pair is Thresh (level 2) -> Kalista (level 2), which is case c06 and passes. An earlier run passed c02
  only through a loose connection (Thresh's The Box damaging enemies counted toward Kalista's allied deaths), fixed since.

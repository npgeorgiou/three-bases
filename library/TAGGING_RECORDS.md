# Tagging per effect

## Agreed with Kaptain (26 Oct 2026)
- **All or nothing.** A new structure is built for every entry of every game, or not at all. No mix of entries with and
  without it. It is built in a copy of the database; the real one is replaced only when the whole test below passes.
- **The full record schema below is not pursued now.** Its slots (filters, amounts, which one, area, duration) need new
  pattern sets for every game, a second round of the pattern work, and its feasibility for the prose games is unproven.
- **What is tested instead** (Claude's suggestion): abilities and effect pieces built only from what exists: the tags, their
  stored text positions, the patterns that made them, and generic rules. No new patterns per game, no new tagging.
- Filters ("the next Jump creature") are left out for now. Wrong tags such as Triton Trainer's movement stay until a review.

### The structure under test
- New table `abilities(id, entity, ord, ev_pos, ev_len, kind)`: one row per ability of an entry, cut at sentence ends,
  line breaks and keyword prefixes (Gift, Battlecry, Deathrattle, Deploy, Last Words, "When/Whenever/At", "{T}:").
  Keywords in a keyword list are one ability each. Kind: keyword, triggered, activated, static.
- New table `pieces(id, ability, ord, ev_pos, ev_len)`: an ability cut at "and" / "then" only when a new effect tag or a
  new number follows ("deal 2 to a random enemy" | "1 to all adjacent ones"). Not cut where "and" joins targets or
  conditions.
- `entity_concepts` gets the columns `ability` and `piece`. Each tag's own pattern is re-run inside its stored span to find
  the exact matched words (wide spans like Wild Avenger's "taunt, dash 2 this gains ..." get narrowed), and the tag goes to
  the ability and piece holding them. A piece without its own effect tag inherits the previous piece's effect. Tags from a
  keyword go to that keyword's ability.
- Computed instead of stored: trigger pairs form only inside one ability (replaces the cross product in `trigger_effect`);
  compound tags (aoe_damage, random_target damage, temporary_buff, permanent_growth, scope_*) form only inside one piece.
- Limits: no amounts, filters or areas by distance beyond existing concepts; where sentences are cut badly (prose
  games) abilities are cut badly.

## The test (all 21 games; one failing game fails the whole test)
Pass numbers are Claude's suggestion.
1. **Does it fly (script only).** Per game: share of tags placed in exactly one ability and piece, tags placed nowhere,
   abilities with no effect tag, pieces holding two different effects, trigger pairs before and after.
   Pass: 98%+ of tags placed in every game; outliers few enough to read.
2. **Is it accurate.**
   - Gold sample: per game 10 random entries + 5 targeted ones (modal "choose one", "would ... instead", "for each", X
     costs, multi-sentence text, keyword lists; Spire intents, Darkest Dungeon skills, 40k/AoS ability blocks where the game
     has them), 315 entries. For each, the correct ability and piece cuts, the piece of each tag and the correct trigger
     pairs are written down once (checking reads, not tagging) in `tools/records_test/gold/<game>.json`. Pass: 95%+ of tags in
     the right piece, and trigger pairs right, in every game.
   - The answer key (`tools/key/<game>/key.json`, all 21 games): precision and recall of the computed compound tags against
     the key, compared with today's (`concept_precision`). Pass: no concept worse in any game.
   - Known errors must come out right: Wild Avenger, Invincible, Mortarion, Buzz Lightyear - Jungle Ranger (section "The
     problem" below).
3. **Does it answer questions better.** Old and new database, same questions:
   - `tools/combos.tsv` through `query.py combo`: at least as many known combos found; a sample of found links checked for
     false ones.
   - Six fixed questions: random-target damage; trigger on own unit's death that summons; temporary attack gain on summon;
     growth on a per-turn trigger; engine pairs inside one faction; a three-card chain in one game. Top 3 results per game
     per question are checked by reading (up to 378 rows). Pass: more correct results than today in every game where the
     question has answers.

## Instructions for the chat that runs the test
- Library task: clone as CLAUDE.md says, then `git sparse-checkout disable`. Read only this section and "The structure
  under test"; read code only where the task needs it (`tools/trigger_pairs.py` for the current sentence split,
  `tools/compact_text.py` for evidence positions, `tools/query.py` for `connections`/`combo`).
- Work on a copy: `cp library/three-bases-library.sqlite <scratchpad>/records.sqlite`, and point the tools at it with
  `TB_LIB`. Never write to the real database; push only code and test files.
- New code goes in `tools/records_test/` (one script per step: build abilities and pieces, place tags, compute pairs and
  compounds, report). Steps 1, 2 (key part) and 3 (combos part) are scripts; write their per-game numbers to
  `tools/records_test/REPORT.md`.
- Gold sample: a script picks the 315 entries with a fixed seed and lists them; Claude writes the gold files in batches per
  game, reading only each entry's text. Then the script scores against them.
- Reading budget: gold entries, the outliers from step 1, the top-3 results of step 3. Nothing else is read entry by entry.
  Before the gold reading starts, tell Kaptain the outlier count and an estimate of the reading left, and wait.
- At the end: the report per game with pass or fail per step, and a one-line verdict. Present it to Kaptain before anything
  goes into the real database.

## Earlier proposal (Claude, 26 Oct 2026; not pursued, kept for reference)

## The problem
A card's tags are one flat list. Nothing says which tags belong to the same effect, so the library glues facts together with
compound concepts: `aoe_damage` (damage + many targets), `multi_target_attack`, `random_target`, `temporary_buff` (stat gain +
this turn), `permanent_growth` (stat gain + again and again + kept), `in_hand_buff`, `friendly_fire`, `scope_self`. That only
works for the combinations someone gave a name: an area lock (Taunt) or an area stat loss has no tag, and a card with two effects
mixes them up.

The library's `trigger_effect` table was meant to keep the pairs, but it is the cross product of every trigger and every effect
it finds in a sentence or paragraph. What it holds today (live examples):
- Wild Avenger (Faeria), "Taunt, Dash 2 / This gains +0/+1 for each time you've been dealt damage this game": on_play -> taunt,
  on_play -> immobilize, on_play -> forced_movement, on_play -> attack_gain. Taunt is not summon-timed, Dash moves its own
  creature, and +0/+1 gains no Attack.
- Invincible (Hearthstone), "Reborn. Battlecry and Deathrattle: Give another random friendly Undead +5/+5 and Taunt": on_play ->
  death_trigger, on_play -> revive, death_trigger -> summon.
- Mortarion (40k): one keyword list ("Special rules: Blast, Deadly Demise, ...") paired with every trigger: aura -> damage,
  death_trigger -> play_restriction, buff -> piercing.
- Buzz Lightyear (Lorcana): Shift (an alternative cost) became activated -> revive and activated -> discard.

## The idea
Tag each effect of a card as one record with fixed slots. The flat tags stay, but they are derived from the records, so search,
signatures, archetypes, combos and the key keep working while the records are built.

### A card
A card has abilities; a keyword is an ability other cards reuse. Each ability has:
- **zone**: where it works: in play (default), hand, deck, hand or deck, discard pile, anywhere.
- **kind**: static (always on), triggered, activated, replacement ("would ... instead"), cost or play rule.
- **trigger** (triggered only): the event (summoned, dies, attacks, is dealt damage, turn start or end, a card is played, a
  card is drawn, a god or player is dealt damage, moves onto a tile ...) and a filter on the event's object: whose (own, enemy,
  any), what (this, a unit, a Yak, a Jump creature, an event, a creature with higher Attack than Life).
- **condition**: a gate ("if you attacked a god this turn", "while you control 2 lakes", "first time").
- **cost**: what is paid (faeria, life, sacrifice a creature, damage to this, discard, exhaust/tap).
- **frequency**: once (per card), first time, once per turn or round, every time the trigger fires.
- **effects**: one or more records, in order, each linked to the one before: and, then, if you do, instead, for each.

### An effect record
- **verb**: what happens: damage, heal, stat change, destroy, remove (exile, swallow), return to hand, draw, discard, create
  card, summon, transform, copy, move, lock (can't move or act), grant (a keyword or an ability), gain resource, change cost,
  change land, win or lose life ...
- **stat** (stat change): attack, defence, both, other (lore, armour); **sign**: up, down, set, double, swap.
- **amount**: a number, X from a count now (cards in hand, lakes you control), a count over the game (times you were dealt
  damage), a stat of something ("equal to its Life"), random range, or unbounded.
- **target**: side (own, enemy, both), kind (unit, structure, god/player, card in hand, deck, discard pile, land, the new card or
  unit just made), and **selection**: self, the trigger's object ("it", "that creature"), chosen (how many), random (how many),
  all.
- **area** (selection all, or anything spatial): none, adjacent, a line or shape, a row or lane, within a distance, whole board.
- **duration**: instant, this turn or round or phase, until a condition, while the source is in play, lasting.
- **payload** (grant, create, summon, delayed effects): the ability or card the effect makes, itself made of abilities and
  records. "Give the next Jump creature you summon +1/+1" is an effect whose payload is a one-shot triggered ability.

## What the old concepts become
Most compound concepts become questions over one record (or one ability), so they cannot be mixed up between effects:
- `aoe_damage`: verb damage, selection all (or a shape) with more than one target. `area_effect` (new, any verb): selection
  all within an area, more than one target. Taunt: static; verb lock (and "must attack this"); target enemy units, all,
  adjacent.
- `multi_target_attack`: verb damage, selection chosen, 2 or more. `random_target`: selection random.
- `scope_self` / `scope_multi` / `scope_global`: selection self / several / all with area whole board.
- `friendly_fire`: a harmful verb whose target side includes own (Famine: damage 1, both sides, all).
- `temporary_buff` / `temporary_effect`: duration this turn, round or phase.
- `permanent_growth` (call it growth): verb stat change up, target self, duration lasting, frequency every time (or a
  turn trigger). The stat tags come from the stat slot, so "repeated, kept, which stat" are three slots of the same record and
  never mix with the card's other effects.
- `in_hand_buff`: target kind card in hand or deck with a beneficial verb, or an ability whose zone is hand or deck and whose
  record targets self (Zealous Crusader, Firebringer, Soul Eater).
- `cost_reduction` / `cost_set`: verb change cost, sign down / set. `cost_type` and `life_payment`: from the cost slot.
- `condition_count` / `count_payoff`: the amount source (a count now / a count over the game).
- `on_kill`, `on_ally_play`, `on_enemy_enter`, `other_death_trigger`, `death_trigger`: trigger event plus whose.
- `delayed`: an effect whose payload is a later trigger. `in_hand_buff` vs `delayed` (Triton Trainer) stops being a judgement.
- What a card benefits from stays a separate list (`benefits`, `counters`), as now.
The tree keeps its outcome groups (what a player gets); the leaves under them that only combine two slots stop being stored.

## Does it work? Cards with many tags
Each card written as records (Claude's reading), then what the model needed.

**Wild Avenger (Faeria)**: "Taunt, Dash 2 / This gains +0/+1 for each time you've been dealt damage this game."
- Taunt (keyword ability, static): lock + must-attack-this, enemy units, all, adjacent.
- Dash 2 (keyword, trigger summoned): move, self, 2 tiles in a line.
- Static: stat change up, defence, amount = count over the game of "you were dealt damage", self, lasting.
Derived: taunt, immobilize, area_effect, adjacency, movement, on_play, defence_gain, count_payoff, scope_self. Not attack_gain,
not growth (it is computed, not gained again and again; today's key says growth: a key question the slots make visible).

**Firebringer (Faeria)**: "This gains +1/+1 whenever you summon a creature with higher Attack than Life (while in your deck or
hand)." Zone hand or deck; trigger summoned, own, filter Attack > Life; every time; stat change up, both, +1, self, lasting.
Derived: on_ally_play, stat_condition (the filter), in_hand_buff, growth, attack_gain, defence_gain, scope_self. All seven come
from one record; today they were seven separate judgements.

**Triton Trainer (Faeria)**: "Gift - Give the next Jump creature you summon +1/+1." Trigger summoned (self); effect grant with
payload: trigger summoned, own, filter has Jump, frequency once; stat change up both +1 to the trigger's object.
Derived: on_play, delayed, on_ally_play, attack_gain, defence_gain. Jump is a keyword filter, not a tribe: no tribal.

**Shozen, the Sky Eater (Faeria)**: "The first time Shozen would kill a creature in combat, instead swallow and gain control of
it." Replacement; trigger would kill in combat; frequency first time; effects: remove (until Shozen dies) the trigger's object,
then take control of it. Derived: on_kill, removal, steal. The "instead" kind keeps destroy away, which today needed a review.

**Doomgate, Door to Oblivion (Faeria)**: activated; cost sacrifice an own creature; effects: draw 1, and stat change up defence
+2 self lasting. Static: condition this has 13 Life or more; effects: destroy self, then summon Ostregoth here. Derived:
activated, sacrifice (cost), draw, defence_gain, growth (repeatable activation), stat_condition, self_destruct, summon. The
Annoying Gnat combo is a cost slot (sacrifice) meeting a trigger (dies): exact, not a guess from two flat lists.

**Invincible (Hearthstone)**: "Reborn. Battlecry and Deathrattle: Give another random friendly Undead +5/+5 and Taunt." Reborn
(keyword: when it dies the first time, return it with 1 Health). One ability with two triggers (summoned, dies) sharing the
records: stat change up both +5 and grant Taunt; target own, Undead, random 1, not self. Derived: on_play, death_trigger,
cheat_death, random_target, attack_gain, defence_gain, tribal, taunt (grants). Gone: revive and summon from the wrong pairs.
Needed: an ability may list several triggers.

**Magtheridon (Hearthstone)**: Dormant (keyword: can't act until a condition); trigger summoned: summon three 1/3 Warders on
the enemy side; nested ability on those Warders' deaths (all three): destroy all minions, both sides, then end Dormant.
Needed: a condition over several made units ("when they die") and a target side that differs from the owner's
(enemy_benefit, from summon + side enemy).

**Dagon: Promised (Gwent)**: Deploy: grant to 5 units in your deck the ability "Deathwish: stat change up 2 to the lowest-power
own unit; worship Dagon"; summon (spawn) Call of the Depths into the discard pile. Order (activated, cooldown): consume an own
unit (remove it, gain its power). Triggered, every time an own Deathwish unit is played: +1 to it. Zone hand or deck: after you
win a round, evolve. Needed: payload abilities on other cards (the 5 infused units), a selection "lowest power" (selection by
stat: stat_condition), and a zone condition for the evolve.

**Buzz Lightyear - Jungle Ranger (Lorcana)**: Shift 5 is a play rule (alternative cost, on top of a Buzz Lightyear): cost slot,
not an activation. On summon: return an action card with cost 7 or less from your discard pile to your hand. Every time you play
an action: chosen character, stat change up lore +1, this turn. Derived: cost_type, upgrade, recycle (graveyard to hand),
cost_condition, on_spell, stat_gain (lore), temporary_effect. Gone: revive, discard.

**Mortarion (Warhammer 40k)**: end of your Movement phase: for each enemy unit within 6", roll (random), on 3+ D3 mortal wounds:
damage, enemy units, all within 6" (area: distance), amount random, chance. Static while 1-6 wounds: own attacks -1 to Hit
(condition_life, drawback). Each keyword in "Special rules" is its own keyword ability, not paired with every trigger.
Needed: area by distance, chance as part of the amount, phases as turn parts.

**The Legend of Kyoshi (MTG)**: chapters I, II, III are triggers "lore counter reaches N" (delayed, by counter). I: draw, amount
= greatest power among own creatures. II: change land (Earthbend), amount = cards in hand. III: remove self, then return it
transformed. Back face: static, own lands, all: grant trample and hexproof; mana ability (activated, cost tap): gain resource,
amount = greatest power. Needed: the two faces as two cards (they are), counters as a trigger.

**Psion Abomination (Into the Breach)**: static aura: all other Vek (enemy side from the player's view), all, whole board: stat
change up Health +1; grant Regeneration; grant "explode on death" (payload: dies -> damage, adjacent, all). Derived: aura,
area_effect, defence_gain, regeneration, death_trigger (granted), aoe_damage (granted). Today the explosion counts as its own
death trigger; the payload keeps it on the Vek it is given to.

**Awakened One (Slay the Spire)**: an enemy with an intent list: each intent is an ability (trigger: chosen intent) with its
records: Slash damage 20; Soul Strike damage 6, four times (repeat count, which is multi_attack); Sludge damage 18 plus the debuff
the library lists; Rebirth, which the library lists as unknown (from general knowledge, Claude: the second phase, revive at full
health). Needed: a repeat count on a record (hits x4).

## What the cards showed
- The slots above were enough for every card once five things were added: several triggers per ability, a repeat count per
  record, area by distance, chance or dice as part of the amount, and payload abilities (granted, delayed, on made units).
- Every wrong pair in today's `trigger_effect` came from mixing abilities; none needed a judgement once the ability boundary
  was right. The boundary is the hard part, not the slots.
- Several key questions of the Faeria pass become slot facts instead of opinions (Wild Avenger growth or count, Triton Trainer
  delayed, Swallow removal or merge, Aquatic as placement plus self-destruct).

## How it would be built
1. **Ability boundaries**: split the text into abilities: keyword lists, "Keyword - " prefixes (Gift, Last Words, Production,
   Battlecry, Deploy, Order), "When/Whenever/At", activations ("{T}:", "Activate -", "Order:"), replacement ("would ...
   instead"), quoted granted abilities (payloads). The clause splitter in `reading.py` is the starting point.
2. **Slots by small shared pattern sets**, one per slot, not per concept: triggers (the existing trigger patterns), verbs (the
   existing effect patterns), selection ("all", "each", "every", "a random", "another", "up to N", "target", "it"), area
   ("adjacent", "within N", "in a row/lane", "all ... in play"), duration ("this turn", "until", "while"), frequency ("first
   time", "once per", "whenever"), amount ("equal to", "for each", "X, where"). Game files add their own words, as now.
3. **Derived flat tags**: the definitions above as queries; they replace the compound concepts in `entity_concepts` (method
   `record`) and keep the rest of the build (signatures, archetypes, combos, the key score) unchanged at first.
4. **Fallback**: an ability the parser cannot fill keeps today's flat tags (marked unbound), so no game loses tags; the share of
   bound abilities per game is the progress measure.
5. **Pilot on Faeria** (443 entries, regular text): derived tags against today's tags and the key, ability by ability. Then
   Hearthstone, Duelyst, TESL, Lorcana, Runeterra (keyworded card text), then the prose games (40k, AoS, Into the Breach,
   Darkest Dungeon, the Spire enemies), where boundaries are hardest.
6. **Links**: combos match a record's verb and target against another card's trigger and filter (Feed the Forest's "destroy a
   friendly creature" meets "Last Words"), and two cards that answer the same trigger become a link type ("both reward attacking
   the god": Khalim's Prayer and Zealous Crusader).

## Risks
- Wrong boundaries make wrong records, and derived tags then fail together. The fallback and the per-game bound share limit it.
- The key stays flat at first. A record-level key (a sample per game) would be the later test of the slots themselves.
- It touches the build chain (`trigger_pairs.py`, `link_types.py`, `engine_links.py`, `query.connections`), the tree (compound
  leaves become derived) and the scoring. Every game must be compared (`compare_builds.py`) at each step.

## Decisions for Kaptain
1. Records per ability as above, with flat tags derived from them?
2. Compound concepts (aoe_damage, multi_target_attack, random_target, scope_*, friendly_fire, temporary_buff, permanent_growth,
   in_hand_buff, cost_* from slots) derived instead of stored, and `area_effect` added for any verb?
3. Faeria as the pilot, then the keyworded games, then the prose games?

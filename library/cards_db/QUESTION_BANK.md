# Question bank: design questions the card connections must answer (31 Oct 2026, Claude, from Kaptain's examples)

How to read: each question has its parts as roles (LINKS_PLAN.md section 6): `concept[facet=value, ...]`. Facets: whose
(mine, enemy), on (unit, spell, card, player, position), zone, pick, cost_band (cheap, mid, expensive), lasts, amount, when
(trigger concept), cond (condition concept). `A -> B` means "the answer must show lines from A to B". `!X` means a tension
to look for (X hurts the plan). Sources of the questions: Kaptain's five (K), the 20 archetypes of
library/realworld/archetypes.txt (A), mechanic pairs and trades from the concept tree (M, T), and published design
practice: Mark Rosewater's mechanical colour pie (each colour's share of removal, draw, selection, recursion, tutors, mana,
copying, stealing) and faction-design columns (distinct identity, overlap, pairing), Félix Moll's set-up and pay-off
archetypes (Game Developer) (C, I, V). Every answer has the shape of LINKS_PLAN.md section 7.

## K. Kaptain's test questions (answer these first, after every step)
- K1 Speed up the summoning of big costly units, and protect the board until they are summoned.
  Parts: cost_reduction[whose=mine, on=unit, cost_band=expensive]; free_play[on=unit, cost_band=expensive, zone=hand|deck];
  cost_set[on=unit, cost_band=expensive]; protection[whose=mine]; taunt; heal[on=player]; removal[cost_band=cheap].
  Links: protection -> high_cost[on=unit] (time bought); each speed-up part -> high_cost units. !board_presence needs
  (a discount per ally vs few allies).
- K2 The same, by earning resources faster. Parts: resource_gain[lasts=permanent|growing]; base_resource_gain;
  resource_gain[lasts=now]; then high_cost units, protection as K1. Links: resource_gain -> high_cost (pays for it).
  Compare with K1: how many games do each, which factions mix both.
- K3 Spell-based, units mostly as spell enhancers. Parts: spell_power[on=unit-card]; on_spell[when, card category unit];
  spells_played_condition; cost_reduction[on=spell]; generate_cards[on=spell]; spells[cost_band=cheap]. Links: units ->
  spells (stronger, cheaper, repeated), spells -> units (triggers). Density: share of a faction's units that link to spells.
- K4 Choose what you draw from the top 2 cards, but everything costs 1 more. Parts: selection[zone=deck_top, amount=2];
  draw; cost_increase_self (cost_change up on my cards). Links: selection -> cards that want a known top card or a kind
  (tutor targets, deck_position needs). Tension: !cost_increase_self vs cheap-card needs. Expected: the second half has no
  match in any game: say so as new ground, and what the closest trades are (T group).
- K5 Steal cards from the opponent and copy its units and spells. Parts: steal[on=unit]; steal[on=card, zone=hand|deck];
  copy[source=enemy, on=unit]; copy[source=enemy, on=spell]; play enemy cards. Links: copies -> my cards that count
  played cards, generated cards or other factions' cards (variety_payoff). !Cards that need my own types (tribal).

## A. Archetype factions ("How to make a <archetype> faction?"; parts from realworld.ARCHETYPE plus these)
- A1 swarm: summon[amount>=2]; generate_cards[on=unit]; board_presence cond; aoe buffs (stat_gain[pick=all]). Links: makers ->
  count_payoff. !board_limit.
- A2 sacrifice: sacrifice; death_trigger; other_death_trigger; revive; summon[cheap]. Links: summon -> sacrifice (fodder),
  sacrifice -> death_trigger.
- A3 graveyard: self_mill; discard; revive; recycle; graveyard cond. Links: self_mill -> revive, discard -> on_discard.
- A4 control: removal; suppress; board_wipe; heal[on=player]; card_advantage. Links: card_advantage -> removal (keeps answers).
- A5 burn: direct_damage[on=player]; aoe_damage; spell_power; nexus_damage_condition. Links: spell_power -> direct_damage.
- A6 aggro_tempo: haste; attack_gain; evasion; cost[cheap]; extra_turn. Links: evasion -> on_nexus-hit needs.
- A7 scaling: permanent_growth; count_payoff; stat_multiply. Links: what triggers growth -> growers.
- A8 fortress: protection; taunt; tank; defence_gain; damage_reduction; counterattack. Links: defence_gain -> counterattack,
  taunt -> heal.
- A9 sustain: heal; lifesteal; regeneration; on_lifegain. Links: heal -> on_lifegain.
- A10 spellslinger: on_spell; spells_played_condition; spell_power; cost_reduction[on=spell]; generate_cards[on=spell].
- A11 ramp: base_resource_gain; resource_gain; cost_reduction; high_cost. Links: ramp -> high_cost.
- A12 positional: movement; forced_movement; positional cond; adjacency; terrain. Links: forced_movement -> hazards/terrain.
- A13 disruption: hand_disruption; discard[whose=enemy]; cost_increase; steal; mill. Links: what counts enemy losses.
- A14 trickery: stealth; trap_secret; information; reactions. Links: trap makers -> trap payoffs (trap_activated).
- A15 chaos: random_effect; random_target; generate_cards[random]; polymorph. Links: random makers -> variety_payoff.
- A16 card_advantage: draw; tutor; selection; generate_cards; hand_size cond. Links: draw -> on_draw, hand_size needs.
- A17 tribal: tribal cond; summon[type]; type_grant; buffs[on=type]. Links: makers of the type -> type payoffs.
- A18 objectives: zone_control; scoring_objectives; movement. Links: movement -> zone needs.
- A19 poison_attrition: damage_over_time; stacking_keyword; spread. Links: dot givers -> dot payoffs ("whenever poisoned").
- A20 transformation: transform; stances; merge_attach; upgrade. Links: what triggers a form change -> form payoffs.
For each A question also: which two archetypes the densest factions mix (the faction's second plan), and which archetype
pairs no faction mixes.

## M. Mechanics together ("What works with X?", "Ideas for cards that do X and Y")
For each pair: lines X -> Y and Y -> X per game, the factions where both are common, one example pair, and cards that do
both on one card. Pairs (from Kaptain's examples and the tree): M1 sacrifice + draw; M2 heal + damage; M3 discard + recycle;
M4 damage_over_time + aoe_damage; M5 movement + zone_control; M6 stealth + direct_damage; M7 summon + sacrifice; M8 armour
(block_armor, damage_reduction) + counterattack; M9 on_spell + cost_reduction; M10 revive + self_mill; M11 transform +
stat_gain; M12 copy + death_trigger; M13 taunt + lifesteal; M14 shield + on_damaged; M15 forced_movement + terrain hazards;
M16 generate_cards + variety_payoff; M17 retain + cost_reduction (Establishment); M18 exhaust + on_exhaust payoffs; M19
slots_queue (Orbs) + repeat_trigger (Loop); M20 haste + return_to_hand (replay on-play effects); M21 silence + removal;
M22 tutor + high_cost; M23 attack_token (extra_turn) + on_attack triggers; M24 freeze/disable + kill of disabled units;
M25 mill + deck_condition; M26 board_clog + enemy-side payoffs; M27 life_payment + low_life; M28 stances + on_stance;
M29 adjacency + summon (where units enter); M30 cost_set + cost_condition.
Also "random combinations": every pair of the 60 most common concepts with lines in at least 2 games but in no faction of
those games as a plan (both ends under 5% of the faction): ideas no faction has built.

## T. Trades: pay X to get Y ("What do games charge for Y?")
For Y in (draw, selection, removal, resource_gain, stat_gain, revive, extra_turn, steal, copy): every X that comes with Y on
the same card or the same ability as a cost or drawback (life_payment, discard, sacrifice, cost_increase_self, self-damage,
exhaust, self_destruct, donate, enemy_benefit), with counts per game. Questions: T1 what do games charge for card
selection? (K4); T2 for an extra attack? T3 for stealing? T4 for a big discount? T5 which drawbacks come with the cheapest
big units? T6 which payments are a mechanic of their own (a faction's identity, e.g. Bones, Blood, life)?

## S. Speed, curve and tempo
S1 How do factions cheat big units into play (K1 parts), and which is most common per game? S2 What does a faction with
many cheap units use to win late (scaling, buffs to all, burn)? S3 How do games punish expensive plays (cost_increase,
counter_spell, removal of high_cost, tempo)? S4 Which cheap cards link to the most expensive cards (the curve's bridges)?
S5 Which mechanics only pay off with many turns (permanent_growth, countdown, delayed) and what protects them meanwhile?
S6 What gives units haste or attack_now, and what do those link to? S7 What makes the opponent skip or lose tempo
(disable, bounce_enemy, cost_increase)? S8 Which factions have a cheap removal and which have none (gaps)?

## C. Answers and counters ("What beats X?")
For each plan X: the enemy-side roles that cancel it, from lines whose A acts on enemy rows that are X's ends: C1 a
fortress (taunt, protection): piercing, silence, steal, transform, aoe; C2 a swarm: aoe_damage, board_wipe, board_limit;
C3 big units: destroy, polymorph, deathtouch, steal, attack_lock; C4 spells: counter_spell, cost_increase on spells; C5
graveyard: banish, recycle denial; C6 stealth: reveal, aoe, random_target; C7 healing: anti-heal, lifesteal denial; C8
tempo: taunt, heal, cheap blockers; C9 movement: immobilize, cant_move, terrain; C10 card draw: hand_disruption, mill;
C11 tribal: silence, transform, type removal; C12 buffs: silence, stat_loss, bounce. Each answer: per game, which factions
hold the counter, so a designer sees which pairs of factions fight each other.

## P. Board and position
P1 How do games make placement matter (adjacency auras, lanes, rows, terrain)? P2 Push and pull: what makes forced moves
pay (hazards, terrain, collisions, lining enemies up)? P3 Zone control: what holds a spot and what takes it? P4 What
protects one key unit (bodyguard, taunt next to it, shield)? P5 How do games limit the board (board_limit) and what plays
around it (merge_attach, transform)? P6 Which mechanics need the enemy close or far (ranged, flanking, cross_lane)? P7 What
moves my own units forward and what waits for them there (territory_trigger, harvest, Corrupt)? P8 Which line rules exist
only in positional games and what would they need in a lane game?

## R. Resources
R1 Which games have a second resource and how is it earned and spent (Bones, gems, Echo, faeria wells)? R2 What converts
one resource into another (resource_conversion) and what links to that? R3 Growing income vs one-off bursts (K2): counts
and examples. R4 What pays a cost with units or life instead of mana? R5 What do cards that cost 0 or X link to? R6 Which
factions spend a resource the others do not have (identity by resource)? R7 What happens to unspent resources (banked,
spell mana) and what links to that? R8 How do games tax the opponent's resources?

## F. Card flow
F1 What fills the hand and what wants a full or an empty hand? F2 Discard as a resource: discard outlets -> cards with a
discard effect (never "any card", R1). F3 Draw vs selection vs tutor: which factions prefer which? F4 Retain and cards
that grow while kept. F5 What shuffles cards back or plants cards in the deck, and what waits for them to be drawn?
F6 Generated cards: which factions make cards and what counts them? F7 Exhaust and one-use cards: what pays them off?
F8 Deck manipulation of the enemy (mill, junk_cards, planting): what links to it?

## V. Feasibility ("Is a faction built on X viable?")
V1 For mechanic X: per game, how many cards link to an X card (in and out), how many factions have 10%+ of their cards in
X's links, the median partners per X card. V2 For a plan (two parts): how many cards sit on each end per faction and how
many lines join them; the minimum a faction has where guides call the plan playable (real-world cases). V3 Which cards
are hubs (most partners) and which are isolated (none) per faction: the deck's core and its dead cards. V4 How many
payoffs vs set-ups a plan has per faction (Moll: a mix of hard and easy payoffs). V5 Does a plan rely on one card (a hub
whose removal cuts most lines)? V6 Which mechanics have many cards but few lines (tags without combos)? V7 Which plans
work in two-faction decks only (Runeterra regions, Monster Train clans): the links between factions. V8 For Three Bases:
how many cards would a faction of plan X need to match the real games' density?

## N. New ground
N1 Which role pairs have no line in any game (K4's second half)? N2 Which concepts appear in one game only (a game's
signature)? N3 Which trades (T) does no game use? N4 Which archetype pairs does no faction mix? N5 Which counters (C)
have no counter in some game (an unanswered plan)? N6 For each of Three Bases' factions (summary/11-faction-*.txt), which
of its mechanics have the fewest partners in real games (risk) and which real links it lacks (ideas).

## I. Faction identity (from faction-design practice)
I1 Per game, what makes each faction distinct: its roles with the highest share vs the game (weighted, narrow roles
count). I2 Where do factions overlap, and is the overlap shared parts or shared plans? I3 Which faction pairs combine best
(Runeterra region pairs, Monster Train clan pairs): the lines between two factions. I4 Does each faction have its own
removal, draw and finisher, and of what kind (the colour-pie question: who gets what kind of removal)? I5 Which
weaknesses does each faction have (roles it lacks that all others have)? I6 How do games give each faction its own way to
pay (a cost or drawback it alone uses)?

## Kept from library/design_questions (same questions, now answered by plan)
01 mechanic in each game; 02 stop enemy units acting; 03 combos of combos (chains of three); 04 a family viable for a
faction; 05 card ideas X and Y; 06 works with; 07 staying power; 08 disruptive; 09 map control; 10 spell-centric; 11 go-wide
one type; 12 die and come back; 13 push and pull; 14 out-draw; 15 tricks and traps; 16 what feeds revive. Each maps to
the groups above (01 -> M/I, 02 -> C, 03 -> M chains, 04 -> V2, 05 -> M, 06 -> M, 07 -> A8/A9, 08 -> A13, 09 -> P3,
10 -> K3/A10, 11 -> A1/A17, 12 -> A2, 13 -> P2, 14 -> A16/F, 15 -> A14, 16 -> M10).

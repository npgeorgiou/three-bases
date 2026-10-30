# Into the Breach

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: single-player turn-based tactics roguelike (Subset Games, 2018) on an 8x8 grid.
- Squad: 3 mechs (from a squad); pilots give perks and survive or die; mechs can be repaired.
- Turn: the Vek show their attacks (telegraphs); the player then moves and attacks with each mech, and the Vek attacks resolve after.
- Push: most weapons push, pull or redirect units, so enemies can hit each other or fall into water and chasms.
- Lose: the Power Grid (shared by the buildings) reaches 0; a mission is won by surviving its turns and meeting bonus objectives.
- Specific: perfect information and deterministic attacks; once per battle the player can reset a turn.

## The game's rules (from sources)
Researched 30 Oct 2026 from the game's wiki (intothebreach.fandom.com, read through api.php) and Wikipedia's Gameplay section;
each line names its page. Used for read/into_the_breach/game_rules.jsonl (cards_db PROCESS step 0.10).
- How units fight: the player controls three mechs; each turn the player moves each mech and fires one of its weapons
  (Wikipedia, Gameplay). Before the player's turn every active Vek moves to a tile and prepares to attack a tile, aiming for a
  mech, a building or an objective; the attacks happen in the enemy turn unless cancelled or the Vek is killed first (wiki
  Vek). The player sees the direction of each Vek's attack (Wikipedia). All weapons have friendly fire on unless they say
  otherwise (wiki Weapons).
- How units move: Move = how many tiles a mech can move each turn; Flying units can move over any terrain tile (wiki Mechs).
  Mountains block movement and projectiles (wiki Mountain Tile); buildings block grounded movement and projectiles (wiki
  Civilian Building).
- How units reach things: most weapons push, pull or toss; a ground unit displaced into a Chasm is destroyed (wiki Chasm
  Tile); most non-flying enemies die in Water, and Massive units (all player Mechs and boss Vek) stand in Water but cannot
  attack (wiki Water Tile). Units pushed into other units take Push damage; Stable units cannot be pushed (wiki Status
  Effects). With Force Amp (+1) a pull into the mech does 2 damage (wiki Force Amp), so a bump does 1.
- What is attacked: damaging a Civilian Building lowers the Power Grid; the run is lost when it reaches 0 (wiki Civilian
  Building, Grid Power). A battle is lost when all three mechs are disabled, the grid is lost or the objective fails
  (Wikipedia). Health = how much damage a mech takes before it is disabled; a disabled mech cannot act unless repaired
  (wiki Mechs).
- Where units enter: Vek emerge from the ground on spawn tiles at the start of the enemy turn; a unit standing on one blocks
  the Vek and takes 1 damage (wiki Vek, Spawn Tile). Gana's pilot skill "Deploy anywhere on the map" shows that mechs
  normally deploy in a limited area; the area itself is not described by any page read (unknown). Deployed tanks, Walking
  Bombs and Arachnoids are put on the board by the weapons that name them (wiki weapon pages).
- Once per battle the player can reset a turn (wiki Reset Turn).
- Loadout: each mech has 2 slots, so 2 weapons at most; a passive (Rocket Mech's Storm Generator) takes a slot too. The
  starting weapon fills one slot, the second holds the starting passive or one extra weapon; never two extra weapons
  (Kaptain, 30 Oct 2026). A starting weapon can be swapped for another.

## Sources and notes

Sources:
[1] https://intothebreach.fandom.com/wiki/Weapons?oldid=3699 (weapon list by mech class)
[2] https://www.giantbomb.com/profile/majormitch/blog/thoughts-on-into-the-breachs-squads/116986/ (squads)
[3] https://www.thegamer.com/into-the-breach-best-most-powerful-mech-squads-teams/ (best squads; also r/IntoTheBreach comments/1r85f24)
[4] https://www.reddit.com/r/IntoTheBreach/comments/155pe9u/most_op_combos/ (most op combos; given by Kaptain, not readable from here)
[5] https://steamcommunity.com/app/590380/discussions/0/1694914736001439741/ (Steam custom squad guide, Laser Mech line-ups)

"Any" is not a mech class. Push and pull are forced_movement; smoke and freeze stop an enemy from acting (disable); fire and
acid are damage_over_time.

## Factions

### Prime
*Claude:* Melee mechs: punching and pushing adjacent targets.
Weapons: mostly punches and strikes that damage and push [1].
Only one each: shield (Spartan Shield), fire (Flame Thrower), acid (an upgrade) [1].

### Brute
*Claude:* Direct-fire mechs: projectiles and charges in a line.
Weapons: projectiles and charges that damage and push [1].
Only one or two: pull (Grappling Hook), shields (Phase Cannon, Grappling Hook), smoke (Aerial Bombs) [1].

### Ranged
*Claude:* Artillery mechs: arcing shots that push tiles around the target.
Weapons: artillery strikes that damage and push; smoke and fire artillery [1].
Only one: freeze; smoke (Rocket Artillery, Smoke Mortar) also disables, so no disable splash [1].

### Science
*Claude:* Support mechs: shields, pulls and pushes rather than damage.
Weapons: utility, not damage: pull, push, swap, acid, shields, smoke, fire, freeze [1].

## Combos
- Electric Whip + Grappling Hook: the Hook Mech extends the Whip's chain [2]
- Smog Mech + Rocket Mech: the Smog Mech spreads Smoke, the Rocket Mech's Storm Generator makes Smoke deal damage [3]
- Smog Mech + Exchange Mech: the Exchange Mech swaps a Vek into the Smoke, where it cannot attack [3]
- Kai Miller + Arachnoid Injector: Kai's boost secures the kill, the kill creates a friendly spider [4]
- Laser Mech + Combat Mech: pushes line the Vek up for the piercing beam [5]
- Laser Mech + Judo Mech: tosses line the Vek up for the piercing beam [5]
- Jet Mech + Rocket Mech: Aerial Bombs leave Smoke on enemy tiles; Storm Generator makes Smoke damage enemies (deck read)
- Aegis Mech + Gravity Mech: Spartan Shield turns an enemy's attack onto other enemies, which Vek Hormones adds to (deck read)

## Notes for readers (30 Oct 2026, deck read)
- Swap Mech's Teleporter swaps places: the unit on the other tile moves too.
- Statuses put on tiles (Smoke, Fire, Energy Shield, A.C.I.D.) reach the unit standing there.
- Viscera Nanobots heals the Mech that kills; Vek Hormones needs an enemy to damage another enemy, not my Mechs.
- Every Mech moves itself each turn: moving itself is no help to another Mech's shot.

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics of Into the Breach: name|expected concept|wording on the cards. Checked with coverage.py --mechanics.
# Research (20 Oct 2026, built-in browser): intothebreach.fandom.com wiki pages Weapons, Status_Effects, Tiles, Environments,
# Passives, Pilots, Squads, Vek, Tips_and_tricks; guides giantbomb.com/profile/majormitch/blog/thoughts-on-into-the-breachs-squads/116986/
# and gameskinny.com/i7374/into-the-breach-squads-guide (squad synergies: pushes, Vek hitting Vek, fire, line-ups, smoke).
# --- weapons (Weapons page, class by class)
push|forced_movement|\bpush
pull|forced_movement|\bpull
toss a unit|forced_movement|\b(toss\w*|throws?) (a|an|the|adjacent) (unit|target)
swap places|swap|\bswap
teleport|movement|\bteleport
leap or dash (mech moves as it attacks)|movement|\b(leap|dash|charge|fly) (to|in a line|forward|away)
line attack|area_templates|\b(tiles|everything|all units) in a line\b|\bpiercing beam\b
area around target|adjacency|\b(adjacent tiles|nearby tiles|surrounding tiles)\b
artillery and projectiles|ranged|\b(artillery|projectile)
self damage|friendly_fire|\b(damaging self|hurting yourself|self damage|damage itself|damages both shooter)
flip attack direction|disruption|\bflip\w* (its|a target's|the target's) attack direction
force an attack|forced_attack|\bforces? a unit to attack
control an enemy|steal|\b(temporarily )?controls? a unit
deploy a tank or bomb|summon|\bdeploy (a|an) [a-z.\- ]{0,12}tank\b|\blaunches walking bombs\b
damage grows with distance or hits|variable_stats|\bdamage increases\b|\bgains damage\b
# --- statuses (Status_Effects page)
fire|damage_over_time|\b(on fire|ignite\w*|applies fire|light\w* [^.]{0,15}on fire|sets? [^.]{0,15}on fire)
frozen|disable|\bfreez|\bfrozen\b
a.c.i.d. (double weapon damage)|debuff|\ba\.c\.i\.d\b|\bacid\b
smoke (cannot attack)|attack_lock|\bsmoke
webbed (cannot move)|immobilize|\bweb
armored|damage_reduction|\barmou?red\b|\bincoming weapon damage (is )?reduced\b
shield|shield|\bshield
boosted|temporary_buff|\bboost
stable (cannot be moved)|immunity|\bstable\b
# --- tiles and environment (Tiles, Environments pages)
water or chasm kills|terrain|\b(drowned|chasm|pushed into water|die in water)\b
crack tiles|terrain|\bcrack\w* (adjacent )?tiles\b
environment hazards announced a turn ahead|telegraphed_threats|\b(will be dropped|will fall|will strike|will become|will emerge|next turn)\b
# --- passives, pilots, Vek (Passives, Pilots, Vek pages)
repair|heal|\b(repairs? (all|one|a|adjacent)|repairing one|heals? (\d|all|1)|prepare to heal)\b
extra move|movement|\b\+\d+ move\b
psion aura over all other Vek|aura|\ball other vek\b
explode on death|death_trigger|\b(explode\w* on death|on death|when (killed|destroyed))\b
spawn eggs or minions|summon|\bspawns? (a|an|one|two|three|\d) |\blays? (an |)eggs?\b|\bspawning a friendly\b
regeneration|regeneration|\bregenerat
# "capable of drowning" / "able to drown" on Vek is trivia (no immunity), not an effect, so the water line reads "drowned" only.
# Not checked: Flying (the game's Flying lets a unit cross water and chasms; patterns/into_the_breach.txt switches evasion off for it on purpose);
# single-use weapons (no concept for once per battle).
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Science	swap	swap	https://intothebreach.fandom.com/wiki/Weapons?oldid=3699
signature	Science	shield	shields	https://intothebreach.fandom.com/wiki/Weapons?oldid=3699
archetype	Science	positional	utility: pull, push, swap	https://intothebreach.fandom.com/wiki/Weapons?oldid=3699
splash	Prime	shield	only Spartan Shield	https://intothebreach.fandom.com/wiki/Weapons?oldid=3699
splash	Brute	shield	Phase Cannon, Grappling Hook	https://intothebreach.fandom.com/wiki/Weapons?oldid=3699
combo	Electric Whip	Grappling Hook	the Hook pulls Vek next to each other for the Whip's chain	https://www.giantbomb.com/profile/majormitch/blog/thoughts-on-into-the-breachs-squads/116986/
combo	Smog Mech	Rocket Mech	Smog Mech spreads Smoke, Rocket Mech's Storm Generator makes Smoke deal damage	https://www.thegamer.com/into-the-breach-best-most-powerful-mech-squads-teams/
combo	Smog Mech	Exchange Mech	the Exchange Mech swaps a Vek into the Smoke	https://www.thegamer.com/into-the-breach-best-most-powerful-mech-squads-teams/
combo	Kai Miller	Arachnoid Injector	Kai's boost secures the kill, the kill creates a spider	https://www.reddit.com/r/IntoTheBreach/comments/155pe9u/most_op_combos/
combo	Combat Mech	Laser Mech	pushes line the Vek up for the piercing beam	https://steamcommunity.com/app/590380/discussions/0/1694914736001439741/
combo	Judo Mech	Laser Mech	tosses line the Vek up for the piercing beam	https://steamcommunity.com/app/590380/discussions/0/1694914736001439741/
```

## Notes from the patterns check
Patterns check, 26 Oct 2026 (key wrong 70.5 → 53.3, missed 36.2 → 13.7 per 100 on the corrected key; cases below).
- Damage types (Kaptain's rules, tree v3): `multi_target_attack` = several separately named targets (the player chooses them, or one chosen plus a fixed one); `aoe_damage` = damage reaching several units without choosing each (around the target, a row, all); `random_target` = a random target. Every Into the Breach weapon with a fixed pattern (beams, lines, two projectiles, adjacent tiles) is `aoe_damage` plus `area_templates` (a named shape) and/or `adjacency` (neighbours); chained or bounced damage (Electric Whip, Ricochet Rocket) is `damage` only. A weapon that only pushes the neighbours (Artemis Artillery) is `damage` plus `adjacency`.
- Key changes (Claude, Kaptain's rule "change the key where sure"): smoke entries `suppress` → `attack_lock` (as the Smoke keyword key; Submerged stays `suppress`); `silence` removed from the three A.C.I.D. entries (it doubles damage taken, it does not remove an ability); `ranged` added to 8 projectile weapons; `adjacency` added to 8 "push adjacent tiles" weapons; Thermal Discharger `area_templates`; Aerial Bombs and Jet Mech `attack_lock`.
- Cases removed (the cards show no lead of 1.5 times or more): signature Prime damage 84% vs 59%, Prime forced_movement 55% vs 69%, Brute damage 79% vs 61%, Brute forced_movement 76% vs 61%, Ranged forced_movement 62% vs 66%, Science forced_movement 68% vs 64%, Science damage_over_time 12% vs 9%, Science disable 1 of 25 cards; splash Prime damage_over_time 10% vs 10%, Brute disable 0 of 29. Kept and met: Science swap and shield, the Science positional archetype, splash Prime and Brute shield. Solved later (combo Electric Whip + Grappling Hook now met through `forced_movement` and `adjacency`). Case signature Ranged `ranged` removed 26 Oct 2026: `ranged` is on 54 of 117 faction cards (46%), above the 25% bound for a concept that can belong to one faction (Brute has it on 55% of its cards too), so signature.py rightly leaves it out.
- Open (shared, for its own pass): entries that only mention a keyword inherit its tags (Fire mentions Flying, so it gets `placement_rules`, `immunity`); old hand reviews over-tag `terrain`. About 70 wrong Into the Breach tags come from these two.
- Wording found in the check: "Upgrade:" lines are `upgrade` ("Upgrades:" lists are not); "Deploy a ... mine" and "spawned by other Vek" are `summon`; "Freeze yourself" is `friendly_fire`; "Repair adjacent Mechs" is `heal`.

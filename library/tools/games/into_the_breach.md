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

## Sources and notes

Sources:
[1] https://intothebreach.fandom.com/wiki/Weapons?oldid=3699 (weapon list by mech class)
[2] https://www.giantbomb.com/profile/majormitch/blog/thoughts-on-into-the-breachs-squads/116986/ (squads)

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
signature	Ranged	ranged	artillery	https://intothebreach.fandom.com/wiki/Weapons?oldid=3699
signature	Science	swap	swap	https://intothebreach.fandom.com/wiki/Weapons?oldid=3699
signature	Science	shield	shields	https://intothebreach.fandom.com/wiki/Weapons?oldid=3699
archetype	Science	positional	utility: pull, push, swap	https://intothebreach.fandom.com/wiki/Weapons?oldid=3699
splash	Prime	shield	only Spartan Shield	https://intothebreach.fandom.com/wiki/Weapons?oldid=3699
splash	Brute	shield	Phase Cannon, Grappling Hook	https://intothebreach.fandom.com/wiki/Weapons?oldid=3699
```

## Notes from the patterns check
Patterns check, 26 Oct 2026 (key wrong 70.5 → 53.3, missed 36.2 → 13.7 per 100 on the corrected key; cases below).
- Damage types (Kaptain's rules, tree v3): `multi_target_attack` = several separately named targets (the player chooses them, or one chosen plus a fixed one); `aoe_damage` = damage reaching several units without choosing each (around the target, a row, all); `random_target` = a random target. Every Into the Breach weapon with a fixed pattern (beams, lines, two projectiles, adjacent tiles) is `aoe_damage` plus `area_templates` (a named shape) and/or `adjacency` (neighbours); chained or bounced damage (Electric Whip, Ricochet Rocket) is `damage` only. A weapon that only pushes the neighbours (Artemis Artillery) is `damage` plus `adjacency`.
- Key changes (Claude, Kaptain's rule "change the key where sure"): smoke entries `suppress` → `attack_lock` (as the Smoke keyword key; Submerged stays `suppress`); `silence` removed from the three A.C.I.D. entries (it doubles damage taken, it does not remove an ability); `ranged` added to 8 projectile weapons; `adjacency` added to 8 "push adjacent tiles" weapons; Thermal Discharger `area_templates`; Aerial Bombs and Jet Mech `attack_lock`.
- Cases removed (the cards show no lead of 1.5 times or more): signature Prime damage 84% vs 59%, Prime forced_movement 55% vs 69%, Brute damage 79% vs 61%, Brute forced_movement 76% vs 61%, Ranged forced_movement 62% vs 66%, Science forced_movement 68% vs 64%, Science damage_over_time 12% vs 9%, Science disable 1 of 25 cards; splash Prime damage_over_time 10% vs 10%, Brute disable 0 of 29. Kept and met: Science swap and shield, the Science positional archetype, splash Prime and Brute shield. Open: the combo Electric Whip + Grappling Hook is real but the library finds no link (no relation between forced_movement and adjacency); signature Ranged `ranged` (65% vs 36%, lift 1.8) is still not found by signature.py.
- Open (shared, for its own pass): entries that only mention a keyword inherit its tags (Fire mentions Flying, so it gets `placement_rules`, `immunity`); old hand reviews over-tag `terrain`. About 70 wrong Into the Breach tags come from these two.
- Wording found in the check: "Upgrade:" lines are `upgrade` ("Upgrades:" lists are not); "Deploy a ... mine" and "spawned by other Vek" are `summon`; "Freeze yourself" is `friendly_fire`; "Repair adjacent Mechs" is `heal`.

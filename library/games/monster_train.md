# Monster Train

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: single-player roguelike deckbuilder (Shiny Shoe, 2020), with The Last Divinity DLC.
- Board: a train with 3 floors and the Pyre on top. Enemies enter the bottom floor and move up a floor after each combat; units fight on the same floor.
- Lose: the Pyre loses all its health; a run is won by beating the final boss.
- Turn: play cards with Ember (refilled each turn), place units on floors (each floor has limited capacity), then combat resolves floor by floor.
- Clans: a run picks a primary and an allied clan; the primary clan gives the Champion.
- Specific: buffs and debuffs are status stacks; the rules and terms are listed in full under Mechanics.

## The game's rules (from sources)
*Checked 29 Oct 2026 against https://www.bluestacks.com/blog/game-guides/monster-train/mstn-beginners-guide-en.html.*
- Floors: three floors where units are placed, and the Pyre on top; combat happens on the floor the enemies are on; enemies
  climb one floor at the end of each turn if they survive; an enemy that reaches the top attacks the Pyre.

## Sources and notes

Sources:
[1] https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/
[2] https://progameguides.com/monster-train/best-builds-in-monster-train/
[3] https://indiecator.org/2021/07/12/monster-train-my-favourite-clans/ (blog)

Clanless is not a clan. Monster Train 2 pages are not used. Rage (an attack bonus that wears off) is temporary_buff;
Burnout (dies when its stacks run out) is self_destruct; Reform (back to hand stronger after dying) is revive.

## Factions

### Hellhorned
*Claude:* Demons: Rage, Armor and imps.
Known for: Multistrike, Rage, Imps (cheap minions with strong abilities), glass-cannon offence [1]; Imp Parade makes Imps,
Imperialist deals damage when Imps die [2]; buffing one unit to be very strong [3].
Builds: Imp build [1][2].

### Awoken
*Claude:* Spirits of nature: Spikes, healing and sturdy walls.
Known for: Sweep (hits every enemy on the floor), tanks: giant minions that protect fragile ones [1]; tanks for Frostbite [2].

### Stygian Guard
*Claude:* Sea creatures: Frostbite, spells and Spell Weakness.
Known for: powerful spells, weak minions [1]; Frostbite, damage at the end of each turn that shrinks each turn [2].

### Umbra
*Claude:* Shadows: Morsels that units eat for bonuses.
Known for: strong champions and minions, defensive spells [1]; units eating Morsels or Primordium for their buffs [2]; Gorge,
buffing units by killing other units [3].

### Melting Remnant
*Claude:* Wax: Burnout, Reform and units that come back.
Known for: minions with death abilities that come back with upgraded stats, wanting minions to die soon [1]; Burnout and
Reform [2]; Harvest (the champion grows when units die), short-lived units that hit hard [3].

### Wurmkin
*Claude:* DLC clan: Echo on floors, Infused and Extract cards.
Known for: Charged Echoes, Hatching Eggs; Infused cards and devouring Eggs buff monsters [1].

## Combos
- Molded + Rector Flicker: Molded returns the fallen Flicker to hand by Reform [2]
- Crushing Demise + Rector Flicker: it kills a friendly unit, Flicker upgrades on each death and Reform [2]
- Cannibalize + Penumbra: Cannibalize gives Morsels for Penumbra to Gorge on [2]
- Morselmaker + Penumbra: Morselmaker summons Morsels for Penumbra to eat [2]

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name: name|expected concept|wording on the cards. Checked with coverage.py --mechanics.
# https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/ , https://indiecator.org/2021/07/12/monster-train-my-favourite-clans/
# Rules and terms for the game block (key.py read), only facts the source states: https://railtools.net/monster-train-2/keywords/
# term: Armor: absorbs incoming damage before health is lost, one point per point of Armor.
# term: Avarice: unblocked damage from this unit grants Gold equal to its stacks.
# term: Buffet: this unit can be eaten more than once.
# term: Burnout: the unit dies when its stacks run out; the count drops each turn.
# term: Burst: extra attacks per stack, losing one stack after each bonus attack.
# term: Conduit: adds Magic Power to the floor for each stack.
# term: Cooldown: the unit's ability can't be used while stacks remain.
# term: Damage Shield: blocks the next source of damage.
# term: Dazed: can't attack or use Action or Resolve abilities; wears off each turn.
# term: Decay: 3 damage per stack at turn end; fades each turn.
# term: Emberdrain: costs 1 Ember per stack at the start of each turn; fades each turn.
# term: Endless: when the unit dies or is eaten, its card returns to the top of the draw pile.
# term: Fragile: the unit dies if it loses any health.
# term: Frostbite: 1 damage per stack at turn end; fades each turn.
# term: Fuel: cancels Inert and Dormant; loses one stack each turn.
# term: Hatch: Corrupt on the floor removes Hatch from the front unit; the unit hatches once all Hatch is gone.
# term: Immobile: the unit can't change floors or its position on its floor.
# term: Inert: can't attack unless the unit has Fuel.
# term: Lifesteal: heals by the damage dealt on attack; weakens with each attack.
# term: Mageblade: Attack per stack equal to the floor's Magic Power.
# term: Melee Weakness: the next attack against the unit deals extra damage per stack.
# term: Multistrike: one additional attack each turn.
# term: Mute: disables triggers, abilities and enchants; fades each turn.
# term: Pyregel: more incoming damage per stack.
# term: Quick: attacks before enemy units in combat.
# term: Rage: Attack per stack; fades each turn.
# term: Reanimate: when the unit dies it comes back with 1 health, costing one stack.
# term: Reap: 1 damage per Corrupt stack on the floor after combat; does not fade.
# term: Regen: restores health per stack at turn end; fades each turn.
# term: Rooted: blocks the next floor change (bosses are immune).
# term: Sap: less Attack per stack; fades each turn.
# term: Spell Weakness: the next damage spell hit deals extra damage per stack.
# term: Spikes: attackers take damage per stack when they hit this unit.
# term: Stealth: can't be targeted in combat; fades each turn.
# term: Steelguard: limits Armor loss per hit to a set amount.
# term: Sweep: attacks all enemy units.
# term: Titanskin: less damage taken by a set amount per stack.
# term: Trample: excess attack damage carries over to the next enemy unit.
# term: Troop: Attack and Health per stack; losing one stack's worth of Health removes a stack.
# term: Unstable: dies at end of combat if its HP is at or below its stacks, then explodes for damage to enemies on the floor.
# term: Valor: Attack per stack, and Armor raised to the stack count if this is the front unit after combat.
# term: Armored (trigger): when Armor is added to this unit.
# term: Artificer (trigger): when Equipment is attached to an ally of this unit.
# term: Celebrate (trigger): after a boss is defeated.
# term: Consume: once played, the card is removed from the deck for the rest of the battle.
# term: Eaten (trigger): when the front unit eats this unit.
# term: Enchant: an aura giving other units on the floor the listed bonus.
# term: Equipped (trigger): when Equipment is attached to this unit.
# term: Etch (trigger): when a card is consumed on this floor.
# term: Extinguish (trigger): when this unit dies.
# term: Gorge (trigger): when this unit eats another unit.
# term: Harvest (trigger): when any unit dies on this floor.
# term: Hunger (trigger): when a unit with Eaten is summoned.
# term: Incant (trigger): when a spell is played on this floor.
# term: Inspire (trigger): when the clan's resource is gained on this floor.
# term: Mooncycle (trigger): when the moon changes phase.
# term: Moonlit: active while the moon is in its Moonlit phase.
# term: Moonshade: active while the moon is in its Moonshade phase.
# term: Propagate: raises existing buff stacks on friendly units and debuff stacks on enemies by the stated amount, except Dazed.
# term: Rally (trigger): when a friendly unit is summoned on this floor.
# term: Reanimated (trigger): when this unit is revived by Reanimate.
# term: Rejuvenate (trigger): when this unit is healed, even at full health.
# term: Resolve (trigger): after combat.
# term: Revenge (trigger): when this unit is hit.
# term: Shift (trigger): whenever this unit moves.
# term: Slay (trigger): after dealing a killing blow.
# term: Strike (trigger): when this unit attacks.
# term: Summon (trigger): when this unit is played.
# term: Unplayable: this card cannot be played.
# Rules and terms, second source (only facts it states): https://monster-train.fandom.com/wiki/Frozen
# term: Frozen: the card is not discarded at the end of the turn and stays in hand until played.
# term: Permafrost: when drawn, the card gains Frozen.
# term: Purge: once played, the card is removed from the deck for the rest of the run.
# term: Reserve (trigger): if the card is still in hand when the turn ends.
# term: Piercing: the card's damage ignores Armor and Damage Shield.
# term: Pyrebound: can only be played in the Pyre Room and the floor directly below it.
# term: Attuned: Magic Power effects on the card count five times.
# term: Offering: if the card is discarded before the end of the turn, it is played instead (not when Purged or Consumed by other effects).
# term: Infused: when played, the current floor gains 1 Echo.
# term: Magic Power: increases the damage and healing of spells.
# term: Extract: playing the card costs 1 Echo; with none it can't be played.
# term: Unpurgeable: can't be removed by shops or Unstable Vortexes.
# term: Ascend: moves a unit up a floor, to the back of that floor.
# term: Descend: moves a unit down a floor, to the back of that floor (not onto a frozen floor).
# term: Reform: returns a defeated friendly unit to the hand as an upgraded version.
# term: Cultivate: raises the max and current health and the attack of the lowest-health friendly unit by the Cultivate value.
# Rules and terms assumed from game knowledge (no source found; Kaptain: assume when no source exists)
# term: Action (trigger): the unit's ability happens on its turn in combat. (assumed)
# term: Charged Echo: Echo stored on a floor that other cards spend for an effect. (assumed)
# term: Phased: the unit can't attack or be attacked while it is phased. (assumed)
# term: Shell: absorbs damage per stack; when the last stack is gone, the unit's Hatch ability happens. (assumed)
# term: Silence: the unit's abilities and triggers stop working. (assumed)
multistrike|multi_attack|\bmultistrike\b
rage|stat_gain|\brage\b
sweep|aoe_damage|\bsweep\b
incant|on_spell|\bincant\b
frostbite|damage_over_time|\bfrostbite\b
morsels|summon|\bmorsel
gorge|on_sacrifice|\bgorge\b
reform|revive|\breform
burnout|self_destruct|\bburnout\b
eggs|transform|\b(hatch|shell \d)
harvest|other_death_trigger|\bharvest\b
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Hellhorned	multi_attack	Multistrike	https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/
signature	Hellhorned	temporary_buff	Rage	https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/
signature	Hellhorned	tribal	Imps	https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/
signature	Hellhorned	summon	Imp Parade makes Imps	https://progameguides.com/monster-train/best-builds-in-monster-train/
signature	Awoken	aoe_damage	Sweep	https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/
signature	Awoken	tank	giant minions that protect others	https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/
signature	Stygian Guard	damage_over_time	Frostbite	https://progameguides.com/monster-train/best-builds-in-monster-train/
signature	Umbra	sacrifice	buffing units by killing other units	https://indiecator.org/2021/07/12/monster-train-my-favourite-clans/
signature	Umbra	stat_gain	eating Morsels for their buffs	https://progameguides.com/monster-train/best-builds-in-monster-train/
signature	Melting Remnant	death_trigger	minions with death abilities	https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/
signature	Melting Remnant	revive	Reform	https://progameguides.com/monster-train/best-builds-in-monster-train/
signature	Melting Remnant	self_destruct	Burnout	https://progameguides.com/monster-train/best-builds-in-monster-train/
signature	Melting Remnant	other_death_trigger	Harvest	https://indiecator.org/2021/07/12/monster-train-my-favourite-clans/
signature	Wurmkin	buff	Infused cards and Eggs buff monsters	https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/
archetype	Hellhorned	aggro_tempo	glass-cannon offence	https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/
archetype	Hellhorned	tribal	Imp build	https://progameguides.com/monster-train/best-builds-in-monster-train/
archetype	Awoken	fortress	tanks	https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/
archetype	Stygian Guard	spellslinger	powerful spells	https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/
archetype	Stygian Guard	poison_attrition	Frostbite	https://progameguides.com/monster-train/best-builds-in-monster-train/
archetype	Umbra	sacrifice	killing units to buff others	https://indiecator.org/2021/07/12/monster-train-my-favourite-clans/
archetype	Melting Remnant	sacrifice	wanting minions to die	https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/
combo	Molded	Rector Flicker	returns the fallen Flicker by Reform	https://progameguides.com/monster-train/best-builds-in-monster-train/
combo	Crushing Demise	Rector Flicker	Flicker upgrades on each death	https://progameguides.com/monster-train/best-builds-in-monster-train/
combo	Cannibalize	Penumbra	Morsels for Penumbra to Gorge on	https://progameguides.com/monster-train/best-builds-in-monster-train/
combo	Morselmaker	Penumbra	Morsels for Penumbra	https://progameguides.com/monster-train/best-builds-in-monster-train/
```

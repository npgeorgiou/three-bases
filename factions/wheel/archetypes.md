# The archetypes in this game (made from archetypes.tsv by work/archetypes_plain.py; all Claude's)

Engine: a part that works by feeding another part of the same archetype. Brick: a part that works alone.

## Aggro
Cheap units take two bases in rounds 1-2, before the enemy has a board.

- **cheap units that hit hard at once** (brick): Act the turn it arrives (haste, rush); Attack right away; Attack gain (+attack); Excess damage carries on (trample); Cost matters; In or entering enemy territory.
- **many cheap plays, and units that gain from each** (engine): Summon units / tokens; Cards cost less; Set a cost to a fixed number; When I play another card; Grows with what happened this game.
- **clear the unit cancelling my dot** (brick): Deal damage; Small repeatable damage; My unit fights a chosen enemy; Mark a target for later hits; Damaged unit matters; Move enemy units (push, pull); Send an enemy unit back (bounce); Can't attack (lock on an enemy).

## Control
Remove every enemy unit that comes, then hold the bases late with a few big units.

- **answers to every enemy unit** (engine): Destroy outright; Deal damage; Mark a target for later hits; Damaged unit matters; Damage to many at once; Board wipe; Small repeatable damage; Damage to several separate targets; My unit fights a chosen enemy; Any damage kills (deathtouch, poisonous); Stat loss (-power, -health); Attack set to 0; Make a unit weaker (debuff); Silence (abilities removed); Can't act at all (stun, freeze); Send an enemy unit back (bounce); Banish / exile (gone for good); Move enemy units (push, pull).
- **cards keep coming from the removal** (engine): When it kills; Counts deaths; Grows with what happened this game; Draw cards; Create new cards; Look at cards and pick (scry); Reuse my cards (shuffle back).
- **a few finishers that are hard to answer** (brick): Stats equal to a count; Grows again and again; Immune / can't be targeted; Keep my units alive (protection); Absorb one hit (shield, ward); Heal every turn (regeneration); Cheat death (survive lethal).

## Midrange
Units that are hard to remove and give more than one card's worth, with removal for any enemy.

- **units that are hard to remove** (brick): Keep my units alive (protection); Absorb one hit (shield, ward); Cheat death (survive lethal); Take less damage (armour); Block points that wear off; Heal every turn (regeneration); Immune / can't be targeted; Restore health (heal).
- **units that give more than their body** (engine): Summon units / tokens; Draw cards; Create new cards; When it dies (deathrattle); Copy cards or units; When it kills; Grows again and again.
- **removal for any enemy, much of it by my units fighting** (engine): My unit fights a chosen enemy; Destroy outright; Deal damage; Damage to several separate targets; Stat loss (-power, -health); Silence (abilities removed); Send an enemy unit back (bounce); When it kills.

## Tempo
Cheap units take the front cells; cheap cards stop the enemy units that could remove them.

- **cheap units that hit at once** (brick): Act the turn it arrives (haste, rush); Attack right away; Attack gain (+attack); Stealth / hidden until it acts; Cards cost less.
- **cheap cards that stop or move enemy units** (brick): Send an enemy unit back (bounce); Move enemy units (push, pull); Swap positions; Can't attack (lock on an enemy); Can't act at all (stun, freeze); Can't move (root); Silence (abilities removed); Stat loss (-power, -health); Attack set to 0; Make the opponent's cards cost more; Attack the opponent's hand.
- **cheap cards that keep my units alive** (brick): Keep my units alive (protection); Absorb one hit (shield, ward); Immune / can't be targeted; Return my unit to hand.

## Combo
A game is won only by holding bases, so the combo is two cards that set each other off again and again inside one action, and the loop takes the lane.

- **find the pieces** (brick): Search the deck for a card (tutor); Draw cards; Look at cards and pick (scry); Better or chosen cards; Top or bottom of the deck matters; Create new cards; Copy cards or units.
- **a card that resets or repeats another card** (engine): Repeat or double triggers; Ready a used unit again (untap); Return my unit to hand; Reuse my cards (shuffle back); Bring back dead units (revive); Put into play for free; Set a cost to a fixed number; Cards cost less; Copy cards or units; Extra turns or actions.
- **a card that gains each time the first one works** (engine): Having a card in play or hand; When I play another card; When a spell is played; When it dies (deathrattle); When another unit dies; When a unit is sacrificed; When it leaves play; When another unit leaves play; When a card is drawn; When a card is discarded; Order of my plays matters (combo); Grows with what happened this game; Grows again and again; Small repeatable damage.

## Aggro-Combo
Cheap units take lanes early, then one play makes them much stronger at once and takes the last base.

- **early pressure: many cheap units** (engine): Summon units / tokens; Act the turn it arrives (haste, rush); Attack right away; When I play another card; Cards cost less.
- **the sudden finish: grows with the units already there** (engine): Stats equal to a count; Counts / thresholds; Grows with what happened this game; Double or multiply stats; Attack gain (+attack); Attack more than once; Attack right away; Damage to many at once; Put into play for free.

## Control-Combo
Remove every enemy unit early, then the loop of Combo.

- **answers to every enemy unit** (brick): Destroy outright; Deal damage; Mark a target for later hits; Damaged unit matters; Damage to many at once; Board wipe; Small repeatable damage; Damage to several separate targets; My unit fights a chosen enemy; Any damage kills (deathtouch, poisonous); Stat loss (-power, -health); Attack set to 0; Make a unit weaker (debuff); Silence (abilities removed); Can't act at all (stun, freeze); Send an enemy unit back (bounce); Banish / exile (gone for good); Move enemy units (push, pull).
- **find the pieces** (brick): Search the deck for a card (tutor); Draw cards; Look at cards and pick (scry); Better or chosen cards; Top or bottom of the deck matters; Create new cards; Copy cards or units.
- **a card that resets or repeats another card** (engine): Repeat or double triggers; Ready a used unit again (untap); Return my unit to hand; Reuse my cards (shuffle back); Bring back dead units (revive); Put into play for free; Set a cost to a fixed number; Cards cost less; Copy cards or units; Extra turns or actions.
- **a card that gains each time the first one works** (engine): Having a card in play or hand; When I play another card; When a spell is played; When it dies (deathrattle); When another unit dies; When a unit is sacrificed; When it leaves play; When another unit leaves play; When a card is drawn; When a card is discarded; Order of my plays matters (combo); Grows with what happened this game; Grows again and again; Small repeatable damage.

## Prison / Stax
Rules that bind only the enemy: his units can't move, attack or act, his cards cost more, his cells and hand fill with junk.

- **restrictions on the enemy only** (engine): Make the opponent's cards cost more; Can't attack (lock on an enemy); Can't act at all (stun, freeze); Can't move (root); Silence (abilities removed); Attack set to 0; Attack the opponent's hand; Row-wide lasting effects (weather); Terrain / board features; Clog the opponent's board; Junk cards into a deck or hand; Taunt (enemies must attack it); Force enemy units to attack; Change the game's rules.
- **punish him for acting** (engine): When an enemy arrives; When it becomes a target; Strike back when attacked (counterattack, thorns); When it is damaged.

## Tokens / Go-Wide
Many small units in a lane, and cards that make all of them stronger.

- **many small units** (engine): Summon units / tokens; Copy cards or units; Create new cards; Bring back dead units (revive); Cards cost less.
- **bonuses for all of them** (engine): Attack gain (+attack); Defence gain (+health); Stat gain (+power, +health); Make a unit stronger (buff); Help from nearby allies (assists); Stats equal to a count; Counts / thresholds; Grows with what happened this game; When I play another card.

## Voltron
One unit gets bonus after bonus and holds a base alone.

- **bonuses piled on one unit** (engine): Attack gain (+attack); Defence gain (+health); Stat gain (+power, +health); Make a unit stronger (buff); Double or multiply stats; Set stats to a number; Attack more than once; Excess damage carries on (trample).
- **the unit gains more each time it gets one** (engine): When it becomes a target; Grows again and again; Stats matter (highest, lowest).
- **keep that unit alive** (brick): Keep my units alive (protection); Absorb one hit (shield, ward); Immune / can't be targeted; Stealth / hidden until it acts; Cheat death (survive lethal); Heal every turn (regeneration); Take less damage (armour); Restore health (heal); Return my unit to hand.

## +1/+1 Counters
Units that keep the strength or defence they gain, then gain it twice over.

- **units that grow and keep it** (engine): Grows again and again; Stat gain (+power, +health); Attack gain (+attack); Defence gain (+health); Make a unit stronger (buff).
- **the growth is doubled, repeated or copied** (engine): Double or multiply stats; Repeat or double triggers; Copy cards or units; Stats equal to a count.
- **cards that care about big stats** (engine): Stats matter (highest, lowest); A unit levels up on the board; Strikes with its defence.

## Extra Combats
A unit attacks more than once in a turn or a round.

- **attack again** (engine): Attack more than once; Ready a used unit again (untap); Attack right away; Extra turns or actions; My unit fights a chosen enemy.
- **something happens each time it attacks** (engine): When it attacks; When it fights; When it kills; Grows again and again; Strikes of a given size; Excess damage carries on (trample); Lifesteal / drain.
- **survive the attacks** (brick): Heal every turn (regeneration); Restore health (heal); Take less damage (armour); Cheat death (survive lethal); Absorb one hit (shield, ward).

## Defenders / Toughness Matters
Units with high defence that hit with their defence.

- **high defence** (engine): Defence gain (+health); Take less damage (armour); Block points that wear off; Heal every turn (regeneration); Restore health (heal); When life or health is restored.
- **hits as hard as its defence** (engine): Strikes with its defence; Set stats to a number; Strike back when attacked (counterattack, thorns).
- **make the enemy hit the walls** (engine): Taunt (enemies must attack it); Force enemy units to attack; When it is damaged.

## Toolbox
Fetch from the deck the unit that answers what the enemy has.

- **fetch a chosen card** (engine): Search the deck for a card (tutor); Look at cards and pick (scry); Top or bottom of the deck matters; Create new cards; Better or chosen cards; Copy cards or units.
- **a different answer on each unit** (brick): Destroy outright; Deal damage; Damage to many at once; Silence (abilities removed); Can't act at all (stun, freeze); Send an enemy unit back (bounce); Move enemy units (push, pull); Keep my units alive (protection); Absorb one hit (shield, ward); Restore health (heal).
- **fetch it again** (engine): Reuse my cards (shuffle back); Return my unit to hand; Bring back dead units (revive).

## Aristocrats
I kill my own units, and other cards gain each time one dies.

- **units to kill: cheap, made or coming back** (engine): Summon units / tokens; Bring back dead units (revive); Cheat death (survive lethal); Destroys itself / temporary unit.
- **kill my own units** (engine): Sacrifice my own units; Destroys itself / temporary unit; Hits my own side too; Board wipe.
- **gain when a unit dies** (engine): When it dies (deathrattle); When another unit dies; When a unit is sacrificed; Counts deaths; Grows with what happened this game; Grows again and again; Gain resources (ramp).

## Reanimator
Big units go to the discard pile early, then come back for little supply.

- **put big units in the discard pile** (engine): Fill my own discard pile (self-mill); Discard my own cards; Sacrifice my own units; Destroys itself / temporary unit; Hits my own side too.
- **bring them back cheaply** (engine): Bring back dead units (revive); Return my unit to hand; Reuse my cards (shuffle back); Put into play for free; Set a cost to a fixed number; Cards cost less.

## Dredge / Self-Mill
Cards go from my deck and hand to my discard pile, and other cards use them from there.

- **fill my discard pile** (engine): Fill my own discard pile (self-mill); Discard my own cards; Sacrifice my own units; Destroys itself / temporary unit; Hits my own side too.
- **use the cards there** (engine): Reuse my cards (shuffle back); Bring back dead units (revive); Return my unit to hand; Put into play for free; Banish / exile (gone for good); Grows with what happened this game; Counts / thresholds; Deck contents matter.

## Delirium / Threshold
Once my discard pile holds enough cards, or enough different ones, cards get a bonus.

- **fill my discard pile** (engine): Fill my own discard pile (self-mill); Discard my own cards; Sacrifice my own units; Destroys itself / temporary unit; Hits my own side too.
- **a bonus past a number** (engine): Counts / thresholds; Variety matters (all different); Grows with what happened this game; Counts deaths; A unit levels up on the board; Stats equal to a count.

## Graveyard Recursion
Cards come back from the discard pile and are played again.

- **play cards again from the discard pile** (engine): Reuse my cards (shuffle back); Return my unit to hand; Bring back dead units (revive); Put into play for free; Cards cost less.
- **cards worth playing again** (engine): Summon units / tokens; Draw cards; Deal damage; Damage to many at once; Gain resources (ramp); When it dies (deathrattle); When I play another card.

## Madness
I discard cards and gain from it.

- **discard my cards** (engine): Discard my own cards; Hand size matters.
- **gain when a card is discarded** (engine): When a card is discarded; Alternative costs; Put into play for free; Grows again and again; Grows with what happened this game; Set stats to a number; Stats equal to a count.
- **refill the hand** (engine): Draw cards; Create new cards.

## Spellslinger / Prowess
Many cheap spells, and units that gain from each.

- **many cheap spells** (engine): Cards cost less; Set a cost to a fixed number; Create new cards; Copy cards or units; Reuse my cards (shuffle back); Improve cards in hand or deck; Upgrade a card.
- **gain from each spell** (engine): When a spell is played; Enough spells played; My spells and abilities get stronger; Grows with what happened this game; Order of my plays matters (combo); Grows again and again; Put into play for free; Repeat or double triggers.

## Storm
One action per turn, so "one turn" becomes one round: gains from how many cards I played this round.

- **play many cards** (engine): Cards cost less; Set a cost to a fixed number; Put into play for free; Draw cards; Create new cards; Copy cards or units; Return my unit to hand; Gain resources (ramp).
- **gain from how many** (engine): Grows with what happened this game; Order of my plays matters (combo); When I play another card; When a spell is played; Enough spells played; Counts / thresholds; Stats equal to a count; Grows again and again.

## Blink / Flicker
A unit leaves and comes back, and its Place fires again (Place fires every time a unit enters).

- **the unit leaves and comes back** (engine): Return my unit to hand; Bring back dead units (revive); Reuse my cards (shuffle back); Repeat or double triggers; Copy cards or units; Put into play for free; Cards cost less.
- **what fires again** (engine): When it leaves play; When another unit leaves play; When I play another card; Summon units / tokens; Draw cards; Deal damage; Destroy outright; Create new cards; Gain resources (ramp).

## Cascade / Discover
Without randomness: new cards picked from a set the player sees.

- **new cards picked from a set** (engine): Create new cards; Look at cards and pick (scry); Copy cards or units; Put into play for free; Better or chosen cards; Top or bottom of the deck matters.
- **gain from the made cards** (engine): Hand size matters; Variety matters (all different); Grows with what happened this game; When a card is drawn.

## Clone / Copy
Copy my best unit or spell.

- **copy a card, a unit or its stats** (engine): Copy cards or units; Repeat or double triggers; Set stats to a number; Create new cards.
- **the unit worth copying** (engine): Grows again and again; Double or multiply stats; When it dies (deathrattle); When I play another card; Stats matter (highest, lowest).

## Cheat-into-Play
Big units come in without their supply paid.

- **put a unit in for free or for less** (engine): Put into play for free; Set a cost to a fixed number; Cards cost less; Alternative costs; Bring back dead units (revive); Improve cards in hand or deck.
- **big units, and cards that care about them** (engine): Cost matters; Stats matter (highest, lowest); Stats equal to a count; Excess damage carries on (trample).

## Eggs
Cheap units die for value and come back to die again.

- **cheap units that die and give something** (engine): Destroys itself / temporary unit; Sacrifice my own units; Hits my own side too; When it dies (deathrattle); Summon units / tokens.
- **they come back** (engine): Return my unit to hand; Bring back dead units (revive); Reuse my cards (shuffle back); Cheat death (survive lethal); When it leaves play.
- **gain from all the dying** (engine): When another unit dies; Counts deaths; Grows with what happened this game; When a unit is sacrificed.

## Ramp
More supply in a lane early (a lane holds at most 12), then big spells.

- **more supply in a lane, or cards that cost less** (engine): Gain resources (ramp); More or faster base resource (ramp); Cards cost less; Set a cost to a fixed number; Alternative costs; Return my unit to hand.
- **big spells** (engine): Board wipe; Damage to many at once; My spells and abilities get stronger; Cost matters; Summon units / tokens; Stats equal to a count.

## Stompy
More supply in a lane early, then big units.

- **more supply in a lane, or cards that cost less** (engine): Gain resources (ramp); More or faster base resource (ramp); Cards cost less; Set a cost to a fixed number; Alternative costs; Return my unit to hand.
- **big units, and cards that care about them** (engine): Cost matters; Stats matter (highest, lowest); Stats equal to a count; Grows again and again; Excess damage carries on (trample).

## Discard / 8-Rack
Empty the enemy's hand, then punish him for holding few cards.

- **take, discard or tax the cards in his hand** (engine): Attack the opponent's hand; Hidden and revealed information; Steal from the opponent; Make the opponent's cards cost more.
- **punish a small hand** (engine): Hand size matters; Counts / thresholds.

## Wheels
Discard my hand and draw a new one, and cards gain from each draw and discard (hand limit 10).

- **draw and discard many** (engine): Draw cards; Discard my own cards; Hand size matters; Reuse my cards (shuffle back); Create new cards; Look at cards and pick (scry).
- **gain from draws and discards** (engine): When a card is drawn; When a card is discarded; Grows with what happened this game; Grows again and again; Double or multiply stats; Stats equal to a count.

## Cycling
Swap a card I don't want for a new one, and gain from the swap.

- **swap a card for a new one** (engine): Discard my own cards; Draw cards; Reuse my cards (shuffle back); Look at cards and pick (scry); Top or bottom of the deck matters; Better or chosen cards.
- **gain from the swap** (engine): When a card is discarded; When a card is drawn; Grows with what happened this game; Grows again and again.

## Pillowfort
No player to attack: attacks on my units in a lane are made bad for the attacker.

- **attacking my units is pointless** (brick): Keep my units alive (protection); Absorb one hit (shield, ward); Immune / can't be targeted; Stealth / hidden until it acts; Take less damage (armour); Block points that wear off; Heal every turn (regeneration); Taunt (enemies must attack it).
- **the attacker pays** (engine): Strike back when attacked (counterattack, thorns); When it is damaged; Any damage kills (deathtouch, poisonous); Make the opponent's cards cost more; When an enemy arrives.

## Turbo-Fog
No answers on the enemy's turn: on my turn, stop his attacks again and again while I hold the bases.

- **stop his attacks or their damage** (engine): Can't attack (lock on an enemy); Can't act at all (stun, freeze); Can't move (root); Attack set to 0; Move enemy units (push, pull); Take less damage (armour); Absorb one hit (shield, ward); Keep my units alive (protection); Immune / can't be targeted.
- **get those cards again** (engine): Reuse my cards (shuffle back); Return my unit to hand; Copy cards or units; Draw cards; Create new cards.

## Hatebears / Death & Taxes
Small units that each bind the enemy, and less supply for him (his supply comes from his units in the lane).

- **small units that disrupt** (brick): Silence (abilities removed); Make the opponent's cards cost more; Can't attack (lock on an enemy); Can't move (root); Can't act at all (stun, freeze); Attack the opponent's hand; Stat loss (-power, -health); When an enemy arrives; Taunt (enemies must attack it).
- **less supply for him: his units gone or taken** (brick): Destroy outright; Deal damage; Small repeatable damage; Send an enemy unit back (bounce); Banish / exile (gone for good); Steal from the opponent; Make the opponent's cards cost more.

## Theft
Take the enemy's units or cards for myself.

- **take or copy enemy units or cards** (engine): Steal from the opponent; Copy cards or units; Attack the opponent's hand.
- **use what I took** (engine): Sacrifice my own units; Move my units (reposition); Move enemy units (push, pull); When it attacks; Give my units or cards to the opponent.

## Aikido / Judo
The enemy's attacks and spells turn back on him, by triggers on my units, not answers.

- **make him hit where I want** (engine): Taunt (enemies must attack it); Force enemy units to attack.
- **his hits and spells come back at him** (engine): Strike back when attacked (counterattack, thorns); When it is damaged; When it becomes a target; Strikes with its defence; Any damage kills (deathtouch, poisonous); Steal from the opponent; Copy cards or units.

## Extra Turns
Extra actions, played again and again.

- **extra actions** (engine): Extra turns or actions; Ready a used unit again (untap); Attack right away.
- **play them again** (engine): Return my unit to hand; Reuse my cards (shuffle back); Copy cards or units; Repeat or double triggers; Order of my plays matters (combo); Create new cards.

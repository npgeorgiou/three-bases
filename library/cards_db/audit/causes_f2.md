# Faeria part g: causes found (partial check, stopped by coordinator)

Read: lines 462-1742; not read: lines 1743-3524

Groups read in full: "they reach enemy ground", "it can enter where it needs to be", "turns a land into the colour it needs", "within reach of the enemy player", "kills it for its death effect", "{A} moves your units, and {B} acts on units next to it", "moves it where it must be", "can give it more power and health". Not read: from "clears its line of fire" (line 1740) to the end.

## Cause 1. A unit's own movement keyword is read as moving another card
Wrong thinking: a card with Flying, Jump, Dash or Charge moves my other units, so it gets that other card onto enemy land or to an enemy well.
Rule broken: L20 (a movement keyword works for the card that has it), L7 (Luduan: "whenever THIS harvests").
B's Corrupt (Faeria: when it moves onto enemy land) or "this harvests" needs B itself to move. A's keyword moves only A.
- Triton Warrior -> Kobold Smuggler: moves: moves my units or land forward: they reach enemy ground
- Sagami Warrior -> Baldurion, Evil Archsmith: moves: moves my units or land forward: they reach enemy ground
- Crystal Dragon -> Vile Bloatfly: moves: moves my units or land forward: they reach enemy ground
- Windborne Emissary -> Luduan: moves: moves my units or land forward: they reach enemy ground
- Khalim, Sky Prodigy -> Sapphire Yak: moves: moves my units or land forward: they reach enemy ground (Khalim is no Yak)
Rough count: about 40 of the 50 sampled lines of "they reach enemy ground" (about 2200 of 2712 overall). The lines are right only where A moves another unit or gives it movement (Flash Wind, Celestial Tower, Cloud Machine, Oradrim Fanatic, Windborne Champion, Syland Horsemaster, Mistral Guide, Khalim's Training, Secret of Strength, Majinata).

## Cause 2. A placement line goes to a card that has no placement need, or that asks for a kind A is not
Wrong thinking: any mover helps any card whose text mentions "adjacent" or a summon place.
Rule broken: L20 (a card asked for by kind must be that kind) and L1 (no need in B's text).
Topaz Yak asks for Yaks and Tide Lord asks for tritons; a mover that is neither gives nothing. Mother of All Yaks, Prophet of Tides and Coral Polliwog have no need about where they are summoned.
- Spear of the Guardians -> Topaz Yak: moves: moves my units or land forward: it can enter where it needs to be
- Magic Carpet -> Tide Lord: moves: moves my units or land forward: it can enter where it needs to be
- Demon Wing -> Mother of All Yaks: moves: moves my units or land forward: it can enter where it needs to be
- Rebel Glider -> Prophet of Tides: moves: moves my units or land forward: it can enter where it needs to be
- Flash Wind -> Coral Polliwog: moves: moves my units or land forward: it can enter where it needs to be
Rough count: about 25 of the 50 sampled lines (Topaz Yak, Tide Lord, Mother of All Yaks, Prophet of Tides, Coral Polliwog, Rakoakopter, Emerald Salamander as B).

## Cause 3. Something that moves nothing is read as a mover
Wrong thinking: destroying or changing lands counts as moving land forward.
Rule broken: L1 (the line must come from what A's text does).
- Meteor -> Luduan: moves: moves my units or land forward: they reach enemy ground (Meteor destroys lands)
- Baeru, the First Wave -> Bomb Slinger: moves: moves my units or land forward: it can enter where it needs to be (Baeru only turns lands next to it into lake)
Rough count: a few lines per group.

## Cause 4. A teleport to my own land is read as reaching enemy ground
Wrong thinking: any teleport triggers Corrupt.
Rule broken: L1. Desert Twister and Sagami Grovecaller teleport only to "a desert/forest you control", which is never enemy land.
- Desert Twister -> Baldurion, Evil Archsmith: waits: moves it for its effect
- Sagami Grovecaller -> Monstrous Hydra: waits: moves it for its effect
- Sagami Grovecaller -> Sapphire Yak: moves: moves my units or land forward: they reach enemy ground
Rough count: about 5 lines in the part.

## Cause 5. The same reason is said two or three times for one pair
Rule broken: L10 (one reason is said once, by its strongest kind).
"waits: moves it for its effect", "moves: ... they reach enemy ground" and "moves: moves it where it must be" are all given for one pair. "type: A moves your units, and B acts on units next to it" also repeats "it can enter where it needs to be".
- Celestial Tower -> Imperial Drakerider: three lines (waits / reach enemy ground / where it must be)
- Mistral Guide -> Lost Explorer: three lines
- Radiance, Scourge of Oversky -> Voice of Hunger: type ... acts on units next to it + moves ... it can enter where it needs to be
Rough count: about 30 pairs in the part.

## Cause 6. "Moves your units, and B acts on units next to it" from a unit's own movement, or from help aimed at any unit
Wrong thinking: a unit that can move itself next to Kobold Barracks, Rakoan Chieftain or Tiki Adventurer is a combo with them.
Rule broken: L1 (every creature can move next to another), L20 (the keyword moves only its owner), L14 (Secret of Strength, Triton Banquet: help to any creature).
- Triton Diver -> Kobold Barracks: type: Triton Diver moves your units, and Kobold Barracks acts on units next to it
- Unlikely Hero -> Rakoan Chieftain: type: Unlikely Hero moves your units, and Rakoan Chieftain acts on units next to it
- Secret of Strength -> Kobold Barracks: type: Secret of Strength moves your units, and Kobold Barracks acts on units next to it
- Thunder Eel -> Tiki Adventurer: type: Thunder Eel moves your units, and Tiki Adventurer acts on units next to it
Rough count: about 40 of the 50 sampled lines (all but the kind-matched ones such as Clockwork Yak -> Topaz Yak).

## Cause 7. A unit's own reach to the enemy god is linked to another card's "when a friendly creature attacks a god"
Wrong thinking: a Flying or Charge unit attacks the god, so it feeds every card that counts attacks on gods.
Rule broken: L20 (Nasus's Fearsome gets Nasus there, not Abyssal Eye) and L2 (attacking is what every unit does).
Some targets also do not fit: Defender of the Homeland waits for ME being attacked (L9, wrong direction). War Yak and Exalted Ogre wait for low enemy Life (more damage is generic, L18). Sky Anemone is a 0-attack building.
- Demon Wing -> Zealous Crusader: moves: moves it within reach of the enemy player
- Rakoan Chieftain -> Shaytan Scavenger: moves: moves it within reach of the enemy player
- Sunsilk Faerie -> Defender of the Homeland: moves: moves it within reach of the enemy player
- Demonic Salmon -> War Yak: moves: moves it within reach of the enemy player
- Sky Anemone -> The World's Tear: moves: moves it within reach of the enemy player
Rough count: about 40 of the 50 sampled lines.

## Cause 8. A transform removes B's text but is linked as helping that text
Wrong thinking: Frogify or The World's Tear moves B (the new form has Jump or Flying), so B's effect goes off.
Rule broken: L1 (after the transform, B's text is gone).
- Frogify -> Oradrim Monk: moves: moves it within reach of the enemy player
- Frogify -> Tax Collector: moves: moves it where it must be
- The World's Tear -> Krog, the Ogre King: moves: moves it where it must be
- The World's Tear -> Llamacorn: moves: moves it where it must be
Rough count: about 8 lines in the part.

## Cause 9. Movement is linked to "Combat -" cards
Wrong thinking: moving a unit lets its Combat effect go off.
Rule broken: L2 (only text that adds an attack or fight makes the line) and L4 (movement is not a fight).
- Windborne Champion -> King's Guard: moves: moves it where it must be
- Spirit Spice -> Krog, the Ogre King: moves: moves it where it must be
- Syland Horsemaster -> Underground Boss: moves: moves it where it must be
- Cloud Machine -> Herald of War: moves: moves it where it must be
Rough count: about 20 of the 50 sampled lines of "moves it where it must be".

## Cause 10. A card that destroys my deck is read as killing a creature
Wrong thinking: "Destroy your deck" is read as a kill.
Rule broken: L1.
- Void Guardian -> Village Elder: waits: kills it for its death effect
- Void Guardian -> Seifer's Fodder: waits: kills it for its death effect
- Void Guardian -> Long-horned Yak: waits: kills it for its death effect
Rough count: 3 lines in the sample; every Void Guardian kill line overall.

## Cause 11. Removal aimed at one creature is read as killing my own Last Words card
Wrong thinking: any "destroy/deal damage to a creature" is a way to set off my own Last Words.
Rule broken: L11 and L9 (a plain hit on one target feeds no death trigger; it is enemy removal).
Lines from cards built to kill my own unit stay: Feed the Forest, Death's Desire, Lord of the Wastes, Demon Wrangler, Oath to Oblivion, Doom Scythe, Doomgate, Death Walker, Shaytan Assassin's sacrifice, Failed Experiment.
- Flame Burst -> Imperial Guard: waits: kills it for its death effect
- Firebomb -> Seifer's Fodder: waits: kills it for its death effect
- Last Nightmare -> Soulbound Sagami: waits: kills it for its death effect
- Soul Drain -> Aryana, Soul of Gagana: waits: kills it for its death effect
- The Emperor's Command -> Imperial Guard: waits: kills it for its death effect
Rough count: about 15 of the 50 sampled lines.

## Cause 12. A Last Words that helps the opponent is linked as a need
Wrong thinking: any Last Words is a death effect worth setting off.
Rule broken: L5 (drawbacks are no needs).
- Feed the Forest -> Ruunin's Shrine: waits: kills it for its death effect (Last Words: your opponent gains 2 faeria)
- Demon Wrangler -> Hunted Outlaw: waits: kills it for its death effect (Last Words: your opponent draws and gains 2 faeria)
Rough count: 2 in the sample.

## Cause 13. A stat boost on the board is linked to a Gift fight that already happened
Wrong thinking: more power helps a card whose Gift fights, but the Gift went off when the card was played.
Rule broken: L18 (power counts only in a fight its text starts; a boost given later cannot reach it). A boost to a card in hand (Court Jester) would be right.
- Spirit Spice -> Barrensky Vermin: stronger: can give it more power and health
- Savior of the Meek -> Barrensky Vermin: stronger: can give it more power and health
- Soulbound Sagami -> Barrensky Vermin: stronger: can give it more power and health
- Fortune Hunter -> Deepwood Stalker: stronger: can give it more power and health
- Chrysalis -> Deepwood Stalker: stronger: can give it more power and health
Rough count: 5 in the sample. Also Tethra, Soul of the Wild -> Ulani, Defender of Oversky: Ulani's text reads no stat and has no Taunt.

## Unsure
- Land creators to every card of that colour (1784 lines; for example Wild Growth -> Deepwood Grizzly) follow L22 and the colours match. The count is very large; is this what Kaptain wants?
- "Can be summoned adjacent to friendly creatures" (Swarming Carassius, Khalim's Skyguard, Spear of the Guardians) and Bomb Slinger, Axe Grinder, Blazing Salamander, Daring Adventurer: does a mover help them, or is it generic because every creature moves (L1)?
- Movers to Bloodstone Sprite, Azure Wisp and Wavecrash Colossus ("a friendly creature / you harvest from an enemy well"): the mover harvests itself. Is that L20 (no line) or a real feed?
- Secret of Strength -> Oradrim Sagittarius: a Ranged Attack unit cannot attack after moving, so giving it Charge may not help.
- Triton Banquet -> Dwordia, Chief of the Bright Fox Tribe: Dwordia can move into a forest on its own, so giving Jump may add nothing.
- Chrysalis or Crystalis -> Taunt units: a swallowed unit is off the board while it grows.
- Drakkar Skycaptain -> Shadowsilk Faerie: stronger: gives it more power and health when it comes. This is help to any Flying creature (L14?).

## Must-stay correct lines (tests)
- Clockwork Yak -> Topaz Yak: type: is a yak it asks for
- Triton Stargazer -> Tide Lord: type: is a triton it asks for
- Syland Horsemaster -> Lost Explorer: waits: moves it for its effect
- Celestial Tower -> Oradrim Monk: moves: moves it within reach of the enemy player
- Oath to Oblivion -> Eredon, Voice of All: waits: kills it for its death effect

# Faeria check, part f1 (a-f and h)

Read: lines 1-461 and 3525-4035; not read: none (all lines of my part were read; some card texts behind "(text above)" were not looked up).

## Causes

1. A card's own move keyword (Flying, Jump, Dash, Charge, Aquatic) or a land maker is read as "moves my units forward". Breaks L20 and L2: Flying moves only the card that has it, and moving forward is what every creature does. Land makers (Path to Paradise, Earthcraft, Wood Elemental) move nothing.
   - Ghost Dragon -> Lost Explorer: moves: moves my units or land forward: they reach enemy ground
   - Wood Elemental -> Wavecrash Colossus: moves: moves my units or land forward: they reach enemy ground
   - Sturdy Shell -> Mother of All Yaks: moves: moves my units or land forward: it can enter where it needs to be
   - Glidehopper -> Mystic Beast: moves: moves my units or land forward: it can enter where it needs to be
   - Airbot -> Wind Wisp: moves: moves it within reach of the enemy player
   About 6000 lines (the top 3 reasons in part a: 2712 + 2280 + 1422). Only real moves of another card stay ("moves it where it must be": Flash Wind, Oradrim Fanatic, Desert Twister, Celestial Tower).

2. "Enters where it needs to be" is given to cards whose need is only where they are summoned, or is only about themselves. Breaks L2 and L1: Axe Grinder, Mystic Beast, Topaz Yak, Tide Lord, Triton Tactician, Daring Adventurer, Blazing Salamander, Bomb Slinger, Rakoakopter and Emerald Salamander are placed when summoned. Prophet of Tides and Coral Polliwog move their own land. Mother of All Yaks and Voice of Hunger act next to themselves.
   - Barrensky Vulture -> Triton Tactician: moves: moves my units or land forward: it can enter where it needs to be
   - Cloud Machine -> Bomb Slinger: moves: moves my units or land forward: it can enter where it needs to be
   - Twinsoul Spirit -> Coral Polliwog: moves: moves my units or land forward: it can enter where it needs to be
   This is part of the 2280 lines in cause 1.

3. Generic movement next to an "adjacent friendly" aura or Gift is read as a position line. Breaks L14 and L18: Kobold Barracks and Rakoan Chieftain give generic power. Tiki Adventurer, Voice of Hunger and Sharra's Inspiration help any card of a kind. Coral Polliwog moves only its own land, so it cannot move Daring Adventurer, and Daring Adventurer's Gift only works when it is summoned.
   - Demonic Salmon -> Tiki Adventurer: type: Demonic Salmon moves your units, and Tiki Adventurer acts on units next to it
   - Flamesilk Faerie -> Kobold Barracks: type: Flamesilk Faerie moves your units, and Kobold Barracks acts on units next to it
   - Spear of the Guardians -> Kobold Barracks: type: Spear of the Guardians moves your units, and Kobold Barracks acts on units next to it
   - Coral Polliwog -> Daring Adventurer: type: Coral Polliwog moves Daring Adventurer, and Daring Adventurer acts on units next to it
   - Swarming Carassius -> Sharra's Inspiration: type: Swarming Carassius moves your units, and Sharra's Inspiration acts on units next to its target
   About 800 lines (667 + the "next to its target" lines).

4. A need about the enemy god is fed by any creature that reaches or attacks the god. Breaks L2 and L1, and some lines point the wrong way:
   - Defender of the Homeland wants to be attacked (wrong way round).
   - Exalted Ogre and War Yak read the opponent's Life (damage, not reach).
   - Volcanic Colossus counts turns with damage to the opponent, which every attack does.
   - Oradrim Sagittarius, Wind Wisp, Zealous Crusader, Shaytan Scavenger and Khalim's Prayer count any friendly attack on a god.

   Examples:
   - Seed of Paradise -> Defender of the Homeland: moves: moves it within reach of the enemy player
   - Airbot -> Volcanic Colossus: moves: moves it within reach of the enemy player
   - Volcanic Colossus -> Defender of the Homeland: type: makes units hit the enemy player (by fighting)
   - Volcanic Colossus -> Oradrim Sagittarius: waits: makes your units hit the enemy player (by fighting)

   About 1400 lines.

5. A kill line is made from text that kills nothing, or ignores the need's own condition. Breaks L1, L11 and L9:
   - Solem destroys a faeria well, not a creature.
   - Blood Obelisk needs a death "in combat", but Gift damage (Garudan, Sorocco) and destroy effects (Astral Weapon) are not combat.
   - Earthfire Shaker counts only the kills of its own Gift.
   - Hunted Outlaw's Last Words helps the opponent (L5, a drawback).

   Examples:
   - Solem -> Annoying Gnat: waits: kills it for its death effect (Solem lists 32 such lines)
   - Garudan, Heart of the Mountain -> Blood Obelisk: waits: makes enemy units die
   - Astral Weapon -> Earthfire Shaker: type: kills enemy units
   - Doom Scythe -> Hunted Outlaw: waits: kills it for its death effect

   About 32 Solem lines, plus about 10 Earthfire Shaker lines, about 10 Blood Obelisk lines and about 30 Hunted Outlaw lines.

6. A stat change is linked to a card it cannot reach, or goes the wrong way. Breaks L8 and L21 (read wants right):
   - Doomgate and Faeria Tree are structures, so creature buffs (Campfire, Ancient Beastmaster, Aurora's Gift, Banon, Eredon) cannot hit them.
   - Tower of Curses' -1/-1 lowers Life, which Doomgate (13+) and Faeria Tree (5+) need to rise.
   - Aurora's 6/6 stops Seedling.

   Examples:
   - Tower of Curses -> Doomgate, Door to Oblivion: type: changes its stats for its effect
   - Tower of Curses -> Faeria Tree: type: changes its stats for its effect
   - Aurora, Myth Maker -> Faeria Tree: type: changes its stats for its effect
   - Campfire -> Doomgate, Door to Oblivion: type: changes its stats for its effect

   About 60 lines (49 into Doomgate, plus the lines into Faeria Tree and Seedling).

7. Generic power is linked where the card's text does not read its power. Breaks L18:
   - Enslaved Priest and Malevolent Spirit drain a fixed 2.
   - Kaios drains a fixed 1.
   - Boulder Thrower only hits.
   - Seedling reads Life only.
   - Animated Banquet's buff comes after Deepwood Stalker's Gift has already fought.

   Examples:
   - Path to Paradise -> Enslaved Priest: stronger: more power: its text uses the damage it deals when it comes
   - Kobold Warlord -> Seedling: stronger: can give it more power
   - Animated Banquet -> Deepwood Stalker: stronger: more power: its text uses the damage it deals
   - Banon, Captain of the Radiance -> Boulder Thrower: stronger: more power

   About 40 lines.

8. Help or a tutor aimed at a kind (Flying, Jump, Combat, legend, yak, 5+ Life) links to every card of that kind. Breaks L14, L15 and L1b: the receiving card's text does not use the help, and a draw by kind is no line.

   Examples:
   - Golden Aviary -> Solem: stronger: gives it more power
   - Drakkar Skycaptain -> Seed of Paradise: stronger: gives it more power and health when it comes
   - Iona's Smile -> Astral Weapon: puts: draws it from the deck
   - Time of Legends -> Ulani, Oversky Shaman: puts: draws it from the deck
   - Yak Shepherd -> Prairie Yak: stronger: can give it more power

   The same cause covers Herald of War -> CAP-10 and Krog, Triton Trainer -> Fugoro and Sorocco, and Magda -> 27 legends ("makes it cheaper").

   About 150 lines in my part.

9. "Creates cards" or "fills your hand" is linked where the receiving text does not count made cards, or the cards go to the enemy. Breaks L1, L9 and L19:
   - Gemshell Tortoise only copies a card it draws.
   - Rapala fills the opponent's hand.

   Examples:
   - Amai Mapdealer -> Gemshell Tortoise: type: creates cards
   - Intrepid Explorer -> Gemshell Tortoise: type: creates cards
   - Rapala, the Dopefish -> Ruby Fish: puts: creates
   - Rapala, the Dopefish -> Dream Keeper: waits: fills your hand

   About 15 lines.

10. A made or summoned unit is not checked against the stat or cost filter of the need. Breaks L20 (a card made by name must be the kind the need asks):
    - Mother of All Yaks' Yak Guards are 4/4. They are not "higher Attack than Life" (Hate Seed, Firebringer) and do not have "5 Life or more" (Ancient Beastmaster).

    Examples:
    - Mother of All Yaks -> Hate Seed: cheaper: puts your units into play
    - Mother of All Yaks -> Ancient Beastmaster: waits: puts your units into play

    About 5 lines.

11. Text that does not exist is read as self-death or as a keyword giver. Breaks L1:
    - Baeru and Rapala never die by their own effect.
    - Seed of Paradise gives no keywords.

    Examples:
    - Baeru, the First Wave -> Bone Collector: waits: dies by its own effect
    - Rapala, the Dopefish -> Spirit Spice: cheaper: dies by its own effect
    - Seed of Paradise -> Herald of War: type: makes your units get Combat
    - Seed of Paradise -> Imperial Engineer: type: makes your units get Production
    - Mother of All Yaks -> Seek Shelter: type: makes your units get Taunt

    About 20 lines.

12. A card that hits Flying creatures is linked from my Flying cards. Breaks L9: Destructive Volley is aimed at enemies.

    Examples:
    - Astral Weapon -> Destructive Volley: type: has Flying
    - Seed of Paradise -> Destructive Volley: type: makes units get Flying

    About 60 lines (one or two from every Flying card).

13. A neutral card gets "turns a land into the colour it needs". Breaks L22: a neutral card needs no land colour.

    Examples:
    - Fire Elemental -> Path to Paradise: type: turns a land into the colour it needs: helps pay its land cost
    - Ring of Dominion -> Path to Paradise: type: turns a land into the colour it needs: helps pay its land cost, and can take that land from the enemy

    About 10 lines.

14. What every turn does is read as a trigger. Breaks L1.

    Examples:
    - Doomsday -> Compass of Gagana: waits: makes this happen: your turn ends (Doomsday also destroys the Compass)
    - Kaios, Demented Overmind -> Blightblade Knight: waits: damages it for its effect (Blightblade's text is a drawback, L5)

    About 2 lines.

15. Missed lines: these cards' own texts clearly work together, but they have no line.
    - Ancient Gargoyle destroys the Treasure Maps in your deck and gains +1/+1 per map.
    - Amai Mapdealer, Aryana, Compass of Gagana and Gagana, Treasure Seeker all put Treasure Maps into the deck.
    - Each of them should have a line to Ancient Gargoyle: "puts Treasure Maps in your deck: it counts them".

## Unsure
- Ancient Beastmaster and Ancient Herald -> vanilla 5+ Life creatures (Simulacrum of Obedience, Steamforge Enforcer, Syland Warrior): this is generic if half the creatures have 5+ Life (L21).
- Earthcraft -> Drakkar Skycaptain, Flamesilk Faerie, Gabrian Commander: a random draw may or may not be the kind they wait for.
- Kaios "<- more health" (13 lines): Kaios' Attack equals his Life, so this may count as "a stat his text reads".
- Gabrian Enchantress -> Flamestoker, and Gabrian Enchantment -> Seifer: a one-off "Attack = Life" probably does not use their growth.
- "Clears its line of fire" to Ranged Attack cards (Rain of Fish -> Hilltop Archer): it depends on whether Faeria ranged attacks are blocked by units in between.
- Doomgate -> Ancient Beastmaster, Firebringer, Illusion of Grandeur: Ostregoth's stats are unknown.
- Day of the Dragons -> Fugoro, Merchant of Wonders ("makes the Crystal Dragon it names"): Fugoro draws the dragon from the deck, not from the hand.
- Shozen and Spirit Spice -> The World's Tear: the Tear needs "attacked a god", which any creature does.
- Amai Mapdealer -> Fugoro, Captain of the Gagana (missing?): this depends on the Treasure Map's text.
- CAP-10 -> Gift of Steel has two reasons for one effect ("creates" and "draws it from the deck"). L10 says to say one reason once.

## Correct lines that must stay (tests)
- Fragmenter -> Hate Seed: cheaper: puts your units into play (the 4/2 Mecha has higher Attack than Life).
- Farm Boy -> Illusion of Grandeur: waits: is a unit whose summoning sets off its effect (cost 1).
- Architect -> Doomgate, Door to Oblivion: stronger: can give it more health (a structure gets +0/+2).
- Death Walker -> Spirit Spice: cheaper: makes your units die
- Prairie Yak -> Mother of All Yaks: waits: is a yak it counts when dies

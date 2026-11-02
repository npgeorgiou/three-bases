# Faeria deck check, part f3 (d_faeria.txt) — causes found

Read: lines 1-1650; not read: lines 1651-2095

The coordinator stopped the check, so lines 1651-2095 were not read. No card texts were looked up with txt.py, so every cost or colour that a line depends on is unknown and listed under "unsure".

## Cause 1. A unit's own movement keyword, or a land change, is read as moving another card forward (L20, L1)
Wrong thinking: a card with Flying, Jump, Dash or Charge, or a card that changes or destroys lands, "moves my units or land forward" for any partner that wants enemy ground. But a fight or movement keyword only works for the card that has it. Turning lands into lake (Baeru) or destroying lands (Meteor) moves nothing.
- Airbot -> Imperial Trooper: moves into place: moves my units or land forward: they reach enemy ground
- Rakoan War Machine -> Imperial Trooper: moves into place: moves my units or land forward: they reach enemy ground
- Triton Warrior -> Wavecrash Colossus: moves into place: moves my units or land forward: they reach enemy ground
- Baeru, the First Wave -> Wavecrash Colossus: ...; also moves into place: moves my units or land forward: they reach enemy ground
- Meteor -> Baldurion, Evil Archsmith: moves into place: moves my units or land forward: they reach enemy ground
- Ancient Boar -> Voice of Hunger: enables: Ancient Boar moves your units, and Voice of Hunger acts on units next to it; ... (Boar's Dash moves only the Boar; Feral Kodama's Jump is the same case)
Rough count: about 19 lines (Imperial Trooper 4, Wavecrash Colossus 7 not counting Sunken Tower, Baldurion 3, Garudan -> Axe Grinder/Bomb Slinger 2, Ancient Boar/Feral Kodama -> Voice of Hunger 2). Sunken Tower -> Wavecrash Colossus moves a land and can stay.

## Cause 2. Moving a unit that is already in play is linked to a Gift that only goes off when the unit is summoned (wrong reason)
Wrong thinking: "it can enter where it needs to be". But Bomb Slinger, Axe Grinder and Voice of Hunger read their position only once, when they are summoned. Giving them Charge later (Syland Horsemaster) or flying next to them (Garudan) does nothing for that Gift.
- Syland Horsemaster -> Bomb Slinger: moves into place: moves my units or land forward: it can enter where it needs to be
- Syland Horsemaster -> Axe Grinder: moves into place: moves my units or land forward: it can enter where it needs to be
- Syland Horsemaster -> Voice of Hunger: ...; also moves into place: moves my units or land forward: it can enter where it needs to be
Rough count: about 8 lines. This includes the "also moves into place" half of the four lines into Voice of Hunger. The "moves your units next to it" half from Horsemaster and Sagami Grovecaller may stay.

## Cause 3. Stat help given to any card of a kind links to cards whose text never uses the stats (L14, L18)
Wrong thinking: "gives it more power and health when it comes" is drawn to every card that fits the filter: 5+ Life (Ancient Beastmaster), Flying drawn (Drakkar Skycaptain), next Jump creature (Triton Trainer), next Combat creature (Herald of War). These cards are not Taunt, do not wait to survive damage, and do not read their stats.
- Ancient Beastmaster -> Thyrian Golem: makes stronger: gives it more power and health when it comes (blank card)
- Ancient Beastmaster -> Feral Kodama: makes stronger: gives it more power and health when it comes
- Drakkar Skycaptain -> Khalim, Sky Prodigy: makes stronger: gives it more power and health when it comes
- Triton Trainer -> Ninja Toad: makes stronger: gives it more power and health when it comes
- Herald of War -> Underground Boss: makes stronger: gives it more power and health when it comes
- Khalim's Training -> Shaytan Monstrosity: makes stronger: more power (Monstrosity reads the Attack of the friend that dies, not its own)
Rough count: about 14 lines (Beastmaster -> Golem, Kodama, Oakling, Ancient Boar; Drakkar -> Khalim, Windborne Champion, Demon Wing, Manta Rider, Iona; Trainer -> 2; Herald -> 2; Khalim's Training -> Monstrosity). Lines to Taunt cards (Grove Guardian, Living Willow) and to Deepwood Stalker stay.

## Cause 4. The helper is said to "need" the cards it helps: wrong direction (L6, L14)
Wrong thinking: Triton Trainer gives the next Jump creature +1/+1, so Jump cards "enable" it. Trainer is the helper. Jump cards do not feed any need on Trainer.
- Ninja Toad -> Triton Trainer: enables: has Jump
- Triton Warrior -> Triton Trainer: enables: has Jump
- Battle Toads -> Triton Trainer: enables: makes your units get Jump; also triggers: puts units into play (for the ability it gives)
Rough count: 3 lines.

## Cause 5. The reason words do not match the giver's text (wrong reason)
Wrong thinking: a label is given that the card's text does not do.
- Iona's Smile -> Sunsilk Faerie: ...; also triggers: makes you draw cards. Iona's Smile draws Flying creatures, never an event, so it cannot set off "the first time you draw an event". The "draws it from the deck" half is right.
- Mirror Phantasm -> Windstorm Archer: clears the way: clears its line of fire. Mirror Phantasm turns a creature into a 5/5. That makes a blocker bigger and clears nothing.
Rough count: 2 lines.

## Cause 6. Real lines are missing where a card's text names what the other card makes or needs
- Amai Mapdealer -> Triton Stargazer and Message in a Bottle -> Triton Stargazer. Both shuffle Treasure Maps into the deck. Stargazer: "If any of them are a Treasure Map, this gains +2/+2". Both are in Bamsers' doomgaydisciple, and Mapdealer and Stargazer have no partner there.
- Gift of Steel -> Grim Guard. Gift of Steel's own text gives a Combat creature +3/+3, and Grim Guard is a Taunt Combat creature, so this is health to a Taunt unit (L18). Campfire -> Grim Guard exists, but this line is missing in Red Archers and in Red Blue Mobility Burn.
- Gagana, Rainbow Birdship -> Illusion of Grandeur. Gagana adds a crew member that costs 0, and Illusion of Grandeur waits for "a creature that costs 1 faeria or less". Gagana has no partner in How Greedy. Magnus ("It costs 0 faeria") and Aurora's Dream ("cost of all cards to 0") -> Illusion of Grandeur should also say "triggers", not only "pays for it".
Rough count: about 6 missing lines.

## Unsure
- Removal spells -> Ranged Attack cards ("clears its line of fire": Flame Burst, Seifer's Wrath, Choking Sand, Soul Drain -> Hilltop Archer, Windstorm Archer, Flame Thrower). I am not sure Faeria's Ranged Attack is blocked by creatures in between. If it is not, all of these lines (about 9) are wrong.
- Single-target damage to my own Last Words card: Soul Drain -> Deathwish Ghoul, Falcon Dive -> Plague Bearer, Hammer of Destruction -> Baron Thulgar, The Emperor's Command -> Eredon. These may fall under L11 (a plain hit on one target).
- Plain draw cards -> Sunsilk Faerie and Flight of the Mantas (Shifting Tide, Wisdom, Haunted Husk, Storyteller): a random draw may or may not be an event, and every turn draws anyway (L1, L1b).
- Land colour lines (L22): Baeru -> Humbling Vision, Mirror Phantasm, Battle Toads; Wild Growth -> Seek Shelter, Ruunin's Guidance; Seed of Paradise -> Demon Wing. Card colours were not checked. A line is wrong where the card does not need that colour, or where Demon Wing is only a summoned token with no land cost.
- Lines from base cost 7+ (Gabrian Commander, Gabrian Archon) from Gabrian Warden, Mirror Phantasm, Baeru and Wavecrash Colossus: base costs were not checked.
- Krog, Bold Bargainer, Ogre Dance, Red Devil "can make it cheaper" / "pays for it" to Bold Bargainer, Red Devil, Ogre Battler, Barbarian Ogre: these are right only if those cards count as expensive (L13). Costs were not checked.
- Manta Rider -> Mistral Guide (triggers: puts your units into play): the Manta appears where the Rider died, not always next to the Guide.
- Syland Horsemaster / Triton Banquet -> Combat creatures ("moves it where it must be"): this depends on what Faeria's Combat trigger needs.

## Correct lines that must stay (tests)
- Rakoan Cannoneer -> Rakoan Shield Mates: triggers: kills it for its death effect
- Krog's Dinner -> Krog, the Ogre King: puts it into play: draws it from the deck; also brings it back to your hand; also makes cheaper: makes it cheaper
- Ancient Beastmaster -> Deepwood Stalker: makes stronger: more power: its text uses the damage it deals
- Failed Experiment -> Village Elder: triggers: kills it for its death effect
- Khalim, Sky Prodigy -> Windborne Emissary: enables: has Flying; also is a unit with Flying it counts or asks for

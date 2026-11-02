# Runeterra part h (champions) - causes found

Read: lines 6562-7011; not read: lines 7012-7810 (stopped by coordinator; Janna is partly read, and everything from Jarvan IV to Zoe is not checked).

## Causes

1. **"if you have one" / "if you don't already have one" is read as "your hand is empty".** No card text asks for an empty hand. This is a misread of the card text (L1, L21 "read wants right").
   - Get Excited! -> Aphelios: empties your hand
   - Spinning Axe -> Gnar: empties your hand
   - Rummage -> Aphelios: empties your hand
   - Count: 88 (44 lines for Aphelios and 44 for Gnar).

2. **"Creates a card" links to every card with "created" in its text, without checking what is created or who is created.** Cunning Kitten and Hextech Anomaly wait for themselves to be created. Portal Scholar, Sneezy Biggledust! and Norra want created allies. Sump Fumes wants cards added to hand. Buster Shot and Yordles in Arms count regions, Elder Dragon counts Dragon Boons and The World Ender counts Darkin. Trundle (level 2) wants 8+ cost cards. Caitlyn creates nothing at all (she plants). This breaks L1 and L20 (a made card must be the kind the need asks for).
   - Ashe -> Cunning Kitten: creates cards
   - Caitlyn -> Sump Fumes: creates cards
   - Draven -> Buster Shot: creates cards: more different cards to play
   - Irelia -> Trundle (level 2): fills your hand
   - Ashe -> Norra: creates cards (levels it up)
   - Count: about 15 lines per champion that creates anything, about 150 in the part I read.

3. **"Makes more cards to play" links to cards that count any card played.** Any card can be played (L1). This also covers cards that react to playing any follower or ally (L19, L1b).
   - Annie -> The Swindler's Den: makes more cards to play
   - Gnar -> Vi: makes more cards to play
   - Annie -> Beguiling Cobra: makes more cards to play
   - Annie -> Breakneck Husk: makes more cards to play
   - Count: about 60.

4. **"Is played" links to Aphelios's "play 2 other cards".** That count is filled by any card (L1).
   - Prank -> Aphelios: is played
   - Volibear -> Aphelios: is played
   - Count: 20.

5. **Flashbomb Trap is read as hitting my side.** I plant it in the enemy deck, so it damages the enemy's ally. The lines still feed "your units die", "damages your units" and Braum's "survive damage" (L9, L7).
   - Caitlyn -> Kalista: through Flashbomb Trap: makes your units die (levels it up)
   - Caitlyn -> Vladimir: through Flashbomb Trap: damages your units without killing them (levels it up)
   - Caitlyn -> Braum: through Flashbomb Trap: damages it without killing it, for its effect (levels it up)
   - Count: about 17.

6. **Cards that give a random keyword are read as giving "Trap", which then levels Caitlyn.** Caitlyn counts her activated traps, and no random keyword is a trap.
   - Acceleration Gate -> Caitlyn: makes units get Trap (levels it up)
   - Fabled Poro -> Caitlyn: makes units get Trap (levels it up)
   - Hothead -> Caitlyn: makes units get Trap (levels it up)
   - Count: 64.

7. **Gwen is read as giving or using any stat change.** Her text only uses Power gained from Hallowed, and she gives other units nothing. This breaks L15 and L14.
   - Bayou Brunch -> Gwen: changes your units' stats (563 lines)
   - Gwen -> Breakneck Husk: more power
   - Gwen -> Nasus: more power: its text uses the damage it deals
   - Gwen -> Vi: changes its stats for its effect
   - Count: about 650.

8. **A generic stat boost to a champion is added as a "stronger" line next to its real level-up line.** The champion's text does not read its own stats, or the boost is health on a unit without Taunt or "survive" (L18).
   - Galio -> Aurelion Sol: gives it more health
   - Tybaulk -> Bard: gives it more power
   - Arachnoid Host -> Elise: gives it more power
   - Jagged Taskmaster -> Annie: gives it more power
   - Paparo the Great -> Gnar: gives it more power
   - Count: about 900. Each of Aurelion Sol, Bard and Gwen has about 200; Annie, Elise, Gnar and Aphelios have a few each.

9. **What a made card does is credited to its maker (L3).** Aurelion Sol's own text gives no health or stats. These lines come from the Celestial cards he creates.
   - Aurelion Sol -> Braum: more health or protection: survives damage (levels it up)
   - Aurelion Sol -> Bone Scryer: more health or protection: survives damage
   - Aurelion Sol -> Gwen: changes your units' stats
   - Count: about 15.

10. **"Mecha Yordle" is read as "Yordle".** Gnar is not a Mecha.
    - Gnar -> Skrappy's Partsapalooza: is a Mecha whose summoning sets off its effect
    - Gnar -> Rumble (level 2): is a Yordle it asks for
    - Rumble (level 2) -> Gnar: makes it cheaper
    - Count: 5.

11. **A copy put into the deck is linked.** This is generic per L19.
    - Nautilus -> Ashe: copies it
    - Nautilus -> Braum: copies it
    - Count: 7 in the part I read.

12. **A faction or cost filter is treated as narrower than a deck (L14, L17).**
    - Kinkou Wayfinder -> Annie: puts it into play from the deck. This is by kind ("a 1 cost ally"), and Annie has no summon effect.
    - Annie -> Trifarian Hopeful: is a unit it asks for. This only asks for "another Noxus ally".
    - Draven -> Trifarian Hopeful: is a unit it asks for
    - Reaver's Row -> Annie: gives it Fearsome
    - Count: about 8.

13. **The same reason is said twice under two names (L10).**
    - Headmistress Telsi -> Annie: "repeats its Attack effects" and also "repeats its effects". The same pair appears for Ashe, Bard, Elise, Gwen and Hecarim.
    - Braum has two lists of 313 cards: "levels: more health or protection" and "waits: more health or protection", with the same cards in both.
    - Irelia has "makes units attack (levels it up)" (67) and "another attack (levels it up)" (61), mostly the same cards.
    - Aurelion Sol has "changes your units' stats (levels it up)" (530) and "more power (levels it up)" (101).
    - Count: about 1100.

14. **The link direction is wrong, and the same pair is said several times.** Akshan names Warlord's Palace; Warlord's Palace does not name Akshan.
    - Warlord's Palace -> Akshan: is the A it names
    - Warlord's Palace -> Akshan: is a landmark it counts
    - Warlord's Palace -> Akshan: is a landmark or structure it asks for
    - Spinning Axe -> Draven: is the A it names
    - Count: 4.

15. **Akshan only advances Warlord's Palace, but the check links him to every Countdown landmark (L1).**
    - Akshan -> Dragon Roost: finishes countdowns
    - Akshan -> Buried Armory: finishes countdowns
    - Count: 7.

16. **Wrong reason words for summoning a landmark (L10, L8).** Akshan summons a landmark, not units.
    - Akshan -> Chip: puts units into play
    - Akshan -> Shaped Stone: puts your units into play
    - Akshan -> Taliyah: puts your units into play (levels it up)
    - The other wording errors in this part are "B sets thems stats" and "is an Ascended it counts when levels_up". Both are code text, not what a player would say.
    - Count: about 12.

17. **Buried Sun Disc is linked as levelling or waking champions.** It only counts Ascended level-ups, and Akshan and Annie are not helped by it.
    - Buried Sun Disc -> Akshan: makes champions level up (it levels up from what it then does)
    - Buried Sun Disc -> Annie: makes champions level up
    - Count: 3.

18. **Annie's damage to enemies is linked to death effects that only my own units have (L9).**
    - Annie -> Blades of the Fallen: makes units die (for the ability it gives)
    - Annie -> Empire Reconstructor: makes units die
    - Annie -> Chronoshift: makes units die
    - Annie -> The Darkin Bloodletters: makes units die
    - Count: about 6.

19. **Twisted Catalyzer is linked to Annie and Gwen.** It boosts only "your Darkness", and neither of them is Darkness.
    - Annie -> Twisted Catalyzer: damages units or players (for the ability it gives)
    - Gwen -> Twisted Catalyzer: damages units or players (for the ability it gives)
    - Count: 2.

20. **The Dreadway's "double all damage" is linked to champions whose text does not read damage (L18).**
    - The Dreadway -> Bard: doubles its damage
    - The Dreadway -> Aurelion Sol: doubles its damage
    - The Dreadway -> Annie: doubles its damage
    - Gwen keeps her link, because her level-up counts the damage she deals.
    - Count: 3.

21. **Strike spells are said to set off an Attack effect.** A strike is not an attack.
    - Bone Skewer -> Gwen: makes it attack or strike again: its own effect goes off
    - Count: 24.

22. **Twilit Protector's Nightfall buff to Nightfall allies is linked to Aphelios.** Nightfall on Nightfall gives no line (L15), and Aphelios does not read his Power.
    - Twilit Protector -> Aphelios: gives it more power
    - Count: 1.

23. **Level-up lines are filed under "type" instead of "levels".** In both cases the count is the champion's level-up condition.
    - Gifts From Beyond -> Aphelios: makes a Moon Weapon it asks for. Aphelios levels from 4+ Moon Weapons played.
    - Spiderling -> Elise: is a Spider it asks for. Elise levels from 3+ other Spiders.
    - Count: about 16.

24. **Ashe's "changes enemy units' stats" list includes Husks.** Husks grant their stats to my own ally, not to an enemy.
    - Breakneck Husk -> Ashe: changes enemy units' stats (levels it up)
    - Ashe -> Gwen (level 2): changes units' stats (for the ability it gives)
    - Count: about 12.

## Unsure
- Destined Poro, Devoted Council and the others ("makes champions level up") are linked from every champion. This may be generic because every champion has a level-up, or it may be a fair minority kind.
- A cost match exactly ("play a 2 cost card": Insightful Investigator; Tri-beam Improbulator) is linked to champions of that cost. It may be generic under L21.
- Elise -> Plunder cards (helps it hit the enemy player). Fearsome is not in L2's list of keywords that reach the Nexus.
- Janna <- 173 draw cards (makes you draw cards). L5 names Janna's "first 3 times you draw" as a limit, and any card can be drawn.
- Bard -> Kindred (through Chime: helps my units kill). This may only be a generic stat link.
- Bard -> Living Library / Origami Slicer (plants traps). It depends on whether Chime counts as a trap or boon.
- Braum -> Ezreal (targets enemy cards). Challenger may not count as targeting.
- Azir -> Taloned Strike (is a Bird). I could not check whether Azir is a Bird.
- Azir -> Miss Fortune (makes your units attack). "When allies attack" goes off once per attack, not once per attacker.
- Gnar <- Rumble (level 2) and Yordle Explorer, "gives it more power". This may be generic, or a Mecha mismatch as in cause 10.
- King Jarvan III -> Gwen (can give it Scout). Scout may count as a second attack.

## Correct, must stay
- Vekauran Vagabond -> Akshan: finishes countdowns (levels it up)
- Annie -> Tibbers: creates
- Braum -> Baccai Witherclaw: makes this happen: challenges
- Gnar -> Janna: changes card costs (levels it up)
- Caitlyn -> Proximity Puffcap: plants traps that go off later

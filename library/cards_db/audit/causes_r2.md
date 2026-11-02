# Runeterra, part b second half (lines 846-1653): causes

Answer to the question: yes. Most lines here come from three generic reasons: any unit hitting the Nexus feeds Plunder, a "gives my keywords" card matched to every keyword, and group help (Yordle, 1 cost, Fearsome, more damage) sent to cards whose own text does not use it.

## Cause 1. A unit's own fight keyword (Elusive, Overwhelm, Fearsome, Impact, Scout) is read as "damages the enemy player" for every Plunder or Nexus-damage card
Wrong thinking: a unit that can reach the Nexus by its keyword feeds another card's "if you damaged the enemy Nexus". Breaks L20 (the keyword works for the card that has it) and L2 (attacking is the game's rule). Also wrong timing: Plunder is checked when the card is played, so moving or helping the Plunder card itself after play does nothing.
- Abyssal Eye -> Dashing Dandy: damages the enemy player (Abyssal Eye: only Elusive, Deep, Nexus Strike draw)
- Aatrox (level 2) -> Samira (level 2): damages the enemy player (only Overwhelm)
- Dashing Dandy -> Plunder Poro: helps it hit the enemy player (Dandy's own Overwhelm)
- Marai Songstress -> Barbed Chain: makes it cheaper: damages the enemy player (Songstress only grants itself Elusive)
- Bone Skewer -> Dashing Dandy: moves it within reach of the enemy player
Same cause: the "-> damages the enemy player / helps it hit the enemy player" groups to the 31-37 Plunder cards, Fix-Em-Uppers, Loaded Dice, Rumble (level 2), Sejuani (level 2), Swain (level 2) and Gnar's level-up, from Dashing Dandy, Atakhan, Fizz, Samira (level 2), Papercraft Dragon (created), Marai Songstress, Abyssal Guard, Xolaani, Ambush and Rainbowfish (created). The "damages the enemy player (by fighting)" group of 35 Scout units goes too. Kept: cards whose own text deals Nexus damage (Annie, Atrocity, Stylish Shot, Flair).
Rough count in my part: about 3,000 lines (522+372+35+7 into Dandy, 520+370+35+7 into Samira (level 2), plus about 80 out of each of about 10 cards).

## Cause 2. "Grant it my stats and keywords" (Attach) is matched to every keyword
Wrong thinking: Papercraft Dragon and Rainbowfish give "keywords", so they are linked to every card that waits for, counts or levels from any keyword or status. But they give only their own (Double Attack, or Elusive). Breaks L14/L16 (the help must be the thing B uses).
- Papercraft Dragon (created) -> Teemo: makes units get Plant (levels it up)
- Papercraft Dragon (created) -> Falling Star: makes enemy units get Stun
- Rainbowfish (created) -> Caitlyn: makes units get Trap (levels it up)
- Rainbowfish (created) -> Sinner's Vise: makes enemy units get Curse
- Papercraft Dragon (created) -> General of the Dunes: makes units get Daybreak
Rough count: about 90 lines from each of the 2 cards, about 180.

## Cause 3. Help aimed at a group is sent to a card whose text does not use it
Wrong thinking: "grant Yordles / 1 cost allies / Fearsome allies +1|+0" links to every member. Breaks L14 and L15 (Vilemaw's Fearsome buff is the keyword's rule).
- Paparo the Great -> Heimerdinger: gives it more power (Heimerdinger counts Tech allies summoned, not its own power)
- Yordle Explorer -> Fizz: gives it more power when it comes
- Jagged Taskmaster -> Fizz: gives it more power
- Reaver's Row -> Fizz: gives it Fearsome
- Vilemaw -> Abyssal Guard: gives it more power
Rough count: about 12 lines (including Heimerdinger (level 2), Domination, Siren Song, Professor von Yipp and Grandfather Fae to Fizz and the Attach cards).

## Cause 4. "More damage" is linked to anything that deals damage
Wrong thinking: "your spells deal 1 extra damage" or "double all damage" makes a damage spell or an attacker stronger. Breaks L18 (more damage is generic; gives_lines says more damage alone is never a use).
- Funsmith -> High Note: its damage gets 1 more
- Tybaulk -> Fatal Encore: its damage gets 1 more
- The Dreadway -> Fizz: doubles its damage
- The Dreadway -> Marai Songstress: doubles its damage
Rough count: about 20 lines (4 each into High Note, Ambush and Fatal Encore; The Dreadway into 8 cards). Blowback -> Morgana (Lifesteal) may stay.

## Cause 5. Health help is sent to a card that reads only Power
Wrong thinking: Xolaani counts "allies that died with power increased", so all stat help links to it. Health alone does nothing for it, and its own stats are not read (Overwhelm, L18). Breaks L15 ("+1|+0 raises no Health", and the reverse) and L18.
- Tiny Shield -> Xolaani the Bloodweaver: can give it more health
- Galio -> Xolaani the Bloodweaver: gives it more health
- Bayou Brunch -> Xolaani the Bloodweaver: turns the Health it grows into Health
- Glacial Fell -> Xolaani the Bloodweaver: turns the Power it grows into Health
Rough count: about 30 lines. The "more power / can give it more power and health" groups aimed at Xolaani itself (about 250) are also doubtful, because it reads allies that die, not its own power.

## Cause 6. A summon of the wrong kind is linked to a level-up that counts one kind
Wrong thinking: any "puts your units into play" feeds "summon 12+ Power of Tech allies" (Heimerdinger) or "summoned 5+ multi-region allies" (Tristana). Breaks L20 (a card made must be the kind the need asks) and L1b.
- Island Navigator -> Heimerdinger: puts your units into play (levels it up) (random 1 cost follower, not Tech)
- Mysterious Portal -> Heimerdinger: puts your units into play (levels it up), and the "through Mysterious Portal" group
- Mischievous Marai -> Tristana: puts your units into play (levels it up) (Powder Keg is single region)
- Claws of the Dragon -> Tristana: puts your units into play (levels it up) (Ionia only)
Rough count: about 55 lines.

## Cause 7. Reasons that do not match B's text at all
- Catalogue of Regrets -> Vayne / Veigar / Senna / Aphelios: empties your hand (Catalogue adds a card to hand; these "create X if you don't have one"). There are 23 such lines.
- Catalogue of Regrets -> Ancient Warmonger / Fallen Rider: makes you discard cards (the Fleeting copy is a spell, not the unit). There are 14+4+1 such lines.
- Arena Bookie / Get Excited! / Rummage -> Samira (level 2): empties your hand (Samira's text has no hand need). There are 45 such lines.
- Lee Sin -> Legion General: has Barrier; Fizz -> Legion General: has Elusive; Morgana -> Legion General: makes units get a keyword or status (Legion General counts only units Stunned or Recalled). There are about 15 such lines.
- Lee Sin -> Threaded Volley: makes enemy units block: B damages them (Threaded Volley hits Taliyah's blocker, L7). There are 8 such lines.
- Ambush -> Abyssal Eye / Attentive Accountant / Zoe / Teemo: makes your units hit the enemy player (they already have Elusive; Ambush adds nothing they need). There are about 6 such lines.
Rough count: about 115 lines.

## Cause 8. "When you play 6 cards" counted from every card
Samira (level 2) <- is played (15): Riptide Rex, Volibear, The Darkin Fan... Samira counts any card played. That is L1 (After Image example). There are about 15 lines, plus Samira's "is played" level groups.

## Unsure
- Papercraft Dragon / Rainbowfish <- makes cards leave play (333 each): "Recall me" is a rider, and most of these remove enemies (L9, L5). These are probably wrong.
- Papercraft Dragon / Rainbowfish -> equips your units, and Innovative Blacksmith: Attach may not count as Equip.
- Stance Swap and Prank -> spell counters: is played. Stance Swap plays nothing; Prank is unclear.
- Rumble (level 2) -> Heimerdinger: makes it cheaper / gives it more power and health. This depends on whether Heimerdinger is a Mecha Yordle.
- Flashbomb Peddler -> Kalista/Thresh: "through Flashbomb Trap: makes your units die". The trap is in the enemy deck, so the side may be wrong.
- Samira (level 2) -> Ardent Tracker / Island Navigator (Scout): another attack. This may be Scout's own rule (L15).
- Morgana -> Sinner's Vise: makes enemy units get Curse. Sinner's Vise does not need a Curse there.
- High Note -> own Last Breath units: kills it for its death effect. A 2-damage hit on my own unit is a weak "sacrifice".

## Must-stay examples (checked against both texts)
- Mischievous Marai -> Kennen: puts your units into play (levels it up) (the same Powder Keg is summoned again and again)
- Morgana -> Soul Shackles: makes enemy units get Curse
- Lee Sin -> Sacred Protector: has Barrier (allies with Barrier have Double Attack)
- Chronobreak -> Marai Songstress: brings it back: its summon effect goes off
- Catalogue of Regrets -> Lillia: is a landmark it needs summoned for its count (levels it up)

Read: lines 846-1653; not read: none

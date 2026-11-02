# runeterra, part r1 (a_runeterra.txt lines 1-845): causes

Answer to part b: yes. Most of the biggest cards' partners come from fighting, from a fight keyword on any unit, or from help to any ally.

## 1. "by fighting": every unit that can fight is a source
Wrong thinking: any unit can block or attack, so it "makes units die / strike / damage the Nexus". Breaks L1, L2.
- Ye Been Warned <- Affectionate Poro: makes enemy units die (by fighting)  (Poro text: only Challenger)
- Viego (level 2) <- Aatrox: makes units die (by fighting)
- Kalista (level 2) -> For Glory!: cheaper: makes units strike (by fighting)
- Snowy Razorclaw <- Ardent Tracker: damages the enemy player (by fighting)  (Tracker text: Scout, cost drop on Elite)
- Gangplank <- Valor: levels: damages the enemy player (by fighting) (levels it up)
Rough count in my part: about 2,400 (Ye Been Warned 1077, Viego (level 2) 1076, plus 36-group lines on Razorclaw, Tuskraider, Gangplank, Sejuani, Darius, Eternal Dancers, Kalista).

## 2. A fight keyword on one card is read as Nexus damage for another card
Wrong thinking: a unit with Elusive, Overwhelm, Fearsome or Quick Attack (or Nexus Strike) "damages the enemy player" for every Plunder card and for every champion that levels from Nexus damage. Breaks L20 (Nasus's Fearsome gets Nasus to the Nexus, not Abyssal Eye) and L2. Only a card whose own text deals Nexus damage (Chemtech Drake, Ezreal (level 2)'s spell ping, Swain's Nexus Strike damage) or that gives the keyword to the card that needs it should link.
- Alpha Wildclaw -> Snowy Razorclaw: damages the enemy player  (Wildclaw: only Overwhelm)
- Amateur Aeronaut -> Gangplank: levels: helps it hit the enemy player (levels it up)  (only Elusive)
- Viego (level 2) -> Jagged Butcher: helps it hit the enemy player  (only Fearsome)
- Fleet Admiral Shelly -> Plunder Poro: damages the enemy player  (only Elusive)
- Wiggly Burblefish -> Swain (level 2): waits: damages the enemy player  (Swain needs NON-combat Nexus damage; wrong also by words)
Rough count: about 5,500 (Razorclaw and Tuskraider about 900 each; Gangplank, Sejuani, Darius about 900 each; the 35-40 Plunder groups on Viego, Kalista, Ezreal, Shelly, Burblefish, Eternal Dancers, Fizz; the Fix-Em-Uppers/Loaded Dice/Rumble/Swain groups).

## 3. Help aimed at any ally linked to every ally
Wrong thinking: "when you summon another ally, grant it +1|+1" helps every unit. Breaks L14 (this exact example is named there).
- Yordle Captain -> Aatrox: gives it more power and health when it comes
- Yordle Captain -> Affectionate Poro: gives it more power and health when it comes
- Yordle Captain -> Alpha Wildclaw: gives it more power and health when it comes
Rough count: 1,221.

## 4. "All your spells deal 1 extra damage" linked to every spell
Wrong thinking: a spell damage boost makes every spell's effect bigger, also spells that deal no damage. Breaks L18 (gives_lines: more damage alone is never a use) and L4.
- Powder Keg -> Advanced Intel: makes its effect bigger
- Powder Keg -> Ancestral Boon: makes its effect bigger
- Powder Keg -> Answered Prayer: makes its effect bigger
Rough count: 880.

## 5. Draw by kind linked to every card
Wrong thinking: Realm Warp draws 3 and keeps non-followers, so it "draws and keeps" every non-follower. Breaks L1b.
- Realm Warp -> Aatrox: draws it and keeps it
- Realm Warp -> Absorb Soul: draws it and keeps it
Rough count: 969.

## 6. "If you don't have one" read as "wants an empty hand"
Wrong thinking: a card that creates X in hand "if you don't have one" waits for an empty hand. Breaks L5 (a limit is no need) and L21 (read wants right). Also Realm Warp fills the hand, it does not empty it.
- Realm Warp -> Aatrox: waits: empties your hand
- Realm Warp -> Vayne: waits: empties your hand
- Avatar of the Tides -> Senna: waits: empties your hand
Rough count: about 50 (24 per giver, 2 givers in my part, plus level lines to Jinx).

## 7. Stat help to a card whose text does not read its stats
Wrong thinking: The Tuskraider has Plunder, so more power/health helps it. Its text (draw Sejuani, double allies in deck) reads no stat of its own. Breaks L18. (Snowy Razorclaw does read its stats: "grow an ally's stats to mine", so its lines stay.)
- Adept Weaponsmith -> The Tuskraider: more power
- Astral Protection -> The Tuskraider: more health
Rough count: about 480.

## 8. Giver cannot give the help to that card
Wrong thinking: any card that touches stats "gives it more power". Breaks L4 and L8 (who it can target).
- Here to Help -> Gangplank: more power: its text uses the damage it deals  (gives +0|+3 only)
- Counter Strike -> Darius: more power: its text uses the damage it deals  (only Jax)
- Faithful Wolfdog -> Sejuani: more power: its text uses the damage it deals  (Forges itself)
- Domination -> Fizz (level 2): gives it more power when it comes  (only 1 cost allies; Fizz level 2 is never summoned as 1 cost)
Rough count: not counted; seen in the 80- and 18-groups of Gangplank, Sejuani, Darius (likely tens per champion).

## 9. Kalista (level 2) read wrongly
Wrong thinking: her bond ("it takes damage for me") is read as a need for damage, as protection for others, and as damage to others; her revive of a follower is linked to champions; a revived attacker is read as "another attack". Breaks L7, L4 ("another attack" is only Rally or a free attack), L20 (a made card must be the kind the need asks).
- Kalista (level 2) <- Absorb Soul: damages units or players (for the ability it gives)
- Kalista (level 2) -> Ahri (level 2): makes it attack for its effect  (Kalista revives only followers)
- Kalista (level 2) -> Braum: damages it without killing it, for its effect
- Kalista (level 2) -> Braum: more health or protection: survives damage
- Kalista (level 2) -> Quinn: another attack  (same on Eternal Dancers -> Quinn)
Rough count: about 600 (431 + champions inside the 93 + 35 + 24 + 18), plus about 70 on Eternal Dancers for "another attack".

## 10. Moving an ally into the deck read as moving it toward the Nexus
Wrong thinking: any "move" helps reach the enemy player. Bone Skewer moves the ally to the top of the deck; Sugary Snare puts it on the bottom. Breaks L4.
- Bone Skewer -> Darius: levels: moves it within reach of the enemy player (levels it up)
- Sugary Snare -> Snowy Razorclaw: moves it within reach of the enemy player
Rough count: about 2 per target, about 15 in my part.

## Unsure
- Chemtech Drake <- "fills your hand" (496): every card that creates or draws; maybe too generic under L21.
- Mirror Mage <- "is a spell whose playing sets off its effect" (733): it needs CREATED spells only; plain spells may not trigger it.
- Mirror Mage -> Breakneck Husk etc. "makes more cards to play": its copy is summoned, not played, so "when you play an ally" may not trigger (L19).
- Powder Keg -> Barkbeast etc. "dies by its own effect": not sure "Destroy me" counts as an ally dying.
- Starlit Seer / Gemcrafter / Shelly / Nami -> Adnere's Aviarists, Bayou Brunch: "more power": Aviarists grows to another's stats; Bayou Brunch is a spell.
- Avatar of the Tides -> 114 spells "pays for it": refills only spell mana (max 3); maybe generic.
- "waits: is played" from Prank and Stance Swap: not sure these play another card.

## Must-stay (correct)
- Chemtech Drake -> Jagged Butcher: damages the enemy player
- Fae Guide -> Fizz (level 2): can give it Elusive
- For Demacia! -> Darius: can give it more power and health
- The Tuskraider -> Sejuani: draws it from the deck
- Ye Been Warned -> Fizz: is a spell whose playing sets off its effect

Read: lines 1-845; not read: none (stopped before checking more card texts; 10 causes)

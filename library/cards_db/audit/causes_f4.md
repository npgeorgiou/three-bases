# Faeria deck check, part 4: causes

Read: lines 2096-2875; not read: lines 2876-4269

Decks fully read: BRGY Structures, RY Flyers, YBR Angry Old Turtle, YAK ATTACK!, Wishes 25, Victory Celebration Red, Twinsoul Control, Turbo Illusion. Swarm - Heal read up to line 2875 (its section e list is cut off there). Every deck after it was not checked.

## 1. A card that waits for a kind of card to be drawn gets no line from the cards of that kind
Wrong thinking: "the first time you draw an event" or "whenever you draw a Flying creature" is fed only by cards that make you draw, never by the events or flyers in the deck. L1b keeps the line when the kind is a minority (events are about 97 of about 460 Faeria cards). Case nfa09 says the same: "drawing a Flying creature needs a card that has Flying". The only line of this kind that exists is for a 7+ cost card (Illusion of Grandeur -> Gabrian Commander).
Missing, for example:
- Flame Burst -> Flamesilk Faerie, Seifer's Wrath -> Flamesilk Faerie, Soul Drain -> Flamesilk Faerie (RY Flyers)
- Soul Drain / Last Nightmare / Spirit Theft / Flight of the Mantas / Message in a Bottle -> Sunsilk Faerie (Twinsoul Control)
- Airbot / Demon Wing / Thunder Eel / Rakoakopter -> Drakkar Skycaptain: is a Flying creature it needs drawn (RY Flyers)
Rough count in my part: about 13 missing lines.

## 2. Drakkar Skycaptain's buff on a drawn flyer is linked as stat help to cards that never read their stats
Wrong thinking: +1/+1 to any Flying creature drawn is linked to every flyer. This is help aimed at any card of a kind (L14), and more power or health is generic (L18). None of these cards' texts read their stats. The real line goes the other way, from the flyer to the Skycaptain (cause 1).
- Drakkar Skycaptain -> Airbot: makes stronger: gives it more power and health when it comes
- Drakkar Skycaptain -> Flamesilk Faerie: makes stronger: gives it more power and health when it comes
- Drakkar Skycaptain -> Thunder Eel: makes stronger: gives it more power and health when it comes
- Drakkar Skycaptain -> Rakoakopter: moves into place: ...; also makes stronger: gives it more power and health when it comes
Count: 5 lines in RY Flyers, counting the "also" part on Rakoakopter and Imperial Drakerider.

## 3. Yak Shepherd's +2/+0 is linked to every yak
Wrong thinking: power given to "2 friendly yaks" counts as a use for every yak. A tribe is no narrower than a deck (L14), and more power is generic (L18). No yak's text reads its power.
- Yak Shepherd -> Roaming Yak: makes stronger: can give it more power
- Yak Shepherd -> Oversky Yak: makes stronger: can give it more power
- Yak Shepherd -> Emerald Yak: makes stronger: can give it more power
- Yak Shepherd -> Mother of All Yaks: makes stronger: can give it more power
Count: 6 lines, also as the "also" part on Topaz Yak and Sapphire Yak. Yak Shepherd's Charge 2 lines (moves it where it must be) stay.

## 4. A lowering effect is linked as if it helped a card that wants its stats high
Wrong thinking: any change to stats "enables" a card that reads its stats. The direction is not checked (L21: read wants right). Faeria Tree wants 5 or more Life. The Command deals 3 damage to a structure, which kills the 1 Life Tree. Humbling Vision halves a creature, and the Tree is a structure.
- The Emperor's Command -> Faeria Tree: enables: changes its stats for its effect
- Humbling Vision -> Faeria Tree: enables: changes its stats for its effect
Count: 2 lines.

## 5. A line from an ability the card does not have
Wrong thinking: Grappling Hook only gives Ranged Attack and a move after the attack, but it is linked as giving Production.
- Grappling Hook -> Imperial Engineer: enables: makes your units get Production
Count: 1 line. The cause in the code is unknown and needs to be found.

## 6. "Higher Attack than Life" is counted as a deck choice
Wrong thinking: summoning a creature with higher Attack than Life is linked as a count. L21 names exactly this filter as generic, because about half the creatures pass it. Wind Soldier, Deathwish Ghoul and Oradrim Fanatic pass it too, and they rightly get no line.
- Demon Wrangler -> Firebringer: triggers: puts your units into play
- Demon Wrangler -> Hate Seed: makes cheaper: puts your units into play
Count: 2 lines.

## 7. A cost that drops for each yak that died is said as "triggers"
Wrong thinking: Mother of All Yaks "costs 1 faeria less for each friendly yak that has died". L10 says X "makes it cheaper" for such a cost, never "triggers" or "enables".
- Topaz Yak -> Mother of All Yaks: triggers: is a yak it counts when dies
- Sapphire Yak -> Mother of All Yaks: triggers: is a yak it counts when dies
- Emerald Yak -> Mother of All Yaks: triggers: is a yak it counts when dies
Count: 5 lines.

## 8. The same reason is said two or three times in one line
Wrong thinking: separate rules say the same thing about movement, and one_link joins them all. L10 says one reason is said once, by its strongest kind.
- Celestial Tower -> Imperial Drakerider: triggers: moves it for its effect; also moves into place: moves my units or land forward: they reach enemy ground; also moves into place: moves it where it must be
- Roaming Yak -> Topaz Yak: enables: is a yak it asks for; also Roaming Yak moves your units, and Topaz Yak acts on units next to it; also moves into place: moves my units or land forward: it can enter where it needs to be
- Oversky Yak -> Topaz Yak: (same three reasons)
- Bloated Toad -> Illusion of Grandeur: triggers: puts your units into play; also is a unit whose summoning sets off its effect
Count: about 6 lines.

## 9. Cards that make a card by description get no line to a card that counts or waits for that card
Wrong thinking: the lines miss what a card makes when it makes it by description (L17).
- Missing: Crystal Spice -> Gabrian Archon. Crystal Spice discovers 2 cards that cost 7 or more, and the Archon counts cards with base cost 7+ played.
- Missing: Amai Mapdealer -> Triton Stargazer, Message in a Bottle -> Triton Stargazer, Gagana, Treasure Seeker -> Triton Stargazer. Each one adds Treasure Maps to the deck, and the Stargazer gains +2/+2 if it draws one.
- Missing: Yak Attack -> Topaz Yak (is a yak it asks for). Yak Attack summons three Angry Yaks. Mother of All Yaks -> Topaz Yak gets this same reason for its Yak Guards, so the miss is only for Yak Attack.
Count: about 5 missing lines.

## 10. A need to stand on enemy land is not seen
Wrong thinking: only "moves onto" and "harvests" enemy ground count as a need for the units to be deep in enemy ground. Triton Adventurer's "at the end of your turn, draw a card if this is on an enemy land" is not seen.
- Missing: Oradrim Fanatic -> Triton Adventurer (Gift: move a friendly creature). Wind Soldier and Glidehopper are probably missing as well, by the same rule as nfa21 and nfa27.
Count: 1 to 3 missing lines (YBR Angry Old Turtle).

## Unsure
- "makes you draw cards" to cards that wait for one kind of card to be drawn (Lore Thief -> Ancient Herald, Message in a Bottle -> Flight of the Mantas, Shifting Tide -> Gabrian Commander): any draw might draw it, so this may be generic under L1b.
- Spirit Spice -> Topaz Yak and Triton Banquet -> Topaz Yak ("moves your units"): they give a keyword to any creature, and Topaz only cares about yaks next to it.
- Last Nightmare -> Istanu, Eternal Light: kills it for its death effect. It is unclear whether destroying your own Istanu is a real play.
- Flight of the Mantas -> Windborne Emissary: "makes your units get Flying". The card summons a flyer and gives Flying to no unit, so the wording may be wrong.
- Victory Celebration has no partner. +1 faeria a turn might pay for Radiance, Hellfire and Stormspawn under L22, but it is small.

## Correct lines that must stay (test cases)
- Imperial Engineer -> Faeria Tree: repeats its effects: repeats its effects
- Architect -> Faeria Tree: makes stronger: can give it more health
- Faeria Tree -> Garudan, Heart of the Mountain: makes cheaper: pays for it: more mana or a lower cost
- Illusion of Grandeur -> Gabrian Commander: triggers: is a card whose drawing sets off its effect
- Fire Elemental -> Hellfire: enables: turns a land into the colour it needs: helps pay its land cost

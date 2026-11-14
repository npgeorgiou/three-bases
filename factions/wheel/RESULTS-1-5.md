# Results of the wheel, steps 1-5.1 (second try, 14 Nov 2026)
How each was made and how to redo it: `factions/wheel/PIPELINE.md`.

## Step 1. The radii
24 radii, measured on 43 real factions: `factions/wheel-axes.html`, `library/cards_db/axes.tsv`. Names used below:
strong = strength, grows = grows strength, strikes = strikes more or first, textdmg = damage from units' text, kills = kills outright, many = many at once, spelldmg = damage from spells, spellpay = rewards playing spells, stops = stops them, disrupts = breaks their plan in other ways, one = one chosen, supply = more supply, cheaper = cheaper or stronger hand, cards = more cards, picks = picks and copies, back = brings back, wide = many cheap units, spends = spends them, together = position and combos, heals = heals them, growsdef = grows defence, protects = protects them, tough = defence, tall = a few big units

## Step 2. The radii that work together
44 strong pairs read by agents (12 real card pairs each):
- KEEP (5): grows+heals, kills+spends, many+spends, spellpay+supply, supply+spends
- WEAK (27): grows+strikes, grows+back, grows+growsdef, strikes+textdmg, strikes+back, strikes+spends, textdmg+back, kills+supply, kills+back, many+supply, spelldmg+cheaper, spellpay+cheaper, spellpay+cards, supply+cheaper, supply+back, cheaper+cards, cheaper+back, cheaper+tall, cards+back, picks+back, back+wide, back+spends, back+growsdef, wide+spends, spends+protects, spends+tall, heals+growsdef
- DROP (12): strikes+growsdef, strikes+tall, textdmg+many, textdmg+cheaper, many+back, spelldmg+supply, spellpay+picks, cheaper+picks, back+heals, back+protects, back+tall, spends+heals
Each with the reason: `work/radius_verdicts.tsv`. Numbers for every pair: `library/cards_db/wheel/radius_links.tsv`.

## Step 3. The 20 shapes (letters only; no names or themes yet)
| faction | strong radii (value: 1 = an average real faction) |
|---|---|
| A | many cheap units 1.4, spends them 1.9, brings back 1.6 |
| B | spends them 1.7, more supply 1.5, a few big units 1.4 |
| C | many at once 1.8, spends them 1.4, kills outright 1.2 |
| D | rewards playing spells 2.0, more cards 1.5, more supply 1.3 |
| E | damage from spells 1.9, cheaper or stronger hand 1.4, rewards playing spells 1.3 |
| F | heals them 1.8, grows strength 1.3, grows defence 1.5, defence 1.3 |
| G | strikes more or first 1.8, grows strength 1.5, strength 1.4 |
| H | brings back 1.7, damage from units' text 1.5, more cards 1.2 |
| I | more supply 1.6, cheaper or stronger hand 1.4, a few big units 1.8 |
| J | picks and copies 1.9, brings back 1.4, more cards 1.2 |
| K | kills outright 1.6, brings back 1.4, cheaper or stronger hand 1.2 |
| L | stops them 2.2, more supply 1.2, a few big units 1.3, defence 1.2 |
| M | breaks their plan in other ways 1.9, cheaper or stronger hand 1.3, more cards 1.4 |
| N | protects them 1.8, spends them 1.2, defence 1.5 |
| O | many cheap units 1.9, position and combos 1.5, spends them 1.2 |
| P | a few big units 1.7, spends them 1.4, strikes more or first 1.3, strength 1.4 |
| Q | damage from units' text 1.8, strikes more or first 1.3, one chosen 1.5 |
| R | brings back 1.5, grows strength 1.6, grows defence 1.4 |
| S | many at once 1.6, more supply 1.4, kills outright 1.4 |
| T | one chosen 1.6, kills outright 1.5, spends them 1.3 |

## Step 4. The order on the circle
A T I L M E D J H Q G F R N P C S B K O (side by side = their radii work together the most).
Kaptain, 15 Nov 2026: not a strict rule.

## Step 5.1. The 48 mechanics
Full sentences, concepts and sources: `factions/wheel/mechanics.tsv`. SMALL = under 30 right cards in every real faction.
| key | I do X -> I gain from X | size |
|---|---|---|
| deathfeed | my units die -> my other units or cards grow from each death | OK |
| lastwords | I die -> my Death effect acts (a unit worth more dead than alive) | OK |
| sacrifice | I let my own unit die -> an enemy unit dies or is hit (a trade of units, never a gain of supply or strength: that is the Offering) | SMALL |
| selfhurt | I damage my own units -> they act when hit, or something else gains | SMALL |
| revive | my dead units come back from the discard pile -> their Place acts again | OK |
| recycle | my spent cards go from the discard pile back to deck or hand -> I play them again | SMALL |
| returnhand | I take my unit back to hand -> I place it again and its Place acts again | SMALL |
| tokens | my Place or Death effect puts extra small units on the grid -> they fill cells and front cells cheaply (never round-end seeding: Rootkin) | OK |
| countboard | I fill my camp with units -> cards that count my units grow | OK |
| allyplay | I place allies -> my units already on the grid react to each placement | OK |
| adjacency | my units stand beside, behind or around each other -> they give each other more | OK |
| movement | I move my own units inside my camp -> they reach the cells they need (front cells, beside an ally) | OK |
| push | I move enemy units -> they leave the cells facing my dots, or stand where my cards hit them | OK |
| lanes | my cards act in another lane -> one lane's strength or supply helps another | SMALL |
| cells | I claim cells -> my units on claimed cells gain, enemies there lose (NEW RULE) | OK |
| onattack | my unit attacks -> its attack has an effect besides the hit | OK |
| strikes | my unit strikes twice or first -> every paid attack does more, it survives the trade | OK |
| overkill | my unit hits for more than the enemy's defence -> the rest hits the unit behind | OK |
| onkill | my unit kills an enemy -> it gains or acts again | OK |
| fight | I make my unit strike a chosen enemy, or make enemies strike -> removal by my unit's strength | OK |
| ping | my units' text and spells deal small fixed damage, often or many times (never round end: Barrage) -> wounded and small enemies are finished | OK |
| area | my cards hit every enemy in a row, column or area -> many enemies are hit by one card | OK |
| kill | I destroy an enemy outright, no damage -> its defence does not matter | OK |
| spelldmg | my spells deal damage -> removal from the hand, no unit needed | OK |
| spellpay | I cast spells -> my units and later spells gain from each spell | OK |
| hurt | my unit is hit and survives -> it acts | SMALL |
| silence | I take an enemy's text away -> its keywords and abilities stop for good | SMALL |
| weaken | I take an enemy's strength away for good -> it stays in its cell but hits for little | OK |
| change | I turn an enemy into another unit or take it -> its card is gone without dying | SMALL |
| hand | I act on the enemy's hand and costs -> his next cards cost more or are gone | SMALL |
| junk | I put useless cards or units on the enemy's side -> his cells and hand fill with nothing | SMALL |
| supply | I gain extra supply or carry-over -> big units come early | OK |
| cheaper | my cards get cheaper or free -> two cards in one turn's supply | OK |
| inhand | my cards grow in hand -> a bigger card for the same supply | SMALL |
| draw | I draw extra cards -> more choices each round | OK |
| create | I create cards that were not in my deck -> more cards and answers | OK |
| copy | I copy my own cards -> a strong card twice | OK |
| pick | I pick cards of my deck -> the card I need comes when I need it | OK |
| discard | I discard my own cards -> the discarded card acts, or my units grow | OK |
| heal | I restore my units' defence -> wounded units hold the front cells longer | OK |
| shield | I give shields or armour -> the next hit does less or nothing | OK |
| guard | my unit guards my others -> enemy attacks must go where I choose | OK |
| hide | my unit can't be targeted or hit -> enemy attacks and spells can't reach it | OK |
| attach | I attach a unit or item to another unit -> the carrier gets its stats and text (NEW RULE) | OK |
| roundstart | at round start my cards act -> a plan set up last round pays at once | OK |
| leave | my unit leaves the grid (dies, returns, moves) -> my other cards react | SMALL |
| bigstrength | my units have strength 5 or more -> cards that need big strength fire | SMALL |
| offering | I let my own unit die -> I gain supply, carry-over, a card or strength (the library's usual sacrifice) | OK |

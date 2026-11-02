# Causes, runeterra decks p2_3 (Lurkers, Draven Sion, Poppy Lux, Jarvan Lulu Poppy Midrange)

Note: the c) and b) blocks do not print every line of a card (Rek'Sai 12 partners, Sion 10, Jarvan 16 show fewer), so "missing" is only claimed where a card is printed with no partner at all, or where its twin card has the line.

## Causes (wrong lines)

1. Power/health help is linked to a card whose own text does not read power or health (L18, L14).
   Radiant Guardian only gets Lifesteal/Tough if a unit died; Snapjaw Swarm only attacks. "Does a card hit / attack" is no reason for a boost.
   - Poppy -> Radiant Guardian: makes stronger: gives it more power and health   (decks 3 and 4)
   - Poppy (level 2) -> Radiant Guardian: makes stronger: gives it more power and health
   - Twin Disciplines -> Radiant Guardian: makes stronger: can give it more power   (also Sharpsight -> Radiant Guardian)
   - Rek'Sai -> Snapjaw Swarm: makes stronger: gives it more power   (also Rek'Sai (level 2) -> Snapjaw Swarm)
   Right counterparts: Rek'Sai/Snapjaw -> Xerxa'Reth, because Xerxa'Reth reads "power ge 8".

2. A card is given an effect on another card that its rows never show: Snapjaw Swarm only does "start_attack self".
   - Snapjaw Swarm -> Xerxa'Reth, The Undertitan: enables: changes its stats for its effect; also makes stronger: more power
   Swarm changes no stats and gives nothing to Xerxa'Reth, whose power only comes from Rek'Sai's buff (L3/L6).

3. "More damage" from a unit's own power or Overwhelm is generic (L18); Ravenous Flock deals a fixed 4 and reads no power.
   - Sion -> Ravenous Flock: enables: more damage
   - Sion (level 2) -> Ravenous Flock: enables: more damage
   Flock's real need is a damaged or stunned target; Sion does neither.

4. Lux (level 2) goes off only when ONE spell costs 6 or more (IF amount event_amount ge 6), but every spell is given a "triggers" line, including spells that cannot cost 6.
   - Conchologist -> Lux (level 2): triggers: makes a spell whose playing sets off its effect   (Manifests a spell with [cost le 3], so it can never set it off)
   - Trinket Trade -> Lux (level 2): triggers: is a spell whose playing sets off its effect; also makes a spell whose playing sets off its effect   (same cost le 3 filter in the second half)
   - Pokey Stick -> Lux (level 2): triggers: is a spell whose playing sets off its effect
   - Concerted Strike -> Lux (level 2): triggers: is a spell whose playing sets off its effect
   Rows do not print costs; Sharpsight and Final Spark need the same cost check. Kept: Minimorph -> Lux (level 2) (cost 6), and all "helps it level up" lines to Lux (total mana of spells, L17).

## Causes (missing lines)

5. Any damage on a unit makes it "damaged", which is what Ravenous Flock asks for (state in damaged), but only stun was linked. Mystic Shot is printed with NO partner at all in its deck.
   - Missing: Mystic Shot -> Ravenous Flock (enables: makes a unit damaged)
   - Missing: Thermogenic Beam -> Ravenous Flock, Get Excited! -> Ravenous Flock (same reason)
   Existing twin that shows the pattern: Arachnoid Sentry -> Ravenous Flock: enables: makes enemy units get Stun

6. Rally (a free attack) is linked to Draven (level 1) as "helps it level up" but not to Draven (level 2), whose text also waits for his strikes ("WHEN strikes by self DO create Spinning Axe x2").
   - Printed: Sion Returned -> Draven: helps it level up: helps my units strike more (levels it up)
   - Missing: Sion Returned -> Draven (level 2): triggers: another attack   (Draven (level 2) has only 2 partners, Sion Returned only 2)
   Same logic is printed for Jarvan: Cataclysm -> Jarvan IV (level 2): triggers: another attack

## Unsure

- Arachnoid Sentry -> Paralyzing Bite: puts it into play: casts its skill. Rows show Sentry only stuns; they do not cast or create the Bite skill. Looks like two cards with the same effect, not a line. If Bite is Sentry's own skill by the card data, the rows hide it.
- Snapjaw Swarm -> Frenzied Feast: enables: is a Lurker it asks for. Right if Lurker is a minority type of all units (L21; same idea as the Elite lines, kept). Wrong if Lurker counts as the deck's own type (L2, L14). Kaptain should decide once for the Lurker deck.
- Possible missing: Jaull-fish -> Pyke and Frenzied Feast -> Pyke (Pyke is a Lurker; the strike makes him deal damage, and his level-up counts damage dealt by Pyke, ge 15; L18 keeps lines where the text reads the damage). Not printed under Pyke, 5 partners.
- Possible missing: Golden Aegis (Rally) and Cataclysm (free attack) -> Poppy ("event_count attacks by self ge 3": level up from attacks, L4 allows only Rally/free attack) and -> Poppy (level 2) / Cithria the Bold ("WHEN attacks by self"). The printed Jarvan IV lines ("triggers: another attack") do the same for Jarvan; Poppy's printed lines show only Radiant Guardian and Jarvan IV.
- Poppy -> Poppy (level 2) "levels into" is not printed in either deck, while Lux, Lulu, Sion, Draven, Jarvan print theirs. May be a print gap.
- Lux lines for Prank, Poison Dart and For Demacia! (spells that add mana to Lux's count of 6) are not printed; Lux shows 12 partners, only 9 are printed.

## Clearly right (checked against the rows)

- Waking Sands -> Sandstone Charger: puts it into play: summons
- Arachnoid Sentry -> Ravenous Flock: enables: makes enemy units get Stun
- Cataclysm -> Jarvan IV: triggers: another attack (Cataclysm: start_attack; Jarvan: WHEN attacks by mine player)
- Minimorph -> Lux: helps it level up: costs 6: pays it alone (levels it up)
- Penitent Squire -> Tattered Banner: puts it into play: creates

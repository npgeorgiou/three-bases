# Duelyst deck check: causes (part u3)

Read: lines 1-1200; not read: lines 1201-2617

## Causes

1. Stats given to a tribe are linked to every card of that tribe, even when its text never uses stats. Breaks L14, L18 (health only to Provoke/Taunt or "survive damage").
   - Oakenheart -> Helm of MECHAZ0R: makes stronger: gives it more power and health
   - Oakenheart -> Replicant: makes stronger: gives it more power and health
   - Owlbeast Sage -> Manaforger: makes stronger: gives it more health
   - Owlbeast Sage -> Araras Prophet: makes stronger: gives it more health
   - About 13 lines (7 Oakenheart, 6 Owlbeast Sage), plus the "also makes stronger" part on Oakenheart -> Metaltooth and Oakenheart -> MECHAZ0R!.

2. Healing your General is linked to the General card (or to a minion) whose text never uses healing. Breaks L14, L16.
   - Trinity Oath -> Argeon Highmayne: heals: can heal it
   - Ragebinder -> Vaath the Immortal: heals: can heal it
   - Void Pulse -> Lilithe Blightchaser: heals: can heal it
   - Azure Herald -> Ciphyron Ascendant: heals: can heal it
   - Healing Mystic -> Inquisitor Kron: heals: can heal it
   - About 14 lines (also Desolator, Spectral Blade, Brilliant Plume -> Kara Winterblade, Aymara Healer, Rescue-RX, Healing Mystic -> Aymara Healer, Lifestream -> Silverguard Knight).

3. Artifacts and spells that give the General Attack, a keyword or damage protection are linked to the General card, whose only text is "Bloodbound Spell: X". More damage and fight keywords are generic. Breaks L18, L14, L20.
   - Overload -> Vaath the Immortal: makes stronger: can give it more power
   - Dawn's Eye -> Argeon Highmayne: makes stronger: can give it more power
   - Cyclone Mask -> Shidai Stormblossom: gives keyword: can give it Ranged
   - Concealing Shroud -> Faie Bloodwing: makes stronger: can negate damage it
   - About 11 lines (also White Asp -> Faie, Crescent Spear -> Shidai, Mask of Shadows -> Shidai, Bangle -> Shidai, Arclyte Regalia -> Argeon, Phantasm -> Desolator).

4. "Spells deal +1 damage" is linked to every damage spell. More damage is generic. Breaks L18 (gives_lines: more damage alone is never a use).
   - Crescent Spear -> Ghost Lightning: makes stronger: makes its effect bigger
   - Crescent Spear -> Phoenix Fire: makes stronger: makes its effect bigger
   - Crescent Spear -> Spiral Technique: makes stronger: makes its effect bigger
   - 6 lines.

5. A plain hit on one target, or ordinary attack damage, is read as a kill or a death trigger. Breaks L11, L2.
   - Daemonic Lure -> Grasp of Agony: triggers: makes units die (for the ability it gives)
   - White Widow -> Abyssal Scar (Bloodbound Spell): triggers: makes units die (for the ability it gives)
   - Flash Reincarnation -> Unseven: triggers: kills it for its death effect (2 damage, Unseven has 4 Health; Dagona 8, Grimes 3)
   - Dispirited Prisoner -> Punish: enables: damages enemy units or players: Punish kills them (Frenzy only; any attack damages)
   - About 8 lines (also Daemonic Lure -> Abyssal Scar, Flash Reincarnation -> Dagona, Flash Reincarnation -> Grimes, Dispirited Prisoner -> Abyssal Scar).

6. A kill with a condition is linked without checking the condition. Breaks "read like a player".
   - Plasma Storm -> Dagona: triggers: kills it for its death effect (Plasma Storm destroys 3 or less Attack; Dagona has 8)
   - 1 line here; check the same filter in every game.

7. Wrong side: a kill of my own minion linked to a card that waits for an enemy minion to die. Breaks L9.
   - Darkfire Sacrifice -> Grasp of Agony: triggers: makes units die (for the ability it gives)
   - 1 line.

8. A summon not from the action bar is linked to Hideatsu, whose Trial counts minions summoned from the action bar. Breaks the card's own wording.
   - Inquisitor Kron -> Hideatsu the Ebon Ox: triggers: puts your units into play
   - Dagona -> Hideatsu the Ebon Ox: triggers: puts your units into play
   - 2 lines.

9. Movement lines from a card that only moves itself (any unit moves) or does not move anything. Breaks L1.
   - Azurite Lion -> Roar: enables: Azurite Lion moves your units, and Roar acts on units around your leader or base (Azurite Lion has only Celerity)
   - Azurite Lion -> Holy Immolation: enables: Azurite Lion moves your units, and Holy Immolation acts on units around its target
   - Spirit of the Wild -> Avalanche: enables: Spirit of the Wild moves units, and Avalanche acts on units base's starting side or on your leader (Spirit only reactivates, moves nothing)
   - 3 lines.

10. Wrong reason words. Breaks L10.
    - Replace is called "shuffles cards into the deck": Aethermaster -> White Widow: triggers: shuffles cards into the deck; Theobule -> Inquisitor Kron: triggers: shuffles cards into the deck. Should say it replaces cards. About 9 lines.
    - Blood Taura's cost is the General's Health, so damage to my General makes it cheaper, not "enables": Flameblood Warlock -> Blood Taura: enables: damages your leader. 3 lines.
    - A fight reason for a card that takes no fight: Mirkblood Devourer -> Inquisitor Kron: makes stronger: keeps it alive in the fights it takes on when it comes. 1 line.
    - One reason said twice: Frigid Corona -> Disciple of Yggdra: enables: makes enemy units get Stunned; also triggers: makes enemy units get Stunned; Punish -> Abyssal Scar (Bloodbound Spell): triggers: makes units die (for the ability it gives); also makes units die. About 7 lines.

11. Stats on a move spell linked as extra help where only the move matters. Breaks L18.
    - Mist Dragon Seal -> Bonereaper: ...; also makes stronger: can give it more power and health
    - 1 line.

12. Missing lines.
    - Fractal Replication summons copies into play (L19): should link to Dying Wish cards in its deck: Unseven, Grimes, Dagona (Vaath Dying Wish deck). None exist.
    - A return to the action bar of a card with Opening Gambit (L14): Hailstone Prison -> Hearth-Sister (Kara Arcanysts deck); Sandswirl Reader -> Azure Herald, Sandswirl Reader -> Healing Mystic (Ciphyron Build deck). None exist.

## Unsure
- Golem Metallurgist -> Ragebinder / Juggernaut / Lavaslasher: correct only if these are Golems; the tribe is not in the printed text.
- Replicant -> Theobule: triggers: fills your hand. Drawing a card is generic (L1b); probably wrong.
- Primus Fist -> Abhorrent Unbirth and Mirkblood Devourer -> Abhorrent Unbirth: Unbirth reads the Attack and Health of the destroyed minions, so it may be a correct stat-reader line.
- Bangle of Blinding Strike -> Mask of Shadows: Celerity is extra moves, not a move effect; likely L1, but it does help reach "behind".
- Holy Immolation -> Silverguard Knight: heals: can heal it. Silverguard has Provoke; L18 keeps health for Taunt, not clearly healing.
- Mirrorrim -> Lifestream (missing?): Mirrorrim puts copies into the deck that Lifestream draws; copies into deck are generic by L19.
- The 27 "is a spell whose playing sets off its effect" lines (Owlbeast Sage, Prismatic Illusionist, Blue Conjurer): right only if spells are a minority in Duelyst (L1b).

## Must stay (correct)
- Flicker -> Mask of Shadows: enables: Flicker moves your units, and Mask of Shadows acts on units behind its target
- Unseven -> Dagona: puts it into play: puts it into play from the hand
- Abyssal Scar (Bloodbound Spell) -> Punish: enables: damages enemy units or players: Punish kills them
- Kujata -> Juggernaut: triggers: damages it for its effect
- Wraithling -> Inkling Surge: enables: is the Wraithling it names

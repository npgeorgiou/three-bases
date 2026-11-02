# Duelyst check, part u1 (parts a-f, h)

Read: lines 1-779 and 3877-4268; not read: none

## Causes

1. **Help to a General whose text does not use it.** A General's own text is only its Bloodbound Spell, yet every heal, power boost and keyword for the General links to every General. Breaks L14, L18 and L20. About 300 lines in part h.
   - Aer Pridebeak -> Argeon Highmayne: heals: can heal it
   - Dawn's Eye -> Argeon Highmayne: stronger: can give it more power
   - Grove Lion -> Faie Bloodwing: keyword: can give it Forcefield
   - Notion of Starless Eternity -> Zirix Starstrider: keyword: can give it Frenzy
   - Time Maelstrom -> Scioness Sajj: stronger: can ready it

2. **Damage to a General is read as damage to the minion.** The card hurts only the Generals, but it links to a minion that waits to take damage, or to a minion-only effect. Breaks L7. About 10 lines.
   - Flameblood Warlock -> Lantern Fox: waits: damages it for its effect
   - Elucidator -> Juggernaut: waits: damages it for its effect (also Sellsoul, Tectonic Spikes and Dreamgazer -> Juggernaut)
   - Dark Nemesis -> Deathstrike Seal: waits: damages units or players (for the ability it gives). The Seal destroys only minions.

3. **An attack every General or unit makes, or the counterattack rule, is counted as a combo.** Breaks L1, L2 and L9. About 12 lines.
   - Faie Bloodwing -> Resonance Scythe: waits: kills enemy units (by fighting). The same pair also has "(by the game's rule: units counterattack)". Kara Winterblade and Ilena Cryobyte have the same two lines.
   - Pyromancer -> Day Watcher: waits: makes your units attack (by fighting). Blast is no extra attack. Starfire Scarab has the same line.
   - Grandmaster Zendo -> Day Watcher: waits: makes your units attack (by fighting). Zendo makes the ENEMY General attack.
   - Grandmaster Kraigon -> Day Watcher: waits: makes your units attack (by fighting)

4. **Sentinel is triggered by the opponent's summon, and Night Watcher punishes Rush minions, yet my own summons link to them as help.** Breaks L9 and "read wants right" (L21). The Sentinel's effect also hits the ENEMY minion, so its lines to my damage and death cards are wrong. About 50 lines.
   - Firestarter -> Night Watcher: waits: puts units into play. Night Watcher exhausts my own Spellspark.
   - Saberspine Tiger -> Night Watcher: waits: is a unit whose summoning sets off its effect (the same for Spectral Revenant and Tusk Boar)
   - Grailmaster -> Night Watcher: type: makes units get Rush
   - Firestarter -> Bound Tormentor: waits: puts units into play (the same for Freeblade and Hundred-Handed Rakushi, from every summoner)
   - Hundred-Handed Rakushi -> Rawr: waits: damages it for its effect. The same goes for Rakushi -> Sarlac (kills it) and Rakushi -> Zurael.

5. **A summoner links to a card that waits for a certain kind of summon (from the action bar, a Mech, a Vespyr, 1 or less Attack) although it does not make that kind.** Breaks L17 and L20. About 40 lines.
   - Firestarter -> Hideatsu the Ebon Ox: waits: puts your units into play. Hideatsu counts summons from the action bar only. The same line comes from Prismatic Illusionist, Dagona, Unseven, Sarlac, Zurael, Jax Truesight and Inquisitor Kron.
   - Spriggin -> S.I.L.V.E.R.: waits: puts your units into play. Spriggin Kin is no Mech.
   - Zurael, the Lifegiver -> Echo Deliverant: waits: puts your units into play. The same comes from Dagona and Unseven, and also to Borean Bear and Glacial Elemental (Vespyr).
   - Prismatic Illusionist -> Grand Strategos: type: puts your units into play. An Illusion has 2 Attack.

6. **"Summon from deck" or "summon a copy" links to cards with no summon or death effect.** An Opening Gambit also does not go off when the minion is summoned from the deck. Breaks L17 and L19. About 15 lines.
   - Radiant Standard -> Futureshaker: puts: puts it into play from the deck (the same for Ghoulie, Silvertongue Corsair and Mogwai)
   - Radiant Standard -> Lady Locke: puts: puts it into play from the deck. Lady Locke's effect is an Opening Gambit.
   - Mirror Meld -> Bluetip Scorpion: puts: copies it (the same for Araki Headhunter and Tusk Boar)

7. **A power or health boost links to cards whose text reads a different card's stats, or no stats at all.** Calculator reads Battle Pets in the action bar. Drogon and Effulgent Infusion read the General. Sunset Paragon reads ALL nearby minions. Thunderhorn and Mortar-maw only hit several. Desolator and Nightshroud steal a fixed amount. Bloodsworn Gambler attacks again. Breaks L18 and L7. About 250 lines.
   - Afterblaze -> Calculator: stronger: more power (62 such, plus 45 "more health")
   - Afterblaze -> Thunderhorn: stronger: more power (61 such)
   - Afterblaze -> Sunset Paragon: stronger: more power (63 such)
   - Mirkblood Devourer -> Drogon: stronger: more power (Effulgent Infusion, Blood Baronette and Calculator in the same row)
   - Lady Locke -> Desolator: stronger: more power: its text uses the damage it deals when it comes (Nightshroud, Bloodsworn Gambler and Mortar-maw too; Wind Runner and Surgeforger also)

8. **A heal links to Provoke minions.** L18 lets only "more health" reach Taunt units, and a heal is no more health. Breaks L14. About 60 lines.
   - Lux Ignis -> Fireblazer: heals: can heal it (38 such)
   - Sundrop Elixir -> Fireblazer: heals: can heal it
   - Healing Mystic -> Lady Locke: heals: can heal it (the same to Bonereaper and Inquisitor Kron)

9. **A unit's own Celerity, Flying or move keyword is read as "A moves your units" near B.** The keyword moves only the card itself (L20). A card that moves only the General is also linked as moving B (L7). About 70 lines.
   - Azurite Lion -> Azure Horn Shaman: type: A moves your units, and B acts on units around it
   - Binky -> Shiro Puppydragon: type: Binky moves your units, and Shiro Puppydragon acts on units around it (Wings of Paradise -> Shiro Puppydragon is the same)
   - Silhouette Tracer -> Mizuchi: type: Silhouette Tracer moves Mizuchi, and Mizuchi acts on units behind its target
   - Bangle of Blinding Strike -> Wind Runner: waits: moves it for its effect (Notion of Starless Eternity and Resonance Scythe -> Wind Runner are the same)

10. **"Another friendly minion" is read as the card itself.** Oropsisaur waits for ANOTHER Grow minion to survive damage. Breaks L7. About 5 sure lines.
    - Owlbeast Sage -> Oropsisaur: waits: more health or protection: survives damage. Owlbeast buffs Arcanysts only.
    - Healing Mystic -> Oropsisaur: waits: more health or protection: survives damage
    - Mirkblood Devourer -> Oropsisaur: waits: more health or protection: survives damage

11. **A spell filter is ignored, and the filter of a card's need or of its made card is not checked.** Breaks L21 ("read wants right"). About 320 lines.
    - Accumulonimbus -> The Scientist: waits: is a spell whose playing sets off its effect. The Scientist needs a spell that targets a friendly minion, yet all 308 spells link.
    - Alcuin Fugitive -> Pantheran: type: creates cards: more different cards to play. Pantheran needs the three Scion's Wish spells.
    - Alcuin Fugitive -> Hideatsu the Ebon Ox: type: creates cards: more different cards to play. Alcuin makes spells, but Hideatsu needs minions.
    - Blue Conjurer -> Oak in the Nemeton: type: creates cards. An Arcanyst is no token.
    - Lady Locke -> Hatefurnace: stronger: does what it waits for or counts (stat changed) when it comes. Hatefurnace counts spells.

12. **Any card that adds cards to hand links to Theobule as "fills your hand".** Theobule only replaces cards; it does not want a full hand. Breaks L21 ("read wants right"). Replace triggers are also worded as "shuffles cards into the deck" (L10). About 95 lines.
    - Aegis Barrier -> Theobule: waits: fills your hand (91 such)
    - Spelljammer -> Theobule: waits: fills your hand
    - Theobule -> Inquisitor Kron: waits: shuffles cards into the deck. The pair is right, but the reason should be about replacing.

13. **"Transforms" is equated with "built".** Breaks L10 and L1. About 4 lines.
    - Cloudcaller -> Rescue-RX: waits: transforms it for its effect
    - Disciple of Yggdra -> Architect-T2K5: waits: transforms cards
    - Eternity Painter -> Manakite Drifter: waits: transforms cards (for the ability it gives)

14. **My killing or damage of ENEMY minions links to cards that give MY minions Dying Wish, or to "whenever an enemy takes damage".** A damage trigger fed by a quarter of the game's cards is generic. Breaks L9 and L21. About 120 lines.
    - Bonereaper -> Ancient Grove: waits: makes units die (for the ability it gives). The same goes to Auroraboros, from Gnasher, Thunderhorn and Coldbiter.
    - Beastbound Savage -> Shadow Sister Kelaino: waits: damages enemy units or players (56 such)
    - Bonereaper -> Blood Rage: type: damages units or players

15. **A damage boost for spells links to every damaging spell.** Breaks L18 (gives_lines: more damage alone is never a use). 16 lines.
    - Crescent Spear -> Phoenix Fire: stronger: makes its effect bigger
    - Crescent Spear -> Twin Strike: stronger: makes its effect bigger
    - Psionic Strike -> Scioness Sajj: stronger: makes its effect bigger

16. **Repairing artifacts is read as healing.** Breaks L10. 8 lines.
    - Dawn's Eye -> Lightchaser: waits: heals units
    - Dawn's Eye -> Gold Vitriol: heals: can heal it
    - Dawn's Eye -> Excelsious: type: heals units

17. **One reason is given twice for the same pair.** Breaks L10 (one reason is said once). About 30 lines.
    - Disciple of Yggdra has "type: makes enemy units get Stunned" and "waits: makes enemy units get Stunned" from the same 11 cards.
    - Chassis of MECHAZ0R -> Echo Deliverant: waits: is a Mech whose summoning sets off its effect, AND waits: puts your units into play
    - Petal Flurry -> Kensho Vortex: waits: is a spell whose playing sets off its effect, AND cheaper: is a spell it needs played for its count

18. **A wrong stat word, or movement called stats.** Golden Justicar gives movement, not stats. Breaks L10. About 5 lines.
    - Golden Justicar -> Lady Locke: stronger: gives it more stats
    - Golden Justicar -> Bonereaper: stronger: gives it more stats
    - Bonechill Barrier (token) -> Letigress: keyword: gives it a keyword (when it is attacks for it). The Barrier stuns enemy attackers.

### Missed lines
- Cryoblade ("double damage to Stunned enemies") has no line from the Stun cards: Icy, Permafrost, Avalanche, Crystallize, Bellow, Tremor, Beam Shock.
- Omniseer (turns a space into Primal Flourish) has no line to Verdant Fulmination ("your minions on friendly Primal Flourish grow").

## Unsure
- Are spells (308 of 1036 cards) a minority for L1b? Each spell trigger (Owlbeast Sage, Firestarter and others) gets 308 lines, 15.5% of all lines.
- Auroara's "minion with 2 or less Attack" may be a filter that half the minions pass (L21). That would make its 129 lines generic.
- Kindling and Owlbeast Sage buff every Arcanyst. A tribe may be "no narrower than a deck" (L14).
- Health to a Grow minion pointed at Oropsisaur (21 lines). The help goes to the other Grow minion, not to Oropsisaur.
- Bonereaper, Gnasher and Thunderhorn -> Deathwatch cards (Shadowdancer and others) via "makes units die" may be generic by L21.
- Arctic Displacer -> Cryogenesis: Cryogenesis draws a Vespyr, which may be a tutor by kind (L1b).
- Aer Pridebeak -> Lucent Beam: Aer heals on the opponent's turn, but Lucent Beam needs a heal this turn.
- Psychic Conduit -> Bone Swarm: Conduit takes control of a minion; it does not move it.
- Calculator <- Rawr: Rawr summons the pet to the board, not to the action bar.
- Golem Vanquisher -> Juggernaut: Vanquisher gives Provoke, which Juggernaut's text does not use (L14).

## Must-stay examples (checked, correct)
- Lurking Fear -> Gnasher: cheaper: makes it cheaper
- Bonereaper -> Deathstrike Seal: waits: damages units or players (for the ability it gives)
- Progenitor -> Dreadnought: waits: puts your units into play
- Timekeeper -> Biomimetic Hulk: stronger: can speed up its countdown
- Xho -> Hydrax: type: is a Battle Pet it asks for

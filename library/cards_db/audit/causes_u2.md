# Duelyst, part g (lines 780-3876): causes

Read: lines 780-3876; not read: none (all 3097 lines read).
Card texts checked with txt.py for about 190 cards. Counts are rough: share of the 50-line sample times the group size.

## 1. Opponent-side triggers fed by my cards (L9)
Wrong thinking: "whenever a spell is cast / a minion is summoned" is read without "your opponent" or "Sentinel". Sentinel cards (Xerroloth, Mind-Cage Oni, Moonlit Basilysk, Bound Tormentor, Freeblade, Hundred-Handed Rakushi) and "your opponent casts" cards go off on the ENEMY's act, so my spells and summons feed nothing.
- Lurking Fear -> Xerroloth: waits: is a spell whose playing sets off its effect
- Twin Strike -> Mind-Cage Oni: waits: is a spell whose playing sets off its effect
- Brilliant Plume -> Moonlit Basilysk: waits: is a spell whose playing sets off its effect
- Gloomchaser -> Bound Tormentor: waits: puts units into play
- Wintertide -> Freeblade: waits: puts units into play
Count: about 380 of the 2388 spell lines, and about 130 of the 179 "puts units into play" lines.

## 2. Night Watcher read as a payoff (L5, L9)
Wrong thinking: "whenever ANY player summons a minion with Rush, exhaust it" counted as a need. It punishes Rush, and most summoners linked to it make no Rush minion at all.
- Accumulonimbus -> Night Watcher: waits: puts units into play
- Vale Ascension -> Night Watcher: waits: puts units into play
- Rasha's Curse -> Night Watcher: waits: puts units into play
Count: about 40 lines (all Night Watcher lines in this group).

## 3. Damage or kills on one side fed to a need on the other side (L9, L11)
Wrong thinking: any damage or kill counts for any death or damage trigger. Enemy-only kills cannot set off my Dying Wish or "friendly minion dies". Friendly-only kills cannot set off a need that an enemy dies (Grasp of Agony). Damage to my General is not damage to a minion.
- Deathmark -> Ironclad: waits: kills it for its death effect
- Fortified Assault -> Fog: waits: kills it for its death effect
- Obliterate -> Sarlac the Eternal: waits: kills it for its death effect
- Cryogenesis -> Auroraboros: waits: makes units die (for the ability it gives)
- Darkfire Sacrifice -> Grasp of Agony: waits: makes units die (for the ability it gives)
Also: Hydrogarm/Chromatic Cold/Mana Deathgrip -> Ancient Grove; Crossbones -> Dance of Dreams; Flameblood Warlock, Hamon Bladeseeker, Dreamgazer -> Rawr/Jade Monk/Ooz; Bloodfire Totem -> Eclipse; Sellsoul -> Nimbus.
Count: about 100 of 376 "for the ability it gives", about 60 of 998 "kills it for its death effect", about 50 of 356 "damages it for its effect".

## 4. Damage to a card whose damage effect punishes or helps the enemy (L5, L9)
Wrong thinking: "whenever this takes damage" is always a need. Haruspex makes your opponent draw, and Tethermancer dispels the minion that damaged it. Both are drawbacks or anti-enemy effects, not combos with my own damage.
- Riftwalker -> Haruspex: waits: damages it for its effect
- Kinetic Equilibrium -> Haruspex: waits: damages it for its effect
- Spirit Harvester -> Tethermancer: waits: damages it for its effect
- Homeostatic Rebuke -> Tethermancer: waits: damages it for its effect
Count: about 50 lines.

## 5. The General gets lines from what every General is (L1, L13, L14, L18)
Wrong thinking: each General card is a partner for "your General gains +Attack", heals to your General, or "your General gains Backstab". Every deck has a General, and its text is only "Bloodbound Spell: X". That makes the line generic.
- Staff Of Y'Kir -> Ciphyron Ascendant: stronger: can give it more power
- Mask of Shadows -> Kaleos Xaan: keyword: can give it Backstab
- Azure Herald -> Ilena Cryobyte: heals: can heal it
- Day Watcher -> Vaath the Immortal: heals: can heal it
- Arclyte Regalia -> Argeon Highmayne: stronger: can shield it from damage
Count: about 140 of 158 "can give it more power" and about 200 of 515 "can heal it".

## 6. A minion buff sent to a card that reads the General's stat (L7)
Wrong thinking: Drogon ("double your General's Attack"), Effulgent Infusion ("+Attack equal to your General's Attack") and Blood Taura ("cost is your General's health") read the General. Buffs to minions do not feed them, and General health makes Blood Taura cost more, not less.
- Blood Rage -> Effulgent Infusion: stronger: more power
- Diretide Frenzy -> Drogon: stronger: more power
- Greater Fortitude -> Drogon: stronger: more power
- Hsuku -> Blood Taura: stronger: more health
- Frostfire -> Blood Taura: stronger: more health
Count: about 110 of 319 "more power" and about 10 of 150 "more health".

## 7. Movers that move the General linked as moving the minion (L7)
Wrong thinking: "teleport your General" or "your General has Celerity" moves the minion. Backstab minions need to be moved behind an enemy themselves. Bombard reactivates Ranged minions, but the Backstab targets have no Ranged.
- Mist Walking -> Gore Horn: type: Mist Walking moves Gore Horn, and Gore Horn acts on units behind its target
- Flicker -> Dusk Rigger: type: Flicker moves Dusk Rigger, ...
- Silhouette Tracer -> Katara: type: ...
- Bangle of Blinding Strike -> Kaido Assassin: type: ...
- Bombard -> Penumbraxx: waits: makes it attack for its effect
Count: about 75 of 175.

## 8. A unit's own movement keyword linked to every positional card (L1, L20)
Wrong thinking: a card with Flying or Celerity "moves your units", so it links to every card that acts on units nearby (Shiro Puppydragon, Vigilator, Deepfire Devourer, Fealty, Halo Bulwark, Dauntless Advance, Roar, Pupabomb, Synaptic Arbitrage). These keywords only move the card itself, and every unit can move. Pupabomb needs an Egg, and Synaptic Arbitrage acts on enemies.
- Dragonlark -> Vigilator: type: Dragonlark moves your units, and Vigilator acts on units around it
- Storm Aratha -> Shiro Puppydragon: type: ...
- Emberwyrm -> Skywind Glaives: type: ... acts on units around your leader or base
- Trinity Wing -> Pupabomb: type: ... acts on units around its target
- Mindlathe -> Void Steal: type: Mindlathe moves your units, ...
Count: about 450 of the 640 lines in the three "moves your units" groups.

## 9. Revival cards linked against their own limits (L20, L21)
Wrong thinking: any friendly death feeds any reviver. Zurael brings back only minions destroyed on the opponent's last turn, so my own-turn sacrifices do not count. Blood Echoes brings back only the minions it destroys itself. Simulacra Obelysk and Kujata kill nothing.
- Darkfire Sacrifice -> Zurael, the Lifegiver: type: makes your units die: Zurael, the Lifegiver brings them back
- Abhorrent Unbirth -> Blood Echoes: type: makes your units die: Blood Echoes brings them back
- Simulacra Obelysk -> Keeper of the Vale: type: makes your units die: ...
- Deathmark -> Blood Echoes: type: ... (enemy-only kill, also cause 3)
Count: about 65 of 175.

## 10. Tribe-limited summon payoffs fed by the wrong tribe (L20)
Wrong thinking: any summon feeds "whenever you summon a Mech / Vespyr / Ranged minion". Hideatsu's Trial counts only minions summoned from the action bar, so effect summons and MECHAZ0R pieces do not count.
- Gate to the Undervault -> S.I.L.V.E.R.: waits: puts your units into play
- Spriggin -> Borean Bear: waits: puts your units into play
- Dagona -> Xenkai Cannoneer: waits: puts your units into play
- Helm of MECHAZ0R -> Hideatsu the Ebon Ox: waits: puts your units into play
- Khymera -> Hideatsu the Ebon Ox: waits: puts your units into play
Count: about 200 of 724.

## 11. Frenzy and plain fighting counted as "makes units die" (L2, L18)
Wrong thinking: a minion with Frenzy (or only fight keywords) makes units die for Deathwatch. That is attacking, a game rule; Frenzy only hits more.
- Piercing Mantis -> Gate to the Undervault: waits: makes units die
- Serpenti -> Mana Deathgrip: waits: makes units die
- War Talon -> Shadowdancer: waits: makes units die
- MECHAZ0R! -> Stygian Observer: waits: makes units die
- Furor Chakram -> Inkhorn Gaze: waits: makes units die
Count: about 100 of 443.

## 12. Hits-several-times and fight-on-summon cards given generic stat lines (L18, L14)
Wrong thinking: a buff helps Bloodsworn Gambler (attacks again) or Mortar-maw (splash). L18 calls that generic. Lavaslasher fights on summon, before any later buff. Filters are also ignored: Oak in the Nemeton buffs only tokens, and Iceblade Dryad/Vespyrian Might buff any Vespyr, which is a tribe and no narrower than a deck.
- Killing Edge -> Bloodsworn Gambler: stronger: can give it more power and health
- Greater Fortitude -> Mortar-maw: stronger: can give it more power and health
- Blood Rage -> Lavaslasher: stronger: can give it more power and health
- Oak in the Nemeton -> Wind Stopper: stronger: gives it more power and health
- Iceblade Dryad -> Winter Maerid: stronger: can give it more power and health
Count: about 70 of the 405 + 456 stat lines. Note: Scion's Third Wish -> Duskweaver goes the wrong way; Duskweaver makes Scion's Wishes.

## 13. Follow-ups, placeholders and AI helpers treated as owned cards (L9)
Wrong thinking: internal follow-up effects and placeholders are cards a player plays. No player owns them.
- Teleport (follow-up, FollowupTeleportMyGeneralBehindEnemy) -> Chakri Avatar: waits: is a spell whose playing sets off its effect
- MECHAZ0R Progression -> Firestorm Mantra: type: is a spell it needs played for its count
- Spell Damge -> Soul Grimwar: waits: makes units die (for the ability it gives)
- Cascading Rebirth (follow-up) -> Sellsoul: waits: kills it for its death effect
- Teleport Enemy To Me -> Firestorm Mantra / Festive Spirit -> Firestorm Mantra
Count: about 120 across all groups.

## 14. One reason said twice or with an extra wrong reason (L10)
- Corporeal Cadence -> Soul Grimwar: both "makes units die (for the ability it gives)" and "makes units die"
- Chassis of MECHAZ0R -> S.I.L.V.E.R.: "puts your units into play" added to the Mech reasons, but Chassis summons nothing (it is only played)
- Lifestream -> Lightchaser: "waits: heals units" plus "heals: can heal it"
- Ritual Banishing -> The Releaser: "waits: makes your cards leave play"; The Releaser goes off when the artifact breaks, not when minions leave play
- Amplification -> Hatefurnace: "stronger: can give it more power" added to the correct type line
Count: about 150.

## Unsure
- Heal to Provoke minions (Fiz -> Slo, Fountain of Youth -> Tombstone): L18 allows more health for Taunt, but it is not clear whether healing counts.
- Wind Sister Maia -> Snow Rippler/Shivers: is Infiltrate a narrow enough kind for an aimed buff?
- Riftwalker/Warbird/White Widow -> Mana Deathgrip and -> Inkhorn Gaze: helps the target die this turn. Possibly fine.
- Kotetsu, Gotatsu, Murasame, Kiyomori -> spell triggers: kind not checked; they may not be spells.
- Death Knell / Corpse Combustion / Amaranthine Vow fed by any friendly kill: they revive only Arcanysts, Dying Wish or Provoke minions.
- Windstorm Obelysk -> Zurael (Dervishes disappear, they are not destroyed).
- Missing? Artifacts that raise the General's Attack (Staff Of Y'Kir, Adamantite Claws) have no lines to Drogon or Effulgent Infusion in this sample. Those lines should exist (L18: doubles or reads the stat). Not checked in the full line list.

## Must-stay examples (correct)
- Holy Immolation -> Sunriser: waits: heals units
- Juxtaposition -> Scroll Bandit: type: Juxtaposition moves Scroll Bandit, and Scroll Bandit acts on units behind its target
- Helm of MECHAZ0R -> Alter Rexx: waits: puts your units into play
- Bolster -> Divine Bond: stronger: more health
- Skywind Glaives -> Windblade Adept: stronger: can give it more power

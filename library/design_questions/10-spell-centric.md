# How to make a spell-centric faction?

`ask.py all kit spells_played_condition spell_power`

```
## duelyst
Songhai Empire (117 cards): spells_played_condition 1, spell_power 4
  Crescent Spear: Your General gains +1 Attack. Spells you cast that deal damage deal +1 damage.
  Eight Gates: Spells you cast this turn that deal damage deal +2 damage.
  Firestorm Mantra: Steal Health from the enemy General equal to twice the number of spells cast this turn.
  Storm Sister Alkyone: Spells you cast that deal damage deal +1 damage.
Vetruvian Imperium (114 cards): spells_played_condition 0, spell_power 3
  Grandmaster Nosh-Rak: Keywords: Blast, Flying. The enemy General takes double damage.
  Psionic Strike: Keywords: Bloodbound Spell. Your General deals double damage to minions this turn.
  Scioness Sajj: Bloodbound Spell: Psionic Strike.
  works with: on_spell (e.g. Ghost Seraphim -> Owlbeast Sage); on_lifegain (e.g. Firestorm Mantra -> Sunriser); tribal (e.g. Ghost Seraphim -> Nightshroud)
## faeria
Blue (72 cards): spells_played_condition 1, spell_power 0
  Dark Stalker: If you've played an event this turn, this costs 2 faeria less.
## monster_train
Stygian Guard (41 cards): spells_played_condition 0, spell_power 6
  Crypt Builder: Offering. Attuned. / Deal 60 damage to the front enemy unit and push it to the back.
  Gifts for a Guard: Draw 3 spells and apply Consume, +20 Magic Power and 0 Ember.
  Harness the Titan: Apply +5 Magic Power to spells in hand.
  Ice and Pyre: Pyrebound. Attuned. / Deal 90 damage to the front enemy unit.
Melting Remnant (43 cards): spells_played_condition 0, spell_power 2
  Mortal Entrapment: Attuned. / Deal 25 damage and apply Dazed 3 to an already damaged unit.
  Subsuming Blade: Piercing. / Deal 5 damage. / Slay: Increase damage by 3 permanently.
## runeterra
Bilgewater (218 cards): spells_played_condition 2, spell_power 20
  Bilgewater Tellstones: Create a Fleeting More Powder!, Playful Trickster, or Chum the Waters in hand.
  Boomship: Deal 1 to a unit. Summon Powder Kegs equal to the amount of damage dealt.
  Dreadway Deckhand: When I'm summoned, summon a Powder Keg.
  Fleet Admiral Shelly: Keywords: Elusive, Imbue. When you play 2 spells each round, grant other allies +1|+1.
Ionia (235 cards): spells_played_condition 14, spell_power 0
  Claws of the Dragon: While I'm in hand, summon me when you play 2 spells in a round.
  Deep Meditation: Keywords: Flow. Flow: I cost 2 less. Draw 2 other spells.
  Dragoncaller: Keywords: Attune, Flow. Round Start: Flow: Summon The Empyrean and grant it Ephemeral.
  Eye of the Dragon: Keywords: Attune, Flow. Round Start: Flow: Summon a Dragonling.
  works with: recycle (e.g. Deep Meditation -> Janna); on_discard (e.g. Master Yi's Wuju Style -> Rumble); turn_start (e.g. Deep Meditation -> Janna)
## sts1
Curse (14 cards): spells_played_condition 1, spell_power 2
  Doubt: Keywords: Unplayable. At the end of your turn, gain 1 Weak.
  Normality: Keywords: Unplayable. While in hand, you cannot play more than 3 cards this turn.
  Shame: Keywords: Unplayable. At the end of your turn, gain 1 Frail.
Defect (89 cards): spells_played_condition 1, spell_power 18
  Beam Cell: Deal 3 damage. Apply 1 Vulnerable.
  Biased Cognition: Gain 4 Focus. At the start of your turn, lose 1 Focus.
  Bullseye: Deal 8 damage. Apply 2 Lock-On.
  Chaos: Channel 1 random Orb.
  works with: passive (e.g. Velvet Choker -> Void); attack_gain (e.g. Mind Bloom -> Du-Vu Doll); spell_power (e.g. FTL -> Ritual Dagger)
```

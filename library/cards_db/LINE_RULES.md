# Rules every line must keep (network.py; Kaptain's decisions, each a rule for every game)

A line joins two cards of one deck when a player would say "A does this for B". These rules decide, with their exceptions,
not taste. A case in cases/network.tsv written by Kaptain ("Kaptain <date>" in its source) is his decision.

- L1 A line comes from what a card's TEXT does, never from what every card does or is. Every card can be played, drawn,
  discarded, can attack and has Life: none of these makes a line (Chump Whump -> Get Excited!: no, any card can be discarded;
  "whenever you play a card", After Image: no line from every card).
- L1b (1 Nov 2026) A draw, return to hand or tutor by kind only ("draw a unit", "return a spell") makes no line. "Whenever you
  play a spell" or "the number of spells in your deck" makes no line where most of the game's cards are of that kind (Monster
  Train's Incant); a minority kind is a deck choice and keeps its line (Annie).
- L2 The game's rules are no combo, also not for a level-up: what every card can do counts for nothing (Living Shadow -> Zed, any unit -> Poppy, Jagged Butcher -> Gangplank, Ashe -> LeBlanc: no
  line). Only a card whose own text adds an attack (Rally, a free attack), a strike now, a second strike, or a keyword that
  does the need (Overwhelm and Elusive reach the Nexus for a card that needs it, deathtouch kills) makes the line.
- L3 A makes B, B acts on C: A gets NO line to C (Targonian Tellstones makes Blessing of Targon; only the Blessing helps Braum).
  A's own act of making links to a card that waits for that making (Zed summons Ephemeral units: Moonlit Glenkeeper). Only a
  planted card that goes off by itself when drawn counts as the planter's act (Chimes for Bard).
- L4 A help must do the very thing needed. Power gets no unit past blockers (For Demacia! does not help Zed hit the Nexus).
  Health and protection help "survive damage". "Another attack" is only Rally or a free attack.
- L5 Limits and drawbacks are no needs ("the first 3 times you draw", Janna; "lose 1 energy when drawn", Void).
- L6 A helper points at what it helps and never "needs" it (Strength -> Attacks; Focus -> Orbs).
- L7 Read who does it: "I've attacked" = the card itself; "I've seen you" = the player; "your General" = the General.
- L8 Costs as paid: "X" and "spend all your mana" are variable (card.cost_x). A made or summoned card has its own kind (Tail of
  the Dragon is a unit, not a landmark).
- L9 My effects feed my needs; an effect on enemies feeds needs about enemies. Lines link only cards a player can own.
- L10 Line words say what a player says: triggers (a reaction), enables (a count or a thing that must be there), makes
  stronger / cheaper, helps it level up, puts it into play, can aim at it. A cost that drops for each X: what does X "makes it
  cheaper" (Gambling Chip -> Eviscerate), never "enables". One reason is said once, by its strongest kind.
- L11 A plain hit on one target (Strike, Mystic Shot) feeds no "when an enemy dies"; poison, hits on all and kill effects do.
- L12 Say who gets it: where the player is no card (Slay the Spire), a status on the player is "gives you Strength".
- L13 Per game: network.EXPENSIVE (the cost from which a card is expensive); a deck holds what the game gives every deck of its
  character (Slay the Spire's starting relic) unless a card replaces it; read the game's own limits of a mechanic (Dexterity
  adds only to Block a card gives when played).
- L14 (1 Nov 2026) Help aimed at any card of a kind ("give an ally +2|+0", "heal a unit", "copy an ally", "a unit strikes",
  "when you summon an ally, grant it +1|+1") links only to a card whose own text uses that help (Wuju Style -> Patched
  Porobot: no line). A faction or card kind ("a green creature", "a Demacia ally", "a follower") is no narrower than a deck.
  Kept: power and health as L18 says; a strike, attack or ready to a card with "Strike:"/"Attack:" or an activated ability; a
  copy as L19 says; a return to hand of a card with Play or Summon; a sacrifice of a card with Last Words; a cleanse to a card
  that puts that status on my side; help aimed near my leader to a card that acts near it (Roar -> Windblade Adept's Zeal); a
  keyword a card gives itself counts as its own; anything a card waits for, counts or levels from ("when healed", "allies
  with Barrier", "Level up: targeted").
- L15 (2 Nov 2026) What a keyword does to cards with the same keyword is the keyword's rule, no line (Pyke's Lurk grants
  Lurkers +1|+0: no Lurker -> Lurker line), unless the receiving card's own text uses it (Xerxa'Reth: "If I have 8+ Power";
  Gwen: "when another ally gains Power from Hallowed"). A card's own needs are its text and its reaction keywords (Revenge,
  Slay), never a keyword's inner working (Barrier pops when damaged, Challenger picks when attacking). "+1|+0" raises no Health.
- L16 A line said only as "can aim at it" is no reason. An act on a card (strike, return, copy, damage) links only with the
  card's own reason ("makes it attack or strike again: its own effect goes off").
- L17 Putting my units into play by kind (revive, summon from deck or discard) links to cards whose "when I'm summoned" goes
  off (The Harrowing -> Captain Farron). A card that makes a card by description links to a card that counts such cards played
  (Ferros Financier manifests a 6+ cost spell: Jayce, Lux). A count of mana spent on a kind ("6+ mana of spells", Lux) is fed
  like a count of that kind played.
- L18 (2 Nov 2026) More damage is generic: more power, Strength, Dexterity, Magic Power, Vulnerable, Wrath, Mantra or A.C.I.D.
  make NO line because a card hits, has Overwhelm, Elusive, Fearsome, Quick or Double Attack, Multistrike, hits several times
  (Twin Strike), or has "Strike:", "Nexus Strike:" or "Slay:" (more damage is always good: the game's goal, not the card's text).
  A line stays only where the card's own text reads the damage or the stat: it deals damage by its power in a fight its text
  starts (Deepwood Stalker), needs one big strike (Vi: 10+ damage), gets something back from the damage (Reaper, Lifesteal),
  doubles what is there (Burst -> Catalyst; "The Dreadway -> Decimate is a combo that works"), reads its power ("double my
  Power", "grant it my stats"), or levels up from it (L24). More health links only to Taunt units and to cards that wait to
  survive damage. Stat help is said in three families, never with numbers: "gives it more power", "more health", "more power
  and health" (Stormbound: "more strength"; less: "lowers its stats").
- L19 (2 Nov 2026) A copy put into hand or deck is one more card of any kind: no line. A copy put into play links only to cards
  whose summon or death effect it sets off (Dawn and Dusk -> Vekauran Vagabond); a summoned copy is not played, so a Play effect
  does not count. "When you play a follower" (Beguiling Cobra) is any unit (L1b).
- L20 A fight keyword (Elusive, Fearsome, Overwhelm, Quick Attack...) works for the card that has it: Nasus's Fearsome gets
  Nasus to the Nexus, not Abyssal Eye. A card made by name must be the kind the need asks ("when you summon an Elite":
  Emperor's Divide's Sand Soldiers are none). Giving Overwhelm or Elusive to a card whose text needs to hit the Nexus is a line
  ("helps it hit the enemy player").
- L21 (2 Nov 2026) What most cards do is no deck choice: a filter that half the cards of the kind pass ("costs 2 or more", "a
  creature with higher Attack than Life", "summoned near your General") or a type a fifth of its own kind has (Slay the Spire's
  Skill, Attack) is generic for a pick, tutor, repeat or boost (Secret Technique, Burst: no line); a count of a minority type
  stays (Kunai, Rage: "every Attack played"). A repeat or bigger effect for spells, landmarks or equipment stays only where they
  are a minority (Doctor Mia; not Monster Train's spells). Damage or kills that a quarter of the game's cards make by their own
  text feed no "whenever damage is dealt" trigger (Envenom, The Boot), unless it levels up or the doer is the enemy (Vek
  Hormones). Read wants right: "draw until you have 6" (Expertise) wants an empty hand; "if you have no Block" (Auto-Shields)
  wants none; "repeat Summon effects" (Transcendimp) is for cards with Summon.
- L22 (2 Nov 2026) What pays a card's cost is a line: a land changed to the colour a card needs pays its land cost (Ring of
  Dominion: "turns a land into the colour it needs: helps pay its land cost, and can take that land from the enemy").
- L23 (3 Nov 2026) A unit that moves itself gives no line to cards that depend on positions (Faeria, Duelyst).
- L24 (Kaptain, 3 Nov 2026) Everything that helps a champion's level-up condition (and the same in other games: a card that
  grows, levels or transforms when a condition is met) is a link, said "helps it level up". Gwen levels from dealing 10+
  damage, so more power for Gwen (Tybaulk) helps her level. Older rules and cases that say otherwise (n269) give way to this.

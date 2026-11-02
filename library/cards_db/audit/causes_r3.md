# Runeterra check r3 (parts c, d, e, start of f)

Read: lines 1654-3063; not read: lines 3064-3221

Note: stopped by the coordinator before part f was finished. Only one line of f was judged. The card texts used are the ones printed in the file; txt.py was not run.

## Causes (wrong lines)

1. Help to any card of a kind goes to cards whose text does not use it (L14, L18). A stat boost or keyword "for 1 cost allies", "Elite allies", "Tech allies", "Yordles", "Fae" or "Challenging allies" is linked to plain cards with no text, or only Quick Attack or Challenger. About 70 lines.
   - Battlesmith -> Blocking Badgerbear: stronger: gives it more power and health when it comes (this is the L14 example: Blocking Badgerbear has no text)
   - Professor von Yipp -> Bloodthirsty Marauder: stronger: gives it more power and health when it comes
   - Reaver's Row -> Snow Hare: keyword: gives it Fearsome
   - Hextech Handler -> Golden Crushbot: stronger: gives it more power
   - Swiftwing Flight -> Laurent Protege: stronger: can give it more power and health
   - The same shape: Domination, Jagged Taskmaster, Siren Song (1 cost); Might of the Vanguard, Reinforcements (Elite); Paparo the Great, Yordle Explorer, Rumble (level 2) (Yordle); Fae Aid, Grandfather Fae (Fae); Terror of the Tides -> The Beast Below (Fearsome).

2. Any stat change is read as Gwen's Hallowed trigger (L15 names Gwen). Gwen, Gwen (level 2) and Sacred Shears wait only for "another ally gains Power from Hallowed". Frostbite on an enemy, a self-buff keyword (Fated, Augment, Deep) or enemy Gloom is not that. About 20 lines.
   - Rimetusk Shaman -> Gwen (level 2): waits: changes units' stats (for the ability it gives)
   - Starhound Pack -> Sacred Shears: waits: changes your units' stats
   - Grotesque Gift -> Gwen: waits: changes your units' stats
   - Icevale Archer -> Sacred Shears: waits: changes units' stats (for the ability it gives)

3. A card that changes stats is linked to Out Of The Way, which only makes "this round" buffs permanent. None of these give a "this round" buff, and Grotesque Gift acts on enemies (L9). 4 lines.
   - Starhound Pack -> Out Of The Way: type: changes your units' stats: Out Of The Way lets them do more
   - Grotesque Gift -> Out Of The Way: type: changes your units' stats: Out Of The Way lets them do more
   - Also The Beast Below and Carved Bladetwirler.

4. An enemy debuff is read as "changes your units' stats" for champion level-ups (L9). Grotesque Gift gives an ENEMY Gloom but is linked as if it buffed allies. 3 lines.
   - Grotesque Gift -> Aurelion Sol: levels: changes your units' stats (levels it up)
   - Grotesque Gift -> Bard: levels: changes your units' stats (levels it up)
   - Grotesque Gift -> Galio: levels: changes your units' stats (levels it up)

5. Wrong doer (L7). Molten Shield, Obeyed Order, Short Fuse and Threaded Volley hit Annie's, Captive Greyback's, Ziggs' and Taliyah's blocker. A Challenger choosing a blocker for itself does not feed them. About 12 lines.
   - Laurent Protege -> Obeyed Order: type: makes enemy units block: Obeyed Order damages them
   - Fiora (level 2) -> Molten Shield (created): type: makes enemy units block: Molten Shield (created) damages them
   - Trifarian Gloryseeker -> Threaded Volley: type: makes enemy units block: Threaded Volley damages them

6. Challenger is read as targeting (L15: "Challenger picks when attacking" is the keyword's own working). Ezreal counts spell or skill targets. 3 lines.
   - Laurent Protege -> Ezreal: levels: targets enemy cards (levels it up)
   - Fiora (level 2) -> Ezreal: levels: targets enemy cards (levels it up)
   - Trifarian Gloryseeker -> Ezreal: levels: targets enemy cards (levels it up)

7. Any keyword or status is read as the one that is counted. Legion General counts only Stunned or Recalled units, and Curse, Vulnerable and Gloom are neither. Lux: Illuminated and Void Abomination count POSITIVE keywords, and Curse is negative. About 6 lines.
   - Chained Caster -> Legion General: type: has Curse
   - Chained Caster -> Lux: Illuminated: levels: has Curse (levels it up)
   - Chained Caster -> Void Abomination: waits: has Curse
   - Lisa and Dolly -> Legion General: type: makes units get a keyword or status
   - Baccai Sandspinner -> Legion General / Grotesque Gift -> Legion General: same

8. A faction ask is treated as a deck choice (L14: a faction is no narrower than a deck). Trifarian Hopeful asks for "another Noxus ally". 4 lines.
   - Reckless Trifarian -> Trifarian Hopeful: type: is a unit it asks for
   - Legion Rearguard -> Trifarian Hopeful: type: is a unit it asks for
   - Arena Kingpin -> Trifarian Hopeful / Trifarian Gloryseeker -> Trifarian Hopeful: same

9. Nautilus copies Tossed 4+ cost allies into the deck. A copy into the deck is generic (L19), and it is also by kind only. About 11 lines.
   - Nautilus -> Bull Elnuk: puts: copies it
   - Nautilus -> Illegal Contraption: puts: copies it
   - Nautilus -> Starhound Pack: puts: copies it

10. A copy put into play is linked to a card with no summon or death effect (L19).
    - Pack Attack -> Pakaa Protector: puts: copies it (Pakaa Protector has no text)

11. Grandmaster at Arms is an Origin (a deckbuilding rule), not a spell or skill a player plays. It is counted as a played spell, and Jax "casts" it. 15 lines.
    - Grandmaster at Arms -> Annie: levels: is a spell it needs played for its count (levels it up)
    - Grandmaster at Arms -> The Prefect: waits: is a spell whose playing sets off its effect
    - Jax -> Grandmaster at Arms: puts: casts its skill

12. A unit summoned for the opponent is linked as mine (L9).
    - Stalking Wolf -> Snow Hare: puts: summons ("your opponent summons a Snow Hare")

13. A drawback is replayed as if it were a gain (L5). Chained Caster's Play only curses itself, so returning it to hand gives nothing. 5 lines.
    - Gruesome Theater -> Chained Caster: waits: returns it to hand: its Play or summon effect goes off again
    - Also Lead and Follow, Lightning Rush, Shadows of the Past, Tag Out! (created) -> Chained Caster.

14. The f line is half wrong (L20). They Who Endure's own Overwhelm damages the Nexus, which Mammoth Shaman counts, so that reason is right. But They Who Endure does not give Mammoth Shaman anything that helps it hit.
    - They Who Endure -> Mammoth Shaman: type: helps it hit the enemy player (wrong; keep "damages the enemy player")

## Causes (missing lines)

15. Champion spells ("X's Spell ... Create an X in your deck") get no lines at all. They are missing both the made champion and their own effects. The plain versions of these spells do have lines, for example Grotesque Gift -> Vex. 22 of the 49 cards in part d.
    - missing: Vex's Glare -> Vex (grants Gloom, levels it up) and Vex's Glare -> Shadow
    - missing: Xerath's Rite of the Arcane -> Xerath (destroys an allied landmark)
    - missing: Gnar's Wallop and Zoe's Sleepy Trouble Bubble (Stun) -> Legion General, Deadly Flourish, Curtain Call, Paddle Star, Jhin
    - missing: Norra's Portalpalooza -> Norra (level 2) (Mysterious Portals); Teemo's Mushroom Cloud -> Teemo
    - missing: Jax's Counter Strike -> Jax; Shen's Stand United (Barrier) -> Kinkou Student

16. A transform into a named card is not seen as "puts it into play".
    - missing: Avenging Vastaya's Ambush -> Avenging Vastaya, Blimp-Pack Poacher's Ambush -> Blimp-Pack Poacher, All-Terrain Trooper's Ambush, Packmother Nidalee's Ambush
    - missing: Pyke / Pyke (level 2) -> Death From Below ("When I Lurk, transform me into Death From Below"); Death From Below -> Pyke (summons Pyke)
    - missing: The Darkin Halberd -> Taarosh ("play me as Taarosh")

17. Ephemeral revives are not seen. Taarosh fills the attack with revived Ephemeral copies.
    - missing: Taarosh -> Moonlit Glenkeeper (the L3 example shape) and Taarosh -> Fallen Sands General

18. World Runes are not a kind the database knows.
    - missing: Shard of Hope / Reverence / Violence -> Ryze ("I see 3+ unique World Runes")
    - missing: Delve Into The Past -> each Shard (creates World Runes)

19. Overwhelm given to a card that needs to hit the Nexus is missing (L20).
    - missing: Heavy Blade Fragment and Wildclaw Stance -> Chempunk Pickpocket and Pakaa Cub ("Nexus Strike:")

## Unsure
- Insightful Investigator ("play a 2 cost card") and Tri-beam Improbulator ("play a 3 cost card"): these cost filters give many lines. Is one cost a minority (kept) or generic (L21)?
- Dragon Dedicant and The Smokescaled Host ("reduce a random card by 5") -> Mk5, Rimetusk Shaman, Vanguard Cavalry: a random card is not aimed help. It is unknown which of these cards count as expensive.
- Rumble (level 2) -> Arena Kingpin / Wizened Wizard (stronger, cheaper) and Arena Kingpin / Wizened Wizard -> Skrappy's Partsapalooza (Mecha): this is right only if they are Mecha Yordles, which their printed text does not show.
- Wizened Wizard -> Production Surge / Thermogenic Beam: does refilled spell mana count toward "spend all your mana"?
- Starhound Pack, Carved Bladetwirler, The Beast Below -> Aurelion Sol, Bard, Galio: a self-buff keyword does feed an ally-stat count. Is that a line or a keyword's inner working (L15)?
- Baccai Sandspinner (-1|-0) -> Ashe: this reduces Power to 0 only for 1-power enemies.
- Missing? Crumble, Blighted Caretaker, Astral Fox -> Fluft of Poros (sacrifice of a Last Breath card, L14).
- Missing? Horazi -> Frightened Ibex ("When I'm supported").
- Missing? Restored Sun Disc -> the Ascended champions; which cards are Ascended is not shown.
- Missing? Viego's Despair and Senna's Dawning Shadow (kill a unit) -> Kalista ("seen 3+ allies die").
- Data: Jayce (other form) and Yuumi (other form) each appear twice with different texts. No base form links to them.

## Correct lines (must stay)
- Laurent Protege -> Baccai Witherclaw: waits: makes this happen: challenges
- Cursed Keeper -> Escaped Abomination: puts: summons
- Aspiring Chronomancer -> Ekko: levels: makes this happen: predicts (levels it up)
- Grotesque Gift -> Vex: levels: makes units get Gloom (levels it up)
- Blocking Badgerbear -> Trusty Ramhound: waits: is an Elite whose summoning sets off its effect

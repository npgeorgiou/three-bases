# Causes, d_runeterra lines 1-1411 (findings appended per piece)

## Piece 1 (lines 1-150, Braum Zoe; Annie Gwen start)
Unsure:
- Sunburst -> Braum (level 2) exists ("damages it without killing it") but no Sunburst -> Braum (level 1), while Spirits Unleashed -> Braum exists. Sunburst (Sunburst has 1 partner). Unsure whether Braum L1 health survives 6.
- Omen Hawk -> Spectral Surveyor ("makes stronger: can give it more power and health", Lifesteal) exists, but Esmus, Breath of the World (support +1|+1) -> Spectral Surveyor is absent.
- Braum -> Zoe (level 2) "triggers: puts your units into play": the given ability is not visible in the rows (Zoe (level 2) shows no summon trigger); cannot confirm.
Must-stay: Braum -> Mighty Poro (summons); Targonian Tellstones -> Hush (creates); Zoe -> Zoe (level 2) levels into; Spirits Unleashed -> Braum (damage without killing, survives).
Read: 1-150

## Piece 2 (lines 151-300, Annie Gwen rest; Caitlyn Teemo start)
CAUSE A (missed line): a kill on a chosen unit of either side feeds The Harrowing only for some cards. Rule: L10/L9 (a kill that can hit my own unit "enables: makes your units die").
  - Soul Harvest (1 partners): `Soul Harvest: WHEN played of self DO choose_one OR kill chosen unit in board [category is follower] [power le 3] OR ...` has only "Soul Harvest -> Ceaseless Sentry" and no "-> The Harrowing"
  - same deck, present: `Glimpse Beyond -> The Harrowing: enables: makes your units die: The Harrowing brings them back`; `Disintegrate -> The Harrowing: enables: ...` (both can also pick my unit)
  - lines showing it: 1 (Soul Harvest)
Unsure:
- Mister Thrift (1 partners) has only Corina, Mastermind ("uses Trap"). Volatile Bloom (`repeat 5 top enemy card in deck [keyword is Trap]`, sets Traps off) and Chime (KW Boon, planted by Bursting Backpack, goes off by itself) have no line to it. Per L3 exception (planted card that goes off alone counts as the planter's act) Bursting Backpack -> Mister Thrift may be missing.
- Glare -> Gwen "changes your units' stats": Glare's row is give_keyword Gloom, no stat_change row; depends on Gloom's entry.
Must-stay: Annie -> Annie (level 2) levels into; Torment -> Annie (spell counted for her level up); Insider Knowledge -> Puffcap Peddler (spell sets off Imbue); Teemo -> Teemo (level 2) levels into; Disintegrate -> Ceaseless Sentry (kill sets off Last Breath).
Read: 151-300

## Piece 3 (lines 301-450, Caitlyn Teemo rest; Pyke Rek'Sai start)
CAUSE B (reason said twice, L10): one power boost is said as both "enables: changes its stats for its effect" and "makes stronger: more power" (or "triggers" plus "makes stronger") for the same pair. "One reason is said once, by its strongest kind."
  - `Call the Pack -> Xerxa'Reth, The Undertitan: enables: changes its stats for its effect; also makes stronger: more power`
  - `Bloodbait -> Xerxa'Reth, The Undertitan: enables: changes its stats for its effect; also makes stronger: more power`
  - `Blood in the Water -> Rek'Sai: helps it level up: another attack (levels it up); also makes it attack for its effect (levels it up); also triggers: makes it attack for its effect` (one extra attack said three times)
  - lines showing it so far: about 9 in 301-450 (every Lurk card -> Xerxa'Reth, plus Blood in the Water -> Rek'Sai / Xerxa'Reth); also piece 1: Omen Hawk -> Mihira
CAUSE C (stat help to a kind, L14/L18): Rek'Sai buffs "all Lurker units" (a kind, no narrower than a deck); lines "gives it more power" go to Lurkers whose own rows do not read power.
  - `Rek'Sai -> Sharkling: makes stronger: gives it more power` (Sharkling rows: only KW Lurk)
  - `Rek'Sai (level 2) -> Redfin Hammersnout: makes stronger: gives it more power` (Hammersnout rows: gives Vulnerable, no power read)
  - kept correctly: Rek'Sai -> Jaull-fish (its strike uses the Lurkers' power)
  - lines showing it: 4 here (Sharkling x2, Redfin Hammersnout x2)
CAUSE D (missed line, L2 a strike now): Bone Skewer (0 partners; `strike chosen mine unit in board to chosen enemy unit`) has no line to Pyke, whose level-up counts `damaged by mine unit [name_has is Pyke] damage ge 15`, nor to Pyke (level 2) (`killed by self of enemy unit`). Lines showing it: 1 (Bone Skewer; may repeat in Pyke's own list later).
Unsure:
- Teemo (level 2) copies Poison Puffcap Traps into the enemy deck: has -> Poison Puffcap but no -> Caitlyn, while Teemo (level 1) -> Caitlyn "plants traps that go off later" exists.
- Tybaulk -> Gwen (level 1) "also makes stronger: gives it more power": Gwen level 1 rows do not read power (only Hallowed, which is already the "triggers" reason).
Must-stay: Beguiling Blossom -> Flashbomb Trap (plants); Flashbomb Trap -> Caitlyn (a trap that goes off levels her); Poison Puffcap -> Teemo (is the card it names); Bloodbait -> Snapjaw Swarm (creates); Jaull-fish -> Frenzied Feast (casts its skill, is a Lurker it asks for).
Read: 301-450

## Piece 4 (lines 451-600, Pyke Rek'Sai rest; Bard Norra start)
CAUSE C grows (stat help aimed at "all Lurkers" goes to Lurkers whose rows do not read power; L14, L18 Overwhelm/Fearsome/Quick): more lines:
  - `Rek'Sai -> Xer'sai Dunebreaker: makes stronger: gives it more power` (Dunebreaker rows: KW Lurk, Overwhelm only)
  - `Rek'Sai (level 2) -> Xer'sai Hatchling: makes stronger: gives it more power` (KW Lurk, Fearsome only)
  - `Rek'Sai -> Xer'sai Caller: makes stronger: gives it more power` (Caller: Predict only)
  - `Rek'Sai -> Pyke: makes stronger: gives it more power` (Pyke: Quick Attack, levels from damage 15; L18 says more power is generic there)
  - total lines now showing it: about 17 (Sharkling, Redfin Hammersnout, Caller, Dunebreaker, Hatchling, Pyke, Pyke (level 2), each from Rek'Sai and Rek'Sai (level 2))
CAUSE B again (same boost said twice, L10): every Lurk card -> Xerxa'Reth, e.g. `Pyke -> Xerxa'Reth, The Undertitan: enables: changes its stats for its effect; also makes stronger: more power`, `Xer'sai Hatchling -> Xerxa'Reth ...` (about 8 more lines, 17 in total so far); also `Rek'Sai (level 2) -> Frenzied Feast: enables: is a Lurker it asks for; also makes a Lurker it asks for`.
CAUSE D extends: Pyke (5 partners) has no line from the other strikes now: `Frenzied Feast: strike all mine unit [type is Lurker] to random enemy unit` and `Jaull-fish: strike all mine unit [type is Lurker] ...` -> Pyke (Pyke -> Frenzied Feast "is a Lurker it asks for" proves Pyke is a Lurker, so they strike with Pyke and count for `damaged by mine unit [name_has is Pyke] damage ge 15`). Lines showing it: 2 more missing (Frenzied Feast -> Pyke, Jaull-fish -> Pyke); Blood in the Water (Rally) -> Pyke also absent (unsure).
CAUSE E (making a kind into hand/deck is a draw by kind, L1b/L19; Frenzied Feast needs Lurkers on the board): "makes a Lurker it asks for" from creating cards of a kind into hand or deck.
  - `Call the Pack -> Frenzied Feast: enables: makes a Lurker it asks for` (Call the Pack: create 2 random unit [type is Lurker] in hand)
  - `Bloodbait -> Frenzied Feast: enables: makes a Lurker it asks for` (Bloodbait: create <Snapjaw Swarm> in deck_top)
  - `Rek'Sai (level 2) -> Frenzied Feast: ... also makes a Lurker it asks for` (create random Lurker in hand)
  - lines showing it: 3. (Medium confidence: Frenzied Feast asks for Lurkers in play, not for cards made.)
Unsure:
- `Flashbomb Trap -> Junk Construct: triggers: damages it: its own effect goes off`: Flashbomb Trap only does `damage random mine unit (amount=1)`, a plain 1 hit (L11); Junk Construct's effect is `dies of self`. Only right if a 1 hit can kill it.
- Bard Norra part (a): Bard levels from `stat_changed of mine unit total_stats ge 20`; only Glare -> Bard is seen. Chime (+1|+1 to a unit in hand) -> Bard not seen yet; check in Bard's own list.
Must-stay: Pyke -> Pyke (level 2) levels into; Rek'Sai -> Rek'Sai (level 2) levels into; Poison Puffcap -> Living Library (a trap that goes off); Eclectic Collection -> Poison Puffcap (plants); Portalpalooza -> Norra (portal puts units into play, levels her).
Read: 451-600

## Piece 5 (lines 601-750, Bard Norra rest; Darius Gnar start)
CAUSE B again (L10, one reason said twice): `Chime -> Bard: helps it level up: changes your units' stats (levels it up); also makes stronger: can give it more power and health` (Bard's rows only read `stat_changed ... total_stats ge 20`, which is the level-up reason; compare `Esmus, Breath of the World -> Bard: helps it level up: changes your units' stats (levels it up)` with no extra "makes stronger"). Lines showing it here: 1.
CAUSE F (missed line, same planter treated differently): in Bard Norra Esmus, Breath of the World has 5 partners but only 4 lines are printed (Bard, Living Library, Proximity Puffcap, Bard (level 2)); its row `summoned of self DO keyword_action top mine card in deck_top <Chime Plant>` gives "Esmus -> Chime: puts it into play: plants", as `Byrd, The Bellringer -> Chime` (same row) has. Lines: 1 missing. (Also Junk Construct says 5 partners, 4 distinct partners printed.)
Unsure:
- `Proximity Puffcap -> Junk Construct: triggers: kills it for its death effect` and earlier `Flashbomb Trap -> Junk Construct`: both are plain `damage chosen unit (amount=1/3)` hits, not kills (L11); the reasons also read differently ("kills it" vs "damages it") for the same kind of hit.
- Mysterious Portal -> Portal Scholar (Scholar waits for `summoned ... mine unit [state is created]`, Portal summons such units) not visible in the printed lists.
Must-stay: Cosmic Binding -> Chime (plants); Bard -> The Wandering Caretaker (casts its skill, is the Bard it names); Chime -> Bard (level 2) (is the Chime it names); Portal Scholar -> Norra (portal puts units into play); Norra -> Norra (level 2) levels into.
Read: 601-750

## Piece 6 (lines 751-900, Darius Gnar rest; Ashe LeBlanc start)
CAUSE G (one reason said twice, L10/L20): a card whose only reason is the keyword Overwhelm is described both as "damages the enemy player" and "helps it hit the enemy player".
  - `Iron Ballista -> Gnar: helps it level up: damages the enemy player (levels it up); also helps it hit the enemy player (levels it up)` (Iron Ballista rows: `KW: Overwhelm` only)
  - `Darius (level 2) -> Gnar: ... damages the enemy player (levels it up); also helps it hit the enemy player (levels it up)` (rows: `KW: Overwhelm` only)
  - `Mega Gnar (level 2) -> Darius: ...` (same two phrases; no damage text in its rows), `Glacial Saurian -> Gnar` (same)
  - correct, two real reasons: `Tusk Speaker -> Darius` (text damages all players, and Overwhelm). `Pokey Stick -> Darius` (one phrase, text damage)
  - lines showing it: 7 (Iron Ballista x2, Darius (level 2), Darius -> Gnar, Mega Gnar (level 2), Glacial Saurian x2)
CAUSE H (missed line, L19 a copy put into play sets off summon effects): Mirror Image `copy chosen mine unit in board in board` has no line to cards with a "when I'm summoned" effect, and those cards stand with no partner.
  - Omen Hawk (`summoned of self DO stat_change 2 top mine unit in deck`): 0 partners, Mirror Image printed beside it as no line
  - Avarosan Hearthguard (`summoned of self DO stat_change all mine unit in deck`), Trifarian Assessor (`summoned of self DO draw ...`): both 0 partners
  - Incisive Tactician (`summoned of self DO keyword_action <Rally>`) the same
  - lines showing it: 4 missing (Mirror Image -> Omen Hawk, Hearthguard, Assessor, Incisive Tactician)
CAUSE I (missed line, medium confidence, L14 "counts"/L10 enables): power boosts have no line to cards that count or need units with power 5+.
  - Trifarian Assessor `draw ... count of (all mine unit in board [power ge 5])` has 0 partners; Bloody Business `strike chosen mine unit [power ge 5] to ...`
  - boosters with no partner: `Avarosan Hearthguard: stat_change all mine unit in deck (power=1, health=1)`, `Omen Hawk`, `Sky Splitter: stat_change chosen mine unit (power=1, health=3)`
  - lines showing it: 3-4 missing (-> Trifarian Assessor).
Unsure: Whirling Death has no line to Darius (fine, Darius reads Nexus life).
Must-stay: Whirling Death -> Gnar (makes it strike, its strike effect goes off); Gnar -> Pokey Stick (creates, cheaper); Brothers' Bond -> Darius (more power, Darius is the Overwhelm champion of L18); Gnar -> Mega Gnar (level 2) levels into; Brittle Steel -> Ashe (changes enemy units' stats, levels her).
Read: 751-900

## Piece 7 (lines 901-1050, Ashe LeBlanc rest; Nilah Twisted Fate start)
CAUSE J (L2, what every card does): `Ashe (level 2) -> LeBlanc: helps it level up: damages units or players (levels it up)`. Ashe (level 2) rows only have `attacks by self DO ... <Frostbite>` and `cant ... blocks`; no damage in its text. L2 names this exact pair: "Ashe -> LeBlanc: no line". Lines showing it: 1. (Compare `Bloody Business -> LeBlanc`: its text strikes, a real damage line; and Ashe -> LeBlanc is absent while Ashe (level 2) -> LeBlanc is there, so the two levels disagree.)
CAUSE H confirmed: Mirror Image (2 partners, only LeBlanc and LeBlanc (level 2) as users) has no outgoing line; it `copy chosen mine unit in board in board`, so it should reach the "when I'm summoned" cards (see piece 6).
CAUSE I support: `Yadulski Snowdog` (1 partner, only Incisive Tactician) `Attack: stat_change 2 top mine card in deck (+1|+1)` has no line to Trifarian Assessor (counts power 5+).
Unsure: Nilah (level 1) -> Slipstream (`create 6 random mine card in deck <Slipstream>`) not seen, but Nilah (level 2) -> Slipstream is.
Must-stay: Incisive Tactician -> Ashe (makes it attack, it levels from what it then does); Bloody Business -> Whispered Words (makes cheaper: makes units strike); Troll Chant -> Ashe (changes enemy units' stats); Twisted Fate -> Gold Card (casts its skill); Eye Of The Storm -> Wizened Helmsman (an Elemental it counts).
Read: 901-1050

## Piece 8 (lines 1051-1230, Nilah Twisted Fate rest; Janna Nilah start)
CAUSE B again (L10, one act said twice): `Ruined Rex -> Cannon Barrage: puts it into play: plays; also casts its skill` (Rex row: `play_card random enemy unit in board <Cannon Barrage>`; one play, said as "plays" and "casts its skill"). Compare `Twisted Fate -> Gold Card: puts it into play: casts its skill` and `Annie -> Molten Shield: ... casts its skill` (said once). Lines showing it here: 1.
Unsure:
- Gotcha! (`WHEN drawn of self DO cost_change self (cost=-2)`): 8 lines "Maryam / Pool Shark / Eye Of The Storm / Slipstream / Sunken Temple / Janna / Exalted Cloudwinder / Janna (level 2) -> Gotcha!: makes cheaper: makes you draw cards". Any draw can draw any card (L1/L1b); it is not a cost that drops per draw (Divine Whirlwind, Windborne Mariner are). Doubtful, 8 lines.
- `Eye Of The Storm -> Janna: triggers: makes you draw cards` has no "helps it level up" next to it; Janna's level-up counts cost-reduced cards played and her own draw trigger reduces the drawn card's cost.
Must-stay: Eye Of The Storm -> Divine Whirlwind (cost drops per draw this round); Divine Whirlwind -> Janna (cost change levels her); Eye Of The Storm -> Ruined Rex (draws count for its repeat); Vikrash the Exuberant -> Slipstream (creates); Maryam -> Nilah (draws level her).
Read: 1051-1230

## Piece 9 (lines 1231-1411, Janna Nilah rest; Rally Elusives, Zed Poppy)
CAUSE B again (L10, the same act said two or three times):
  - `Golden Aegis -> Poppy: helps it level up: another attack (levels it up); also makes it attack for its effect (levels it up); also triggers: makes it attack for its effect` (Golden Aegis rows: Barrier then `gain_attack_token`; one Rally said 3 times; same as Blood in the Water -> Rek'Sai)
  - `Ghost -> Zed: helps it level up: helps it hit the enemy player (levels it up); also gives keyword: can give it Elusive` (Ghost's only act is giving Elusive; Zed (level 1) rows do not use a keyword given; one reason said twice). Lines: 1
CAUSE K (missed line, L18 "reads its power"): Poppy and Poppy (level 2) read their own power (`stat_change all mine unit in board [power le stat power of (self)]`), and the power helpers link only to Zed.
  - `Sharpsight -> Zed: makes stronger: more health; also more power` and `Twin Disciplines -> Zed ...`, `Young Witch -> Zed: makes stronger: more power`, `For Demacia! -> Zed ...`: each has no line to Poppy or Poppy (level 2), while `Poppy -> Zed` exists. Sharpsight, Twin Disciplines and Young Witch have exactly 2 partners (Zed, Zed (level 2)).
  - lines showing it: about 8 missing (4 helpers x 2 Poppy cards). Medium confidence.
Unsure:
- Ghost -> Zed (level 2): Zed (level 2) `copy_keywords it to self [state is positive]` uses its own keywords, so a given Elusive may count; absent.
- `Janna -> Nilah: helps it level up: makes you draw cards`: Janna (level 1) rows show no draw act (only `give_ability mine player <Updraft>`); depends on Updraft's entry.
Must-stay: Zed -> Living Shadow (summons); Zed -> Fleetfeather Tracker (puts your units into play); Vanguard Sergeant -> For Demacia! (creates); Ghost -> Zed "helps it hit the enemy player" (Elusive, L20); Poppy -> Poppy (level 2) levels into.
Read: 1051-1411

## Summary of causes (11)
A Soul Harvest misses the Harrowing line the other kills have (1 line)
B same reason said 2-3 times: power boost "enables" + "makes stronger" (Lurk cards -> Xerxa'Reth, Chime -> Bard), attacks said 3 times (Blood in the Water -> Rek'Sai, Golden Aegis -> Poppy), "plays; also casts its skill" (Ruined Rex), Ghost -> Zed (about 22 lines)
C stat help aimed at the Lurker kind linked to Lurkers that do not read power, incl. Overwhelm/Fearsome/Quick Attack/level-up-by-damage cards (about 17 lines)
D strikes now (Bone Skewer, Frenzied Feast, Jaull-fish) have no line to Pyke's damage level-up (3 lines)
E creating a kind into hand/deck is called "makes a Lurker it asks for" (3 lines)
F Esmus -> Chime (plants) missing in Bard Norra (1 line)
G Overwhelm alone said as both "damages the enemy player" and "helps it hit the enemy player" (7 lines)
H Mirror Image (copy into play) has no line to summon-effect cards (4 lines)
I power boosts have no line to cards that count units with power 5+ (Trifarian Assessor) (3-4 lines, medium)
J Ashe (level 2) -> LeBlanc: attacking is what every card does (L2 names this pair) (1 line)
K power helpers skip Poppy cards that read their own power (about 8 lines, medium)

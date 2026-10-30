# Magic: The Gathering

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: physical trading card game (Wizards of the Coast, 1993); players start at 20 life.
- Mana: one land per turn; lands and other sources make mana in five colours (white, blue, black, red, green) plus colourless.
- Turn: untap, upkeep, draw, main phase, combat (attack, the defender blocks), second main phase, end.
- Stack: spells and abilities resolve last-in first-out; instants and abilities can answer at almost any time.
- Card types: creatures, instants, sorceries, enchantments, artifacts, planeswalkers, battles, lands.
- Win: reduce the opponent to 0 life, 10 poison counters, or make them draw from an empty library.
- Specific: colour identity is the faction; most decks use one to three colours.

## Sources and notes

Sources:
[1] https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021 (each mechanic as primary, secondary or tertiary
    in a color; tertiary = appears only occasionally, used here as splash)
[2] https://edhrec.com/articles/foundations-choosing-your-color (strategies each color supports)
[3] https://edhrec.com/combos/early-game-2-card-combos
[4] https://edhrec.com/combos/ur/2905-4702
[5] https://edhrec.com/combos/boros/618-1090
[6] https://edhrec.com/combos/jeskai/142-2781
[7] https://commanderspellbook.com/combo/1295-2503-2726

Colorless: [1] has no colorless list; no faction cases. Multicolor pairs are not measured factions.

## Factions

### White
*Claude:* Order: small creatures, life gain, mass removal and taxes.
Primary: +1/+1 counters and team pumps; token generation; life gain, lifelink; first strike, double strike, flying, vigilance;
protection, indestructible; destroy all creatures; Pacifism-like effects; tapping creatures; taxing; flicker; reanimation;
exiling (Banisher Priest) [1].
Tertiary: card draw, counterspell, drain life, extra attack, hexproof, trample, casting spells from the graveyard [1].
Strategies: small creatures working together (tokens, +1/+1 counters), rules-changing effects, fair mass removal [2].

### Blue
*Claude:* Knowledge: counterspells, card draw, flyers and bouncing.
Primary: card draw, filtering, scry; counterspells; can't be blocked, flying; freeze, lockdown; return to hand; milling;
permanently copying and stealing; Time Walk; hexproof; instant/sorcery triggers; untapping; transformation [1].
Tertiary: +1/+1 counters, trample, protection, Treasure creation [1].
Strategies: countering spells, card draw, library manipulation; weak at destroying cards on the battlefield [2].

### Black
*Claude:* Ambition: removal, sacrifice, the graveyard and paying life.
Primary: destroying creatures; deathtouch; -N/-N; discard as cost and effect; drain life, lifelink; life loss as a cost;
sacrifice; forced sacrifice; reanimation, returning creatures to hand, casting from graveyards; rewards for death; tutoring for
any card; menace; can't block [1].
Tertiary: first strike, permanently stealing, trample, protection [1].
Strategies: graveyard recursion and reanimation, creature removal, sacrifice, life drain [2].

### Red
*Claude:* Freedom: burn, haste, aggression and chaos.
Primary: damage to creatures, planeswalkers and players, to several targets; haste; +N/+0; double strike, first strike, extra
attack; forced attack, must attack; temporary copying and stealing; spell copying; random destruction; polymorph; can't block;
temporary mana; impulsive draw [1].
Tertiary: +1/+1 counters, card draw, Time Walk, protection [1].
Strategies: damage to creatures and players, chaotic random play, haste, stealing creatures [2].

### Green
*Claude:* Nature: ramp, big creatures, trample and fight.
Primary: +1/+1 counters; token generation; mana production, extra lands; trample, reach; fight; life gain; putting creatures
from hand onto the battlefield; tutoring for creatures and lands; untapping; returning cards from graveyard to hand [1].
Tertiary: flying, casting from the graveyard, protection [1].
Strategies: mana ramp and mana creatures, big monsters with trample; can't usually kill creatures outside combat [2].

## Combos
- Sanguine Bond + Exquisite Blood; Vito, Thorn of the Dusk Rose + Exquisite Blood; Sanguine Bond + Bloodthirsty Conqueror:
  life gain and life loss loop [3]
- Demonic Consultation / Tainted Pact + Thassa's Oracle: exile the library, win [3]
- Dramatic Reversal + Isochron Scepter: infinite mana [3]
- Gravecrawler + Phyrexian Altar: infinite death triggers [3]
- Dualcaster Mage + Twinflame: infinite creature tokens [3]
- Curiosity + Niv-Mizzet, Parun: infinite draw and damage [3]
- Basalt Monolith + Forsaken Monument: infinite colorless mana [3]
- The Gitrog Monster + Dakmor Salvage: infinite self-mill [3]
- Splinter Twin + Pestermite; Kiki-Jiki, Mirror Breaker + Restoration Angel; Saheeli Rai + Felidar Guardian: infinite hasty
  tokens [4][5][6]
- Inverter of Truth + Thassa's Oracle: win the game [7]

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name: name|expected concept|wording on the cards. Checked with coverage.py --mechanics (not yet run).
# Sources (21 Oct 2026): magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021 (primary/secondary/tertiary per colour),
# edhrec.com/articles/foundations-choosing-your-color, edhrec.com/combos/early-game-2-card-combos.
flying|evasion|\bflying\b
can't be blocked|evasion|\bcan't be blocked\b
menace|evasion|\bmenace\b
first strike|first_strike|\bfirst strike\b
double strike|multi_attack|\bdouble strike\b
trample|excess_damage|\btrample\b
deathtouch|deathtouch|\bdeathtouch\b
lifelink|lifesteal|\blifelink\b
haste|haste|\bhaste\b
vigilance|untap|\bvigilance\b
hexproof|immunity|\bhexproof\b
ward|immunity|\bward\b
protection|protection|\bprotection from\b
indestructible|cheat_death|\bindestructible\b
defender|cant_attack|\bdefender\b
reach|blocking|\breach\b
flash|reactions|\bflash\b
can't block|cant_block|\bcan't block\b
scry|selection|\bscry \d+\b
counter target spell|counter_spell|\bcounter target\b
draw cards|draw|\bdraw (a|\d+|two|three) cards?\b
return to hand (bounce)|bounce_enemy|\breturn target [a-z ]{0,30} to its owner's hand\b
mill|mill|\bmills?\b
gain control|steal|\bgain control of\b
copy|copy|\bcopy of\b
extra turn|extra_turn|\bextra turn\b
tap creatures|disable|\btap target creature\b|\bdoesn't untap\b
+1/+1 counters|stat_gain|\+1/\+1 counters?\b
-N/-N|stat_loss|\b-\d+/-\d+\b
tokens|summon|\bcreate [a-z0-9 ,/]{0,40}tokens?\b
life gain|heal|\byou gain \d+ life\b
destroy creatures|destroy|\bdestroy target creature\b
destroy all creatures|board_wipe|\bdestroy all creatures\b
exile|banish|\bexile target\b
sacrifice|sacrifice|\bsacrifice (a|an|another) \b
discard (opponent)|hand_disruption|\b(target|each) (player|opponent) discards\b
reanimation|revive|\breturn target creature card from your graveyard to the battlefield\b
tutor|tutor|\bsearch your library\b
damage to any target|damage|\bdeals? \d+ damage\b
must attack|forced_attack|\battacks each (combat|turn) if able\b
fight|attack_now|\bfights?\b
extra land and mana|resource_gain|\badd \{[wubrgc]\}|\bplay an additional land\b
flicker|blink|\bexile [a-z ]{0,30}, then return (it|that card) to the battlefield\b
taxes|cost_increase|\bcosts? \{\d\} more\b
# term: The colour pie sorts every mechanic as primary, secondary or tertiary in each colour; tertiary means it appears only occasionally (magic.wizards.com Mechanical Color Pie 2021).
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	White	buff	+1/+1 counters and team pumps	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	White	summon	token generation	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	White	heal	life gain	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	White	lifesteal	lifelink	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	White	first_strike	first strike and double strike	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	White	evasion	flying	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	White	protection	protection, indestructible	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	White	board_wipe	destroy all creatures	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	White	attack_lock	Pacifism-like effects	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	White	cost_increase	taxing	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	White	blink	flicker	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Blue	draw	card draw	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Blue	selection	filtering and scry	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Blue	counter_spell	counterspells	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Blue	evasion	can't be blocked, flying	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Blue	disable	freeze and lockdown	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Blue	bounce_enemy	return to hand	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Blue	mill	milling	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Blue	copy	copying permanents and spells	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Blue	steal	permanently stealing permanents	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Blue	extra_turn	Time Walk	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Blue	on_spell	instant and sorcery triggers	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Black	destroy	destroying creatures	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Black	deathtouch	deathtouch	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Black	stat_loss	-N/-N	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Black	hand_disruption	discard as an effect	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Black	life_payment	life loss as a cost	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Black	sacrifice	sacrifice its own creatures	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Black	revive	reanimation	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Black	other_death_trigger	rewards for death	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Black	tutor	tutoring for any card	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Black	lifesteal	drain life, lifelink	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Red	direct_damage	damage to players	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Red	aoe_damage	damage to several targets	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Red	haste	haste	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Red	temporary_buff	+N/+0	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Red	multi_attack	double strike, extra attack	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Red	forced_attack	forced attack, must attack	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Red	random_effect	random destruction, chaotic play	https://edhrec.com/articles/foundations-choosing-your-color
signature	Red	steal	temporary stealing	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Red	cant_block	can't block	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Green	stat_gain	+1/+1 counters	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Green	summon	token generation	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Green	resource_gain	mana production, extra lands	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Green	excess_damage	trample	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Green	tutor	tutoring for creatures and lands	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Green	free_play	creatures from hand onto the battlefield	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
signature	Green	heal	life gain	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
archetype	White	swarm	small creatures, tokens, team pumps	https://edhrec.com/articles/foundations-choosing-your-color
archetype	Blue	control	counterspells, card draw	https://edhrec.com/articles/foundations-choosing-your-color
archetype	Blue	card_advantage	card draw, library manipulation	https://edhrec.com/articles/foundations-choosing-your-color
archetype	Black	graveyard	graveyard recursion and reanimation	https://edhrec.com/articles/foundations-choosing-your-color
archetype	Black	sacrifice	sacrifice, rewards for death	https://edhrec.com/articles/foundations-choosing-your-color
archetype	Black	control	creature removal	https://edhrec.com/articles/foundations-choosing-your-color
archetype	Red	burn	damage to creatures and players	https://edhrec.com/articles/foundations-choosing-your-color
archetype	Red	chaos	random card play	https://edhrec.com/articles/foundations-choosing-your-color
archetype	Red	aggro_tempo	haste	https://edhrec.com/articles/foundations-choosing-your-color
archetype	Green	ramp	mana ramp and mana creatures	https://edhrec.com/articles/foundations-choosing-your-color
splash	White	draw	card draw is tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	White	counter_spell	counterspell is tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	White	immunity	hexproof is tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	White	excess_damage	trample is tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	White	cast_from_zone	casting from the graveyard is tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	Blue	stat_gain	+1/+1 counters are tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	Blue	excess_damage	trample is tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	Black	first_strike	first strike is tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	Black	steal	permanently stealing is tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	Black	excess_damage	trample is tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	Red	stat_gain	+1/+1 counters are tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	Red	draw	card draw is tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	Red	extra_turn	Time Walk is tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	Green	evasion	flying is tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
splash	Green	cast_from_zone	casting from the graveyard is tertiary	https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021
combo	Sanguine Bond	Exquisite Blood	life gain and life loss loop	https://edhrec.com/combos/early-game-2-card-combos
combo	Vito, Thorn of the Dusk Rose	Exquisite Blood	life gain and life loss loop	https://edhrec.com/combos/early-game-2-card-combos
combo	Sanguine Bond	Bloodthirsty Conqueror	life gain and life loss loop	https://edhrec.com/combos/early-game-2-card-combos
combo	Demonic Consultation	Thassa's Oracle	exile the library, win	https://edhrec.com/combos/early-game-2-card-combos
combo	Tainted Pact	Thassa's Oracle	exile the library, win	https://edhrec.com/combos/early-game-2-card-combos
combo	Dramatic Reversal	Isochron Scepter	infinite mana	https://edhrec.com/combos/early-game-2-card-combos
combo	Gravecrawler	Phyrexian Altar	infinite death triggers	https://edhrec.com/combos/early-game-2-card-combos
combo	Dualcaster Mage	Twinflame	infinite creature tokens	https://edhrec.com/combos/early-game-2-card-combos
combo	Curiosity	Niv-Mizzet, Parun	infinite draw and damage	https://edhrec.com/combos/early-game-2-card-combos
combo	Basalt Monolith	Forsaken Monument	infinite colorless mana	https://edhrec.com/combos/early-game-2-card-combos
combo	The Gitrog Monster	Dakmor Salvage	infinite self-mill	https://edhrec.com/combos/early-game-2-card-combos
combo	Splinter Twin	Pestermite	infinite hasty tokens	https://edhrec.com/combos/ur/2905-4702
combo	Kiki-Jiki, Mirror Breaker	Restoration Angel	infinite hasty tokens	https://edhrec.com/combos/boros/618-1090
combo	Saheeli Rai	Felidar Guardian	infinite hasty tokens	https://edhrec.com/combos/jeskai/142-2781
combo	Inverter of Truth	Thassa's Oracle	win the game	https://commanderspellbook.com/combo/1295-2503-2726
```

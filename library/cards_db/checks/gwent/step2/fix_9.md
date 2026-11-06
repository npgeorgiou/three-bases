# Fix 9 (gwent, verify3.md: The Virtuoso -> The Witness lost)
Cause: fix_8's rule compared the named cards' category with the need's kind directly, so Lotus Trap (category ability, a Skill) was not a spell.
Fix: network.py main match loop, the fix_8 line now asks `matches(c, game, card, tkind, tw)`, the code's own test of whether a card fits a kind and its filters (`matches` lets an ability fit "spell" when the need says "spells or Skills").
Kaer Seren -> Keldar, Uprising -> Keldar: named units fail `matches` for kind spell: still no line.
The Virtuoso -> The Witness: Lotus Trap fits through the skill rule: line returns.
Same for every game. network.py parses. Not run: load.py, links.py.

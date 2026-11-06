FIXED: Vrygheff repeats turn_end effects, so a repeat that names an event now goes only to cards with an effect on that event. Files: network.py, cases/network.tsv. Cases: n618, n619, n620.
Only the Vrygheff repeat (event=turn_end) is known to carry an event param in the repeat acts of any game.
Other games with a repeat that has event= (Monster Train, others) get the same filter; checked only for gwent.

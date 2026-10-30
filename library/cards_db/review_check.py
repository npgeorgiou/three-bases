"""review_check.py <game>: Kaptain's deck checks are fixed by cause, not by example.

deck_read_<game>.md lists every wrong or missing line as families, each a section headed "## F<n> <name>" (other
sections are free). Each family must say:
  Root cause:            which rule or reading made the wrong line (file and rule), in one or two lines
  Same error elsewhere:  what the same cause does in this game's other decks and in every other game (counts, examples),
                         or why it cannot happen there
  Fix:                   the rule that replaced it, for every card of every game
A family without these three lines fails the build: it is the sign of a fix made for one card (PROCESS.md, "Fixing a review").
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEED = ('Root cause:', 'Same error elsewhere:', 'Fix:')


def main():
    game = sys.argv[1]
    path = os.path.join(HERE, f'deck_read_{game}.md')
    if not os.path.exists(path): print(f'no deck_read_{game}.md yet'); return
    text = open(path, encoding='utf-8').read()
    fams = [f for f in re.split(r'\n(?=## )', text)[1:] if re.match(r'## F\d+', f)]
    if not fams: print(f'deck_read_{game}.md has no families ("## F1 <name>")'); sys.exit(1)
    bad = [f.splitlines()[0][3:] for f in fams if not all(re.search(r'(^|\n)\s*-?\s*\**' + re.escape(n), f) for n in NEED)]
    if bad:
        print(f'{len(bad)} of {len(fams)} families lack ' + ' / '.join(NEED) + ': ' + '; '.join(bad))
        sys.exit(1)
    print(f'{len(fams)} families, each with root cause, same error elsewhere and fix')


main()

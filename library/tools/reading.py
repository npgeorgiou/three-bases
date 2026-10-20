"""How wording patterns read an entry's text, in one place: lower case, without reminder text (the words in parentheses that
explain a keyword) for the games whose cards print it, and with the entry's own name written as 'name'."""
import re
NO_REMINDER = {'mtg', 'lorcana', 'swu'}   # cards that print reminder text; the keyword brings its own concepts
def strip(game, low): return re.sub(r'\([^()]*\)', ' ', low) if game in NO_REMINDER else low

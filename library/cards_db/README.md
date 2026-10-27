# Card database (what cards do, as a network)

Each card is described as abilities: an event (when), conditions (if) and effects (do). Every field is a value from
`vocab.tsv`, a number, or a link (id) to another card, keyword or type. No free text. The reader records in `read/<game>/`
are the source; `cards.sqlite` is rebuilt from them.

| File | What it is |
|---|---|
| `BRIEF.md` | The record shapes, reading rules and approved examples (what readers follow) |
| `vocab.tsv` | Every allowed value per field, its meaning, its concept-tree concept, and (for effects) the events it causes |
| `build_input.py` | Cards to read, cut into batches by amount of text; keyword-only cards get an empty record directly |
| `check.py` | Checks records against the shapes and values and resolves names to ids |
| `load.py` | Builds `cards.sqlite` from the records |
| `input/<game>/` | Reader input batches |
| `read/<game>/` | Reader output: one JSON record per card (the source of truth), plus proposals for new values |
| `CHANGES.md` | Every change to the shapes or values, with the card that caused it |

Tables in `cards.sqlite`: card, type, card_type, card_keyword, card_link (levels into, generates), ability, event, cond,
effect, param, target, filter, amount, keyword_trigger, unsure, vocab, causes (which effect causes which event: the join for
connections).

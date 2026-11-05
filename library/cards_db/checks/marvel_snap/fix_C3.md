FIXED: Repeating a keyword gave a line to cards with that keyword but no effect, and protection by cost was treated as a narrow deck choice, so it reached cards that do not use it. Files: network.py. Cases: n426, n427, n428.
- Repeat with a keyword filter now needs the card to have own effect rows (other games' keyword-only cards lose repeat lines too).
- A "cant" (protect) aimed by cost now needs the target's text to use it (L14); other games' cost-filtered protections change too.
- Checked with pair.py: both wrong examples now NONE, Joaquin Torres Falcon II -> Electro stays.

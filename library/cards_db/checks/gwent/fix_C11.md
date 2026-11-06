FIXED: Armor and Vitality given to a tribe or kind (health-like help) now link only to cards whose text uses them (L14, L18), as stats already did. Files: network.py (aimed, new line before the increase_effect sharp rule), cases/network.tsv. Cases: n621-n626.
Other games: any give_keyword of a DEFENCE_KW keyword (shield, armor, regeneration, immunity...) with a kind or tribe filter loses its blanket lines to cards that do not use it (Monster Train, Slay the Spire, etc.).
Checked with pair.py: all 5 wrong examples now NONE, Witch Hunter -> Vigilantes stays.

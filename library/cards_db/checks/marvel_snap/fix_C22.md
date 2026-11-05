FIXED: Absorbing Man's need for an On Reveal unit played before it now gets a line from every On Reveal card (an earlier fixer's network.py change, site 1866; Wong already right); I only checked and added cases. Files: cases/network.tsv. Cases: n497-n501.
pair.py: Brood, Silver Surfer, Hazmat, Magik -> Absorbing Man all show "is a unit with On Reveal it counts or asks for"; Wong -> Absorbing Man still "plays it again".
No code or data changed by me.
Same last_card rule touches other games' "if the last card played was X" needs.

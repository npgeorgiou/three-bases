FIXED: The flood line (a card that stops cards being played -> a summoner) was made for every play block; it now needs a total, unconditional flood of the place (no cost filter, no one side, not other lanes, no IF). Files: network.py, cases/network.tsv. Cases: n525-n529.
- Goose (cost 3+ only), Jean Grey (other lanes, conditional) and Invisible Woman & Namor Doomsday (enemy only, conditional) lost their lines; Storm -> White Tiger and Doctor Doom stay (cms07, cms08).
- Other blockers with a total flood (Flooded, Flooding, Professor X, Storm) keep lines to summoners in all games using flood_lines; Marvel Snap locations with an IF (The Vault) lose it.
- Fix came from C26 (d10a545), which made flood_lines too wide.

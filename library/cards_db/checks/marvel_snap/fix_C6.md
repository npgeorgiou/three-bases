FIXED: In Marvel Snap a lane is a location, so a card that acts "in its lane" (Danger) no longer waits for a move, and moving a unit gives it no line. Files: network.py (line 626 skip in the need loop, generic_use skip of lane-move needs), cases/network.tsv. Cases: n439-n443.
Ghost-Spider -> Drax, Blink -> Moonstone, Doctor Octopus -> Pizza Slice were already NONE from earlier fixers; Angel -> Hydra Stomper stays.
The change is limited to game marvel_snap and filter "position is same_lane"; other games are untouched.
Any other Marvel Snap card with a same_lane filter (kill or act in its lane) also loses a moves line.
No records, refs.py or flat.py changed; pair.py showed the result at once.

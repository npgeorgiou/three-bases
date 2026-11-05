FIXED: A create with no side named fed a need about the ENEMY side (Gorgon counts enemy created cards); now only an enemy-side maker does. Files: network.py, cases/network.tsv. Cases: n447-n450.
Other examples (Doctor Octopus -> Dagger, Aero -> Armor) were already fixed by earlier fixers; Moira X -> Quinjet stays.
The new skip applies to every game: a "created" maker with no side never feeds an enemy-side need.

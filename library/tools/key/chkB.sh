#!/bin/bash
# helper for reader B set 2: check a game's B folder with notkw moved aside
cd /home/claude/three-bases/library/tools/key
g=$1; f=kw_$g/B/notkw.json
[ -f $f ] && mv $f kw_$g/notkwB.tmp
python3 key.py check kw_$g B
[ -f kw_$g/notkwB.tmp ] && mv kw_$g/notkwB.tmp $f

#!/bin/bash
# fixdone.sh <game> <report> (e.g. marvel_snap fix_C3): adds the report's first word to the "7. Fixers" line of
# checks/<game>/PROGRESS.md, commits every changed file of the database with the report's first line, and pushes.
cd "$(dirname "$0")"; D=checks/$1; R=$D/$2.md
st=$(head -1 "$R" | cut -d: -f1)
python3 -c "
import sys; p='$D/PROGRESS.md'; s=open(p).read(); i=s.index('7. Fixers'); j=s.index('\n', i)
s=s[:j]+' ${2#fix_} $st;'+s[j:]; open(p,'w').write(s)"
git add -A . && git commit -qm "$1 fixer ${2#fix_}: $(head -1 "$R" | cut -c1-150)" && (git push -q 2>/dev/null || (git pull -q --rebase && git push -q))
git log --oneline -1 | cut -c1-80

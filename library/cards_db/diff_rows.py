"""diff_rows.py <diff.txt> <out.txt>: a dump_lines.py --diff with each group's example pairs' rows added (when / if / do, as
causes.py prints them), so a line reader can judge gone and new lines by the rows (START_DATABASE.md Part 3 step 8)."""
import re, sys
sys.argv, args = sys.argv[:1] + ['--out', '/dev/null'], sys.argv[1:]
import causes
src, out = args
sec, o = '', open(out, 'w', encoding='utf-8')
o.write('Each group: GONE = lines the fixes removed (wrong if the line was right: a MISSED CAUSE), NEW = lines the fixes added\n'
        '(a CAUSE if wrong). Rows of the first example pairs follow each group.\n\n')
for line in open(src, encoding='utf-8'):
    o.write(line)
    if line.strip() in ('GONE', 'NEW'): sec = line.strip()
    m = re.match(r'\s*\d+ (\w+) \| [^|]+ \| [^|]+ \| (.*)$', line)
    if not m or not sec: continue
    game, seen = m.group(1), set()
    for a, b in re.findall(r'(?:^|; )(.+?) -> (.+?) \(', m.group(2))[:2]:
        for name in (a, b):
            n, ids = causes.ids(name)
            for i, g in ids:
                if g == game and i not in seen:
                    seen.add(i); o.write(f'  {n}:\n' + ''.join(f'    {r[:200]}\n' for r in causes.rows(i)))

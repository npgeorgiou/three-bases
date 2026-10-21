import json
yes = set("""4986
3792 3793 5349
6571 6572 6573 6574 6575 6576 6577 6578 6579
4890
2389
2856 2857 2858 2859 2860 2861 2862 2864 2865
8007
4121 4122""".split())
qids = []
for line in open('/home/claude/three-bases/library/tools/step3/judge/r038.txt'):
    if line[:1].isdigit():
        qids.append(line.split('|')[0].strip().rstrip('*'))
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open('/home/claude/three-bases/library/tools/step3/judge/A/r038.json','w'), indent=0)
print(len(qids), sum(v=="yes" for v in out.values()))

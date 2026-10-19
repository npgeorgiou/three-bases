import json
yes = set("""3796 3798 3800 3802 3803 5350
6590 6591 6592 6593 6594 6595 6596 6597 6598 6599 8818 8819
4248 4249 4250 4251 4252 4254
2396
936 937 938 939 940 942 943 944 945
3519 3520
2870
4130 6207
748 749 4486
6621
4485
1223 1224 1225 1226 1227 1231 1232
1517 2688 2697 4035""".split())
qids = []
for line in open('/home/claude/three-bases/library/tools/step3/judge/r041.txt'):
    if line[:1].isdigit():
        qids.append(line.split('|')[0].strip().rstrip('*'))
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open('/home/claude/three-bases/library/tools/step3/judge/A/r041.json','w'), indent=0)
print(len(qids), sum(v=="yes" for v in out.values()))

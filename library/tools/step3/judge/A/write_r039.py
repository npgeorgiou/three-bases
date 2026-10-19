import json
yes = set("""5825 5826 5827 5828 5829 5830 7079 7080 7081 7082 7083 7084
3712 3713 3714 3715 3716 3717 3719 3720
8247
736 737
6178 6179
8308 8309
7317 7318 7319 7320 7321 7322 7323 7324 7325 7326
5093 5094 5095 5096 5097 5098 5099 5100
2447 2448 2453 2454 2455 2681""".split())
qids = []
for line in open('/home/claude/three-bases/library/tools/step3/judge/r039.txt'):
    if line[:1].isdigit():
        qids.append(line.split('|')[0].strip().rstrip('*'))
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open('/home/claude/three-bases/library/tools/step3/judge/A/r039.json','w'), indent=0)
print(len(qids), sum(v=="yes" for v in out.values()))

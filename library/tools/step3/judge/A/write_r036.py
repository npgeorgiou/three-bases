import json
yes = set("754 2531 2532 2533 2534 2535 2536 2537 2538 2539 2540 6180 6181 6182 6804 6805 6806 6807 6808 6809 8310 8311 8312 8313 8315 8316 8317 8318 8319 7328 7329 1562 1563 5436 5439 5440 5444 2702 8507 8508 8509 4952 4953 4954 4955 4956".split())
qids = []
for line in open('/home/claude/three-bases/library/tools/step3/judge/r036.txt'):
    if line[:1].isdigit():
        qids.append(line.split('|')[0].strip().rstrip('*'))
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open('/home/claude/three-bases/library/tools/step3/judge/A/r036.json','w'), indent=0)
print(len(qids), sum(v=="yes" for v in out.values()))

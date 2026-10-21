import json
yes = set("""6070 6073 6076 6244 6248
8613 8614 8615 8616 8617 8618 8619 8620 8621 8622
6729 5622 1813 4467 4468 4469 4470 4471 4472 6457 6458
2784 2785 2786 2787 2788 2789 2790 2791 2792 2793 5245
4982 4984
8374 8375 8376 8377 8378 8379 8380 8381 8382 8383""".split())
qids = []
for line in open('/home/claude/three-bases/library/tools/step3/judge/r037.txt'):
    if line[:1].isdigit():
        qids.append(line.split('|')[0].strip().rstrip('*'))
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open('/home/claude/three-bases/library/tools/step3/judge/A/r037.json','w'), indent=0)
print(len(qids), sum(v=="yes" for v in out.values()))

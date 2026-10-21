import json
yes = set("""4036 4037 4038 4039 4040
7576 8530 8531 8532 8533 8534 8535 8536 8537 8538 8539
3614
864 865 866 867 868 869 870 871 872 873 3406 3408 5612 5613 5614 5615 5616 5617 5618 5619 5620 5621
2783
5237 5238 5240 5241 5242 5244
8644""".split())
qids = []
for line in open('/home/claude/three-bases/library/tools/step3/judge/r042.txt'):
    if line[:1].isdigit():
        qids.append(line.split('|')[0].strip().rstrip('*'))
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open('/home/claude/three-bases/library/tools/step3/judge/A/r042.json','w'), indent=0)
print(len(qids), sum(v=="yes" for v in out.values()))

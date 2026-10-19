import json
yes = set("""2145 2620 2621 2622 8391 8392 8393 8394 8395 8396 8397 8398
4283 4284 4285 4286 4287 4288 4289 4290 8151
8497 8498 8499 8500 8501 8502 8503 8504 8505 8506
4942 6059 6060 6062 6063 6064 6066 6239 6240
7381 7388
2781 5234 5235""".split())
qids = []
for line in open('/home/claude/three-bases/library/tools/step3/judge/r040.txt'):
    if line[:1].isdigit():
        qids.append(line.split('|')[0].strip().rstrip('*'))
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open('/home/claude/three-bases/library/tools/step3/judge/A/r040.json','w'), indent=0)
print(len(qids), sum(v=="yes" for v in out.values()))

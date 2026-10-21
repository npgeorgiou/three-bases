import json
yes = {"7908","7909","7910","7911","7912","7913"}
yes |= {str(i) for i in range(6336,6364)}
yes |= {str(i) for i in range(6754,6764)}
yes |= {"7999"} | {str(i) for i in range(8000,8007)}
yes |= {str(i) for i in range(7835,7845)} | {str(i) for i in range(8028,8037)}
yes |= {"1674","4268","4269","4273","4277"}
qids = [l.split("|")[0].strip().rstrip("*") for l in open("/home/claude/three-bases/library/tools/step3/judge/r008.txt") if l.strip() and l[0].isdigit()]
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open("/home/claude/three-bases/library/tools/step3/judge/A/008.json","w"))
print(len(qids), sum(v=="yes" for v in out.values()))

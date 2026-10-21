import json
yes = set()
yes |= {"8972","8973","8974","8975"}
yes |= {"5912","5913","5914","5915","5916","5917","5918","5919","5920"}
yes |= {str(i) for i in range(9030,9040)}
yes |= {str(i) for i in range(5716,5726)}
yes |= {"3166","3167","3168","3170","3171","3172","3173","3174","3175"}
yes |= {"6675","6680","6681","6682","6684"}
yes |= {str(i) for i in range(4148,4158)} | {str(i) for i in range(6216,6226)}
qids = [l.split("|")[0].strip().rstrip("*") for l in open("/home/claude/three-bases/library/tools/step3/judge/r013.txt") if l.strip() and l[0].isdigit()]
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open("/home/claude/three-bases/library/tools/step3/judge/A/013.json","w"))
print(len(qids), sum(v=="yes" for v in out.values()))

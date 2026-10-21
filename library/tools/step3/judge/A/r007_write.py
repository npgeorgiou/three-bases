import json, sys
yes = {"8305","8057","8061","8065","8760","8761","8762","8763","8764","8765","8766","8767","8768","8769"}
yes |= {str(i) for i in range(5880,5890)}
yes |= {str(i) for i in range(3834,3843)}
yes |= {str(i) for i in range(5361,5371)}
yes |= {str(i) for i in range(2263,2273)}
yes |= {"7904","7905","7906","7907"}
qids = [l.split("|")[0].strip().rstrip("*") for l in open("/home/claude/three-bases/library/tools/step3/judge/r007.txt") if l.strip() and l[0].isdigit()]
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open("/home/claude/three-bases/library/tools/step3/judge/A/007.json","w"))
print(len(qids), sum(v=="yes" for v in out.values()))

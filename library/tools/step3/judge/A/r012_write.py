import json
yes = set()
yes |= {str(i) for i in range(6286,6296)}
yes |= {"5633","5634","5635","5637","5638","5639","5640","5641","5642"}
yes |= {str(i) for i in range(8430,8439)}
yes |= {"8340","8341","8342","8343","8345","8346","8347","8348","8349"}
yes |= {"8966","8967","8969","8970","8971"}
qids = [l.split("|")[0].strip().rstrip("*") for l in open("/home/claude/three-bases/library/tools/step3/judge/r012.txt") if l.strip() and l[0].isdigit()]
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open("/home/claude/three-bases/library/tools/step3/judge/A/012.json","w"))
print(len(qids), sum(v=="yes" for v in out.values()))

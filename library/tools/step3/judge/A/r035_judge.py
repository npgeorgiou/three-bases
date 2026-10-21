import json, sys
src = "/home/claude/three-bases/library/tools/step3/judge/r035.txt"
no = {"214","4255","6600","6601","4899","4901","6653","6654","6897","2312","2313","2315","2316","2317","2318","2319","2320","2321","6002","507","508","946","6400","2721","2722","7136","7137","7138","7139","3522","6784","8018","8023","8025","7095","7097","7745","7747","7749","7750","8083","8085","7006","7007","7008","8248","8249","8252","8255","8256","8257"}
qids = []
for line in open(src, encoding="utf-8"):
    if "|" in line and not line.startswith("#"):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 5 and parts[0].rstrip("*").isdigit():
            qids.append(parts[0].rstrip("*"))
ans = {q: ("no" if q in no else "yes") for q in qids}
assert len(ans) == len(qids), "duplicate qids"
out = "/home/claude/three-bases/library/tools/step3/judge/A/r035.json"
json.dump(ans, open(out, "w", encoding="utf-8"), indent=1)
print(len(ans), "answers,", sum(v=="no" for v in ans.values()), "no")

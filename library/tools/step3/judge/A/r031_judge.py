import json, sys
src = "/home/claude/three-bases/library/tools/step3/judge/r031.txt"
no = {"4556","2159","2161","8756","1184","7987","4902","4903","4904","4905","4906","4907","4908","4909","4910","4911","2407","2408","2409","2410","2411","2412","2413","2414","2415","2416","1741","4188","4189","4190"}
qids = []
for line in open(src, encoding="utf-8"):
    if "|" in line and not line.startswith("#"):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 5 and parts[0].rstrip("*").isdigit():
            qids.append(parts[0].rstrip("*"))
ans = {q: ("no" if q in no else "yes") for q in qids}
assert len(ans) == len(qids), "duplicate qids"
out = "/home/claude/three-bases/library/tools/step3/judge/A/r031.json"
json.dump(ans, open(out, "w", encoding="utf-8"), indent=1)
print(len(ans), "answers,", sum(v=="no" for v in ans.values()), "no")

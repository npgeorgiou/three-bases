import json, sys
src = "/home/claude/three-bases/library/tools/step3/judge/r028.txt"
no = {"8809","8935","8067","60","3370","3375","3376","7233"}
qids = []
for line in open(src, encoding="utf-8"):
    if "|" in line and not line.startswith("#"):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 5 and parts[0].rstrip("*").isdigit():
            qids.append(parts[0].rstrip("*"))
ans = {q: ("no" if q in no else "yes") for q in qids}
assert len(ans) == len(qids), "duplicate qids"
out = "/home/claude/three-bases/library/tools/step3/judge/A/r028.json"
json.dump(ans, open(out, "w", encoding="utf-8"), indent=1)
print(len(ans), "answers,", sum(v=="no" for v in ans.values()), "no")

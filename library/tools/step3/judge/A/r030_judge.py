import json, sys
src = "/home/claude/three-bases/library/tools/step3/judge/r030.txt"
no = {"1933","1934","1935","1936","1937","1938","1939","1940","1941","1942","565","8073","8074","8071","71","72","7199","8593","6707","3380","3382","3389","8936","4553"}
qids = []
for line in open(src, encoding="utf-8"):
    if "|" in line and not line.startswith("#"):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 5 and parts[0].rstrip("*").isdigit():
            qids.append(parts[0].rstrip("*"))
ans = {q: ("no" if q in no else "yes") for q in qids}
assert len(ans) == len(qids), "duplicate qids"
out = "/home/claude/three-bases/library/tools/step3/judge/A/r030.json"
json.dump(ans, open(out, "w", encoding="utf-8"), indent=1)
print(len(ans), "answers,", sum(v=="no" for v in ans.values()), "no")

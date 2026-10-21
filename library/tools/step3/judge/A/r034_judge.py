import json, sys
src = "/home/claude/three-bases/library/tools/step3/judge/r034.txt"
no = {"1818","1819","1820","5703","5246","5247","5249","2156","8403","4988","4989","4990","4991","4993","4994","4996","1579","1580","7485","7486","7487","7492","7493","7494","3812","3813","5352"}
qids = []
for line in open(src, encoding="utf-8"):
    if "|" in line and not line.startswith("#"):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 5 and parts[0].rstrip("*").isdigit():
            qids.append(parts[0].rstrip("*"))
ans = {q: ("no" if q in no else "yes") for q in qids}
assert len(ans) == len(qids), "duplicate qids"
out = "/home/claude/three-bases/library/tools/step3/judge/A/r034.json"
json.dump(ans, open(out, "w", encoding="utf-8"), indent=1)
print(len(ans), "answers,", sum(v=="no" for v in ans.values()), "no")

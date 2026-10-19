import json, sys
src = "/home/claude/three-bases/library/tools/step3/judge/r033.txt"
no = {"8327","7330","3936","3937","3938","4487","4488","4489","4490","4491","4492","4493","2567","5445","5446","5447","5448","5449","5450","5451","5452","5453","5454","6313","6314","6315","1036","1037","6730","6731","3617","3618","3619","3620","3621","3622","3623","3624","3625","3626","3420","3422","3423","3424","3425","3426","3427"}
qids = []
for line in open(src, encoding="utf-8"):
    if "|" in line and not line.startswith("#"):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 5 and parts[0].rstrip("*").isdigit():
            qids.append(parts[0].rstrip("*"))
ans = {q: ("no" if q in no else "yes") for q in qids}
assert len(ans) == len(qids), "duplicate qids"
out = "/home/claude/three-bases/library/tools/step3/judge/A/r033.json"
json.dump(ans, open(out, "w", encoding="utf-8"), indent=1)
print(len(ans), "answers,", sum(v=="no" for v in ans.values()), "no")

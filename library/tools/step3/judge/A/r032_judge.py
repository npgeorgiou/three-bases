import json, sys
src = "/home/claude/three-bases/library/tools/step3/judge/r032.txt"
no = {"4192","4193","4194","4195","4196","4197","1888","1889","1890","1891","1892","6168","1980","1981","1982","1983","1984","4137","6137","7752","4371","4372","8258","8260","8261","8262","8264","8267","757","2054","2058","2059","2061","2062","6811","6816","6817","8323"}
qids = []
for line in open(src, encoding="utf-8"):
    if "|" in line and not line.startswith("#"):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 5 and parts[0].rstrip("*").isdigit():
            qids.append(parts[0].rstrip("*"))
ans = {q: ("no" if q in no else "yes") for q in qids}
assert len(ans) == len(qids), "duplicate qids"
out = "/home/claude/three-bases/library/tools/step3/judge/A/r032.json"
json.dump(ans, open(out, "w", encoding="utf-8"), indent=1)
print(len(ans), "answers,", sum(v=="no" for v in ans.values()), "no")

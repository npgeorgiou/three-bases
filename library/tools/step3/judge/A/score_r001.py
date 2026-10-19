import json, re
ans = "4674y 4675y 4676n 6438y 6439y 6440n 6441n 5133y 5134y 5135y 5136y 5137y 5138y 5139y 5140y 5141y 4280y 4281y 4282y 6830y 6831y 6832y 6833y 6834y 3369y 4373y 4374y 4375y 6437y 4548y 4549y 4550y 2588y 4278y 4279y 6829y 2194y 7845y 7955y 7956y 6695y 6696y 3543y 3544y 3545y 3546n 3547y 3548y 442y 447y 795y 797y 4628y 4629y 4630y 3266y 3267y 3268y 3269y 3270y 3271y 3272y 3273y 8872y 8873y 8874y 8933y 8934y 4093y 4094y 4095y 4096y 4097y 4098y 2903y 2904y 2905y 2906n 2907y 2908y"
B = '/home/claude/three-bases/library/tools/step3/judge/'
src = open(B+'r001.txt').read().splitlines()
qids = [re.match(r'^(\d+)\*?\s*\|', l).group(1) for l in src if re.match(r'^\d+\*?\s*\|', l)]
toks = {t[:-1]: ('yes' if t[-1]=='y' else 'no') for t in ans.split()}
assert len(toks) == len(ans.split()), "dup"
missing = [q for q in qids if q not in toks]; extra = [q for q in toks if q not in qids]
assert not missing and not extra, (missing, extra)
out = {q: toks[q] for q in qids}
json.dump(out, open(B+'A/r001.json','w'))
print(len(out), "answers written; yes =", sum(v=='yes' for v in out.values()))

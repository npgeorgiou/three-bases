import json, re
ans = "7333y 7334y 7335y 7336y 7337y 7338y 7339y 7340y 7341y 7342y 5726y 5727y 5728n 5729n 5730y 5731y 5732y 5733n 7213n 7214y 7215n 7216y 7217n 7218y 7219y 7220y 7221y 7222y 4497y 4498y 4499y 4500y 4501y 4502y 4503y 4504y 4505y 4506y 1518y 3888y 5653y 5654y 5655y 5656y 8540n 8541n 8542n 8543n 8544n 8545n 8546n 8547n 4111y 4112y 4113y 4114y 4115y 4116y 4117y 4118y 4119y 4120y 6203y 6204y 6205y 6206y 5525y 5526y 5527y 5528y 5529y 5530y 5531y 5532y 5533y 5534y 2916n 2917n 2918n 2919n"
B = '/home/claude/three-bases/library/tools/step3/judge/'
src = open(B+'r005.txt').read().splitlines()
qids = [re.match(r'^(\d+)\*?\s*\|', l).group(1) for l in src if re.match(r'^\d+\*?\s*\|', l)]
toks = {t[:-1]: ('yes' if t[-1]=='y' else 'no') for t in ans.split()}
assert len(toks) == len(ans.split()), "dup"
missing = [q for q in qids if q not in toks]; extra = [q for q in toks if q not in qids]
assert not missing and not extra, (missing, extra)
out = {q: toks[q] for q in qids}
json.dump(out, open(B+'A/r005.json','w'))
print(len(out), "answers written; yes =", sum(v=='yes' for v in out.values()))

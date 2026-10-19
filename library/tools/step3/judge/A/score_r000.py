import json, re, sys
ans = "7118n 7119n 3488y 3489y 3490y 7077n 7078n 7733n 8068n 8069n 8070n 4757n 4758y 4759y 4760n 4761n 4762n 3022n 3023y 2068y 2069y 2070y 2071n 8778n 8779n 8780n 2551n 2552n 2553y 2554n 2555n 2556n 6306n 6307n 6308n 8586y 7359n 7360n 7361n 7362n 7363n 7364n 7365y 7366n 7367n 7368n 992y 993y 994y 995y 1529n 1530n 1531n 1532n 1533n 1534n 1535n 1536n 4376y 4377y 4378y 4379y 4380n 4381y 4382y 4383y 4384n 4385y 1803n 1804n 1805n 1806n 1807n 1808n 1809n 1810n 1811n 4671y 4672n 4673n"
src = open('/home/claude/three-bases/library/tools/step3/judge/r000.txt').read().splitlines()
qids = [re.match(r'^(\d+)\*?\s*\|', l).group(1) for l in src if re.match(r'^\d+\*?\s*\|', l)]
toks = {t[:-1]: ('yes' if t[-1]=='y' else 'no') for t in ans.split()}
assert len(toks) == len(ans.split()), "dup"
missing = [q for q in qids if q not in toks]; extra = [q for q in toks if q not in qids]
assert not missing and not extra, (missing, extra)
out = {q: toks[q] for q in qids}
json.dump(out, open('/home/claude/three-bases/library/tools/step3/judge/A/r000.json','w'))
print(len(out), "answers written; yes =", sum(v=='yes' for v in out.values()))

import json, re
ans = "2477n 2478y 2479y 2480y 2481y 2482y 1557y 1558y 3899n 2733y 2734y 2735y 4547y 2598n 8208n 8209n 8210n 8211n 8212n 8213n 8214n 8215n 8216n 8217n 8748y 5214y 5215y 5216y 5217y 5218y 5219y 5220y 5221y 5222y 5223y 5371y 5372y 2176n 2177y 2178y 2179n 2180n 2181y 2182n 2183y 2644n 2645y 4083y 4084y 4085y 4086y 4087y 4088y 4089y 4090y 4091y 4092y 4301y 4302y 4303y 4304y 4305y 4306y 4307y 4308y 4309y 4310y 8153y 8154y 8155y 8156y 8157y 5008n 7675y 7676y 7677n 7678y 7679y 7680y 7681y"
B = '/home/claude/three-bases/library/tools/step3/judge/'
src = open(B+'r002.txt').read().splitlines()
qids = [re.match(r'^(\d+)\*?\s*\|', l).group(1) for l in src if re.match(r'^\d+\*?\s*\|', l)]
toks = {t[:-1]: ('yes' if t[-1]=='y' else 'no') for t in ans.split()}
assert len(toks) == len(ans.split()), "dup"
missing = [q for q in qids if q not in toks]; extra = [q for q in toks if q not in qids]
assert not missing and not extra, (missing, extra)
out = {q: toks[q] for q in qids}
json.dump(out, open(B+'A/r002.json','w'))
print(len(out), "answers written; yes =", sum(v=='yes' for v in out.values()))

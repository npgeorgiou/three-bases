import json, re
ans = "2920y 2921n 2922n 2923n 2924y 2925n 8457y 8458y 8459y 8460y 8461y 8462y 8463y 8464y 8465y 8466y 2956y 578y 579n 580n 581n 582y 8075n 8076n 8077y 8078y 6962n 6963n 73y 74y 9067n 9068n 9069n 9070n 9071n 9072n 9073n 9074n 9075n 9076n 7307y 7308y 7309y 7310y 7311y 7312y 7313y 7314n 7315y 7316y 24y 2668y 3302y 3303y 3304n 3305y 3306y 3307y 3308y 3309n 8594y 8595y 7262n 7263n 7264n 7265n 7266n 8228y 8229n 8230n 8231n 8232n 8233n 8234n 8235n 8236n 8237n 8298n 8299n 8300n"
B = '/home/claude/three-bases/library/tools/step3/judge/'
src = open(B+'r006.txt').read().splitlines()
qids = [re.match(r'^(\d+)\*?\s*\|', l).group(1) for l in src if re.match(r'^\d+\*?\s*\|', l)]
toks = {t[:-1]: ('yes' if t[-1]=='y' else 'no') for t in ans.split()}
assert len(toks) == len(ans.split()), "dup"
missing = [q for q in qids if q not in toks]; extra = [q for q in toks if q not in qids]
assert not missing and not extra, (missing, extra)
out = {q: toks[q] for q in qids}
json.dump(out, open(B+'A/r006.json','w'))
print(len(out), "answers written; yes =", sum(v=='yes' for v in out.values()))

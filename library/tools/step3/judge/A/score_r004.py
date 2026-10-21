import json, re
ans = "7811y 7812y 7813y 7989y 7990y 7991y 7992y 7993y 7994y 7995y 7996y 7997y 7998y 5550y 5551y 5552y 5553y 5554y 2936y 2937y 2938y 2939y 2940y 2941y 2942y 2943y 2944y 2945y 8477y 8478y 8479y 8480y 8481y 8482y 8483y 8484y 8485y 8486y 8086n 8087y 8088y 8089n 8090y 8091n 8092n 8093n 8094y 8095n 6968n 6969n 6970n 6971n 6972n 6973n 6974n 6975n 115y 9087n 9088n 9089n 9090n 9091y 9092n 9093n 9094n 9095n 9096n 2102y 2103y 2104y 8268y 8269y 8270y 8271n 8272y 8273y 8274y 8275y 8276y 8277y"
B = '/home/claude/three-bases/library/tools/step3/judge/'
src = open(B+'r004.txt').read().splitlines()
qids = [re.match(r'^(\d+)\*?\s*\|', l).group(1) for l in src if re.match(r'^\d+\*?\s*\|', l)]
toks = {t[:-1]: ('yes' if t[-1]=='y' else 'no') for t in ans.split()}
assert len(toks) == len(ans.split()), "dup"
missing = [q for q in qids if q not in toks]; extra = [q for q in toks if q not in qids]
assert not missing and not extra, (missing, extra)
out = {q: toks[q] for q in qids}
json.dump(out, open(B+'A/r004.json','w'))
print(len(out), "answers written; yes =", sum(v=='yes' for v in out.values()))

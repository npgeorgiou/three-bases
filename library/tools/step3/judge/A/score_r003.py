import json, re
ans = "7682y 7683y 7684y 5744y 5745y 5746y 5747y 5748y 5749y 5750y 5751y 7247n 7248n 7249y 7250n 7251n 7252n 7253n 7254n 7255n 7256n 8288n 8289n 8290n 8291y 8292n 8293n 8294n 8295n 8296n 8297n 8048n 8049y 8050y 8051y 8052y 8053y 8054y 8055n 8056n 8757n 8758n 8759n 9137n 9138n 9139n 9140n 9141n 9142n 9143n 9144n 9145n 9146n 3824y 3825y 3826y 3827y 3828y 3829y 3830y 3831y 3832y 3833y 7894n 7895y 7896y 7897y 7898y 7899y 7900y 7901y 7902y 7903y 7804y 7805y 7806y 7807y 7808y 7809y 7810y"
B = '/home/claude/three-bases/library/tools/step3/judge/'
src = open(B+'r003.txt').read().splitlines()
qids = [re.match(r'^(\d+)\*?\s*\|', l).group(1) for l in src if re.match(r'^\d+\*?\s*\|', l)]
toks = {t[:-1]: ('yes' if t[-1]=='y' else 'no') for t in ans.split()}
assert len(toks) == len(ans.split()), "dup"
missing = [q for q in qids if q not in toks]; extra = [q for q in toks if q not in qids]
assert not missing and not extra, (missing, extra)
out = {q: toks[q] for q in qids}
json.dump(out, open(B+'A/r003.json','w'))
print(len(out), "answers written; yes =", sum(v=='yes' for v in out.values()))

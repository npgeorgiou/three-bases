import json
yes = {"7833","7834","5337",
       "5297","5298","5299","5300","5301","5302","5303","5304","5305","5306",
       "6697","6698","6699","6700","6701","6702","6703","6704","6705","6706",
       "8923","8924","8925","8926","8927","8928","8929","8930","8931","8932",
       "2437","2438","2440","2441","2442","2443",
       "6751",
       "3569","3570","3571","3572","3573","3574","3575","3576"}
qids = [l.split("|")[0].strip().rstrip("*") for l in open("/home/claude/three-bases/library/tools/step3/judge/r010.txt") if l.strip() and l[0].isdigit()]
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open("/home/claude/three-bases/library/tools/step3/judge/A/010.json","w"))
print(len(qids), sum(v=="yes" for v in out.values()))

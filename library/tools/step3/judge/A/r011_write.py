import json
yes = {"3577","3578",
       "6003","6004","6005","6006","6007","6008","6009","6010","6011","6012","9188","9189","9194","9195",
       "5073","5074","5075","5076","5077","5078","5079","5080","5081","5082",
       "6493","6494","6495","6496","6497","6498","6499","6500","6501","6502",
       "7695","7696","7697","7698","7699","7700","7701","7702","7703","7704",
       "7527","7528","7529","7530","7531","7532","7533","7534","7535","7536",
       "7656"}
qids = [l.split("|")[0].strip().rstrip("*") for l in open("/home/claude/three-bases/library/tools/step3/judge/r011.txt") if l.strip() and l[0].isdigit()]
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open("/home/claude/three-bases/library/tools/step3/judge/A/011.json","w"))
print(len(qids), sum(v=="yes" for v in out.values()))

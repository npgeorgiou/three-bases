import json
yes = {"7469","7470","7471","7473","7641","7643","7644","7645","7646","7647","7648","7649","7780",
       "8548","8549","8550","8551","8552","8553","8554","8555","8556","8557",
       "6604","6606","6607","6608","6609","6610","6613","8842","8844","8845","8846","8847","8848",
       "7826","7827","7828","7829","7830","7831"}
qids = [l.split("|")[0].strip().rstrip("*") for l in open("/home/claude/three-bases/library/tools/step3/judge/r009.txt") if l.strip() and l[0].isdigit()]
out = {q: ("yes" if q in yes else "no") for q in qids}
json.dump(out, open("/home/claude/three-bases/library/tools/step3/judge/A/009.json","w"))
print(len(qids), sum(v=="yes" for v in out.values()))

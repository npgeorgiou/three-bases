"""Slay the Spire records, 18 Nov 2026 (v53), wheel probe fixes; safe to run twice.
Cursed Key, Matryoshka, N'loth's Hungry Face (non-boss chest) and Smoke Bomb (non-boss combat): the "non-boss" was lost; the ability now
has the condition it_matches state not boss (the shape of the boss condition on other cards)."""
import glob, json, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE)
def edit(game, fn):
    n = 0
    for P in glob.glob(os.path.join(HERE, "read", game, "*.jsonl")):
        recs = [json.loads(l) for l in open(P) if l.strip()]; ch = False
        for r in recs:
            if fn(r): n += 1; ch = True
        if ch: open(P, "w").write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs))
    return n

IDS = {7000439: 1, 7000485: 0, 7000500: 0, 7000615: 0}
def f(r):
    i = IDS.get(r.get("id"))
    if i is None: return False
    ab = r["abilities"][i]
    if "if" in ab: return False
    ab["if"] = [{"test": "it_matches", "of": {"with": [{"attr": "state", "op": "not", "val": "boss"}]}}]; return True
print(edit("sts1", f), "cards")

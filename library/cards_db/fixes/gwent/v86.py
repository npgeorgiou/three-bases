"""Gwent records, 18 Nov 2026 (v86), roster probe fixes; safe to run twice.
- Stockpile: "each non-Neutral unit on that row" had no target on the Cooldown step: now units of mine on the summoned unit's row, region not Neutral.
- Whoreson Senior: Tribute 3 replaces the single transform: the single transform now holds only when Tribute is not paid (as Blindeye Apothecary);
  the Tribute ability spends 3 and transforms both neighbours."""
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

def stock(r):
    if r.get("id") != 756724: return False
    st = r["abilities"][0]["do"][1]
    if "on" in st: return False
    st["on"] = {"kind": "unit", "side": "mine", "pick": "all", "zone": "board", "with": [{"attr": "position", "op": "is", "val": "same_row", "of": {"pick": "it"}}, {"attr": "region", "op": "not", "val": "Neutral"}]}
    return True
def who(r):
    if r.get("id") != 756854: return False
    ab = r["abilities"][1]
    if "if" in ab: return False
    single, spend, allt = ab["do"]
    allt = dict(allt); allt["link"] = "then"
    r["abilities"][1] = {"when": ab["when"], "if": [{"test": "keyword_condition", "ref": "Tribute", "op": "not"}], "do": [single]}
    r["abilities"].append({"when": ab["when"], "do": [dict(spend, link=None) if False else {k: v for k, v in spend.items() if k != "link"}, allt]})
    return True
print(edit("gwent", stock), "Stockpile;", edit("gwent", who), "Whoreson Senior")

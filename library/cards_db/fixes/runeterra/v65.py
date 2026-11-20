"""Runeterra records, 18 Nov 2026 (v65), roster probe fixes; safe to run twice.
- Flow ("activates at Round Start if you played 2+ spells or skills last round") was keyword_condition Flow, which links to nothing:
  now event_count played spells/skills (mine) ge 2, span last_round (the shape of the 6/12 spells counts, with last_round).
- Curious Shellfolk: "non-champion card" was lost: the event's object is now a non-champion card of mine.
- Restored Sun Disc: "your level 2 Ascended allies are level 3" was a can with no event: now level_up on my Ascended units, permanent."""
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

FLOW = {"test": "event_count", "event": {"event": "played", "actor": {"kind": "player", "side": "mine"}, "object": {"kind": "spell", "with": [{"attr": "category", "op": "in", "vals": ["fast_spell", "slow_spell", "skill"]}]}}, "op": "ge", "n": 2, "span": "last_round"}
def flow(r):
    c = False
    for ab in r.get("abilities", []):
        for i, cd in enumerate(ab.get("if", [])):
            if cd.get("test") == "keyword_condition" and cd.get("ref") == "Flow":
                ab["if"][i] = dict(FLOW); c = True
    return c
def shell(r):
    if r.get("id") != 751433 or "abilities" not in r: return False
    w = r["abilities"][0]["when"]
    if "object" in w: return False
    w["object"] = {"kind": "card", "side": "mine", "with": [{"attr": "category", "op": "not", "val": "champion"}]}; return True
def disc(r):
    if r.get("id") != 796844 or "abilities" not in r: return False
    for ab in r["abilities"]:
        for st in ab["do"]:
            if st.get("act") == "can":
                st.clear(); st.update({"act": "level_up", "on": {"kind": "unit", "side": "mine", "pick": "all", "zone": "board", "with": [{"attr": "type", "op": "is", "ref": "Ascended"}]}, "lasts": "permanent"}); return True
    return False
print(edit("runeterra", flow), "Flow cards;", edit("runeterra", shell), "Shellfolk;", edit("runeterra", disc), "Sun Disc")

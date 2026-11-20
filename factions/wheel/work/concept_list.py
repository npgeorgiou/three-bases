"""A faction's list (factions/START_DESIGN-1-wheel.md step 6.4): every concept with 5+ cards (usable, helpers and out) except
the faction's own concepts, with its score for how strongly it links with them. In each game alone: real links between the
concept's instances and the instances of the faction's concepts (the faction's concepts counted together as one key), against
the links chance alone gives there (the same count as concept_tags.pair_links); the game's score = (real + 1) / (chance + 1); the
score = the average over the games where the concept and the faction's concepts both appear. Beside it: the level
(mechanics_wheel.level of the linked card pairs) and in how many games real cards link them.
Usage (from library/cards_db): python3 ../../factions/wheel/work/concept_list.py -> factions/wheel/work/lists/<letter>.tsv
for every faction of factions/wheel/work/kernel_factions.tsv; kernel_factions.py imports Library and writes the same lists."""
import collections, csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, '..', '..', '..', 'library', 'cards_db')
sys.path.insert(0, DB)
import concept_tags, mechanics_wheel  # noqa: E402


def concept_rows():
    with open(os.path.join(HERE, 'concepts.tsv'), encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))


class Library:
    """per game: the concepts each card counts for, the linked card pairs with the concepts each side made, so that a list
    for any set of concepts is counted in seconds"""

    def __init__(self):
        cwd = os.getcwd(); os.chdir(DB)
        c, games, x, con, pools, _ = mechanics_wheel.setup()
        os.chdir(cwd)
        rows = concept_rows()
        self.listed = [r['concept'] for r in rows if int(r['card_count']) >= 5]
        keys = mechanics_wheel.concepts(con)
        pairs = concept_tags.link_pairs()
        self.games = {}
        for g in games:
            ids = list(pools[g]); idset = set(ids)
            of = {i: {s[0] for s in keys if concept_tags.counts(con[i], g, s[4])} for i in ids}
            dens = sum(1 for a, b in pairs if a in idset and b in idset) / (len(ids) * (len(ids) - 1) / 2)
            plist = []  # (a, b, concepts a's side made, concepts b's side made, linked (ka, kb))
            for (a, b), sides in pairs.items():
                if a in idset and b in idset:
                    on_a, on_b, linked = set(), set(), set()
                    for sa, sb in sides:
                        ka_, kb_ = concept_tags.side_keys(a, sa, g, keys, con), concept_tags.side_keys(b, sb, g, keys, con)
                        on_a.update(ka_); on_b.update(kb_); linked |= {(ka, kb) for ka in ka_ for kb in kb_}
                    plist.append((a, b, on_a, on_b, linked))
            ends, made = collections.Counter(), collections.Counter()
            for a, b, on_a, on_b, _ in plist:
                for i, on in ((a, on_a), (b, on_b)):
                    for k in of[i]: ends[k] += 1; made[k] += k in on
            share = {k: made[k] / ends[k] for k in ends if ends[k]}
            n = collections.Counter(k for i in ids for k in of[i])
            sides = collections.defaultdict(list)  # card -> what its side made, one entry per linked pair
            index = collections.defaultdict(list)  # concept -> per linked pair counting for it: (concepts after it, before it)
            for a, b, on_a, on_b, linked in plist:
                sides[a].append(on_a); sides[b].append(on_b)
                for k in {k for t in linked for k in t}:
                    index[k].append((frozenset(kb for ka, kb in linked if ka == k), frozenset(ka for ka, kb in linked if kb == k)))
            self.games[g] = (ids, of, dens, sides, index, share, n)

    def scores(self, own, only=None):
        """concept -> (score, level, games) for every listed concept not in own (or only those in only)"""
        own = set(own)
        want = [k for k in self.listed if k not in own and (only is None or k in only)]
        per = collections.defaultdict(list); plain = collections.Counter(); seen = collections.Counter()
        for g, (ids, of, dens, sides, index, share, n) in self.games.items():
            fac = [i for i in ids if of[i] & own]
            if not fac: continue
            ends = sum(len(sides[i]) for i in fac)
            made = sum(1 for i in fac for on in sides[i] if on & own)
            obs, linked_pairs = collections.Counter(), collections.Counter()
            for k in want:
                for after, before in index.get(k, ()):
                    x1 = not after.isdisjoint(own)
                    x2 = not before.isdisjoint(own)
                    obs[k] += x1 + x2; linked_pairs[k] += x1 or x2
            sf = made / ends if ends else 0
            nf = len(fac); facset = set(fac)
            for k in want:
                if not n[k]: continue
                both = sum(1 for i in facset if k in of[i])
                exp = (n[k] * nf - both) * dens * share.get(k, 0) * sf
                per[k].append((obs[k] + 1) / (exp + 1))
                plain[k] += linked_pairs[k]; seen[k] += bool(linked_pairs[k])
        return {k: (round(sum(v) / len(v), 3), mechanics_wheel.level(plain[k]), seen[k]) for k, v in per.items()}


def main():
    lib = Library()
    out = os.path.join(HERE, 'lists'); os.makedirs(out, exist_ok=True)
    with open(os.path.join(HERE, 'kernel_factions.tsv'), encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            own = r['concepts'].split(',')
            sc = lib.scores(own)
            with open(os.path.join(out, r['letter'] + '.tsv'), 'w', encoding='utf-8') as w:
                w.write('concept\tscore\tlevel\tgames\n')
                for k, (s, lv, gm) in sorted(sc.items(), key=lambda t: (-t[1][0], t[0])):
                    w.write(f'{k}\t{s}\t{lv}\t{gm}\n')
    print('lists written:', out)


if __name__ == '__main__':
    main()

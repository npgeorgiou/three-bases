"""Switch off old wording patterns that are right less than half the time (asked by Kaptain, 19-20 Oct 2026).
An old wording pattern is switched off in a game when it is right less than half the time there (Kaptain, 20 Oct 2026): on the
answer key where it matches 3+ key entries, else on the judged sample where that has 5+ matches (step3/results.tsv). Removing it
then removes more wrong tags than right ones. Pairs that already have a judged
narrowing in decisions.tsv keep it. A switch-off is a 'narrow' line whose new regex never matches ('(?!)'): pattern_fix.py then
removes the old pattern's tags in that game, except where the entry is known right (key, judged sample, hand review) or another
pattern of the concept still matches. Rewrites the switch-off lines of decisions.tsv; prints counts only. Usage: switch_off.py"""
import collections, csv, os
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, 'decisions.tsv')
lines = open(D, encoding='utf-8').readlines()
keyc = {(l.split('\t')[2], l.split('\t')[1].split('|')[0]) for l in lines if l.startswith('new\t')}
narrowed = {(l.split('\t')[1], g) for l in lines if l.startswith('narrow\t') and not l.rstrip('\n').endswith('\t(?!)') for g in l.split('\t')[2].split(',')}
off = collections.defaultdict(list)
for r in csv.DictReader(open(os.path.join(HERE, 'results.tsv'), encoding='utf-8'), delimiter='\t'):
    k = r['pattern'].split('|')[0]
    kn, kr, sn, sr = int(r['key_n']), int(r['key_right']), int(r['sample_n']), int(r['sample_right'])
    n, right = (kn, kr) if kn >= 3 else (sn, sr) if sn >= 5 else (0, 0)
    if n and right < 0.5 * n and (r['pattern'], r['game']) not in narrowed: off[r['pattern']].append(r['game'])
keep = [l for l in lines if not (l.startswith('narrow\t') and l.rstrip('\n').endswith('\t(?!)')) and not l.startswith('# switch_off')]
i = next((n for n, l in enumerate(keep) if l.startswith('# key_patterns')), len(keep))   # before the new lines
add = ['# switch_off.py: old patterns right less than half the time switched off\n'] + [f'narrow\t{p}\t{",".join(sorted(gs))}\t(?!)\n' for p, gs in sorted(off.items())]
open(D, 'w', encoding='utf-8').writelines(keep[:i] + add + keep[i:])
print('patterns switched off', len(off), 'pattern-game pairs', sum(len(v) for v in off.values()))

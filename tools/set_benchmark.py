#!/usr/bin/env python3
"""Put a Benchmark file from the AI lab ("Make this the Benchmark") into the game.

  python3 tools/set_benchmark.py "<file>.json"

The file holds the values that won the lab's check match against the current Benchmark. This writes them as
BENCH_VALUES in src/game/js/ai/benchmark.js and names them in its header line; then build (tools/build.py), run
node tools/simtest.js (the hash changes: the Benchmark plays differently) and update summary/15.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PART = os.path.join(ROOT, 'src', 'game', 'js', 'ai', 'benchmark.js')


def main():
    data = json.load(open(sys.argv[1], encoding='utf-8'))
    if data.get('kind') != 'benchmark' or not isinstance(data.get('values'), dict):
        sys.exit('not a Benchmark file from the AI lab')
    src = open(PART, encoding='utf-8').read()
    line = 'const BENCH_VALUES = ' + json.dumps(data['values'], separators=(', ', ': ')) + ';'
    src, n = re.subn(r'^const BENCH_VALUES = .*;$', lambda m: line, src, count=1, flags=re.M)
    if n != 1:
        sys.exit('BENCH_VALUES not found in ' + PART)
    src = re.sub(r'THE BENCHMARK: .*', 'THE BENCHMARK: the AI lab\'s ifelse AI with its tuned values ("%s")' % data.get('name', 'lab values'), src, count=1)
    open(PART, 'w', encoding='utf-8').write(src)
    c = data.get('check', {})
    print('Benchmark values written (check match: won %s, lost %s, drawn %s of %s).' % (c.get('won'), c.get('lost'), c.get('drawn'), c.get('games')))


if __name__ == '__main__':
    main()

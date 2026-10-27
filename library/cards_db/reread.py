"""Re-reading of chosen records under the current brief (after values or rules changed), without losing the old readings.
  reread.py make <game> unsure [chars]    input/<game>/fix_NNN.jsonl from every record marked unsure (cut by amount of text)
  reread.py make <game> ids <id,id,...>   the same for listed card ids
  reread.py merge <game>                  for each finished fix_NNN (read/<game>/fix_NNN.jsonl passing check), the new
                                          records replace the old ones in their batch files; the old readings are kept in
                                          replaced/<game>/, the fix output moves to fixes/<game>/ (so load.py sees each card once)
The fix batches are read with READER_PROMPT.md like any batch (BATCH = fix_NNN)."""
import glob, json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))

def records(path): return [json.loads(l) for l in open(path) if l.strip()]

def batch_files(game):
    return [f for f in sorted(glob.glob(os.path.join(HERE, 'read', game, 'batch_*.jsonl'))) if 'proposals' not in f and '.part' not in f]

def make(game, ids, budget):
    inputs = {}
    for f in glob.glob(os.path.join(HERE, 'input', game, 'batch_*.jsonl')):
        for x in records(f): inputs[x['id']] = x
    todo = [inputs[i] for i in sorted(ids) if i in inputs]
    start = len(glob.glob(os.path.join(HERE, 'input', game, 'fix_*.jsonl'))) + 1
    batches, cur, size = [], [], 0
    for x in todo:
        if cur and size + len(x['text']) > budget: batches.append(cur); cur, size = [], 0
        cur.append(x); size += len(x['text'])
    if cur: batches.append(cur)
    for k, b in enumerate(batches, start):
        with open(os.path.join(HERE, 'input', game, 'fix_%03d.jsonl' % k), 'w') as f:
            for x in b: f.write(json.dumps(x) + '\n')
    print(f'{len(todo)} cards in {len(batches)} fix batches starting at fix_{start:03d}')

def merge(game):
    os.makedirs(os.path.join(HERE, 'replaced', game), exist_ok=True); os.makedirs(os.path.join(HERE, 'fixes', game), exist_ok=True)
    for fx in sorted(glob.glob(os.path.join(HERE, 'read', game, 'fix_*.jsonl'))):
        if 'proposals' in fx or '.part' in fx: continue
        name = os.path.basename(fx)[:-6]
        r = subprocess.run([sys.executable, os.path.join(HERE, 'check.py'), game, fx, '--input',
                            os.path.join(HERE, 'input', game, name + '.jsonl')], capture_output=True, text=True)
        if r.returncode: print(name, 'does not pass check: not merged'); continue
        new = {x['id']: x for x in records(fx)}; n = 0
        for bf in batch_files(game):
            old = records(bf); out = []; gone = []
            for x in old:
                if x['id'] in new: gone.append(x); out.append(new[x['id']]); n += 1
                else: out.append(x)
            if gone:
                with open(os.path.join(HERE, 'replaced', game, os.path.basename(bf)), 'a') as f:
                    for x in gone: f.write(json.dumps(x, separators=(',', ':')) + '\n')
                open(bf, 'w').write(''.join(json.dumps(x, separators=(',', ':')) + '\n' for x in out))
        for f in glob.glob(os.path.join(HERE, 'read', game, name + '*')): shutil.move(f, os.path.join(HERE, 'fixes', game, os.path.basename(f)))
        print(name, n, 'records replaced')

if __name__ == '__main__':
    cmd, game = sys.argv[1], sys.argv[2]
    if cmd == 'make':
        if sys.argv[3] == 'unsure':
            ids = {x['id'] for f in batch_files(game) for x in records(f) if x.get('unsure')}
            make(game, ids, int(sys.argv[4]) if len(sys.argv) > 4 else 8000)
        else: make(game, {int(i) for i in sys.argv[4].split(',')}, 8000)
    elif cmd == 'merge': merge(game)

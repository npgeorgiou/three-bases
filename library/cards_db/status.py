"""Where the reading of a game stands, from the files alone (no memory of earlier chats needed). For every input batch:
done (all cards read, check passes), problems (all read, check fails), partial (some cards or only part files), todo.
Writes STATUS.md and prints it.  Usage: status.py <game>"""
import glob, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))

def ids(path):
    out = set()
    for f in glob.glob(path):
        for l in open(f):
            try: out.add(json.loads(l)['id'])
            except Exception: pass
    return out

def main():
    game = sys.argv[1]; rows = []; tot = {'done': 0, 'problems': 0, 'partial': 0, 'todo': 0}
    for inp in sorted(glob.glob(os.path.join(HERE, 'input', game, '*.jsonl'))):
        name = os.path.basename(inp)[:-6]
        want = ids(inp)
        folder = 'second' if name.startswith('second') else 'read'
        out = os.path.join(HERE, folder, game, name + '.jsonl')
        parts = glob.glob(os.path.join(HERE, folder, game, name + '.part*.jsonl'))
        got = ids(out) if os.path.exists(out) else set()
        merged = os.path.join(HERE, 'fixes', game, name + '.jsonl')
        if name.startswith('fix_') and os.path.exists(merged):
            tot['done'] += 1; rows.append(f'| {name} | {len(want)} | {len(ids(merged))} | merged |'); continue
        if got >= want:
            r = subprocess.run([sys.executable, os.path.join(HERE, 'check.py'), game, out, '--input', inp], capture_output=True, text=True)
            state = 'done' if r.returncode == 0 else 'problems'
        elif got or parts: state = 'partial'
        else: state = 'todo'
        tot[state] += 1
        rows.append(f'| {name} | {len(want)} | {len(got | ids(os.path.join(HERE, folder, game, name + ".part*.jsonl")))} | {state} |')
    text = (f'# Reading status: {game}\n\nMade by `status.py {game}` from the files. done {tot["done"]}, problems {tot["problems"]}, '
            f'partial {tot["partial"]}, todo {tot["todo"]}.\n\n| batch | cards | read | state |\n|---|---|---|---|\n' + '\n'.join(rows) + '\n')
    open(os.path.join(HERE, 'STATUS.md'), 'w').write(text); print(text)

if __name__ == '__main__':
    main()

"""Definitions for keywords the sources left without one (tools/keyword_defs.json, key 'game|name'): sets text and source_type.
An entry with only text_note records a keyword left unmapped on purpose (kept in extra.unmapped_reason). Usage: keyword_defs.py <db>"""
import json, sqlite3, sys, os
c = sqlite3.connect(sys.argv[1])
d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keyword_defs.json'), encoding='utf-8'))
for key, v in d.items():
    g, n = key.split('|', 1)
    if 'text' in v: c.execute("UPDATE entities SET text=?, source_type=? WHERE game=? AND name=? AND category='keyword' AND (text IS NULL OR text='')", (v['text'], v['source_type'], g, n))
    if 'text_note' in v:
        r = c.execute("SELECT id, extra FROM entities WHERE game=? AND name=? AND category='keyword'", (g, n)).fetchone()
        if r:
            ex = json.loads(r[1]) if r[1] else {}
            ex['unmapped_reason'] = v['text_note']; c.execute('UPDATE entities SET extra=? WHERE id=?', (json.dumps(ex), r[0]))
c.commit(); print('keyword definitions applied:', len(d))

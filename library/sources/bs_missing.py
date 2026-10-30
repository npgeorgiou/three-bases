"""BSData entries whose text the library does not have (helper for conv_bs.py)."""
import sys,sqlite3,collections,re,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import bsdata
c=None
N=lambda t: re.sub(r'[^a-z]+',' ',re.sub(r'\d+','',t.lower())).strip()
def missing(g,repo,ptypes,desc=('Description','Effect','Ability')):
    R=bsdata.read(repo)
    texts=[N(t or '') for (t,) in c.execute("select text from entities where game=?",(g,))]
    big='\n'.join(texts)
    names={n for (n,) in c.execute("select name from entities where game=?",(g,))}|{n for (n,) in c.execute("select name from merged_entities where game=?",(g,))}
    out=[];seen=set()
    for r in R:
        if r['kind']=='profile' and r['ptype'] in ptypes:
            t=next((r['chars'][k] for k in desc if r['chars'].get(k)),'')
        elif r['kind']=='rule' and 'rule' in ptypes: t=r['text']
        else: continue
        if not t: continue
        n=N(t)
        if len(n)<12 or n in seen: continue
        seen.add(n)
        if n[:120] in big: continue
        out.append((r,t))
    return out

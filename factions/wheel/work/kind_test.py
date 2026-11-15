# Test (15 Nov 2026): does a link's kind predict the agents' verdicts? Result: no (KEEP and DROP both ~95% "combo" kinds;
# correlation with the true-pair rate 0.09). Run from library/cards_db with links.sqlite built.
import sys,os,sqlite3,collections,re
sys.path.insert(0,'.')
import mechanics_wheel as mw
mechs=mw.load(); c,games,x,con,pools,stats=mw.setup(); mem=mw.members(mechs,con,pools)
S={k:{i for g in games for i in mem[k][g]} for k in mem}
L=sqlite3.connect('links.sqlite')
rows=L.execute('select l.a,l.b,p.kind from link l join phrase p on p.id=l.phrase').fetchall()
kinds=collections.defaultdict(set)
for a,b,k in rows:
    if a!=b: kinds[(min(a,b),max(a,b))].add(k)
COMBO={'waits','type','puts','repeats','rules','moves','levelsinto','carries','levels','clears'}
out=[]
for l in open('../../factions/wheel/work/mechanic_pair_verdicts.tsv'):
    p=l.rstrip('\n').split('\t')
    a,b=p[0].split('+'); v=p[2]; m=re.search(r'true (\d+) of (\d+)',p[1]); tr=int(m.group(1))/int(m.group(2)) if m else None
    if a not in S or b not in S: continue
    ks=[kinds[(min(s,t),max(s,t))] for s in S[a] for t in S[b] if s!=t and (min(s,t),max(s,t)) in kinds]
    if not ks: continue
    share=sum(bool(k&COMBO) for k in ks)/len(ks)
    out.append((v,share,tr,len(ks)))
by=collections.defaultdict(list)
for v,s,tr,n in out: by[v].append(s)
for v in by: 
    L_=sorted(by[v]); print(v,len(L_),'combo-kind share median %.2f  quartiles %.2f-%.2f'%(L_[len(L_)//2],L_[len(L_)//4],L_[3*len(L_)//4]))
# best single cut: KEEP vs not
best=None
for cut in [i/100 for i in range(5,96)]:
    tp=sum(1 for v,s,*_ in out if v=='KEEP' and s>=cut); fp=sum(1 for v,s,*_ in out if v!='KEEP' and s>=cut)
    fn=sum(1 for v,s,*_ in out if v=='KEEP' and s<cut); tn=sum(1 for v,s,*_ in out if v!='KEEP' and s<cut)
    acc=(tp+tn)/len(out)
    if not best or acc>best[0]: best=(acc,cut,tp,fp,fn,tn)
print('pairs',len(out),'best cut',best)
# correlation share vs true rate
xs=[(s,tr) for v,s,tr,n in out if tr is not None]
import statistics as st
print('corr share~true rate %.2f'%st.correlation([a for a,b in xs],[b for a,b in xs]))
print('base: KEEP',sum(v=='KEEP' for v,*_ in out),'of',len(out))
allk=sorted({k for ks in kinds.values() for k in ks})
for K in allk:
    vals=[]
    for l in open('../../factions/wheel/work/mechanic_pair_verdicts.tsv'):
        p=l.rstrip('\n').split('\t'); a,b=p[0].split('+'); m=re.search(r'true (\d+) of (\d+)',p[1])
        if not m or a not in S or b not in S: continue
        ks=[kinds[(min(s,t),max(s,t))] for s in S[a] for t in S[b] if s!=t and (min(s,t),max(s,t)) in kinds]
        if ks: vals.append((sum(K in k for k in ks)/len(ks), int(m.group(1))/int(m.group(2))))
    if len(vals)>20 and len({v for v,_ in vals})>1: print(K,'corr %.2f'%st.correlation([a for a,_ in vals],[b for _,b in vals]))

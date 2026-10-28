"""One HTML page that draws the networks of the decks in decks.tsv (decks taken from the web, with their source), opened
locally without internet: a tab per deck, a dot per card (pointing at it shows its name, keywords and text), an arrow per
line coloured by kind, and the deck's central cards, chains, groups and loose cards beside it.
Usage: python3 network_page.py [out.html]   (default network.html)"""
import csv, json, os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import deck_analysis, mechanics, network, source

PAGE = r'''<!doctype html><html><head><meta charset="utf-8"><title>Deck networks</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><style>
:root{--bg:#fafaf7;--fg:#222;--mut:#777;--ln:#ddd;--card:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#1b1c1e;--fg:#e6e6e6;--mut:#999;--ln:#3a3a3a;--card:#26272a}}
body{margin:0;font:14px system-ui,sans-serif;background:var(--bg);color:var(--fg)}
#tabs{display:flex;flex-wrap:wrap;gap:4px;padding:8px}#tabs button{border:1px solid var(--ln);background:var(--card);color:var(--fg);
padding:4px 8px;border-radius:6px;cursor:pointer}#tabs button.on{border-color:var(--fg);font-weight:600}
#main{display:flex;gap:8px;padding:0 8px 8px}#draw{flex:1;min-width:0;background:var(--card);border:1px solid var(--ln);border-radius:8px}
#side{width:380px;max-height:86vh;overflow:auto;font-size:13px}#side pre{white-space:pre-wrap;margin:0}
#tip{position:fixed;max-width:340px;background:var(--card);border:1px solid var(--fg);border-radius:6px;padding:8px;font-size:13px;
display:none;pointer-events:none}#legend span{display:inline-block;margin:0 8px 4px 0}
svg text{font-size:11px;fill:var(--fg);pointer-events:none}a{color:inherit}
@media (max-width:800px){#main{flex-direction:column}#side{width:auto}}</style></head><body>
<div id="tabs"></div><div id="main"><div><svg id="draw" width="900" height="700"></svg>
<div id="legend"></div><label><input type="checkbox" id="aim"> show "can aim at it" lines</label></div><div id="side"></div></div>
<div id="tip"></div><script>
const D=__DATA__;
const KIND={waits:'#3b82f6',levels:'#a855f7',puts:'#16a34a',repeats:'#ea580c',rules:'#dc2626',targets:'#9ca3af',type:'#0891b2',levelsinto:'#111827'};
const GROUP=['#f59e0b','#3b82f6','#10b981','#ef4444','#8b5cf6','#06b6d4','#84cc16','#ec4899'];
let cur=0;const svg=document.getElementById('draw'),tip=document.getElementById('tip'),aim=document.getElementById('aim');
document.getElementById('legend').innerHTML=Object.entries(KIND).map(([k,c])=>`<span style="color:${c}">&#9632; ${k}</span>`).join('');
D.forEach((d,i)=>{const b=document.createElement('button');b.textContent=d.deck;b.onclick=()=>{cur=i;show()};document.getElementById('tabs').appendChild(b)});
aim.onchange=()=>show();
function layout(d,W,H){ // spring layout: lines pull, all dots push, a fixed number of steps
 const N=d.nodes,ix={};N.forEach((n,i)=>{ix[n.id]=i;n.x=W/2+200*Math.cos(i*2.4);n.y=H/2+200*Math.sin(i*2.4)});
 const E=d.lines.filter(l=>l.kind!=='targets');
 for(let t=0;t<400;t++){const k=1-t/400;
  for(const a of N){a.dx=0;a.dy=0}
  for(let i=0;i<N.length;i++)for(let j=i+1;j<N.length;j++){const a=N[i],b=N[j];let x=a.x-b.x,y=a.y-b.y,r=Math.max(20,Math.hypot(x,y)),f=9000/(r*r);
   a.dx+=x/r*f;a.dy+=y/r*f;b.dx-=x/r*f;b.dy-=y/r*f}
  for(const l of E){const a=N[ix[l.from]],b=N[ix[l.to]],x=b.x-a.x,y=b.y-a.y,r=Math.max(1,Math.hypot(x,y)),f=(r-130)*0.02;
   a.dx+=x/r*f;a.dy+=y/r*f;b.dx-=x/r*f;b.dy-=y/r*f}
  for(const a of N){a.dx+=(W/2-a.x)*0.004;a.dy+=(H/2-a.y)*0.004;
   a.x=Math.min(W-60,Math.max(60,a.x+Math.max(-20,Math.min(20,a.dx))*k*2));a.y=Math.min(H-20,Math.max(20,a.y+Math.max(-20,Math.min(20,a.dy))*k*2))}}
 return ix}
function esc(s){return String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function show(){const d=D[cur],W=900,H=700;[...document.querySelectorAll('#tabs button')].forEach((b,i)=>b.className=i===cur?'on':'');
 const ix=layout(d,W,H),N=d.nodes,nm=id=>N[ix[id]].name;
 let s=Object.entries(KIND).map(([k,c])=>`<marker id="m${k}" viewBox="0 0 10 10" refX="17" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="${c}"/></marker>`).join('');
 s=`<defs>${s}</defs>`;
 for(const l of d.lines){if(l.kind==='targets'&&!aim.checked)continue;const a=N[ix[l.from]],b=N[ix[l.to]];
  s+=`<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" stroke="${KIND[l.kind]}" stroke-width="${1+Math.min(3,l.weight*6)}" opacity=".55" marker-end="url(#m${l.kind})" data-l="${d.lines.indexOf(l)}"/>`}
 for(const n of N){const c=n.group<0?'#9ca3af':GROUP[n.group%GROUP.length];
  s+=`<circle cx="${n.x}" cy="${n.y}" r="9" fill="${c}" stroke="var(--fg)" stroke-dasharray="${n.made?'2 2':''}" data-n="${ix[n.id]}"/><text x="${n.x+12}" y="${n.y+4}">${esc(n.name)}</text>`}
 svg.innerHTML=s;
 document.getElementById('side').innerHTML=`<b>${esc(d.deck)}</b> (${esc(d.game)}) <a href="${d.source}">source</a><pre>${esc(d.report.join('\n'))}</pre>`;
 svg.onmousemove=e=>{const t=e.target;let h='';
  if(t.dataset.n){const n=N[+t.dataset.n];h=`<b>${esc(n.name)}</b>${n.made?' (made by the deck)':''}<br>${n.keywords.length?'<i>'+esc(n.keywords.join(', '))+'</i><br>':''}${esc(n.text)}`}
  else if(t.dataset.l){const l=d.lines[+t.dataset.l];h=`${esc(nm(l.from))} &rarr; <b>${esc(l.why)}</b> &rarr; ${esc(nm(l.to))}<br><span style="color:var(--mut)">${l.kind}, weight ${l.weight}</span>`}
  tip.style.display=h?'block':'none';tip.innerHTML=h;tip.style.left=Math.min(innerWidth-360,e.clientX+14)+'px';tip.style.top=(e.clientY+14)+'px'};
 svg.onmouseleave=()=>tip.style.display='none'}
show();
</script></body></html>'''


def deck_data(c, lib, game, deck, src, text):
    ids, _ = deck_analysis.parse_deck(c, game, text)
    ids = list(dict.fromkeys(ids))
    nodes, lines = network.network(c, game, ids)
    best = network.best_lines(lines)
    group = {}
    for k, (g, _) in enumerate(network.groups(best, nodes)):
        for n in g: group[n] = k
    out = []
    for i, made in nodes.items():
        r = lib.execute('select text from entities where id=?', (i,)).fetchone()
        txt = ' '.join(((r[0] if r else '') or '').replace('Missing Translation', '').split())
        kws = [n for (n,) in c.execute('select k.name from card_keyword ck join card k on k.id=ck.keyword where ck.card=?', (i,))]
        out.append({'id': i, 'name': mechanics.name(c, i), 'made': made, 'group': group.get(i, -1), 'keywords': kws, 'text': txt})
    ls = []
    for (a, b), rs in lines.items():  # one arrow per pair and kind, its strongest reason
        per = {}
        for kind, w, why in rs:
            if kind not in per or w > per[kind][0]: per[kind] = (w, why)
        ls += [{'from': a, 'to': b, 'kind': k, 'weight': round(w, 3), 'why': y} for k, (w, y) in per.items()]
    return {'game': game, 'deck': deck, 'source': src, 'nodes': out, 'lines': ls,
            'report': network.report(c, game, ids, f'{deck}')[1:]}


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'network.html')
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite')); lib = source.lib()
    data = [deck_data(c, lib, r['game'], r['deck'], r['source'], r['cards'])
            for r in csv.DictReader(open(os.path.join(HERE, 'decks.tsv'), encoding='utf-8'), delimiter='\t')]
    open(out, 'w', encoding='utf-8').write(PAGE.replace('__DATA__', json.dumps(data, ensure_ascii=False).replace('</', '<\\/')))
    print(out)


main()

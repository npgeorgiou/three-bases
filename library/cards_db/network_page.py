"""One HTML page that draws the networks of the decks in decks.tsv (decks taken from the web, with their source), opened
locally without internet: a tab per deck, a dot per card (pointing at it shows its name, keywords and text), an arrow per
line coloured by kind (legend click hides a kind), zoom and pan, a node clicked keeps its lines highlighted, and the deck's
central cards, chains, groups and loose cards beside it.
Usage: python3 network_page.py [out.html]   (default network.html)"""
import csv, json, os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import deck_analysis, mechanics, network, source

PAGE = r'''<!doctype html><html><head><meta charset="utf-8"><title>Deck networks</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><style>
:root{--bg:#f6f6f3;--fg:#1f2328;--mut:#6b7280;--ln:#d9dbe0;--card:#fff;--chip:#eef0f3}
@media (prefers-color-scheme:dark){:root{--bg:#18191b;--fg:#e7e7e7;--mut:#9aa0a6;--ln:#34363a;--card:#222326;--chip:#2c2e32}}
*{box-sizing:border-box}html,body{height:100%}body{margin:0;font:14px system-ui,sans-serif;background:var(--bg);color:var(--fg);display:flex;flex-direction:column}
#tabs{display:flex;gap:4px;padding:6px 8px;overflow-x:auto;flex:none}
#tabs button{flex:none;border:1px solid var(--ln);background:var(--card);color:var(--fg);padding:4px 10px;border-radius:6px;cursor:pointer}
#tabs button.on{border-color:var(--fg);font-weight:600}
#main{flex:1;display:flex;min-height:0}
#graph{flex:1;position:relative;min-width:0;background:var(--card);border-top:1px solid var(--ln)}
#draw{width:100%;height:100%;display:block;cursor:grab}#draw.pan{cursor:grabbing}
#legend{position:absolute;left:8px;top:8px;background:var(--card);border:1px solid var(--ln);border-radius:8px;padding:6px 8px;font-size:12px;max-width:260px}
#legend b{display:block;margin:2px 0}#legend div.k{display:flex;align-items:center;gap:6px;padding:1px 4px;border-radius:4px;cursor:pointer;user-select:none}
#legend div.k:hover{background:var(--chip)}#legend div.off{opacity:.35;text-decoration:line-through}#legend div.n{cursor:default}
#tools{position:absolute;right:8px;top:8px;display:flex;gap:4px}#tools button{border:1px solid var(--ln);background:var(--card);color:var(--fg);
border-radius:6px;padding:2px 9px;cursor:pointer;font-size:15px}
#side{width:360px;flex:none;overflow:auto;padding:10px 12px;border-left:1px solid var(--ln);border-top:1px solid var(--ln);font-size:13px;line-height:1.45}
#side h2{font-size:16px;margin:0 0 2px}#side h3{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:14px 0 4px}
#side .sub{color:var(--mut)}#side ul{margin:0;padding:0;list-style:none}#side li{margin:3px 0}
.chip{display:inline-flex;align-items:center;gap:4px;background:var(--chip);border-radius:10px;padding:0 7px;cursor:pointer;white-space:nowrap;margin:1px 0}
.chip:hover{outline:1px solid var(--fg)}.chip i{width:9px;height:9px;border-radius:50%;display:inline-block;border:1px solid var(--fg)}.chip.made{font-style:italic}
.why{color:var(--mut);font-size:12px;margin:0 3px}.num{color:var(--mut);font-size:12px;margin-left:4px}.chain{padding:4px 0;border-bottom:1px solid var(--ln)}
#tip{position:fixed;max-width:340px;background:var(--card);border:1px solid var(--fg);border-radius:6px;padding:8px;font-size:13px;display:none;pointer-events:none;z-index:9}
svg text{font-size:12px;fill:var(--fg);pointer-events:none;paint-order:stroke;stroke:var(--card);stroke-width:3px}
@media (max-width:800px){#main{flex-direction:column}#side{width:auto;height:40%;border-left:0}}</style></head><body>
<div id="tabs"></div><div id="main"><div id="graph"><svg id="draw"></svg><div id="legend"></div>
<div id="tools"><button id="zin" title="zoom in">+</button><button id="zout" title="zoom out">&minus;</button><button id="fit" title="fit">fit</button></div></div>
<div id="side"></div></div><div id="tip"></div><script>
const D=__DATA__;
const LINE={waits:['#0d9488','makes what it waits for'],levels:['#c026d3','helps it level up'],puts:['#65a30d','puts it into play'],
 repeats:['#ea580c','repeats its effects'],rules:['#dc2626','changes how it works'],type:['#4f46e5','has the type it asks for'],
 levelsinto:['#6b7280','levels into'],targets:['#9ca3af','can aim at it']};
const CARD={hero:['#facc15','champion'],unit:['#7dd3fc','unit'],spell:['#c4b5fd','spell'],building:['#6ee7b7','landmark / structure'],
 item:['#fdba74','equipment'],ability:['#d1d5db','skill']};
const R=14,NS='http://www.w3.org/2000/svg',svg=document.getElementById('draw'),tip=document.getElementById('tip');
const hidden=new Set();let cur=0,sel=null,hov=null,vb=null,d=null,N=[],ix={},els={};
D.forEach((x,i)=>{const b=document.createElement('button');b.textContent=x.deck;b.onclick=()=>{cur=i;sel=null;show()};document.getElementById('tabs').appendChild(b)});
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const col=n=>(CARD[n.cat]||['#d1d5db'])[0];
function layout(){ // spring layout on the lines that tie cards together; cards with none go in a row below
 const E=d.lines.filter(l=>l.kind!=='targets'),deg={};E.forEach(l=>{deg[l.from]=1;deg[l.to]=1});
 const L=N.filter(n=>deg[n.id]),F=N.filter(n=>!deg[n.id]);
 L.forEach((n,i)=>{n.x=Math.cos(i*2.4)*(60+8*i);n.y=Math.sin(i*2.4)*(60+8*i)});
 for(let t=0;t<500;t++){const k=1-t/500;L.forEach(a=>{a.dx=-a.x*0.01;a.dy=-a.y*0.01});
  for(let i=0;i<L.length;i++)for(let j=i+1;j<L.length;j++){const a=L[i],b=L[j],x=a.x-b.x,y=a.y-b.y,r=Math.max(25,Math.hypot(x,y));
   if(r>600)continue;const f=40000/(r*r)+(r<90?(90-r)*0.5:0);a.dx+=x/r*f;a.dy+=y/r*f;b.dx-=x/r*f;b.dy-=y/r*f}
  E.forEach(l=>{const a=N[ix[l.from]],b=N[ix[l.to]],x=b.x-a.x,y=b.y-a.y,r=Math.max(1,Math.hypot(x,y)),f=(r-190)*0.03;
   a.dx+=x/r*f;a.dy+=y/r*f;b.dx-=x/r*f;b.dy-=y/r*f});
  L.forEach(a=>{a.x+=Math.max(-25,Math.min(25,a.dx))*k;a.y+=Math.max(-25,Math.min(25,a.dy))*k})}
 for(let t=0;t<200;t++){let moved=0; // labels must not cover other cards: a card and its label are a box
  for(let i=0;i<L.length;i++)for(let j=i+1;j<L.length;j++){const a=L[i],b=L[j],[l,r]=a.x<b.x?[a,b]:[b,a],
   need=R+10+l.name.length*7,dx=r.x-l.x,dy=Math.abs(a.y-b.y);
   if(dx<need&&dy<34){const p=(34-dy)/2+1,up=a.y<=b.y?a:b,dn=up===a?b:a;up.y-=p;dn.y+=p;moved=1}}
  if(!moved)break}
 let x0=Infinity,x1=-Infinity,y1=-Infinity;L.forEach(n=>{x0=Math.min(x0,n.x);x1=Math.max(x1,n.x);y1=Math.max(y1,n.y)});
 if(!L.length){x0=0;x1=600;y1=-60}
 const w=Math.max(x1-x0,600),per=Math.max(1,Math.floor(w/190));
 F.forEach((n,i)=>{n.x=x0+(i%per)*190;n.y=y1+90+Math.floor(i/per)*50})}
function fit(){let a=Infinity,b=Infinity,c=-Infinity,e=-Infinity;
 N.forEach(n=>{a=Math.min(a,n.x-R);b=Math.min(b,n.y-R);c=Math.max(c,n.x+R+8+n.name.length*7);e=Math.max(e,n.y+R)});
 vb={x:a-30,y:b-30,w:c-a+60,h:e-b+60};setVB()}
function setVB(){svg.setAttribute('viewBox',`${vb.x} ${vb.y} ${vb.w} ${vb.h}`)}
function zoom(f,cx,cy){const r=svg.getBoundingClientRect(),s=Math.max(vb.w/r.width,vb.h/r.height);
 const px=cx==null?vb.x+vb.w/2:vb.x+(cx-r.left)*s-(r.width*s-vb.w)/2,py=cy==null?vb.y+vb.h/2:vb.y+(cy-r.top)*s-(r.height*s-vb.h)/2;
 vb={x:px-(px-vb.x)*f,y:py-(py-vb.y)*f,w:vb.w*f,h:vb.h*f};setVB()}
svg.onwheel=e=>{e.preventDefault();zoom(e.deltaY>0?1.15:1/1.15,e.clientX,e.clientY)};
document.getElementById('zin').onclick=()=>zoom(1/1.3);document.getElementById('zout').onclick=()=>zoom(1.3);document.getElementById('fit').onclick=()=>fit();
let drag=null;svg.onmousedown=e=>{if(e.target.dataset.n)return;drag={x:e.clientX,y:e.clientY,vb:{...vb},moved:false};svg.classList.add('pan')};
addEventListener('mousemove',e=>{if(!drag)return;const r=svg.getBoundingClientRect(),s=Math.max(vb.w/r.width,vb.h/r.height),dx=e.clientX-drag.x,dy=e.clientY-drag.y;
 if(Math.abs(dx)+Math.abs(dy)>3)drag.moved=true;vb={...drag.vb,x:drag.vb.x-dx*s,y:drag.vb.y-dy*s};setVB()});
addEventListener('mouseup',e=>{if(drag&&!drag.moved&&!e.target.dataset.n&&e.target.closest('#draw')){sel=null;mark()}drag=null;svg.classList.remove('pan')});
function el(t,a){const x=document.createElementNS(NS,t);for(const k in a)x.setAttribute(k,a[k]);return x}
function draw(){svg.innerHTML='';const defs=el('defs',{});
 for(const[k,[c]]of Object.entries(LINE))defs.appendChild(el('marker',{id:'m'+k,viewBox:'0 0 10 10',refX:9,refY:5,markerWidth:12,markerHeight:12,markerUnits:'userSpaceOnUse',orient:'auto'})).appendChild(el('path',{d:'M0,0L10,5L0,10z',fill:c}));
 svg.appendChild(defs);const gl=el('g',{}),gn=el('g',{});svg.append(gl,gn);els={lines:[],nodes:[]};
 d.lines.forEach((l,i)=>{const a=N[ix[l.from]],b=N[ix[l.to]],x=b.x-a.x,y=b.y-a.y,r=Math.max(1,Math.hypot(x,y)),ux=x/r,uy=y/r;
  const p={x1:a.x+ux*R,y1:a.y+uy*R,x2:b.x-ux*(R+2),y2:b.y-uy*(R+2)},c=LINE[l.kind][0];
  const ln=el('line',{...p,stroke:c,'stroke-width':l.kind==='targets'?2:2+Math.min(3,l.weight*6),'marker-end':`url(#m${l.kind})`});
  if(l.kind==='targets')ln.setAttribute('stroke-dasharray','6 4');if(l.kind==='levelsinto')ln.setAttribute('stroke-dasharray','2 3');
  const hit=el('line',{...p,stroke:'transparent','stroke-width':10,'data-l':i});gl.append(ln,hit);els.lines.push(ln)});
 N.forEach((n,i)=>{const g=el('g',{});const c=el('circle',{cx:n.x,cy:n.y,r:R,fill:col(n),stroke:'currentColor','stroke-width':n.made?1.5:2,'data-n':i,style:'cursor:pointer;color:var(--fg)'});
  if(n.made)c.setAttribute('stroke-dasharray','3 3');const t=el('text',{x:n.x+R+5,y:n.y+4});t.textContent=n.name;g.append(c,t);gn.appendChild(g);els.nodes.push(g)});
 mark()}
function mark(){const f=hov!=null?hov:sel,on=new Set();
 d.lines.forEach((l,i)=>{const ln=els.lines[i],show=!hidden.has(l.kind),touch=f!=null&&(ix[l.from]===f||ix[l.to]===f);
  ln.style.display=show?'':'none';els.lines[i].nextSibling.style.display=show?'':'none';
  if(touch&&show){on.add(ix[l.from]);on.add(ix[l.to])}
  ln.style.opacity=f==null?(l.kind==='targets'?.45:.6):touch?1:.08;ln.style.filter=touch?'saturate(1.6)':''});
 els.nodes.forEach((g,i)=>{g.style.opacity=f==null||i===f||on.has(i)?1:.25;g.firstChild.setAttribute('r',i===sel?R+4:R)});
 document.querySelectorAll('.chip').forEach(c=>c.style.outline=+c.dataset.id===(sel!=null?N[sel].id:-1)?'2px solid var(--fg)':'')}
svg.onmousemove=e=>{if(drag&&drag.moved)return;const t=e.target;let h='';
 if(t.dataset.n){const n=N[+t.dataset.n];hov=+t.dataset.n;h=`<b>${esc(n.name)}</b> <span style="color:var(--mut)">${esc((CARD[n.cat]||['',n.cat])[1])}${n.made?', made by the deck':''}</span><br>${n.keywords.length?'<i>'+esc(n.keywords.join(', '))+'</i><br>':''}${esc(n.text)}`}
 else{hov=null;if(t.dataset.l){const l=d.lines[+t.dataset.l];h=`${esc(N[ix[l.from]].name)} &rarr; <b>${esc(l.why)}</b> &rarr; ${esc(N[ix[l.to]].name)}<br><span style="color:var(--mut)">${LINE[l.kind][1]}</span>`}}
 mark();tip.style.display=h?'block':'none';tip.innerHTML=h;tip.style.left=Math.min(innerWidth-360,e.clientX+14)+'px';tip.style.top=Math.min(innerHeight-120,e.clientY+14)+'px'};
svg.onmouseleave=()=>{hov=null;mark();tip.style.display='none'};
svg.onclick=e=>{if(e.target.dataset.n){const i=+e.target.dataset.n;sel=sel===i?null:i;mark()}};
function legend(){const cats=[...new Set(N.map(n=>n.cat))],kinds=new Set(d.lines.map(l=>l.kind));
 let h='<b>Cards</b>'+cats.map(c=>`<div class="k n"><svg width="14" height="14"><circle cx="7" cy="7" r="6" fill="${(CARD[c]||['#ccc'])[0]}" stroke="currentColor"/></svg>${esc((CARD[c]||['',c])[1])}</div>`).join('')
  +'<div class="k n"><svg width="14" height="14"><circle cx="7" cy="7" r="6" fill="none" stroke="currentColor" stroke-dasharray="2 2"/></svg>made by the deck</div>'
  +'<b>Lines: A &rarr; B (click to hide)</b>'+Object.entries(LINE).filter(([k])=>kinds.has(k)).map(([k,[c,t]])=>`<div class="k${hidden.has(k)?' off':''}" data-k="${k}"><svg width="26" height="10"><line x1="1" y1="5" x2="25" y2="5" stroke="${c}" stroke-width="3" ${k==='targets'?'stroke-dasharray="5 3"':''}/></svg>${t}</div>`).join('');
 const L=document.getElementById('legend');L.innerHTML=h;L.querySelectorAll('[data-k]').forEach(x=>x.onclick=()=>{const k=x.dataset.k;hidden.has(k)?hidden.delete(k):hidden.add(k);legend();mark()})}
function chip(id){const n=N[ix[id]];return `<span class="chip${n.made?' made':''}" data-id="${id}"><i style="background:${col(n)}"></i>${esc(n.name)}</span>`}
function side(){const m=d.m,s=document.getElementById('side');let h=`<h2>${esc(d.deck)}</h2><div class="sub">${esc(d.game)} &middot; <a href="${esc(d.source)}" target="_blank">source</a> &middot; ${m.own} cards, ${m.made} made by them, ${m.lines} lines &middot; ${m.linked} of ${m.own} cards linked</div>`;
 h+='<h3>Central cards</h3><ul>'+m.central.map(([i,a,b])=>`<li>${chip(i)}<span class="num">${a} in &middot; ${b} out</span></li>`).join('')+'</ul>';
 if(m.through.length)h+='<h3>Most chains pass through</h3>'+m.through.map(chip).join(' ');
 h+='<h3>Strongest chains</h3>'+m.chains.map(([head,whys,ends])=>'<div class="chain">'+head.map((x,i)=>chip(x)+`<span class="why">&rarr; ${esc(whys[i])} &rarr;</span>`).join('')+ends.map(chip).join(' ')+'</div>').join('');
 h+='<h3>Groups</h3>'+m.groups.map(([g,why])=>`<div class="chain"><div class="why" style="margin:0">${esc(why||'linked')} (${g.length})</div>${g.map(chip).join(' ')}</div>`).join('');
 const lo=[['no lines at all',m.alone],['only give to others',m.gives],['only get from others',m.gets]].filter(x=>x[1].length);
 if(lo.length||m.lack.length){h+='<h3>Loose cards</h3>'+lo.map(([t,xs])=>`<div class="chain"><div class="why" style="margin:0">${t}</div>${xs.map(chip).join(' ')}</div>`).join('');
  h+=m.lack.map(([i,w])=>`<div class="chain">${chip(i)}<span class="why">waits for &ldquo;${esc(w)}&rdquo;, nothing here does it</span></div>`).join('')}
 s.innerHTML=h;s.querySelectorAll('.chip').forEach(c=>{const i=ix[+c.dataset.id];c.onclick=()=>{sel=sel===i?null:i;mark()};c.onmouseenter=()=>{hov=i;mark()};c.onmouseleave=()=>{hov=null;mark()}})}
function show(){d=D[cur];N=d.nodes;ix={};N.forEach((n,i)=>ix[n.id]=i);
 document.querySelectorAll('#tabs button').forEach((b,i)=>b.className=i===cur?'on':'');layout();draw();fit();legend();side();mark()}
show();
</script></body></html>'''


def deck_data(c, lib, game, deck, src, text):
    ids, _ = deck_analysis.parse_deck(c, game, text)
    m = network.measure(c, game, list(dict.fromkeys(ids)))
    nodes, lines = m['nodes'], m['lines']
    out = []
    for i, made in nodes.items():
        r = lib.execute('select text from entities where id=?', (i,)).fetchone()
        txt = ' '.join(((r[0] if r else '') or '').replace('Missing Translation', '').split())
        kws = [n for (n,) in c.execute('select k.name from card_keyword ck join card k on k.id=ck.keyword where ck.card=?', (i,))]
        cat = c.execute('select category from card where id=?', (i,)).fetchone()[0]
        out.append({'id': i, 'name': mechanics.name(c, i), 'made': made, 'cat': cat, 'keywords': kws, 'text': txt})
    ls = []
    for (a, b), rs in lines.items():  # one arrow per pair and kind, its strongest reason
        per = {}
        for kind, w, why in rs:
            if kind not in per or w > per[kind][0]: per[kind] = (w, why)
        ls += [{'from': a, 'to': b, 'kind': k, 'weight': round(w, 3), 'why': y} for k, (w, y) in per.items()]
    by_name = lambda xs: sorted(dict.fromkeys(xs), key=lambda i: mechanics.name(c, i))
    meas = {'own': len(m['own']), 'made': sum(nodes.values()), 'lines': len(m['best']), 'linked': m['linked'],
            'central': m['central'], 'through': m['through'], 'chains': m['chains'],
            'groups': [[by_name(g), why] for g, why in m['groups']], 'alone': by_name(m['alone']), 'gives': by_name(m['gives']),
            'gets': by_name(m['gets']), 'lack': m['lack']}
    return {'game': game, 'deck': deck, 'source': src, 'nodes': out, 'lines': ls, 'm': meas}


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'network.html')
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite')); lib = source.lib()
    data = [deck_data(c, lib, r['game'], r['deck'], r['source'], r['cards'])
            for r in csv.DictReader(open(os.path.join(HERE, 'decks.tsv'), encoding='utf-8'), delimiter='\t')]
    open(out, 'w', encoding='utf-8').write(PAGE.replace('__DATA__', json.dumps(data, ensure_ascii=False).replace('</', '<\\/')))
    print(out)


main()

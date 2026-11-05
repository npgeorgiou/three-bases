// Check: a saved network whose unit-state list differs (a keyword gone, order changed) loads, keeps its weights by name,
// and the missing one starts at zero; and a keyword worth set in the ifelse values changes a unit's worth. Run: node tools/net_byname_check.js
const fs=require('fs'),path=require('path'),vm=require('vm');
const R=path.join(__dirname,'..','src');
const gp=fs.readFileSync(R+'/game/parts.txt','utf8').split('\n').map(s=>s.trim()).filter(n=>/^js\/(00-intro|cards\/|rules\/|ai\/)/.test(n));
const lp=['decks.js','benchmark-v1.js','known.js','ifelse-fields.js','network-encode.js','network-play.js'].map(n=>R+'/lab/js/engine/'+n);
const code=gp.map(n=>fs.readFileSync(R+'/game/'+n,'utf8')).join('\n')+'\n'+lp.map(f=>fs.readFileSync(f,'utf8')).join('\n');
const ctx={console,performance,structuredClone,atob,btoa,WebAssembly,setTimeout};
vm.createContext(ctx);
vm.runInContext(code+'\n;globalThis.G={newGame,applyAction,listActions,cloneState,chooseIfelseAction,BENCH_VALUES,aiMulligan,randomRedraw,encode3,F3,net3Create,net3Instance,netJudge,chooseNetActionEx,DECKS,PREMADE,CARDS,ifelseEval,nextRoundView:typeof nextRoundView!=="undefined"?nextRoundView:null,evaluateOutcome,randomMove,net3FromData,F3_MIRROR,F3_PRINTED,net3Layout,net3ToData,net3Valid,F3_UNIT_NAMES,KW_FLAGS,kwWorth,IFELSE_FIELDS,kw};',ctx,{filename:'engine.js'});

// a saved network whose unit-state list differs (one keyword gone, order changed) still loads and keeps its weights by name
const G=ctx.G;const F3=G.F3;const n=G.net3Create(F3.hidden);const d=G.net3ToData(n);
const L=G.net3Layout(F3.props.length,F3.hidden),WC=L.blocks.WC.o,CO=F3.CO;n.views&&n.views();const w=Float32Array.from(n.w);
// old list: without 'kw:ranged', 'moves' moved to the end
const names=G.F3_UNIT_NAMES,oldNames=[...names.filter(k=>k!=='kw:ranged'&&k!=='moves'),'moves'];
const csO=20+oldNames.length,Lo=G.net3Layout(F3.props.length,F3.hidden,csO),old=new Float32Array(Lo.total);
const row=(arr,base,r)=>arr.subarray(base+r*CO,base+(r+1)*CO);
for(let j=0;j<20;j++)old.set(row(w,WC,j),Lo.blocks.WC.o+j*CO);
oldNames.forEach((k,i)=>old.set(row(w,WC,20+names.indexOf(k)),Lo.blocks.WC.o+(20+i)*CO));
for(let j=0;j<F3.props.length+7;j++)old.set(row(w,WC,F3.CS+j),Lo.blocks.WC.o+(csO+j)*CO);
old.set(w.subarray(L.blocks.BC.o),Lo.blocks.BC.o);
const b64=a=>Buffer.from(a.buffer).toString('base64');
const od={...d,arch:{...d.arch,unitNow:oldNames},weights:b64(old)};
console.log('valid',G.net3Valid(od,F3.hidden));const m=G.net3FromData(od);m.views&&m.views();
let same=true;oldNames.forEach(k=>{const a=row(m.w,WC,20+names.indexOf(k)),b=row(w,WC,20+names.indexOf(k));for(let i=0;i<CO;i++)if(a[i]!==b[i])same=false;});
const r0=row(m.w,WC,20+names.indexOf('kw:ranged'));console.log('kept by name',same,'new one starts at zero',r0.every(x=>x===0),'rest same',m.w.subarray(L.blocks.W0.o).every((x,i)=>x===w[L.blocks.W0.o+i]));
const kf=G.IFELSE_FIELDS.find(x=>x[0].startsWith('kw_'))[0],card=Object.keys(G.CARDS).find(k=>G.CARDS[k].sup&&G.CARDS[k][kf.slice(3)]);
console.log('keyword worth works',G.kwWorth({card},{})===0&&G.kwWorth({card},{[kf]:5})===5);

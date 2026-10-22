// Offline asset audit. Writes fixed corrections; the game never generates building layouts.
import fs from 'node:fs';
import {Game} from '../dist/engine.js';
import {LOCATIONS} from '../dist/data.js';
import {SCENE_PLANS} from '../dist/scenes.js';
import {buildingAsset} from '../dist/geometry.js';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{loadImage}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/@napi-rs/canvas');
const g=new Game();g.newGame();const cache={},changes={},audit=[];
const auditPath=new URL('../docs/building-scale-v11.json',import.meta.url);
const baseline=new Map((fs.existsSync(auditPath)?JSON.parse(fs.readFileSync(auditPath)):[]).map(a=>[a.location+':'+a.index,a.before]));
for(const l of LOCATIONS.filter(l=>!l.interior)){
 const plan=SCENE_PLANS[l.id],rows=[];
 for(const [i,current]of plan.buildings.entries()){
  const b={...current,...(baseline.get(l.id+':'+i)||{})};
  const a=buildingAsset(b.asset),im=cache[a.file]??=await loadImage(new URL('../dist/assets/'+a.file,import.meta.url).pathname),natural=(b.w+b.d)*32*1.06*im.height/im.width;
  if(!b.footprintFit||natural<=b.h*1.08)continue;
  const factor=Math.min(1,b.h/natural),w=Math.max(2,Math.round(b.w*factor)),d=Math.max(2,Math.round(b.d*factor));
  rows.push([i,b.q+b.w-w,b.r+b.d-d,w,d]);
  audit.push({location:l.id,index:i,asset:b.asset,label:b.label,before:{q:b.q,r:b.r,w:b.w,d:b.d,height:Math.round(natural)},after:{q:b.q+b.w-w,r:b.r+b.d-d,w,d,height:Math.round(Math.min((w+d)*32*1.06*im.height/im.width,b.h))}});
 }
 if(rows.length)changes[l.id]=rows;
}
const source=`// Fixed scale corrections from the v0.11 asset audit. Parcels keep their authored front edge.\nconst CORRECTIONS=${JSON.stringify(changes,null,1)};\nexport function installBuildingScale(plans){for(const [id,rows]of Object.entries(CORRECTIONS))for(const [i,q,r,w,d]of rows)Object.assign(plans[id].buildings[i],{q,r,w,d});}\n`;
fs.writeFileSync(new URL('../dist/building-scale-v11.js',import.meta.url),source);fs.writeFileSync(new URL('../docs/building-scale-v11.json',import.meta.url),JSON.stringify(audit,null,2)+'\n');
console.log(JSON.stringify({buildings:audit.length,zones:Object.keys(changes).length,largestBefore:Math.max(...audit.map(x=>x.before.height)),largestAfter:Math.max(...audit.map(x=>x.after.height))}));

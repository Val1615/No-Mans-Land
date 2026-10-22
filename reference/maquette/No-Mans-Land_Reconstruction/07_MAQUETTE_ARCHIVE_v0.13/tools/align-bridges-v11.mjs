import fs from 'node:fs';
import {Game} from '../dist/engine.js';
import {SCENE_PLANS} from '../dist/scenes.js';
const g=new Game();g.newGame();
const audit=JSON.parse(fs.readFileSync(new URL('../docs/building-scale-v11.json',import.meta.url))),overrides={};
const distance=(p,b)=>Math.hypot(Math.max(b.q-p[0],0,p[0]-(b.q+b.w)),Math.max(b.r-p[1],0,p[1]-(b.r+b.d)));
for(const [id,plan]of Object.entries(SCENE_PLANS)){
 for(const [index,link]of (plan.links||[]).entries()){
  if(link.kind!=='skybridge')continue;
  const endpoints=['from','to'].map(key=>{const p=link[key];const nearest=plan.buildings.map((b,i)=>({b,i,before:audit.find(a=>a.location===id&&a.index===i)?.before||b})).sort((a,b)=>distance(p,a.before)-distance(p,b.before))[0];if(!nearest||distance(p,nearest.before)>2)return p;const b=nearest.b;return[Math.max(b.q,Math.min(b.q+b.w,p[0])),Math.max(b.r,Math.min(b.r+b.d,p[1]))];});
  (overrides[id]??={})[index]={from:endpoints[0],to:endpoints[1]};
 }
}
fs.writeFileSync(new URL('../dist/bridge-anchors-v11.js',import.meta.url),`// Authored skywalk endpoints follow the resized building fronts.\nconst BRIDGES=${JSON.stringify(overrides,null,1)};\nexport function installBridgeAnchors(plans){for(const [id,links]of Object.entries(BRIDGES))for(const [i,endpoints]of Object.entries(links))Object.assign(plans[id].links[i],endpoints);}\n`);console.log(JSON.stringify(overrides));

// Offline alignment of every real entrance after the scale audit.
import fs from 'node:fs';
import {Game,DIRS} from '../dist/engine.js';
import {LOCATIONS,OBJECTS} from '../dist/data.js';
import {SCENE_PLANS} from '../dist/scenes.js';
import {buildingAsset,buildingRect,project,titanRect} from '../dist/geometry.js';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{loadImage}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/@napi-rs/canvas');
const g=new Game();g.newGame();const cache={},overrides={},audit=[];
for(const l of LOCATIONS.filter(l=>!l.interior)){
 g.enter(l.id);g.scene.enemies=[];const m=g.scene,seen=new Set([m.spawn.q+','+m.spawn.r]),queue=[m.spawn];let head=0;while(head<queue.length){const a=queue[head++];for(const [dq,dr]of DIRS){const q=a.q+dq,r=a.r+dr,k=q+','+r;if(!seen.has(k)&&g.walkable(q,r,true)){seen.add(k);queue.push({q,r});}}}
 for(const door of m.objects.filter(o=>OBJECTS[o.id]?.type==='door'&&o.anchor)){
  const a=door.anchor;let rect,flip=false;if(a.building!==undefined){const b=m.buildings[a.building],asset=buildingAsset(b.asset),im=cache[asset.file]??=await loadImage(new URL('../dist/assets/'+asset.file,import.meta.url).pathname);rect=buildingRect(b,im);flip=b.flip;}else{const im=cache.titan??=await loadImage(new URL('../dist/assets/titan-prone-v4.webp',import.meta.url).pathname);rect=titanRect(m,im);}
  const x=rect.x+rect.w*(flip?1-a.uv[0]:a.uv[0]),y=rect.y+rect.h*a.uv[1];let best;
  for(const p of queue){if(!g.walkable(p.q,p.r))continue;const a=project(p.q,p.r),distance=Math.hypot(a.x-x,a.y-y);if(!best||distance<best.distance)best={...p,distance};}
  (overrides[l.id]??={})[door.id]=[best.q,best.r];audit.push({location:l.id,door:door.id,at:[best.q,best.r],distance:Math.round(best.distance)});
 }
}
fs.writeFileSync(new URL('../dist/door-approaches-v11.js',import.meta.url),`// Fixed approach cells aligned to the visible thresholds of all 21 entrances.\nconst APPROACHES=${JSON.stringify(overrides,null,1)};\nexport function installDoorApproaches(plans){for(const [id,doors]of Object.entries(APPROACHES))Object.assign(plans[id].obj,doors);}\n`);
fs.writeFileSync(new URL('../docs/door-approaches-v11.json',import.meta.url),JSON.stringify(audit,null,2)+'\n');console.log(JSON.stringify(audit));

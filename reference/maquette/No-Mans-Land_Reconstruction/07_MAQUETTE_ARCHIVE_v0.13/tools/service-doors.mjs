// Offline alignment aid: emits fixed approach coordinates; no runtime layout generation.
import {Game} from '../dist/engine.js';
import {SERVICE_INTERIORS} from '../dist/service-interiors.js';
import {buildingAsset,buildingRect,project} from '../dist/geometry.js';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{loadImage}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/@napi-rs/canvas');
const g=new Game();g.newGame();
for(const spec of SERVICE_INTERIORS){g.enter(spec.parent);g.scene.enemies=[];const b=g.scene.buildings[spec.building],asset=buildingAsset(b.asset),im=await loadImage(new URL('../dist/assets/'+asset.file,import.meta.url).pathname),rect=buildingRect(b,im),x=rect.x+rect.w*(b.flip?1-spec.uv[0]:spec.uv[0]),y=rect.y+rect.h*spec.uv[1];let best=null;
for(let q=0;q<50;q++)for(let r=0;r<50;r++){if(!g.walkable(q,r)||!g.path(g.s.pos,{q,r}).length)continue;const a=project(q,r),d=Math.hypot(a.x-x,a.y-y);if(!best||d<best.d)best={q,r,d};}
console.log(JSON.stringify({id:spec.id,asset:b.asset,at:[best.q,best.r],distance:Math.round(best.d)}));}

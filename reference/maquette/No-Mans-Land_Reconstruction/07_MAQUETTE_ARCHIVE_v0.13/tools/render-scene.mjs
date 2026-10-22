// Offline rendering of the production Canvas code. Does not emulate a browser.
import {createRequire} from 'node:module';
import fs from 'node:fs';
import {Game} from '../dist/engine.js';
import {LOCATIONS} from '../dist/data.js';
import {Renderer} from '../dist/render.js';
import {buildingSprite,buildingRect,titanRect} from '../dist/geometry.js';
const require=createRequire(import.meta.url);
const {createCanvas,loadImage}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/@napi-rs/canvas');
globalThis.devicePixelRatio=1;
globalThis.requestAnimationFrame=()=>0;
globalThis.ResizeObserver=class{observe(){}};
globalThis.document={createElement:()=>createCanvas(1,1),hidden:false};
const canvas=createCanvas(1200,750);
canvas.getBoundingClientRect=()=>({width:1200,height:750});canvas.offsetParent={};
const game=new Game();game.newGame();const r=new Renderer(canvas,game);
game.s.overland.seed=2175;
const event=process.argv.find(a=>a.startsWith('--event='))?.slice(8);
const targets=process.argv.includes('--all')?LOCATIONS.map(l=>l.id):process.argv.slice(2).filter(a=>!a.startsWith('--'));if(!targets.length)targets.push('dusk');
async function atlas(key,n,file){for(let i=0;i<n;i++)r.sprites[key][i]=await loadImage(new URL('../dist/assets/'+file(i)+'.webp',import.meta.url).pathname);}
await atlas('linear',6,i=>'linear-v12-'+i);
await atlas('ioInteriors',6,i=>'io-interior-v10-'+i);await atlas('services',12,i=>'service-v10-'+i);await atlas('freighter',1,()=> 'io-freighter-v10');
await atlas('settlements',18,i=>'settlement-v9-'+i);await atlas('dressing',24,i=>'props-v9-'+i);await atlas('utilities',6,i=>'utility-v9-'+i);await atlas('streetDetails',6,i=>'street-detail-v9-'+i);
await atlas('newBuildings',6,i=>'buildings-v6-'+i);await atlas('newProps',6,i=>'props-v6-'+i);
await atlas('buildings',6,i=>'building-'+i);await atlas('actors',6,i=>'actor-'+i);
await atlas('humans',6,i=>'actors-v2-'+i);await atlas('props',6,i=>'props-v2-'+i);
await atlas('interiors',6,i=>'interiors-v2-'+i);
await atlas('city',8,i=>i<6?'city-v3-'+i:'city-upper-v3-'+(i-6));
await atlas('cityProps',6,i=>'city-props-v3-'+i);await atlas('cityPeople',6,i=>'city-people-v3-'+i);
await atlas('terrain',12,i=>i<6?'terrain-v4-'+i:'terrain-nature-v4-'+(i-6));
r.sprites.terrain[12]=await loadImage(new URL('../dist/assets/interior-wood-v10.webp',import.meta.url).pathname);
for(const [key,file] of [['waste','scenery-waste-v4'],['street','scenery-city-v4'],['exterior','exterior-buildings-v4'],['landmarks','landmarks-v4'],['details','props-detail-v4']])await atlas(key,6,i=>file+'-'+i);
r.sprites.skybridge=await loadImage(new URL('../dist/assets/skybridge-v9.webp',import.meta.url).pathname);
r.sprites.forestTree=await loadImage(new URL('../dist/assets/forest-tree-v4.webp',import.meta.url).pathname);
r.sprites.titan=await loadImage(new URL('../dist/assets/titan-prone-v4.webp',import.meta.url).pathname);
for(const target of targets){
 if(event&&target.startsWith('wild-')){const [col,row]=target.slice(5).split('-').map(Number);game.worldState({col,row}).event=event;}if(!game.enter(target))throw Error('Terrain inconnu : '+target);const position=process.argv.find(a=>a.startsWith('--position='))?.slice(11).split(',').map(Number);if(position)game.s.pos={q:position[0],r:position[1]};r.rebuild();r.zoom=+(process.argv.find(a=>a.startsWith('--zoom='))?.slice(7)||.34);
 const p=r.project(game.scene.focus.q,game.scene.focus.r);r.cam={x:p.x,y:p.y-45};if(process.argv.includes('--focus-player')){const player=r.project(game.s.pos.q,game.s.pos.r);r.cam={x:player.x,y:player.y-50};}
 if(process.argv.includes('--overview')){const scene=game.scene,bb=scene.bounds,points=bb?[[bb[0],bb[1]],[bb[2],bb[1]],[bb[2],bb[3]],[bb[0],bb[3]]].map(([q,rr])=>r.project(q,rr)):null,extents=bb?[{x:Math.min(...points.map(p=>p.x)),y:Math.min(...points.map(p=>p.y))-80,w:Math.max(...points.map(p=>p.x))-Math.min(...points.map(p=>p.x)),h:Math.max(...points.map(p=>p.y))-Math.min(...points.map(p=>p.y))+80}]:[{x:-scene.size*32,y:0,w:scene.size*64,h:scene.size*32}];for(const b of scene.buildings){const im=buildingSprite(r,b);if(im)extents.push(buildingRect(b,im));}if(scene.titan)extents.push(titanRect(scene,r.sprites.titan));const x0=Math.min(...extents.map(b=>b.x)),x1=Math.max(...extents.map(b=>b.x+b.w)),y0=Math.min(...extents.map(b=>b.y)),y1=Math.max(...extents.map(b=>b.y+b.h));r.cam={x:(x0+x1)/2,y:(y0+y1)/2};r.zoom=Math.min((1200-80)/(x1-x0),(750-70)/(y1-y0));}
 r.draw(1800);
 const path='/workspace/scratch/00d29d1aab63/scene-'+target+(event?'-'+event:'')+(position?'-proximity':'')+'.png';
 fs.writeFileSync(path,canvas.toBuffer('image/png'));console.log(path);
}

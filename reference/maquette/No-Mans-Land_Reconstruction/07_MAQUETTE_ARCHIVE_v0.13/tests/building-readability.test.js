import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createRequire} from 'node:module';
import {Game,makeScene} from '../dist/engine.js';
import {LOCATIONS,OBJECTS} from '../dist/data.js';
import {Renderer} from '../dist/render.js';
import {buildingAsset,buildingRect,buildingBoost,entityPoint,project} from '../dist/geometry.js';
import {accessForBuilding,proximityOpacity,accessMarkerRect} from '../dist/building-access.js';
const require=createRequire(import.meta.url),{createCanvas,loadImage}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/@napi-rs/canvas');
const assets={};
const start=()=>{const g=new Game();g.newGame();return g;};
async function asset(file){return assets[file]??=await loadImage(new URL('../dist/assets/'+file,import.meta.url).pathname);}
async function renderer(g){const r=Object.create(Renderer.prototype);Object.assign(r,{game:g,sprites:{buildings:[],newBuildings:[],settlements:[],exterior:[],city:[],terrain:[]},cam:{x:0,y:0},width:1200,height:750,zoom:1});for(const [family,n,prefix]of [['buildings',6,'building'],['newBuildings',6,'buildings-v6'],['settlements',18,'settlement-v9'],['exterior',6,'exterior-buildings-v4'],['city',6,'city-v3']])for(let i=0;i<n;i++)r.sprites[family][i]=await asset(prefix+'-'+i+'.webp');r.sprites.city[6]=await asset('city-upper-v3-0.webp');r.sprites.city[7]=await asset('city-upper-v3-1.webp');r.sprites.titan=await asset('titan-prone-v4.webp');return r;}
test('whole-world scale audit honours every authored height and shrinks collisions inside the original parcels',async()=>{const audit=JSON.parse(fs.readFileSync(new URL('../docs/building-scale-v11.json',import.meta.url)));assert.equal(audit.length,495);assert.equal(new Set(audit.map(a=>a.location)).size,31);for(const a of audit){const b=makeScene(a.location).buildings[a.index];assert.ok(b.q>=a.before.q&&b.r>=a.before.r&&b.q+b.w<=a.before.q+a.before.w&&b.r+b.d<=a.before.r+a.before.d,a.location+'/'+a.index);assert.ok(b.w*b.d<=a.before.w*a.before.d);}for(const l of LOCATIONS.filter(l=>!l.interior))for(const b of makeScene(l.id).buildings.filter(b=>!b.wall)){const im=await asset(buildingAsset(b.asset).file),rect=buildingRect(b,im);assert.ok(rect.h<=b.h*1.25*1.5+.01,l.id+'/'+b.asset+' exceeds height');}});
test('all 21 door thresholds stay close to their visible facade and remain walkable',async()=>{const g=start(),r=await renderer(g);let count=0;for(const l of LOCATIONS.filter(l=>!l.interior)){g.enter(l.id);for(const o of g.scene.objects.filter(o=>OBJECTS[o.id]?.type==='door')){const a=entityPoint(r,o),p=project(o.q,o.r);assert.ok(Math.hypot(a.x-p.x,a.y-p.y)<40,l.id+'/'+o.id);assert.ok(g.walkable(o.q,o.r,true));count++;}}assert.equal(count,21);});
test('building access badges distinguish real entrances, locks and nonvisitable structures without guessing',()=>{for(const l of LOCATIONS.filter(l=>!l.interior)){const m=makeScene(l.id);m.buildings.forEach((b,i)=>{if(b.wall)return;const a=accessForBuilding(m,i,OBJECTS),doors=m.objects.filter(o=>o.anchor?.building===i&&OBJECTS[o.id]?.type==='door');assert.equal(a.state==='closed',doors.length===0,l.id+'/'+i);if(a.state!=='closed')assert.ok(doors.includes(a.door));});}const m=makeScene('junk'),door=m.objects.find(o=>o.id==='backdoor'),i=door.anchor.building;assert.equal(accessForBuilding(m,i,OBJECTS).state,'locked');assert.equal(accessForBuilding(m,i,OBJECTS,{backdoor:true}).state,'open');});
test('proximity restores whole-building transparency on every facade and stays opaque at a distance',()=>{const b={q:10,r:10,w:4,d:3};for(const p of [{q:9,r:11},{q:14,r:11},{q:11,r:9},{q:11,r:13}])assert.equal(proximityOpacity(b,p),.48);assert.equal(proximityOpacity(b,{q:2,r:2}),1);assert.equal(proximityOpacity(b,{q:20,r:20}),1);});
test('the actual renderer draws the complete model once with proximity opacity, including when the player is in front',async()=>{const g=start(),r=await renderer(g),b=g.scene.buildings[15],canvas=createCanvas(1500,1500),c=canvas.getContext('2d'),draw=c.drawImage.bind(c),alphas=[];c.drawImage=(...args)=>{alphas.push(c.globalAlpha);return draw(...args);};g.s.pos={q:b.q+b.w,r:b.r+b.d-1};r.building(c,b);assert.equal(alphas.length,1);assert.ok(Math.abs(alphas[0]-.48)<.01);alphas.length=0;g.s.pos={q:49,r:49};r.building(c,b);assert.deepEqual(alphas,[1]);});
test('entrance badges stay readable and tappable at every supported zoom and target the actual door',async()=>{const g=start(),r=await renderer(g),c=createCanvas(1200,750).getContext('2d');for(const zoom of [.25,.75,1.15,2.4]){r.zoom=zoom;const b=g.scene.buildings[15],rect=buildingRect(b,r.sprites.settlements[2]);r.cam={x:rect.x+rect.w/2,y:rect.y};r.accessMarkers(c);const target=r.accessTargets.find(t=>t.door.id==='dusk-hotel-door');assert.ok(target);assert.equal(target.w,78);assert.equal(target.h,26);const hit=r.hitAt(target.x+target.w/2,target.y+target.h/2);assert.equal(hit.id,'dusk-hotel-door');assert.equal(hit.type,'object');}assert.ok(accessMarkerRect({x:100,y:100},'locked').w>78);});
test('a save on a newly freed courtyard remains valid without moving the character or changing inventory',()=>{const g=start();g.enter('steel');g.s.pos={q:2,r:3};assert.ok(g.walkable(2,3));const n=new Game();assert.ok(n.import(g.s));assert.deepEqual(n.s.pos,g.s.pos);assert.deepEqual(n.s.inventory,g.s.inventory);});
test('v13 enlarges small model families by 25 to 50 percent with fixed ground baselines',async()=>{for(const l of LOCATIONS.filter(l=>!l.interior))for(const b of makeScene(l.id).buildings.filter(b=>!b.wall)){const im=await asset(buildingAsset(b.asset).file),rect=buildingRect(b,im),points=[[b.q,b.r],[b.q+b.w,b.r],[b.q+b.w,b.r+b.d],[b.q,b.r+b.d]].map(p=>project(...p)),left=Math.min(...points.map(p=>p.x)),right=Math.max(...points.map(p=>p.x)),bottom=Math.max(...points.map(p=>p.y))+6,oldH=Math.min((right-left)*1.06*im.height/im.width,b.h||350);assert.ok(Math.abs(rect.h-oldH*1.25*buildingBoost(b,oldH*1.25))<1e-8);assert.ok(Math.abs(rect.w-oldH*im.width/im.height*1.25*buildingBoost(b,oldH*1.25))<1e-8);assert.ok(Math.abs(rect.x+rect.w/2-(left+right)/2)<1e-8);assert.ok(Math.abs(rect.y+rect.h-bottom)<1e-8);assert.deepEqual(buildingRect(b,im),rect);}});
test('inaccessible buildings draw no badge while all real entrances keep their marker',async()=>{const g=start(),r=await renderer(g),c=createCanvas(1200,750).getContext('2d'),texts=[],fill=c.fillText.bind(c);c.fillText=(s,...args)=>{texts.push(s);return fill(s,...args);};r.zoom=.1;r.cam={x:0,y:800};r.accessMarkers(c);const doors=g.scene.objects.filter(o=>OBJECTS[o.id]?.type==='door');assert.equal(r.accessTargets.length,doors.length);assert.equal(texts.length,doors.length);assert.ok(texts.every(s=>s==='ENTRER'||s==='VERROUILLÉ'));});

test('visible facade pixels open their real doors while transparent margins and unvisitable buildings do not',async()=>{
 globalThis.document={createElement:()=>createCanvas(1,1)};
 const g=start(),r=await renderer(g);r.accessTargets=[];
 let checked=0,flipped=0;
 for(const l of LOCATIONS.filter(l=>!l.interior)){
  g.enter(l.id);
  for(const door of g.scene.objects.filter(o=>OBJECTS[o.id]?.type==='door'&&o.anchor?.building!==undefined)){
   const b=g.scene.buildings[door.anchor.building],im=r.sprites[buildingAsset(b.asset).family][buildingAsset(b.asset).index],box=buildingRect(b,im);let found=false;
   r.zoom=.75;r.cam={x:box.x+box.w/2,y:box.y+box.h/2};
   for(let v=.2;v<.85&&!found;v+=.1)for(let u=.15;u<.9&&!found;u+=.1){const p={x:box.x+box.w*u,y:box.y+box.h*v};if(r.spriteAlpha(im,box,!!b.flip,p)<200)continue;const x=(p.x-r.cam.x)*r.zoom+r.width/2,y=(p.y-r.cam.y)*r.zoom+r.height/2,hit=r.hitAt(x,y);if(hit?.id===door.id)found=true;}
   assert.ok(found,l.id+'/'+door.id+' has clickable facade');if(b.flip)flipped++;checked++;
  }
 }
 assert.equal(checked,20);assert.ok(flipped>0);
 g.enter('dusk');const b=g.scene.buildings[1],im=r.sprites.settlements[0],box=buildingRect(b,im);assert.equal(r.spriteAlpha(im,box,!!b.flip,{x:box.x-1,y:box.y}),0);
 assert.equal(r.buildingHitAt(-10000,-10000),null);
});

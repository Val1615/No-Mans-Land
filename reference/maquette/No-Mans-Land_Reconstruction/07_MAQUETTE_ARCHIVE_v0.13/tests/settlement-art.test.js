import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {Game,makeScene} from '../dist/engine.js';
import {LOCATIONS} from '../dist/data.js';
import {SETTLEMENT_REVISIONS} from '../dist/settlement-v9.js';
import {sceneryAsset} from '../dist/scenery.js';
import {entityPoint} from '../dist/geometry.js';

test('every solid scenery type has a real raster asset; no box fallback can conceal a missing model',()=>{
 for(const l of LOCATIONS){const scene=makeScene(l.id);for(const p of [...scene.props,...scene.objects.filter(o=>!o.anchor).map(o=>({kind:o.visual}))]){
  if(p.kind==='dune')continue;const a=sceneryAsset(p.kind);assert.ok(a,l.id+'/'+p.kind);assert.ok(fs.existsSync(new URL('../dist/assets/'+a.file,import.meta.url)),a.file);
 }}
});
test('reconstructed quarters have distinct non-overlapping building footprints and decor stays outside structures',()=>{
 const signatures=new Set();for(const id of Object.keys(SETTLEMENT_REVISIONS)){const m=makeScene(id);const signature=JSON.stringify([m.buildings,m.roads]);assert.ok(!signatures.has(signature),id);signatures.add(signature);
 for(let i=0;i<m.buildings.length;i++){const a=m.buildings[i];for(const b of m.buildings.slice(i+1))assert.ok(!(a.q<b.q+b.w&&a.q+a.w>b.q&&a.r<b.r+b.d&&a.r+a.d>b.r),id+'/'+i);}
 for(const p of m.props)assert.ok(!m.buildings.some(b=>p.q>=b.q&&p.q<b.q+b.w&&p.r>=b.r&&p.r<b.r+b.d),id+'/'+p.kind+' '+p.q+','+p.r);
 }
});
test('Dusk structures use small physical footprints and each quarter retains reachable circulation',()=>{
 for(const id of ['dusk','dusk-courts','dusk-workshops']){const g=new Game();g.newGame();g.enter(id);for(const b of g.scene.buildings)assert.ok(b.w*b.d<=64,id);assert.ok(g.scene.buildings.length>=18,id);assert.ok(g.path(g.scene.spawn,g.scene.exit).length,id);}
});
test('mirror variants move the visual doorway with the facade while leaving its vertical position intact',()=>{
 const b={q:2,r:3,w:4,d:4,asset:'b0',h:200},im={width:100,height:80};const r={game:{scene:{buildings:[b]}},sprites:{buildings:[im]}};const o={q:4,r:7,anchor:{building:0,uv:[.2,.85]}};const a=entityPoint(r,o);b.flip=true;const z=entityPoint(r,o);assert.ok(z.x>a.x);assert.equal(z.y,a.y);
});

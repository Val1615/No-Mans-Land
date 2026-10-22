import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {Game,makeScene} from '../dist/engine.js';
import {LOCATIONS} from '../dist/data.js';
import {CITY_LOCATIONS,CITY_LEVELS} from '../dist/city-data.js';
import {buildingAsset} from '../dist/geometry.js';
import {SCENE_PLANS} from '../dist/scenes.js';

test('all city districts have different circulation and building footprints',()=>{
 const signatures=new Set();
 for(const l of CITY_LOCATIONS){const m=makeScene(l.id);const shape=JSON.stringify([m.buildings.map(b=>[b.q,b.r,b.w,b.d]),m.roads]);assert.ok(!signatures.has(shape),'duplicate '+l.id);signatures.add(shape);}
});
test('Big Larry is an uninhabited vitrified impact, including when an old encounter is loaded',()=>{
 const m=makeScene('crater');assert.equal(m.buildings.length,0);assert.equal(m.npcs.length,0);assert.equal(m.enemies.length,0);assert.ok(m.areas.some(a=>a.material==='glass'));assert.ok(m.props.some(p=>p.kind==='minegate'));
 const g=new Game();g.newGame();g.enter('titan');const old=structuredClone(g.scene.enemies);g.enter('crater');delete g.s.worldRevision;g.s.flags['enemies-crater']=old;g.s.combat={turn:2,phase:'player'};g.s.inventory.antirad=9;g.s.quests.main=3;
 const n=new Game();assert.ok(n.import(g.s));assert.equal(n.scene.enemies.length,0);assert.equal(n.s.combat,null);assert.equal(n.s.inventory.antirad,9);assert.equal(n.s.quests.main,3);
});
test('the exterior perimeter stays arid and uses no interior cyberpunk tower assets',()=>{
 for(const l of CITY_LOCATIONS.filter(l=>!l.dome)){const m=makeScene(l.id);assert.equal(m.ground,'sand',l.id);assert.ok(m.buildings.every(b=>!b.asset.startsWith('c')),l.id);}
 assert.equal(CITY_LOCATIONS.find(l=>l.id==='under').cityLevel,'under');assert.ok(fs.existsSync(new URL('../dist/assets/'+CITY_LEVELS.under.file,import.meta.url)));
});
test('China Lake water blocks movement and the shoreline remains connected',()=>{
 const g=new Game();g.newGame();g.enter('china');assert.equal(g.walkable(13,12),false);assert.ok(g.scene.links.some(l=>l.kind==='lanterns'));assert.ok(g.path(g.scene.spawn,{q:23,r:18}).length>0);assert.ok(g.path(g.scene.spawn,{q:6,r:7}).length>0);
});
test('solid dressing blocks movement, inhabitants avoid scenery and every building has a model',()=>{
 for(const l of LOCATIONS){const g=new Game();g.newGame();g.enter(l.id);for(const p of g.scene.props.filter(p=>p.solid))assert.equal(g.walkable(p.q,p.r),false,l.id+'/'+p.kind);for(const a of [...g.scene.crowd,...g.scene.npcs,...g.scene.enemies])assert.equal(g.scene.blocked.has(a.q+','+a.r),false,l.id+'/'+(a.id||'passer-by'));for(const b of g.scene.buildings.filter(b=>!b.wall)){assert.ok(fs.existsSync(new URL('../dist/assets/'+buildingAsset(b.asset).file,import.meta.url)),l.id+'/'+b.asset);}}
});
test('migration repositions obsolete enemy coordinates without resurrecting or healing them',()=>{
 const g=new Game();g.newGame();g.enter('titan');g.scene.enemies[0].q=24;g.scene.enemies[0].r=24;g.scene.enemies[0].hp=3;g.scene.enemies[1].dead=true;g.persistEnemies();delete g.s.worldRevision;const n=new Game();assert.ok(n.import(g.s));assert.deepEqual([n.scene.enemies[0].q,n.scene.enemies[0].r],SCENE_PLANS.titan.enemies[0]);assert.equal(n.scene.enemies[0].hp,3);assert.equal(n.scene.enemies[1].dead,true);
});
test('new battlefield barriers provide real cover',()=>{
 const g=new Game();g.newGame();g.enter('eastbase');const p=g.scene.props.find(p=>p.kind==='sandbag');assert.ok(g.cover({q:p.q,r:p.r+1}));
});

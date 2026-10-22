import test from 'node:test';
import assert from 'node:assert/strict';
import {Game,DIRS,dist} from '../dist/engine.js';
import {LOCATIONS,OBJECTS} from '../dist/data.js';
import {buildingBoost} from '../dist/geometry.js';
test('small houses, services and larger structures receive the intended additional scale',()=>{
 assert.equal(buildingBoost({asset:'v0'},162.5),1.5);assert.equal(buildingBoost({asset:'x5'},225),1.5);assert.equal(buildingBoost({asset:'b0'},206),1.35);assert.equal(buildingBoost({asset:'v2'},260),1.25);assert.equal(buildingBoost({asset:'c0'},380),1);
});
test('each real interior can be approached from the actual zone arrival and entered with or without Nilo',()=>{
 for(const companion of [false,true])for(const l of LOCATIONS.filter(l=>l.interior)){
  const g=new Game();g.newGame({origin:'augmente'});if(companion)g.recruitCompanion();g.enter(l.parent);g.scene.enemies=[];
  const door=g.scene.objects.find(o=>OBJECTS[o.id]?.target===l.id);g.prepareV2().opened[door.id]=true;
  const d=g.interact(door.id),c=d?.choices.find(c=>c.label==='Entrer');assert.ok(c,l.id);c.act();assert.equal(g.s.loc,l.id);
 }
});
test('door approach uses a real free threshold when it gives the shortest route',()=>{
 const g=new Game();g.newGame();const door=g.scene.objects.find(o=>o.id==='dusk-hotel-door');
 g.s.pos={q:door.q+2,r:door.r};g.scene.blocked.delete(`${g.s.pos.q},${g.s.pos.r}`);
 const d=g.interact(door.id);assert.ok(d?.choices.some(c=>c.label==='Entrer'));assert.ok(dist(g.s.pos,door)<=1);
 d.choices.find(c=>c.label==='Entrer').act();assert.equal(g.s.loc,'dusk-hotel');
});
test('a blocked door reports its obstruction and combat refusal in the dialogue',()=>{
 const g=new Game();g.newGame();g.scene.blocked=new Set(Array.from({length:50},(_,q)=>Array.from({length:50},(_,r)=>q+','+r)).flat());
 const d=g.interact('dusk-hotel-door');assert.match(d.text,/obstrué/);assert.equal(g.s.loc,'dusk');
 g.s.combat={phase:'player',turn:1};assert.match(g.interact('dusk-hotel-door').text,/combat/);
});

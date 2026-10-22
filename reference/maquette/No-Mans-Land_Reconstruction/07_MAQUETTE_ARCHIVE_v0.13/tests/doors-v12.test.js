import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {Game,dist} from '../dist/engine.js';
import {LOCATIONS,OBJECTS} from '../dist/data.js';
const start=()=>{const g=new Game();g.newGame({origin:'augmente'});g.recruitCompanion();return g;};
test('all 21 interiors support repeated door round trips with Nilo alongside the player',()=>{
 const g=start();let count=0;
 for(const l of LOCATIONS.filter(l=>l.interior)){
  g.enter(l.parent);g.scene.enemies=[];
  const d=g.scene.objects.find(o=>OBJECTS[o.id]?.target===l.id);assert.ok(d,l.id);
  g.prepareV2().opened[d.id]=true;g.s.pos={q:d.q,r:d.r};g.placeCompanion();
  for(let repeat=0;repeat<2;repeat++){
   assert.ok(g.enterInterior(l.id),l.id+' entry '+repeat);
   assert.ok(g.move(g.scene.exit.q,g.scene.exit.r));
   assert.ok(g.leaveInterior(),l.id+' return '+repeat);
   assert.equal(g.s.loc,l.parent);assert.ok(dist(g.s.pos,d)<=1);
   const ally=g.prepareCompanion();assert.equal(ally.loc,l.parent);
   assert.ok(dist(g.s.pos,ally.pos)<=2,l.id+' companion at return');
   assert.equal(g.scene.npcs.filter(n=>n.id==='nilo').length,0);
  }count++;
 }assert.equal(count,21);
});
test('old saves with Nilo stranded at the parent spawn repair once, while waiting companions stay put',()=>{
 for(const status of ['following','waiting']){
  const g=start(),d=g.scene.objects.find(o=>o.id==='dusk-hotel-door');
  g.s.pos={q:d.q,r:d.r};g.s.flags['return-dusk-hotel']={...g.s.pos};
  const ally=g.prepareCompanion();ally.status=status;ally.pos={...g.scene.spawn};
  if(status==='waiting')g.s.companion=null;
  const old={...ally.pos},n=new Game();assert.ok(n.import(g.s));
  assert.equal(n.s.flags.doorReturnFixed12,true);
  if(status==='following')assert.ok(dist(n.s.pos,n.prepareCompanion().pos)<=2);
  else assert.deepEqual(n.prepareCompanion().pos,old);
  n.prepareCompanion().pos={...n.scene.spawn};const save=structuredClone(n.s),again=new Game();assert.ok(again.import(save));assert.deepEqual(again.prepareCompanion().pos,save.allies.nilo.pos);
 }
});
test('an actual door choice explains why an entry is refused instead of silently closing',()=>{
 const g=start(),d=g.scene.objects.find(o=>o.id==='dusk-hotel-door');g.s.pos={q:d.q,r:d.r};g.placeCompanion();
 g.prepareCompanion().status='downed';g.prepareCompanion().hp=0;
 const dialog=g.interact(d.id),choice=dialog.choices.find(c=>c.label.includes('Entrer'));
 assert.ok(choice);assert.match(choice.act(),/Nilo.*terre/);assert.equal(g.s.loc,'dusk');
 g.prepareCompanion().status='following';g.prepareCompanion().hp=10;g.placeCompanion();
 g.s.combat={phase:'player',turn:1};assert.match(g.interiorBlockReason('dusk-hotel'),/combat/);
 g.s.combat=null;g.enter('junk');const locked=g.scene.objects.find(o=>o.id==='backdoor');g.s.pos={q:locked.q,r:locked.r};g.placeCompanion();assert.match(g.interiorBlockReason('backroom'),/verrouillée/);
});
test('the deployed HTML loads a versioned module graph identical to the tested production sources',()=>{
 const root=new URL('../dist/',import.meta.url),html=fs.readFileSync(new URL('index.html',root),'utf8'),entry=html.match(/src="(runtime-v\d+)\/app\.js"/)[1],manifest=JSON.parse(fs.readFileSync(new URL(entry+'/manifest.json',root)));
 assert.equal(manifest.directory,entry);
 for(const file of fs.readdirSync(root).filter(f=>f.endsWith('.js'))){const canonical=fs.readFileSync(new URL(file,root)),packaged=fs.readFileSync(new URL(entry+'/'+file,root));assert.deepEqual(packaged,canonical,file);assert.equal(createHash('sha256').update(packaged).digest('hex'),manifest.files[file]);}
});

import assert from 'node:assert/strict';
import {LOCATIONS,OBJECTS} from '../dist/data.js';
// Existing quest tests follow relocated staff through their actual public doors.
export function visitNpc(g,id){
 if(g.scene.npcs.some(n=>n.id===id))return;
 const destination=LOCATIONS.find(l=>l.npcs.includes(id));assert.ok(destination,id);
 assert.ok(destination.interior,id+' moved to interior');
 const here=LOCATIONS.find(l=>l.id===g.s.loc);
 if(here.interior){assert.ok(g.move(g.scene.exit.q,g.scene.exit.r));assert.ok(g.leaveInterior());}
 assert.equal(g.s.loc,destination.parent,id+' parent');
 const door=g.scene.objects.find(o=>OBJECTS[o.id]?.target===destination.id);assert.ok(door,id+' door');
 const d=g.interact(door.id);assert.ok(d,id+' approach');const c=d.choices.find(c=>c.label==='Entrer');assert.ok(c);c.act();assert.equal(g.s.loc,destination.id);
}

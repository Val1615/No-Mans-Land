import assert from 'node:assert/strict';
// Quest fixtures use a quiet road; encounter behavior has its own tests.
export function travel(g,id){const random=g.random;g.random=()=>.99;try{const ok=g.travel(id);if(!ok)return false;for(let i=0;i<440&&g.s.overland.route.length;i++){assert.equal(g.s.overland.paused,false,'unexpected interrupted journey');assert.ok(g.advanceJourney());}assert.equal(g.s.loc,id);return true;}finally{g.random=random;}}

// Coordinate and route QA only; this is not a browser/layout screenshot.
import {createRequire} from 'node:module';
import fs from 'node:fs';
import {Game} from '../dist/engine.js';
import {WORLD_CELLS,cellKey,cellLabel,locationCell} from '../dist/world.js';
const require=createRequire(import.meta.url),{createCanvas,loadImage}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/@napi-rs/canvas');
const g=new Game();g.newGame();g.random=()=>.99;g.travel('junk');g.advanceJourney();
const canvas=createCanvas(1100,1000),c=canvas.getContext('2d'),map=await loadImage(new URL('../dist/assets/world-map.svg',import.meta.url).pathname);
c.drawImage(map,0,0);const w=g.s.overland,route=new Set(w.route.map(cellKey));
for(const p of WORLD_CELLS){c.strokeStyle='#a5bb7c55';c.lineWidth=1;c.strokeRect(p.col*50,p.row*50,50,50);if(route.has(cellKey(p))){c.fillStyle='#d0b87665';c.fillRect(p.col*50+1,p.row*50+1,48,48);}c.fillStyle='#d4d5b088';c.font='9px monospace';c.fillText(cellLabel(p),p.col*50+4,p.row*50+12);}
c.fillStyle='#f2d995';c.beginPath();c.arc(w.position.col*50+25,w.position.row*50+25,10,0,7);c.fill();
fs.writeFileSync('/workspace/scratch/00d29d1aab63/regional-grid-qa.png',canvas.toBuffer('image/png'));console.log('Regional coordinates rendered.');

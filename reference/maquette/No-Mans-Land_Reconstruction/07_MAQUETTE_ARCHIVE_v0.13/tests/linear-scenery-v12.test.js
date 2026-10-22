import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createRequire} from 'node:module';
import {makeScene} from '../dist/engine.js';
import {LOCATIONS} from '../dist/data.js';
import {project} from '../dist/geometry.js';
import {sceneryAsset,drawLink} from '../dist/scenery.js';
import {linkPanels,RASTER_LINKS,LINEAR_ANCHORS} from '../dist/linear-scenery-v12.js';
const require=createRequire(import.meta.url),{createCanvas,loadImage}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/@napi-rs/canvas');
test('fixed infrastructure routes join short upright panels in both axes without moving their endpoints',()=>{
 let count=0;
 for(const l of LOCATIONS)for(const link of makeScene(l.id).links||[]){if(!RASTER_LINKS.has(link.kind))continue;const ps=linkPanels(link);assert.ok(ps.length,l.id);assert.deepEqual(ps[0].from,link.from);assert.deepEqual(ps.at(-1).to,link.to);for(let i=0;i<ps.length;i++){const p=ps[i];assert.ok(p.from[0]===p.to[0]||p.from[1]===p.to[1]);assert.ok(Math.abs(p.to[0]-p.from[0])+Math.abs(p.to[1]-p.from[1])<=(link.kind==='balustrade'?2:3)+1e-8);if(i)assert.deepEqual(ps[i-1].to,p.from);count++;}}
 assert.ok(count>100);
});
test('all six measured raster variants render actual textured panels without broad placeholder strokes',async()=>{
 const kinds=['chainFenceQ','chainFenceR','stoneBalustradeQ','stoneBalustradeR','insulatedPipeQ','insulatedPipeR'],r={project,sprites:{linear:[]}},c=createCanvas(900,800).getContext('2d'),draw=c.drawImage.bind(c);let draws=0;c.drawImage=(...args)=>{draws++;return draw(...args);};c.stroke=()=>{throw Error('native placeholder stroke');};
 const manifest=JSON.parse(fs.readFileSync(new URL('../art-source/linear-v12-manifest.json',import.meta.url)));
 for(let i=0;i<6;i++){const asset=sceneryAsset(kinds[i]);assert.equal(asset.file,'linear-v12-'+i+'.webp');r.sprites.linear[i]=await loadImage(new URL('../dist/assets/'+asset.file,import.meta.url).pathname);assert.deepEqual(LINEAR_ANCHORS[i].ground,manifest.sprites[i].ground_endpoints_uv);const axis=i%2,link={kind:['fence','balustrade','pipe'][Math.floor(i/2)],from:[8,8],to:axis?[8,11]:[11,8]};const before=draws;drawLink(r,c,link);assert.equal(draws-before,linkPanels(link).length);}
 assert.ok(c.getImageData(0,0,900,800).data.some((n,i)=>i%4===3&&n>0));
});

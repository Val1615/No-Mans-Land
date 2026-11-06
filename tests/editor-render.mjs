import vm from 'node:vm';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const vendorContext=vm.createContext({console});const vendor=new vm.SourceTextModule(fs.readFileSync('vendor/three.module.js','utf8'),{context:vendorContext});await vendor.link(()=>{throw Error('Unexpected vendor dependency');});await vendor.evaluate();const RealThree=vendor.namespace;
const unitsModule=new vm.SourceTextModule(fs.readFileSync('src/data/units.js','utf8'),{context:vendorContext});await unitsModule.link(()=>{});await unitsModule.evaluate();const UNITS=unitsModule.namespace.UNITS;
const context=vm.createContext({console,innerWidth:1200,innerHeight:900,devicePixelRatio:1,performance,addEventListener(){},document:{getElementById(){return null;},createElement(){return {width:2,height:2,dataset:{},style:{},classList:{contains(){return false;}},remove(){},offsetWidth:0,offsetHeight:0,getContext(){return {drawImage(){},getImageData(){return {data:new Uint8Array(16).fill(255)};}};}};}}});
let rendered;
class TestRenderer{setPixelRatio(){}setSize(){}render(scene,camera){scene.updateMatrixWorld(true);camera.updateMatrixWorld(true);rendered=scene;}}
class TestLoader{load(){return new RealThree.Texture();}}
const three={...RealThree,WebGLRenderer:TestRenderer,TextureLoader:TestLoader};
const mod=(exports)=>new vm.SyntheticModule(Object.keys(exports),function(){for(const[k,v]of Object.entries(exports))this.setExport(k,v);},{context});
const dependencies={'three':mod(three),'../data/units.js':mod({UNITS}),'../core/grid.js':mod({wallsOf:()=>[]}),'./textures.js?v=editor2':mod({groundTexture:()=>new RealThree.Texture(),margeTexture:()=>new RealThree.Texture(),SKIN:{b:{width:2,height:2}}})};
const source=new vm.SourceTextModule(fs.readFileSync('src/render/view.js','utf8'),{context});await source.link(s=>dependencies[s]);await source.evaluate();
const location=()=>({id:'dusk_q1',kind:'exterior',size:{w:48,d:36},ground:{},buildings:[{id:'house',sprite:'b',x:1,z:8,w:7,d:5}],props:[]});
const state={location:'dusk_q1',player:{x:0,z:0,path:[],heading:0},companion:{x:0,z:0,path:[],mode:'off'},npcs:{},discovered:{},combat:null};
const world={LOCATIONS:{dusk_q1:location()},DOORS:[],NPCS:[],COMPANION:{sprite:'nilo'}};
const sprites={player:{height_m:1.8,px:[50,100]},nilo:{height_m:1.8,px:[50,100]}};
const view=source.namespace.createView({getBoundingClientRect:()=>({left:0,top:0,width:1200,height:900})},{world,state},sprites,{b:{px:[400,300],anchor:[200,300]}},{appendChild(){}});
const building=()=>{let found;rendered.traverse(s=>{if(s.userData.buildingId==='house')found=s;});return found;};
view.setCamera({x:24,z:18,ppm:23});view.render();assert.equal(building().position.x,8);
// A restored/imported document replaces LOCATIONS. All later changes must render it.
world.LOCATIONS={dusk_q1:location()};world.LOCATIONS.dusk_q1.buildings[0].x=11;world.LOCATIONS.dusk_q1.buildings[0].k=1.5;
view.invalidate();view.render();assert.equal(building().position.x,18,'renderer must use current document after load/undo/reset');assert.equal(building().scale.x,12,'renderer must show updated scale');
world.LOCATIONS.dusk_q1.buildings[0].x=15;view.invalidate();view.render();assert.equal(building().position.x,22);
const liveSprite=building();world.LOCATIONS.dusk_q1.buildings[0].x=17;world.LOCATIONS.dusk_q1.buildings[0].k=.75;view.editorUpdate();view.render();assert.equal(building(),liveSprite,'drag must reuse existing sprite');assert.equal(building().position.x,24);assert.equal(building().scale.x,6);const point=view.editorGround(0,0);assert(Number.isFinite(point.x)&&Number.isFinite(point.z),'picking must work beyond terrain bounds');
console.log('PASS: actual Three.js scene positions and sprite scale after document replacement and subsequent edits. GPU output not exercised.');

world.editorLayers={zone:{visible:false},building:{visible:false},prop:{visible:false},actor:{visible:false}};view.render();assert.equal(building().visible,false);let player;rendered.traverse(s=>{if(s.userData.actor==='player')player=s;});assert.equal(player.visible,false);
world.testing=true;view.render();assert.equal(building().visible,true);assert.equal(player.visible,true);world.testing=false;
world.editorLayers.actor.visible=true;world.NPCS=[{id:'placed_nilo',sprite:'nilo',name:'Nilo',location:'dusk_q1',x:18,z:19,editorScale:1.25}];view.invalidate();view.render();let npc;rendered.traverse(s=>{if(s.userData.npc==='placed_nilo')npc=s;});assert(npc);assert.equal(npc.position.x,18);world.NPCS[0].x=21;view.editorUpdate();view.render();assert.equal(npc.position.x,21);console.log('PASS: independent Three.js visibility, full test-mode visibility, placed NPC rendering and live movement.');

const cameraModule=new vm.SourceTextModule(fs.readFileSync('editor/camera.js','utf8'),{context:vendorContext});await cameraModule.link(()=>{});await cameraModule.evaluate();const analyticProject=cameraModule.namespace.project;
const cameraCase={x:17,z:11,ppm:41,cx:720,cy:430};view.setCamera(cameraCase);view.render();
for(const point of [{x:1,z:2},{x:17,z:11},{x:34,z:23}]){const expected=analyticProject(cameraCase,point),actual=view.project(point.x,0,point.z);assert(Math.abs(expected.x-actual.x)<1e-6);assert(Math.abs(expected.y-actual.y)<1e-6);const inverse=view.editorGround(actual.x,actual.y);assert(Math.abs(inverse.x-point.x)<1e-6);assert(Math.abs(inverse.z-point.z)<1e-6);}
console.log('PASS: actual Three camera agrees with shared projection and ground picking at an offset viewport center.');

const beforePaintSprite=building();world.LOCATIONS.dusk_q1.ground.paint=[{x:1,z:1,w:3,d:2,skin:"g_asphalt"}];view.refreshGround();view.render();assert.equal(building(),beforePaintSprite,"painting refreshes only the ground texture, preserving scene objects");console.log("PASS: terrain repaint keeps the current Three scene and sprites.");

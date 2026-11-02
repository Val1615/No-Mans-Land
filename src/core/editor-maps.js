import {REFERENCE_LOCATIONS,REFERENCE_INTERIORS} from '../../editor/base.js';
import {validate} from '../../editor/model.js';
// Only editable map geometry overrides native data. Executable conditions,
// scripted transitions, dialogue IDs and all other regions stay native.
export function applyEditorProject(source,input,base){
 if(!input)return {...source,editorProject:null};const project=validate(input,base),scope=new Set(Object.keys(project.locations)),LOCATIONS={...source.LOCATIONS},originalNPC=new Map(source.NPCS.map(n=>[n.id,n]));
 const permitted=new Set([...REFERENCE_LOCATIONS,...REFERENCE_INTERIORS]);for(const id of scope)if(source.LOCATIONS[id]&&!permitted.has(id))throw Error('Cette région du jeu n’est pas modifiable par cet éditeur : '+id);for(const d of project.doors){const old=source.DOORS.find(o=>o.id===d.id);if(old&&!scope.has(old.location))throw Error('Identifiant de porte réservé à une autre région.');}for(const l of Object.values(project.locations))for(const a of l.actors){const old=source.NPCS.find(n=>n.id===a.id);if(old&&!scope.has(old.location))throw Error('Identifiant de personnage réservé à une autre région.');}
 const actorAliases={};for(const l of Object.values(project.locations))for(const a of l.actors){const old=source.NPCS.find(n=>n.id===a.id||a.id===l.id+'_npc_'+n.id);if(old)actorAliases[a.id]=old.id;}
 for(const [id,l]of Object.entries(project.locations)){const {actors,...geometry}=l;LOCATIONS[id]={...source.LOCATIONS[id],...geometry};}
 const nativeDoors=new Map(source.DOORS.map(d=>[d.id,d]));
 const DOORS=[...source.DOORS.filter(d=>!scope.has(d.location)),...project.doors.map(d=>{const old=nativeDoors.get(d.id),door=old?{...old}: {conditions:[]};for(const k of ['id','location','buildingId','opening','threshold','target','label'])if(Object.hasOwn(d,k))door[k]=structuredClone(d[k]);return door;})];
 const represented=new Set(Object.values(actorAliases));const NPCS=source.NPCS.filter(n=>!scope.has(n.location)||!represented.has(n.id)).map(n=>scope.has(n.location)?{...n,location:'_editor_removed'}:n);
 for(const l of Object.values(project.locations))for(const a of l.actors.filter(a=>a.role!=='player')){const id=actorAliases[a.id]||a.id,old=originalNPC.get(id);NPCS.push({...old,...(old?{}:{portrait:false}),id,name:a.label||a.sprite,sprite:a.sprite,location:l.id,x:a.x,z:a.z,editorScale:a.editorScale||1,dialogue:old?.dialogue||'editor_silence',editorDialogueId:a.dialogueId||'',editorActorId:a.id});}
 // An unpaired interior exit remains visible, but cannot crash a transition.
 const SPOTS=(source.SPOTS||[]).flatMap(spot=>{if(!scope.has(spot.location))return [spot];const original=source.LOCATIONS[spot.location]?.props||[],index=original.findIndex(p=>Math.hypot(p.x-spot.x,p.z-spot.z)<.01);if(index<0)return [spot];const p=project.locations[spot.location].props.find(p=>p.id===(original[index].id||spot.location+'_prop_'+index));return p?[{...spot,x:p.x,z:p.z}]:[];});
 const oldLab=source.LOCATIONS.dusk_q3.buildings.find(b=>b.id==='s_lab'),lab=LOCATIONS.dusk_q3.buildings.find(b=>b.id==='s_lab'),ratio=lab&&oldLab?lab.w/oldLab.w:1;const editorScenePoints=lab&&oldLab?{porte:{x:lab.x+(28-oldLab.x)*ratio,z:lab.z+(5.8-oldLab.z)*ratio}}:{};
 return {...source,LOCATIONS,DOORS,NPCS,SPOTS,editorScenePoints,editorProject:project,editorActorAliases:actorAliases};
}
export async function loadPublishedMaps(fetcher=fetch){const r=await fetcher('./src/data/editor-maps.json',{cache:'no-store'});if(!r.ok)throw Error('Cartes publiées indisponibles ('+r.status+').');return r.json();}

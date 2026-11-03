import {validate,editedLocations} from '../../editor/model.js';
// Seule la géométrie éditée remplace les données natives : le code de chaque zone reste la valeur par défaut et
// editor-maps.json ne remplace que les zones modifiées (comparées à la source du jeu). Conditions exécutables,
// transitions scriptées, identifiants de dialogue et clés narratives (city, arrive, labelsProches…) restent natifs.
export function applyEditorProject(source,input,base,{force=[]}={}){
 if(!input)return {...source,editorProject:null};const project=validate(input,base),scope=new Set([...editedLocations(project,base),...force.filter(id=>project.locations[id])]),LOCATIONS={...source.LOCATIONS},originalNPC=new Map(source.NPCS.map(n=>[n.id,n]));
 const editable=new Set([...Object.keys(base.locations),...Object.keys(base.interiorTemplates||{})]);for(const id of scope)if(source.LOCATIONS[id]&&!editable.has(id))throw Error('Cette région du jeu n’est pas modifiable par cet éditeur : '+id);
 const doors=project.doors.filter(d=>scope.has(d.location)),locations=Object.fromEntries([...scope].filter(id=>project.locations[id]).map(id=>[id,project.locations[id]]));
 for(const d of doors){const old=source.DOORS.find(o=>o.id===d.id);if(old&&!scope.has(old.location))throw Error('Identifiant de porte réservé à une autre région : '+d.id);}for(const l of Object.values(locations))for(const a of l.actors){const old=source.NPCS.find(n=>n.id===a.id);if(old&&!scope.has(old.location))throw Error('Identifiant de personnage réservé à une autre région : '+a.id);}
 const actorAliases={};for(const l of Object.values(locations))for(const a of l.actors){const old=source.NPCS.find(n=>n.id===a.id||a.id===l.id+'_npc_'+n.id);if(old)actorAliases[a.id]=old.id;}
 for(const [id,l]of Object.entries(locations)){const {actors,...geometry}=l;LOCATIONS[id]={...source.LOCATIONS[id],...geometry};}
 const nativeDoors=new Map(source.DOORS.map(d=>[d.id,d]));
 const DOORS=[...source.DOORS.filter(d=>!scope.has(d.location)),...doors.map(d=>{const old=nativeDoors.get(d.id),door=old?{...old}: {conditions:[]};for(const k of ['id','location','buildingId','opening','threshold','target','label'])if(Object.hasOwn(d,k))door[k]=structuredClone(d[k]);return door;})];
 // PNJ sans sprite (déclencheurs de scène ou de combat) : jamais édités, ils restent à leur place.
 const represented=new Set(Object.values(actorAliases));const NPCS=source.NPCS.filter(n=>!scope.has(n.location)||!represented.has(n.id)).map(n=>scope.has(n.location)&&n.sprite?{...n,location:'_editor_removed'}:n);
 for(const l of Object.values(locations))for(const a of l.actors.filter(a=>a.role!=='player')){const id=actorAliases[a.id]||a.id,old=originalNPC.get(id);NPCS.push({...old,...(old?{}:{portrait:false}),id,name:a.label||a.sprite,sprite:a.sprite,location:l.id,x:a.x,z:a.z,editorScale:a.editorScale||1,dialogue:old?.dialogue||'editor_silence',editorDialogueId:a.dialogueId||'',editorActorId:a.id});}
 // An unpaired interior exit remains visible, but cannot crash a transition.
 const SPOTS=(source.SPOTS||[]).flatMap(spot=>{if(!scope.has(spot.location))return [spot];const original=source.LOCATIONS[spot.location]?.props||[],index=original.findIndex(p=>Math.hypot(p.x-spot.x,p.z-spot.z)<.01);if(index<0)return [spot];const p=locations[spot.location].props.find(p=>p.id===(original[index].id||spot.location+'_prop_'+index));return p?[{...spot,x:p.x,z:p.z}]:[];});
 const oldLab=source.LOCATIONS.dusk_q3.buildings.find(b=>b.id==='s_lab'),lab=LOCATIONS.dusk_q3.buildings.find(b=>b.id==='s_lab'),ratio=lab&&oldLab?lab.w/oldLab.w:1;const editorScenePoints=lab&&oldLab&&scope.has('dusk_q3')?{porte:{x:lab.x+(28-oldLab.x)*ratio,z:lab.z+(5.8-oldLab.z)*ratio}}:{};
 return {...source,LOCATIONS,DOORS,NPCS,SPOTS,editorScenePoints,editorProject:project,editorActorAliases:actorAliases,editorScope:[...scope]};
}
export async function loadPublishedMaps(fetcher=fetch){const r=await fetcher('./src/data/editor-maps.json',{cache:'no-store'});if(!r.ok)throw Error('Cartes publiées indisponibles ('+r.status+').');return r.json();}

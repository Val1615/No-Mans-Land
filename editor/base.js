// Catalogue de l'éditeur construit depuis la source du jeu : toutes les zones chargées par le jeu (extérieurs et intérieurs),
// régions déduites des données, ressources issues de tous les manifestes (src/core/catalogue.js).
const copy=o=>JSON.parse(JSON.stringify(o));
// Anciennes listes (Dusk-Town, PR #1) conservées pour compatibilité ; les régions sont désormais dérivées des données.
export const REFERENCE_LOCATIONS=['dusk_q1','dusk_q2','dusk_q3','dusk_q4'];
export const REFERENCE_INTERIORS=['clinic_in','bar_in','mara_in','grocery_in','guet_in','atelier_in','citerne_in'];
// Clés de lieu purement narratives ou d'interface : elles restent dans le code du jeu et ne passent pas par l'éditeur.
export const NATIVE_LOCATION_KEYS=['city','arrive','labelsProches','accessLabels'];
export const REGION_NAMES={dusk:'Dusk-Town',steel:'Steel',autre:'Autres zones'};
const exteriorRegion=l=>l.city==='steel'||/^(steel_|sv_)/.test(l.id)?'steel':/^dusk_/.test(l.id)?'dusk':'autre';
// Région de chaque zone : un extérieur par son identifiant / sa ville, un intérieur par l'extérieur auquel ses portes mènent.
export function deriveRegions(world){const regions={};for(const l of Object.values(world.LOCATIONS))if(l.kind!=='interior')regions[l.id]=exteriorRegion(l);
 const byId=new Map(world.DOORS.map(d=>[d.id,d]));for(let pass=0;pass<3;pass++)for(const l of Object.values(world.LOCATIONS)){if(regions[l.id])continue;for(const d of world.DOORS.filter(d=>d.location===l.id)){const t=byId.get(d.target?.doorId)?.location;if(t&&regions[t]){regions[l.id]=regions[t];break;}}}
 for(const l of Object.values(world.LOCATIONS))regions[l.id] ||= l.city==='steel'?'steel':'autre';return regions;}
const actorOf=(n,taken)=>({id:taken.has(n.id)?n.location+'_npc_'+n.id:n.id,sprite:n.sprite,label:n.name,x:n.x,z:n.z,role:'npc',editorScale:n.editorScale||1});
export function createEditorBase(world,{sprites,bman,iman,sols={}}){
 const regions=deriveRegions(world),editable=l=>l&&typeof l==="object"&&l.ground&&l.size;
 // Un PNJ peut porter le même identifiant que son stand (ag_mei…) : l'éditeur lui donne alors l'alias <zone>_npc_<id>, ramené à l'identifiant natif au chargement du jeu.
 const taken=new Set(Object.values(world.LOCATIONS).flatMap(l=>[...(l.buildings||[]),...(l.props||[])].map(b=>b.id).filter(Boolean)));
 const prepare=(id,interior)=>{const l=copy(world.LOCATIONS[id]);for(const k of NATIVE_LOCATION_KEYS)delete l[k];l.props ||= [];l.buildings ||= [];l.ground.zones ||= [];if(interior){l.spawn ||= {player:{x:l.size.w/2,z:l.size.d-1},companion:{x:l.size.w/2+1,z:l.size.d-1}};l.props.forEach((p,i)=>p.id ||= id+'_furn_'+i);}
  l.actors=world.NPCS.filter(n=>n.location===id&&typeof n.sprite==='string'&&n.sprite&&Number.isFinite(n.x)&&Number.isFinite(n.z)).map(n=>actorOf(n,taken));return l;};
 const all=Object.values(world.LOCATIONS).filter(editable);
 const locations=Object.fromEntries(all.filter(l=>l.kind!=='interior').map(l=>[l.id,prepare(l.id,false)]));
 const interiorTemplates=Object.fromEntries(all.filter(l=>l.kind==='interior').map(l=>[l.id,prepare(l.id,true)]));
 const every=[...Object.values(locations),...Object.values(interiorTemplates)];
 const keys=new Set(every.flatMap(l=>l.buildings.map(b=>b.sprite))),buildings=Object.fromEntries([...keys].filter(k=>bman[k]).map(k=>[k,bman[k]]));
 const characterAssets=[{sprite:'player',label:'Voyageur'},{sprite:'nilo',label:'Nilo'}];for(const n of world.NPCS.filter(n=>typeof n.sprite==='string'&&n.sprite))if(!characterAssets.some(a=>a.sprite===n.sprite))characterAssets.push({sprite:n.sprite,label:n.name});
 const furnitureNames={clinic_cabinet:'Armoire médicale',clinic_table:'Table médicale',clinic_cot_b:'Lit médical',clinic_stretcher_b:'Brancard',m_archive_shelf:'Étagère',m_desk:'Bureau',bar_backshelf_b:'Étagères de bar',bar_counter_b:'Comptoir de bar',bar_table_b:'Table de bistrot',home_mattress_d:'Matelas',home_curtain:'Rideau',home_table:'Table',home_water:'Réserve d’eau',shop_shelf:'Rayonnage',shop_counter:'Comptoir'};
 const furnitureKeys=new Set(every.flatMap(l=>l.props.filter(p=>p.furn).map(p=>p.furn)));
 const interiorFloors=[...new Set(['f_tiles','f_wood','f_earth','f_concrete',...Object.values(interiorTemplates).map(l=>l.ground.skin)])].filter(Boolean);
 const interiorWalls=[...new Set(['w_plaster','w_brick','w_clay','w_planks',...Object.values(interiorTemplates).map(l=>l.wallSkin)])].filter(Boolean);
 const groundSkins=[...new Set([...Object.keys(sols),...Object.values(locations).flatMap(l=>[l.ground.skin,...l.ground.zones.map(z=>z.skin),...(l.ground.paint||[]).map(p=>p.skin)])])].filter(s=>typeof s==='string'&&!interiorFloors.includes(s));
 const zoneKinds=[...new Set(['grass','asphalt','track','packed','plate',...every.flatMap(l=>l.ground.zones.map(z=>z.kind))])].filter(Boolean);
 // Sprites des décors, figurants, passants et personnages de toutes les zones ; les conditions et métadonnées scriptées des portes restent dans le jeu.
 const wanted=new Set(['player','nilo','st_drone',...characterAssets.map(a=>a.sprite),...every.flatMap(l=>[...l.props.map(p=>p.sprite),...(l.extras||[]).map(e=>e.sprite),...(l.walkers||[]).map(w=>w.sprite)]),...furnitureKeys,...interiorFloors,...interiorWalls]);const allSprites={...sprites,...iman};const editorSprites=Object.fromEntries([...wanted].filter(k=>k&&allSprites[k]).map(k=>[k,allSprites[k]]));
 const doors=world.DOORS.map(d=>({...copy(d),conditions:[]}));
 return {sourceCommit:'game-source',regions,regionNames:REGION_NAMES,locations,interiorTemplates,doors,bman:buildings,allBman:bman,sprites:editorSprites,allSprites,characterAssets,furnitureAssets:[...furnitureKeys].map(id=>({id,label:furnitureNames[id]||id})),interiorFloors,interiorWalls,groundSkins,groundSkinFiles:{...sols},zoneKinds};
}

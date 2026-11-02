// Build the editor catalog from the current game source, never from a copied town.
const copy=o=>JSON.parse(JSON.stringify(o));
export const REFERENCE_LOCATIONS=['dusk_q1','dusk_q2','dusk_q3','dusk_q4'];
export const REFERENCE_INTERIORS=['clinic_in','bar_in','mara_in','grocery_in','guet_in','atelier_in','citerne_in'];
export function createEditorBase(world,{sprites,bman,iman}){
 const locations=Object.fromEntries(REFERENCE_LOCATIONS.map(id=>[id,copy(world.LOCATIONS[id])]));
 const interiorTemplates=Object.fromEntries(REFERENCE_INTERIORS.map(id=>{const l=copy(world.LOCATIONS[id]);l.ground.zones ||= [];l.spawn ||= {player:{x:l.size.w/2,z:l.size.d-1},companion:{x:l.size.w/2+1,z:l.size.d-1}};l.actors=world.NPCS.filter(n=>n.location===id&&n.sprite).map(n=>({id:n.id,sprite:n.sprite,label:n.name,x:n.x,z:n.z,role:'npc',editorScale:n.editorScale||1}));l.props.forEach((p,i)=>p.id ||= id+'_furn_'+i);return[id,l];}));
 const keys=new Set(Object.values(locations).flatMap(l=>l.buildings.map(b=>b.sprite))),buildings=Object.fromEntries([...keys].map(k=>[k,bman[k]]));
 const characterAssets=[{sprite:'player',label:'Voyageur'},{sprite:'nilo',label:'Nilo'}];for(const n of world.NPCS.filter(n=>REFERENCE_INTERIORS.includes(n.location)&&n.sprite))if(!characterAssets.some(a=>a.sprite===n.sprite))characterAssets.push({sprite:n.sprite,label:n.name});
 const furnitureNames={clinic_cabinet:'Armoire médicale',clinic_table:'Table médicale',clinic_cot_b:'Lit médical',clinic_stretcher_b:'Brancard',m_archive_shelf:'Étagère',m_desk:'Bureau',bar_backshelf_b:'Étagères de bar',bar_counter_b:'Comptoir de bar',bar_table_b:'Table de bistrot',home_mattress_d:'Matelas',home_curtain:'Rideau',home_table:'Table',home_water:'Réserve d’eau',shop_shelf:'Rayonnage',shop_counter:'Comptoir'};
 const furnitureKeys=new Set(Object.values(interiorTemplates).flatMap(l=>l.props.filter(p=>p.furn).map(p=>p.furn)));
 // conditions and scripted door metadata remain in the game; only geometry is edited.
 const wanted=new Set(['player','nilo',...characterAssets.map(a=>a.sprite),...Object.values(locations).flatMap(l=>l.props.map(p=>p.sprite)),...furnitureKeys,'f_tiles','f_wood','f_earth','f_concrete','w_plaster','w_brick','w_clay','w_planks']);const allSprites={...sprites,...iman};const editorSprites=Object.fromEntries([...wanted].filter(k=>allSprites[k]).map(k=>[k,allSprites[k]]));
 const doors=world.DOORS.map(d=>({...copy(d),conditions:[]}));
 return {sourceCommit:'game-source',locations,interiorTemplates,doors,bman:buildings,sprites:editorSprites,characterAssets,furnitureAssets:[...furnitureKeys].map(id=>({id,label:furnitureNames[id]||id})),interiorFloors:['f_tiles','f_wood','f_earth','f_concrete'],interiorWalls:['w_plaster','w_brick','w_clay','w_planks']};
}

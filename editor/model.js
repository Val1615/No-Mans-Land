import {hydrateInteriors} from './interiors.js';
import {validateStory} from './story-model.js';
import {defaultLayers} from './layers.js';
// Format nml-map-editor, version 5 : toutes les zones du jeu (régions dérivées des données), sol peint, décors,
// PNJ, figurants, passants, lueurs et lumière, portes. Règle clé : une zone ouverte puis enregistrée sans
// modification ne change rien au jeu — compact() ne garde que les zones qui diffèrent de la source du jeu.
export const VERSION=5;
export const clone=o=>structuredClone(o);
export function upgrade(doc){doc.editorLayers={...defaultLayers(),...(doc.editorLayers||{})};doc.activeLayer ||= 'building';doc.version=VERSION;doc.dialogues ||= {};doc.quests ||= {};for(const l of Object.values(doc.locations)){l.actors ||= [];if(!l.actors.some(a=>a.role==='player'))l.actors.unshift({id:l.id+'_player_spawn',sprite:'player',label:'Départ du joueur',role:'player',x:l.spawn.player.x,z:l.spawn.player.z,editorScale:1});}return doc;}
export function initial(base){const locations={...clone(base.locations),...clone(base.interiorTemplates||{})};for(const l of Object.values(locations)){l.buildings.forEach(b=>{b.editorScale=1;b.editorLayer=0;b.editorDepth=0;});l.props.forEach((p,i)=>p.id ||= `${l.id}_prop_${i}`);l.ground.zones.forEach((p,i)=>p.id=`${l.id}_zone_${i}`);}return upgrade(hydrateInteriors({format:'nml-map-editor',version:1,sourceCommit:base.sourceCommit,locations,doors:clone(base.doors.filter(d=>locations[d.location]))},base));}
const refs=new WeakMap();
// Document de référence (source du jeu non modifiée), mis en cache ; ne jamais le modifier.
export function reference(base){if(!refs.has(base))refs.set(base,initial(base));return refs.get(base);}
export function canonical(v){return JSON.stringify(v,(k,x)=>x&&typeof x==='object'&&!Array.isArray(x)?Object.fromEntries(Object.keys(x).sort().map(k=>[k,x[k]])):x);}
// Zones réellement modifiées : lieu différent de la source, ou porte nouvelle / modifiée qui lui appartient.
export function editedLocations(doc,base){const ref=reference(base),out=new Set();for(const [id,l]of Object.entries(doc.locations))if(!ref.locations[id]||canonical(l)!==canonical(ref.locations[id]))out.add(id);const refDoors=new Map(ref.doors.map(d=>[d.id,d]));for(const d of doc.doors)if(!refDoors.has(d.id)||canonical(d)!==canonical(refDoors.get(d.id)))out.add(d.location);for(const d of ref.doors)if(doc.locations[d.location]&&!doc.doors.some(x=>x.id===d.id))out.add(d.location);return out;}
// Fichier publié : seulement les zones modifiées (et leurs portes) ; le reste reste le code du jeu.
export function compact(doc,base){const kept=editedLocations(doc,base),out={...clone(doc),version:VERSION,locations:{},doors:[]};for(const id of kept)if(doc.locations[id])out.locations[id]=clone(doc.locations[id]);out.doors=clone(doc.doors.filter(d=>kept.has(d.location)));return out;}
// Complète un fichier compact avec les zones non modifiées de la source du jeu.
function complete(doc,base){const ref=reference(base),added=new Set();for(const [id,l]of Object.entries(ref.locations))if(!doc.locations[id]){doc.locations[id]=clone(l);added.add(id);}const known=new Set(doc.doors.map(d=>d.id));for(const d of ref.doors)if(added.has(d.location)&&!known.has(d.id))doc.doors.push(clone(d));for(const l of Object.values(doc.locations))if(l.kind==='exterior')for(const b of l.buildings){const room=ref.locations[l.id]?.buildings.find(x=>x.id===b.id)?.interiorId;if(room&&!b.interiorId&&doc.locations[room])b.interiorId=room;}return doc;}
export function transform(doc,locId,id,changes){const l=doc.locations[locId],b=l.buildings.find(b=>b.id===id);const p=b||l.props.find(b=>b.id===id)||l.ground.zones.find(b=>b.id===id)||l.actors?.find(b=>b.id===id);if(!p)return;const old=clone(p);Object.assign(p,changes);if(b){const ratio=(p.editorScale||1)/(old.editorScale||1);if(ratio!==1){p.w=old.w*ratio;p.d=old.d*ratio;p.k=(old.k||1)*ratio;}if(old.solid&&!Object.hasOwn(changes,'solid'))p.solid=old.solid.map(s=>({...s,x:p.x+(s.x-old.x)*ratio,z:p.z+(s.z-old.z)*ratio,w:s.w*ratio,d:s.d*ratio}));for(const d of doc.doors.filter(d=>d.buildingId===id&&d.location===locId)){for(const k of ['opening','threshold']){d[k].x=p.x+(d[k].x-old.x)*ratio;d[k].z=p.z+(d[k].z-old.z)*ratio;}}}if(p.role==='player')l.spawn.player={x:p.x,z:p.z};return p;}
const LOCATION_KEYS=['id','name','size','kind','ground','buildings','props','spawn','actors','wall','wallSkin','light','glows','extras','walkers','drones','gardeCorps','doorSkin','enseignes','projecteurs'];
export const EFFETS_ENSEIGNE=['fixe','clignote','gresille','saute','pulse']; // enseignes animées par le code (docs/villes/steel/ENSEIGNES_CODE.md)
const GROUND_KEYS=['base','skin','zones','tileM','paint','tint','clean','water'];
const KEYS={building:['id','label','sprite','x','z','w','d','visitable','cue','k','sy','y','solid','editorScale','editorLayer','editorDepth','interiorId','named','tint','sign','cover','defile','groupe','ph','fige','ecran'],
 prop:['id','label','sprite','furn','box','w','d','h','color','x','z','y','solid','fp','glow','flip','tint','editorScale','editorLayer','editorDepth'],
 actor:['id','label','sprite','role','x','z','editorScale','dialogueId'],zone:['id','label','kind','x','z','w','d','skin','tint','tileM','editorScale','editorLayer','editorDepth']};
const LABEL={building:'bâtiment',prop:'décor',actor:'personnage',zone:'zone de sol'};
// Valeur JSON simple (nombres finis, textes courts, tableaux, objets), utilisée pour les réglages avancés repris du jeu.
function plain(v,depth=0){if(depth>6)return false;if(v===null||typeof v==='boolean')return true;if(typeof v==='number')return Number.isFinite(v);if(typeof v==='string')return v.length<=400;if(Array.isArray(v))return v.length<=4000&&v.every(x=>plain(x,depth+1));if(typeof v==='object')return Object.keys(v).length<=60&&Object.values(v).every(x=>plain(x,depth+1));return false;}
export class MapValidationError extends Error{constructor(issues){super(issues.length===1?'Carte invalide : '+issues[0]:`Carte invalide (${issues.length} erreurs) :\n- `+issues.slice(0,12).join('\n- ')+(issues.length>12?`\n- … et ${issues.length-12} autres.`:''));this.issues=issues;}}
export function validate(input,base){
 if(!input||typeof input!=='object'||input.format!=='nml-map-editor'||![1,2,3,4,5].includes(input.version))throw new MapValidationError(['format ou version incompatible (attendu : nml-map-editor, version 1 à 5).']);
 if(!input.locations||typeof input.locations!=='object'||Array.isArray(input.locations)||!Array.isArray(input.doors||[]))throw new MapValidationError(['liste des zones ou des entrées absente.']);
 const legacy=input.version<5,doc=upgrade(complete(input.version<3?hydrateInteriors({...clone(input),doors:clone(input.doors||[])},base):{...clone(input),doors:clone(input.doors||[])},base)),ref=reference(base),errors=[],ids=new Set();
 // Anciens fichiers (v4) : les PNJ des extérieurs n'étaient pas représentés ; on reprend ceux de la source pour ne pas les perdre.
 if(legacy)for(const [id,l]of Object.entries(doc.locations)){const r=ref.locations[id];if(r&&!l.actors.some(a=>a.role==='npc'))l.actors.push(...clone(r.actors.filter(a=>a.role==='npc')));}
 const err=(where,msg)=>errors.push((where?where+' : ':'')+msg);
 const finite=(v,min,max)=>typeof v==='number'&&Number.isFinite(v)&&v>=min&&v<=max;const coord=p=>p&&finite(p.x,-100,300)&&finite(p.z,-100,300);
 const allSprites=base.allSprites||base.sprites,allBman=base.allBman||base.bman,groundSkins=[...(base.groundSkins||[]),...(base.interiorFloors||[])];
 const refItem=new Map();for(const l of Object.values(ref.locations))for(const arr of [l.buildings,l.props,l.ground.zones,l.actors])for(const p of arr)refItem.set(l.id+'/'+p.id,p);
 const allowed=new Set(Object.keys(doc.locations));if(allowed.size>200)err('','trop de zones (200 maximum).');
 for(const [key,l]of Object.entries(doc.locations)){const at=`zone « ${key} »`;
  if(!l||typeof l!=='object'){err(at,'zone illisible.');continue;}
  for(const k of Object.keys(l))if(!LOCATION_KEYS.includes(k)&&canonical(l[k])!==canonical(ref.locations[key]?.[k]))err(at,`paramètre « ${k} » non pris en charge.`);
  if(l.id!==key||!/^[a-zA-Z0-9_-]{1,100}$/.test(key))err(at,'identifiant invalide.');
  if(!['exterior','interior'].includes(l.kind))err(at,'type de zone inconnu (exterior ou interior).');
  if(typeof l.name!=='string'||!l.name||l.name.length>100)err(at,'nom manquant ou trop long.');
  const lim=l.kind==='interior'?[4,48]:[8,160];if(!finite(l.size?.w,...lim)||!finite(l.size?.d,...lim)){err(at,`taille hors limites (${lim[0]} à ${lim[1]} m).`);continue;}
  if(!l.ground||!Array.isArray(l.ground.zones)){err(at,'sol absent.');continue;}
  for(const k of Object.keys(l.ground))if(!GROUND_KEYS.includes(k))err(at,`paramètre de sol « ${k} » non pris en charge.`);
  if(typeof l.ground.base!=='string'||l.ground.base.length>30)err(at,'couleur de sol invalide.');
  if(!groundSkins.includes(l.ground.skin))err(at,`texture de sol inconnue « ${l.ground.skin} ».`);
  if(l.ground.tileM!=null&&!finite(l.ground.tileM,.5,40))err(at,'taille de motif de sol invalide.');
  for(const k of ['tint','clean','water'])if(l.ground[k]!=null&&!plain(l.ground[k]))err(at,`réglage de sol « ${k} » invalide.`);
  if(Array.isArray(l.ground.water))for(const w of l.ground.water)if(!coord(w)||(w.image&&!groundSkins.includes(w.image)))err(at,'plan d’eau invalide (position ou texture).');
  if(l.ground.paint!=null){if(!Array.isArray(l.ground.paint)||l.ground.paint.length>36864)err(at,'peinture de terrain invalide.');else{const bad=l.ground.paint.filter(r=>!r||Object.keys(r).some(k=>!['x','z','w','d','skin'].includes(k))||!finite(r.x,0,l.size.w)||!finite(r.z,0,l.size.d)||!finite(r.w,.5,l.size.w)||!finite(r.d,.5,l.size.d)||r.x+r.w>l.size.w+.001||r.z+r.d>l.size.d+.001||[r.x,r.z,r.w,r.d].some(v=>Math.abs(v*2-Math.round(v*2))>.001)||!groundSkins.includes(r.skin));if(bad.length)err(at,`${bad.length} case(s) de peinture hors de la zone ou de texture inconnue.`);}}
  if(!l.spawn||!coord(l.spawn.player)||!coord(l.spawn.companion))err(at,'départ du joueur ou du compagnon invalide.');
  if(l.kind==='interior'&&(!base.interiorWalls.includes(l.wallSkin)||!/^#[0-9a-f]{6}$/i.test(l.wall||'')))err(at,'revêtement de mur invalide.');
  if(l.light!=null&&(!plain(l.light)||typeof l.light!=='object'))err(at,'éclairage invalide.');
  if(l.doorSkin!=null&&typeof l.doorSkin!=='string')err(at,'habillage de porte invalide.');
  for(const [k,check]of [['glows',g=>coord(g)&&finite(g.rx??1,0,60)&&finite(g.rz??1,0,60)&&finite(g.i??1,0,5)],['extras',e=>coord(e)&&!!allSprites[e.sprite]],['walkers',w=>!!allSprites[w.sprite]&&Array.isArray(w.path)&&w.path.length>=2&&w.path.every(p=>Array.isArray(p)&&finite(p[0],-100,300)&&finite(p[1],-100,300))],['drones',coord],['gardeCorps',g=>coord(g)&&finite(g.w,0,160)&&finite(g.d,0,160)],
   ['enseignes',e=>typeof e.id==='string'&&/^[A-Za-z0-9_-]{1,60}$/.test(e.id)&&Array.isArray(l.buildings)&&l.buildings.some(b=>b?.id===e.building)&&(e.neon==null||!!allBman[e.neon])&&(e.effet==null||EFFETS_ENSEIGNE.includes(e.effet))&&finite(e.periode??3,.2,60)&&finite(e.decale??0,-100,100)&&finite(e.intensite??.6,0,2)&&(e.couleur==null||/^#[0-9a-f]{6}$/i.test(e.couleur))&&(e.saute==null||(Array.isArray(e.saute)&&e.saute.length===2&&finite(e.saute[0],0,1)&&finite(e.saute[1],0,1)&&e.saute[0]<e.saute[1]))&&(e.dev==null||typeof e.dev==='boolean')],
   ['projecteurs',p=>(p.building!=null?Array.isArray(l.buildings)&&l.buildings.some(b=>b?.id===p.building):p.fx!=null?finite(p.fx,0,1)&&finite(p.fz,0,1):finite(p.x,-20,l.size.w+20)&&finite(p.z,-20,l.size.d+20))&&finite(p.y??.5,-1,40)&&(p.couleur==null||/^#[0-9a-f]{6}$/i.test(p.couleur))&&finite(p.longueur??28,1,120)&&finite(p.ouverture??5,.5,30)&&finite(p.inclinaison??20,0,80)&&finite(p.cap??0,-360,360)&&finite(p.balayage??25,0,90)&&finite(p.periode??14,1,120)&&finite(p.decale??0,-120,120)&&finite(p.intensite??.35,0,1.5)]]){
   if(l[k]==null)continue;if(!Array.isArray(l[k])||l[k].length>200||!l[k].every(x=>x&&typeof x==='object'&&plain(x))){err(at,`liste « ${k} » invalide.`);continue;}const bad=l[k].filter(x=>!check(x));if(bad.length)err(at,`${bad.length} élément(s) « ${k} » invalides (position hors limites ou sprite inconnu${bad[0]?.sprite?' : '+bad[0].sprite:bad[0]?.id?' : '+bad[0].id:''}).`);}
  for(const [kind,arr]of [['building',l.buildings],['prop',l.props],['zone',l.ground.zones],['actor',l.actors]]){
   if(!Array.isArray(arr)||arr.length>600){err(at,`liste de ${LABEL[kind]}s invalide ou trop grande.`);continue;}
   for(const p of arr){const name=`${at} · ${LABEL[kind]} « ${p?.id??'?'} »`;
    if(!p||typeof p.id!=='string'||!p.id||p.id.length>100){err(at,`${LABEL[kind]} sans identifiant.`);continue;}
    if(ids.has(p.id))err(name,'identifiant en double.');ids.add(p.id);
    if(!coord(p))err(name,'coordonnées hors limites (−100 à 300 m).');
    const native=refItem.get(key+'/'+p.id);for(const k of Object.keys(p))if(!KEYS[kind].includes(k)&&canonical(p[k])!==canonical(native?.[k]))err(name,`propriété « ${k} » non prise en charge.`);
    if(p.label!=null&&(typeof p.label!=='string'||p.label.length>100))err(name,'nom invalide.');
    if(p.y!=null&&!finite(p.y,-10,40))err(name,'hauteur invalide.');if(p.sy!=null&&!finite(p.sy,.1,3))err(name,'proportion invalide.');
    if(!finite(p.editorScale??1,.5,1.5))err(name,'échelle hors limites (0,5 à 1,5).');
    if(kind==='building'){if(!allBman[p.sprite])err(name,`asset de bâtiment inconnu « ${p.sprite} ».`);if(!finite(p.w,.1,160)||!finite(p.d,.1,160)||!finite(p.k??1,.1,5)||!finite(p.editorLayer??0,-1,1)||!finite(p.editorDepth??0,-100,100))err(name,'dimensions ou calque invalides.');if(p.solid&&(!Array.isArray(p.solid)||p.solid.length>16||p.solid.some(s=>!coord(s)||!finite(s.w,0,160)||!finite(s.d,0,160))))err(name,'collision invalide.');for(const k of ['cue','sign','cover','defile','groupe','ph','fige','ecran','tint','named'])if(p[k]!=null&&!plain(p[k]))err(name,`réglage « ${k} » invalide.`);}
    else if(kind==='prop'){if(p.box?!(p.box===true&&finite(p.w,.1,40)&&finite(p.d,.1,40)&&finite(p.h,.01,6)&&/^#[0-9a-f]{6}$/i.test(p.color||'')):p.furn?!base.furnitureAssets?.some(a=>a.id===p.furn):!allSprites[p.sprite])err(name,`asset de décor inconnu « ${p.furn||p.sprite||'?'} ».`);if(p.fp&&(!Array.isArray(p.fp)||p.fp.length!==2||p.fp.some(n=>!finite(n,0,48))))err(name,'emprise invalide.');if(p.solid!=null&&!finite(p.solid,0,48))err(name,'collision invalide.');if(p.glow!=null&&!finite(p.glow,0,5))err(name,'lueur invalide.');if(p.flip!=null&&typeof p.flip!=='boolean')err(name,'retournement invalide.');}
    else if(kind==='actor'){if(!base.characterAssets?.some(c=>c.sprite===p.sprite))err(name,`sprite de personnage inconnu « ${p.sprite} ».`);if(!['player','npc'].includes(p.role))err(name,'rôle inconnu.');if(p.dialogueId!=null&&(typeof p.dialogueId!=='string'||p.dialogueId.length>100))err(name,'dialogue invalide.');}
    else{if(!(base.zoneKinds||['grass','asphalt','track','packed','plate']).includes(p.kind))err(name,`type de zone inconnu « ${p.kind} ».`);if(!finite(p.w,.1,160)||!finite(p.d,.1,160))err(name,'dimensions invalides.');if(p.skin!=null&&!groundSkins.includes(p.skin))err(name,`texture inconnue « ${p.skin} ».`);if(p.tileM!=null&&!finite(p.tileM,.5,40))err(name,'taille de motif invalide.');}
    delete p.editorGhost;}}
  const players=(l.actors||[]).filter(a=>a.role==='player');if(players.length!==1||players[0].sprite!=='player'||players[0].x!==l.spawn?.player?.x||players[0].z!==l.spawn?.player?.z)err(at,'départ du joueur incohérent.');}
 for(const [kind,layer]of Object.entries(doc.editorLayers))if(!['zone','building','prop','actor'].includes(kind)||typeof layer?.visible!=='boolean'||typeof layer?.locked!=='boolean')err('','calque invalide.');if(!['zone','building','prop','actor'].includes(doc.activeLayer))err('','calque actif invalide.');
 if(doc.doors.length>800)err('','trop d’entrées.');const doorIds=new Set();
 for(const d of doc.doors){const at=`entrée « ${d?.id??'?'} »`;if(!d||typeof d.id!=='string'||doorIds.has(d.id)){err(at,'identifiant manquant ou en double.');continue;}doorIds.add(d.id);if(!allowed.has(d.location)){err(at,`zone inconnue « ${d.location} ».`);continue;}if(!coord(d.opening)||!coord(d.threshold))err(at,'position hors limites.');if(d.buildingId&&!doc.locations[d.location].buildings?.some(b=>b.id===d.buildingId))err(at,`bâtiment inconnu « ${d.buildingId} ».`);if(d.target?.doorId&&!base.doors.some(x=>x.id===d.target.doorId)&&!doc.doors.some(x=>x.id===d.target.doorId))err(at,`destination inconnue « ${d.target.doorId} ».`);}
 for(const l of Object.values(doc.locations))for(const b of l.buildings||[]){if(b.interiorId&&doc.locations[b.interiorId]?.kind!=='interior')err(`zone « ${l.id} » · bâtiment « ${b.id} »`,'intérieur manquant.');if(b.visitable&&!doc.doors.some(d=>d.location===l.id&&d.buildingId===b.id)&&!ref.doors.some(d=>d.location===l.id&&d.buildingId===b.id)&&!ref.locations[l.id]?.buildings.some(x=>x.id===b.id&&x.visitable))err(`zone « ${l.id} » · bâtiment « ${b.id} »`,'bâtiment visitable sans entrée.');}
 if(errors.length)throw new MapValidationError(errors);
 try{return validateStory(doc);}catch(e){throw new MapValidationError([e.message]);}
}

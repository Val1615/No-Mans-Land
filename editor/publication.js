// Préparation d'un envoi : fichier compact (zones modifiées seulement), relu et validé avant tout envoi (commit ou PR).
import {validate,compact,MapValidationError} from './model.js';
import {storyIssues} from './story-model.js';
import {MAX_BYTES} from './github-store.js';
const asIssues=e=>e instanceof MapValidationError||Array.isArray(e?.issues)?e:new MapValidationError([String(e?.message||e)]);
export function prepareExport(doc,base){
 let full,project,json;try{full=validate(doc,base);project=compact(full,base);json=JSON.stringify(project,null,2)+'\n';}catch(e){throw asIssues(e);}
 let reread;try{reread=JSON.parse(json);}catch{throw new MapValidationError(['export illisible : le JSON produit ne se relit pas.']);}
 try{validate(reread,base);}catch(e){throw asIssues(e);}
 const story=storyIssues(full);if(story.length)throw new MapValidationError(story.map(i=>'histoire : '+i));
 if(new TextEncoder().encode(json).length>MAX_BYTES)throw new MapValidationError(['fichier trop volumineux (900 ko maximum).']);
 return {project:reread,json,zones:Object.keys(reread.locations)};
}
// Conflit : on repart de la version GitHub fraîche et on n'y remplace que nos zones (les autres zones publiées entre-temps sont gardées).
export function mergeRemote(prepared,remote,base){if(!remote)return {project:prepared.project,both:[]};let theirs;try{theirs=compact(validate(remote,base),base);}catch{return {project:prepared.project,both:[],remoteInvalid:true};}
 const mine=new Set(prepared.zones),both=Object.keys(theirs.locations).filter(z=>mine.has(z));const project={...prepared.project,locations:{...theirs.locations,...prepared.project.locations},doors:[...theirs.doors.filter(d=>!mine.has(d.location)),...prepared.project.doors]};
 validate(JSON.parse(JSON.stringify(project)),base);return {project,both};}

// Publication GitHub de l'éditeur, API GitHub simulée (aucun push réel, aucun jeton réel) :
// commit direct sur main par défaut, PR en option, jeton dans le localStorage seulement, erreurs traduites,
// conflit -> version fraîche et nouvel essai sans écrasement, export cassé bloqué avant tout envoi.
import fs from 'node:fs';import path from 'node:path';import vm from 'node:vm';import assert from 'node:assert/strict';
const root=path.resolve(import.meta.dirname,'..'),context=vm.createContext({console,structuredClone,TextEncoder,TextDecoder,URLSearchParams,atob,btoa,Math,performance,Date}),cache=new Map();
async function load(relative){const file=path.resolve(root,relative);if(cache.has(file))return cache.get(file);const mod=new vm.SourceTextModule(fs.readFileSync(file,'utf8'),{context,identifier:file});cache.set(file,mod);await mod.link(spec=>load(path.relative(root,path.resolve(path.dirname(file),spec.split('?')[0]))));await mod.evaluate();return mod;}
const ns=async p=>(await load(p)).namespace,source=await ns('src/data/dusk_town.js'),{createEditorBase}=await ns('editor/base.js'),{initial,transform}=await ns('editor/model.js'),{chargerCatalogue}=await ns('src/core/catalogue.js'),{createGitHubStore,defaultMessage,TOKEN_KEY}=await ns('editor/github-store.js'),{prepareExport,mergeRemote}=await ns('editor/publication.js');
const base=createEditorBase(source,await chargerCatalogue(async p=>JSON.parse(fs.readFileSync(path.join(root,p))))),TOKEN='github_pat_TEST_mock';
const API='https://api.github.com/repos/Val1615/No-Mans-Land',FILE=API+'/contents/src/data/editor-maps.json';
const b64=o=>Buffer.from(JSON.stringify(o)).toString('base64'),unb64=s=>JSON.parse(Buffer.from(s,'base64').toString('utf8'));
// Faux GitHub : un fichier par branche, SHA vérifié à chaque écriture (409 si périmé).
function fakeGitHub({status}={}){const gh={files:{main:{sha:'v1',content:null}},branches:{main:'c0'},calls:[],pulls:[],n:1};
 gh.fetch=async(url,opts={})=>{gh.calls.push({url,method:opts.method||'GET',opts});assert.equal(opts.redirect,'error');const res=(code,body)=>({ok:code<300,status:code,headers:{get:()=>null},json:async()=>body});if(status)return res(status,{});
  const auth=opts.headers?.Authorization;if(opts.method&&opts.method!=='GET')assert.equal(auth,'Bearer '+TOKEN,'jeton dans l’en-tête Authorization uniquement');if(opts.body)assert(!opts.body.includes(TOKEN),'jeton absent du contenu envoyé');
  if(url.startsWith(FILE)&&(!opts.method||opts.method==='GET')){const ref=new URL(url).searchParams.get('ref')||'main',f=gh.files[ref];return f?res(200,{type:'file',sha:f.sha,encoding:'base64',content:b64(f.content)}):res(404,{});}
  if(url===FILE&&opts.method==='PUT'){const body=JSON.parse(opts.body),f=gh.files[body.branch];if(!f)return res(404,{});if(body.sha!==f.sha)return res(409,{message:'sha mismatch'});const sha='v'+(++gh.n);gh.files[body.branch]={sha,content:unb64(body.content),message:body.message};return res(200,{commit:{sha:'commit'+gh.n,html_url:'https://github.com/Val1615/No-Mans-Land/commit/commit'+gh.n},content:{sha}});}
  if(url===API+'/git/ref/heads/main')return res(200,{object:{sha:gh.branches.main}});
  if(url===API+'/git/refs'&&opts.method==='POST'){const body=JSON.parse(opts.body),name=body.ref.replace('refs/heads/','');gh.branches[name]=body.sha;gh.files[name]={...gh.files.main};return res(201,{ref:body.ref});}
  if(url===API+'/pulls'&&opts.method==='POST'){const body=JSON.parse(opts.body);gh.pulls.push(body);return res(201,{number:7,html_url:'https://github.com/Val1615/No-Mans-Land/pull/7'});}
  return res(500,{});};return gh;}
const storage=()=>{const m=new Map();return {getItem:k=>m.has(k)?m.get(k):null,setItem:(k,v)=>m.set(k,String(v)),removeItem:k=>m.delete(k),m};};
const edited=(zone,dx=0.5)=>{const doc=initial(base),b=doc.locations[zone].buildings[0];transform(doc,zone,b.id,{x:b.x+dx});return doc;};
// 1. Commit direct sur main (par défaut), message automatique, jeton mémorisé localement seulement.
let gh=fakeGitHub(),st=storage(),store=createGitHubStore(gh.fetch,st);const prep=prepareExport(edited('steel_pulse'),base);
assert.equal(JSON.stringify(prep.zones),'["steel_pulse"]');assert.equal(defaultMessage(prep.zones),'Éditeur : steel_pulse modifiée');
store.token.set(TOKEN);assert.equal(st.getItem(TOKEN_KEY),TOKEN);let res=await store.publish(prep.project,{message:defaultMessage(prep.zones),zones:prep.zones});
assert.equal(res.kind,'commit');assert.match(res.url,/commit\/commit2$/);assert.equal(gh.files.main.message,'Éditeur : steel_pulse modifiée');assert.equal(JSON.stringify(Object.keys(gh.files.main.content.locations)),'["steel_pulse"]');assert.equal(gh.calls.filter(c=>c.method==='PUT').length,1);
assert(!JSON.stringify(gh.files.main.content).includes(TOKEN));
// 2. Option « Proposer en PR plutôt » : branche editeur/<zone>-<date>, PR vers main, main inchangé.
gh=fakeGitHub();store=createGitHubStore(gh.fetch,st);res=await store.publish(prep.project,{message:'Éditeur : steel_pulse modifiée',pr:true,zones:prep.zones,date:new Date(2026,10,2,14,5,9)});
assert.equal(res.kind,'pr');assert.equal(res.branch,'editeur/steel_pulse-20261102-140509');assert.equal(res.url,'https://github.com/Val1615/No-Mans-Land/pull/7');assert.equal(gh.pulls[0].head,res.branch);assert.equal(gh.pulls[0].base,'main');assert.equal(gh.files.main.content,null,'main non modifié en mode PR');assert(gh.files[res.branch].content.locations.steel_pulse);
// 3. Conflit : quelqu'un publie dusk_q1 entre la lecture et l'envoi -> refus, version fraîche relue, nouvel essai qui garde dusk_q1.
gh=fakeGitHub();store=createGitHubStore(gh.fetch,st);await store.read();const other=prepareExport(edited('dusk_q1',1),base).project;gh.files.main={sha:'v9',content:other};
const err=await store.publish(prep.project,{zones:prep.zones,message:'m'}).then(()=>null,e=>e);assert(err&&err.code==='conflit'&&/Conflit/.test(err.message)&&/Rien n’a été écrasé/.test(err.message),'conflit signalé');assert.equal(gh.files.main.sha,'v9','rien écrasé');assert.equal(err.fresh.sha,'v9');
const merged=mergeRemote(prep,err.fresh.project,base);res=await store.publish(merged.project,{zones:prep.zones,message:'m'});assert.equal(res.kind,'commit');assert.equal(JSON.stringify(Object.keys(gh.files.main.content.locations).sort()),'["dusk_q1","steel_pulse"]');
// 4. Erreurs traduites simplement.
for(const [code,re] of [[401,/Jeton invalide/],[403,/Droits insuffisants/],[404,/Droits insuffisants/]]){const g=fakeGitHub();const s=createGitHubStore(async(u,o)=>u.startsWith(FILE)&&!o.method?g.fetch(u,o):({ok:false,status:code,headers:{get:()=>null},json:async()=>({})}),st);await assert.rejects(()=>s.publish(prep.project,{zones:prep.zones}),re);}
const pr403=createGitHubStore(async(u,o)=>u.startsWith(FILE)&&!o.method?fakeGitHub().fetch(u,o):({ok:false,status:403,headers:{get:()=>null},json:async()=>({})}),st);await assert.rejects(()=>pr403.publish(prep.project,{zones:prep.zones,pr:true}),/Pull requests : Read and write/);
await assert.rejects(()=>createGitHubStore(async()=>{throw new TypeError('offline');},st).publish(prep.project,{zones:prep.zones}),/Connexion à GitHub impossible/);
store.token.forget();assert.equal(st.getItem(TOKEN_KEY),null,'bouton Oublier');await assert.rejects(()=>createGitHubStore(fakeGitHub().fetch,st).publish(prep.project,{}),/jeton/);
// 5. Export cassé : refusé avant tout envoi, avec la liste des erreurs en français.
const broken=edited('steel_pulse');broken.locations.steel_pulse.buildings[0].sprite='asset_inexistant';broken.locations.steel_pulse.buildings[1].x=999;broken.doors.push({id:'porte_fantome',location:'zone_inconnue',opening:{x:1,z:1},threshold:{x:1,z:1}});
gh=fakeGitHub();let blocked=null;try{const p=prepareExport(broken,base);await createGitHubStore(gh.fetch,st).publish(p.project,{token:TOKEN});}catch(e){blocked=e;}
assert(blocked&&blocked.issues?.length>=3,'export cassé bloqué');assert(blocked.issues.some(i=>/asset de bâtiment inconnu « asset_inexistant »/.test(i)));assert(blocked.issues.some(i=>/coordonnées hors limites/.test(i)));assert(blocked.issues.some(i=>/zone inconnue « zone_inconnue »/.test(i)));assert.equal(gh.calls.length,0,'aucune requête GitHub pour un export cassé');
assert.throws(()=>prepareExport({format:'autre'},base),/format ou version incompatible/);
console.log('PASS editor-github : commit direct sur main (message automatique), PR editeur/<zone>-<date> vers main, jeton en localStorage seulement (oubli), erreurs traduites (jeton invalide, droits insuffisants, réseau), conflit -> rien écrasé, version fraîche, nouvel essai fusionné ; export cassé bloqué avant envoi avec '+blocked.issues.length+' erreurs listées. API GitHub simulée, aucun push réel.');

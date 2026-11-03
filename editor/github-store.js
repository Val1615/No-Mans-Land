// Publication GitHub de l'éditeur : un seul fichier (src/data/editor-maps.json) du dépôt Val1615/No-Mans-Land.
// Par défaut, commit direct sur main ; en option, branche editeur/<zone>-<date> et PR vers main.
// Le jeton n'est jamais écrit dans le dépôt ni dans les cartes : il reste dans le localStorage de ce navigateur (bouton « Oublier »).
export const REPOSITORY='Val1615/No-Mans-Land',MAP_PATH='src/data/editor-maps.json',MAIN='main',TOKEN_KEY='nml-editeur-jeton-github',MAX_BYTES=900000;
export const TOKEN_URL='https://github.com/settings/personal-access-tokens/new';
const API=`https://api.github.com/repos/${REPOSITORY}`,CONTENTS=`${API}/contents/${MAP_PATH}`;
const headers=token=>({'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28',...(token?{Authorization:'Bearer '+token}:{})});
const decode=s=>new TextDecoder().decode(Uint8Array.from(atob(s.replace(/\s/g,'')),c=>c.charCodeAt(0)));
const encode=s=>{const bytes=new TextEncoder().encode(s);let out='';for(let i=0;i<bytes.length;i+=8192)out+=String.fromCharCode(...bytes.subarray(i,i+8192));return btoa(out);};
export class GitHubError extends Error{constructor(code,message,extra={}){super(message);this.code=code;Object.assign(this,extra);}}
// Erreurs HTTP traduites simplement (jeton invalide, droits insuffisants, conflit…).
async function fail(r,what,pr){const remaining=r.headers?.get?.('x-ratelimit-remaining');
 if(r.status===401)throw new GitHubError('jeton','Jeton invalide ou expiré. Crée un nouveau jeton puis colle-le ici.');
 if(r.status===403&&remaining==='0')throw new GitHubError('limite','Limite de requêtes GitHub atteinte. Réessaie dans quelques minutes.');
 if(r.status===403||(r.status===404&&what!=='lecture'))throw new GitHubError('droits',`Droits insuffisants : le jeton doit viser le dépôt ${REPOSITORY} avec « Contents : Read and write »${pr?' et « Pull requests : Read and write »':''}.`);
 if(r.status===409||(r.status===422&&what==='fichier'))throw new GitHubError('conflit','Conflit : le fichier a changé sur GitHub depuis ta lecture. Rien n’a été écrasé.');
 throw new GitHubError('http',`GitHub a refusé la requête (${what}, code ${r.status}).`);}
async function call(fetcher,url,opts,what,pr){let r;try{r=await fetcher(url,{redirect:'error',cache:'no-store',...opts});}catch{throw new GitHubError('reseau','Connexion à GitHub impossible. Vérifie le réseau puis réessaie.');}if(!r.ok)await fail(r,what,pr);return r.json();}
export function branchFor(zones,date=new Date()){const slug=(zones.length?zones.slice(0,2).join('-'):'cartes').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9_-]+/g,'-').replace(/^-+|-+$/g,'').slice(0,60)||'cartes',p=n=>String(n).padStart(2,'0');return `editeur/${slug}-${date.getFullYear()}${p(date.getMonth()+1)}${p(date.getDate())}-${p(date.getHours())}${p(date.getMinutes())}${p(date.getSeconds())}`;}
export function defaultMessage(zones){return zones.length?`Éditeur : ${zones.join(', ')} ${zones.length>1?'modifiées':'modifiée'}`:'Éditeur : cartes remises sur le code du jeu';}
export function createGitHubStore(fetcher=fetch,storage=globalThis.localStorage){let loaded=null;
 const token={get(){try{return storage?.getItem(TOKEN_KEY)||'';}catch{return '';}},set(v){const t=String(v||'').trim();try{t?storage?.setItem(TOKEN_KEY,t):storage?.removeItem(TOKEN_KEY);}catch{}return t;},forget(){try{storage?.removeItem(TOKEN_KEY);}catch{}}};
 const need=t=>{const v=(t??token.get()).trim();if(!v)throw new GitHubError('jeton','Colle d’abord ton jeton GitHub.');return v;};
 // Lit le fichier publié sur main (sans jeton si besoin : dépôt public). Fichier absent = premier envoi.
 async function read(t=token.get()){let r;try{r=await fetcher(CONTENTS+'?ref='+MAIN,{headers:headers(t),cache:'no-store',redirect:'error'});}catch{throw new GitHubError('reseau','Connexion à GitHub impossible. Vérifie le réseau puis réessaie.');}
  if(r.status===404){loaded={sha:null,project:null};return loaded;}if(!r.ok)await fail(r,'lecture');const data=await r.json();if(data.type!=='file'||!data.sha||data.encoding!=='base64')throw new GitHubError('format','Fichier de carte GitHub incompatible.');let project;try{project=JSON.parse(decode(data.content));}catch{throw new GitHubError('format','Le fichier publié sur GitHub n’est pas un JSON lisible.');}loaded={sha:data.sha,project};return loaded;}
 function body(project,message,branch,sha){const json=JSON.stringify(project,null,2)+'\n';if(new TextEncoder().encode(json).length>MAX_BYTES)throw new GitHubError('taille','Projet trop volumineux pour GitHub (900 ko maximum). Télécharge le JSON.');return JSON.stringify({message:String(message||'').slice(0,200)||'Éditeur : cartes modifiées',branch,content:encode(json),...(sha?{sha}:{})});}
 // Envoi : jamais d'écrasement silencieux. Le SHA lu avant l'envoi est transmis ; s'il a changé, GitHub refuse (409/422) et on relit la version fraîche.
 async function publish(project,{token:t,message,pr=false,zones=[],date=new Date()}={}){const tk=need(t);if(!loaded)await read(tk);const expected=loaded.sha;
  try{if(!pr){const res=await call(fetcher,CONTENTS,{method:'PUT',headers:{...headers(tk),'Content-Type':'application/json'},body:body(project,message,MAIN,expected)},'fichier');if(!res.commit?.sha||!res.content?.sha)throw new GitHubError('http','GitHub n’a pas confirmé l’écriture.');loaded={sha:res.content.sha,project};return {kind:'commit',sha:res.commit.sha,url:res.commit.html_url||`https://github.com/${REPOSITORY}/commit/${res.commit.sha}`};}
   const ref=await call(fetcher,`${API}/git/ref/heads/${MAIN}`,{headers:headers(tk)},'branche main',true),branch=branchFor(zones,date);
   await call(fetcher,`${API}/git/refs`,{method:'POST',headers:{...headers(tk),'Content-Type':'application/json'},body:JSON.stringify({ref:'refs/heads/'+branch,sha:ref.object.sha})},'création de branche',true);
   const res=await call(fetcher,CONTENTS,{method:'PUT',headers:{...headers(tk),'Content-Type':'application/json'},body:body(project,message,branch,expected)},'fichier',true);
   const pull=await call(fetcher,`${API}/pulls`,{method:'POST',headers:{...headers(tk),'Content-Type':'application/json'},body:JSON.stringify({title:String(message||'').slice(0,200)||'Éditeur : cartes modifiées',head:branch,base:MAIN,body:`Proposé depuis l’éditeur de cartes (${MAP_PATH}).\nZones : ${zones.join(', ')||'aucune (retour au code du jeu)'}.`})},'pull request',true);
   return {kind:'pr',branch,number:pull.number,url:pull.html_url,commit:res.commit?.sha};}
  catch(e){if(e.code==='conflit'){const fresh=await read(tk).catch(()=>null);throw new GitHubError('conflit',e.message,{fresh});}throw e;}}
 return {token,read,publish,get reference(){return loaded&&{sha:loaded.sha};},clear(){loaded=null;}};
}

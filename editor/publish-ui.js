// Bouton unique « Publier sur GitHub » : jeton mémorisé dans ce navigateur, dépôt / main / fichier préremplis, message automatique,
// commit direct sur main (ou PR en option), validation avant envoi, conflit -> version fraîche et nouvel essai proposé.
import {createGitHubStore,MAP_PATH,REPOSITORY,MAIN,TOKEN_URL,defaultMessage} from './github-store.js';
import {prepareExport,mergeRemote} from './publication.js';
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[c]);
export function initPublication(api,{store=createGitHubStore()}={}){const modal=document.createElement('dialog');modal.id='publication';
 modal.innerHTML=`<form method="dialog"><div class="panel-heading"><h2>Publier sur GitHub</h2><button aria-label="Fermer">×</button></div></form>
 <p class="pub-target"><strong>${REPOSITORY}</strong> · branche <code>${MAIN}</code> · <code>${MAP_PATH}</code></p>
 <p id="pubZones"></p>
 <div id="pubHelp" class="pub-help" hidden><p>Pour publier, crée un jeton GitHub limité à ce dépôt, puis colle-le ci-dessous : <a id="pubTokenLink" href="${TOKEN_URL}" target="_blank" rel="noopener">créer le jeton ↗</a> (dépôt <strong>${REPOSITORY}</strong>, permission <strong>Contents : Read and write</strong><span id="pubHelpPr" hidden> et <strong>Pull requests : Read and write</strong></span>).</p></div>
 <label>Jeton GitHub<input id="gitToken" type="password" autocomplete="off" spellcheck="false" placeholder="github_pat_…"></label>
 <p class="form-help">Le jeton reste uniquement dans ce navigateur (jamais dans le dépôt ni dans les cartes). <button id="pubForget" type="button" class="link">Oublier le jeton</button></p>
 <label>Message du commit<input id="gitMessage" maxlength="200"></label>
 <label class="pub-check"><input id="pubPr" type="checkbox"> Proposer en PR plutôt</label>
 <div class="form-row"><button id="gitWrite" class="primary">Publier sur GitHub</button><button id="pubRetry" hidden>Réessayer avec la version actuelle</button><button id="pubDownload">Télécharger le JSON</button></div>
 <div id="gitResult" role="status" aria-live="polite"></div>
 <details><summary>Autres options</summary><p class="form-help">Écrire directement dans un dépôt local (navigateurs compatibles) ; le push Git reste séparé.</p><button id="folderWrite">Choisir le dépôt local et enregistrer</button></details>`;
 document.body.append(modal);const $=id=>modal.querySelector('#'+id);let busy=false,prepared=null,pending=null;
 const status=(html,kind='')=>{$('gitResult').className=kind;$('gitResult').innerHTML=html;};
 const errorList=e=>`<strong>Envoi refusé : la carte n’est pas valide.</strong><ul>${(e.issues||[e.message]).slice(0,20).map(i=>`<li>${esc(i)}</li>`).join('')}</ul>${(e.issues?.length||0)>20?`<p>… et ${e.issues.length-20} autres.</p>`:''}<p>Corrige ces points, puis publie à nouveau.</p>`;
 const help=()=>{const pr=$('pubPr').checked;$('pubHelp').hidden=!!store.token.get()&&!pr;$('pubHelpPr').hidden=!pr;};
 const prepare=()=>{prepared=prepareExport(api.getDocument(),api.base);return prepared;};
 const refreshSummary=()=>{try{const p=prepare();$('pubZones').textContent=p.zones.length?`Zones modifiées : ${p.zones.join(', ')}. Les autres zones restent celles du code du jeu.`:'Aucune zone modifiée : publier remet toutes les zones sur le code du jeu.';if(!$('gitMessage').dataset.edited)$('gitMessage').value=defaultMessage(p.zones);return true;}catch(e){prepared=null;$('pubZones').textContent='';status(errorList(e),'error');return false;}};
 const run=async fn=>{if(busy)return;busy=true;for(const b of modal.querySelectorAll('button'))b.disabled=true;try{await fn();}catch(e){status(esc(e.message),'error');}finally{busy=false;for(const b of modal.querySelectorAll('button'))b.disabled=false;}};
 const done=res=>{pending=null;$('pubRetry').hidden=true;if(res.kind==='pr'){status(`<strong>PR ouverte</strong> : <a href="${esc(res.url)}" target="_blank" rel="noopener">voir la PR #${esc(res.number)} ↗</a> (branche <code>${esc(res.branch)}</code>). La carte sera publiée quand la PR sera fusionnée dans main.`,'ok');api.toast('PR ouverte sur GitHub.');}
  else{status(`<strong>Publié</strong> sur main : <a href="${esc(res.url)}" target="_blank" rel="noopener">voir le commit ${esc(res.sha.slice(0,7))} ↗</a>. GitHub Pages met environ 1 minute à mettre le jeu à jour.`,'ok');api.toast('Carte publiée sur GitHub.');}};
 const send=async project=>{const token=store.token.set($('gitToken').value);if(!token)throw Error('Colle d’abord ton jeton GitHub (lien ci-dessus).');status('Publication en cours…','busy');try{done(await store.publish(project,{token,message:$('gitMessage').value,pr:$('pubPr').checked,zones:prepared.zones}));help();}
  catch(e){if(e.code==='conflit'){pending=e.fresh;const m=mergeRemote(prepared,e.fresh?.project,api.base);$('pubRetry').hidden=false;status(`<strong>Conflit</strong> : quelqu’un a publié sur GitHub depuis ta lecture. Rien n’a été écrasé.<br>« Réessayer » repart de la version actuelle de GitHub et n’y remplace que tes zones (${esc(prepared.zones.join(', ')||'aucune')})${m.both.length?` ; attention, ${esc(m.both.join(', '))} a aussi été modifiée sur GitHub : ta version la remplacera`:''}.`,'error');return;}if(e.code==='jeton'||e.code==='droits'){$('pubHelp').hidden=false;$('pubHelpPr').hidden=!$('pubPr').checked;}throw e;}};
 $('gitWrite').onclick=()=>run(async()=>{if(!refreshSummary())return;await send(prepared.project);});
 $('pubRetry').onclick=()=>run(async()=>{if(!refreshSummary())return;const m=mergeRemote(prepared,pending?.project,api.base);await send(m.project);});
 $('pubDownload').onclick=()=>{if(!refreshSummary())return;const url=URL.createObjectURL(new Blob([prepared.json],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download='editor-maps.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);status(`JSON téléchargé : remplace <code>${MAP_PATH}</code> par ce fichier.`,'ok');};
 $('pubForget').onclick=()=>{store.token.forget();$('gitToken').value='';help();status('Jeton oublié dans ce navigateur.','ok');};
 $('pubPr').onchange=help;$('gitMessage').oninput=()=>{$('gitMessage').dataset.edited='1';};
 $('folderWrite').onclick=async()=>{try{if(!window.showDirectoryPicker)throw Error('Ce navigateur ne permet pas l’écriture de dossiers. Utilise « Publier sur GitHub » ou « Télécharger le JSON ».');if(!refreshSummary())return;const root=await window.showDirectoryPicker({mode:'readwrite'});await root.getFileHandle('index.html');const src=await root.getDirectoryHandle('src'),data=await src.getDirectoryHandle('data');await data.getFileHandle('dusk_town.js');const file=await data.getFileHandle('editor-maps.json',{create:true}),writer=await file.createWritable();await writer.write(prepared.json);await writer.close();status('Fichier du jeu écrit : '+MAP_PATH+'. Tu peux lancer le jeu local puis committer ce fichier.','ok');}catch(e){status(esc(e.name==='AbortError'?'Écriture annulée.':e.message),'error');}};
 const gameLink=document.querySelector('header .game-link');if(gameLink){gameLink.textContent='Jeu publié ↗';gameLink.onclick=()=>{gameLink.href='./?dev=1&map='+encodeURIComponent(api.getLocation());};}
 const open=()=>{status('');$('pubRetry').hidden=true;pending=null;$('gitToken').value=store.token.get();delete $('gitMessage').dataset.edited;help();refreshSummary();store.clear();modal.showModal();};
 document.getElementById('publishProject').onclick=open;return {open,modal};
}

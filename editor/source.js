import * as sourceWorld from '../src/data/dusk_town.js';
import {createEditorBase} from './base.js';
import {validate} from './model.js';
import {chargerCatalogue} from '../src/core/catalogue.js';
// Même catalogue que le jeu : tous les manifestes, y compris assets/steel/<quartier>/manifest.json.
export async function loadEditorSource(){
 const get=async path=>{const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw Error('Chargement impossible : '+path);return r.json();};
 const [catalogue,published]=await Promise.all([chargerCatalogue(get),get('./src/data/editor-maps.json')]);
 const base=createEditorBase(sourceWorld,catalogue);let doc=null;try{doc=published?validate(published,base):null;}catch(e){console.warn('Cartes publiées invalides, source du jeu utilisée :',e.message);}
 return {base,published:doc};
}

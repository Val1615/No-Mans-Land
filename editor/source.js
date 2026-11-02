import * as sourceWorld from '../src/data/dusk_town.js';
import {createEditorBase} from './base.js';
import {validate} from './model.js';
export async function loadEditorSource(){
 const get=async path=>{const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw Error('Chargement impossible : '+path);return r.json();};
 const [sprites,iman,bman,published]=await Promise.all(['assets/reused/manifest.json','assets/interiors/manifest.json','assets/buildings/manifest.json','src/data/editor-maps.json'].map(get));
 const base=createEditorBase(sourceWorld,{sprites,bman,iman});return {base,published:published?validate(published,base):null};
}

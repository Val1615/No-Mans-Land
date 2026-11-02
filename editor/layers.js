export const LAYERS={zone:'Sols',building:'Bâtiments',prop:'Objets',actor:'Personnages'};
export const defaultLayers=()=>Object.fromEntries(Object.keys(LAYERS).map(k=>[k,{visible:true,locked:false}]));
export function canEdit(kind,active,layers){return kind===active&&!!layers[kind]?.visible&&!layers[kind]?.locked;}
export function allowedKinds(active,layers){return Object.keys(LAYERS).filter(k=>canEdit(k,active,layers));}

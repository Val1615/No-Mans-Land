# Outils communs : chevauchements icône/libellé entre repères ; élément visible au-dessus (elementFromPoint).
def chevauchements(E, sel):
    return E("""(sel=>{const R=[...document.querySelectorAll(sel)].flatMap((b,k)=>[...b.querySelectorAll('img:not(.me),span')].map(e=>[k,(b.dataset.key||b.dataset.lieu)+':'+e.tagName,e.getBoundingClientRect(),getComputedStyle(e)])).filter(([,,r,c])=>r.width>0&&c.display!=='none'&&c.visibility!=='hidden');
      const o=[];for(let i=0;i<R.length;i++)for(let j=i+1;j<R.length;j++){const[ka,a,r]=R[i],[kb,b,s]=R[j];if(ka===kb)continue;const w=Math.min(r.right,s.right)-Math.max(r.left,s.left),h=Math.min(r.bottom,s.bottom)-Math.max(r.top,s.top);if(w>1&&h>1)o.push(a+'/'+b)}return o})""", sel)
def dessus(E, id):
    return E("""(id=>{const m=document.getElementById(id);if(!m||!m.textContent)return 'vide';const pe=m.style.pointerEvents;m.style.pointerEvents='auto';const r=m.getBoundingClientRect(),pts=[[r.left+r.width/2,r.top+r.height/2],[r.left+8,r.top+r.height/2],[r.right-8,r.top+r.height/2]];
      const ok=pts.every(([x,y])=>{const e=document.elementFromPoint(x,y);return e&&(e===m||m.contains(e))});m.style.pointerEvents=pe;return ok})""", id)

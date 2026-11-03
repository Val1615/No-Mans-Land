// Shared analytic projection for editor input and both rendering paths.
const yaw=34.5*Math.PI/180,pitch=28.8*Math.PI/180;
export const AXES={rx:Math.cos(yaw),rz:-Math.sin(yaw),ux:-Math.sin(yaw)*Math.sin(pitch),uz:-Math.cos(yaw)*Math.sin(pitch),uy:Math.cos(pitch)};
export function plane(p){return {x:p.x*AXES.rx+p.z*AXES.rz,y:p.x*AXES.ux+p.z*AXES.uz+(p.y||0)*AXES.uy};}
export function inverse(x,y){const a=AXES,d=a.rx*a.uz-a.rz*a.ux;return {x:(x*a.uz-a.rz*y)/d,z:(a.rx*y-x*a.ux)/d};}
export function project(camera,p){const a=plane({x:p.x-camera.x,z:p.z-camera.z,y:p.y||0});return {x:camera.cx+a.x*camera.ppm,y:camera.cy-a.y*camera.ppm};}
export function unproject(camera,p){const q=inverse((p.x-camera.cx)/camera.ppm,-(p.y-camera.cy)/camera.ppm);return {x:camera.x+q.x,z:camera.z+q.z};}
export function panFrom(start,from,to){const a=unproject(start,from),b=unproject(start,to);return {...start,x:start.x+a.x-b.x,z:start.z+a.z-b.z};}
export function zoomAt(start,factor,anchor){const before=unproject(start,anchor),next={...start,ppm:Math.max(4,Math.min(120,start.ppm*factor))},after=unproject(next,anchor);next.x+=before.x-after.x;next.z+=before.z-after.z;return next;}
export function pinchFrom(start,initialMid,currentMid,factor){const next=zoomAt(start,factor,initialMid);return panFrom(next,initialMid,currentMid);}
export function fitBounds(bounds,viewport){const w=Math.max(100,viewport.right-viewport.left),h=Math.max(100,viewport.bottom-viewport.top),ppm=Math.max(4,Math.min(110,Math.min(w/Math.max(1,bounds.x1-bounds.x0),h/Math.max(1,bounds.y1-bounds.y0))*.92)),p=inverse((bounds.x0+bounds.x1)/2,(bounds.y0+bounds.y1)/2);return {...p,ppm,cx:(viewport.left+viewport.right)/2,cy:(viewport.top+viewport.bottom)/2};}
export function sceneBounds(loc,base){const p=[];const add=(x,z,y=0)=>p.push(plane({x,z,y}));for(const x of [0,loc.size.w])for(const z of [0,loc.size.d])add(x,z,loc.kind==='interior'?3:0);for(const x of [0,loc.size.w])for(const z of [0,loc.size.d])add(x,z);
for(const b of loc.buildings){const m=base.bman[b.sprite];if(!m)continue;const q=plane({x:b.x+b.w+(b.ancre?.[0]||0),z:b.z+b.d+(b.ancre?.[1]||0)}),k=(b.k||1)/50;for(const x of [q.x-m.anchor[0]*k,q.x+(m.px[0]-m.anchor[0])*k])for(const y of [q.y-(m.px[1]-m.anchor[1])*k,q.y+m.anchor[1]*k])p.push({x,y});}
return {x0:Math.min(...p.map(q=>q.x)),x1:Math.max(...p.map(q=>q.x)),y0:Math.min(...p.map(q=>q.y)),y1:Math.max(...p.map(q=>q.y))};}

from atlas_data import *
from math import hypot

def inside(p,b):return b['x']<p[0]<b['x']+b['w'] and b['y']<p[1]<b['y']+b['h']
def poly_inside(p,pts):
 x,y=p;hit=False
 for a,b in zip(pts,pts[1:]+pts[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:hit=not hit
 return hit

def clip_rect(poly,b):
 for axis,value,sign in [(0,b['x'],1),(0,b['x']+b['w'],-1),(1,b['y'],1),(1,b['y']+b['h'],-1)]:
  out=[]
  if not poly:return []
  for a,c in zip(poly[-1:]+poly[:-1],poly):
   ai=(a[axis]-value)*sign>=0;ci=(c[axis]-value)*sign>=0
   if ai!=ci:
    t=(value-a[axis])/(c[axis]-a[axis]);out.append((a[0]+(c[0]-a[0])*t,a[1]+(c[1]-a[1])*t))
   if ci:out.append(c)
  poly=out
 return poly

def area(poly):return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])))/2 if poly else 0

def intersections(q):
 issues=[];bs=q['buildings']
 for i,b in enumerate(bs):
  if not (0<=b['x']<b['x']+b['w']<=100 and 0<=b['y']<b['y']+b['h']<=80):issues.append(('BOUND',b['id']))
  for c in bs[i+1:]:
   overlap=max(0,min(b['x']+b['w'],c['x']+c['w'])-max(b['x'],c['x']))*max(0,min(b['y']+b['h'],c['y']+c['h'])-max(b['y'],c['y']))
   if overlap:issues.append(('BUILDING',b['id'],c['id'],overlap))
  if b['status'] in ['O','C']:
   x,y,w,h=b['x'],b['y'],b['w'],b['h'];p={'N':(x+w/2,y-1.5),'S':(x+w/2,y+h+1.5),'W':(x-1.5,y+h/2),'E':(x+w+1.5,y+h/2)}[b['face']]
   for c in bs:
    if c is not b and inside(p,c):issues.append(('DOOR',b['id'],'against',c['id']))
   for f in q['features']:
    if f['kind'] in ['eau','canal','impact'] and poly_inside(p,f['points']):issues.append(('DOOR WATER',b['id']))
  for r in q['roads']:
   if r['kind']=='sureleve':continue
   overlap=0
   for a,c in zip(r['points'],r['points'][1:]):
    dx,dy=c[0]-a[0],c[1]-a[1];length=hypot(dx,dy)
    if not length:continue
    ox,oy=-dy/length*r['w']/2,dx/length*r['w']/2
    poly=[(a[0]+ox,a[1]+oy),(c[0]+ox,c[1]+oy),(c[0]-ox,c[1]-oy),(a[0]-ox,a[1]-oy)]
    overlap+=area(clip_rect(poly,b))
   if overlap>3:issues.append(('ROAD',b['id'],r['name'],round(overlap,1)))
 return issues
if __name__=='__main__':
 issues=[(q['id'],*i) for q in PLANS for i in intersections(q)]
 for i in issues:print(*i)
 print('ISSUES',len(issues))

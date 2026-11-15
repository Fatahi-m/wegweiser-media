import sys,re
sys.path.insert(0,"../batch2")
from split import load, split_lines, SR
name=sys.argv[1]; thr=float(sys.argv[2]) if len(sys.argv)>2 else -32
x=load(name+".wav")
paras=[l for l in open(name+".txt").read().split("\n") if l]
segs,gaps,cuts=split_lines(x,len(paras),[len(p) for p in paras],thr)
res=[]
for i,p in enumerate(paras):
  a,b=cuts[i]/100,cuts[i+1]/100
  units=[s for s in re.split(r"(?<=[.؟?:;؛،,])\s+",p) if s.strip()]
  sub=x[cuts[i]*441:cuts[i+1]*441]
  if len(units)>1:
    try: _,g2,c2=split_lines(sub,len(units),[len(u) for u in units],thr-4)
    except Exception as e: c2=None
  else: c2=[0,len(sub)//441]
  print(f"P{i} {a:6.2f}-{b:6.2f} {(b-a)/len(p)*100:5.2f}s/100c gap{gaps[i-1] if i else 0:.2f}")
  if c2:
    for j,u in enumerate(units): print(f"     {a+c2[j]/100:6.2f} {u[:45]}")

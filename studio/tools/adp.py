import subprocess,re,math,sys
wav,txt=sys.argv[1],sys.argv[2]
o=subprocess.run(['ffmpeg','-i',wav,'-af','silencedetect=n=-35dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
ss=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',o)]; se=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',o)]
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',wav],capture_output=True,text=True).stdout)
sil=[(a,b) for a,b in zip(ss,se) if b>0.05 and a<dur-0.3]
start=sil[0][1] if sil and sil[0][0]<0.05 else 0.0
cands=[(b,b-a) for a,b in sil if a>0.5]   # boundary = silence end
P=[l for l in open(txt).read().split('\n') if l.strip()]
L=[len(p) for p in P]; end=[a for a,b in sil if a>dur-2][:1] or [dur]; end=end[-1] if sil[-1][0]>dur-2 else dur
end=sil[-1][0] if sil[-1][1]>=dur-0.05 else dur
rate=(end-start)/sum(L)
N=len(P); C=len(cands)
INF=1e9; pts=[(start,0)]+cands+[(end+0.0,0)]
import functools
@functools.lru_cache(None)
def f(i,k):  # paragraph i starts at pts[k]; return min cost
  if i==N: return (0,()) if k==len(pts)-1 else (INF,())
  best=(INF,())
  for j in range(k+1,len(pts)):
    if i==N-1 and j!=len(pts)-1: continue
    d=pts[j][0]-pts[k][0]-(pts[j][1] if j<len(pts)-1 else 0)
    if d<=0: continue
    c=math.log(d/(L[i]*rate))**2 - (2.0*pts[j][1] if j<len(pts)-1 else 0)
    r=f(i+1,j)
    if c+r[0]<best[0]: best=(c+r[0],(pts[k][0],)+r[1])
  return best
c,s=f(0,0); print(round(c,2)); print([round(x,2) for x in s], round(end,2))

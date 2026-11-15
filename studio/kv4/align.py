import sys,re,subprocess
name=sys.argv[1]
dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",name+".wav"]))
out=subprocess.run(["ffmpeg","-hide_banner","-i",name+".wav","-af","silencedetect=n=-32dB:d=0.2","-f","null","-"],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r"silence_start: ([0-9.]+)",out)]; en=[float(x) for x in re.findall(r"silence_end: ([0-9.]+)",out)]
P=list(zip(st,en)); s0=P[0][1] if P and P[0][0]<0.05 else 0; e0=P[-1][0] if P and P[-1][1]>dur-0.05 else dur
paras=[l for l in open(name+".txt").read().split("\n") if l]
# sentence-level units
units=[]
for pi,p in enumerate(paras):
  for s in re.split(r"(?<=[.؟?:;؛])\s+",p):
    if s.strip(): units.append((pi,s))
L=[len(s) for _,s in units]; T=sum(L); c=0
print(name,"dur",dur,"speech",s0,e0,"chars",T,"rate",round(T/(e0-s0),1))
for (pi,s),l in zip(units,L):
  est=s0+(e0-s0)*c/T; c+=l
  near=min(P,key=lambda p:abs(p[1]-est)) if P else (0,0)
  print(f"P{pi} est {est:6.2f} pause_end {near[1]:6.2f} ({near[1]-near[0]:.2f}) | {s[:40]}")

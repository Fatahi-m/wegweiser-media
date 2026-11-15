#!/usr/bin/env python3
"""seqsplice.py cfg.json outdir
cfg: {"seq": [["P","a.wav"],["G","b.wav"],...]}  -> outdir/voice.wav + timings.json {"segs":[{"k":"P","t":[a,b],"pauses":[...]}...],"total":T}"""
import sys, json, subprocess
sys.argv_backup = sys.argv
import numpy as np
exec(open(__file__.replace("seqsplice.py", "splice2.py")).read().split("cfg = json.load")[0])
cfg = json.load(open(sys.argv_backup[1])); od = sys.argv_backup[2]
GAP = {("P", "G"): 0.10, ("G", "P"): 0.18, ("G", "G"): 0.42, ("P", "P"): 0.25}
LEAD, TAIL = 0.25, 0.4
auds = []
for k, f in cfg["seq"]:
    x = trim(load(f), keep=0.04 if k == "G" else 0.03)
    if k == "P": x = squeeze(x)
    auds.append((k, x))
ref = np.median([rms(x) for k, x in auds if k == "P"])
auds = [(k, fade(x * (ref / rms(x)) if k == "G" else x)) for k, x in auds]
sil = lambda s: np.zeros(int(SR * s), np.float32)
out = [sil(LEAD)]; t = LEAD; segs = []; prev = None
for k, x in auds:
    if prev: out.append(sil(GAP[(prev, k)])); t += GAP[(prev, k)]
    pz = [[t + a, t + b] for a, b in pauses(x)] if k == "P" else []
    segs.append({"k": k, "t": [t, t + len(x) / SR], "pauses": pz}); out.append(x); t += len(x) / SR; prev = k
out.append(sil(TAIL)); t += TAIL
y = np.concatenate(out); y = y / max(1e-6, np.abs(y).max()) * 0.89
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", od + "/voice.wav"],
               input=y.astype(np.float32).tobytes(), check=True)
json.dump({"segs": segs, "total": t}, open(od + "/timings.json", "w"), indent=1)
print(json.dumps([[s["k"], round(s["t"][0], 2), round(s["t"][1], 2)] for s in segs]), round(t, 2))

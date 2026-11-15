#!/usr/bin/env python3
"""splice.py P1..P7 (mp3) GERMAN.mp3 out_dir -> out_dir/voice.wav + timings.json"""
import sys, subprocess, json, numpy as np
SR = 44100
def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()
def trim(x, thr_db=-42, keep=0.03):
    win = int(SR * 0.01); n = len(x) // win
    e = 20 * np.log10(np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1)) + 1e-9)
    idx = np.where(e > thr_db)[0]
    a = max(0, idx[0] * win - int(keep * SR)); b = min(len(x), (idx[-1] + 1) * win + int(keep * SR))
    return x[a:b]
def rms(x):
    win = int(SR * 0.05); n = len(x) // win
    r = np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1)); return np.median(r[r > np.percentile(r, 40)])
def words(x, thr_db=-40, min_gap=0.25):
    """split German file into word chunks at silences >= min_gap"""
    win = int(SR * 0.01); n = len(x) // win
    e = 20 * np.log10(np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1)) + 1e-9)
    voiced = e > thr_db; segs = []; i = 0
    while i < n:
        if voiced[i]:
            j = i
            while j < n:
                k = j
                while k < n and not voiced[k]: k += 1
                if k - j >= min_gap * 100 or k >= n: break
                j = k + 1 if k < n else k
                while j < n and voiced[j]: j += 1
            segs.append((i, j)); i = j
        else: i += 1
    segs = [(a, b) for a, b in segs if b - a > 15]
    return [x[max(0, a * win - int(.03 * SR)):min(len(x), b * win + int(.04 * SR))] for a, b in segs]
def pauses(x, thr_db=-38, min_gap=0.12):
    win = int(SR * 0.01); n = len(x) // win
    e = 20 * np.log10(np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1)) + 1e-9)
    out = []; i = 0
    while i < n:
        if e[i] <= thr_db:
            j = i
            while j < n and e[j] <= thr_db: j += 1
            if (j - i) >= min_gap * 100 and i > 5 and j < n - 5: out.append([i / 100, j / 100])
            i = j
        else: i += 1
    return out
def squeeze(x, thr_db=-40, maxgap=0.38):
    win = int(SR * 0.01); n = len(x) // win
    e = 20 * np.log10(np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1)) + 1e-9)
    keep = np.ones(len(x), bool); i = 0; mg = int(maxgap * 100)
    while i < n:
        if e[i] <= thr_db:
            j = i
            while j < n and e[j] <= thr_db: j += 1
            if j - i > mg and i > 0 and j < n:
                a = (i + mg // 2) * win; b = (j - mg // 2) * win
                keep[a:b] = False
            i = j
        else: i += 1
    return x[keep]
def fade(x, ms=8):
    k = int(SR * ms / 1000); x = x.copy(); x[:k] *= np.linspace(0, 1, k); x[-k:] *= np.linspace(1, 0, k); return x

cfg = json.load(open(sys.argv[1])); P = [squeeze(trim(load(p))) for p in cfg["P"]]
G = [trim(load(g), keep=0.04) for g in cfg["G"]]
nP, nG = len(P), len(G)
ref = np.median([rms(p) for p in P])
G = [fade(g * (ref / rms(g))) for g in G]
P = [fade(p) for p in P]
GAP_PG, GAP_GP, LEAD, TAIL = 0.10, 0.18, 0.25, 0.45
sil = lambda s: np.zeros(int(SR * s), np.float32)
out = [sil(LEAD)]; t = LEAD; Pt = []; Gt = []
PP = []
for i in range(nP):
    PP.append([[t + a, t + b] for a, b in pauses(P[i])])
    Pt.append([t, t + len(P[i]) / SR]); out.append(P[i]); t += len(P[i]) / SR
    if i < nG:
        out.append(sil(GAP_PG)); t += GAP_PG
        Gt.append([t, t + len(G[i]) / SR]); out.append(G[i]); t += len(G[i]) / SR
        out.append(sil(GAP_GP)); t += GAP_GP
out.append(sil(TAIL)); t += TAIL
y = np.concatenate(out); y = y / max(1e-6, np.abs(y).max()) * 0.89
od = sys.argv[2]
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", od + "/voice.wav"],
               input=y.astype(np.float32).tobytes(), check=True)
json.dump({"P": Pt, "G": Gt, "pauses": PP, "total": t}, open(od + "/timings.json", "w"), indent=1)
print(json.dumps({"P": Pt, "G": Gt, "total": t}))

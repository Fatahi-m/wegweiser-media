#!/usr/bin/env python3
"""split.py file.mp4 durP startG nLinesP nWordsG outprefix 'line chars csv'
Splits the Persian part (0..durP) into nLinesP lines using the longest silences (sanity-checked against
char proportions) and the German part (startG..end) into nWordsG word chunks. Writes outprefix_P{i}.wav / _G{i}.wav"""
import sys, subprocess, numpy as np
sys.path.insert(0, "/home/claude/wegweiser/batch2")
SR = 44100
def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()
def energy(x):
    win = int(SR * 0.01); n = len(x) // win
    return 20 * np.log10(np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1)) + 1e-9)
def silences(e, thr):
    out = []; i = 0; n = len(e)
    while i < n:
        if e[i] <= thr:
            j = i
            while j < n and e[j] <= thr: j += 1
            out.append((i, j)); i = j
        else: i += 1
    return out
def save(x, path):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", path],
                   input=x.astype(np.float32).tobytes(), check=True)

def split_lines(x, n, chars, thr=-45):
    e = energy(x); sil = [(a, b) for a, b in silences(e, thr) if a > 5 and b < len(e) - 5]
    # expected boundaries from char proportions
    tot = sum(chars); cum = np.cumsum(chars)[:-1] / tot * len(e)
    # DP: pick n-1 silences in order maximizing length minus deviation penalty
    S = sorted(sil); m = len(S)
    import functools
    best = {}
    def score(k, s):
        a, b = S[s]; mid = (a + b) / 2
        return (b - a) - 0.08 * abs(mid - cum[k])
    # dp[k][s] best total choosing boundary k at silence s
    NEG = -1e18
    dp = np.full((n - 1, m), NEG); bp = np.zeros((n - 1, m), int)
    for s in range(m): dp[0][s] = score(0, s)
    for k in range(1, n - 1):
        run_best, run_arg = NEG, -1
        for s in range(m):
            if s > 0 and dp[k - 1][s - 1] > run_best: run_best, run_arg = dp[k - 1][s - 1], s - 1
            if run_arg >= 0: dp[k][s] = run_best + score(k, s); bp[k][s] = run_arg
    s = int(np.argmax(dp[n - 2])); picks = [s]
    for k in range(n - 2, 0, -1): s = bp[k][s]; picks.append(s)
    picks = picks[::-1]
    cuts = [0] + [int((S[p][0] + S[p][1]) / 2) for p in picks] + [len(e)]
    win = int(SR * 0.01)
    segs = [x[cuts[i] * win:cuts[i + 1] * win] for i in range(n)]
    return segs, [(S[p][1] - S[p][0]) / 100 for p in picks], cuts

def split_words(x, n, thr=-42):
    e = energy(x); sil = [(a, b) for a, b in silences(e, thr) if a > 3 and b < len(e) - 3]
    sil = sorted(sorted(sil, key=lambda s: s[1] - s[0], reverse=True)[:n - 1])
    cuts = [0] + [int((a + b) / 2) for a, b in sil] + [len(e)]
    win = int(SR * 0.01)
    return [x[cuts[i] * win:cuts[i + 1] * win] for i in range(n)], [(b - a) / 100 for a, b in sil]

if __name__ == "__main__":
    f, durP, startG, nP, nG, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    chars = [int(c) for c in sys.argv[7].split(",")]
    x = load(f)
    P = x[:int((durP + 0.15) * SR)]; G = x[int((startG - 0.1) * SR):]
    segs, gaps, cuts = split_lines(P, nP, chars)
    print("P gaps:", gaps)
    for i, s in enumerate(segs):
        save(s, f"{out}_P{i}.wav"); print(f"P{i}", round(len(s) / SR, 2), "s  chars", chars[i], "ratio", round(len(s) / SR / chars[i] * 100, 2))
    ws, wg = split_words(G, nG)
    print("G gaps:", wg)
    for i, s in enumerate(ws): save(s, f"{out}_G{i}.wav"); print(f"G{i}", round(len(s) / SR, 2))

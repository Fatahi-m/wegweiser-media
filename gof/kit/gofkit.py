#!/usr/bin/env python3
"""Geld ohne Filter – 'Wie viel musst du sparen?' short. usage: sparen.py audio out.mp4 [--frames ...]"""
import os, sys, math, subprocess, json, re
KIT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, KIT)
from render import El, Dyn, text_sprite, rounded, shadowed, ease_out, ease_back, Image, ImageDraw, ImageFont, W, H, FPS
D = KIT
NAVY = (15, 26, 43); PANEL = (23, 38, 61); PANEL2 = (30, 50, 80); MUST = (242, 182, 50); RENT = (226, 104, 90)
LIFE = (90, 169, 226); SAVE = (108, 199, 154); CHALK = (238, 241, 244); MUTED = (147, 163, 184)
cx = W // 2
OFF = 170

def F(w, s): return ImageFont.truetype(KIT + "/fonts/InterDisplay-" + w + ".otf", s)
def T(s, size, col=CHALK, w="Black"): return text_sprite(s, F(w, size), col)
def fit(s, size, maxw, col=CHALK, w="Black"):
    while text_sprite(s, F(w, size), col).width > maxw and size > 20: size -= 2
    return text_sprite(s, F(w, size), col)

def de(n): return f"{n:,.0f}".replace(",", ".")

def pill(s, bg, fg, size=40, w="ExtraBold"):
    t = T(s, size, fg, w); c = rounded(t.width + 60, t.height + 26, (t.height + 26) // 2, bg); c.alpha_composite(t, (30, 13)); return c

def card(w, h, col=PANEL, r=40, outline=None):
    return rounded(w, h, r, col, outline=outline, ow=4 if outline else 0)

SUB = "Folge"; FOOT1 = "Keine Beratung"; FOOT2 = ""
def make_bg():
    bg = Image.new("RGBA", (W, H), NAVY + (255,)); d = ImageDraw.Draw(bg)
    for y in range(H):
        k = y / H; c = tuple(int(PANEL[i] * (1 - k) * 0.9 + NAVY[i] * (0.1 + k * 0.9)) for i in range(3)); d.line((0, y, W, y), fill=c)
    for x in range(0, W, 64): d.line((x, 0, x, H), fill=(28, 45, 73))
    for y in range(0, H, 64): d.line((0, y, W, y), fill=(28, 45, 73))
    # header
    logo = Image.open(D + "/brand/logo.png").convert("RGBA").resize((96, 96), Image.LANCZOS)
    m = Image.new("L", (96, 96), 0); ImageDraw.Draw(m).ellipse((0, 0, 95, 95), fill=255); logo.putalpha(m)
    bg.alpha_composite(logo, (70, 92))
    bg.alpha_composite(T("GELD OHNE FILTER", 44, MUST), (186, 100))
    bg.alpha_composite(T(SUB, 30, MUTED, "SemiBold"), (188, 150))
    # bottom strip
    d.rectangle((0, H - 120, W, H), fill=(11, 19, 32))
    ft = T(FOOT1, 28, MUTED, "SemiBold"); bg.alpha_composite(ft, (cx - ft.width // 2, H - 100))
    fs = T(FOOT2, 24, MUTED, "Medium"); bg.alpha_composite(fs, (cx - fs.width // 2, H - 58))
    return bg

def money_count(t0, dur, val, y, col, size=230, prefix="", suffix=" €", t_out=1e9):
    f = F("Black", size)
    def fn(frame, t):
        if t < t0 or t > t_out + 0.3: return
        p = ease_out((t - t0) / dur); o = ease_out((t - t0) / 0.25)
        if t > t_out: o *= 1 - ease_out((t - t_out) / 0.3)
        s = prefix + de(round(val * p)) + suffix
        sp = text_sprite(s, f, col)
        if o < 0.999: sp.putalpha(sp.getchannel("A").point(lambda a: int(a * o)))
        frame.alpha_composite(sp, (cx - sp.width // 2, y))
    return Dyn(fn)

def bar(t0, y, w, frac, col, t_out, h=46, label=None):
    def fn(frame, t):
        if t < t0 or t > t_out + 0.3: return
        o = ease_out((t - t0) / 0.3) * ((1 - ease_out((t - t_out) / 0.3)) if t > t_out else 1)
        p = ease_out((t - t0 - 0.2) / 0.9)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, w - 1, h - 1), h // 2, fill=(11, 19, 32))
        if p > 0.02: d.rounded_rectangle((0, 0, max(h, int(w * frac * p)) - 1, h - 1), h // 2, fill=col)
        if o < 0.999: im.putalpha(im.getchannel("A").point(lambda a: int(a * o)))
        frame.alpha_composite(im, (cx - w // 2, y))
    return Dyn(fn)


def rowcard(s, col, w=900, h=150, num=None, size=50):
    c = card(w, h, PANEL, 40, col); x = 40
    if num is not None:
        ic = Image.new("RGBA", (76, 76), (0, 0, 0, 0)); ImageDraw.Draw(ic).ellipse((0, 0, 75, 75), fill=col)
        it = T(str(num), 46, NAVY); ic.alpha_composite(it, ((76 - it.width) // 2, (76 - it.height) // 2 - 3)); c.alpha_composite(ic, (36, (h - 76) // 2)); x = 140
    st = fit(s, size, w - x - 40, CHALK, "ExtraBold"); c.alpha_composite(st, (x, (h - st.height) // 2))
    return shadowed(c, alpha=70)



def tile(title, val, col):
    c = card(420, 300, PANEL, 44, col)
    t1 = T(title, 46, MUTED, "ExtraBold"); c.alpha_composite(t1, ((420 - t1.width) // 2, 50))
    t2 = fit(val, 110, 380, col); c.alpha_composite(t2, ((420 - t2.width) // 2, 130))
    return shadowed(c, alpha=80)

def timings(script, total):
    """Estimate the start time (s) of every sentence. Lines = paragraphs. Returns (sentences, starts)."""
    segs = []
    for p in [l for l in script.strip().split("\n") if l.strip()]:
        ss = re.split(r'(?<=[.:!?])\s+', p.strip())
        for i, s in enumerate(ss): segs.append((s, i == len(ss) - 1))
    w = [len(s) + (16 if last else 9) for s, last in segs]
    k = (total - 0.3) / sum(w); t = 0.15; st = []
    for x in w: st.append(round(t, 2)); t += x * k
    return [s for s, _ in segs], st

def render(build, total, out, tt=None):
    """build() -> list of El. Renders a SILENT mp4 of length `total`; the voice is added later with vidiq_compose."""
    els = build(); bg = make_bg()
    def frame_at(t):
        f = bg.copy(); L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for e in els: e.draw(L, t)
        f.alpha_composite(L.crop((0, 0, W, H - OFF)), (0, OFF))
        d = ImageDraw.Draw(f); d.rectangle((0, 0, W, 12), fill=(11, 19, 32)); d.rectangle((0, 0, int(W * t / total), 12), fill=MUST)
        return f.convert("RGB")
    if tt:
        for t in tt: frame_at(t).save(f"{out}_{t:05.2f}.png")
        return
    n = int(math.ceil(total * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "-movflags", "+faststart", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n): pr.stdin.write(frame_at(i / FPS).tobytes())
    pr.stdin.close(); pr.wait()

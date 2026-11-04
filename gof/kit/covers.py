import os; KIT = os.path.dirname(os.path.abspath(__file__))
#!/usr/bin/env python3
"""Covers 1080x1920. Key content kept inside the centre 1080x1350 so the IG profile grid crop still reads."""
import math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = KIT
sys.path.insert(0, D + "/tax2")
VZ = D + "/fontdl/vz/fonts/ttf/Vazirmatn-"
INTER = KIT + "/fonts/"
W, H = 1080, 1920
OUT = D + "/covers/"

def fa(w, s): return ImageFont.truetype(VZ + w + ".ttf", s, layout_engine=ImageFont.Layout.RAQM)
def la(w, s, disp=True): return ImageFont.truetype(INTER + ("InterDisplay-" if disp else "Inter-") + w + ".otf", s, layout_engine=ImageFont.Layout.RAQM)

def tsprite(text, font, fill, rtl=False, pad=8, stroke=0, sfill=None):
    kw = dict(direction="rtl", language="fa") if rtl else {}
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    b = d.textbbox((0, 0), text, font=font, stroke_width=stroke, **kw)
    im = Image.new("RGBA", (b[2] - b[0] + 2 * pad, b[3] - b[1] + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - b[0], pad - b[1]), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=sfill, **kw)
    return im

def fit(text, mk, maxw, start, rtl=False, **kw):
    s = start
    while True:
        sp = tsprite(text, mk(s), rtl=rtl, **kw)
        if sp.width <= maxw or s < 30: return sp
        s -= 4

def shadow(im, r=26, off=(0, 18), a=140):
    pad = r * 2
    out = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    blk = Image.new("RGBA", im.size, (0, 0, 0, 255)); blk.putalpha(im.getchannel("A").point(lambda v: v * a // 255))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0)); sh.paste(blk, (pad + off[0], pad + off[1]), blk)
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(r))); out.alpha_composite(im, (pad, pad))
    return out, pad

def place(canvas, sp, cx, y, sh=False, rot=0):
    if rot: sp = sp.rotate(rot, resample=Image.BICUBIC, expand=True)
    pad = 0
    if sh: sp, pad = shadow(sp)
    canvas.alpha_composite(sp, (int(cx - sp.width / 2), int(y - pad)))
    return y + sp.height - 2 * pad

def box(sp, bg, padx=34, pady=18, r=26):
    b = Image.new("RGBA", (sp.width + 2 * padx, sp.height + 2 * pady), (0, 0, 0, 0))
    ImageDraw.Draw(b).rounded_rectangle((0, 0, b.width - 1, b.height - 1), r, fill=bg)
    b.alpha_composite(sp, (padx, pady)); return b

def gradient_bg(top, bot, glows=()):
    bg = Image.new("RGB", (W, H)); d = ImageDraw.Draw(bg)
    for y in range(H):
        k = y / H; d.line((0, y, W, y), fill=tuple(int(top[i] + (bot[i] - top[i]) * k) for i in range(3)))
    bg = bg.convert("RGBA")
    for (x, y, r, col, a) in glows:
        g = Image.new("RGBA", (4 * r, 4 * r), col + (0,))
        ImageDraw.Draw(g).ellipse((r, r, 3 * r, 3 * r), fill=col + (a,))
        bg.alpha_composite(g.filter(ImageFilter.GaussianBlur(r // 2)), (x - 2 * r, y - 2 * r))
    return bg

def rays(canvas, cx, cy, col, a=22, n=18):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(n):
        a0 = i * 2 * math.pi / n; a1 = a0 + math.pi / n * 0.55; R = 2200
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=col + (a,))
    canvas.alpha_composite(lay)

# ---------------- Netti ----------------
NAVY = (15, 26, 43); MUST = (242, 182, 50); MUST_D = (217, 154, 28); SKIN = (232, 196, 160)
def netti(size, mood="shock"):
    S = 4 * size; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); u = S / 800
    def e(x0, y0, x1, y1, **k): d.ellipse([v * u for v in (x0, y0, x1, y1)], **k)
    e(70, 70, 730, 730, fill=NAVY)
    e(190, 260, 610, 650, fill=SKIN)
    d.chord([v * u for v in (183, 205, 617, 520)], 180, 360, fill=MUST)
    d.rounded_rectangle([v * u for v in (180, 360, 620, 420)], radius=int(28 * u), fill=MUST_D)
    e(363, 143, 437, 217, fill=MUST_D)
    lw = int(12 * u)
    for cx in (325, 475):
        e(cx - 55, 415, cx + 55, 525, outline=NAVY, width=lw)
    d.line([v * u for v in (380, 468, 420, 468)], fill=NAVY, width=lw)
    if mood == "shock":
        for cx in (325, 475): e(cx - 16, 455, cx + 16, 487, fill=NAVY)
        e(370, 545, 430, 625, fill=NAVY)                      # open "O" mouth
        d.arc([v * u for v in (255, 375, 345, 415)], 200, 340, fill=NAVY, width=lw)   # raised brows
        d.arc([v * u for v in (455, 375, 545, 415)], 200, 340, fill=NAVY, width=lw)
    elif mood == "think":
        for cx in (338, 488): e(cx - 13, 448, cx + 13, 474, fill=NAVY)   # eyes looking up-right
        d.line([v * u for v in (365, 590, 445, 575)], fill=NAVY, width=lw)
    else:
        for cx in (325, 475): e(cx - 13, 463, cx + 13, 489, fill=NAVY)
        d.arc([v * u for v in (345, 520, 455, 590)], 20, 160, fill=NAVY, width=lw)
    return im.resize((size, size), Image.LANCZOS)

def footer(c, handle):
    t = tsprite(handle, la("Bold", 40, False), (170, 185, 205)); c.alpha_composite(t, ((W - t.width) // 2, 1700))

def qmark(size, col):
    return tsprite("?", la("Black", size), col)

# ======================= German 1: Mindestlohn =======================
def de_mindestlohn():
    c = gradient_bg((22, 36, 60), (8, 14, 26), [(900, 650, 380, (242, 182, 50), 70), (150, 1500, 380, (226, 104, 90), 60)])
    rays(c, 540, 900, (242, 182, 50), a=14)
    d = ImageDraw.Draw(c)
    y = 330
    y = place(c, box(tsprite("MINDESTLOHN", la("Black", 64), NAVY), MUST, 40, 16, 20), 540, y, rot=-3) + 40
    y = place(c, fit("So lebst du", lambda s: la("Black", s), 940, 150, fill=(238, 241, 244)), 540, y) - 10
    y = place(c, fit("WIRKLICH", lambda s: la("Black", s), 960, 210, fill=MUST, stroke=0), 540, y, sh=True) + 30
    # price tag with hidden value
    tag = Image.new("RGBA", (700, 230), (0, 0, 0, 0)); td = ImageDraw.Draw(tag)
    td.rounded_rectangle((0, 0, 699, 229), 40, fill=(238, 241, 244))
    td.text((40, 20), "NETTO / MONAT", font=la("Bold", 34, False), fill=(90, 105, 125))
    qs = tsprite("?.??? €", la("Black", 120), (226, 104, 90))
    tag.alpha_composite(qs, ((700 - qs.width) // 2, 70))
    place(c, tag, 420, y + 60, sh=True, rot=4)
    n = netti(380, "shock"); n, p = shadow(n)
    c.alpha_composite(n, (W - 380 - 20 - p, y + 260 - p))
    place(c, tsprite("Reicht das zum Leben?", la("ExtraBold", 66), (238, 241, 244)), 540, 1440)
    footer(c, "@Geld-ohne-Filter")
    return c

# ======================= German 2: entspannt =======================
def de_entspannt():
    c = gradient_bg((20, 34, 58), (8, 14, 26), [(200, 600, 380, (108, 199, 154), 60), (950, 1350, 400, (242, 182, 50), 60)])
    y = 310
    y = place(c, fit("Ab welchem", lambda s: la("Black", s), 900, 120, fill=(238, 241, 244)), 540, y) - 6
    y = place(c, fit("GEHALT", lambda s: la("Black", s), 960, 220, fill=MUST), 540, y, sh=True) - 6
    y = place(c, fit("wird's entspannt?", lambda s: la("Black", s), 960, 110, fill=(238, 241, 244)), 540, y) + 50
    # rising salary bars; last one hidden
    bars = [("1.750 €", 170, (226, 104, 90)), ("2.650 €", 270, (90, 169, 226)), ("3.700 €", 380, (108, 199, 154)), ("?", 500, MUST)]
    bx = 110; bw = 165; base = y + 520
    for i, (lab, h, col) in enumerate(bars):
        x = bx + i * (bw + 40)
        bar = Image.new("RGBA", (bw, h), (0, 0, 0, 0))
        ImageDraw.Draw(bar).rounded_rectangle((0, 0, bw - 1, h + 30), 26, fill=col)
        c.alpha_composite(bar, (x, base - h))
        if lab == "?":
            q = qmark(170, NAVY); c.alpha_composite(q, (x + (bw - q.width) // 2, base - h + (h - q.height) // 2))
            t = tsprite("???? €", la("Black", 44), MUST)
        else:
            t = tsprite(lab, la("Black", 40), (238, 241, 244))
        c.alpha_composite(t, (x + (bw - t.width) // 2, base - h - t.height - 8))
    ImageDraw.Draw(c).rounded_rectangle((90, base, 990, base + 10), 5, fill=(60, 80, 110))
    n = netti(230, "think"); n, p = shadow(n)
    c.alpha_composite(n, (W - 230 - 40 - p, 1430 - p))
    place(c, tsprite("Die Zahl überrascht 👀", la("ExtraBold", 56), (238, 241, 244)) if False else tsprite("Die Zahl überrascht!", la("ExtraBold", 60), (238, 241, 244)), 430, 1500)
    footer(c, "@Geld-ohne-Filter")
    return c

# ======================= Persian common =======================
PNAVY = (11, 42, 87); RED = (226, 35, 26); GOLD = (255, 196, 61); WHITE = (255, 255, 255); SOFT = (200, 214, 236); CARD = (28, 78, 150)
def wd_logo(size):
    lg = Image.open(D + "/aof/wegweiser-deutschland-logo.png").convert("RGBA").resize((size, size), Image.LANCZOS)
    m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).ellipse((0, 0, size - 1, size - 1), fill=255); lg.putalpha(m); return lg

def brand_strip(c, y):
    lg = wd_logo(84); t = tsprite("WEGWEISER DEUTSCHLAND", la("Bold", 34, False), SOFT)
    w = lg.width + 20 + t.width; x = (W - w) // 2
    c.alpha_composite(lg, (x, y)); c.alpha_composite(t, (x + lg.width + 20, y + (84 - t.height) // 2))

# ======================= Persian 1: Jobcenter letter =======================
def letter(size_w):
    h = int(size_w * 0.68); S = 2
    im = Image.new("RGBA", (size_w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    w2, h2 = size_w * S, h * S
    d.rounded_rectangle((0, 0, w2 - 1, h2 - 1), 30 * S, fill=(246, 241, 228))
    d.polygon([(0, 0), (w2 // 2, h2 * 0.55), (w2, 0)], fill=(230, 222, 204))
    d.line([(0, 0), (w2 // 2, h2 * 0.55), (w2, 0)], fill=(200, 190, 170), width=6 * S)
    # red stamp
    st = tsprite("Jobcenter", la("Black", 46 * S), RED)
    sb = Image.new("RGBA", (st.width + 40 * S, st.height + 20 * S), (0, 0, 0, 0))
    ImageDraw.Draw(sb).rounded_rectangle((0, 0, sb.width - 1, sb.height - 1), 14 * S, outline=RED, width=7 * S)
    sb.alpha_composite(st, (20 * S, 10 * S)); sb = sb.rotate(-12, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(sb, (w2 - sb.width - 40 * S, h2 - sb.height - 30 * S))
    return im.resize((size_w, h), Image.LANCZOS)

def fa_jobcenter():
    c = gradient_bg((14, 52, 108), (6, 24, 52), [(540, 950, 420, (226, 35, 26), 70)])
    rays(c, 540, 1000, (255, 255, 255), a=10)
    brand_strip(c, 300)
    y = 440
    y = place(c, fit("نامه از جاب‌سنتر", lambda s: fa("Black", s), 960, 120, rtl=True, fill=WHITE), 540, y) - 10
    y = place(c, fit("اومده؟", lambda s: fa("Black", s), 960, 170, rtl=True, fill=GOLD), 540, y, sh=True) + 10
    lt = letter(640)
    place(c, lt, 540, y + 10, sh=True, rot=-6)
    # exclamation badge
    b = Image.new("RGBA", (170, 170), (0, 0, 0, 0)); ImageDraw.Draw(b).ellipse((0, 0, 169, 169), fill=RED)
    ex = tsprite("!", la("Black", 130), WHITE); b.alpha_composite(ex, ((170 - ex.width) // 2, (170 - ex.height) // 2))
    place(c, b, 840, y - 10, sh=True)
    footer(c, "@wegweiser.deutschland")
    place(c, box(fit("قبل از جواب دادن، اینو ببین!", lambda s: fa("Black", s), 900, 64, rtl=True, fill=PNAVY), WHITE, 40, 22, 30), 540, 1430, sh=True)
    return c

# ======================= Persian 2: Steuer =======================
def fa_steuer():
    c = gradient_bg((14, 52, 108), (6, 24, 52), [(540, 900, 460, (255, 196, 61), 70)])
    rays(c, 540, 880, (255, 196, 61), a=16)
    brand_strip(c, 300)
    y = 450
    y = place(c, fit("این پولِ توئه!", lambda s: fa("Black", s), 960, 110, rtl=True, fill=WHITE), 540, y) + 10
    big = fit("+1.000 €", lambda s: la("Black", s), 900, 250, fill=GOLD, stroke=0)
    y = place(c, big, 540, y, sh=True) + 10
    # coins
    for (x, yy, r) in [(540, 1150, 80), (400, 1215, 62), (690, 1210, 66), (230, 1120, 46), (860, 1110, 50)]:
        co = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0)); cd = ImageDraw.Draw(co)
        cd.ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=(222, 160, 30)); cd.ellipse((8, 8, 2 * r - 9, 2 * r - 9), fill=GOLD)
        e = tsprite("€", la("Black", int(r * 1.1)), (200, 140, 20)); co.alpha_composite(e, (r - e.width // 2, r - e.height // 2 - 3))
        place(c, co, x, yy, sh=True)
    de = box(tsprite("Steuererklärung", la("Black", 72), PNAVY), WHITE, 40, 18, 28)
    y = place(c, de, 540, y + 20, sh=True, rot=-2) + 50
    footer(c, "@wegweiser.deutschland")
    place(c, box(fit("هنوز پس نگرفتی؟", lambda s: fa("Black", s), 900, 76, rtl=True, fill=WHITE), RED, 44, 20, 34), 540, 1420, sh=True)
    return c

if __name__ == "__main__":
    jobs = {"YT-Mindestlohn": de_mindestlohn, "YT-Gehalt-entspannt": de_entspannt,
            "Reel-Jobcenter": fa_jobcenter, "Reel-Steuer": fa_steuer}
    for k, f in jobs.items():
        f().convert("RGB").save(OUT + f"cover-{k}.jpg", quality=92)
    print("ok")

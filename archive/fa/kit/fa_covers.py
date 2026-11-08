#!/usr/bin/env python3
"""Persian reel cover kit (v2 style). Add one function per reel, register it in JOBS, run: python3 fa_covers.py <name>
New designed covers (1080x1920) for the last 7 Persian reels of @wegweiser.deutschland.
Key content sits inside y=285..1635 so the 4:5 / 3:4 profile-grid crop still reads."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = os.path.dirname(os.path.abspath(__file__))
VZ = S + "/fonts/Vazirmatn-"
INTER = os.path.normpath(S + "/../../../gof/kit/fonts") + "/"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
OUT = os.environ.get("COVER_OUT", os.path.normpath(S + "/../v2")) + "/"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920

NAVY = (10, 40, 86); NAVY_D = (5, 18, 42); RED = (226, 35, 26); GOLD = (255, 196, 61)
WHITE = (255, 255, 255); SOFT = (196, 212, 236); GREEN = (46, 204, 135); INK = (12, 30, 62)
BLUE = (64, 140, 255); BURG = (122, 24, 42)

def fa(w, s): return ImageFont.truetype(VZ + w + ".ttf", s, layout_engine=ImageFont.Layout.RAQM)
def la(w, s): return ImageFont.truetype(INTER + "InterDisplay-" + w + ".otf", s, layout_engine=ImageFont.Layout.RAQM)
def la_t(w, s): return ImageFont.truetype(INTER + "Inter-" + w + ".otf", s, layout_engine=ImageFont.Layout.RAQM)

def T(text, font, fill, rtl=False, pad=10, stroke=0, sfill=None):
    kw = dict(direction="rtl", language="fa") if rtl else {}
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    b = d.textbbox((0, 0), text, font=font, stroke_width=stroke, **kw)
    im = Image.new("RGBA", (b[2] - b[0] + 2 * pad, b[3] - b[1] + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - b[0], pad - b[1]), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=sfill, **kw)
    return im

def F(text, weight, maxw, start, fill, rtl=True, latin=False, **kw):
    s = start
    while True:
        f = la(weight, s) if latin else fa(weight, s)
        sp = T(text, f, fill, rtl=rtl and not latin, **kw)
        if sp.width <= maxw or s < 30: return sp
        s -= 3

def emoji(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    r = size / max(im.size)
    return im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)

def shadow(im, r=28, off=(0, 20), a=150):
    pad = r * 2
    out = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    blk = Image.new("RGBA", im.size, (0, 0, 0, 255)); blk.putalpha(im.getchannel("A").point(lambda v: v * a // 255))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0)); sh.paste(blk, (pad + off[0], pad + off[1]), blk)
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(r))); out.alpha_composite(im, (pad, pad))
    return out, pad

def place(c, sp, cx, y, sh=False, rot=0, anchor="top"):
    if rot: sp = sp.rotate(rot, resample=Image.BICUBIC, expand=True)
    pad = 0
    if sh: sp, pad = shadow(sp)
    yy = y - pad if anchor == "top" else y - sp.height // 2
    c.alpha_composite(sp, (int(cx - sp.width / 2), int(yy)))
    return int(yy + sp.height - pad)

def pill(sp, bg, px=36, py=16, r=None, outline=None, ow=0):
    b = Image.new("RGBA", (sp.width + 2 * px, sp.height + 2 * py), (0, 0, 0, 0))
    r = r if r is not None else b.height // 2
    ImageDraw.Draw(b).rounded_rectangle((0, 0, b.width - 1, b.height - 1), r, fill=bg, outline=outline, width=ow)
    b.alpha_composite(sp, (px, py)); return b

def hstack(items, gap=16):
    w = sum(i.width for i in items) + gap * (len(items) - 1); h = max(i.height for i in items)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); x = 0
    for i in items: im.alpha_composite(i, (x, (h - i.height) // 2)); x += i.width + gap
    return im

# ---------------- background ----------------
def background(glows):
    bg = Image.new("RGB", (W, H)); d = ImageDraw.Draw(bg)
    for y in range(H):
        k = y / H; d.line((0, y, W, y), fill=tuple(int(NAVY[i] + (NAVY_D[i] - NAVY[i]) * k) for i in range(3)))
    bg = bg.convert("RGBA")
    for (x, y, r, col, a) in glows:
        g = Image.new("RGBA", (4 * r, 4 * r), col + (0,))
        ImageDraw.Draw(g).ellipse((r, r, 3 * r, 3 * r), fill=col + (a,))
        bg.alpha_composite(g.filter(ImageFilter.GaussianBlur(r // 2)), (x - 2 * r, y - 2 * r))
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(dots)
    for yy in range(30, H, 54):
        for xx in range(27, W, 54): dd.ellipse((xx - 2, yy - 2, xx + 2, yy + 2), fill=(255, 255, 255, 16))
    bg.alpha_composite(dots)
    return bg

def logo(size):
    s = size * 4; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, s - 1, s - 1), fill=WHITE)
    m = s * 0.035; d.ellipse((m, m, s - m, s - m), fill=(18, 52, 104))
    m2 = s * 0.25; d.ellipse((m2, m2, s - m2, s - m2), outline=(255, 255, 255, 120), width=int(s * 0.01))
    c = s / 2; L = s * 0.2; w = s * 0.055
    d.polygon([(c, c - L), (c + w, c), (c, c + L), (c - w, c)], fill=WHITE)
    d.polygon([(c - L, c), (c, c - w), (c + L, c), (c, c + w)], fill=WHITE)
    d.polygon([(c, c - L), (c + w, c), (c - w, c)], fill=RED)
    f = la_t("Bold", int(s * 0.085))
    def ring(text, start, end, r, top=True):
        n = len(text)
        for i, ch in enumerate(text):
            a = math.radians(start + (end - start) * (i + 0.5) / n)
            g = T(ch, f, WHITE, pad=2)
            rot = -math.degrees(a) - 90 if top else -math.degrees(a) + 90
            g = g.rotate(rot, resample=Image.BICUBIC, expand=True)
            x = c + r * math.cos(a); y = c + r * math.sin(a)
            im.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    ring("WEGWEISER", 215, 325, s * 0.37, True)
    ring("DEUTSCHLAND"[::-1], 30, 150, s * 0.37, False)
    return im.resize((size, size), Image.LANCZOS)

def frame(c, tag, tag_col=RED):
    lg = logo(96); c.alpha_composite(lg, (84, 112))
    c.alpha_composite(T("WEGWEISER", la("Black", 40), WHITE, pad=0), (204, 122))
    c.alpha_composite(T("DEUTSCHLAND", la("Medium", 31), SOFT, pad=0), (204, 172))
    tg = pill(T(tag, fa("Bold", 36), WHITE, rtl=True, pad=4), tag_col, 34, 14)
    c.alpha_composite(tg, (W - 84 - tg.width, 160 - tg.height // 2))
    # footer
    h = T("@wegweiser.deutschland", la("Bold", 38), SOFT)
    save = pill(hstack([T("سیو کن", fa("Bold", 36), INK, rtl=True, pad=4), emoji("📌", 40)], 10), GOLD, 28, 12)
    row = hstack([save, h], 30)
    c.alpha_composite(row, ((W - row.width) // 2, 1700))

# ---------------- illustrations ----------------
def passport(w, title="REISEPASS"):
    h = int(w * 1.38); k = 3; s = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    W2, H2 = w * k, h * k
    d.rounded_rectangle((0, 0, W2 - 1, H2 - 1), 34 * k, fill=BURG)
    d.rounded_rectangle((0, 0, 34 * k, H2 - 1), 20 * k, fill=(100, 18, 34))
    gold = (226, 182, 92)
    f1 = la_t("Bold", int(W2 * 0.06)); f2 = la_t("Bold", int(W2 * 0.095))
    for txt, f, y in [("BUNDESREPUBLIK", f1, 0.12), ("DEUTSCHLAND", f1, 0.18)]:
        t = T(txt, f, gold, pad=0); s.alpha_composite(t, ((W2 - t.width) // 2 + 10 * k, int(H2 * y)))
    # eagle-ish emblem
    cx, cy, r = W2 // 2 + 10 * k, int(H2 * 0.48), int(W2 * 0.2)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=gold, width=6 * k)
    d.polygon([(cx, cy - r * 0.55), (cx + r * 0.55, cy - r * 0.15), (cx + r * 0.3, cy + r * 0.55), (cx, cy + r * 0.3),
               (cx - r * 0.3, cy + r * 0.55), (cx - r * 0.55, cy - r * 0.15)], fill=gold)
    t = T(title, f2, gold, pad=0); s.alpha_composite(t, ((W2 - t.width) // 2 + 10 * k, int(H2 * 0.75)))
    # biometric chip mark
    cw = int(W2 * 0.1); x0 = (W2 - cw) // 2 + 10 * k; y0 = int(H2 * 0.88)
    d.rounded_rectangle((x0, y0, x0 + cw, y0 + int(cw * 0.6)), 6 * k, outline=gold, width=4 * k)
    d.ellipse((x0 + cw * 0.38, y0 + cw * 0.18, x0 + cw * 0.62, y0 + cw * 0.42), outline=gold, width=3 * k)
    return s.resize((w, h), Image.LANCZOS)

def rcard(w, para="25 Abs. 2", remark=None, highlight=GOLD):
    """German electronic residence permit (stylised)."""
    h = int(w * 0.63); k = 2; s = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    W2, H2 = w * k, h * k
    for y in range(H2):
        t = y / H2; d.line((0, y, W2, y), fill=(int(226 + 12 * t), int(236 - 6 * t), int(232 - 18 * t)))
    m = Image.new("L", (W2, H2), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, W2 - 1, H2 - 1), 36 * k, fill=255); s.putalpha(m)
    d = ImageDraw.Draw(s)
    # flag stripe
    for i, col in enumerate([(20, 20, 20), (210, 30, 30), (240, 190, 40)]):
        d.rectangle((0, int(H2 * 0.03) + i * 8 * k, W2, int(H2 * 0.03) + (i + 1) * 8 * k), fill=col)
    t = T("AUFENTHALTSTITEL", la_t("Bold", int(H2 * 0.07)), (40, 60, 90), pad=0); s.alpha_composite(t, (int(W2 * 0.06), int(H2 * 0.13)))
    t = T("D", la_t("Bold", int(H2 * 0.09)), (40, 60, 90), pad=0); s.alpha_composite(t, (W2 - t.width - int(W2 * 0.06), int(H2 * 0.12)))
    # photo
    px, py, pw, ph = int(W2 * 0.06), int(H2 * 0.29), int(W2 * 0.24), int(H2 * 0.5)
    d.rounded_rectangle((px, py, px + pw, py + ph), 14 * k, fill=(176, 192, 206))
    d.ellipse((px + pw * 0.3, py + ph * 0.18, px + pw * 0.7, py + ph * 0.52), fill=(120, 138, 158))
    d.pieslice((px + pw * 0.12, py + ph * 0.58, px + pw * 0.88, py + ph * 1.3), 180, 360, fill=(120, 138, 158))
    # chip
    cx0, cy0 = int(W2 * 0.36), int(H2 * 0.31)
    d.rounded_rectangle((cx0, cy0, cx0 + int(W2 * 0.1), cy0 + int(H2 * 0.13)), 8 * k, fill=(214, 176, 90))
    # field lines
    for i in range(3):
        y = int(H2 * (0.52 + i * 0.09)); d.rounded_rectangle((cx0, y, cx0 + int(W2 * (0.42 - i * 0.08)), y + 9 * k), 5 * k, fill=(170, 186, 200))
    # big paragraph highlight
    sp = T(para, la("Black", int(H2 * 0.16)), INK, pad=0)
    hb = pill(sp, highlight, 22 * k, 10 * k, r=18 * k)
    s.alpha_composite(hb, (W2 - hb.width - int(W2 * 0.05), int(H2 * 0.72) - hb.height // 2 + 10 * k))
    if remark:
        rt = T(remark, ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", int(H2 * 0.065)), (40, 60, 90), pad=0)
        s.alpha_composite(rt, (cx0, int(H2 * 0.87)))
    return s.resize((w, h), Image.LANCZOS)

def coin(r, sym="€"):
    k = 3; R = r * k; co = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0)); cd = ImageDraw.Draw(co)
    cd.ellipse((0, 0, 2 * R - 1, 2 * R - 1), fill=(214, 150, 24)); cd.ellipse((7 * k, 7 * k, 2 * R - 7 * k, 2 * R - 7 * k), fill=GOLD)
    cd.ellipse((14 * k, 14 * k, 2 * R - 14 * k, 2 * R - 14 * k), outline=(236, 172, 40), width=3 * k)
    e = T(sym, la("Black", int(R * 1.05)), (196, 132, 16), pad=0); co.alpha_composite(e, (R - e.width // 2, R - e.height // 2 - 2 * k))
    return co.resize((2 * r, 2 * r), Image.LANCZOS)

def circle_badge(d_, col, inner, ring=None):
    b = Image.new("RGBA", (d_, d_), (0, 0, 0, 0)); bd = ImageDraw.Draw(b)
    bd.ellipse((0, 0, d_ - 1, d_ - 1), fill=col, outline=ring, width=8 if ring else 0)
    b.alpha_composite(inner, ((d_ - inner.width) // 2, (d_ - inner.height) // 2)); return b

def arrow_down(w, h, col):
    a = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(a)
    d.rectangle((w * 0.38, 0, w * 0.62, h * 0.55), fill=col); d.polygon([(0, h * 0.5), (w, h * 0.5), (w / 2, h)], fill=col)
    return a

# ======================= 1. § 22 / § 23 =======================
def c_22_23():
    c = background([(250, 760, 340, BLUE, 70), (830, 760, 340, GOLD, 60), (540, 1350, 380, RED, 45)])
    frame(c, "اقامت ۲۲ و ۲۳")
    y = 400
    y = place(c, F("روی کارتت کدوم نوشته؟", "Black", 940, 92, WHITE), 540, y) + 40
    L = pill(T("§ 22", la("Black", 150), INK, pad=0), WHITE, 40, 26, r=40)
    R_ = pill(T("§ 23", la("Black", 150), INK, pad=0), GOLD, 40, 26, r=40)
    vs = circle_badge(150, RED, T("VS", la("Black", 66), WHITE, pad=0), ring=WHITE)
    yy = y + 20
    place(c, L, 270, yy, sh=True, rot=4); place(c, R_, 810, yy, sh=True, rot=-4)
    place(c, vs, 540, yy + L.height // 2 - 20, sh=True, anchor="mid")
    y = yy + L.height + 70
    pp = passport(330)
    place(c, pp, 540, y + 10, sh=True, rot=-8)
    q = circle_badge(130, GOLD, T("?", la("Black", 110), INK, pad=0))
    place(c, q, 720, y - 10, sh=True)
    y = y + pp.height + 60
    y = place(c, F("یکی‌شون مستقیم پاسپورت میده!", "Black", 960, 76, GOLD), 540, y, sh=True) + 18
    place(c, pill(F("فرق مهم برای افغان‌ها", "Bold", 700, 48, INK, pad=4), GREEN, 34, 14), 540, y, sh=True)
    return c

# ======================= 2. 5 Hilfen Jobcenter =======================
def c_5_komak():
    c = background([(540, 820, 440, GOLD, 70), (900, 1400, 300, RED, 50)])
    frame(c, "۵ کمک مالی جاب‌سنتر")
    y = 420
    big = T("۵", fa("Black", 520), GOLD, rtl=True, pad=0)
    big, p = shadow(big, r=40, a=170)
    for (x, yy, r) in [(230, 700, 86), (850, 650, 76), (110, 880, 50), (970, 900, 54), (320, 500, 44), (770, 470, 40)]:
        place(c, coin(r), x, yy + 70, sh=True)
    c.alpha_composite(big, (540 - big.width // 2, y - 60 - p))
    y = y + 520
    y = place(c, F("کمک مالی", "Black", 900, 150, WHITE), 540, y - 20) - 10
    y = place(c, F("که جاب‌سنتر بهت میده", "ExtraBold", 900, 76, SOFT), 540, y) + 30
    y = place(c, pill(F("ولی هیچ‌کس بهت نمیگه!", "Black", 820, 68, WHITE, pad=4), RED, 44, 20), 540, y, sh=True, rot=-2) + 40
    place(c, F("شماره‌ی ۱ حتی بدون جاب‌سنتر هم هست", "Bold", 920, 50, GOLD), 540, y)
    return c

# ======================= 3. Besuchsvisum =======================
def c_besuch():
    c = background([(820, 700, 360, BLUE, 80), (260, 1200, 360, GOLD, 55)])
    frame(c, "ویزای دیدار")
    y = 360
    y = place(c, F("پدر و مادرت", "Black", 900, 130, WHITE), 540, y) - 10
    y = place(c, F("بیان آلمان؟", "Black", 900, 150, GOLD), 540, y, sh=True) + 20
    # illustration: passport + visa stamp + plane + parents
    pp = passport(280, "PASS")
    place(c, pp, 330, y + 30, sh=True, rot=10)
    stamp = Image.new("RGBA", (300, 170), (0, 0, 0, 0)); sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle((0, 0, 299, 169), 22, outline=GREEN, width=10)
    t1 = T("SCHENGEN", la("Black", 50), GREEN, pad=0); t2 = T("VISUM ✓", la("Black", 46), GREEN, pad=0)
    stamp.alpha_composite(t1, ((300 - t1.width) // 2, 28)); stamp.alpha_composite(t2, ((300 - t2.width) // 2, 94))
    place(c, stamp, 720, y + 290, sh=True, rot=-12)
    pl = emoji("✈️", 150); place(c, pl, 880, y + 10, sh=True)
    fam = hstack([emoji("👵", 130), emoji("👴", 130)], 8); place(c, fam, 680, y + 70, sh=True)
    y = y + int(280 * 1.38) + 150
    y = place(c, pill(T("Schengen-Visum", la("Black", 70), INK, pad=0), WHITE, 40, 16), 540, y, sh=True) + 36
    place(c, F("این اشتباه رو نکن!", "Black", 900, 96, GOLD, stroke=0), 540, y, sh=True)
    return c

# ======================= 4. Beschäftigungsduldung =======================
def c_beschaeft():
    c = background([(540, 1000, 460, GREEN, 50), (900, 420, 300, GOLD, 50)])
    frame(c, "Beschäftigungsduldung")
    y = 340
    y = place(c, F("Duldung داری و کار می‌کنی؟", "Black", 960, 84, WHITE), 540, y) + 20
    y = place(c, pill(T("Beschäftigungsduldung", la("Black", 64), INK, pad=0), GOLD, 36, 16), 540, y, sh=True, rot=-2) + 50
    steps = [("Duldung", "کار", SOFT, INK), ("۳۰ ماه", "", WHITE, INK), ("§ 25b", "اقامت", GREEN, INK), ("دائم", "اقامت", BLUE, WHITE), ("پاسپورت", "", GOLD, INK)]
    # vertical timeline
    x_line = 260
    ys = []
    for i, (main, sub, col, tc) in enumerate(steps):
        yy = y + i * 184; ys.append(yy)
    ImageDraw.Draw(c).rounded_rectangle((x_line - 6, ys[0] + 60, x_line + 6, ys[-1] + 60), 6, fill=(255, 255, 255, 90))
    icons = ["💼", "⏳", "🪪", "🏠", "🇩🇪"]
    for i, (main, sub, col, tc) in enumerate(steps):
        yy = ys[i]
        node = circle_badge(120, col, emoji(icons[i], 66), ring=NAVY_D)
        place(c, node, x_line, yy, sh=True)
        lab_txt = main if not sub else (sub + " " + main if sub == "اقامت" else main)
        lat = main.startswith("Duldung") or main.startswith("§")
        if lat and sub:
            parts = [T(main, la("Black", 64), WHITE, pad=2)] + ([T("+", la("Black", 60), SOFT, pad=2)] if sub == "کار" else []) + [T(sub, fa("Black", 60), SOFT, rtl=True, pad=2)]
            lab = hstack(parts, 14)
        elif lat:
            lab = T(main, la("Black", 64), WHITE, pad=2)
        else:
            lab = T(lab_txt, fa("Black", 66), WHITE if i < 4 else GOLD, rtl=True, pad=2)
        c.alpha_composite(lab, (x_line + 100, yy + 60 - lab.height // 2))
    y = ys[-1] + 160
    place(c, pill(F("همه‌ی شرط‌ها اینجاست", "Bold", 700, 48, INK, pad=4), GREEN, 34, 14), 540, y, sh=True)
    return c

# ======================= 5. Karte 25.2 =======================
def c_karte():
    c = background([(540, 900, 460, BLUE, 70), (200, 1400, 300, GOLD, 45)])
    frame(c, "روی کارتت چی نوشته؟")
    y = 300
    y = place(c, F("روی کارتت فقط نوشته", "Black", 940, 92, WHITE), 540, y) + 30
    card = rcard(860, "25 Abs. 2")
    y = place(c, card, 540, y, sh=True, rot=-3) + 50
    q = circle_badge(130, RED, T("?", la("Black", 110), WHITE, pad=0), ring=WHITE)
    a = pill(T("Flüchtling", la("Black", 68), INK, pad=0), WHITE, 34, 16)
    b = pill(T("subsidiär", la("Black", 68), INK, pad=0), GOLD, 34, 16)
    place(c, a, 250, y + 20, sh=True, rot=3); place(c, b, 830, y + 20, sh=True, rot=-3)
    place(c, T("یا", fa("Black", 64), WHITE, rtl=True), 540, y + 20 + a.height // 2, anchor="mid")
    y = y + a.height + 90
    y = place(c, F("کدومشی؟", "Black", 900, 130, GOLD), 540, y, sh=True) + 10
    place(c, pill(F("جواب سوال همه‌تون اینجاست", "Bold", 760, 46, INK, pad=4), GREEN, 34, 14), 540, y, sh=True)
    return c

# ======================= 6. 25.2 subsidiär =======================
def c_25_2():
    c = background([(820, 760, 380, GOLD, 60), (240, 1200, 360, GREEN, 45)])
    frame(c, "اقامت 25.2")
    y = 300
    y = place(c, F("حمایت تکمیلی داری؟", "Black", 940, 104, WHITE), 540, y) + 30
    card = rcard(840, "25 Abs. 2", remark="(4 AsylG)")
    y = place(c, card, 540, y, sh=True, rot=3) + 60
    # two goal tiles
    def tile(icon, txt, col):
        t = Image.new("RGBA", (400, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
        d.rounded_rectangle((0, 0, 399, 299), 40, fill=(255, 255, 255, 26), outline=col, width=5)
        ic = emoji(icon, 110); t.alpha_composite(ic, ((400 - ic.width) // 2, 34))
        tx = F(txt, "Black", 360, 56, WHITE); t.alpha_composite(tx, ((400 - tx.width) // 2, 170)); return t
    place(c, tile("🏠", "اقامت دائم", GREEN), 310, y, sh=True)
    place(c, tile("🇩🇪", "پاسپورت", GOLD), 770, y, sh=True)
    place(c, circle_badge(120, RED, T("?", la("Black", 100), WHITE, pad=0), ring=WHITE), 540, y + 150, sh=True, anchor="mid")
    y += 330
    place(c, F("حالا ۳ ساله!", "Black", 900, 100, GOLD), 540, y, sh=True)
    return c

# ======================= 7. 25.5 / 25a / 25b =======================
def c_25_5ab():
    c = background([(540, 1050, 480, GREEN, 50), (860, 420, 300, RED, 50)])
    frame(c, "اقامت بدون پناهندگی")
    y = 300
    # rejected stamp
    st = T("ABGELEHNT", la("Black", 70), RED, pad=0)
    sb = pill(st, (0, 0, 0, 0), 30, 12, r=18, outline=RED, ow=9)
    y = place(c, F("پناهندگیت رد شده؟", "Black", 940, 108, WHITE), 540, y + 20) + 6
    y = place(c, sb, 540, y, rot=-5) + 6
    y = place(c, F("ولی هنوز ۳ راه هست!", "Black", 960, 130, GOLD), 540, y, sh=True) + 60
    cols = [(WHITE, "§ 25.5", "🚪"), (GOLD, "§ 25a", "🎓"), (GREEN, "§ 25b", "🤝")]
    subs = ["خروج غیرممکن", "جوان‌ها", "ادغام موفق"]
    for i, (col, para, ic) in enumerate(cols):
        x = 200 + i * 340
        t = Image.new("RGBA", (300, 470), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
        d.rounded_rectangle((0, 0, 299, 469), 46, fill=col)
        n = circle_badge(84, INK, T(str(i + 1), la("Black", 54), col, pad=0)); t.alpha_composite(n, (108, 28))
        e = emoji(ic, 120); t.alpha_composite(e, ((300 - e.width) // 2, 138))
        p = F(para, "Black", 260, 74, INK, latin=True); t.alpha_composite(p, ((300 - p.width) // 2, 290))
        s_ = F(subs[i], "Bold", 260, 40, (40, 60, 90)); t.alpha_composite(s_, ((300 - s_.width) // 2, 385))
        place(c, t, x, y + (0 if i == 1 else 30), sh=True, rot=(4 if i == 0 else -4 if i == 2 else 0))
    y += 560
    place(c, pill(F("ببین کدوم مال توئه", "Bold", 700, 50, INK, pad=4), WHITE, 36, 14), 540, y, sh=True)
    return c

JOBS = {
    "Wegweiser-22-23": c_22_23,
    "Wegweiser-5-Komak": c_5_komak,
    "Wegweiser-Besuchsvisum": c_besuch,
    "Wegweiser-Beschaeftigungsduldung": c_beschaeft,
    "Wegweiser-Karte": c_karte,
    "Wegweiser-25-2": c_25_2,
    "Wegweiser-Aufenthalt-25-5-a-b": c_25_5ab,
}

if __name__ == "__main__":
    only = sys.argv[1:]
    for k, f in JOBS.items():
        if only and k not in only: continue
        f().convert("RGB").save(OUT + f"cover-{k}.jpg", quality=93)
        print("ok", k)

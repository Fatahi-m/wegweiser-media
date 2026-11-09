#!/usr/bin/env python3
"""Kurdish (Sorani) reel cover kit (v2 style) for @wegweiser_kurdi.
Cream brand frame (sun, Kurdish-flag waves), big headline, per-topic illustration.
Key content sits inside y=285..1635 so the profile-grid crop still reads.
Add one function per reel, register it in JOBS as <file name without -Reel.mp4>, run: python3 ku_covers.py <name>
Output: archive/ku/v2/cover-<name>.jpg"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(S + "/../../fa/kit"))
os.environ.setdefault("COVER_OUT", os.path.normpath(S + "/../v2"))
import fa_covers as k
from fa_covers import fa, la, T, emoji, pill, hstack, passport, rcard, coin, circle_badge

OUT = os.path.normpath(S + "/../v2") + "/"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
CREAM = (247, 242, 232); INK = (22, 34, 30); GREEN = (16, 94, 62); RED = (204, 32, 40)
GOLD = (243, 170, 18); SUN = (250, 226, 180); MUTED = (92, 104, 98); WHITE = (255, 255, 255)

def F(text, weight, maxw, start, fill, latin=False, **kw):
    s = start
    while True:
        f = la(weight, s) if latin else fa(weight, s)
        sp = T(text, f, fill, rtl=not latin, **kw)
        if sp.width <= maxw or s < 30: return sp
        s -= 3

def shadow(im, r=26, off=(0, 16), a=70):
    pad = r * 2
    out = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    blk = Image.new("RGBA", im.size, (40, 50, 40, 255)); blk.putalpha(im.getchannel("A").point(lambda v: v * a // 255))
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

def sun(size, col=GOLD, rays=16):
    s = size * 3; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    import math
    c = s / 2
    for i in range(rays):
        a = 2 * math.pi * i / rays; a1 = a - 0.07; a2 = a + 0.07
        d.polygon([(c + s * 0.27 * math.cos(a1), c + s * 0.27 * math.sin(a1)), (c + s * 0.49 * math.cos(a), c + s * 0.49 * math.sin(a)),
                   (c + s * 0.27 * math.cos(a2), c + s * 0.27 * math.sin(a2))], fill=col)
    d.ellipse((c - s * 0.25, c - s * 0.25, c + s * 0.25, c + s * 0.25), fill=col)
    return im.resize((size, size), Image.LANCZOS)

def background():
    c = Image.new("RGBA", (W, H), CREAM + (255,)); d = ImageDraw.Draw(c)
    for y in range(48, H, 48): d.line((0, y, W, y), fill=(232, 226, 212), width=2)
    big = sun(760, SUN + (255,), 18); c.alpha_composite(big, (W - 430, -330))
    # Kurdish-flag waves
    import math
    red = [(x, 1752 + 26 * math.sin(x / 170)) for x in range(0, W + 10, 10)]
    d.polygon(red + [(W, H), (0, H)], fill=RED)
    grn = [(x, 1800 + 30 * math.sin(x / 210 + 1.6)) for x in range(0, W + 10, 10)]
    d.polygon(grn + [(W, H), (0, H)], fill=GREEN)
    return c

def logo(size):
    s = size * 3; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, s - 1, s - 1), fill=GREEN); d.ellipse((s * .06, s * .06, s * .94, s * .94), fill=RED)
    d.ellipse((s * .11, s * .11, s * .89, s * .89), fill=(252, 248, 238))
    sn = sun(int(s * .62)); im.alpha_composite(sn, ((s - sn.width) // 2, (s - sn.height) // 2))
    c = s / 2; L = s * .3; w = s * .06
    d.polygon([(c + L * .7, c - L * .7), (c + w, c + w), (c - w, c - w)], fill=RED)
    d.polygon([(c - L * .7, c + L * .7), (c + w, c + w), (c - w, c - w)], fill=INK)
    return im.resize((size, size), Image.LANCZOS)

def frame(c, tag):
    hd = hstack([logo(70), T("@wegweiser_kurdi", la("Bold", 38), INK, pad=2)], 16)
    hp = pill(hd, (252, 250, 244), 16, 12, outline=(206, 226, 214), ow=3)
    c.alpha_composite(hp, (70, 150 - hp.height // 2))
    tg = pill(F(tag, "Black", 380, 40, WHITE, pad=4) if any("؀" <= ch <= "ۿ" for ch in tag)
              else T(tag, la("Black", 40), WHITE, pad=4), GREEN, 34, 14)
    c.alpha_composite(tg, (W - 70 - tg.width, 150 - tg.height // 2))
    save = pill(hstack([F("سەیڤی بکە", "Black", 400, 44, INK, pad=4), emoji("📌", 44)], 12), GOLD, 34, 14)
    place(c, save, 540, 1650, sh=True)

def de_card(main, sub, w=None, col=GREEN, fsize=78):
    m = T(main, la("Black", fsize), WHITE, pad=4)
    s_ = F(sub, "Bold", 760, 44, GOLD, pad=4) if sub else None
    ww = w or max(m.width, s_.width if s_ else 0) + 100
    hh = m.height + (s_.height + 6 if s_ else 0) + 60
    b = Image.new("RGBA", (ww, hh + 26), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle((0, 26, ww - 1, hh + 25), 34, fill=col)
    d.rounded_rectangle((ww - 22, 50, ww - 10, hh), 6, fill=RED)
    b.alpha_composite(m, ((ww - m.width) // 2, 26 + 28))
    if s_: b.alpha_composite(s_, ((ww - s_.width) // 2, 26 + 28 + m.height + 2))
    de = pill(T("DE", la("Black", 30), INK, pad=2), GOLD, 22, 6); b.alpha_composite(de, (40, 0))
    return b

def tile(icon, txt, col, w=400, h=300):
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 40, fill=WHITE, outline=col, width=7)
    ic = emoji(icon, 110); t.alpha_composite(ic, ((w - ic.width) // 2, 36))
    tx = F(txt, "Black", w - 40, 54, INK); t.alpha_composite(tx, ((w - tx.width) // 2, 176)); return t

# ======================= Widerruf =======================
def letter(w):
    h = int(w * 0.72); s = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=WHITE, outline=(214, 208, 196), width=4)
    d.polygon([(6, 8), (w / 2, h * 0.52), (w - 6, 8)], fill=(240, 236, 226), outline=(214, 208, 196))
    t = T("BAMF", la("Black", int(w * 0.16)), INK, pad=0); s.alpha_composite(t, (int(w * 0.08), int(h * 0.64)))
    for i in range(2):
        y = int(h * (0.68 + i * 0.1)); d.rounded_rectangle((int(w * 0.55), y, int(w * (0.9 - i * 0.1)), y + 12), 6, fill=(204, 210, 206))
    return s

def c_widerruf():
    c = background(); frame(c, "Widerruf")
    y = 300
    y = place(c, F("نامەی BAMF ت بۆ هاتووە؟", "Black", 960, 96, INK), 540, y) + 30
    lt = letter(620)
    place(c, lt, 500, y, sh=True, rot=-5)
    st = pill(T("WIDERRUF", la("Black", 74), RED, pad=0), (0, 0, 0, 0), 30, 12, r=18, outline=RED, ow=10)
    place(c, st, 620, y + 390, sh=True, rot=10)
    place(c, emoji("✉️", 120), 890, y - 10, sh=True)
    y += 580
    y = place(c, pill(F("مەترسە!", "Black", 600, 92, WHITE, pad=4), GREEN, 52, 18), 540, y, sh=True, rot=-2) + 34
    y = place(c, F("بەڵام ماوەکان زۆر کورتن!", "Black", 960, 84, RED), 540, y) + 30
    a = de_card("Anhörung", "وەڵام بدەرەوە", fsize=60)
    b = de_card("Klage", "٢ هەفتە", fsize=60)
    arr = T("←", la("Black", 70), MUTED, pad=0)
    place(c, hstack([b, arr, a], 22), 540, y, sh=True)
    return c

# ======================= 3 AsylG vs 4 AsylG =======================
def c_asylg_3_4():
    c = background(); frame(c, "کارتی ئیقامە")
    y = 310
    y = place(c, F("لەسەر کارتەکەت", "Black", 900, 104, INK), 540, y) - 6
    y = place(c, F("چی نووسراوە؟", "Black", 900, 128, GREEN), 540, y) + 50
    def card(para, label, sub, col, tc):
        t = Image.new("RGBA", (440, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
        d.rounded_rectangle((0, 0, 439, 559), 46, fill=col)
        r = T("REMARKS", la("Bold", 30), tc, pad=0); t.alpha_composite(r, ((440 - r.width) // 2, 40))
        p = T(para, la("Black", 104), tc, pad=0); t.alpha_composite(p, ((440 - p.width) // 2, 100))
        a = T("AsylG", la("Black", 70), tc, pad=0); t.alpha_composite(a, ((440 - a.width) // 2, 230))
        d.line((60, 340, 380, 340), fill=tc + (90,), width=4)
        l = F(label, "Black", 380, 64, tc, latin=True); t.alpha_composite(l, ((440 - l.width) // 2, 370))
        s_ = F(sub, "Bold", 380, 46, tc); t.alpha_composite(s_, ((440 - s_.width) // 2, 460))
        return t
    R_ = card("§ 3", "Flüchtling", "پەنابەر", GREEN, WHITE)
    L = card("§ 4", "subsidiär", "پاراستنی سنووردار", GOLD, INK)
    place(c, R_, 790, y, sh=True, rot=-4); place(c, L, 290, y, sh=True, rot=4)
    place(c, circle_badge(150, RED, T("VS", la("Black", 66), WHITE, pad=0), ring=WHITE), 540, y + 290, sh=True, anchor="mid")
    y += 640
    y = place(c, F("جیاوازییان زۆرە!", "Black", 960, 120, RED), 540, y) + 20
    place(c, pill(F("ئیقامەی هەمیشەیی و هێنانی خێزان", "Bold", 860, 46, WHITE, pad=4), GREEN, 34, 14), 540, y, sh=True)
    return c

# ======================= 25.2 subsidiär =======================
def c_25_2():
    c = background(); frame(c, "ئیقامەی 25.2")
    y = 300
    y = place(c, F("پاراستنی سنووردارت هەیە؟", "Black", 960, 92, INK), 540, y) + 34
    card = rcard(840, "25 Abs. 2", remark="(4 AsylG)")
    y = place(c, card, 540, y, sh=True, rot=3) + 60
    place(c, tile("🏠", "ئیقامەی هەمیشەیی", GREEN), 770, y, sh=True)
    place(c, tile("🇩🇪", "پاسپۆرت", GOLD), 310, y, sh=True)
    place(c, circle_badge(120, RED, T("?", la("Black", 100), WHITE, pad=0), ring=WHITE), 540, y + 150, sh=True, anchor="mid")
    y += 350
    place(c, F("کەی وەریدەگریت؟", "Black", 900, 110, RED), 540, y)
    return c

# ======================= Besuchsvisum =======================
def c_besuch():
    c = background(); frame(c, "ڤیزای سەردان")
    y = 300
    y = place(c, F("دایک و باوکت", "Black", 900, 130, INK), 540, y) - 10
    y = place(c, F("بێنە ئەڵمانیا؟", "Black", 900, 140, GREEN), 540, y) + 20
    pp = passport(280, "PASS")
    place(c, pp, 330, y + 30, sh=True, rot=10)
    stamp = Image.new("RGBA", (300, 170), (0, 0, 0, 0)); sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle((0, 0, 299, 169), 22, fill=(247, 242, 232, 230), outline=GREEN, width=10)
    t1 = T("SCHENGEN", la("Black", 50), GREEN, pad=0); t2 = T("VISUM ✓", la("Black", 46), GREEN, pad=0)
    stamp.alpha_composite(t1, ((300 - t1.width) // 2, 28)); stamp.alpha_composite(t2, ((300 - t2.width) // 2, 94))
    place(c, stamp, 730, y + 290, sh=True, rot=-12)
    place(c, emoji("✈️", 150), 890, y + 10, sh=True)
    place(c, hstack([emoji("👵", 130), emoji("👴", 130)], 8), 680, y + 70, sh=True)
    y = y + int(280 * 1.38) + 140
    y = place(c, pill(T("Schengen-Visum", la("Black", 70), WHITE, pad=0), INK, 40, 16), 540, y, sh=True) + 30
    place(c, F("ئەم هەڵەیە مەکە!", "Black", 900, 104, RED), 540, y)
    return c

# ======================= 5 Yarmati Jobcenter =======================
def c_5_yarmati():
    c = background(); frame(c, "یارمەتیی Jobcenter")
    y = 330
    big = T("٥", fa("Black", 480), GREEN, rtl=True, pad=0)
    for (x, yy, r) in [(230, 560, 86), (850, 520, 76), (110, 400, 46), (970, 390, 50), (330, 380, 40), (760, 360, 38)]:
        place(c, coin(r), x, yy, sh=True)
    place(c, big, 540, y - 70, sh=True)
    y += 500
    y = place(c, F("یارمەتیی دارایی", "Black", 940, 140, INK), 540, y) - 6
    y = place(c, hstack([T("Jobcenter", la("Black", 76), GREEN, pad=4), F("کە", "Black", 300, 76, INK, pad=4)], 18), 540, y) + 30
    y = place(c, pill(F("بەڵام کەس پێت ناڵێت!", "Black", 820, 70, WHITE, pad=4), RED, 44, 20), 540, y, sh=True, rot=-2) + 40
    place(c, F("ژمارە ١ تەنانەت بێ Jobcenter یش هەیە!", "Bold", 940, 50, GREEN), 540, y)
    return c

JOBS = {
    "Kurdi-Widerruf": c_widerruf,
    "Kurdi-AsylG-3-4": c_asylg_3_4,
    "Kurdi-25-2-Subsidiaer": c_25_2,
    "Kurdi-Besuchsvisum": c_besuch,
    "Kurdi-5-Yarmati-Jobcenter": c_5_yarmati,
}

if __name__ == "__main__":
    only = sys.argv[1:]
    for n, f in JOBS.items():
        if only and n not in only: continue
        f().convert("RGB").save(OUT + f"cover-{n}.jpg", quality=93)
        print("ok", n)

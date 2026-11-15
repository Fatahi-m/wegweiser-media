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

MAIN_LOGO = os.path.normpath(S + "/../../../brand/logo-kurdi-main.png")

def logo(size):
    if os.path.exists(MAIN_LOGO):
        return Image.open(MAIN_LOGO).convert("RGBA").resize((size, size), Image.LANCZOS)
    return logo_old(size)

def logo_old(size):
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

# ======================= 25.5 / 25a / 25b =======================
def c_25_5ab():
    c = background(); frame(c, "ئیقامە بێ پەنابەری")
    y = 300
    y = place(c, F("پەنابەرییەکەت ڕەفز کرا؟", "Black", 960, 100, INK), 540, y) + 6
    st = pill(T("ABGELEHNT", la("Black", 70), RED, pad=0), (0, 0, 0, 0), 30, 12, r=18, outline=RED, ow=9)
    y = place(c, st, 540, y, rot=-5) + 10
    y = place(c, F("هێشتا ٣ ڕێگا هەیە!", "Black", 960, 128, GREEN), 540, y) + 60
    cols = [(WHITE, "§ 25.5", "🚪", "گەڕانەوە مەحاڵە"), (GOLD, "§ 25a", "🎓", "گەنجان"), (GREEN, "§ 25b", "🤝", "ئینتیگراسیۆن")]
    for i, (col, para, ic, sub) in enumerate(cols):
        x = 200 + i * 340; tc = WHITE if col == GREEN else INK
        t = Image.new("RGBA", (300, 470), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
        d.rounded_rectangle((0, 0, 299, 469), 46, fill=col, outline=(214, 208, 196) if col == WHITE else None, width=4)
        n = circle_badge(84, RED, T(str(i + 1), la("Black", 54), WHITE, pad=0)); t.alpha_composite(n, (108, 28))
        e = emoji(ic, 120); t.alpha_composite(e, ((300 - e.width) // 2, 138))
        pp = F(para, "Black", 260, 74, tc, latin=True); t.alpha_composite(pp, ((300 - pp.width) // 2, 290))
        s_ = F(sub, "Bold", 260, 40, tc); t.alpha_composite(s_, ((300 - s_.width) // 2, 385))
        place(c, t, x, y + (0 if i == 1 else 30), sh=True, rot=(4 if i == 0 else -4 if i == 2 else 0))
    y += 580
    place(c, pill(F("ببینە کامیان بۆ تۆیە", "Black", 760, 54, WHITE, pad=4), INK, 38, 14), 540, y, sh=True)
    return c

# ======================= 25.5 =======================
def c_25_5():
    c = background(); frame(c, "ئیقامەی 25.5")
    y = 300
    y = place(c, F("لەسەر کارتەکەت 25.5 نووسراوە؟", "Black", 960, 88, INK), 540, y) + 4
    y = place(c, F("لاوازترین ئیقامەی ئەڵمانیا!", "Black", 960, 92, RED), 540, y) + 26
    y = place(c, rcard(700, "25 Abs. 5", highlight=(255, 120, 110)), 540, y, sh=True, rot=-3) + 36
    def row(icon, txt, col):
        r = Image.new("RGBA", (880, 116), (0, 0, 0, 0)); d = ImageDraw.Draw(r)
        d.rounded_rectangle((0, 0, 879, 115), 34, fill=WHITE, outline=col, width=5)
        b = circle_badge(80, col, emoji(icon, 46)); r.alpha_composite(b, (880 - 18 - 80, 18))
        t = F(txt, "Black", 720, 54, INK); r.alpha_composite(t, (880 - 18 - 80 - 24 - t.width, (116 - t.height) // 2))
        return r
    for icon, txt, col in [("❌", "هێنانی خێزان قەدەغەیە", RED), ("❌", "پاسپۆرتی ڕاستەوخۆ نییە", RED), ("⚠️", "سەفەر بۆ وڵاتی خۆت = مەترسی", GOLD)]:
        y = place(c, row(icon, txt, col), 540, y) + 16
    y += 4
    place(c, pill(hstack([F("بەڵام ڕێگای دەربازبوونی هەیە!", "Black", 700, 54, WHITE, pad=4), emoji("🔑", 54)], 14), GREEN, 38, 14), 540, y, sh=True)
    return c

# ======================= 25a =======================
def c_25a():
    c = background(); frame(c, "ئیقامەی گەنجان")
    y = 300
    y = place(c, F("گەنجیت و لە ئەڵمانیا", "Black", 960, 104, INK), 540, y) - 6
    y = place(c, F("خوێندوویت؟", "Black", 960, 132, GREEN), 540, y) + 30
    card = rcard(760, "25a")
    place(c, card, 560, y + 20, sh=True, rot=3)
    place(c, emoji("🎓", 190), 190, y - 30, sh=True)
    place(c, emoji("🎒", 130), 150, y + 330, sh=True)
    y += 560
    y = place(c, pill(F("ئیقامە وەردەگریت!", "Black", 760, 92, WHITE, pad=4), GREEN, 52, 18), 540, y, sh=True, rot=-2) + 34
    place(c, F("تەنانەت ئەگەر پەنابەرییەکەت ڕەفز کرابێت", "Bold", 940, 54, RED), 540, y)
    return c

# ======================= Beschäftigungsduldung =======================
def c_beschaeft():
    c = background(); frame(c, "Duldung")
    y = 300
    y = place(c, F("Duldung ت هەیە و کار دەکەیت؟", "Black", 960, 90, INK), 540, y) + 18
    y = place(c, pill(T("Beschäftigungsduldung", la("Black", 62), INK, pad=0), GOLD, 36, 16), 540, y, sh=True, rot=-2) + 50
    steps = [("💼", [T("Duldung", la("Black", 66), INK, pad=2), T("+", la("Black", 60), MUTED, pad=2), T("کار", fa("Black", 64), INK, rtl=True, pad=2)], WHITE),
             ("⏳", [T("٣٠ مانگ", fa("Black", 70), INK, rtl=True, pad=2)], GOLD),
             ("🪪", [T("§ 25b", la("Black", 70), GREEN, pad=2), T("ئیقامەی", fa("Black", 64), GREEN, rtl=True, pad=2)], GREEN)]
    x_line = 250; gap = 210
    ImageDraw.Draw(c).rounded_rectangle((x_line - 7, y + 70, x_line + 7, y + 70 + gap * 2), 7, fill=GREEN)
    for i, (ic, parts, col) in enumerate(steps):
        yy = y + i * gap
        place(c, circle_badge(140, col, emoji(ic, 76), ring=GREEN), x_line, yy, sh=True)
        lab = hstack(parts, 14); c.alpha_composite(lab, (x_line + 110, yy + 70 - lab.height // 2))
    y += gap * 2 + 200
    y = place(c, F("دوای ٣٠ مانگ ئیقامە!", "Black", 960, 100, RED), 540, y) + 20
    place(c, pill(T("§ 60d AufenthG", la("Black", 48), WHITE, pad=2), INK, 34, 14), 540, y, sh=True)
    return c

# ======================= Spurwechsel =======================
def c_spurwechsel():
    c = background(); frame(c, "Spurwechsel")
    y = 300
    y = place(c, F("چەند ساڵە چاوەڕێی", "Black", 960, 104, INK), 540, y) - 6
    y = place(c, F("BAMF دەکەیت؟", "Black", 960, 124, GREEN), 540, y) + 40
    a = tile("⏳", "Asyl", RED, w=360, h=290)
    b = tile("💼", "ئیقامەی کار", GREEN, w=360, h=290)
    place(c, b, 260, y, sh=True, rot=4); place(c, a, 820, y, sh=True, rot=-4)
    place(c, circle_badge(140, GOLD, emoji("🔀", 80), ring=WHITE), 540, y + 145, sh=True, anchor="mid")
    y += 380
    y = place(c, de_card("Spurwechsel", "ڕێگایەک بۆ ئیقامەی کار", fsize=84), 540, y, sh=True) + 40
    place(c, pill(hstack([F("بەڵام زۆر ئاگاداربە!", "Black", 700, 66, WHITE, pad=4), emoji("⚠️", 60)], 14), RED, 44, 18), 540, y, sh=True, rot=-2)
    return c

# ======================= 16g =======================
def c_16g():
    c = background(); frame(c, "Ausbildung")
    y = 300
    y = place(c, F("Ausbildung دەکەیت؟", "Black", 960, 112, INK), 540, y) + 0
    y = place(c, F("بەڵام Gestattung یان Duldung ت هەیە؟", "Black", 960, 70, MUTED), 540, y) + 40
    place(c, rcard(780, "16g"), 540, y, sh=True, rot=-3)
    place(c, pill(F("نوێ لە ٢٠٢٤ەوە", "Black", 400, 50, INK, pad=4), GOLD, 30, 12), 830, y - 30, sh=True, rot=8)
    place(c, emoji("🛠️", 150), 150, y + 380, sh=True)
    y += 560
    y = place(c, F("ئیقامەیەکی نوێ:", "Black", 900, 100, GREEN), 540, y) + 10
    place(c, pill(T("§ 16g AufenthG", la("Black", 80), WHITE, pad=2), RED, 46, 18), 540, y, sh=True, rot=-2)
    return c

JOBS = {
    "Kurdi-Widerruf": c_widerruf,
    "Kurdi-AsylG-3-4": c_asylg_3_4,
    "Kurdi-25-2-Subsidiaer": c_25_2,
    "Kurdi-Besuchsvisum": c_besuch,
    "Kurdi-5-Yarmati-Jobcenter": c_5_yarmati,
    "Kurdi-Aufenthalt-25-5-a-b": c_25_5ab,
    "Kurdi-25-5": c_25_5,
    "Kurdi-25a": c_25a,
    "Kurdi-Beschaeftigungsduldung": c_beschaeft,
    "Kurdi-Spurwechsel": c_spurwechsel,
    "Kurdi-16g": c_16g,
}

# ======================= helpers for batch 2 =======================
def letter2(w, label, col=INK):
    h = int(w * 0.72); s = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=WHITE, outline=(214, 208, 196), width=4)
    d.polygon([(6, 8), (w / 2, h * 0.52), (w - 6, 8)], fill=(240, 236, 226), outline=(214, 208, 196))
    t = F(label, "Black", int(w * 0.5), int(w * 0.16), col, latin=True); s.alpha_composite(t, (int(w * 0.07), int(h * 0.62)))
    for i in range(2):
        y = int(h * (0.68 + i * 0.1)); d.rounded_rectangle((int(w * 0.62), y, int(w * (0.92 - i * 0.1)), y + 12), 6, fill=(204, 210, 206))
    return s

def para_card(txt, sub, col, tc, w=430, h=330):
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 44, fill=col, outline=(214, 208, 196) if col == WHITE else None, width=4)
    p = F(txt, "Black", w - 50, 100, tc, latin=True); t.alpha_composite(p, ((w - p.width) // 2, 50))
    s_ = F(sub, "Bold", w - 50, 48, tc); t.alpha_composite(s_, ((w - s_.width) // 2, 200))
    return t

def natpass(w):
    h = int(w * 1.38); s = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=(28, 70, 56)); d.rounded_rectangle((0, 0, 30, h - 1), 18, fill=(18, 50, 40))
    gold = (226, 182, 92)
    t = T("PASSPORT", la("Black", int(w * 0.13)), gold, pad=0); s.alpha_composite(t, ((w - t.width) // 2 + 10, int(h * 0.12)))
    cx, cy, r = w // 2 + 10, int(h * 0.5), int(w * 0.24)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=gold, width=7)
    d.ellipse((cx - r * 0.45, cy - r, cx + r * 0.45, cy + r), outline=gold, width=5)
    d.line((cx - r, cy, cx + r, cy), fill=gold, width=5); d.line((cx, cy - r, cx, cy + r), fill=gold, width=5)
    cw = int(w * 0.16); x0 = cx - cw // 2; y0 = int(h * 0.83)
    d.rounded_rectangle((x0, y0, x0 + cw, y0 + int(cw * 0.6)), 6, outline=gold, width=4)
    return s

# ======================= Salakan (which years count) =======================
def c_salakan():
    c = background(); frame(c, "Einbürgerung")
    y = 300
    y = place(c, F("چەند ساڵە لە ئەڵمانیایت؟", "Black", 960, 96, INK), 540, y) + 10
    y = place(c, F("کام ساڵەکانت حساب دەکرێن؟", "Black", 960, 96, GREEN), 540, y) + 50
    items = [("Gestattung", "❓", GOLD, INK), ("Duldung", "❓", RED, WHITE), ("Aufenthalt", "✅", GREEN, WHITE)]
    for i, (lab, ic, col, tc) in enumerate(items):
        t = Image.new("RGBA", (310, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
        d.rounded_rectangle((0, 0, 309, 399), 44, fill=col)
        e = emoji("📅", 120); t.alpha_composite(e, ((310 - e.width) // 2, 40))
        l = F(lab, "Black", 270, 56, tc, latin=True); t.alpha_composite(l, ((310 - l.width) // 2, 200))
        b = emoji(ic, 80); t.alpha_composite(b, ((310 - b.width) // 2, 290))
        place(c, t, 870 - i * 330, y + (0 if i == 1 else 30), sh=True, rot=(-4 if i == 0 else 4 if i == 2 else 0))
    y += 520
    y = place(c, pill(F("ئیقامەی هەمیشەیی و پاسپۆرت", "Black", 860, 64, WHITE, pad=4), GREEN, 44, 18), 540, y, sh=True, rot=-2) + 30
    return c

# ======================= Niederlassung =======================
def c_niederlassung():
    c = background(); frame(c, "Niederlassung")
    y = 300
    y = place(c, F("ئیقامەی هەمیشەیی", "Black", 960, 130, GREEN), 540, y) - 6
    y = place(c, F("کەی و بە چ مەرجێک؟", "Black", 960, 104, INK), 540, y) + 40
    place(c, rcard(840, "unbefristet", highlight=(150, 220, 170)), 560, y + 30, sh=True, rot=-3)
    place(c, emoji("🏠", 170), 150, y - 50, sh=True)
    y += 620
    y = place(c, pill(T("Niederlassungserlaubnis", la("Black", 58), INK, pad=0), GOLD, 36, 16), 540, y, sh=True, rot=-2) + 40
    place(c, pill(F("ببینە تۆ لە کام بەشیت", "Black", 760, 60, WHITE, pad=4), RED, 40, 16), 540, y, sh=True)
    return c

# ======================= 25.1 =======================
def c_25_1():
    c = background(); frame(c, "ئیقامەی 25.1")
    y = 300
    y = place(c, F("لەسەر کارتەکەت 25.1 نووسراوە؟", "Black", 960, 88, INK), 540, y) + 4
    y = place(c, F("باشترین جۆری پەنابەرییە!", "Black", 960, 96, GREEN), 540, y) + 30
    y = place(c, rcard(780, "25 Abs. 1", highlight=(150, 220, 170)), 540, y, sh=True, rot=3) + 50
    place(c, tile("🏠", "ئیقامەی هەمیشەیی", GREEN), 770, y, sh=True)
    place(c, tile("🇩🇪", "پاسپۆرت", GOLD), 310, y, sh=True)
    place(c, circle_badge(120, RED, T("?", la("Black", 100), WHITE, pad=0), ring=WHITE), 540, y + 150, sh=True, anchor="mid")
    y += 330
    place(c, F("کەی وەریدەگریت؟", "Black", 900, 100, RED), 540, y)
    return c

# ======================= 31 Jiabunawa =======================
def c_31():
    c = background(); frame(c, "§ 31 AufenthG")
    y = 300
    y = place(c, F("جیا ببیتەوە،", "Black", 960, 120, INK), 540, y) - 6
    y = place(c, F("ئیقامەکەت دەڕوات؟", "Black", 960, 120, RED), 540, y) + 30
    place(c, emoji("💍", 170), 300, y + 20, sh=True, rot=12)
    place(c, emoji("💔", 230), 560, y - 10, sh=True)
    place(c, emoji("💍", 170), 820, y + 20, sh=True, rot=-12)
    y += 300
    y = place(c, pill(F("نا، ئەگەر ئەمە بزانیت!", "Black", 800, 90, WHITE, pad=4), GREEN, 52, 18), 540, y, sh=True, rot=-2) + 50
    place(c, de_card("§ 31 AufenthG", "مافی ئیقامەی سەربەخۆی هاوسەر", fsize=80), 540, y, sh=True)
    return c

# ======================= Rente =======================
def c_rente():
    c = background(); frame(c, "Rente")
    y = 300
    y = place(c, F("دوای ساڵانێک کار لە ئەڵمانیا", "Black", 960, 84, INK), 540, y) + 6
    y = place(c, F("چەند خانەنشینی وەردەگریت؟", "Black", 960, 96, GREEN), 540, y) + 40
    for (x, yy, r) in [(180, y + 60, 70), (900, y + 30, 80), (120, y + 330, 50), (960, y + 320, 56)]:
        place(c, coin(r), x, yy, sh=True)
    place(c, hstack([emoji("👵", 190), emoji("👴", 190)], 10), 540, y, sh=True)
    y += 230
    y = place(c, circle_badge(240, RED, T("€ ?", la("Black", 100), WHITE, pad=0), ring=WHITE), 540, y, sh=True) + 50
    place(c, pill(F("ژمارەکە سەرت سووڕ دەمێنێت!", "Black", 860, 66, WHITE, pad=4), INK, 44, 18), 540, y, sh=True, rot=-2)
    return c

# ======================= Chancenkarte =======================
def c_chancenkarte():
    c = background(); frame(c, "Chancenkarte")
    y = 300
    y = place(c, F("بێ پێشنیاری کار", "Black", 960, 120, INK), 540, y) - 6
    y = place(c, F("وەرە ئەڵمانیا!", "Black", 960, 130, GREEN), 540, y) + 20
    y = place(c, pill(T("Chancenkarte", la("Black", 70), INK, pad=0), GOLD, 40, 16), 540, y, sh=True, rot=-2) + 40
    tiles = [("🎓", "بڕوانامە", GREEN), ("🗣️", "A1 / B2", GOLD), ("⭐", "٦ خاڵ", GOLD), ("💶", "١٠٩١ €", GREEN)]
    for i, (ic, tx, col) in enumerate(tiles):
        x = 770 if i % 2 == 0 else 310; yy = y + (i // 2) * 320
        place(c, tile(ic, tx, col, w=400, h=290), x, yy, sh=True)
    return c

# ======================= DTZ B1 neu =======================
def c_dtz():
    c = background(); frame(c, "DTZ B1")
    y = 300
    y = place(c, F("لە 1ی نۆڤەمبەرەوە", "Black", 960, 110, INK), 540, y) + 0
    y = place(c, F("تاقیکردنەوەی B1", "Black", 960, 120, GREEN), 540, y) - 4
    y = place(c, F("قورستر دەبێت!", "Black", 960, 130, RED), 540, y) + 40
    place(c, emoji("📝", 200), 250, y + 10, sh=True, rot=8)
    place(c, circle_badge(300, GREEN, T("B1", la("Black", 150), WHITE, pad=0), ring=WHITE), 600, y, sh=True)
    place(c, emoji("⚠️", 120), 900, y + 220, sh=True)
    y += 360
    y = place(c, pill(T("01.11.2026", la("Black", 72), INK, pad=0), GOLD, 44, 16), 540, y, sh=True, rot=-2) + 40
    place(c, pill(F("چی گۆڕاوە؟", "Black", 600, 70, WHITE, pad=4), INK, 44, 16), 540, y, sh=True)
    return c

# ======================= Jobcenter letter =======================
def c_jobcenter():
    c = background(); frame(c, "Jobcenter")
    y = 300
    y = place(c, F("نامەت لە Jobcenter ەوە", "Black", 960, 104, INK), 540, y) - 6
    y = place(c, F("بۆ هاتووە؟", "Black", 960, 130, GREEN), 540, y) + 40
    place(c, letter2(640, "Jobcenter", GREEN), 520, y, sh=True, rot=-5)
    place(c, emoji("📩", 140), 900, y - 30, sh=True)
    y += 560
    y = place(c, pill(F("پێش وەڵامدانەوە", "Black", 800, 84, WHITE, pad=4), RED, 50, 18), 540, y, sh=True, rot=-2) + 34
    nums = [circle_badge(110, GREEN, T(n, la("Black", 64), WHITE, pad=0), ring=WHITE) for n in ("3", "2", "1")]
    place(c, hstack(nums + [F("ئەم هەنگاوانە ببینە", "Black", 560, 60, INK)], 18), 540, y, sh=True)
    return c

# ======================= BAMF letter =======================
def c_bamf():
    c = background(); frame(c, "BAMF")
    y = 300
    y = place(c, F("نامەت لە BAMF ەوە", "Black", 960, 112, INK), 540, y) - 6
    y = place(c, F("بۆ هاتووە؟", "Black", 960, 130, GREEN), 540, y) + 40
    place(c, letter2(660, "BAMF", INK), 540, y, sh=True, rot=4)
    place(c, emoji("✉️", 130), 170, y - 20, sh=True)
    place(c, emoji("⚠️", 120), 920, y + 360, sh=True)
    y += 580
    y = place(c, F("ئەمە بزانە", "Black", 900, 110, RED), 540, y) + 10
    place(c, pill(F("پێش ئەوەی هەر کارێک بکەیت", "Black", 860, 60, WHITE, pad=4), GREEN, 40, 16), 540, y, sh=True)
    return c

# ======================= Duldung Arten =======================
def c_duldung_arten():
    c = background(); frame(c, "Duldung")
    y = 300
    y = place(c, F("هەموو Duldung ێک", "Black", 960, 120, INK), 540, y) - 6
    y = place(c, F("وەک یەک نییە!", "Black", 960, 130, RED), 540, y) + 40
    cards = [("§ 60a", "Duldung", WHITE, INK), ("§ 60b", "Identität", RED, WHITE), ("§ 60c", "Ausbildung", GOLD, INK), ("§ 60d", "Beschäftigung", GREEN, WHITE)]
    for i, (p, s_, col, tc) in enumerate(cards):
        x = 770 if i % 2 == 0 else 310; yy = y + (i // 2) * 300
        t = Image.new("RGBA", (420, 270), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
        d.rounded_rectangle((0, 0, 419, 269), 44, fill=col, outline=(214, 208, 196) if col == WHITE else None, width=4)
        pp = T(p, la("Black", 100), tc, pad=0); t.alpha_composite(pp, ((420 - pp.width) // 2, 40))
        ss = F(s_, "Bold", 370, 46, tc, latin=True); t.alpha_composite(ss, ((420 - ss.width) // 2, 180))
        place(c, t, x, yy, sh=True, rot=(3 if i in (0, 3) else -3))
    y += 640
    place(c, pill(F("ببینە کارتەکەی تۆ چی دەڵێت", "Black", 860, 60, WHITE, pad=4), INK, 40, 16), 540, y, sh=True)
    return c

# ======================= Umzug Duldung =======================
def c_umzug():
    c = background(); frame(c, "Wohnsitzauflage")
    y = 300
    y = place(c, F("Duldung یان Gestattung ت هەیە؟", "Black", 960, 80, INK), 540, y) + 10
    y = place(c, F("دەتەوێت بچیتە شارێکی تر؟", "Black", 960, 96, GREEN), 540, y) + 50
    place(c, tile("🏙️", "A", GREEN, w=300, h=290), 820, y, sh=True, rot=-3)
    place(c, tile("🏘️", "B", GOLD, w=300, h=290), 260, y, sh=True, rot=3)
    place(c, emoji("🚚", 150), 540, y + 70, sh=True)
    y += 360
    y = place(c, pill(F("بێ مۆڵەت = پارەکەت دەبڕن!", "Black", 860, 70, WHITE, pad=4), RED, 44, 18), 540, y, sh=True, rot=-2) + 40
    place(c, pill(hstack([F("بەڵام ڕێگای یاسایی هەیە", "Black", 720, 58, WHITE, pad=4), emoji("✅", 54)], 14), GREEN, 38, 14), 540, y, sh=True)
    return c

# ======================= Pass Jawab =======================
def c_pass_jawab():
    c = background(); frame(c, "پاسپۆرت")
    y = 300
    y = place(c, F("وەرگرتنی پاسپۆرتی وڵاتەکەت", "Black", 960, 90, INK), 540, y) + 0
    y = place(c, F("مەترسیدارە؟", "Black", 960, 150, RED), 540, y) + 30
    place(c, natpass(300), 400, y, sh=True, rot=8)
    place(c, circle_badge(170, RED, T("?", la("Black", 140), WHITE, pad=0), ring=WHITE), 720, y + 120, sh=True)
    place(c, emoji("⚠️", 120), 820, y + 330, sh=True)
    y += 470
    y = place(c, pill(F("بۆ هەموو ئیقامەیەک وەک یەک نییە!", "Black", 880, 62, WHITE, pad=4), GREEN, 40, 18), 540, y, sh=True, rot=-2) + 30
    return c

JOBS.update({
    "Kurdi-Salakan": c_salakan,
    "Kurdi-Niederlassung": c_niederlassung,
    "Kurdi-25-1": c_25_1,
    "Kurdi-31-Jiabunawa": c_31,
    "Kurdi-Rente": c_rente,
    "Kurdi-Chancenkarte": c_chancenkarte,
    "Kurdi-DTZ-B1-neu": c_dtz,
    "Kurdi-Jobcenter": c_jobcenter,
    "Kurdi-BAMF": c_bamf,
    "Kurdi-Duldung-Arten": c_duldung_arten,
    "Kurdi-Umzug-Duldung": c_umzug,
    "Kurdi-Pass-Jawab": c_pass_jawab,
})

if __name__ == "__main__":
    only = sys.argv[1:]
    for n, f in JOBS.items():
        if only and n not in only: continue
        f().convert("RGB").save(OUT + f"cover-{n}.jpg", quality=93)
        print("ok", n)

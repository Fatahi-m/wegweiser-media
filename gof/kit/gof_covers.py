import os; KIT = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, KIT)
OUTDIR = os.environ.get('GOF_OUT', os.path.join(KIT, '..', 'work'))
from covers import *
NAVY = (15, 26, 43); MUST = (242, 182, 50); RED_ = (226, 104, 90); BLUE = (90, 169, 226); SAVE = (108, 199, 154); CHALK = (238, 241, 244); MUTED = (160, 175, 196)
def L(w, s): return la(w, s)
def logo(sz):
    lg = Image.open(D + "/brand/logo.png").convert("RGBA").resize((sz, sz), Image.LANCZOS)
    m = Image.new("L", (sz, sz), 0); ImageDraw.Draw(m).ellipse((0, 0, sz - 1, sz - 1), fill=255); lg.putalpha(m); return lg
def strip(c, y):
    lg = logo(84); t = tsprite("GELD OHNE FILTER", L("Black", 38), MUST); w = 84 + 20 + t.width; x = (W - w) // 2
    c.alpha_composite(lg, (x, y)); c.alpha_composite(t, (x + 104, y + (84 - t.height) // 2))
def doc(w, head, big, bigcol, hcol=(30, 60, 110), stamp=None):
    h = int(w * 0.66); S = 2; im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w * S - 1, h * S - 1), 28 * S, fill=(244, 246, 248))
    d.rounded_rectangle((0, 0, w * S - 1, 76 * S), 28 * S, fill=hcol); d.rectangle((0, 46 * S, w * S - 1, 76 * S), fill=hcol)
    t = fit(head, lambda s: L("Black", s), (w - 60) * S, 30 * S, fill=WHITE); im.alpha_composite(t, ((w * S - t.width) // 2, 16 * S))
    for i, yy in enumerate((110, 145)): d.rounded_rectangle((40 * S, yy * S, (w - 60 - i * 90) * S, (yy + 16) * S), 8 * S, fill=(210, 216, 224))
    b = fit(big, lambda s: L("Black", s), (w - 80) * S, 96 * S, fill=bigcol); im.alpha_composite(b, ((w * S - b.width) // 2, int(h * S * 0.52)))
    if stamp:
        st = tsprite(stamp, L("Black", 44 * S), RED_); sb = Image.new("RGBA", (st.width + 40 * S, st.height + 20 * S), (0, 0, 0, 0))
        ImageDraw.Draw(sb).rounded_rectangle((0, 0, sb.width - 1, sb.height - 1), 12 * S, outline=RED_, width=7 * S); sb.alpha_composite(st, (20 * S, 10 * S))
        sb = sb.rotate(-14, resample=Image.BICUBIC, expand=True); im.alpha_composite(sb, (w * S - sb.width - 20 * S, int(h * S * 0.22)))
    return im.resize((w, h), Image.LANCZOS)
def bars(vals, cols, labels, h=480, bw=160, gap=50, q_last=False):
    T0 = 80; w = len(vals) * bw + (len(vals) - 1) * gap; im = Image.new("RGBA", (w, h + T0 + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im); mx = max(vals)
    for i, (v, c, lb) in enumerate(zip(vals, cols, labels)):
        x = i * (bw + gap); bh = int(h * v / mx); d.rounded_rectangle((x, T0 + h - bh, x + bw, T0 + h), 20, fill=c)
        q = q_last and i == len(vals) - 1
        t = tsprite(lb, L("Black", 150 if q else 50), NAVY if q else WHITE)
        im.alpha_composite(t, (x + (bw - t.width) // 2, T0 + h - bh // 2 - t.height // 2 if q else T0 + h - bh - t.height - 8))
    d.rounded_rectangle((0, T0 + h + 8, w, T0 + h + 20), 6, fill=(80, 95, 120)); return im
def badge(txt, col, size=150):
    b = Image.new("RGBA", (size, size), (0, 0, 0, 0)); ImageDraw.Draw(b).ellipse((0, 0, size - 1, size - 1), fill=col, outline=WHITE, width=8)
    t = fit(txt, lambda s: L("Black", s), size - 30, 90, fill=WHITE); b.alpha_composite(t, ((size - t.width) // 2, (size - t.height) // 2)); return b
def cover(name, pill, t1, t2, t2col, visual, low, lowcol=MUST, extra=None, glow=(60, 120, 230)):
    c = gradient_bg((22, 40, 70), (8, 14, 26), [(540, 1050, 440, glow, 80)]); rays(c, 540, 1050, (255, 255, 255), a=9); strip(c, 250)
    y = 370
    y = place(c, box(fit(pill, lambda s: L("Black", s), 900, 70, fill=NAVY), MUST, 40, 16, 34), 540, y, sh=True) + 24
    y = place(c, fit(t1, lambda s: L("Black", s), 980, 96, fill=WHITE), 540, y) - 4
    y = place(c, fit(t2, lambda s: L("Black", s), 990, 140, fill=t2col), 540, y, sh=True) + 40
    vy = y; place(c, visual, 540, y, sh=True)
    if extra: extra(c, vy)
    place(c, box(fit(low, lambda s: L("Black", s), 880, 58, fill=NAVY), lowcol, 40, 20, 30), 540, 1470, sh=True)
    c.alpha_composite(logo(120), (W - 170, 1580))
    t = tsprite("@Geld-ohne-Filter", la("Bold", 34, False), MUTED); c.alpha_composite(t, ((W - t.width) // 2, 1760))
    c.convert("RGB").save(OUTDIR + "/cover-GoF-" + name + ".jpg", quality=93)

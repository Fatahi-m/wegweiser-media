#!/usr/bin/env python3
"""Geld ohne Filter – 'Wie viel musst du sparen?' short. usage: sparen.py audio out.mp4 [--frames ...]"""
import sys, math, subprocess
sys.path.insert(0, "/home/claude/wegweiser/tax2")
from render import El, Dyn, text_sprite, rounded, shadowed, ease_out, ease_back, Image, ImageDraw, ImageFont, W, H, FPS
D = "/home/claude/wegweiser"
NAVY = (15, 26, 43); PANEL = (23, 38, 61); PANEL2 = (30, 50, 80); MUST = (242, 182, 50); RENT = (226, 104, 90)
LIFE = (90, 169, 226); SAVE = (108, 199, 154); CHALK = (238, 241, 244); MUTED = (147, 163, 184)
cx = W // 2
TOTAL = 66.26
OFF = 170

def F(w, s): return ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-" + w + ".otf", s)
def T(s, size, col=CHALK, w="Black"): return text_sprite(s, F(w, size), col)
def fit(s, size, maxw, col=CHALK, w="Black"):
    while text_sprite(s, F(w, size), col).width > maxw and size > 20: size -= 2
    return text_sprite(s, F(w, size), col)

def de(n): return f"{n:,.0f}".replace(",", ".")

def pill(s, bg, fg, size=40, w="ExtraBold"):
    t = T(s, size, fg, w); c = rounded(t.width + 60, t.height + 26, (t.height + 26) // 2, bg); c.alpha_composite(t, (30, 13)); return c

def card(w, h, col=PANEL, r=40, outline=None):
    return rounded(w, h, r, col, outline=outline, ow=4 if outline else 0)

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
    bg.alpha_composite(T("Rente · Folge 2", 30, MUTED, "SemiBold"), (188, 150))
    # bottom strip
    d.rectangle((0, H - 120, W, H), fill=(11, 19, 32))
    ft = T("Keine Anlageberatung · Stand: Oktober 2026", 28, MUTED, "SemiBold"); bg.alpha_composite(ft, (cx - ft.width // 2, H - 84))
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

def curve(t0, t_out, x0=150, y0=1300, w=780, h=420):
    # compound growth 155 €/month at 5% real over 37 years vs simple sum
    r = 0.05 / 12; n = 37 * 12
    pts_c = []; pts_s = []; bal = 0
    for i in range(n + 1):
        if i: bal = bal * (1 + r) + 155
        pts_c.append(bal); pts_s.append(155 * i)
    mx = pts_c[-1]
    def fn(frame, t):
        if t < t0 or t > t_out + 0.3: return
        o = ease_out((t - t0) / 0.3) * ((1 - ease_out((t - t_out) / 0.3)) if t > t_out else 1)
        p = ease_out((t - t0 - 0.3) / 2.6); k = max(2, int(n * p))
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.line((x0, y0, x0 + w, y0), fill=MUTED + (160,), width=4)
        def P(i, v): return (x0 + w * i / n, y0 - h * v / mx)
        d.line([P(i, pts_s[i]) for i in range(0, k + 1, 3)], fill=MUTED + (255,), width=8)
        poly = [P(i, pts_c[i]) for i in range(0, k + 1, 3)]
        d.polygon(poly + [(poly[-1][0], y0), (x0, y0)], fill=SAVE + (50,))
        d.line(poly, fill=SAVE + (255,), width=12)
        d.line([P(i, pts_s[i]) for i in range(0, k + 1, 3)], fill=MUTED + (255,), width=8)
        if o < 0.999: im.putalpha(im.getchannel("A").point(lambda a: int(a * o)))
        frame.alpha_composite(im)
    return Dyn(fn)

def build():
    els = []
    def A(img, x, y, *a, **k):
        if k.get("anchor") == "c": x += img.info.get("pad", 0)
        els.append(El(img, x, y, *a, **k))
    # L0 hook 0–9.15
    e = 8.9
    A(pill("Letzte Folge: Rente", PANEL2, MUTED, 38), cx, 400, 0.1, e, anim="fade", anchor="c")
    A(T("Deine Rentenlücke", 92), cx, 520, 0.3, e, anchor="c")
    els.append(money_count(1.4, 1.0, 1000, 680, RENT, 215, prefix="–", t_out=e))
    A(T("pro Monat", 56, MUTED, "Bold"), cx, 960, 2.0, e, anchor="c")
    q = card(900, 190, MUST, 44); qt = fit("Wie viel musst du sparen?", 72, 820, NAVY); q.alpha_composite(qt, ((900 - qt.width) // 2, (190 - qt.height) // 2))
    A(shadowed(q, alpha=90), cx, 1150, 6.3, e, anim="pop", anchor="c")
    # L1 9.15–12.5
    e = 12.25
    A(T("Wir rechnen in", 70, CHALK, "ExtraBold"), cx, 640, 9.3, e, anchor="c")
    A(T("heutigem Geld", 130, LIFE), cx, 750, 9.7, e, anim="pop", anchor="c")
    A(pill("= nach Inflation", PANEL2, CHALK, 52), cx, 960, 10.9, e, anim="up", anchor="c")
    # L2 12.5–20.63
    e = 20.4
    a = card(400, 260); at = T("1.000 €", 96, SAVE); a.alpha_composite(at, ((400 - at.width) // 2, 50)); al = T("extra pro Monat", 38, MUTED, "Bold"); a.alpha_composite(al, ((400 - al.width) // 2, 175))
    b = card(400, 260); bt = T("20", 110, LIFE); b.alpha_composite(bt, ((400 - bt.width) // 2, 40)); bl = T("Jahre lang", 38, MUTED, "Bold"); b.alpha_composite(bl, ((400 - bl.width) // 2, 175))
    A(shadowed(a, alpha=80), 70, 430, 12.8, e, anim="pop")
    A(T("×", 100, CHALK), cx, 520, 13.6, e, anim="fade", anchor="c")
    A(shadowed(b, alpha=80), W - 70 - b.width - 0, 430, 14.0, e, anim="pop")
    A(T("Startkapital zum Rentenbeginn", 54, CHALK, "ExtraBold"), cx, 830, 16.3, e, anchor="c")
    els.append(money_count(17.3, 1.4, 200000, 940, MUST, 160, prefix="≈ ", t_out=e))
    A(T("Annahme: 2 % Rendite nach Inflation während der Auszahlung", 28, MUTED, "SemiBold"), cx, 1180, 18.2, e, anim="fade", anchor="c")
    # L3 20.63–25.94
    e = 25.7
    A(T("Klingt viel?", 110), cx, 450, 20.8, e, anim="pop", anchor="c")
    A(T("Du hast Zeit.", 80, SAVE), cx, 600, 22.6, e, anchor="c")
    ag = Image.new("RGBA", (820, 230), (0, 0, 0, 0))
    for i, (n_, l_) in enumerate((("30", "heute"), ("67", "Rente"))):
        s1 = T(n_, 150, MUST); s2 = T(l_, 38, MUTED, "Bold"); xx = 70 + i * 520
        ag.alpha_composite(s1, (xx + 90 - s1.width // 2, 0)); ag.alpha_composite(s2, (xx + 90 - s2.width // 2, 175))
    ar = T("→", 120, CHALK); ag.alpha_composite(ar, (410 - ar.width // 2, 20))
    A(ag, cx, 760, 23.6, e, anchor="c")
    els.append(bar(24.4, 1030, 760, 1.0, LIFE, e))
    A(pill("37 Jahre sparen", PANEL2, LIFE, 46), cx, 1120, 24.9, e, anchor="c")
    # L4 25.94–32.98
    e = 32.75
    A(pill("Variante 1", PANEL2, MUTED, 38), cx, 420, 26.1, e, anim="fade", anchor="c")
    A(T("Sparkonto", 130), cx, 520, 26.3, e, anim="pop", anchor="c")
    A(T("ohne echten Zinsgewinn nach Inflation", 44, MUTED, "Bold"), cx, 700, 27.4, e, anchor="c")
    els.append(money_count(29.8, 1.1, 445, 800, RENT, 260, t_out=e))
    A(T("jeden Monat", 64, CHALK, "ExtraBold"), cx, 1100, 30.6, e, anchor="c")
    # L5 32.98–41.18 : comparison
    e = 40.95
    A(pill("Variante 2", PANEL2, MUTED, 38), cx, 400, 33.1, e, anim="fade", anchor="c")
    A(T("Breit gestreuter ETF", 92), cx, 490, 33.3, e, anim="pop", anchor="c")
    A(T("angenommen 5 % pro Jahr nach Inflation", 44, MUTED, "Bold"), cx, 630, 34.6, e, anchor="c")
    def tile(title, amount, col, outline=None):
        c = card(420, 380, PANEL, 44, outline)
        t1 = T(title, 46, MUTED, "ExtraBold"); c.alpha_composite(t1, ((420 - t1.width) // 2, 40))
        t2 = fit(amount, 130, 380, col); c.alpha_composite(t2, ((420 - t2.width) // 2, 120))
        t3 = T("pro Monat", 40, CHALK, "Bold"); c.alpha_composite(t3, ((420 - t3.width) // 2, 290))
        return shadowed(c, alpha=80)
    A(tile("Sparkonto", "445 €", RENT), 75, 760, 36.2, e, anim="left")
    A(tile("ETF", "155 €", SAVE, SAVE), W - 75 - 420, 760, 38.2, e, anim="right")
    A(T("MSCI World seit 1970: Ø ca. 8,5 % pro Jahr (Stiftung Warentest)", 28, MUTED, "SemiBold"), cx, 1250, 38.8, e, anim="fade", anchor="c")
    A(T("Wir rechnen vorsichtig. Renditen schwanken.", 28, MUTED, "SemiBold"), cx, 1295, 38.8, e, anim="fade", anchor="c")
    # L6 41.18–47.43 Zinseszins curve
    e = 47.2
    A(T("Der Grund:", 64, MUTED, "ExtraBold"), cx, 400, 41.3, e, anchor="c")
    A(T("Zinseszins", 140, MUST), cx, 480, 42.3, e, anim="pop", anchor="c")
    els.append(curve(43.6, e))
    lg = Image.new("RGBA", (820, 60), (0, 0, 0, 0)); dl = ImageDraw.Draw(lg)
    dl.rounded_rectangle((0, 22, 50, 34), 6, fill=SAVE); t1 = T("mit Zinseszins", 36, SAVE, "ExtraBold"); lg.alpha_composite(t1, (64, 8))
    dl.rounded_rectangle((440, 22, 490, 34), 6, fill=MUTED); t2 = T("nur eingezahlt", 36, MUTED, "ExtraBold"); lg.alpha_composite(t2, (504, 8))
    A(lg, cx, 1325, 45.4, e, anim="fade", anchor="c")
    A(T("Dein Geld arbeitet 37 Jahre für dich", 52, CHALK, "ExtraBold"), cx, 1420, 44.2, e, anchor="c")
    # L7 47.43–53.94
    e = 53.7
    A(pill("⚠  Achtung", RENT, NAVY, 52, "Black"), cx, 430, 47.5, e, anim="pop", anchor="c")
    A(T("Gleiches Ziel, gleicher ETF:", 50, MUTED, "ExtraBold"), cx, 580, 48.2, e, anchor="c")
    A(T("Start mit 30", 56, CHALK, "ExtraBold"), 160, 700, 49.0, e, anim="fade")
    A(T("155 €", 56, SAVE), W - 160 - T("155 €", 56).width, 700, 49.0, e, anim="fade")
    els.append(bar(49.2, 790, 760, 0.53, SAVE, e))
    A(T("Start mit 40", 56, CHALK, "ExtraBold"), 160, 900, 50.3, e, anim="fade")
    A(T("290 €", 56, RENT), W - 160 - T("290 €", 56).width, 900, 50.3, e, anim="fade")
    els.append(bar(50.5, 990, 760, 1.0, RENT, e))
    q = card(860, 170, MUST, 44); qt = T("Fast doppelt so viel!", 74, NAVY); q.alpha_composite(qt, ((860 - qt.width) // 2, (170 - qt.height) // 2))
    A(shadowed(q, alpha=90), cx, 1140, 52.3, e, anim="pop", anchor="c")
    # L8 53.94–60.93
    e = 60.7
    A(T("Wichtig", 110, MUST), cx, 440, 54.1, e, anim="pop", anchor="c")
    rows = [("Renditen sind nicht garantiert", 54.9), ("Steuern sind nicht eingerechnet", 57.4), ("Keine Anlageberatung", 59.2)]
    for i, (s, t0) in enumerate(rows):
        c = card(900, 150, PANEL); ic = Image.new("RGBA", (70, 70), (0, 0, 0, 0)); ImageDraw.Draw(ic).ellipse((0, 0, 69, 69), fill=MUST)
        it = T("!", 50, NAVY); ic.alpha_composite(it, ((70 - it.width) // 2, (70 - it.height) // 2 - 2))
        c.alpha_composite(ic, (40, 40)); st = fit(s, 50, 740, CHALK, "ExtraBold"); c.alpha_composite(st, (140, (150 - st.height) // 2))
        A(shadowed(c, alpha=70), cx, 640 + i * 200, t0, e, anim="right", anchor="c")
    # L9 60.93–66.26 next episode (no dead air)
    A(pill("Nächste Folge", MUST, NAVY, 48, "Black"), cx, 470, 61.0, anim="pop", anchor="c")
    for i, (s, col) in enumerate((("Riester", RENT), ("Betriebsrente", LIFE), ("ETF", SAVE))):
        c = card(820, 150, PANEL, 40, col); st = T(s, 76, col); c.alpha_composite(st, ((820 - st.width) // 2, (150 - st.height) // 2))
        A(shadowed(c, alpha=70), cx, 620 + i * 190, 61.6 + i * 0.6, anim="up", anchor="c")
    A(T("Was lohnt sich wirklich?", 64, CHALK), cx, 1240, 64.0, anchor="c")
    return els

def render(audio, out, tt=None):
    els = build(); bg = make_bg()
    def frame_at(t):
        f = bg.copy(); L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for e in els: e.draw(L, t)
        f.alpha_composite(L.crop((0, 0, W, H - OFF)), (0, OFF))
        d = ImageDraw.Draw(f); d.rectangle((0, 0, W, 12), fill=(11, 19, 32)); d.rectangle((0, 0, int(W * t / TOTAL), 12), fill=MUST)
        return f.convert("RGB")
    if tt:
        for t in tt: frame_at(t).save(f"{out}_{t:05.2f}.png")
        return
    n = int(math.ceil(TOTAL * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n): pr.stdin.write(frame_at(i / FPS).tobytes())
    pr.stdin.close(); pr.wait()

if __name__ == "__main__":
    tt = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")] if "--frames" in sys.argv else None
    render(sys.argv[1], sys.argv[2], tt)

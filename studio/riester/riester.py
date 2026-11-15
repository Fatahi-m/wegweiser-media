#!/usr/bin/env python3
"""Geld ohne Filter – 'Wie viel musst du sparen?' short. usage: sparen.py audio out.mp4 [--frames ...]"""
import sys, math, subprocess
sys.path.insert(0, "/home/claude/wegweiser/tax2")
from render import El, Dyn, text_sprite, rounded, shadowed, ease_out, ease_back, Image, ImageDraw, ImageFont, W, H, FPS
D = "/home/claude/wegweiser"
NAVY = (15, 26, 43); PANEL = (23, 38, 61); PANEL2 = (30, 50, 80); MUST = (242, 182, 50); RENT = (226, 104, 90)
LIFE = (90, 169, 226); SAVE = (108, 199, 154); CHALK = (238, 241, 244); MUTED = (147, 163, 184)
cx = W // 2
TOTAL = 81.5
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
    bg.alpha_composite(T("Rente · Folge 3", 30, MUTED, "SemiBold"), (188, 150))
    # bottom strip
    d.rectangle((0, H - 120, W, H), fill=(11, 19, 32))
    ft = T("Keine Anlageberatung · Stand: Oktober 2026", 28, MUTED, "SemiBold"); bg.alpha_composite(ft, (cx - ft.width // 2, H - 100))
    fs = T("Quellen: Altersvorsorgereformgesetz 2026 · § 1a BetrAVG", 24, MUTED, "Medium"); bg.alpha_composite(fs, (cx - fs.width // 2, H - 58))
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

def build():
    els = []
    def A(img, x, y, *a, **k):
        if k.get("anchor") == "c": x += img.info.get("pad", 0)
        els.append(El(img, x, y, *a, **k))
    # hook A 0-5.0
    e = 5.0
    A(pill("Letzte Folge: ETF-Sparplan", PANEL2, MUTED, 38), cx, 420, 0.1, e, anim="fade", anchor="c")
    A(T("Es reichen rund", 80), cx, 560, 1.3, e, anchor="c")
    els.append(money_count(1.9, 1.0, 155, 690, SAVE, 230, t_out=e))
    A(T("pro Monat", 56, MUTED, "Bold"), cx, 970, 2.6, e, anchor="c")
    # hook B 5.1-10.9
    e = 10.95
    A(pill("Heute ohne Filter", MUST, NAVY, 46, "Black"), cx, 420, 5.22, e, anim="pop", anchor="c")
    for i, (s, col, t0) in enumerate((("Riester", RENT, 6.5), ("Betriebsrente", LIFE, 7.43), ("ETF", SAVE, 8.5))):
        c = card(820, 150, PANEL, 40, col); st = T(s, 76, col); c.alpha_composite(st, ((820 - st.width) // 2, (150 - st.height) // 2))
        A(shadowed(c, alpha=70), cx, 560 + i * 190, t0, e, anim="up", anchor="c")
    A(T("Was lohnt sich wirklich?", 66, CHALK), cx, 1150, 9.63, e, anim="pop", anchor="c")
    # 1 Riester 11.1-21.9
    e = 21.85
    A(pill("1 · Riester", RENT, NAVY, 46, "Black"), cx, 400, 11.36, e, anim="pop", anchor="c")
    A(T("Riester-Rente", 110), cx, 520, 11.6, e, anchor="c")
    A(rowcard("Ab 2027 keine neuen Verträge", RENT, size=52), cx, 720, 13.34, e, anim="right", anchor="c")
    A(T("Stattdessen:", 56, MUTED, "ExtraBold"), cx, 920, 17.33, e, anchor="c")
    q = card(900, 180, MUST, 44); qt = fit("Altersvorsorgedepot", 86, 840, NAVY); q.alpha_composite(qt, ((900 - qt.width) // 2, (180 - qt.height) // 2))
    A(shadowed(q, alpha=90), cx, 1010, 17.6, e, anim="pop", anchor="c")
    A(pill("Alte Verträge laufen weiter", PANEL2, SAVE, 46), cx, 1250, 20.04, e, anim="up", anchor="c")
    # 2 Zulage 22.0-39.5
    e = 39.5
    A(pill("Das Neue ab 2027", MUST, NAVY, 46, "Black"), cx, 400, 22.08, e, anim="pop", anchor="c")
    A(T("Zulage vom Staat", 92), cx, 510, 22.4, e, anchor="c")
    def zrow(left, right, col):
        c = card(900, 170, PANEL, 40, col)
        l = T(left, 50, CHALK, "ExtraBold"); c.alpha_composite(l, (44, (170 - l.height) // 2))
        r = T(right, 84, col); c.alpha_composite(r, (900 - 44 - r.width, (170 - r.height) // 2))
        return shadowed(c, alpha=70)
    A(zrow("erste 360 € im Jahr", "+50 %", SAVE), cx, 680, 23.17, e, anim="right", anchor="c")
    A(zrow("360 € bis 1.800 €", "+25 %", LIFE), cx, 880, 28.37, e, anim="right", anchor="c")
    A(T("maximal", 50, MUTED, "ExtraBold"), cx, 1090, 32.44, e, anchor="c")
    els.append(money_count(32.7, 1.1, 540, 1150, MUST, 170, t_out=e))
    A(T("Zulage pro Jahr", 46, CHALK, "Bold"), cx, 1350, 33.4, e, anchor="c")
    A(pill("+ bis zu 300 € pro Kind", SAVE, NAVY, 50, "Black"), cx, 1450, 35.76, e, anim="pop", anchor="c")
    # 3 Betriebsrente 39.6-54.7
    e = 54.7
    A(pill("2 · Betriebsrente", LIFE, NAVY, 46, "Black"), cx, 400, 39.76, e, anim="pop", anchor="c")
    A(T("Betriebsrente", 110), cx, 520, 40.0, e, anchor="c")
    A(rowcard("Zahlung aus dem Brutto", SAVE, num="+", size=50), cx, 720, 42.1, e, anim="right", anchor="c")
    A(rowcard("Chef gibt meist mind. 15 % dazu", SAVE, num="+", size=50), cx, 900, 46.28, e, anim="right", anchor="c")
    A(pill("⚠  Achtung", RENT, NAVY, 46, "Black"), cx, 1110, 50.21, e, anim="pop", anchor="c")
    A(rowcard("Im Alter: Steuern + Krankenkasse", RENT, num="–", size=50), cx, 1230, 51.33, e, anim="right", anchor="c")
    # 4 ETF 54.8-61.0
    e = 61.0
    A(pill("3 · ETF-Sparplan", SAVE, NAVY, 46, "Black"), cx, 400, 54.95, e, anim="pop", anchor="c")
    A(T("Freier ETF", 120), cx, 520, 55.43, e, anchor="c")
    def tile(title, val, col):
        c = card(420, 330, PANEL, 44, col)
        t1 = T(title, 46, MUTED, "ExtraBold"); c.alpha_composite(t1, ((420 - t1.width) // 2, 50))
        t2 = fit(val, 90, 380, col); c.alpha_composite(t2, ((420 - t2.width) // 2, 150))
        return shadowed(c, alpha=80)
    A(tile("Zulage", "keine", RENT), 75, 760, 57.9, e, anim="left")
    A(tile("Zugriff", "jederzeit", SAVE), W - 75 - 420, 760, 58.73, e, anim="right")
    # 5 Fazit 61.1-75.2
    e = 75.2
    A(T("Ohne Filter:", 110, MUST), cx, 420, 61.23, e, anim="pop", anchor="c")
    A(rowcard("Chef zahlt dazu? Betriebsrente", LIFE, num=1, size=44), cx, 640, 62.47, e, anim="right", anchor="c")
    A(rowcard("Ab 2027: Altersvorsorgedepot", MUST, num=2, size=50), cx, 830, 66.05, e, anim="right", anchor="c")
    A(T("vor allem mit Kindern", 40, MUTED, "Bold"), cx, 1000, 70.36, e, anim="fade", anchor="c")
    A(rowcard("Alles darüber: freier ETF", SAVE, num=3, size=50), cx, 1080, 72.37, e, anim="right", anchor="c")
    # 6 outro 75.3-81.5
    A(rowcard("Keine Anlageberatung", MUST, num="!", size=50), cx, 420, 75.4, 77.0, anim="right", anchor="c")
    A(pill("Nächste Folge", MUST, NAVY, 48, "Black"), cx, 560, 77.24, anim="pop", anchor="c")
    A(T("Warum dein Sparbuch", 84), cx, 720, 78.0, anchor="c")
    A(T("dich jedes Jahr", 84), cx, 830, 78.6, anchor="c")
    A(T("ärmer macht", 110, RENT), cx, 950, 79.2, anim="pop", anchor="c")
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

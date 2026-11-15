#!/usr/bin/env python3
"""Geld ohne Filter – 'Wie viel musst du sparen?' short. usage: sparen.py audio out.mp4 [--frames ...]"""
import sys, math, subprocess
sys.path.insert(0, "/home/claude/wegweiser/tax2")
from render import El, Dyn, text_sprite, rounded, shadowed, ease_out, ease_back, Image, ImageDraw, ImageFont, W, H, FPS
D = "/home/claude/wegweiser"
NAVY = (15, 26, 43); PANEL = (23, 38, 61); PANEL2 = (30, 50, 80); MUST = (242, 182, 50); RENT = (226, 104, 90)
LIFE = (90, 169, 226); SAVE = (108, 199, 154); CHALK = (238, 241, 244); MUTED = (147, 163, 184)
cx = W // 2
TOTAL = 55.2
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
    bg.alpha_composite(T("Sparen · Folge 4", 30, MUTED, "SemiBold"), (188, 150))
    # bottom strip
    d.rectangle((0, H - 120, W, H), fill=(11, 19, 32))
    ft = T("Keine Anlageberatung · Stand: Oktober 2026", 28, MUTED, "SemiBold"); bg.alpha_composite(ft, (cx - ft.width // 2, H - 100))
    fs = T("Quellen: Destatis 13.10.2026 · tagesgeldvergleich.net 07.10.2026", 24, MUTED, "Medium"); bg.alpha_composite(fs, (cx - fs.width // 2, H - 58))
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
    def A(img, x, y, *a, **k): els.append(El(img, x, y, *a, **k))
    def tile(title, val, col):
        c = card(420, 300, PANEL, 44, col)
        t1 = T(title, 46, MUTED, "ExtraBold"); c.alpha_composite(t1, ((420 - t1.width) // 2, 50))
        t2 = fit(val, 90, 380, col); c.alpha_composite(t2, ((420 - t2.width) // 2, 140))
        return shadowed(c, alpha=80)
    # hook + support 0-7.6
    e = 7.6
    A(T("Dein Sparbuch", 110), cx, 460, 0.28, e, anchor="c")
    A(T("macht dich jedes Jahr", 72, MUTED, "ExtraBold"), cx, 600, 0.9, e, anchor="c")
    A(T("ärmer", 170, RENT), cx, 690, 1.6, e, anim="pop", anchor="c")
    A(pill("Ganz leise.", PANEL2, MUTED, 44), cx, 920, 3.09, e, anim="up", anchor="c")
    A(pill("Folgen für mehr Geld ohne Filter", MUST, NAVY, 44, "Black"), cx, 1120, 4.53, e, anim="pop", anchor="c")
    # inflation vs Zins 7.87-19.8
    e = 19.8
    A(pill("Inflation · September 2026", RENT, NAVY, 46, "Black"), cx, 400, 7.87, e, anim="pop", anchor="c")
    A(T("3,3 %", 230, RENT), cx, 530, 10.8, e, anim="pop", anchor="c")
    A(T("Sparbuch-Zinsen · Ø Sparkasse", 46, MUTED, "ExtraBold"), cx, 850, 12.94, e, anchor="c")
    A(T("0,3 %", 200, SAVE), cx, 920, 15.0, e, anim="pop", anchor="c")
    A(pill("viele nur 0,01 %", PANEL2, CHALK, 46), cx, 1200, 17.26, e, anim="up", anchor="c")
    # loss 20.82-28.7
    e = 28.7
    A(T("Auf", 64, MUTED, "ExtraBold"), cx, 400, 20.82, e, anchor="c")
    A(T("10.000 €", 160), cx, 480, 21.3, e, anim="pop", anchor="c")
    A(T("verlierst du in einem Jahr", 56, MUTED, "ExtraBold"), cx, 700, 22.3, e, anchor="c")
    A(T("fast 300 €", 150, RENT), cx, 780, 23.2, e, anim="pop", anchor="c")
    A(T("Kaufkraft", 64), cx, 960, 23.9, e, anchor="c")
    A(rowcard("Kontostand gleich, Kaufkraft weniger", RENT, size=44), cx, 1120, 25.46, e, anim="right", anchor="c")
    # what to do 28.99-37.1
    e = 37.1
    A(T("Was du tun kannst", 90, MUST), cx, 420, 28.99, e, anim="pop", anchor="c")
    A(pill("1 · Kurzfristig", LIFE, NAVY, 46, "Black"), cx, 590, 30.41, e, anim="pop", anchor="c")
    A(rowcard("Tagesgeld-Zinsen vergleichen", LIFE, num=1, size=48), cx, 720, 31.2, e, anim="right", anchor="c")
    A(rowcard("Einlagensicherung: 100.000 € pro Bank", SAVE, num="!", size=42), cx, 910, 33.1, e, anim="right", anchor="c")
    # ETF 37.28-46.2
    e = 46.2
    A(pill("2 · Langfristig", SAVE, NAVY, 46, "Black"), cx, 420, 37.28, e, anim="pop", anchor="c")
    A(T("ETF-Sparplan", 120), cx, 540, 38.42, e, anchor="c")
    A(T("breit gestreut · für viele Jahre", 50, MUTED, "ExtraBold"), cx, 720, 39.6, e, anchor="c")
    A(tile("Schwankungen", "ja", RENT), 75, 850, 42.94, e, anim="left")
    A(tile("Chancen", "höher", SAVE), W - 75 - 420, 850, 44.2, e, anim="right")
    # disclaimer 46.39-48.6
    e = 48.6
    A(rowcard("Keine Anlageberatung, nur Fakten", MUST, num="!", size=46), cx, 700, 46.39, e, anim="right", anchor="c")
    # outro / comment
    A(pill("Deine Meinung", MUST, NAVY, 48, "Black"), cx, 420, 48.82, anim="pop", anchor="c")
    A(T("Wie viel Zinsen", 96), cx, 560, 49.0, anchor="c")
    A(T("bekommst du?", 110, MUST), cx, 680, 49.6, anim="pop", anchor="c")
    A(pill("Schreib es in die Kommentare", PANEL2, CHALK, 48), cx, 880, 50.3, anim="up", anchor="c")
    A(pill("Kanal abonnieren", SAVE, NAVY, 52, "Black"), cx, 1040, 51.0, anim="pop", anchor="c")
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

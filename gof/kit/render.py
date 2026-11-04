import os; KIT = os.path.dirname(os.path.abspath(__file__))
#!/usr/bin/env python3
"""Tax Reel v2 renderer: 1080x1920 Wegweiser style, synced to spliced audio timings.
usage: render.py timings.json audio.wav out.mp4 [--frames t1,t2,...]"""
import json, sys, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = KIT
VZ = D + "/fontdl/vz/fonts/ttf/Vazirmatn-"
INTER = KIT + "/fonts/Inter-"
W, H, FPS = 1080, 1920, 30
NAVY = (11, 42, 87); NAVY_D = (6, 24, 52); CARD = (28, 78, 150); RED = (226, 35, 26)
WHITE = (255, 255, 255); SOFT = (200, 214, 236); GOLD = (255, 196, 61); GREEN = (61, 201, 140)
M = 90

def fa(w, s): return ImageFont.truetype(VZ + w + ".ttf", s, layout_engine=ImageFont.Layout.RAQM)
def la(w, s): return ImageFont.truetype(INTER + w + ".otf", s, layout_engine=ImageFont.Layout.RAQM)
FAD = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

# ---------- easing ----------
def clamp(x): return max(0.0, min(1.0, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

# ---------- sprite helpers ----------
def text_size(text, font, rtl=False):
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    kw = dict(direction="rtl", language="fa") if rtl else {}
    b = d.textbbox((0, 0), text, font=font, **kw)
    return b, kw

def text_sprite(text, font, fill, rtl=False, pad=6):
    b, kw = text_size(text, font, rtl)
    w, h = b[2] - b[0] + 2 * pad, b[3] - b[1] + 2 * pad
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - b[0], pad - b[1]), text, font=font, fill=fill, **kw)
    return im

def shadowed(im, radius=22, off=(0, 14), alpha=110):
    pad = radius * 2
    out = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    a = im.getchannel("A").point(lambda v: v * alpha // 255)
    blk = Image.new("RGBA", im.size, (2, 10, 25, 255)); blk.putalpha(a)
    sh.paste(blk, (pad + off[0], pad + off[1]), blk)
    sh = sh.filter(ImageFilter.GaussianBlur(radius))
    out.alpha_composite(sh); out.alpha_composite(im, (pad, pad))
    out.info["pad"] = pad
    return out

def rounded(w, h, r, fill, outline=None, ow=0):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill, outline=outline, width=ow)
    return im

def speaker_icon(size, color):
    im = Image.new("RGBA", (size * 4, size * 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im); s = size * 4
    d.polygon([(s*.08, s*.36), (s*.28, s*.36), (s*.5, s*.16), (s*.5, s*.84), (s*.28, s*.64), (s*.08, s*.64)], fill=color)
    for i, r in enumerate((0.2, 0.34)):
        d.arc((s*.5 - s*r, s*.5 - s*r, s*.5 + s*r, s*.5 + s*r), -45, 45, fill=color, width=int(s*.07))
    return im.resize((size, size), Image.LANCZOS)

def chip(text, font, bg, fg, rtl=True, padx=30, h=None):
    t = text_sprite(text, font, fg, rtl)
    h = h or t.height + 26
    c = rounded(t.width + 2 * padx, h, h // 2, bg)
    c.alpha_composite(t, (padx, (h - t.height) // 2))
    return c

def german_card(word, meaning, w=940):
    """White card: speaker badge + German word (big) + Persian meaning."""
    wf = la("Black", 104)
    while text_size(word, wf)[0][2] > w - 200: wf = la("Black", wf.size - 4)
    ws = text_sprite(word, wf, NAVY)
    ms = text_sprite(meaning, fa("Bold", 46), (80, 96, 120), rtl=True)
    h = 60 + ws.height + 18 + ms.height + 56
    c = rounded(w, h, 40, WHITE)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, 18, h - 1), 9, fill=RED)  # accent stripe
    c.alpha_composite(ws, ((w - ws.width) // 2, 60))
    c.alpha_composite(ms, ((w - ms.width) // 2, 60 + ws.height + 18))
    badge = chip("DE", la("Bold", 30), RED, WHITE, rtl=False, padx=18)
    spk = speaker_icon(34, WHITE)
    b2 = Image.new("RGBA", (badge.width + 44, badge.height), (0, 0, 0, 0))
    b2.alpha_composite(rounded(b2.width, b2.height, b2.height // 2, RED)); b2.alpha_composite(spk, (14, (b2.height - 34) // 2))
    b2.alpha_composite(badge, (44, 0))
    return shadowed(c), b2

def list_row(n, meaning, word, w=920, active=False):
    """Row in deductions list: number disc | German word (top) + Persian meaning."""
    h = 186
    bg = WHITE if active else CARD
    c = rounded(w, h, 34, bg)
    d = ImageDraw.Draw(c)
    # number disc on the right (RTL reading)
    cx, cy, r = w - 84, h // 2, 44
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=RED)
    ns = text_sprite(str(n).translate(FAD), fa("Black", 50), WHITE, rtl=True)
    c.alpha_composite(ns, (cx - ns.width // 2, cy - ns.height // 2 - 2))
    ms = text_sprite(meaning, fa("Bold", 46), NAVY if active else WHITE, rtl=True)
    c.alpha_composite(ms, (w - 160 - ms.width, 26 if word else (h - ms.height) // 2))
    if word:
        wf = la("Bold", 58)
        ws = text_sprite(word, wf, RED if active else GOLD)
        c.alpha_composite(ws, (w - 160 - ws.width, h - ws.height - 22))
    return c

# ---------- background ----------
def make_bg():
    bg = Image.new("RGB", (W, H), NAVY)
    top, bot = (14, 52, 108), NAVY_D
    px = bg.load()
    grad = [tuple(int(top[k] + (bot[k] - top[k]) * (y / H)) for k in range(3)) for y in range(H)]
    d = ImageDraw.Draw(bg)
    for y in range(H): d.line((0, y, W, y), fill=grad[y])
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(dots)
    for y in range(30, H, 54):
        for x in range(30, W, 54): dd.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(255, 255, 255, 18))
    bg = bg.convert("RGBA"); bg.alpha_composite(dots)
    return bg

def glow(color, r, a):
    p = r
    g = Image.new("RGBA", (r * 2 + 2 * p, r * 2 + 2 * p), color + (0,))
    ImageDraw.Draw(g).ellipse((p, p, p + r * 2 - 1, p + r * 2 - 1), fill=color + (a,))
    return g.filter(ImageFilter.GaussianBlur(r // 2))

# ---------- scene graph ----------
class El:
    def __init__(self, img, x, y, t_in, t_out=1e9, anim="up", dur=0.45, anchor="tl", out="fade"):
        self.img, self.t_in, self.t_out, self.anim, self.dur, self.out = img, t_in, t_out, anim, dur, out
        pad = img.info.get("pad", 0)
        if anchor == "c": x -= img.width // 2
        elif anchor == "tr": x -= img.width
        self.x, self.y = x - (0 if anchor else 0), y
        self.pad = pad
    def draw(self, frame, t):
        if t < self.t_in or t > self.t_out + 0.35: return
        p = (t - self.t_in) / self.dur
        o = ease_out(p); dx = dy = 0; s = 1.0
        if self.anim == "up": dy = int((1 - ease_out(p)) * 70)
        elif self.anim == "pop": s = 0.6 + 0.4 * ease_back(p); o = ease_out(p * 1.6)
        elif self.anim == "left": dx = int((1 - ease_out(p)) * -120)
        elif self.anim == "right": dx = int((1 - ease_out(p)) * 120)
        elif self.anim == "fade": pass
        if t > self.t_out:
            q = ease_out((t - self.t_out) / 0.3); o *= (1 - q); dy -= int(q * 50)
        if o <= 0.01: return
        img = self.img
        x, y = self.x - self.pad, self.y - self.pad
        if s != 1.0:
            nw, nh = max(1, int(img.width * s)), max(1, int(img.height * s))
            x += (img.width - nw) // 2; y += (img.height - nh) // 2
            img = img.resize((nw, nh), Image.BILINEAR)
        if o < 0.999:
            img = img.copy(); a = img.getchannel("A").point(lambda v: int(v * o)); img.putalpha(a)
        frame.alpha_composite(img, (x + dx, y + dy)) if x + dx >= 0 and y + dy >= 0 else paste_clip(frame, img, x + dx, y + dy)

def paste_clip(frame, img, x, y):
    cx, cy = max(0, -x), max(0, -y)
    img = img.crop((cx, cy, img.width, img.height))
    frame.alpha_composite(img, (x + cx, y + cy))

class Dyn:
    """Per-frame drawn element (count-up, pulse, progress)."""
    def __init__(self, fn): self.fn = fn
    def draw(self, frame, t): self.fn(frame, t)

def build(T):
    """T: dict of segment times. P1..P7 (start,end), G1..G6 (start,end), total."""
    P = T["P"]; G = T["G"]; total = T["total"]; X = T.get("extra", {}); PS = T.get("pauses", [[] for _ in range(7)])
    def at(i, frac):
        """speech-resume time of the pause in segment i nearest to frac of its length"""
        est = P[i][0] + frac * (P[i][1] - P[i][0])
        if not PS[i]: return est
        a, b = min(PS[i], key=lambda p: abs((p[0] + p[1]) / 2 - est))
        return b if abs((a + b) / 2 - est) < 1.6 else est
    els = []
    cx = W // 2
    # ---------------- header (always) ----------------
    logo = Image.open(D + "/aof/wegweiser-deutschland-logo.png").convert("RGBA").resize((92, 92), Image.LANCZOS)
    mask = Image.new("L", (92, 92), 0); ImageDraw.Draw(mask).ellipse((0, 0, 91, 91), fill=255); logo.putalpha(mask)
    hdr = Image.new("RGBA", (W, 140), (0, 0, 0, 0)); hdr.alpha_composite(logo, (M, 24))
    hdr.alpha_composite(text_sprite("WEGWEISER", la("Black", 34), WHITE), (M + 112, 30))
    hdr.alpha_composite(text_sprite("DEUTSCHLAND", la("Medium", 26), SOFT), (M + 113, 74))
    tchip = chip("مالیات در آلمان", fa("Bold", 32), RED, WHITE)
    hdr.alpha_composite(tchip, (W - M - tchip.width, 46))
    els.append(El(hdr, 0, 90, 0.0, anim="fade", dur=0.4))
    disc = text_sprite("اطلاعات عمومی؛ جایگزین مشاوره‌ی مالیاتی نیست", fa("Medium", 28), (150, 170, 200), rtl=True)
    els.append(El(disc, cx, 1640, 0.3, anim="fade", anchor="c"))

    # ---------------- Scene A: hook ----------------
    a_end = at(1, 0.66) - 0.35
    q = text_sprite("می‌دونستی…", fa("Black", 72), SOFT, rtl=True)
    els.append(El(q, cx, 400, 0.05, a_end, anim="up", anchor="c"))
    l1 = text_sprite("بیشتر کسایی که در آلمان", fa("Black", 84), WHITE, rtl=True)
    els.append(El(l1, cx, 510, 0.35, a_end, anim="up", anchor="c"))
    card, badge = german_card("Steuererklärung", "اظهارنامه‌ی مالیاتی")
    els.append(El(card, cx, 690, G[0][0] - 0.05, a_end, anim="pop", anchor="c", dur=0.5))
    els.append(El(badge, cx, 660, G[0][0] + 0.1, a_end, anim="pop", anchor="c", dur=0.4))
    l2 = text_sprite("می‌دن، به‌طور میانگین", fa("Bold", 54), SOFT, rtl=True)
    t_stat = P[1][0] + 0.25
    els.append(El(l2, cx, 1070, t_stat, a_end, anim="up", anchor="c"))
    # count-up stat
    statf = la("Black", 170)
    def stat(frame, t):
        if t < t_stat + 0.2 or t > a_end + 0.35: return
        p = ease_out((t - t_stat - 0.2) / 1.1)
        o = ease_out((t - t_stat - 0.2) / 0.3) * (1 - ease_out((t - a_end) / 0.3) if t > a_end else 1)
        v = int(round(1000 * p))
        s = f"+{v:,}".replace(",", ".") + " €"
        sp = text_sprite(s, statf, GOLD)
        if o < 0.999: sp.putalpha(sp.getchannel("A").point(lambda a: int(a * o)))
        frame.alpha_composite(sp, (cx - sp.width // 2, 1160))
    els.append(Dyn(stat))
    l3 = text_sprite("پول از اداره‌ی مالیات پس می‌گیرن!", fa("Bold", 54), WHITE, rtl=True)
    els.append(El(l3, cx, 1390, t_stat + 1.4, a_end, anim="up", anchor="c"))
    warn = chip("ولی خیلی‌ها اصلاً اظهارنامه نمی‌دن!", fa("Bold", 40), RED, WHITE)
    els.append(El(warn, cx, 1490, at(1, 0.36) - 0.05, a_end, anim="pop", anchor="c"))

    # ---------------- Scene B: deductions list ----------------
    b_end = P[5][0] - 0.05
    ttl = text_sprite("چه هزینه‌هایی کم می‌شه؟", fa("Black", 76), WHITE, rtl=True)
    els.append(El(ttl, cx, 400, a_end + 0.3, b_end, anim="up", anchor="c"))
    items = [("هزینه‌ی رفت‌وآمد", "Pendlerpauschale"), ("وسایل کار", "Arbeitsmittel"),
             ("کلاس آموزشی", "Fortbildung"), ("اسباب‌کشی به‌خاطر کار", "Umzugskosten")]
    row_in = [at(1, 0.82) - 0.05, P[2][0], P[3][0], P[4][0]]
    for i, (fa_t, de_t) in enumerate(items):
        y = 560 + i * 226
        g0, g1 = G[i + 1]
        nxt = G[i + 2][0] if i < 3 else b_end
        # inactive row with persian only, from its persian start
        els.append(El(shadowed(list_row(i + 1, fa_t, None)), 80, y, row_in[i], g0 - 0.02, anim="right", out="fade"))
        # active (white) when German spoken
        els.append(El(shadowed(list_row(i + 1, fa_t, de_t, active=True)), 80, y, g0 - 0.05, nxt - 0.1, anim="pop", dur=0.35))
        # settled dark row with German word
        els.append(El(shadowed(list_row(i + 1, fa_t, de_t)), 80, y, nxt - 0.1, b_end, anim="fade", dur=0.25))

    # ---------------- Scene C: good news / 4 years / ELSTER ----------------
    c_end = P[6][0] + 0.7
    t0 = P[5][0] + 0.25
    gn = chip("خبر خوب", fa("Black", 44), GREEN, NAVY_D)
    els.append(El(gn, cx, 390, t0 + 0.05, c_end, anim="pop", anchor="c"))
    yrs = text_sprite("تا ۴ سال عقب‌تر هم می‌تونی اظهارنامه بدی", fa("Bold", 56), WHITE, rtl=True)
    els.append(El(yrs, cx, 520, t0 + 0.6, c_end, anim="up", anchor="c"))
    # year timeline
    tl_y = 650
    years = ["2022", "2023", "2024", "2025"]
    for i, yv in enumerate(years):
        x = 120 + i * 220
        box = rounded(200, 130, 28, CARD, outline=(70, 120, 190), ow=3)
        ys = text_sprite(yv, la("Black", 52), WHITE); box.alpha_composite(ys, ((200 - ys.width) // 2, (130 - ys.height) // 2))
        els.append(El(shadowed(box), x, tl_y, t0 + 1.0 + i * 0.18, c_end, anim="pop", dur=0.4))
    dl = chip("مهلت سال ۲۰۲۲:  31.12.2026", fa("Bold", 38), RED, WHITE)
    els.append(El(dl, cx, 830, at(5, 0.39) + 0.3, c_end, anim="up", anchor="c"))
    onl = chip("همه‌ش آنلاین", fa("Bold", 40), CARD, WHITE)
    els.append(El(onl, cx, 920 - 0, at(5, 0.68) - 0.05, c_end, anim="up", anchor="c"))
    ec, eb = german_card("ELSTER", "سایت رسمی اداره‌ی مالیات")
    els.append(El(ec, cx, 1090, G[5][0] - 0.05, c_end, anim="pop", anchor="c", dur=0.5))
    els.append(El(eb, cx, 1060, G[5][0] + 0.1, c_end, anim="pop", anchor="c", dur=0.4))
    fr = chip("رایگان", fa("Black", 44), GREEN, NAVY_D)
    els.append(El(fr, cx, 1430, G[5][0] + 0.6, c_end, anim="pop", anchor="c"))

    # ---------------- Scene D: outro ----------------
    t0 = P[6][0] + 1.0
    nx = chip("ویدیوی بعدی", fa("Black", 44), GOLD, NAVY_D)
    els.append(El(nx, cx, 400, t0 + 0.05, anim="pop", anchor="c"))
    items3 = [("چطوری پولت رو پس بگیری", 0.17), ("حقوق تو به‌عنوان کارمند", 0.32), ("کمک‌هایی که از دولت می‌گیری", 0.53)]
    for i, (txt, frac) in enumerate(items3):
        row = rounded(920, 160, 34, CARD)
        d = ImageDraw.Draw(row); d.ellipse((920 - 118, 40, 920 - 40, 118), fill=RED)
        ck = text_sprite(str(i + 1).translate(FAD), fa("Black", 44), WHITE, rtl=True)
        row.alpha_composite(ck, (920 - 79 - ck.width // 2, 79 - ck.height // 2 - 2))
        ts = text_sprite(txt, fa("Bold", 52), WHITE, rtl=True)
        row.alpha_composite(ts, (920 - 150 - ts.width, (160 - ts.height) // 2))
        els.append(El(shadowed(row), 80, 520 + i * 190, at(6, frac) - 0.08, anim="right"))
    # follow button with pulse
    t_f = at(6, 0.77) - 0.05
    btn = rounded(560, 130, 65, RED)
    bs = text_sprite("فالو کن", fa("Black", 60), WHITE, rtl=True)
    btn.alpha_composite(bs, ((560 - bs.width) // 2, (130 - bs.height) // 2 - 4))
    btn = shadowed(btn)
    def follow(frame, t):
        if t < t_f: return
        p = (t - t_f)
        s = (0.6 + 0.4 * ease_back(p / 0.45)) * (1 + 0.035 * math.sin(max(0, p - 0.45) * 6.0))
        img = btn.resize((int(btn.width * s), int(btn.height * s)), Image.BILINEAR)
        o = ease_out(p / 0.25)
        if o < 1: img.putalpha(img.getchannel("A").point(lambda a: int(a * o)))
        frame.alpha_composite(img, (cx - img.width // 2, 1130 + btn.height // 2 - img.height // 2))
    els.append(Dyn(follow))
    hnd = text_sprite("@wegweiser.deutschland", la("Bold", 40), SOFT)
    els.append(El(hnd, cx, 1320, t_f + 0.3, anim="fade", anchor="c"))
    return els

def render(T, audio, out, test_times=None):
    els = build(T); total = T["total"]
    bg = make_bg(); g1 = glow(RED, 360, 60); g2 = glow((60, 130, 230), 420, 70)
    def frame_at(t):
        f = bg.copy()
        f.alpha_composite(g1, (int(W - 420 + 60 * math.sin(t * 0.4)), int(1200 + 80 * math.cos(t * 0.3))))
        f.alpha_composite(g2, (int(-380 + 50 * math.cos(t * 0.35)), int(-200 + 60 * math.sin(t * 0.25))))
        for e in els: e.draw(f, t)
        # progress bar
        ImageDraw.Draw(f).rectangle((0, 0, int(W * t / total), 10), fill=RED)
        return f.convert("RGB")
    if test_times:
        for t in test_times: frame_at(t).save(f"{out}_{t:05.2f}.png")
        return
    n = int(math.ceil(total * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        pr.stdin.write(frame_at(i / FPS).tobytes())
    pr.stdin.close(); pr.wait()

if __name__ == "__main__":
    T = json.load(open(sys.argv[1]))
    tt = None
    if "--frames" in sys.argv: tt = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")]
    render(T, sys.argv[2], sys.argv[3], tt)

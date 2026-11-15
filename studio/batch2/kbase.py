"""Kurdish page visual identity: warm cream paper, deep green, Kurdish red, sun gold."""
import sys, math, subprocess
sys.path.insert(0, "/home/claude/wegweiser/tax2")
import render as R
from render import El, Dyn, text_sprite, rounded, shadowed, fa, la, ease_out, ease_back, Image, ImageDraw, text_size, W, H, FPS
from PIL import ImageFilter

CREAM = (248, 243, 232); PAPER = (255, 252, 245); INK = (24, 38, 32)
GREEN = (14, 92, 62); GREEN_L = (214, 236, 222); KRED = (206, 32, 41); SUN = (242, 169, 0); MUTED = (98, 112, 104)
KD = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
cx = W // 2

def T(s, size=72, col=INK, w="Black"): return text_sprite(s, fa(w, size), col, rtl=True)

def fitT(s, size, maxw, col=INK, w="Black"):
    f = fa(w, size)
    while text_size(s, f, rtl=True)[0][2] > maxw and f.size > 28: f = fa(w, f.size - 2)
    return text_sprite(s, f, col, rtl=True)

def kchip(s, bg, fg, size=42, latin=False):
    t = text_sprite(s, la("Bold", size) if latin else fa("Bold", size), fg, rtl=not latin)
    c = rounded(t.width + 64, t.height + 26, (t.height + 26) // 2, bg); c.alpha_composite(t, (32, 13)); return c

def sun(size, col=SUN, rays=16):
    S = size * 2; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = S / 2
    for i in range(rays):
        a = 2 * math.pi * i / rays; a1 = a - math.pi / rays * 0.45; a2 = a + math.pi / rays * 0.45
        d.polygon([(c + math.cos(a1) * S * .27, c + math.sin(a1) * S * .27), (c + math.cos(a) * S * .49, c + math.sin(a) * S * .49),
                   (c + math.cos(a2) * S * .27, c + math.sin(a2) * S * .27)], fill=col)
    d.ellipse((c - S * .25, c - S * .25, c + S * .25, c + S * .25), fill=col)
    return im.resize((size, size), Image.LANCZOS)

def make_bg():
    bg = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(bg)
    for y in range(0, H, 48): d.line([(0, y), (W, y)], fill=(238, 231, 214), width=1)   # notebook lines
    s = sun(760, (242, 169, 0, 255)); s.putalpha(s.getchannel("A").point(lambda a: int(a * .13)))
    bg.alpha_composite(s, (W - 470, -300))
    # green wave footer
    wave = Image.new("RGBA", (W, 260), (0, 0, 0, 0)); wd = ImageDraw.Draw(wave)
    pts = [(x, 90 + 26 * math.sin(x / 140)) for x in range(0, W + 1, 10)] + [(W, 260), (0, 260)]
    wd.polygon(pts, fill=GREEN); bg.alpha_composite(wave, (0, H - 260))
    pts2 = [(x, 60 + 22 * math.sin(x / 120 + 1.3)) for x in range(0, W + 1, 10)] + [(W, 90), (0, 90)]
    w2 = Image.new("RGBA", (W, 100), (0, 0, 0, 0)); ImageDraw.Draw(w2).polygon(pts2, fill=KRED + (255,)); bg.alpha_composite(w2, (0, H - 290))
    return bg

def header(topic):
    h = Image.new("RGBA", (W, 150), (0, 0, 0, 0))
    s = sun(84); h.alpha_composite(s, (W - 70 - 84, 34))
    t = kchip(topic, GREEN, (255, 255, 255), 36); h.alpha_composite(t, (W - 70 - 84 - 20 - t.width, 46))
    return El(h, 0, 70, 0.0, anim="fade", dur=0.4)

def footer(text):
    return El(T(text, 28, (255, 255, 255), "Medium"), cx, H - 120, 0.3, anim="fade", anchor="c")

def source_line(text):
    z = 30
    while text_size(text, la("Bold", z))[0][2] > 840 and z > 18: z -= 1
    lab = T("سەرچاوە:", z, MUTED, "Bold"); src = text_sprite(text, la("Bold", z), MUTED)
    im = Image.new("RGBA", (src.width + 12 + lab.width, max(src.height, lab.height)), (0, 0, 0, 0))
    im.alpha_composite(src, (0, (im.height - src.height) // 2)); im.alpha_composite(lab, (src.width + 12, (im.height - lab.height) // 2))
    return El(im, cx, 1612, 0.3, anim="fade", anchor="c")

def kcard(word, meaning, w=900):
    wf = la("Black", 100)
    while text_size(word, wf)[0][2] > w - 140: wf = la("Black", wf.size - 4)
    ws = text_sprite(word, wf, (255, 255, 255)); ms = text_sprite(meaning, fa("Bold", 44), SUN, rtl=True)
    h = 56 + ws.height + 14 + ms.height + 48
    c = rounded(w, h, 36, GREEN); d = ImageDraw.Draw(c)
    d.rounded_rectangle((w - 22, 26, w - 10, h - 26), 6, fill=KRED)
    c.alpha_composite(ws, ((w - ws.width) // 2, 50)); c.alpha_composite(ms, ((w - ms.width) // 2, 50 + ws.height + 14))
    tag = kchip("DE 🔊".replace(" 🔊", ""), SUN, INK, 30, latin=True)
    out = Image.new("RGBA", (w, h + tag.height // 2), (0, 0, 0, 0)); out.alpha_composite(c, (0, tag.height // 2)); out.alpha_composite(tag, (60, 0))
    return shadowed(out, radius=18, off=(0, 10), alpha=70)

def knum(n, size=84, bg=KRED):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse((0, 0, size - 1, size - 1), fill=bg)
    t = text_sprite(str(n).translate(KD), fa("Black", int(size * .55)), (255, 255, 255), rtl=True)
    im.alpha_composite(t, ((size - t.width) // 2, (size - t.height) // 2 - 3)); return im

def krow(text, n=None, sub=None, w=920, h=150, icon=None):
    c = rounded(w, h, 30, PAPER, outline=GREEN_L, ow=4)
    ic = icon if icon is not None else knum(n)
    c.alpha_composite(ic, (w - 36 - ic.width, (h - ic.height) // 2))
    maxw = w - 36 - ic.width - 30 - 40
    ts = fitT(text, 50, maxw, INK, "Bold")
    if sub:
        ar = any('\u0600' <= ch <= '\u06ff' for ch in sub)
        mk = (lambda z: fa("Bold", z)) if ar else (lambda z: la("Bold", z))
        sf = mk(38)
        while text_size(sub, sf, rtl=ar)[0][2] > maxw: sf = mk(sf.size - 2)
        ss = text_sprite(sub, sf, GREEN, rtl=ar); top = (h - ts.height - ss.height + 4) // 2
        c.alpha_composite(ts, (w - 36 - ic.width - 30 - ts.width, top)); c.alpha_composite(ss, (w - 36 - ic.width - 30 - ss.width, top + ts.height - 4))
    else:
        c.alpha_composite(ts, (w - 36 - ic.width - 30 - ts.width, (h - ts.height) // 2))
    return shadowed(c, radius=16, off=(0, 8), alpha=45)

def follow_btn(t_f, y, label="فۆڵۆمان بکە"):
    btn = rounded(620, 130, 65, KRED); bs = text_sprite(label, fa("Black", 60), (255, 255, 255), rtl=True)
    btn.alpha_composite(bs, ((620 - bs.width) // 2, (130 - bs.height) // 2 - 4)); btn = shadowed(btn, alpha=70)
    lg = logo(96); hs = text_sprite(HANDLE, la("Black", 50), GREEN)
    hb = Image.new("RGBA", (96 + 20 + hs.width, 96), (0, 0, 0, 0)); hb.alpha_composite(lg, (0, 0)); hb.alpha_composite(hs, (116, (96 - hs.height) // 2))
    def f(frame, t):
        if t < t_f: return
        q = ease_out((t - t_f - 0.5) / 0.4)
        if q > 0:
            h2 = hb.copy()
            if q < 1: h2.putalpha(h2.getchannel("A").point(lambda a: int(a * q)))
            frame.alpha_composite(h2, (cx - hb.width // 2, y + btn.height + 40 + int(20 * (1 - q))))
        p = t - t_f; s = (0.6 + 0.4 * ease_back(p / 0.45)) * (1 + 0.035 * math.sin(max(0, p - 0.45) * 6.0))
        img = btn.resize((int(btn.width * s), int(btn.height * s)), Image.BILINEAR); o = ease_out(p / 0.25)
        if o < 1: img.putalpha(img.getchannel("A").point(lambda a: int(a * o)))
        frame.alpha_composite(img, (cx - img.width // 2, y + btn.height // 2 - img.height // 2))
    return Dyn(f)

HANDLE = "@wegweiser_kurdi.de"
def logo(size):
    im = Image.open("/home/claude/wegweiser/brand_k/Kurdi-Profilbild.jpg").convert("RGBA").resize((size * 4, size * 4), Image.LANCZOS)
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255); im.putalpha(m)
    return im.resize((size, size), Image.LANCZOS)

def brand_badge(size=74):
    lg = logo(size); t = text_sprite(HANDLE, la("Bold", 30), INK)
    pad = 10; w = size + 14 + t.width + 28; h = size + pad * 2
    b = rounded(w, h, h // 2, PAPER + (235,), outline=GREEN_L, ow=3)
    b.alpha_composite(lg, (pad, pad)); b.alpha_composite(t, (pad + size + 14, (h - t.height) // 2))
    return shadowed(b, radius=10, off=(0, 4), alpha=35)

def add_brand(img, x=50, y=87):
    img.alpha_composite(brand_badge(), (x, y)); return img

def render(build, total, audio, out, test_times=None):
    els = build(); bg = add_brand(make_bg())
    def frame_at(t):
        f = bg.copy()
        for e in els: e.draw(f, t)
        ImageDraw.Draw(f).rectangle((0, 0, int(W * t / total), 12), fill=KRED)
        return f.convert("RGB")
    if test_times:
        for t in test_times: frame_at(t).save(f"{out}_{t:05.2f}.png")
        return
    n = int(math.ceil(total * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n): pr.stdin.write(frame_at(i / FPS).tobytes())
    pr.stdin.close(); pr.wait()

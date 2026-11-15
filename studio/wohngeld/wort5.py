#!/usr/bin/env python3
"""5 Wörter reel. usage: wort5.py cfg.json timings.json audio out.mp4 [--frames ...]"""
import sys, json, math
sys.path.insert(0, "/home/claude/wegweiser/tax2")
sys.path.insert(0, "/home/claude/wegweiser/wohngeld")
import render as R
from render import (El, Dyn, text_sprite, chip, rounded, shadowed, fa, la, ease_out, ease_back,
                    W, H, NAVY, NAVY_D, CARD, RED, WHITE, SOFT, GOLD, GREEN, FAD, Image, ImageDraw, D, M)
from wort import ART, text_size_w, wrap_lat

def word_card(wd, w=940):
    col = ART[wd["article"]]
    art = text_sprite(wd["article"], la("Black", 74), col)
    wf = la("Black", 132)
    while text_size_w(wd["word"], wf) > w - 120: wf = la("Black", wf.size - 6)
    ws = text_sprite(wd["word"], wf, NAVY)
    import re
    if re.search(r"[\u0600-\u06FF]", wd["plural"]): pl = text_sprite(wd["plural"], fa("Medium", 36), (100, 115, 140), rtl=True)
    else: pl = text_sprite(wd["plural"], la("Medium", 36), (100, 115, 140))
    pr = text_sprite("تلفظ: " + wd["pron"], fa("Medium", 36), (100, 115, 140), rtl=True)
    h = 46 + art.height - 10 + ws.height + 24 + pl.height + 6 + pr.height + 44
    c = rounded(w, h, 44, WHITE); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, w - 1, 26), 13, fill=col); d.rectangle((0, 13, w - 1, 26), fill=WHITE)
    y = 46; c.alpha_composite(art, ((w - art.width) // 2, y)); y += art.height - 10
    c.alpha_composite(ws, ((w - ws.width) // 2, y)); y += ws.height + 24
    c.alpha_composite(pl, ((w - pl.width) // 2, y)); y += pl.height + 6
    c.alpha_composite(pr, ((w - pr.width) // 2, y))
    return shadowed(c)

def sentence_card(wd, w=940):
    f = la("Bold", 56); lines = wrap_lat(wd["sentence"], f, w - 120)
    sps = [text_sprite(l, f, WHITE) for l in lines]
    fs = text_sprite(wd["sentence_fa"], fa("Bold", 46), GOLD, rtl=True)
    lab = chip("مثال", fa("Bold", 30), RED, WHITE)
    h = 36 + lab.height + 16 + sum(s.height for s in sps) + 18 + fs.height + 42
    c = rounded(w, h, 40, CARD); y = 36
    c.alpha_composite(lab, (w - 50 - lab.width, y)); y += lab.height + 16
    for s in sps: c.alpha_composite(s, ((w - s.width) // 2, y)); y += s.height
    y += 18; c.alpha_composite(fs, ((w - fs.width) // 2, y))
    return shadowed(c)

def dots(i, n=5):
    im = Image.new("RGBA", (n * 70, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(n):
        x = (n - 1 - k) * 70 + 30  # RTL order: first word on the right
        col = RED if k == i else ((255, 255, 255, 90) if k > i else (255, 255, 255, 200))
        r = 26 if k == i else 20
        d.ellipse((x - r, 30 - r, x + r, 30 + r), fill=col)
        t = text_sprite(str(k + 1).translate(FAD), fa("Black", 30 if k == i else 24), WHITE if k == i else NAVY, rtl=True)
        im.alpha_composite(t, (x - t.width // 2, 30 - t.height // 2 - 2))
    return im

def build_for(cfg):
    def build(T):
        S = T["segs"]; cx = W // 2; els = []
        logo = Image.open(D + "/aof/wegweiser-deutschland-logo.png").convert("RGBA").resize((92, 92), Image.LANCZOS)
        mask = Image.new("L", (92, 92), 0); ImageDraw.Draw(mask).ellipse((0, 0, 91, 91), fill=255); logo.putalpha(mask)
        hdr = Image.new("RGBA", (W, 140), (0, 0, 0, 0)); hdr.alpha_composite(logo, (M, 24))
        hdr.alpha_composite(text_sprite("WEGWEISER", la("Black", 34), WHITE), (M + 112, 30))
        hdr.alpha_composite(text_sprite("DEUTSCHLAND", la("Medium", 26), SOFT), (M + 113, 74))
        tc = chip(cfg["chip"], fa("Bold", 32), RED, WHITE); hdr.alpha_composite(tc, (W - M - tc.width, 46))
        els.append(El(hdr, 0, 90, 0.0, anim="fade", dur=0.3))
        # legend
        leg = Image.new("RGBA", (700, 60), (0, 0, 0, 0)); x = 0
        for a in ("der", "die", "das"):
            s = text_sprite(a, la("Black", 34), ART[a]); bx = rounded(s.width + 36, 54, 27, WHITE); bx.alpha_composite(s, (18, (54 - s.height) // 2))
            leg.alpha_composite(bx, (x, 3)); x += bx.width + 14
        els.append(El(leg.crop((0, 0, x - 14, 60)), cx, 1680, 0.3, anim="fade", anchor="c"))
        words = cfg["words"]
        gw = [S[1 + 3 * i]["t"][0] for i in range(5)]
        p_out = S[16]["t"][0]
        # intro
        i_end = gw[0] - 0.35
        b5 = Image.new("RGBA", (220, 220), (0, 0, 0, 0)); ImageDraw.Draw(b5).ellipse((0, 0, 219, 219), fill=RED)
        n5 = text_sprite("۵", fa("Black", 150), WHITE, rtl=True); b5.alpha_composite(n5, ((220 - n5.width) // 2, (220 - n5.height) // 2 - 10))
        els.append(El(shadowed(b5), cx, 470, 0.05, i_end, anim="pop", anchor="c", dur=0.5))
        els.append(El(text_sprite(cfg["title1"], fa("Black", 84), WHITE, rtl=True), cx, 760, 0.3, i_end, anchor="c"))
        els.append(El(text_sprite(cfg["title2"], fa("Black", 84), GOLD, rtl=True), cx, 870, 0.6, i_end, anchor="c"))
        # word scenes
        for i, wd in enumerate(words):
            t0 = gw[i] - 0.12
            t1 = (gw[i + 1] if i < 4 else p_out) - 0.3
            els.append(El(dots(i), cx, 330, t0 - 0.1, t1, anim="fade", anchor="c", dur=0.25))
            els.append(El(word_card(wd), cx, 420, t0, t1, anim="pop", anchor="c", dur=0.45))
            pm = S[2 + 3 * i]["t"][0]
            els.append(El(text_sprite(wd["fa"], fa("Black", 70), WHITE, rtl=True), cx, 900, pm + 0.05, t1, anim="up", anchor="c"))
            if wd.get("fa_sub"):
                els.append(El(text_sprite(wd["fa_sub"], fa("Medium", 40), SOFT, rtl=True), cx, 995, pm + 0.6, t1, anim="up", anchor="c"))
            gs = S[3 + 3 * i]["t"][0]
            els.append(El(sentence_card(wd), cx, 1075, gs - 0.12, t1, anim="pop", anchor="c", dur=0.4))
        # outro recap
        t2 = p_out
        els.append(El(text_sprite("مرور کن و سیو کن", fa("Black", 70), WHITE, rtl=True), cx, 330, t2, anim="up", anchor="c"))
        for i, wd in enumerate(words):
            row = rounded(900, 120, 30, WHITE)
            f_ = text_sprite(wd["fa"], fa("Bold", 40), (90, 105, 130), rtl=True)
            sz = 50
            while True:
                a = text_sprite(wd["article"], la("Black", sz), ART[wd["article"]]); w_ = text_sprite(wd["word"], la("Black", sz), NAVY)
                if 40 + a.width + 14 + w_.width + 30 <= 900 - 40 - f_.width or sz <= 28: break
                sz -= 2
            row.alpha_composite(a, (40, (120 - a.height) // 2)); row.alpha_composite(w_, (40 + a.width + 14, (120 - w_.height) // 2))
            row.alpha_composite(f_, (900 - 40 - f_.width, (120 - f_.height) // 2))
            els.append(El(shadowed(row), 90, 450 + i * 140, t2 + 0.25 + i * 0.12, anim="right", dur=0.4))
        t_f = t2 + 1.4
        btn = rounded(620, 120, 60, RED); bs = text_sprite("فالو کن · هر روز ۵ کلمه", fa("Black", 46), WHITE, rtl=True)
        btn.alpha_composite(bs, ((620 - bs.width) // 2, (120 - bs.height) // 2 - 3)); btn = shadowed(btn)
        def follow(frame, t):
            if t < t_f: return
            p = t - t_f; s = (0.6 + 0.4 * ease_back(p / 0.45)) * (1 + 0.03 * math.sin(max(0, p - 0.45) * 6.0))
            img = btn.resize((int(btn.width * s), int(btn.height * s)), Image.BILINEAR); o = ease_out(p / 0.25)
            if o < 1: img.putalpha(img.getchannel("A").point(lambda a: int(a * o)))
            frame.alpha_composite(img, (cx - img.width // 2, 1180 + btn.height // 2 - img.height // 2))
        els.append(Dyn(follow))
        return els
    return build

if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1])); T = json.load(open(sys.argv[2]))
    R.build = build_for(cfg)
    tt = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")] if "--frames" in sys.argv else None
    R.render(T, sys.argv[3], sys.argv[4], tt)

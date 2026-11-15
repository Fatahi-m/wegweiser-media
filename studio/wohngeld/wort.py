#!/usr/bin/env python3
"""Wort des Tages quick reel. usage: wort.py config.json timings.json audio out.mp4 [--frames ...]
config: {"n":1,"article":"der","word":"Termin","plural":"die Termine","pron":"تِرمین","fa":"وقت ملاقات","fa_sub":"مثلاً وقت دکتر یا اداره",
         "sentence":"Ich möchte einen Termin vereinbaren.","sentence_fa":"می‌خوام یه وقت بگیرم."}"""
import sys, json, math
sys.path.insert(0, "/home/claude/wegweiser/tax2")
import render as R
from render import (El, Dyn, text_sprite, chip, rounded, shadowed, fa, la, ease_out, ease_back,
                    W, H, NAVY, NAVY_D, CARD, RED, WHITE, SOFT, GOLD, GREEN, FAD, Image, ImageDraw, D, M)
ART = {"der": (37, 99, 235), "die": (226, 35, 26), "das": (22, 163, 74)}

def word_card(cfg, w=940):
    col = ART[cfg["article"]]
    art = text_sprite(cfg["article"], la("Black", 78), col)
    wf = la("Black", 132)
    while text_size_w(cfg["word"], wf) > w - 120: wf = la("Black", wf.size - 6)
    wd = text_sprite(cfg["word"], wf, NAVY)
    pl = text_sprite("Plural: " + cfg["plural"], la("Medium", 38), (100, 115, 140)) if cfg.get("plural") else None
    pr = text_sprite("تلفظ: " + cfg["pron"], fa("Medium", 36), (100, 115, 140), rtl=True)
    h = 50 + art.height + wd.height + 30 + (pl.height if pl else 0) + 10 + pr.height + 50
    c = rounded(w, h, 44, WHITE); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, w - 1, 26), 13, fill=col); d.rectangle((0, 13, w - 1, 26), fill=WHITE)
    y = 50; c.alpha_composite(art, ((w - art.width) // 2, y)); y += art.height - 10
    c.alpha_composite(wd, ((w - wd.width) // 2, y)); y += wd.height + 30
    if pl: c.alpha_composite(pl, ((w - pl.width) // 2, y)); y += pl.height + 10
    c.alpha_composite(pr, ((w - pr.width) // 2, y))
    return shadowed(c)

def text_size_w(t, f):
    d = ImageDraw.Draw(Image.new("L", (1, 1))); b = d.textbbox((0, 0), t, font=f); return b[2] - b[0]

def wrap_lat(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if text_size_w(t, font) <= maxw: cur = t
        else: lines.append(cur); cur = wd
    lines.append(cur); return lines

def sentence_card(cfg, w=940):
    f = la("Bold", 58); lines = wrap_lat(cfg["sentence"], f, w - 120)
    sps = [text_sprite(l, f, WHITE) for l in lines]
    fs = text_sprite(cfg["sentence_fa"], fa("Bold", 46), GOLD, rtl=True)
    lab = chip("مثال", fa("Bold", 30), RED, WHITE)
    h = 40 + lab.height + 20 + sum(s.height for s in sps) + 20 + fs.height + 46
    c = rounded(w, h, 40, CARD); y = 40
    c.alpha_composite(lab, (w - 50 - lab.width, y)); y += lab.height + 20
    for s in sps: c.alpha_composite(s, ((w - s.width) // 2, y)); y += s.height
    y += 20; c.alpha_composite(fs, ((w - fs.width) // 2, y))
    return shadowed(c)

def build_for(cfg):
    def build(T):
        P, G = T["P"], T["G"]; cx = W // 2; els = []
        logo = Image.open(D + "/aof/wegweiser-deutschland-logo.png").convert("RGBA").resize((92, 92), Image.LANCZOS)
        mask = Image.new("L", (92, 92), 0); ImageDraw.Draw(mask).ellipse((0, 0, 91, 91), fill=255); logo.putalpha(mask)
        hdr = Image.new("RGBA", (W, 140), (0, 0, 0, 0)); hdr.alpha_composite(logo, (M, 24))
        hdr.alpha_composite(text_sprite("WEGWEISER", la("Black", 34), WHITE), (M + 112, 30))
        hdr.alpha_composite(text_sprite("DEUTSCHLAND", la("Medium", 26), SOFT), (M + 113, 74))
        tc = chip("کلمه‌ی روز · شماره‌ی " + str(cfg["n"]).translate(FAD), fa("Bold", 32), RED, WHITE); hdr.alpha_composite(tc, (W - M - tc.width, 46))
        els.append(El(hdr, 0, 90, 0.0, anim="fade", dur=0.3))
        els.append(El(text_sprite("کلمه‌ی آلمانیِ امروز", fa("Black", 64), SOFT, rtl=True), cx, 360, 0.05, anchor="c"))
        els.append(El(word_card(cfg), cx, 470, G[0][0] - 0.08, anim="pop", anchor="c", dur=0.5))
        mean = text_sprite(cfg["fa"], fa("Black", 72), WHITE, rtl=True)
        els.append(El(mean, cx, 930, P[1][0] + 0.05, anim="up", anchor="c"))
        els.append(El(text_sprite(cfg["fa_sub"], fa("Medium", 42), SOFT, rtl=True), cx, 1030, P[1][0] + 0.9, anim="up", anchor="c"))
        els.append(El(sentence_card(cfg), cx, 1110, G[1][0] - 0.1, anim="pop", anchor="c", dur=0.45))
        # tiny article legend
        leg = Image.new("RGBA", (700, 60), (0, 0, 0, 0)); x = 0
        for a in ("der", "die", "das"):
            s = text_sprite(a, la("Black", 34), ART[a]); bx = rounded(s.width + 36, 54, 27, WHITE); bx.alpha_composite(s, (18, (54 - s.height) // 2))
            leg.alpha_composite(bx, (x, 3)); x += bx.width + 14
        leg = leg.crop((0, 0, x - 14, 60))
        els.append(El(leg, cx, 1680, 0.4, anim="fade", anchor="c"))
        t_f = P[2][0] + 1.6
        btn = rounded(620, 120, 60, RED); bs = text_sprite("فالو کن · هر روز یک کلمه", fa("Black", 44), WHITE, rtl=True)
        btn.alpha_composite(bs, ((620 - bs.width) // 2, (120 - bs.height) // 2 - 3)); btn = shadowed(btn)
        def follow(frame, t):
            if t < t_f: return
            p = t - t_f; s = (0.6 + 0.4 * ease_back(p / 0.45)) * (1 + 0.03 * math.sin(max(0, p - 0.45) * 6.0))
            img = btn.resize((int(btn.width * s), int(btn.height * s)), Image.BILINEAR); o = ease_out(p / 0.25)
            if o < 1: img.putalpha(img.getchannel("A").point(lambda a: int(a * o)))
            frame.alpha_composite(img, (cx - img.width // 2, 1500 + btn.height // 2 - img.height // 2))
        els.append(Dyn(follow))
        return els
    return build

if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1])); T = json.load(open(sys.argv[2]))
    R.build = build_for(cfg)
    tt = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")] if "--frames" in sys.argv else None
    R.render(T, sys.argv[3], sys.argv[4], tt)

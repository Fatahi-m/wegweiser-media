#!/usr/bin/env python3
"""Data-driven Kurdish silent reel generator. Scenes are stacked & centred automatically; timing from reading length."""
import sys, math
sys.path.insert(0, "/home/claude/wegweiser/batch2")
from kbase import *
WHITE = (255, 255, 255)
TOP, BOT = 230, 1580

def ic_check(size=84):
    S = size * 4; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, S - 1, S - 1), fill=GREEN); d.line([(S * .27, S * .52), (S * .44, S * .69), (S * .74, S * .34)], fill=WHITE, width=int(S * .1), joint="curve")
    return im.resize((size, size), Image.LANCZOS)
def ic_cross(size=84):
    S = size * 4; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = int(S * .1)
    d.ellipse((0, 0, S - 1, S - 1), fill=KRED); d.line([(S * .32, S * .32), (S * .68, S * .68)], fill=WHITE, width=w); d.line([(S * .68, S * .32), (S * .32, S * .68)], fill=WHITE, width=w)
    return im.resize((size, size), Image.LANCZOS)
def ic_info(size=84):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse((0, 0, size - 1, size - 1), fill=SUN)
    t = text_sprite("i", la("Black", int(size * .62)), INK); im.alpha_composite(t, ((size - t.width) // 2, (size - t.height) // 2 - 3)); return im
ICONS = {"ok": ic_check, "no": ic_cross, "info": ic_info}

def passport(size=230):
    S = size * 2; h = int(S * 1.36); im = Image.new("RGBA", (S, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, S - 1, h - 1), int(S * .07), fill=(122, 24, 38))
    d.rounded_rectangle((int(S * .06), int(S * .05), S - 1 - int(S * .06), h - 1 - int(S * .05)), int(S * .05), outline=(214, 172, 80), width=6)
    t1 = text_sprite("REISEPASS", la("Bold", int(S * .1)), (232, 196, 110)); im.alpha_composite(t1, ((S - t1.width) // 2, int(h * .12)))
    r = int(S * .2); c0 = (S // 2, int(h * .5)); d.ellipse((c0[0] - r, c0[1] - r, c0[0] + r, c0[1] + r), outline=(232, 196, 110), width=10)
    d.polygon([(c0[0], c0[1] - r * .6), (c0[0] + r * .45, c0[1] + r * .5), (c0[0] - r * .45, c0[1] + r * .5)], fill=(232, 196, 110))
    t2 = text_sprite("DEUTSCHLAND", la("Bold", int(S * .085)), (232, 196, 110)); im.alpha_composite(t2, ((S - t2.width) // 2, int(h * .78)))
    return shadowed(im.resize((size, int(size * 1.36)), Image.LANCZOS), alpha=60)

def tile(top, bottom, w=400, h=270):
    c = rounded(w, h, 34, GREEN)
    a = text_sprite(top, fa("Black", 92), SUN, rtl=True); c.alpha_composite(a, ((w - a.width) // 2, 40))
    b = text_sprite(bottom, fa("Bold", 42), WHITE, rtl=True); c.alpha_composite(b, ((w - b.width) // 2, 50 + a.height))
    return shadowed(c, alpha=50)

def step_img(n, text):
    b = knum(n, 104); tx = fitT(text, 62, W - 300)
    im = Image.new("RGBA", (b.width + 24 + tx.width, 130), (0, 0, 0, 0))
    im.alpha_composite(tx, (0, (130 - tx.height) // 2)); im.alpha_composite(b, (tx.width + 24, 13)); return im

def big_euro(s, col=GREEN, size=190):
    return text_sprite(s, la("Black", size), col)

def make_item(it):
    k = it[0]
    if k == "title": return fitT(it[1], it[2] if len(it) > 2 else 80, 960, it[3] if len(it) > 3 else INK), "c"
    if k == "text": return fitT(it[1], it[2] if len(it) > 2 else 54, 960, it[3] if len(it) > 3 else INK, "Bold"), "c"
    if k == "small": return fitT(it[1], 38, 960, MUTED, "Medium"), "c"
    if k == "card": return kcard(it[1], it[2]), "c"
    if k == "chip": return kchip(it[1], it[2], it[3], it[4] if len(it) > 4 else 44, latin=it[5] if len(it) > 5 else False), "c"
    if k == "row": return krow(it[1], n=it[2] if isinstance(it[2], int) else None, sub=it[3] if len(it) > 3 else None, h=160,
                               icon=None if isinstance(it[2], int) else ICONS[it[2]]()), "row"
    if k == "big": return big_euro(it[1], it[2] if len(it) > 2 else GREEN, it[3] if len(it) > 3 else 190), "c"
    if k == "bigfa": return T(it[1], it[3] if len(it) > 3 else 150, it[2] if len(it) > 2 else GREEN), "c"
    if k == "step": return step_img(it[1], it[2]), "c"
    if k == "passport": return passport(), "c"
    if k == "sun": return sun(it[1] if len(it) > 1 else 200), "c"
    if k == "tiles":
        ts = [tile(a, b) for a, b in it[1]]; gap = 10
        im = Image.new("RGBA", (sum(t.width for t in ts) + gap * (len(ts) - 1), max(t.height for t in ts)), (0, 0, 0, 0)); x = im.width
        for t in ts: x -= t.width; im.alpha_composite(t, (x, 0)); x -= gap      # RTL: first tile on the right
        return im, "c"
    if k == "months":
        names = it[1]; im = Image.new("RGBA", (len(names) * 225, 230), (0, 0, 0, 0))
        for i, m in enumerate(names):
            b = rounded(205, 210, 28, PAPER, outline=GREEN, ow=5); bd = ImageDraw.Draw(b)
            bd.rounded_rectangle((0, 0, 204, 50), 28, fill=GREEN); bd.rectangle((0, 25, 204, 50), fill=GREEN)
            ms = text_sprite(m, la("Black", 54), INK); b.alpha_composite(ms, ((205 - ms.width) // 2, 95)); im.alpha_composite(b, (i * 225, 10))
        return im, "c"
    if k == "img": return it[1], "c"
    raise ValueError(k)

def read_time(it):
    if it[0] == "img": return it[2] if len(it) > 2 else 2.5
    s = " ".join(str(x) for x in it[1:] if isinstance(x, str))
    return 0.55 + min(2.6, len(s) / 22)

def build_reel(spec):
    """spec = {"topic":..,"footer":..,"scenes":[[items...],...],"outro":(line1,line2)}"""
    els = [header(spec["topic"]), footer(spec["footer"])] + ([source_line(spec["source"])] if spec.get("source") else [])
    t = 0.15; strikes = []; TM = spec.get("timing")
    for si, sc in enumerate(spec["scenes"]):
        made = [make_item(it) for it in sc]
        gap = 34; H_tot = sum(m[0].height for m in made) + gap * (len(made) - 1)
        y = TOP + max(0, (BOT - TOP - H_tot) // 2)
        times = []; tt = t
        for k, ((img, mode), it) in enumerate(zip(made, sc)):
            if TM: tt = TM[si][0][k]
            times.append((img, mode, y, tt, it)); y += img.height + gap; tt += read_time(it)
        end = TM[si][1] if TM else tt + 1.4
        for img, mode, yy, ti, it in times:
            x = 80 if mode == "row" else cx
            anim = "pop" if it[0] in ("card", "chip", "big", "bigfa", "step", "tiles", "passport", "sun") else ("right" if mode == "row" else "up")
            els.append(El(img, x, yy, ti, end, anim=anim, anchor="c" if mode == "c" else "tl", dur=0.45))
            if it[0] == "months": strikes.append((cx - img.width // 2, yy, ti + 1.2, end, len(it[1])))
        t = end + 0.35
    for x0, y0, ts, te, n in strikes:
        def strike(frame, tm, x0=x0, y0=y0, ts=ts, te=te):
            if tm < ts or tm > te + 0.3: return
            d = ImageDraw.Draw(frame)
            for i in range(2):
                p = ease_out((tm - ts - i * 0.35) / 0.35)
                if p <= 0: continue
                xa = x0 + i * 225 + 20; ya = y0 + 40
                d.line([(xa, ya), (xa + 165 * p, ya + 170 * p)], fill=KRED, width=14)
        els.append(Dyn(strike))
    # outro
    t2 = spec.get("outro_t", t)
    l1, l2 = spec["outro"]
    o = [(sun(200), 0.0), (T(l1, 84), 0.2), (fitT(l2, 56, 900, GREEN, "Bold"), 0.5)]
    y = 520
    for img, dt in o:
        els.append(El(img, cx, y, t2 + dt, anim="pop" if dt == 0 else "up", anchor="c")); y += img.height + 30
    els.append(follow_btn(t2 + 1.1, y + 40))
    return els, spec.get("total", t2 + 4.2)

if __name__ == "__main__":
    import json, importlib
    mod = importlib.import_module(sys.argv[1]); spec = mod.SPEC
    els, total = build_reel(spec)
    tt = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")] if "--frames" in sys.argv else None
    if "--times" in sys.argv: print(round(total, 1)); sys.exit()
    render(lambda: els, total, sys.argv[2], sys.argv[3], tt)

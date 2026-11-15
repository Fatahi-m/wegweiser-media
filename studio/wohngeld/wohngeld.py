#!/usr/bin/env python3
"""Wohngeld Reel renderer (Wegweiser style). usage: wohngeld.py timings.json audio out.mp4 [--frames ...]"""
import sys, json, math
sys.path.insert(0, "/home/claude/wegweiser/tax2")
import render as R
from render import (El, Dyn, text_sprite, chip, rounded, shadowed, german_card, fa, la, ease_out, ease_back,
                    W, H, NAVY, NAVY_D, CARD, RED, WHITE, SOFT, GOLD, GREEN, FAD, Image, ImageDraw, D, M)

def icon_check(size, col=GREEN, fg=NAVY_D):
    S = size * 4; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, S - 1, S - 1), fill=col)
    d.line([(S * .27, S * .52), (S * .44, S * .69), (S * .74, S * .34)], fill=fg, width=int(S * .1), joint="curve")
    return im.resize((size, size), Image.LANCZOS)

def icon_cross(size, col=RED, fg=WHITE):
    S = size * 4; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, S - 1, S - 1), fill=col); w = int(S * .1)
    d.line([(S * .32, S * .32), (S * .68, S * .68)], fill=fg, width=w); d.line([(S * .68, S * .32), (S * .32, S * .68)], fill=fg, width=w)
    return im.resize((size, size), Image.LANCZOS)

def icon_house(size):
    S = size * 4; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(S * .5, S * .06), (S * .96, S * .46), (S * .04, S * .46)], fill=RED)
    d.rounded_rectangle((S * .14, S * .42, S * .86, S * .95), radius=int(S * .05), fill=WHITE)
    e = text_sprite("€", la("Black", int(S * .42)), NAVY)
    im.alpha_composite(e, (int(S * .5 - e.width / 2), int(S * .68 - e.height / 2)))
    return im.resize((size, size), Image.LANCZOS)

def row(text, icon, w=920, h=150, bg=CARD, fg=WHITE, size=50, sub=None):
    c = rounded(w, h, 34, bg)
    ic = icon(78); c.alpha_composite(ic, (w - 40 - 78, (h - 78) // 2))
    ts = text_sprite(text, fa("Bold", size), fg, rtl=True)
    if sub:
        ss = text_sprite(sub, la("Bold", 40), GOLD)
        top = (h - ts.height - ss.height + 4) // 2
        c.alpha_composite(ts, (w - 140 - ts.width, top)); c.alpha_composite(ss, (w - 140 - ss.width, top + ts.height - 4))
    else:
        c.alpha_composite(ts, (w - 140 - ts.width, (h - ts.height) // 2))
    return shadowed(c)

def num_icon(n):
    def f(size):
        S = size; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse((0, 0, S - 1, S - 1), fill=RED)
        t = text_sprite(str(n).translate(FAD), fa("Black", int(S * .55)), WHITE, rtl=True)
        im.alpha_composite(t, ((S - t.width) // 2, (S - t.height) // 2 - 3)); return im
    return f

def build(T):
    P, G, PS = T["P"], T["G"], T.get("pauses", [[] for _ in range(5)])
    def at(i, frac):
        est = P[i][0] + frac * (P[i][1] - P[i][0])
        if not PS[i]: return est
        a, b = min(PS[i], key=lambda p: abs((p[0] + p[1]) / 2 - est))
        return b if abs((a + b) / 2 - est) < 1.4 else est
    cx = W // 2; els = []
    # header
    logo = Image.open(D + "/aof/wegweiser-deutschland-logo.png").convert("RGBA").resize((92, 92), Image.LANCZOS)
    mask = Image.new("L", (92, 92), 0); ImageDraw.Draw(mask).ellipse((0, 0, 91, 91), fill=255); logo.putalpha(mask)
    hdr = Image.new("RGBA", (W, 140), (0, 0, 0, 0)); hdr.alpha_composite(logo, (M, 24))
    hdr.alpha_composite(text_sprite("WEGWEISER", la("Black", 34), WHITE), (M + 112, 30))
    hdr.alpha_composite(text_sprite("DEUTSCHLAND", la("Medium", 26), SOFT), (M + 113, 74))
    tc = chip("کمک‌هزینه‌ی کرایه", fa("Bold", 32), RED, WHITE); hdr.alpha_composite(tc, (W - M - tc.width, 46))
    els.append(El(hdr, 0, 90, 0.0, anim="fade", dur=0.4))
    disc = text_sprite("اطلاعات عمومی · وضعیت اکتبر ۲۰۲۶ · منبع: service.berlin.de", fa("Medium", 28), (150, 170, 200), rtl=True)
    els.append(El(disc, cx, 1640, 0.3, anim="fade", anchor="c"))

    # ---- Scene A: hook ----
    a_end = at(1, 0.353) - 0.3
    els.append(El(shadowed(icon_house(260)), cx, 400, 0.05, a_end, anim="pop", anchor="c", dur=0.5))
    els.append(El(text_sprite("کار می‌کنی، ولی", fa("Black", 74), SOFT, rtl=True), cx, 720, 0.2, a_end, anchor="c"))
    els.append(El(text_sprite("کرایه کمرت رو شکسته؟", fa("Black", 84), WHITE, rtl=True), cx, 825, 0.7, a_end, anchor="c"))
    card, badge = german_card("Wohngeld", "کمک‌هزینه‌ی کرایه از دولت")
    els.append(El(card, cx, 1030, G[0][0] - 0.05, a_end, anim="pop", anchor="c", dur=0.5))
    els.append(El(badge, cx, 1000, G[0][0] + 0.1, a_end, anim="pop", anchor="c", dur=0.4))
    els.append(El(chip("حق قانونی توئه، ولی خودکار نیست!", fa("Bold", 42), GOLD, NAVY_D), cx, 1400, P[1][0] + 0.2, a_end, anim="up", anchor="c"))

    # ---- Scene B: who ----
    b_end = at(2, 0.506) - 0.3
    els.append(El(text_sprite("به کی تعلق می‌گیره؟", fa("Black", 76), WHITE, rtl=True), cx, 450, a_end + 0.3, b_end, anchor="c"))
    els.append(El(row("کار می‌کنی، ولی درآمدت کمه", icon_check), 80, 620, a_end + 0.5, b_end, anim="right"))
    els.append(El(row("حقوق بازنشستگی کم می‌گیری", icon_check), 80, 800, at(1, 0.55), b_end, anim="right"))
    els.append(El(row("هم‌زمان نباید این رو بگیری:", icon_cross, sub="Grundsicherung"), 80, 980, G[1][0] - 0.05, b_end, anim="pop", dur=0.4))
    els.append(El(row("کمک‌هزینه‌ی بچه جزو درآمد نیست", icon_check, sub="Kindergeld"), 80, 1160, at(2, 0.253), b_end, anim="right"))

    # ---- Scene C: documents ----
    c_end = at(3, 0.588) - 0.15
    els.append(El(text_sprite("مدارک لازم", fa("Black", 80), WHITE, rtl=True), cx, 450, b_end + 0.3, c_end, anchor="c"))
    docs = [("کارت شناسایی و اجازه‌ی اقامت", None, at(2, 0.718)), ("قرارداد اجاره", "Mietvertrag", G[2][0] - 0.05),
            ("فیش حقوقی", None, P[3][0] + 0.1), ("رسید کرایه‌ی ۳ ماه آخر", None, at(3, 0.221))]
    for i, (t, de, t0) in enumerate(docs):
        els.append(El(row(t, num_icon(i + 1), sub=de), 80, 620 + i * 180, t0, c_end, anim="pop" if de else "right"))
    # Rechner card (own mini-scene)
    d_end = at(4, 0.068) + 1.6
    rc, rb = german_card("Wohngeldrechner", "ماشین‌حساب رسمی کمک‌هزینه")
    els.append(El(text_sprite("اول حساب کن چقدر بهت می‌رسه", fa("Black", 62), WHITE, rtl=True), cx, 700, at(3, 0.588) + 0.25, d_end, anchor="c"))
    els.append(El(rc, cx, 900, G[3][0] - 0.05, d_end, anim="pop", anchor="c", dur=0.5))
    els.append(El(rb, cx, 870, G[3][0] + 0.1, d_end, anim="pop", anchor="c", dur=0.4))

    # ---- Scene D: key rule + months ----
    e_end = at(4, 0.418) - 0.3
    t0 = d_end + 0.3
    els.append(El(chip("نکته‌ی خیلی مهم", fa("Black", 46), RED, WHITE), cx, 470, t0, e_end, anim="pop", anchor="c"))
    els.append(El(text_sprite("پول فقط از ماهِ درخواست", fa("Black", 70), WHITE, rtl=True), cx, 590, t0 + 0.3, e_end, anchor="c"))
    els.append(El(text_sprite("پرداخت می‌شه، نه زودتر!", fa("Black", 70), GOLD, rtl=True), cx, 690, t0 + 0.8, e_end, anchor="c"))
    months = ["Okt", "Nov", "Dez", "Jan"]
    t_m = at(4, 0.301)
    for i, mname in enumerate(months):
        x = 120 + i * 220
        box = rounded(200, 210, 30, CARD, outline=(70, 120, 190), ow=3)
        bd = ImageDraw.Draw(box); bd.rounded_rectangle((0, 0, 199, 50), 30, fill=RED); bd.rectangle((0, 25, 199, 50), fill=RED)
        ms = text_sprite(mname, la("Black", 54), WHITE); box.alpha_composite(ms, ((200 - ms.width) // 2, 90))
        els.append(El(shadowed(box), x, 900, t0 + 1.2 + i * 0.15, e_end, anim="pop", dur=0.4))
    # cross out first two months when "every month you wait" is said
    def strike(frame, t):
        if t < t_m or t > e_end + 0.35: return
        d = ImageDraw.Draw(frame)
        for i in range(2):
            p = ease_out((t - t_m - i * 0.35) / 0.35)
            if p <= 0: continue
            x0, y0 = 120 + i * 220 + 20, 930; x1, y1 = x0 + 160 * p, y0 + 150 * p
            d.line([(x0, y0), (x1, y1)], fill=RED, width=14)
        p = ease_out((t - t_m - 0.8) / 0.4)
        if p > 0:
            s = text_sprite("پولِ از دست رفته", fa("Bold", 44), RED, rtl=True)
            s.putalpha(s.getchannel("A").point(lambda a: int(a * p)))
            frame.alpha_composite(s, (120 + 210 - s.width // 2, 1160))
            s2 = text_sprite("همین الان درخواست بده", fa("Bold", 44), GREEN, rtl=True)
            s2.putalpha(s2.getchannel("A").point(lambda a: int(a * p)))
            frame.alpha_composite(s2, (120 + 2 * 220 + 210 - s2.width // 2, 1160))
    els.append(Dyn(strike))

    # ---- Scene E: facts + 2027 ----
    f_end = at(4, 0.805) - 0.3
    t1 = e_end + 0.3
    els.append(El(text_sprite("بدونی بهتره", fa("Black", 76), WHITE, rtl=True), cx, 500, t1, f_end, anchor="c"))
    facts = [("برلین: درخواست آنلاین و رایگان", icon_check, at(4, 0.418)),
             ("بعد از ۱۲ ماه باید تمدید کنی", num_icon(12), at(4, 0.534)),
             ("۲۰۲۷: دولت می‌خواد کمش کنه", icon_cross, at(4, 0.628))]
    for i, (t, ic, tt) in enumerate(facts):
        els.append(El(row(t, ic), 80, 650 + i * 180, tt, f_end, anim="right"))
    els.append(El(text_sprite("طرح دولت هنوز قانون نشده · تصمیم‌های فعلی تا آخر مدت معتبرن", fa("Medium", 32), SOFT, rtl=True),
                  cx, 1230, at(4, 0.628) + 0.6, f_end, anim="fade", anchor="c"))

    # ---- Scene F: outro (no pause) ----
    t2 = f_end + 0.3
    els.append(El(chip("ویدیوی بعدی", fa("Black", 44), GOLD, NAVY_D), cx, 480, t2, anim="pop", anchor="c"))
    kc, kb = german_card("Kindergeld", "کمک‌هزینه‌ی بچه")
    els.append(El(kc, cx, 620, t2 + 0.3, anim="pop", anchor="c", dur=0.5))
    btn = rounded(560, 130, 65, RED); bs = text_sprite("فالو کن", fa("Black", 60), WHITE, rtl=True)
    btn.alpha_composite(bs, ((560 - bs.width) // 2, (130 - bs.height) // 2 - 4)); btn = shadowed(btn)
    t_f = t2 + 1.2
    def follow(frame, t):
        if t < t_f: return
        p = t - t_f
        s = (0.6 + 0.4 * ease_back(p / 0.45)) * (1 + 0.035 * math.sin(max(0, p - 0.45) * 6.0))
        img = btn.resize((int(btn.width * s), int(btn.height * s)), Image.BILINEAR)
        o = ease_out(p / 0.25)
        if o < 1: img.putalpha(img.getchannel("A").point(lambda a: int(a * o)))
        frame.alpha_composite(img, (cx - img.width // 2, 1080 + btn.height // 2 - img.height // 2))
    els.append(Dyn(follow))
    els.append(El(text_sprite("@wegweiser.deutschland", la("Bold", 40), SOFT), cx, 1280, t_f + 0.3, anim="fade", anchor="c"))
    return els

R.build = build
if __name__ == "__main__":
    T = json.load(open(sys.argv[1]))
    tt = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")] if "--frames" in sys.argv else None
    R.render(T, sys.argv[2], sys.argv[3], tt)

#!/usr/bin/env python3
"""Generic Wegweiser fact reel. usage: reel.py K|E|N timings.json audio out.mp4 [--frames ...]"""
import sys, json, math
sys.path.insert(0, "/home/claude/wegweiser/tax2")
sys.path.insert(0, "/home/claude/wegweiser/wohngeld")
import render as R
from render import (El, Dyn, text_sprite, chip, rounded, shadowed, german_card, fa, la, ease_out, ease_back,
                    W, H, NAVY, NAVY_D, CARD, RED, WHITE, SOFT, GOLD, GREEN, FAD, Image, ImageDraw, D, M)
from wohngeld import icon_check, icon_cross, num_icon
from render import text_size
OFF = 150

def row(text, icon, w=920, h=150, bg=CARD, fg=WHITE, size=50, sub=None):
    c = rounded(w, h, 34, bg)
    ic = icon(78); c.alpha_composite(ic, (w - 40 - 78, (h - 78) // 2))
    maxw = w - 140 - 40
    f = fa("Bold", size)
    while text_size(text, f, rtl=True)[0][2] > maxw and f.size > 30: f = fa("Bold", f.size - 2)
    ts = text_sprite(text, f, fg, rtl=True)
    if sub:
        sf = la("Bold", 40)
        while text_size(sub, sf)[0][2] > maxw and sf.size > 24: sf = la("Bold", sf.size - 2)
        ss = text_sprite(sub, sf, GOLD)
        top = (h - ts.height - ss.height + 4) // 2
        c.alpha_composite(ts, (w - 140 - ts.width, top)); c.alpha_composite(ss, (w - 140 - ss.width, top + ts.height - 4))
    else:
        c.alpha_composite(ts, (w - 140 - ts.width, (h - ts.height) // 2))
    return shadowed(c)

def euro(num, col=GOLD, size=200):
    n = text_sprite(num, fa("Black", size), col, rtl=True); e = text_sprite("€", la("Black", int(size * .8)), col)
    im = Image.new("RGBA", (n.width + e.width + 10, max(n.height, e.height)), (0, 0, 0, 0))
    im.alpha_composite(n, (0, (im.height - n.height) // 2)); im.alpha_composite(e, (n.width + 10, (im.height - e.height) // 2 + 6))
    return im


cx = W // 2

def header(label):
    logo = Image.open(D + "/brand/compass-fa.png").convert("RGBA").resize((92, 92), Image.LANCZOS)
    mask = Image.new("L", (92, 92), 0); ImageDraw.Draw(mask).ellipse((0, 0, 91, 91), fill=255); logo.putalpha(mask)
    hdr = Image.new("RGBA", (W, 140), (0, 0, 0, 0)); hdr.alpha_composite(logo, (M, 24))
    hdr.alpha_composite(text_sprite("WEGWEISER", la("Black", 34), WHITE), (M + 112, 30))
    hdr.alpha_composite(text_sprite("FARSI", la("Medium", 26), SOFT), (M + 113, 74))
    tc = chip(label, fa("Bold", 32), RED, WHITE); hdr.alpha_composite(tc, (W - M - tc.width, 46))
    return El(hdr, 0, 90, 0.0, anim="fade", dur=0.4)

def T_(s, size=76, col=WHITE, w="Black"): return text_sprite(s, fa(w, size), col, rtl=True)

def big(s, col=GOLD, size=200):
    """big number/latin string with optional Persian digits"""
    return text_sprite(s, fa("Black", size), col, rtl=True)

def info_icon(size):
    S = size * 4; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, S - 1, S - 1), fill=GOLD)
    t = text_sprite("i", la("Black", int(S * .62)), NAVY_D); im.alpha_composite(t, ((S - t.width) // 2, (S - t.height) // 2 - 4))
    return im.resize((size, size), Image.LANCZOS)

def step_badge(n, label):
    b = Image.new("RGBA", (150, 150), (0, 0, 0, 0)); ImageDraw.Draw(b).ellipse((0, 0, 149, 149), fill=RED)
    t = text_sprite(str(n).translate(FAD), fa("Black", 96), WHITE, rtl=True); b.alpha_composite(t, ((150 - t.width) // 2, (150 - t.height) // 2 - 8))
    return shadowed(b)

def passport(size=300):
    S = size * 2; h = int(S * 1.36)
    im = Image.new("RGBA", (S, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, S - 1, h - 1), int(S * .07), fill=(122, 24, 38))
    d.rounded_rectangle((int(S * .06), int(S * .05), S - 1 - int(S * .06), h - 1 - int(S * .05)), int(S * .05), outline=(214, 172, 80), width=6)
    t1 = text_sprite("REISEPASS", la("Bold", int(S * .1)), (232, 196, 110)); im.alpha_composite(t1, ((S - t1.width) // 2, int(h * .12)))
    r = int(S * .2); c0 = (S // 2, int(h * .5))
    d.ellipse((c0[0] - r, c0[1] - r, c0[0] + r, c0[1] + r), outline=(232, 196, 110), width=10)
    d.polygon([(c0[0], c0[1] - r * .6), (c0[0] + r * .45, c0[1] + r * .5), (c0[0] - r * .45, c0[1] + r * .5)], fill=(232, 196, 110))
    t2 = text_sprite("FARSI", la("Bold", int(S * .085)), (232, 196, 110)); im.alpha_composite(t2, ((S - t2.width) // 2, int(h * .78)))
    return shadowed(im.resize((size, int(size * 1.36)), Image.LANCZOS))

def tile(top, bottom, w=400, h=300, col=CARD, topcol=GOLD):
    c = rounded(w, h, 36, col)
    a = text_sprite(top, fa("Black", 96), topcol, rtl=True); c.alpha_composite(a, ((w - a.width) // 2, 50))
    b = text_sprite(bottom, fa("Bold", 44), WHITE, rtl=True); c.alpha_composite(b, ((w - b.width) // 2, 60 + a.height))
    return shadowed(c)

def follow_btn(els, t_f, y=1080, label="فالو کن"):
    btn = rounded(560, 130, 65, RED); bs = text_sprite(label, fa("Black", 60), WHITE, rtl=True)
    btn.alpha_composite(bs, ((560 - bs.width) // 2, (130 - bs.height) // 2 - 4)); btn = shadowed(btn)
    def follow(frame, t):
        if t < t_f: return
        p = t - t_f
        s = (0.6 + 0.4 * ease_back(p / 0.45)) * (1 + 0.035 * math.sin(max(0, p - 0.45) * 6.0))
        img = btn.resize((int(btn.width * s), int(btn.height * s)), Image.BILINEAR)
        o = ease_out(p / 0.25)
        if o < 1: img.putalpha(img.getchannel("A").point(lambda a: int(a * o)))
        frame.alpha_composite(img, (cx - img.width // 2, y + btn.height // 2 - img.height // 2))
    els.append(Dyn(follow))
    els.append(El(text_sprite("@wegweiser_farsi", la("Bold", 40), SOFT), cx, y + 200, t_f + 0.3, anim="fade", anchor="c"))

def outro(els, t2, line1, line2, icon_txt="📌"):
    els.append(El(T_(line1, 80), cx, 520, t2, anim="up", anchor="c"))
    sz = 60
    while text_size(line2, fa("Bold", sz), rtl=True)[0][2] > 940: sz -= 2
    els.append(El(T_(line2, sz, GOLD, "Bold"), cx, 640, t2 + 0.35, anim="up", anchor="c"))
    s1 = chip("سیو کن", fa("Black", 50), GOLD, NAVY_D); s2 = chip("بفرست برای دوستت", fa("Black", 50), CARD, WHITE)
    els.append(El(s1, cx + 30, 800, t2 + 0.6, anim="pop", anchor="tl"))
    els.append(El(s2, cx - 30 - s2.width, 800, t2 + 0.8, anim="pop", anchor="tl"))
    follow_btn(els, t2 + 1.4, y=1000 + OFF)

# --------------------------------------------------------------------------------------------
def make(T, key):
    S = T["segs"]
    st = lambda i: S[i]["t"][0]
    def at(i, frac):
        a, b = S[i]["t"]; est = a + frac * (b - a)
        ps = S[i].get("pauses") or []
        if not ps or frac <= 0: return est
        p0, p1 = min(ps, key=lambda p: abs((p[0] + p[1]) / 2 - est))
        return p1 if abs((p0 + p1) / 2 - est) < 1.2 else est
    end = lambda i: st(i) - 0.3          # scene that ends when segment i starts
    TW = tile('x','y').width
    els = []
    disc = T_("اطلاعات عمومی · وضعیت اکتبر ۲۰۲۶ · جای مشاوره‌ی رسمی نیست", 28, (150, 170, 200), "Medium")
    els.append(El(disc, cx, 1640, 0.3, anim="fade", anchor="c"))

    if key == "K":
        els.insert(0, header("کمک‌هزینه‌ی بچه"))
        e = end(3)
        els.append(El(T_("این پول رو", 80, SOFT), cx, 380, 0.05, e, anchor="c"))
        els.append(El(T_("همه می‌شناسن...", 90), cx, 480, 0.35, e, anchor="c"))
        els.append(El(chip("ولی این یکی رو چی؟", fa("Black", 54), RED, WHITE), cx, 610, st(2), e, anim="pop", anchor="c"))
        c, b = german_card("Kindergeld", "کمک‌هزینه‌ی بچه")
        els.append(El(c, cx, 820, st(1) - 0.05, e, anim="pop", anchor="c", dur=0.5)); els.append(El(b, cx, 790, st(1) + 0.1, e, anim="pop", anchor="c"))
        # B: Kindergeld facts
        e = end(7); t0 = st(3) - 0.05
        els.append(El(chip("۱ · Kindergeld", fa("Black", 44), GOLD, NAVY_D), cx, 330, t0, e, anim="pop", anchor="c"))
        els.append(El(euro("۲۵۹"), cx, 420, at(3, 0.55), e, anim="pop", anchor="c", dur=0.5))
        els.append(El(T_("در ماه برای هر بچه · ۲۰۲۶", 50, WHITE, "Bold"), cx, 690, at(3, 0.7), e, anchor="c"))
        c, b = german_card("Familienkasse", "اداره‌ی پرداخت کمک‌هزینه‌ی بچه")
        els.append(El(c, cx, 860, st(5) - 0.05, e, anim="pop", anchor="c", dur=0.5)); els.append(El(b, cx, 830, st(5) + 0.1, e, anim="pop", anchor="c"))
        els.append(El(row("حداکثر ۶ ماه عقب‌تر پرداخت می‌شه", num_icon(6)), 80, 1200, st(6), e, anim="right"))
        # C: Kinderzuschlag
        e = end(10); t0 = st(7) - 0.05
        els.append(El(chip("۲ · پولی که خیلیا نمی‌شناسن", fa("Black", 44), RED, WHITE), cx, 330, t0, e, anim="pop", anchor="c"))
        c, b = german_card("Kinderzuschlag", "کمک‌هزینه‌ی تکمیلی بچه")
        els.append(El(c, cx, 470, st(8) - 0.05, e, anim="pop", anchor="c", dur=0.5)); els.append(El(b, cx, 440, st(8) + 0.1, e, anim="pop", anchor="c"))
        els.append(El(T_("تا", 70, SOFT), cx, 800, st(9), e, anchor="c"))
        els.append(El(euro("۲۹۷"), cx, 860, at(9, 0.3), e, anim="pop", anchor="c", dur=0.5))
        els.append(El(T_("در ماه برای هر بچه", 52, WHITE, "Bold"), cx, 1120, at(9, 0.45), e, anchor="c"))
        els.append(El(chip("+ اضافه بر کمک‌هزینه‌ی بچه", fa("Black", 48), GREEN, NAVY_D), cx, 1220, at(9, 0.7), e, anim="pop", anchor="c"))
        # D: who
        e = end(13); t0 = st(10) - 0.05
        els.append(El(T_("به کی تعلق می‌گیره؟", 76), cx, 420, t0, e, anchor="c"))
        els.append(El(row("کار می‌کنی، ولی درآمد کافی نیست", icon_check), 80, 580, at(10, 0.15), e, anim="right"))
        els.append(El(row("زوج: حداقل ۹۰۰ € ناخالص", icon_check), 80, 760, st(11), e, anim="right"))
        els.append(El(row("والد تنها: حداقل ۶۰۰ € ناخالص", icon_check), 80, 940, at(11, 0.42), e, anim="right"))
        els.append(El(row("هم‌زمان با این نمی‌شه:", icon_cross, sub="Grundsicherungsgeld (früher Bürgergeld)"), 80, 1120, st(12) - 0.05, e, anim="pop"))
        # E: extras
        e = end(14); t0 = st(13) - 0.05
        els.append(El(T_("مزیت‌های اضافه", 80), cx, 420, t0, e, anchor="c"))
        els.append(El(chip("Bildung und Teilhabe", la("Bold", 38), CARD, GOLD, rtl=False), cx, 530, t0 + 0.3, e, anim="fade", anchor="c"))
        els.append(El(row("شهریه‌ی مهدکودک حذف می‌شه", icon_check, sub="Kita · § 90 SGB VIII"), 80, 640, at(13, 0.3), e, anim="right"))
        els.append(El(row("کمک برای مدرسه و اردو", icon_check), 80, 820, at(13, 0.6), e, anim="right"))
        els.append(El(row("کمک‌هزینه‌ی ناهار", icon_check), 80, 1000, at(13, 0.8), e, anim="right"))
        # F: warning
        e = end(15); t0 = st(14) - 0.05
        els.append(El(chip("نکته‌ی خیلی مهم", fa("Black", 50), RED, WHITE), cx, 420, t0, e, anim="pop", anchor="c"))
        els.append(El(T_("ماه‌های قبل از درخواست", 70), cx, 590, t0 + 0.4, e, anchor="c"))
        els.append(El(T_("پرداخت نمی‌شه!", 90, GOLD), cx, 700, t0 + 0.8, e, anchor="c"))
        els.append(El(row("همین ماه آنلاین درخواست بده", icon_check, sub="Familienkasse"), 80, 900, at(14, 0.55), e, anim="pop"))
        # G: outro
        outro(els, st(15) - 0.05, "این ویدیو رو سیو کن", "و برای خانواده‌های بچه‌دار بفرست")

    elif key == "E":
        els.insert(0, header("شهروندی آلمان"))
        e = end(2)
        els.append(El(passport(220), cx, 360, 0.05, e, anim="pop", anchor="c", dur=0.5))
        els.append(El(T_("پاسپورت آلمانی می‌خوای؟", 78), cx, 740, 0.25, e, anchor="c"))
        els.append(El(chip("۴ شرط اصلی", fa("Black", 52), GOLD, NAVY_D), cx, 860, at(0, 0.5), e, anim="pop", anchor="c"))
        c, b = german_card("Einbürgerung", "گرفتن شهروندی آلمان")
        els.append(El(c, cx, 1030, st(1) - 0.05, e, anim="pop", anchor="c", dur=0.5)); els.append(El(b, cx, 1000, st(1) + 0.1, e, anim="pop", anchor="c"))
        # 1
        e = end(3); t0 = st(2) - 0.05
        els.append(El(step_badge(1, ""), cx, 330, t0, e, anim="pop", anchor="c"))
        els.append(El(big("۵ سال"), cx, 470, t0 + 0.2, e, anim="pop", anchor="c"))
        els.append(El(T_("اقامت قانونی در آلمان", 60, WHITE, "Bold"), cx, 730, t0 + 0.6, e, anchor="c"))
        els.append(El(row("شهروندی ۳ ساله · از اکتبر ۲۰۲۵ حذف شد", icon_cross), 80, 900, at(2, 0.45), e, anim="pop"))
        # 2
        e = end(7); t0 = st(3) - 0.05
        els.append(El(step_badge(2, ""), cx, 330, t0, e, anim="pop", anchor="c"))
        els.append(El(T_("زبان آلمانی", 70, SOFT), cx, 470, t0 + 0.2, e, anchor="c"))
        els.append(El(text_sprite("B1", la("Black", 210), GOLD), cx, 600, st(4) - 0.05, e, anim="pop", anchor="c"))
        c, b = german_card("Einbürgerungstest", "تست شهروندی")
        els.append(El(c, cx, 960, st(6) - 0.05, e, anim="pop", anchor="c", dur=0.5)); els.append(El(b, cx, 930, st(6) + 0.1, e, anim="pop", anchor="c"))
        # 3
        e = end(10); t0 = st(7) - 0.05
        els.append(El(step_badge(3, ""), cx, 330, t0, e, anim="pop", anchor="c"))
        els.append(El(T_("خرج زندگی‌ت رو خودت بدی", 70), cx, 500, t0 + 0.2, e, anchor="c"))
        els.append(El(row("گرفتن این معمولاً مانعه:", icon_cross, sub="Grundsicherungsgeld (früher Bürgergeld)"), 80, 640, st(8) - 0.05, e, anim="pop"))
        els.append(El(chip("استثنا", fa("Black", 46), GREEN, NAVY_D), cx, 880, st(9) - 0.1, e, anim="pop", anchor="c"))
        els.append(El(row("۲۰ ماه کار تمام‌وقت در ۲ سال آخر", icon_check), 80, 970, st(9) + 0.1, e, anim="right"))
        # 4
        e = end(11); t0 = st(10) - 0.05
        els.append(El(step_badge(4, ""), cx, 330, t0, e, anim="pop", anchor="c"))
        els.append(El(T_("محکومیت سنگین نداشته باشی", 68), cx, 500, t0 + 0.2, e, anchor="c"))
        els.append(El(row("بیشتر از ۹۰ روز جریمه", icon_cross), 80, 640, at(10, 0.45), e, anim="right"))
        els.append(El(row("بیشتر از ۳ ماه زندان", icon_cross), 80, 820, at(10, 0.75), e, anim="right"))
        # good news
        e = end(12); t0 = st(11) - 0.05
        els.append(El(chip("خبر خوب", fa("Black", 54), GREEN, NAVY_D), cx, 400, t0, e, anim="pop", anchor="c"))
        els.append(El(T_("دو تابعیت مجازه", 96), cx, 560, at(11, 0.55), e, anim="pop", anchor="c"))
        els.append(El(row("پاسپورت قبلی‌ت رو نگه دار", icon_check), 80, 760, at(11, 0.3), e, anim="right"))
        # spouse
        e = end(13); t0 = st(12) - 0.05
        els.append(El(T_("همسر شهروند آلمانی", 76), cx, 430, t0, e, anchor="c"))
        els.append(El(tile("۳ سال", "اقامت"), cx + 10, 580, at(12, 0.35), e, anim="pop"))
        els.append(El(tile("۲ سال", "ازدواج"), cx - 10 - TW, 580, at(12, 0.55), e, anim="pop"))
        outro(els, st(13) - 0.05, "این ویدیو رو سیو کن", "و برای کسی که منتظر پاسپورته بفرست")

    elif key == "N":
        els.insert(0, header("اقامت دائم"))
        e = end(2)
        els.append(El(T_("اقامت دائم آلمان", 86), cx, 420, 0.05, e, anchor="c"))
        els.append(El(T_("کی بهت می‌دن؟", 96, GOLD), cx, 540, 0.4, e, anchor="c"))
        els.append(El(chip("شاید زودتر از اونی که فکر می‌کنی!", fa("Black", 46), RED, WHITE), cx, 680, T.get("hook_chip", at(0, 0.55)), e, anim="pop", anchor="c"))
        if "support" in T:
            a_, b_ = T["support"]
            els.append(El(chip("اگه مفیده، فالو و لایک کن", fa("Black", 50), GOLD, NAVY_D), cx, 1180, a_, b_, anim="pop", anchor="c"))
        c, b = german_card("Niederlassungserlaubnis", "اقامت دائم")
        els.append(El(c, cx, 860, st(1) - 0.05, e, anim="pop", anchor="c", dur=0.5)); els.append(El(b, cx, 830, st(1) + 0.1, e, anim="pop", anchor="c"))
        # Blue card
        e = end(8); t0 = st(2) - 0.05
        els.append(El(chip("۱ · بلوکارت", fa("Black", 46), GOLD, NAVY_D), cx, 330, t0, e, anim="pop", anchor="c"))
        c, b = german_card("Blaue Karte EU", "کارت آبی اتحادیه‌ی اروپا")
        els.append(El(c, cx, 460, st(3) - 0.05, e, anim="pop", anchor="c", dur=0.5)); els.append(El(b, cx, 430, st(3) + 0.1, e, anim="pop", anchor="c"))
        els.append(El(tile("۲۱ ماه", "با زبان B1"), cx + 10, 820, st(5) - 0.05, e, anim="pop"))
        els.append(El(tile("۲۷ ماه", "با زبان A1"), cx - 10 - TW, 820, st(7) - 0.05, e, anim="pop"))
        # Fachkraft
        e = end(12); t0 = st(8) - 0.05
        els.append(El(chip("۲ · متخصص", fa("Black", 46), GOLD, NAVY_D), cx, 330, t0, e, anim="pop", anchor="c"))
        c, b = german_card("Fachkraft", "نیروی متخصص")
        els.append(El(c, cx, 460, st(9) - 0.05, e, anim="pop", anchor="c", dur=0.5)); els.append(El(b, cx, 430, st(9) + 0.1, e, anim="pop", anchor="c"))
        els.append(El(row("۳ سال اقامت", num_icon(3)), 80, 800, st(10), e, anim="right"))
        els.append(El(row("۳۶ ماه بیمه‌ی بازنشستگی", icon_check), 80, 980, at(10, 0.4), e, anim="right"))
        els.append(El(row("زبان آلمانی B1", icon_check), 80, 1160, st(11) - 0.05, e, anim="right"))
        # Graduates
        e = end(16); t0 = st(12) - 0.05
        els.append(El(chip("۳ · تحصیل در آلمان", fa("Black", 46), GOLD, NAVY_D), cx, 330, t0, e, anim="pop", anchor="c"))
        els.append(El(row("دانشگاه یا دوره‌ی حرفه‌ای در آلمان", icon_check, sub="Studium / Ausbildung"), 80, 460, t0 + 0.2, e, anim="right"))
        els.append(El(big("فقط ۲ سال", GOLD, 150), cx, 720, at(14, 0.1), e, anim="pop", anchor="c"))
        els.append(El(row("۲۴ ماه بیمه‌ی بازنشستگی", icon_check), 80, 960, at(14, 0.5), e, anim="right"))
        els.append(El(row("زبان آلمانی B1", icon_check), 80, 1140, st(15) - 0.05, e, anim="right"))
        # General
        e = end(18); t0 = st(16) - 0.05
        els.append(El(chip("۴ · حالت عمومی", fa("Black", 46), GOLD, NAVY_D), cx, 330, t0, e, anim="pop", anchor="c"))
        els.append(El(row("۵ سال اقامت", num_icon(5)), 80, 480, at(16, 0.2), e, anim="right"))
        els.append(El(row("۶۰ ماه بیمه‌ی بازنشستگی", icon_check), 80, 660, at(16, 0.5), e, anim="right"))
        els.append(El(row("زبان آلمانی B1", icon_check), 80, 840, st(17) - 0.05, e, anim="right"))
        # All cases
        e = end(19); t0 = st(18) - 0.05
        els.append(El(T_("در همه‌ی حالت‌ها", 80), cx, 420, t0, e, anchor="c"))
        els.append(El(row("خرج زندگی‌ت رو خودت بدی", icon_check), 80, 580, at(18, 0.2), e, anim="right"))
        els.append(El(row("خونه‌ی کافی داشته باشی", icon_check), 80, 760, at(18, 0.42), e, anim="right"))
        els.append(El(row("پناهنده‌ها: قوانین جداگانه", info_icon, sub="§ 26 AufenthG"), 80, 940, at(18, 0.65), e, anim="pop"))
        outro(els, st(19) - 0.05, "سیو کن", "و برای دوستی که دنبال اقامت دائمه بفرست")
        if "comment_q" in T:
            els.append(El(chip(T["comment_q"], fa("Black", 50), RED, WHITE), cx, 250, st(19) + 0.9, anim="pop", anchor="c"))
        if "source" in T:
            lab = text_sprite("منبع:", fa("Bold", 30), (150, 170, 200), rtl=True); src = text_sprite(T["source"], la("Bold", 30), (150, 170, 200))
            im = Image.new("RGBA", (src.width + 12 + lab.width, max(src.height, lab.height)), (0, 0, 0, 0))
            im.alpha_composite(src, (0, (im.height - src.height) // 2)); im.alpha_composite(lab, (src.width + 12, (im.height - lab.height) // 2))
            els.append(El(im, cx, 1440, 0.3, anim="fade", anchor="c"))
    for e_ in els[2:]:
        if isinstance(e_, El): e_.y += OFF
    return els

if __name__ == "__main__":
    key = sys.argv[1]; T = json.load(open(sys.argv[2]))
    R.build = lambda T_: make(T_, key)
    tt = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")] if "--frames" in sys.argv else None
    R.render(T, sys.argv[3], sys.argv[4], tt)

#!/usr/bin/env python3
"""Kurdish (Sorani) silent Steuer reel. usage: kurd_steuer.py audio.wav out.mp4 [--frames ...]"""
import sys, json, math
sys.path.insert(0, "/home/claude/wegweiser/batch2")
from reel import *          # header, row, T_, chip helpers, follow_btn, OFF ...
import render as R
KD = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
TIMES = {"g0": 1.6, "g1": 10.3, "g2": 12.2, "g3": 14.1, "g4": 16.0, "g5": 24.0}
TOTAL = 32.4

def knum(n):
    def f(size):
        im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse((0, 0, size - 1, size - 1), fill=RED)
        t = text_sprite(str(n).translate(KD), fa("Black", int(size * .55)), WHITE, rtl=True)
        im.alpha_composite(t, ((size - t.width) // 2, (size - t.height) // 2 - 3)); return im
    return f

def build(_T):
    els = [header("باج لە ئەڵمانیا")]
    els.append(El(T_("زانیاریی گشتییە · بۆ حاڵەتی تایبەت پرسیار لە Steuerberater بکە", 28, (150, 170, 200), "Medium"), cx, 1640, 0.3, anim="fade", anchor="c"))
    O = OFF
    # ---- Scene 1 ----
    e = 9.0
    els.append(El(T_("ئەمەت دەزانی؟", 92, GOLD), cx, 280 + O, 0.2, e, anim="pop", anchor="c"))
    els.append(El(T_("ئەوانەی لە ئەڵمانیا", 66), cx, 390 + O, 0.9, e, anchor="c"))
    c, b = german_card("Steuererklärung", "فۆرمی ساڵانەی باج")
    els.append(El(c, cx, 515 + O, TIMES["g0"] - 0.05, e, anim="pop", anchor="c", dur=0.5)); els.append(El(b, cx, 485 + O, TIMES["g0"] + 0.1, e, anim="pop", anchor="c"))
    els.append(El(T_("پڕ دەکەنەوە، بە تێکڕایی نزیکەی", 58, SOFT, "Bold"), cx, 865 + O, 3.3, e, anchor="c"))
    t_stat = 4.0; e_s = e; statf = la("Black", 170)
    def stat(frame, t):
        if t < t_stat or t > e_s + 0.35: return
        p = ease_out((t - t_stat) / 1.1); o = ease_out((t - t_stat) / 0.3) * ((1 - ease_out((t - e_s) / 0.3)) if t > e_s else 1)
        s = f"+{int(round(1000 * p)):,}".replace(",", ".") + " €"
        sp = text_sprite(s, statf, GOLD)
        if o < 0.999: sp.putalpha(sp.getchannel("A").point(lambda a: int(a * o)))
        frame.alpha_composite(sp, (cx - sp.width // 2, 950 + O))
    els.append(Dyn(stat))
    els.append(El(T_("یان لە Finanzamt بۆ دەگەڕێتەوە!", 58, WHITE, "Bold"), cx, 1170 + O, 5.2, e, anchor="c"))
    els.append(El(chip("بەڵام زۆر کەس ئەم فۆرمە هەر پڕ ناکاتەوە!", fa("Bold", 40), RED, WHITE), cx, 1265 + O, 6.4, e, anim="pop", anchor="c"))
    # ---- Scene 2 ----
    e = 18.6; t0 = 9.3
    els.append(El(T_("ئەم خەرجییانە باجەکەت کەم دەکەنەوە:", 54), cx, 340 + O, t0, e, anchor="c"))
    items = [("کرێی هاتوچۆ بۆ سەر کار", "Pendlerpauschale", "g1"), ("ئامێر و کەرەستەی کار", "Arbeitsmittel", "g2"),
             ("خولی فێرکاری", "Fortbildung", "g3"), ("گواستنەوەی ماڵ لەبەر کار", "Umzugskosten", "g4")]
    for i, (k, de, g) in enumerate(items):
        els.append(El(row(k, knum(i + 1), h=160, sub=de), 80, 450 + O + i * 195, TIMES[g] - 0.15, e, anim="right"))
    # ---- Scene 3 ----
    e = 27.8; t0 = 18.9
    els.append(El(chip("هەواڵێکی خۆش", fa("Black", 50), GREEN, NAVY_D), cx, 240 + O, t0, e, anim="pop", anchor="c"))
    els.append(El(T_("دەتوانیت تا ٤ ساڵ دواتریش", 70), cx, 360 + O, t0 + 0.5, e, anchor="c"))
    els.append(El(T_("فۆرمەکە پڕ بکەیتەوە", 70, GOLD), cx, 450 + O, t0 + 0.8, e, anchor="c"))
    els.append(El(T_("(بۆ ئەوانەی یاسا ناچاری نەکردوون)", 40, SOFT, "Medium"), cx, 535 + O, t0 + 1.6, e, anchor="c"))
    els.append(El(chip("ساڵی ٢٠٢٢ تا 31.12.2026", fa("Bold", 44), RED, WHITE), cx, 615 + O, 21.6, e, anim="pop", anchor="c"))
    els.append(El(T_("هەمووی بە ئینتەرنێت دەکرێت", 60, WHITE, "Bold"), cx, 720 + O, 23.0, e, anchor="c"))
    c, b = german_card("ELSTER", "ماڵپەڕی فەرمیی Finanzamt")
    els.append(El(c, cx, 850 + O, TIMES["g5"] - 0.05, e, anim="pop", anchor="c", dur=0.5)); els.append(El(b, cx, 820 + O, TIMES["g5"] + 0.1, e, anim="pop", anchor="c"))
    els.append(El(chip("بێ پارەیە", fa("Black", 48), GREEN, NAVY_D), cx, 1195 + O, 25.3, e, anim="pop", anchor="c"))
    # ---- Outro ----
    t2 = 28.1
    els.append(El(T_("ئەم ڤیدیۆیە هەڵبگرە", 84), cx, 420 + O, t2, anim="up", anchor="c"))
    els.append(El(T_("و بۆ هاوڕێکانت بنێرە", 64, GOLD, "Bold"), cx, 540 + O, t2 + 0.35, anim="up", anchor="c"))
    btn = rounded(600, 130, 65, RED); bs = text_sprite("فۆڵۆمان بکە", fa("Black", 60), WHITE, rtl=True)
    btn.alpha_composite(bs, ((600 - bs.width) // 2, (130 - bs.height) // 2 - 4)); btn = shadowed(btn)
    t_f = t2 + 1.0; yb = 720 + O
    def follow(frame, t):
        if t < t_f: return
        p = t - t_f; s = (0.6 + 0.4 * ease_back(p / 0.45)) * (1 + 0.035 * math.sin(max(0, p - 0.45) * 6.0))
        img = btn.resize((int(btn.width * s), int(btn.height * s)), Image.BILINEAR); o = ease_out(p / 0.25)
        if o < 1: img.putalpha(img.getchannel("A").point(lambda a: int(a * o)))
        frame.alpha_composite(img, (cx - img.width // 2, yb + btn.height // 2 - img.height // 2))
    els.append(Dyn(follow))
    return els

if __name__ == "__main__":
    R.build = build
    tt = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")] if "--frames" in sys.argv else None
    R.render({"total": TOTAL}, sys.argv[1], sys.argv[2], tt)

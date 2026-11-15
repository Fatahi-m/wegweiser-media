#!/usr/bin/env python3
import sys, math
sys.path.insert(0, "/home/claude/wegweiser/batch2")
from kbase import *
TIMES = {"g0": 1.6, "g1": 10.3, "g2": 12.2, "g3": 14.1, "g4": 16.0, "g5": 24.0}
TOTAL = 32.4

def build():
    els = [header("باج لە ئەڵمانیا"), footer("زانیاریی گشتییە · بۆ حاڵەتی تایبەت پرسیار لە Steuerberater بکە")]
    els.append(source_line("§ 46 EStG · § 169 AO · ELSTER"))
    # Scene 1
    e = 9.0
    els.append(El(T("ئەمەت دەزانی؟", 96, KRED), cx, 300, 0.2, e, anim="pop", anchor="c"))
    els.append(El(T("ئەوانەی لە ئەڵمانیا", 64, INK, "Bold"), cx, 430, 0.9, e, anchor="c"))
    els.append(El(kcard("Steuererklärung", "فۆرمی ساڵانەی باج"), cx, 540, TIMES["g0"] - 0.05, e, anim="pop", anchor="c", dur=0.5))
    els.append(El(T("پڕ دەکەنەوە، بە تێکڕایی نزیکەی", 56, MUTED, "Bold"), cx, 905, 3.3, e, anchor="c"))
    t_stat = 4.0; e_s = e
    # sun badge behind number
    sb = sun(420, SUN); sb.putalpha(sb.getchannel("A").point(lambda a: int(a * .35)))
    els.append(El(sb, cx, 920, t_stat, e, anim="pop", anchor="c", dur=0.6))
    statf = la("Black", 170)
    def stat(frame, t):
        if t < t_stat or t > e_s + 0.35: return
        p = ease_out((t - t_stat) / 1.1); o = ease_out((t - t_stat) / 0.3) * ((1 - ease_out((t - e_s) / 0.3)) if t > e_s else 1)
        sp = text_sprite(f"+{int(round(1000 * p)):,}".replace(",", ".") + " €", statf, GREEN)
        if o < 0.999: sp.putalpha(sp.getchannel("A").point(lambda a: int(a * o)))
        frame.alpha_composite(sp, (cx - sp.width // 2, 1000))
    els.append(Dyn(stat))
    els.append(El(T("یان لە Finanzamt بۆ دەگەڕێتەوە!", 56, INK, "Bold"), cx, 1245, 5.2, e, anchor="c"))
    els.append(El(kchip("بەڵام زۆر کەس ئەم فۆرمە هەر پڕ ناکاتەوە!", KRED, (255, 255, 255), 40), cx, 1345, 6.4, e, anim="pop", anchor="c"))
    # Scene 2
    e = 18.6; t0 = 9.3
    els.append(El(fitT("ئەم خەرجییانە باجەکەت کەم دەکەنەوە:", 62, 960), cx, 380, t0, e, anchor="c"))
    items = [("کرێی هاتوچۆ بۆ سەر کار", "Pendlerpauschale", "g1"), ("ئامێر و کەرەستەی کار", "Arbeitsmittel", "g2"),
             ("خولی فێرکاری", "Fortbildung", "g3"), ("گواستنەوەی ماڵ لەبەر کار", "Umzugskosten", "g4")]
    for i, (k, de, g) in enumerate(items):
        els.append(El(krow(k, i + 1, de, h=170), 80, 520 + i * 215, TIMES[g] - 0.15, e, anim="right"))
    # Scene 3
    e = 27.8; t0 = 18.9
    els.append(El(kchip("هەواڵێکی خۆش", GREEN, (255, 255, 255), 48), cx, 280, t0, e, anim="pop", anchor="c"))
    els.append(El(T("دەتوانیت تا ٤ ساڵ دواتریش", 68), cx, 410, t0 + 0.5, e, anchor="c"))
    els.append(El(T("فۆرمەکە پڕ بکەیتەوە", 68, KRED), cx, 500, t0 + 0.8, e, anchor="c"))
    els.append(El(T("(بۆ ئەوانەی یاسا ناچاری نەکردوون)", 38, MUTED, "Medium"), cx, 590, t0 + 1.6, e, anchor="c"))
    els.append(El(kchip("ساڵی ٢٠٢٢ تا 31.12.2026", SUN, INK, 44), cx, 670, 21.6, e, anim="pop", anchor="c"))
    els.append(El(T("هەمووی بە ئینتەرنێت دەکرێت", 58, INK, "Bold"), cx, 790, 23.0, e, anchor="c"))
    els.append(El(kcard("ELSTER", "ماڵپەڕی فەرمیی Finanzamt"), cx, 880, TIMES["g5"] - 0.05, e, anim="pop", anchor="c", dur=0.5))
    els.append(El(kchip("بێ پارەیە", GREEN, (255, 255, 255), 48), cx, 1210, 25.3, e, anim="pop", anchor="c"))
    # Outro
    t2 = 28.1
    els.append(El(sun(200), cx, 420, t2, anim="pop", anchor="c"))
    els.append(El(T("ئەم ڤیدیۆیە هەڵبگرە", 84), cx, 680, t2 + 0.2, anim="up", anchor="c"))
    els.append(El(T("و بۆ هاوڕێکانت بنێرە", 64, GREEN, "Bold"), cx, 800, t2 + 0.5, anim="up", anchor="c"))
    els.append(follow_btn(t2 + 1.1, 970))
    return els

if __name__ == "__main__":
    tt = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")] if "--frames" in sys.argv else None
    render(build, TOTAL, sys.argv[1], sys.argv[2], tt)

#!/usr/bin/env python3
import sys, math
sys.path.insert(0, "/home/claude/wegweiser/batch2")
from kbase import *
# German clip index -> time it plays
G_AT = {0: 0.5, 1: 6.8, 2: 13.2, 3: 14.8, 4: 16.4, 5: 18.0, 6: 23.6, 7: 31.4, 8: 36.8}
TOTAL = 47.6

def step(n, text, t, e, y=300):
    im = Image.new("RGBA", (W, 130), (0, 0, 0, 0))
    b = knum(n, 104); tx = fitT(text, 62, W - 300)
    wtot = b.width + 24 + tx.width; x0 = (W - wtot) // 2
    im.alpha_composite(tx, (x0, (130 - tx.height) // 2)); im.alpha_composite(b, (x0 + tx.width + 24, 13))
    return El(im, 0, y, t, e, anim="up")

def build():
    els = [header("نامەی Jobcenter"), footer("زانیاریی گشتییە · بۆ حاڵەتی تایبەت پرسیار لە Beratungsstelle بکە")]
    # S1
    e = 5.5
    env = Image.new("RGBA", (420, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(env)
    d.rounded_rectangle((0, 0, 419, 299), 30, fill=PAPER, outline=GREEN, width=8)
    d.line([(10, 14), (210, 160), (410, 14)], fill=GREEN, width=8)
    st = text_sprite("Jobcenter", la("Black", 44), KRED); sb = rounded(st.width + 30, st.height + 16, 12, (0, 0, 0, 0), outline=KRED, ow=5)
    sb.alpha_composite(st, (15, 8)); sb = sb.rotate(-10, expand=True, resample=Image.BICUBIC); env.alpha_composite(sb, (420 - sb.width - 20, 300 - sb.height - 16))
    els.append(El(shadowed(env, alpha=50), cx, 360, 0.1, e, anim="pop", anchor="c", dur=0.5))
    els.append(El(T("نامەیەکت لە Jobcenter بۆ هاتووە؟", 70), cx, 780, 0.5, e, anchor="c"))
    els.append(El(T("مەترسە!", 96, KRED), cx, 900, 1.8, e, anim="pop", anchor="c"))
    els.append(El(kchip("سەرەتا ئەم ٥ کارە بکە", GREEN, (255, 255, 255), 52), cx, 1040, 2.6, e, anim="pop", anchor="c"))
    # S2 Frist
    e = 12.0
    els.append(step(1, "سەرەتا وادەکە بدۆزەرەوە", 5.8, e))
    els.append(El(kcard("Frist", "دوا وادە"), cx, 500, G_AT[1] - 0.1, e, anim="pop", anchor="c", dur=0.5))
    els.append(El(T("لە نامەکەدا بەدوای «bis zum» بگەڕێ", 54, INK, "Bold"), cx, 850, 8.0, e, anchor="c"))
    els.append(El(T("و ڕێکەوتەکە هەر ئەو ڕۆژە بنووسە", 54, GREEN, "Bold"), cx, 940, 9.0, e, anchor="c"))
    # S3 types
    e = 20.0
    els.append(step(2, "بزانە نامەکە چ جۆرێکە", 12.3, e))
    types = [("بانگهێشت بۆ چاوپێکەوتن", "Einladung", 2), ("داوای بەڵگەنامە", "Mitwirkung", 3),
             ("بڕیار دەربارەی پارەکەت", "Bescheid", 4), ("دەیانەوێت ڕای خۆت بزانن", "Anhörung", 5)]
    for i, (k, de, g) in enumerate(types):
        els.append(El(krow(k, i + 1, de, h=165), 80, 470 + i * 205, G_AT[g] - 0.15, e, anim="right"))
    # S4 Einladung
    e = 27.5
    els.append(step(3, "بانگهێشتت بۆ هاتووە؟ حەتمەن بڕۆ", 20.3, e))
    els.append(El(T("ئەگەر ناتوانیت بچیت، پێش وادەکە", 54, INK, "Bold"), cx, 480, 21.0, e, anchor="c"))
    els.append(El(T("ئاگاداریان بکەرەوە و بەڵگە بهێنە،", 54, INK, "Bold"), cx, 560, 21.6, e, anchor="c"))
    els.append(El(T("بۆ نموونە نامەی دکتۆر:", 54, GREEN, "Bold"), cx, 640, 22.3, e, anchor="c"))
    els.append(El(kcard("Krankmeldung", "نامەی نەخۆشی لە دکتۆرەوە"), cx, 770, G_AT[6] - 0.1, e, anim="pop", anchor="c", dur=0.5))
    els.append(El(kchip("بێ هۆکار نەچیت؟ لەوانەیە پارەکەت کەم بکەنەوە", KRED, (255, 255, 255), 38), cx, 1150, 25.2, e, anim="pop", anchor="c"))
    # S5 documents
    e = 35.5
    els.append(step(4, "بەڵگەنامەیان ویستووە؟", 27.8, e))
    els.append(El(T("پێش تەواوبوونی وادەکە بینێرە:", 58, INK, "Bold"), cx, 480, 28.5, e, anchor="c"))
    els.append(El(krow("باشترین ڕێگا ماڵپەڕەکەیانە", 1, "jobcenter.digital", h=165), 80, 590, 29.3, e, anim="right"))
    els.append(El(krow("یان خۆت بیبە و وەسڵ وەربگرە", 2, "Eingangsbestätigung", h=165), 80, 790, G_AT[7] - 0.15, e, anim="right"))
    els.append(El(kchip("لە هەموو شتێک کۆپییەک لای خۆت هەڵبگرە", GREEN, (255, 255, 255), 40), cx, 1020, 33.0, e, anim="pop", anchor="c"))
    # S6 Widerspruch
    e = 43.0
    els.append(step(5, "لەگەڵ بڕیارەکەیان ڕازی نیت؟", 35.8, e))
    els.append(El(kcard("Widerspruch", "ناڕەزایی"), cx, 470, G_AT[8] - 0.1, e, anim="pop", anchor="c", dur=0.5))
    els.append(El(T("زۆربەی کات مانگێکت هەیە بۆ ناڕەزایی", 56, INK, "Bold"), cx, 830, 38.0, e, anchor="c"))
    els.append(El(T("بێ پارەیە و پارێزەری ناوێت", 56, GREEN, "Bold"), cx, 920, 38.9, e, anchor="c"))
    els.append(El(kchip("وادەی ورد لە کۆتایی نامەکەدا نووسراوە", SUN, INK, 42), cx, 1040, 40.3, e, anim="pop", anchor="c"))
    # S7 outro
    t2 = 43.3
    els.append(El(sun(200), cx, 420, t2, anim="pop", anchor="c"))
    els.append(El(T("ئەم ڤیدیۆیە هەڵبگرە", 84), cx, 680, t2 + 0.2, anim="up", anchor="c"))
    els.append(El(fitT("و بۆ کەسێک بنێرە کە تازە هاتووەتە ئەڵمانیا", 56, 880, GREEN, "Bold"), cx, 800, t2 + 0.5, anim="up", anchor="c"))
    els.append(follow_btn(t2 + 1.1, 970 + 170))
    for x in els[2:]:
        if isinstance(x, El): x.y += 170
    els.append(source_line("§ 59 SGB II · § 60 SGB I · § 84 SGG"))
    return els

if __name__ == "__main__":
    tt = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")] if "--frames" in sys.argv else None
    render(build, TOTAL, sys.argv[1], sys.argv[2], tt)

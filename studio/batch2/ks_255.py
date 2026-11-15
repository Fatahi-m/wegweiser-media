from kbase import *
W_ = (255,255,255)
def bubble(lines, head="پرسیاری ئێوە لە کۆمێنت"):
    w = 900
    hd = T(head, 34, MUTED, "Bold")
    ls = [fitT(l, 50, w - 160, INK, "Bold") for l in lines]
    av = Image.new("RGBA", (84, 84), (0, 0, 0, 0)); ImageDraw.Draw(av).ellipse((0, 0, 83, 83), fill=(205, 212, 208))
    ImageDraw.Draw(av).ellipse((27, 14, 57, 44), fill=W_); ImageDraw.Draw(av).ellipse((14, 50, 70, 100), fill=W_)
    h = 40 + hd.height + 12 + sum(l.height for l in ls) + 8 * (len(ls) - 1) + 44
    c = rounded(w, h, 40, W_, outline=GREEN_L, ow=4)
    c.alpha_composite(av, (w - 34 - 84, 34))
    xr = w - 34 - 84 - 22; y = 40
    c.alpha_composite(hd, (xr - hd.width, y)); y += hd.height + 12
    for l in ls: c.alpha_composite(l, (xr - l.width, y)); y += l.height + 8
    tail = Image.new("RGBA", (w, h + 30), (0, 0, 0, 0)); tail.alpha_composite(c, (0, 0))
    ImageDraw.Draw(tail).polygon([(w - 160, h - 4), (w - 110, h - 4), (w - 150, h + 28)], fill=W_)
    return shadowed(tail, radius=18, off=(0, 10), alpha=60)
SPEC = {"source": "§§ 25 Abs. 5, 26 Abs. 4 AufenthG", "topic": "ئیقامەی مرۆیی",
 "footer": "زانیاریی گشتییە · بۆ حاڵەتی تایبەت پرسیار لە Migrationsberatung بکە",
 "scenes": [
  [("img", bubble(["La sar 25 Abs 5", "qsa bika bi zahmat"]), 3.0), ("title","با بزانین چییە!",76,GREEN)],
  [("card","§ 25 Abs. 5 AufenthG","ئیقامە بۆ خاوەنانی Duldung"),("row","ناتوانن بگەڕێنەوە وڵاتی خۆیان","no"),
   ("text","لەبەر هۆکاری یاسایی یان ڕاستەقینە",50),("chip","هۆکارەکە بەم زووانە نامێنێت",SUN,INK,46)],
  [("chip","نموونە",SUN,INK,46),("row","خێزان و منداڵەکانت لێرەن",1),("row","نەخۆشییەکی قورست هەیە",2),
   ("row","وڵاتەکەت پاسپۆرتت پێ نادات",3,"بەبێ ئەوەی هەڵەی خۆت بێت")],
  [("chip","خاڵی گرنگ",SUN,INK,46),("bigfa","١٨ مانگ",GREEN,150),("text","دوای ١٨ مانگ Duldung، دەبێت ئیقامەت پێ بدرێت",46,GREEN),
   ("chip","بە یەک مەرج: هەڵەی خۆت نەبێت",KRED,W_,44),("row","درۆت لە ناسنامەکەت نەکردبێت","ok"),("row","هەوڵت دابێت پاسپۆرت وەربگریت","ok")],
  [("chip","دەتوانێت ببێتە دائیمی!",GREEN,W_,48),("card","§ 26 Abs. 4 AufenthG","یاسای ئیقامەی دائیمی"),
   ("row","٥ ساڵ ئیقامە",1),("row","زمانی ئەڵمانی B1",2),("row","٦٠ مانگ بیمەی خانەنشینی",3),("row","خەرجیی ژیان بێ Jobcenter",4)],
  [("chip","ئامۆژگاری",SUN,INK,46),("text","داواکارییەکە بە نووسراو بدە بە:",52,GREEN),("card","Ausländerbehörde","فەرمانگەی بیانییەکان"),
   ("card","Migrationsberatung","پێشتر ڕاوێژ وەربگرە")],
 ],
 "timing": [([0.15,5.9],7.9),([8.1,11.7,15.4,18.42],20.35),([20.57,21.58,23.63,25.16],28.9),
   ([29.13,30.2,32.54,35.12,37.59,39.7],41.95),([43.72,45.87,48.47,49.8,50.88,52.6],54.85),([55.07,55.5,56.3,57.8],61.15)],
 "outro_t": 61.39, "total": 67.4,
 "outro": ("ئەم ڤیدیۆیە هەڵبگرە","و بۆ کەسێک بنێرە کە پێویستی پێیەتی")}

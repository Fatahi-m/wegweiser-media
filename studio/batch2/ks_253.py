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
SPEC = {"source": "§§ 25 Abs. 3, 26 Abs. 4 AufenthG · BVerwG 1 C 17.10", "topic": "ئیقامەی دائیمی",
 "footer": "زانیاریی گشتییە · بۆ حاڵەتی تایبەت پرسیار لە Migrationsberatung بکە",
 "scenes": [
  [("img", bubble(["سڵاوو ایقامەی 25//3", "چۆن ئەتوانیت بیکەیتە دایمی"]), 3.0), ("title","پرسیارێکی زۆر باشە!",76,GREEN)],
  [("card","§ 25 Abs. 3 AufenthG","ئیقامە بەهۆی Abschiebungsverbot"),("text","BAMF دەیدات کاتێک ناتوانرێت بگەڕێنرێیتەوە",48),
   ("chip","دەتوانێت ببێتە دائیمی!",GREEN,W_,48),("card","§ 26 Abs. 4 AufenthG","یاسای ئیقامەی دائیمی")],
  [("chip","مەرجی یەکەم",SUN,INK,46),("bigfa","٥ ساڵ",GREEN,160),("row","ساڵانی ئیقامەکەت دەژمێردرێن","ok"),
   ("row","ساڵانی Gestattung دەژمێردرێن","ok","تەنانەت ئەگەر ڕەتکرابێتەوە"),("row","ساڵانی Duldung ناژمێردرێن","no")],
  [("chip","مەرجەکانی تر",SUN,INK,46),("row","خەرجیی ژیان بێ Jobcenter",1),("row","٦٠ مانگ بیمەی خانەنشینی",2),
   ("row","زمانی ئەڵمانی B1",3),("row","تاقیکردنەوەی Leben in Deutschland",4),("row","خانووی گونجاو · بێ تاوانی گەورە",5)],
  [("chip","ئامۆژگاری",SUN,INK,46),("card","Rentenverlauf","لە Rentenversicherung داوای بکە"),
   ("text","ئینجا داواکارییەکە بدە بە:",54,GREEN),("card","Ausländerbehörde","فەرمانگەی بیانییەکان")],
  [("chip","ئاگاداربە",KRED,W_,52),("title","خۆکار نابێتە دائیمی!",84,KRED),("text","دەبێت خۆت داوای بکەیت",58,GREEN)],
 ],
 "timing": [([0.15,5.29],6.6),([6.84,9.5,18.38,21.97],24.4),([24.63,25.83,26.68,28.66,32.81],35.1),
   ([35.31,36.65,40.53,42.97,45.12,47.55],50.8),([51.02,52.34,57.83,58.6],60.5),([60.76,61.99,64.41],65.95)],
 "outro_t": 66.15, "total": 72.6,
 "outro": ("ئەم ڤیدیۆیە هەڵبگرە","و بۆ کەسێک بنێرە کە ئەم ئیقامەیەی هەیە")}

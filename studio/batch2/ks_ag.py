from kbase import *
from PIL import ImageFont
W_ = (255, 255, 255)
def remark(code, w=820):
    h = 150
    c = rounded(w, h, 18, (226, 228, 230), outline=(190, 194, 198), ow=3)
    a = text_sprite("ANMERKUNGEN/REMARKS", la("Bold", 26), (70, 74, 80)); c.alpha_composite(a, (36, 20))
    b = text_sprite(code, ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 54), (40, 44, 50)); c.alpha_composite(b, (36, 62))
    return shadowed(c, radius=14, off=(0, 8), alpha=50)
SPEC = {"source": "§§ 3, 4 AsylG · § 26 AufenthG · Gesetz 23.07.2025", "topic": "کارتی ئیقامە",
 "footer": "زانیاریی گشتییە · بۆ حاڵەتی تایبەت پرسیار لە Migrationsberatung بکە",
 "scenes": [
  [("title", "لەسەر کارتەکەت چی نووسراوە؟", 72), ("img", remark("25 ABS.2 (3 ASYLG)")), ("img", remark("25 ABS.2 (4 ASYLG)")),
   ("title", "جیاوازییان چییە؟", 66, KRED), ("chip", "فۆڵۆ و لایک بکە · سوپاس", GREEN_L, GREEN, 44)],
  [("chip", "Anmerkungen", INK, W_, 60, True), ("text", "لە کارتەکەتدا سەیری ئەم بەشە بکە", 52)],
  [("card", "3 AsylG = Flüchtling", "پەنابەر"), ("text", "BAMF دەڵێت خۆت ڕاو نراویت لەبەر:", 46),
   ("text", "دین · نەتەوە · سیاسەت · گرووپ", 54, GREEN), ("row", "ئیقامەی ٣ ساڵ", "ok"), ("row", "زووتر ئیقامەی دائیمی", "ok")],
  [("card", "4 AsylG = subsidiär", "خۆت ڕاو نەنراویت"), ("text", "بەڵام ئەگەر بگەڕێیتەوە، مەترسیی گەورە:", 44),
   ("text", "لەسێدارەدان · ئەشکەنجە · شەڕ", 54, KRED), ("row", "سەرەتا ١ ساڵ، دواتر ٢ ساڵ", "info"),
   ("row", "ئیقامەی دائیمی دوای ٥ ساڵ", "ok"), ("row", "هێنانی خێزان ڕاگیراوە", "no", "تا مانگی ٧ی ٢٠٢٧")],
 ],
 "timing": [([0.27, 1.0, 1.6, 2.12, 5.07], 8.7),
   ([9.02, 9.6], 11.85),
   ([12.30, 14.5, 16.9, 21.86, 23.51], 25.95),
   ([26.35, 31.49, 34.11, 37.11, 40.07, 42.33], 45.9)],
 "outro_t": 46.18, "total": 52.9,
 "outro": ("تۆ کامیانت هەیە؟", "لە کۆمێنت بنووسە: ٣ یان ٤")}

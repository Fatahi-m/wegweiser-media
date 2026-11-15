from kbase import *
from kremark import remark
W_ = (255, 255, 255)
SPEC = {"source": "§§ 25, 26 AufenthG · §§ 3, 4 AsylG · Gesetz 23.07.2025", "topic": "جۆرەکانی ئیقامە",
 "footer": "زانیاریی گشتییە · بۆ حاڵەتی تایبەت پرسیار لە Migrationsberatung بکە",
 "scenes": [
  [("title", "لەسەر کارتەکەت نووسراوە:", 72), ("chip", "§ 25 Abs. 1 · 2 · 3", INK, W_, 76, True), ("title", "جیاوازییان زۆرە!", 80, KRED),
   ("chip", "فۆڵۆ و لایک بکە · سوپاس", GREEN_L, GREEN, 44)],
  [("card", "§ 25 Abs. 1", "پەنابەری بەپێی یاسای بنەڕەتی"), ("row", "ئیقامەی ٣ ساڵ", "ok")],
  [("card", "§ 25 Abs. 2", "دوو جۆرە"), ("img", remark("25 ABS.2 (3 ASYLG)")), ("chip", "Flüchtling", GREEN, W_, 60, True),
   ("row", "ئیقامەی ٣ ساڵ", "ok")],
  [("img", remark("25 ABS.2 (4 ASYLG)")), ("chip", "subsidiärer Schutz", KRED, W_, 60, True), ("row", "سەرەتا ١ ساڵ، دواتر ٢ ساڵ", "info"),
   ("row", "هێنانی خێزان ڕاگیراوە", "no", "تا مانگی ٧ی ٢٠٢٧")],
  [("card", "§ 25 Abs. 3", "Abschiebungsverbot"), ("text", "BAMF دەڵێت ناتوانیت بگەڕێیتەوە", 48), ("row", "ئیقامەی لانیکەم ١ ساڵ", "ok")],
  [("chip", "ئیقامەی دائیمی", GREEN, W_, 54), ("chip", "§ 25 Abs. 1 + Flüchtling", INK, W_, 50, True), ("row", "دوای ٥ ساڵ", "ok", "Deutsch A2"),
   ("row", "یان دوای ٣ ساڵ", "ok", "Deutsch C1"), ("chip", "§ 26 Abs. 3 AufenthG", INK, W_, 42, True)],
  [("chip", "subsidiär + § 25 Abs. 3", KRED, W_, 50, True), ("row", "دوای ٥ ساڵ", "info", "Deutsch B1"), ("row", "٦٠ مانگ بیمەی خانەنشینی", "info"),
   ("row", "خەرجیی ژیان بێ Jobcenter", "info"), ("text", "ساڵانی Asylverfahren دەژمێردرێن", 46, GREEN), ("chip", "§ 26 Abs. 4 AufenthG", INK, W_, 42, True)],
 ],
 "timing": [([0.3, 1.2, 5.1, 6.6], 8.8), ([9.0, 13.7], 15.2), ([15.4, 18.0, 20.9, 22.3], 23.7), ([23.9, 26.1, 27.9, 30.2], 33.8),
   ([34.0, 37.6, 39.9], 41.7), ([41.9, 43.4, 46.1, 48.3, 49.0], 50.7), ([50.9, 53.4, 55.9, 57.7, 59.9, 60.5], 62.4)],
 "outro_t": 62.6, "total": 70.0,
 "outro": ("تۆ کامیانت هەیە؟", "لە کۆمێنت بنووسە: ١، ٢ یان ٣")}

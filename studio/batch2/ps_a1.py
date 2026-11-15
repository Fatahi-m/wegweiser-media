from reel import GOLD, WHITE, RED, GREEN, NAVY_D, CARD, SOFT
from kremark import remark
SPEC = {"topic": "انواع اقامت", "source": "§§ 25, 26 AufenthG · §§ 3, 4 AsylG · Gesetz 23.07.2025",
 "scenes": [
  [("title", "روی کارت اقامتت نوشته:", 72), ("chip", "§ 25 Abs. 1 · 2 · 3", WHITE, NAVY_D, 72, True), ("title", "فرقشون خیلی زیاده!", 84, GOLD),
   ("chip", "فالو و لایک کن · ممنون", GOLD, NAVY_D, 44)],
  [("card", "§ 25 Abs. 1", "پناهندگی طبق قانون اساسی"), ("row", "اقامت ۳ ساله", "ok")],
  [("card", "§ 25 Abs. 2", "دو نوع داره"), ("img", remark("25 ABS.2 (3 ASYLG)")), ("chip", "Flüchtling", GREEN, NAVY_D, 60, True),
   ("row", "اقامت ۳ ساله", "ok")],
  [("img", remark("25 ABS.2 (4 ASYLG)")), ("chip", "subsidiärer Schutz", RED, WHITE, 60, True), ("row", "اول ۱ سال، بعد ۲ سال", "info"),
   ("row", "آوردن خانواده تا جولای ۲۰۲۷ متوقفه", "no")],
  [("card", "§ 25 Abs. 3", "Abschiebungsverbot"), ("text", "BAMF گفته نمی‌تونی برگردی", 52), ("row", "اقامت حداقل ۱ ساله", "ok")],
  [("chip", "اقامت دائم", GREEN, NAVY_D, 54), ("chip", "§ 25 Abs. 1 + Flüchtling", WHITE, NAVY_D, 50, True), ("row", "بعد از ۵ سال", "ok", "Deutsch A2"),
   ("row", "یا بعد از ۳ سال", "ok", "Deutsch C1"), ("chip", "§ 26 Abs. 3 AufenthG", CARD, WHITE, 40, True)],
  [("chip", "subsidiär + § 25 Abs. 3", RED, WHITE, 50, True), ("row", "بعد از ۵ سال", "info", "Deutsch B1"), ("row", "۶۰ ماه بیمه‌ی بازنشستگی", "info"),
   ("row", "خرج زندگی بدون Jobcenter", "info"), ("text", "سال‌های Asylverfahren حساب می‌شه", 46, GREEN), ("chip", "§ 26 Abs. 4 AufenthG", CARD, WHITE, 40, True)],
 ],
 "timing": [([0.25, 1.5, 4.5, 6.2], 9.4), ([9.7, 15.5], 16.9), ([17.1, 20.1, 23.2, 24.3], 25.6), ([25.8, 28.1, 29.9, 31.9], 36.0),
   ([36.3, 40.7, 42.7], 44.9), ([45.1, 46.7, 49.8, 52.6, 53.2], 54.9), ([55.1, 57.7, 60.5, 62.6, 65.2, 65.6], 67.6)],
 "outro_t": 67.8, "total": 75.0, "outro": ("تو کدوم رو داری؟", "کامنت کن: ۱، ۲ یا ۳")}

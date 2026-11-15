from reel import *
from kremark import remark, rounded, shadowed
def bubble(lines, head="پرسش شما در کامنت‌ها"):
    w = 900; hd = T_(head, 32, (110, 120, 140), "Bold"); ls = [T_(l, 46, (20, 30, 50), "Bold") for l in lines]
    h = 40 + hd.height + 14 + sum(x.height for x in ls) + 8 * (len(ls) - 1) + 40
    c = rounded(w, h, 28, (255, 255, 255), outline=(220, 226, 236), ow=3)
    y = 40; c.alpha_composite(hd, (w - 50 - hd.width, y)); y += hd.height + 14
    for x in ls: c.alpha_composite(x, (w - 50 - x.width, y)); y += x.height + 8
    return shadowed(c, radius=16, off=(0, 8), alpha=60)
SPEC = {"topic": "روی کارتت چی نوشته؟", "source": "§§ 25, 26 AufenthG · §§ 3, 4 AsylG",
 "scenes": [
  [("img", bubble(["روی کارتم فقط ۲۵ بند ۲ نوشته،", "از کجا بفهمم چه اقامتی دارم؟"])), ("title", "امروز جوابش رو می‌گم!", 74, GOLD),
   ("chip", "فالو و لایک کن · ممنون", GOLD, NAVY_D, 44)],
  [("title", "پشت کارت اقامتت", 72), ("img", remark("25 ABS.2 (3 ASYLG)")), ("text", "همین پاراگراف نوع اقامتت رو می‌گه", 46)],
  [("card", "§ 25 Abs. 1", "پناهندگی طبق قانون اساسی"), ("chip", "Asylberechtigung", GREEN, NAVY_D, 56, True), ("row", "اقامت ۳ ساله", "ok")],
  [("img", remark("25 ABS.2 (3 ASYLG)")), ("text", "یا روی کارت‌های قدیمی‌تر:", 46), ("img", remark("25 ABS.2 S.1 1.ALT")),
   ("chip", "Flüchtling", GREEN, NAVY_D, 64, True), ("row", "اقامت ۳ ساله", "ok")],
  [("img", remark("25 ABS.2 (4 ASYLG)")), ("text", "یا روی کارت‌های قدیمی‌تر:", 46), ("img", remark("25 ABS.2 S.1 2.ALT")),
   ("chip", "subsidiärer Schutz", RED, WHITE, 60, True), ("row", "اول ۱ سال، بعد ۲ سال", "info")],
  [("img", remark("25 ABS.2")), ("text", "فقط همین؟ به اقامت اولت نگاه کن", 46, GOLD), ("row", "اقامت اول ۳ سال", "ok", "Flüchtling"),
   ("row", "اقامت اول ۱ سال", "info", "subsidiär"), ("text", "نامه‌ی BAMF هم دقیق نوشته", 44)],
  [("card", "§ 25 Abs. 3", "Abschiebungsverbot"), ("text", "BAMF گفته نمی‌تونی برگردی", 50), ("row", "اقامت حداقل ۱ ساله", "ok")],
  [("title", "یه نکته‌ی مهم مونده!", 80, RED), ("chip", "سیو کن · لایک کن", GOLD, NAVY_D, 56)],
  [("title", "فرقشون فقط اسم نیست", 70), ("chip", "Flüchtling · § 25 Abs. 1", GREEN, NAVY_D, 54, True), ("row", "پاسپورت آبی", "ok", "Reiseausweis"),
   ("row", "آوردن خانواده راحت‌تر", "ok"), ("row", "اقامت دائم بعد از ۵ سال", "ok", "Deutsch A2")],
  [("chip", "subsidiär · § 25 Abs. 3", RED, WHITE, 54, True), ("row", "پاسپورت کشور خودت", "info"), ("row", "اقامت دائم بعد از ۵ سال", "info", "Deutsch B1"),
   ("row", "آوردن خانواده متوقفه", "no", "subsidiär · bis 07/2027")],
 ],
 "timing": [([0.28, 5.2, 8.99], 12.55), ([12.88, 14.5, 16.4], 19.3), ([19.52, 22.2, 26.1], 27.85), ([27.99, 31.5, 32.9, 35.0, 38.6], 40.3),
   ([40.48, 44.0, 45.0, 46.6, 48.5], 52.55), ([52.86, 54.0, 58.3, 59.9, 61.5], 63.7), ([63.93, 68.0, 69.8], 72.15),
   ([72.42, 74.2], 77.25), ([77.37, 81.75, 83.1, 84.7, 86.6], 90.45), ([90.87, 92.3, 95.0, 98.3], 102.95)],
 "outro_t": 103.4, "total": 110.0, "outro": ("تو کدوم رو داری؟", "کامنت کن: ۱، ۲ یا ۳")}

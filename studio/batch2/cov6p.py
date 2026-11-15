from reel import *
def cov(topic, items, out, dy=-60, gap=50):
    bg = R.make_bg().convert("RGBA") if hasattr(R, "make_bg") else Image.new("RGBA", (W, H), NAVY)
    header(topic).draw(bg, 30)
    Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 + dy
    for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
    bg.convert("RGB").save(out, quality=92)
cov("انواع اقامت", [T_("روی کارت اقامتت نوشته:", 76, SOFT), chip("§ 25 Abs. 1 · 2 · 3", la("Black", 90), WHITE, NAVY_D, rtl=False),
    T_("فرقشون خیلی زیاده!", 104, GOLD), chip("اقامت دائم کی؟", fa("Black", 60), GREEN, NAVY_D)], "../out/cover-Wegweiser-Aufenthalt-25-1-2-3.jpg")
cov("اقامت بدون پناهندگی", [T_("پناهندگیت رد شده؟", 96), T_("هنوز ۳ راه هست!", 110, GOLD),
    chip("§ 25 Abs. 5 · § 25a · § 25b", la("Black", 66), WHITE, NAVY_D, rtl=False)], "../out/cover-Wegweiser-Aufenthalt-25-5-a-b.jpg")
cov("روی کارتت چی نوشته؟", [T_("روی کارتت فقط نوشته", 76, SOFT), chip("25 Abs. 2", la("Black", 110), WHITE, NAVY_D, rtl=False),
    T_("Flüchtling یا subsidiär؟", 84, GOLD), chip("جواب سؤال شما", fa("Black", 56), GREEN, NAVY_D)], "../out/cover-Wegweiser-Karte.jpg")
cov("Einstiegsgeld", [T_("برای سر کار رفتن", 72, SOFT), T_("از جاب‌سنتر پاداش بگیر!", 84, WHITE),
    chip("۲۸۰ تا ۵۰۰ یورو", fa("Black", 100), GOLD, NAVY_D), T_("ماهانه، تا ۲۴ ماه، کنار حقوقت", 60, GOLD),
    chip("Einstiegsgeld", la("Black", 64), WHITE, NAVY_D, rtl=False)], "../out/cover-Wegweiser-Einstiegsgeld.jpg")
cov("۵ کمک مالی جاب‌سنتر", [T_("۵ کمک مالی", 110, GOLD), T_("که جاب‌سنتر بهت میده", 72, WHITE),
    chip("و هیچ‌کس بهت نمیگه!", fa("Black", 64), RED, WHITE), T_("شماره‌ی ۱ حتی بدون جاب‌سنتر", 54, SOFT),
    chip("سیو کن!", fa("Black", 56), GOLD, NAVY_D)], "../out/cover-Wegweiser-5-Komak.jpg")
cov("Beschäftigungsduldung", [T_("Duldung داری و کار می‌کنی؟", 70, WHITE),
    chip("Beschäftigungsduldung", la("Black", 66), GOLD, NAVY_D, rtl=False), T_("۳۰ ماه، بعد اقامت 25b", 64, GOLD),
    T_("بعد اقامت دائم و پاسپورت", 58, SOFT), chip("همه‌ی شرط‌ها", fa("Black", 54), GREEN, NAVY_D)], "../out/cover-Wegweiser-Beschaeftigungsduldung.jpg")

from reel import *
def cov(topic, items, out, dy=-60, gap=50):
    bg = R.make_bg().convert("RGBA") if hasattr(R, "make_bg") else Image.new("RGBA", (W, H), NAVY)
    header(topic).draw(bg, 30)
    Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 + dy
    for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
    bg.convert("RGB").save(out, quality=92)
from kremark import remark
cov("اقامت ۲۲ و ۲۳", [chip("§ 22 / § 23", la("Black", 130), WHITE, NAVY_D, rtl=False), T_("روی کارت اقامتت کدوم نوشته؟", 62, WHITE),
    T_("یکی‌شون مستقیم پاسپورت میده!", 74, GOLD), remark("§ 23 ABS. 2 AUFENTHG", w=900),
    chip("فرق مهم برای افغان‌ها", fa("Black", 56), GREEN, NAVY_D)], "../out/cover-Wegweiser-22-23.jpg")

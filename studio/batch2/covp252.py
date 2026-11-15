from reel import *
def cov(topic, items, out, dy=-60, gap=50):
    bg = R.make_bg().convert("RGBA") if hasattr(R, "make_bg") else Image.new("RGBA", (W, H), NAVY)
    header(topic).draw(bg, 30)
    Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 + dy
    for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
    bg.convert("RGB").save(out, quality=92)
from kremark import remark
cov("اقامت 25.2", [chip("§ 25 Abs. 2", la("Black", 120), WHITE, NAVY_D, rtl=False), T_("حمایت تکمیلی داری؟", 74, WHITE),
    T_("کِی دائم میشی و کِی پاسپورت؟", 70, GOLD), remark("§ 25 ABS. 2 (4 ASYLG)", w=900),
    chip("حالا ۳ ساله!", fa("Black", 62), GREEN, NAVY_D)], "../out/cover-Wegweiser-25-2.jpg")

from reel import *
def cov(topic, items, out, dy=-60, gap=50):
    bg = R.make_bg().convert("RGBA") if hasattr(R, "make_bg") else Image.new("RGBA", (W, H), NAVY)
    header(topic).draw(bg, 30)
    Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 + dy
    for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
    bg.convert("RGB").save(out, quality=92)
cov("پول برای کار شخصی", [T_("می‌خوای کار خودت رو راه بندازی؟", 60, WHITE), big("تا ۵۰۰۰ یورو", GOLD, 150),
    T_("از جاب‌سنتر، بدون پس دادن!", 70, WHITE), chip("§ 16c SGB II", la("Black", 70), WHITE, NAVY_D, rtl=False),
    chip("چطوری درخواست بدی؟", fa("Black", 56), GREEN, NAVY_D)], "../out/cover-Wegweiser-16c.jpg")

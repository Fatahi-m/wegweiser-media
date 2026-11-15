from reel import *
def cov(topic, items, out, dy=-60, gap=50):
    bg = R.make_bg().convert("RGBA") if hasattr(R, "make_bg") else Image.new("RGBA", (W, H), NAVY)
    header(topic).draw(bg, 30)
    Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 + dy
    for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
    bg.convert("RGB").save(out, quality=92)
cov("ویزای دیدار", [T_("پدر و مادرت بیان آلمان؟", 92, WHITE), chip("Schengen-Visum", la("Black", 86), WHITE, NAVY_D, rtl=False),
    T_("این اشتباه رو نکن!", 100, GOLD), chip("همه‌ی مدارک لازم", fa("Black", 58), GREEN, NAVY_D)], "../out/cover-Wegweiser-Besuchsvisum.jpg")

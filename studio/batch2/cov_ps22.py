from reel import *
bg = R.make_bg().convert("RGBA") if hasattr(R, "make_bg") else Image.new("RGBA", (W, H), NAVY)
header("مالیات").draw(bg, 30)
items = [T_("پول مالیات ۲۰۲۲", 96), T_("رو پس بگیر!", 110, GOLD),
         chip("فقط تا ۳۱ دسامبر ۲۰۲۶", fa("Black", 60), RED, WHITE),
         T_("میانگین برگشت", 54, SOFT), euro("۱۱۷۲", GOLD, 170)]
gap = 50; Ht = sum(i.height for i in items) + gap * (len(items) - 1); y = (H - Ht) // 2 - 170
for im in items: bg.alpha_composite(im, ((W - im.width) // 2, y)); y += im.height + gap
c, b = german_card("Steuererklärung", "اظهارنامه‌ی مالیاتی")
bg.alpha_composite(c, ((W - c.width) // 2, y + 20)); bg.alpha_composite(b, ((W - b.width) // 2, y - 10))
bg.convert("RGB").save("../out/cover-Wegweiser-Steuer2022.jpg", quality=92)

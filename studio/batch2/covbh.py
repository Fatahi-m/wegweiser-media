from kgen import *
bg = add_brand(make_bg()); h = header("ئیقامەی دائیمی"); h.draw(bg, 30)
W_=(255,255,255)
items = [kchip("Behinderung", KRED, W_, 100, latin=True), fitT("یان نەخۆشیت هەیە؟", 92, 960, INK),
         fitT("ئیقامەی دائیمی", 100, 960, GREEN), kchip("مەرجەکان لادەبرێن", GREEN, W_, 60),
         kcard("§ 9 Abs. 2 AufenthG", "مافی خۆتە!")]
gap = 50; Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 - 40
for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
bg.convert("RGB").save("../out/cover-Kurdi-Behinderung-Daimi.jpg", quality=92)

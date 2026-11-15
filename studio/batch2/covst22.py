from kgen import *
bg = add_brand(make_bg()); header("باج · Steuer").draw(bg, 30)
W_=(255,255,255)
items = [fitT("پارەی باجی ٢٠٢٢", 100, 960, INK), fitT("وەربگرەوە!", 110, 960, GREEN),
         kchip("تەنها تا ٣١ی دیسەمبەری ٢٠٢٦", KRED, W_, 60), T("بە تێکڕایی", 56, MUTED),
         big_euro("1.172 €", GREEN, 170), kcard("Steuererklärung", "بەیاننامەی باج")]
gap = 44; Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 - 50
for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
bg.convert("RGB").save("../out/cover-Kurdi-Steuer2022.jpg", quality=92)

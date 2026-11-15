from kgen import *
bg = add_brand(make_bg()); h = header("ئیقامەی پەنابەری"); h.draw(bg, 30)
items = [T("ئیقامەی", 84, MUTED), kchip("§ 25 Abs. 2", INK, (255,255,255), 96, latin=True),
         fitT("٤ شتی زۆر گرنگ", 100, 960, KRED), kchip("subsidiärer Schutz", GREEN, (255,255,255), 58, latin=True),
         kcard("Familiennachzug", "ڕاگیراوە!")]
gap = 50; Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 - 40
for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
bg.convert("RGB").save("../out/cover-Kurdi-25-2.jpg", quality=92)

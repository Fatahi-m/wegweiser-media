from kgen import *
from ks_255 import bubble
bg = add_brand(make_bg()); header("Duldung").draw(bg, 30)
W_=(255,255,255)
items = [bubble(["دولدونگ ئەپشیگونم وەرگرتیوە", "٩ مانگە لێرەم"], head="وەڵامی پرسیارەکەت"),
         kchip("Duldung", INK, W_, 90, latin=True), fitT("+ Ausbildung = ڕێگای ئیقامە", 92, 960, GREEN),
         kcard("Ausbildungsduldung", "§ 60c AufenthG".replace("§ 60c AufenthG", "مەرج و هەنگاوەکان"))]
gap = 50; Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 - 40
for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
bg.convert("RGB").save("../out/cover-Kurdi-Ausbildungsduldung.jpg", quality=92)

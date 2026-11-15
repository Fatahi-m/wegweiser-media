from kgen import *
from kremark import remark as _remark
W_ = (255, 255, 255)
def cov(topic, items, out, dy=-40, gap=50):
    bg = add_brand(make_bg()); header(topic).draw(bg, 30)
    Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 + dy
    for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
    bg.convert("RGB").save(out, quality=92)
cov("ئیقامەی 25.5", [kchip("§ 25 Abs. 5", INK, W_, 130, latin=True), fitT("١٨ مانگە Duldungت هەیە؟", 66, 960, INK), fitT("بە پێی یاسا دەبێت ئیقامەت بدەنێ!", 74, 960, KRED),
    _remark("§ 25 ABS. 5 AUFENTHG", w=900), kchip("دەتوانیت کاریش بکەیت!", GREEN, W_, 62)], "../out/cover-Kurdi-25-5-Serie.jpg")

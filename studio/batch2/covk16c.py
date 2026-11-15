from kgen import *
from kremark import remark as _remark
W_ = (255, 255, 255)
def cov(topic, items, out, dy=-40, gap=50):
    bg = add_brand(make_bg()); header(topic).draw(bg, 30)
    Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 + dy
    for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
    bg.convert("RGB").save(out, quality=92)
cov("پارە بۆ کاری تایبەت", [fitT("دەتەوێت کاری خۆت دەست پێ بکەیت؟", 62, 960, INK), T("تا ٥٠٠٠ یۆرۆ", 150, KRED),
    fitT("لە Jobcenter، بێ گەڕاندنەوە!", 74, 960, INK), kchip("§ 16c SGB II", INK, W_, 80, latin=True),
    kchip("چۆن داوا بکەیت؟", GREEN, W_, 60)], "../out/cover-Kurdi-16c.jpg")

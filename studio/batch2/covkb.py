from kgen import *
from kremark import remark as _remark
W_ = (255, 255, 255)
def cov(topic, items, out, dy=-40, gap=50):
    bg = add_brand(make_bg()); header(topic).draw(bg, 30)
    Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 + dy
    for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
    bg.convert("RGB").save(out, quality=92)
cov("ڤیزای سەردان", [fitT("دایک و باوکت بێنە ئەڵمانیا؟", 96, 960, INK), kchip("Schengen-Visum", INK, W_, 90, latin=True),
    fitT("ئەم هەڵەیە مەکە!", 100, 960, KRED), kchip("هەموو بەڵگەنامەکان", GREEN, W_, 62)], "../out/cover-Kurdi-Besuchsvisum.jpg")

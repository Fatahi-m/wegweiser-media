"""Generic Persian (navy) reel: stacked scenes like kgen. usage: pgen.py module audio out [--frames ...]"""
import sys, importlib
argv = list(sys.argv)
from reel import *
import reel
TOP, BOT = 300, 1450
ICON = {"ok": icon_check, "no": icon_cross, "info": info_icon}
def mk(it):
    k = it[0]
    if k == "title": return T_(it[1], it[2] if len(it) > 2 else 80, it[3] if len(it) > 3 else WHITE), "c"
    if k == "text":
        sz = it[2] if len(it) > 2 else 52
        while text_size(it[1], fa("Bold", sz), rtl=True)[0][2] > 960 and sz > 28: sz -= 2
        return T_(it[1], sz, it[3] if len(it) > 3 else WHITE, "Bold"), "c"
    if k == "chip":
        latin = len(it) > 5 and it[5]
        f = la("Black", it[4]) if latin else fa("Black", it[4])
        return chip(it[1], f, it[2], it[3], rtl=not latin), "c"
    if k == "card":
        c, b = german_card(it[1], it[2]); im = Image.new("RGBA", (c.width, c.height + 30), (0, 0, 0, 0))
        im.alpha_composite(c, (0, 30)); im.alpha_composite(b, ((c.width - b.width) // 2, 0)); return im, "c"
    if k == "row":
        ic = it[2]; icon = num_icon(ic) if isinstance(ic, int) else ICON[ic]
        return row(it[1], icon, sub=it[3] if len(it) > 3 else None), "row"
    if k == "big": return big(it[1], it[2] if len(it) > 2 else GOLD, it[3] if len(it) > 3 else 170), "c"
    if k == "img": return it[1], "c"
    raise ValueError(k)
def build_from(spec):
    els = [header(spec["topic"])]
    els.append(El(T_("اطلاعات عمومی · وضعیت اکتبر ۲۰۲۶ · جای مشاوره‌ی رسمی نیست", 28, (150, 170, 200), "Medium"), cx, 1640, 0.3, anim="fade", anchor="c"))
    lab = text_sprite("منبع:", fa("Bold", 30), (150, 170, 200), rtl=True); src = text_sprite(spec["source"], la("Bold", 30), (150, 170, 200))
    im = Image.new("RGBA", (src.width + 12 + lab.width, max(src.height, lab.height)), (0, 0, 0, 0))
    im.alpha_composite(src, (0, (im.height - src.height) // 2)); im.alpha_composite(lab, (src.width + 12, (im.height - lab.height) // 2))
    els.append(El(im, cx, 1590, 0.3, anim="fade", anchor="c"))
    for sc, (times, end) in zip(spec["scenes"], spec["timing"]):
        made = [mk(it) for it in sc]; gap = 30
        Ht = sum(m[0].height for m in made) + gap * (len(made) - 1); y = TOP + max(0, (BOT - TOP - Ht) // 2)
        for (img, mode), t, it in zip(made, times, sc):
            if mode == "row": els.append(El(img, 80, y, t, end, anim="right"))
            else: els.append(El(img, cx, y, t, end, anim="pop" if it[0] in ("chip", "card", "big") else "up", anchor="c"))
            y += img.height + gap
    o = []; outro(o, spec["outro_t"], *spec["outro"])
    for e in o:
        if isinstance(e, El): e.y += OFF
    return els + o
if __name__ == "__main__":
    spec = importlib.import_module(argv[1]).SPEC
    R.build = lambda _T: build_from(spec)
    tt = [float(x) for x in argv[argv.index("--frames") + 1].split(",")] if "--frames" in argv else None
    R.render({"total": spec["total"]}, argv[2], argv[3], tt)

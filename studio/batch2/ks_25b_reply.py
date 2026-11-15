from kbase import *
import ks_25b, copy
W_ = (255,255,255)
def bubble():
    w = 900
    lines = ["واز له دروبینن عه یبه ۱۱ساله ئیقامه م نیه", "۵ساله ئیش ئه که م ئاستي زمانيشم B2"]
    hd = T("کامێنتێک لە پەیجەکەمان", 34, MUTED, "Bold")
    ls = [fitT(l, 50, w - 160, INK, "Bold") for l in lines]
    av = Image.new("RGBA", (84, 84), (0, 0, 0, 0)); ImageDraw.Draw(av).ellipse((0, 0, 83, 83), fill=(205, 212, 208))
    ImageDraw.Draw(av).ellipse((27, 14, 57, 44), fill=W_); ImageDraw.Draw(av).ellipse((14, 50, 70, 100), fill=W_)
    h = 40 + hd.height + 12 + sum(l.height for l in ls) + 8 * (len(ls) - 1) + 44
    c = rounded(w, h, 40, W_, outline=GREEN_L, ow=4)
    c.alpha_composite(av, (w - 34 - 84, 34))
    xr = w - 34 - 84 - 22; y = 40
    c.alpha_composite(hd, (xr - hd.width, y)); y += hd.height + 12
    for l in ls: c.alpha_composite(l, (xr - l.width, y)); y += l.height + 8
    tail = Image.new("RGBA", (w, h + 30), (0, 0, 0, 0)); tail.alpha_composite(c, (0, 0))
    ImageDraw.Draw(tail).polygon([(w - 160, h - 4), (w - 110, h - 4), (w - 150, h + 28)], fill=W_)
    return shadowed(tail, radius=18, off=(0, 10), alpha=60)
SPEC = copy.deepcopy({k: v for k, v in ks_25b.SPEC.items()})
SPEC["scenes"] = [[("img", bubble(), 4.0), ("title", "سڵاو برا، ئەم ڤیدیۆیە وەڵامی تۆیە 💚".replace(" 💚", ""), 66, GREEN),
                   ("text", "١١ ساڵ و ٥ ساڵ کار و B2...", 56), ("title", "لەوانەیە مافی ئیقامەت هەبێت! 👇".replace(" 👇", ""), 70, KRED)]] + ks_25b.SPEC["scenes"]

from kgen import *
W_ = (255, 255, 255)
def remark(code):
    w, h = 760, 150
    c = rounded(w, h, 18, (226, 228, 230), outline=(190, 194, 198), ow=3)
    a = text_sprite("ANMERKUNGEN/REMARKS", la("Bold", 26), (70, 74, 80)); c.alpha_composite(a, (36, 20))
    b = text_sprite(code, ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 54), (40, 44, 50)); c.alpha_composite(b, (36, 62))
    return shadowed(c, radius=14, off=(0, 8), alpha=50)
from PIL import ImageFont
def pair(code, label, sub, col):
    r = remark(code); arrow = T("⬇".replace("⬇", "▼"), 40, col) if False else None
    tag = kchip(label, col, W_, 60, latin=True); s = T(sub, 46, col, "Bold")
    im = Image.new("RGBA", (max(r.width, tag.width, s.width), r.height + 20 + tag.height + 10 + s.height), (0, 0, 0, 0))
    im.alpha_composite(r, ((im.width - r.width) // 2, 0)); im.alpha_composite(tag, ((im.width - tag.width) // 2, r.height + 20))
    im.alpha_composite(s, ((im.width - s.width) // 2, r.height + 30 + tag.height)); return im
bg = add_brand(make_bg()); header("کارتی ئیقامە").draw(bg, 30)
items = [fitT("لەسەر کارتەکەت چی نووسراوە؟", 80, 980, INK),
         pair("25 ABS.2 (3 ASYLG)", "Flüchtling", "پەنابەر · ئیقامەی ٣ ساڵ", GREEN),
         pair("25 ABS.2 (4 ASYLG)", "subsidiärer Schutz", "سەرەتا ١ ساڵ، دواتر ٢ ساڵ", KRED),
         kchip("تۆ کامیانت هەیە؟ لە کۆمێنت بنووسە: ٣ یان ٤", SUN, INK, 44),
         text_sprite("سەرچاوە: § 3 + § 4 AsylG · § 26 Abs. 1 AufenthG".replace("سەرچاوە: ", ""), la("Bold", 30), MUTED)]
gap = 56; Ht = sum(i.height for i in items) + gap * (len(items) - 1); y = (H - Ht) // 2
for im in items: bg.alpha_composite(im, ((W - im.width) // 2, y)); y += im.height + gap
bg.convert("RGB").save("../out/Story-Kurdi-AsylG-3-4.jpg", quality=93)

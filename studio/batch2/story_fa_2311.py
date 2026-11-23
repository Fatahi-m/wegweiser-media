"""Persian stories 23.11.2026 (support / quiz / teaser). Look of story_fa_dm.py, new handle + compass logo (reel.py header)."""
import sys
from reel import *
from render import glow
def para(s, size=40, col=WHITE, maxw=940, w="Bold"):
    words=s.split(); lines=[]; cur=""
    for wd in words:
        t=(cur+" "+wd).strip()
        if T_(t,size,col,w).width>maxw and cur: lines.append(cur); cur=wd
        else: cur=t
    lines.append(cur)
    ims=[T_(l,size,col,w) for l in lines]; lh=int(size*1.55)
    out=Image.new("RGBA",(max(i.width for i in ims), lh*len(ims)),(0,0,0,0))
    for k,i in enumerate(ims): out.alpha_composite(i,((out.width-i.width)//2, k*lh+(lh-i.height)//2))
    return out
def gap_box(h): return Image.new("RGBA", (10, h), (0, 0, 0, 0))
def lchip(s, size, bg, fg): return chip(s, la("Black", size), bg, fg, rtl=False)
def handle_line():
    lg = Image.open(D + "/brand/compass-fa.png").convert("RGBA").resize((80, 80), Image.LANCZOS)
    t = text_sprite("@wegweiser_farsi", la("Bold", 42), SOFT)
    im = Image.new("RGBA", (80 + 18 + t.width, 80), (0, 0, 0, 0)); im.alpha_composite(lg, (0, 0)); im.alpha_composite(t, (98, (80 - t.height) // 2))
    return im
def story(head, items, out, gap=40, top=260):
    bg = R.make_bg().convert("RGBA")
    g1 = glow(RED, 360, 50); bg.alpha_composite(g1, (W - g1.width // 2 - 120, -g1.height // 3))
    g2 = glow((60, 130, 230), 420, 60); bg.alpha_composite(g2, (-g2.width // 2, H - g2.height // 2 - 100))
    header(head).draw(bg, 30)
    y = top
    for im in items: bg.alpha_composite(im, ((W - im.width) // 2, y)); y += im.height + gap
    print(out, "content ends at", y - gap)
    h = handle_line(); bg.alpha_composite(h, ((W - h.width) // 2, 1540))
    bg.convert("RGB").save(out, quality=93)

O = sys.argv[1] if len(sys.argv) > 1 else "../out"

# 1) support request (angle: the work behind every video)
story("یه حرف کوتاه", [
 T_("پشت هر ویدیو", 96, GOLD),
 para("ساعت‌ها قانون خوندن و منبع چک کردن هست، تا تو مجانی و بدون سردرگمی جوابت رو بگیری.", 46),
 para("اگه یه ویدیو به کارت اومد، با یه لایک و یه فالو بهمون بگو. همین باعث میشه به دست بقیه هم برسه.", 46, SOFT),
 chip("لایک کن، فالو کن", fa("Black", 60), GOLD, NAVY_D),
 para("حتماً یه نفر توی گوشیت هست که همین الان این اطلاعات رو لازم داره. ویدیو رو از همین پیج براش بفرست.", 46),
 chip("همین الان براش بفرست", fa("Black", 60), GREEN, NAVY_D),
 T_("دمت گرم که همراهمونی", 62, GOLD),
], f"{O}/fa-1.jpg", gap=32, top=250)

# 2) quiz: refugee travel document (blue) valid for all countries except the home country – empty area for the quiz sticker
story("کوییز سفر", [
 T_("تو می‌دونی؟", 104, GOLD),
 lchip("Reiseausweis für Flüchtlinge", 50, CARD, WHITE),
 para("با پاس آبی پناهندگی، به کدوم کشور نمی‌تونی سفر کنی؟", 62, WHITE, maxw=940),
 T_("جوابت رو توی کوییز بزن!", 44, SOFT, "Bold"),
 gap_box(400),
 text_sprite("Quelle: Art. 28 GFK, § 72 AsylG", la("Bold", 30), SOFT),
], f"{O}/fa-2.jpg", gap=40, top=280)

# 3) teaser of today's 16:00 reel (Wegweiser-BAMF-Heimatreise) + space for question box
story("ویدیوی امروز", [
 chip("امروز ساعت ۱۶:۰۰", fa("Black", 56), RED, WHITE),
 lchip("BAMF", 58, CARD, WHITE),
 T_("سفر به کشور خودت", 100, GOLD),
 T_("و بعدش یه نامه!", 88, WHITE),
 para("بعد از سفر به وطن، نامه‌ی بامف اومده؟ نادیده‌ش نگیر. امروز ۵ نکته‌ی مهمش رو می‌گیم.", 48, SOFT),
 T_("سؤالت رو همین‌جا بپرس", 52, GOLD, "Bold"),
 gap_box(300),
], f"{O}/fa-3.jpg", gap=38, top=265)

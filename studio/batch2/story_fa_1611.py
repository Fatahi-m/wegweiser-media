"""Persian stories 16.11.2026 (support / quiz / teaser). Look of story_fa_dm.py, new handle + compass logo (reel.py header)."""
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
def lchip(s, size, bg, fg): return chip(s, la("Black", size), bg, fg)
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

# 1) support request
story("یه خواهش کوچیک", [
 T_("دوستای عزیز", 96, GOLD),
 para("هر روز ساعت ۱۶ یه ویدیوی تازه اینجا می‌ذاریم: اقامت، جاب‌سنتر و قانون‌های جدید، با منبع و به زبون ساده.", 50),
 para("اگه ویدیوها به دردت می‌خوره، یه لایک و یه فالو باعث میشه اینستاگرام اون‌ها رو به آدم‌های بیشتری نشون بده.", 50, SOFT),
 chip("فالو کن و لایک کن", fa("Black", 60), GOLD, NAVY_D),
 para("کسی رو می‌شناسی که این اطلاعات لازمش میشه؟ ویدیو رو از همین پیج براش بفرست.", 50),
 chip("برای یه دوست بفرست", fa("Black", 60), GREEN, NAVY_D),
 T_("ممنون که همراه مایی", 66, GOLD),
], f"{O}/fa-1.jpg", gap=42, top=270)

# 2) quiz (subsidiär = 3 years since 27.02.2024) – empty area for the IG quiz sticker
story("کوییز امروز", [
 T_("تو می‌دونی؟", 104, GOLD),
 lchip("subsidiärer Schutz", 56, CARD, WHITE),
 para("کسی که حمایت تکمیلی گرفته، اولین کارت اقامتش چند ساله‌ست؟", 62, WHITE, maxw=940),
 T_("خیلیا هنوز جواب قدیمی رو فکر می‌کنن!", 44, SOFT, "Bold"),
 gap_box(400),
 text_sprite("Quelle: § 26 Abs. 1 S. 2 AufenthG (seit 27.02.2024)", la("Bold", 30), SOFT),
], f"{O}/fa-2.jpg", gap=40, top=280)

# 3) teaser of today's 16:00 reel + space for question box
story("ویدیوی امروز", [
 chip("امروز ساعت ۱۶:۰۰", fa("Black", 56), RED, WHITE),
 T_("روی کارتت ۲۵ نوشته؟", 92, WHITE),
 T_("ولی کدوم ۲۵؟", 110, GOLD),
 lchip("Abs. 1 – 5   |   25a   |   25b", 46, CARD, WHITE),
 para("هر کدومش حق‌های متفاوتی داره؛ تو کدومی؟", 50, SOFT),
 T_("سؤالت رو اینجا بپرس", 52, GOLD, "Bold"),
 gap_box(320),
], f"{O}/fa-3.jpg", gap=40, top=270)

"""Persian stories 19.11.2026 (support / quiz / teaser). Look of story_fa_dm.py, new handle + compass logo (reel.py header)."""
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

# 1) support request
story("یه لحظه وقت داری؟", [
 T_("ممنون که هستی", 100, GOLD),
 para("هر روز ساعت ۱۶ یه ویدیو می‌ذاریم تا هیچ‌کس توی اداره‌های آلمان سردرگم نمونه.", 50),
 para("خیلیا ویدیوها رو می‌بینن ولی لایک نمی‌کنن. همین یه لایک کمک می‌کنه ویدیو به آدم‌های بیشتری برسه.", 50, SOFT),
 chip("یه لایک، یه فالو", fa("Black", 60), GOLD, NAVY_D),
 para("یه نفر رو در نظر بگیر که تازه اومده آلمان یا یه نامه‌ی اداری گیجش کرده. ویدیو رو از همین پیج براش بفرست.", 50),
 chip("برای همون یه نفر بفرست", fa("Black", 60), GREEN, NAVY_D),
 T_("کمک تو، کمک به یکی دیگه‌ست", 58, GOLD),
], f"{O}/fa-1.jpg", gap=42, top=270)

# 2) quiz (§ 25 Abs. 3 is on the exclusion list of § 10 Abs. 1 Nr. 2 StAG -> NE first) – empty area for the IG quiz sticker
story("یه سؤال از تو", [
 T_("تو می‌دونی؟", 104, GOLD),
 lchip("§ 25 Abs. 3 AufenthG", 56, CARD, WHITE),
 para("با این اقامت می‌شه مستقیم درخواست پاس آلمانی داد؟", 62, WHITE, maxw=940),
 T_("جوابش خیلیا رو غافلگیر می‌کنه!", 44, SOFT, "Bold"),
 gap_box(400),
 text_sprite("Quelle: § 10 Abs. 1 Nr. 2 StAG", la("Bold", 30), SOFT),
], f"{O}/fa-2.jpg", gap=40, top=280)

# 3) teaser of today's 16:00 reel (Klarna/PayPal BNPL, EU 2023/2225 from 20.11.2026) + space for question box
story("ویدیوی امروز", [
 chip("امروز ساعت ۱۶:۰۰", fa("Black", 56), RED, WHITE),
 lchip("Klarna   |   PayPal", 58, CARD, WHITE),
 T_("خرید قسطی", 116, GOLD),
 T_("از فردا عوض میشه!", 88, WHITE),
 para("از ۲۰ نوامبر خیلی از خریدهای «بعداً پرداخت» از نظر قانون وام حساب میشن. یعنی چی برای تو؟", 48, SOFT),
 T_("سؤالت رو اینجا بپرس", 52, GOLD, "Bold"),
 gap_box(300),
], f"{O}/fa-3.jpg", gap=38, top=265)

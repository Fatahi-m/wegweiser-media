import sys
sys.path.insert(0,'.')
from covers import *
sys.path.insert(0, D + "/wohngeld")
from wohngeld import icon_house
ARTC={"der":(37,99,235),"die":(226,35,26),"das":(22,163,74)}

def fa_wohngeld():
    c = gradient_bg((14,52,108),(6,24,52),[(540,700,440,(226,35,26),60),(540,1300,380,(255,196,61),50)])
    rays(c,540,780,(255,255,255),a=9)
    brand_strip(c,300)
    place(c, icon_house(240), 540, 430, sh=True)
    y = place(c, fit("کرایه‌ی خونه‌ت سنگینه؟", lambda s: fa("Black",s), 960, 96, rtl=True, fill=WHITE), 540, 700) + 6
    y = place(c, fit("دولت بخشیش رو می‌ده!", lambda s: fa("Black",s), 960, 96, rtl=True, fill=GOLD), 540, y, sh=True) + 40
    card = box(tsprite("Wohngeld", la("Black",120), PNAVY), WHITE, 60, 22, 36)
    y = place(c, card, 540, y, sh=True, rot=-2) + 40
    q = box(fit("ماهی چقدر بهت می‌رسه؟", lambda s: fa("Black",s), 820, 58, rtl=True, fill=WHITE), CARD, 40, 18, 30)
    place(c, q, 540, y, sh=True)
    footer(c, "@wegweiser.deutschland")
    place(c, box(fit("خیلی‌ها خبر ندارن!", lambda s: fa("Black",s), 900, 66, rtl=True, fill=WHITE), RED, 44, 20, 34), 540, 1440, sh=True)
    return c

def fa_5words():
    c = gradient_bg((14,52,108),(6,24,52),[(540,800,460,(37,99,235),70)])
    rays(c,540,820,(255,255,255),a=9)
    brand_strip(c,300)
    b = Image.new("RGBA",(200,200),(0,0,0,0)); ImageDraw.Draw(b).ellipse((0,0,199,199),fill=RED)
    n = tsprite("۵", fa("Black",140), WHITE, rtl=True); b.alpha_composite(n,((200-n.width)//2,(200-n.height)//2-10))
    place(c, b, 540, 420, sh=True)
    y = place(c, fit("کلمه‌ی آلمانی که توی", lambda s: fa("Black",s), 960, 80, rtl=True, fill=WHITE), 540, 650)
    y = place(c, fit("هر اداره لازمت می‌شه", lambda s: fa("Black",s), 960, 84, rtl=True, fill=GOLD), 540, y, sh=True) + 40
    arts = ["der","die","der","der","die"]; rots=[-4,3,-2,4,-3]
    for i,a in enumerate(arts[:4]):
        cardw = Image.new("RGBA",(420,150),(0,0,0,0)); ImageDraw.Draw(cardw).rounded_rectangle((0,0,419,149),30,fill=WHITE)
        at = tsprite(a, la("Black",50), ARTC[a]); qs = tsprite("?????", la("Black",58), PNAVY)
        cardw.alpha_composite(at,(30,(150-at.height)//2)); cardw.alpha_composite(qs,(30+at.width+16,(150-qs.height)//2))
        x = 300 if i%2==0 else 780; yy = y + (i//2)*175
        place(c, cardw, x, yy, sh=True, rot=rots[i])
    footer(c, "@wegweiser.deutschland")
    place(c, box(fit("تو چندتاش رو بلدی؟", lambda s: fa("Black",s), 900, 70, rtl=True, fill=WHITE), RED, 44, 20, 34), 540, 1440, sh=True)
    return c

for k,f in {"Reel-Wohngeld":fa_wohngeld,"Reel-5-Kalame-01":fa_5words}.items():
    f().convert("RGB").save(OUT+f"cover-{k}.jpg",quality=92)
print("ok")

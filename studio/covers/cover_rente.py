import sys; sys.path.insert(0,'.')
from covers import *
def de_rente():
    c = gradient_bg((20,34,58),(8,14,26),[(880,640,380,(242,182,50),65),(160,1450,400,(226,104,90),60)])
    rays(c,540,880,(242,182,50),a=12)
    y = 300
    y = place(c, fit("Wie viel", lambda s: la("Black",s), 900, 130, fill=(238,241,244)), 540, y) - 8
    y = place(c, fit("RENTE", lambda s: la("Black",s), 960, 250, fill=MUST), 540, y, sh=True) - 8
    y = place(c, fit("bekommst du wirklich?", lambda s: la("Black",s), 960, 100, fill=(238,241,244)), 540, y) + 60
    # two bars: today vs pension
    base = y + 520; bw = 300
    for i,(lab,top,h,col) in enumerate([("HEUTE","2.700 €",440,(108,199,154)),("RENTE","?.??? €",270,(226,104,90))]):
        x = 150 + i*(bw+80)
        bar = Image.new("RGBA",(bw,h),(0,0,0,0)); ImageDraw.Draw(bar).rounded_rectangle((0,0,bw-1,h+30),30,fill=col)
        c.alpha_composite(bar,(x,base-h))
        t = tsprite(top, la("Black",64), (238,241,244) if i==0 else MUST); c.alpha_composite(t,(x+(bw-t.width)//2, base-h-t.height-10))
        l = tsprite(lab, la("Black",48), NAVY); c.alpha_composite(l,(x+(bw-l.width)//2, base-70))
    ImageDraw.Draw(c).rounded_rectangle((110,base,970,base+10),5,fill=(60,80,110))
    # arrow + gap label
    g = box(tsprite("LÜCKE?", la("Black",56), MUST), NAVY, 30, 14, 22)
    place(c, g, 680, base-215, sh=True, rot=-6)
    n = netti(250, "shock"); n, p = shadow(n)
    c.alpha_composite(n, (W-250-30-p, base+40-p))
    place(c, tsprite("Die Zahl schockt!", la("ExtraBold",64), (238,241,244)), 420, base+110)
    footer(c, "@Geld-ohne-Filter")
    return c
de_rente().convert("RGB").save(OUT+"cover-YT-Rente.jpg", quality=92); print("ok")

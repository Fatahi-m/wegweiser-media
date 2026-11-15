import sys
sys.path.insert(0,'.')
from covers import *
sys.path.insert(0, D + "/batch2")
from reel import passport

def euro_big(num, col, size):
    n = tsprite(num, fa("Black", size), col, rtl=True); e = tsprite("€", la("Black", int(size*.8)), col)
    im = Image.new("RGBA", (n.width+e.width+10, max(n.height,e.height)), (0,0,0,0))
    im.alpha_composite(n,(0,(im.height-n.height)//2)); im.alpha_composite(e,(n.width+10,(im.height-e.height)//2+6)); return im

def fa_kinder():
    c = gradient_bg((14,52,108),(6,24,52),[(540,800,460,(255,196,61),55),(540,1300,380,(226,35,26),50)])
    rays(c,540,820,(255,255,255),a=9); brand_strip(c,300)
    y = place(c, fit("کیندرگلد رو می‌شناسی...", lambda s: fa("Black",s), 960, 84, rtl=True, fill=WHITE), 540, 400) + 10
    y = place(c, fit("ولی این یکی رو چی؟", lambda s: fa("Black",s), 960, 100, rtl=True, fill=GOLD), 540, y, sh=True) + 40
    card = box(tsprite("Kinderzuschlag", la("Black",104), PNAVY), WHITE, 56, 22, 36)
    y = place(c, card, 540, y, sh=True, rot=-2) + 40
    t = tsprite("تا", fa("Black",80), SOFT if 'SOFT' in globals() else WHITE, rtl=True)
    eb = euro_big("۲۹۷", GOLD, 210)
    row = Image.new("RGBA",(t.width+eb.width+30,max(t.height,eb.height)),(0,0,0,0))
    row.alpha_composite(eb,(0,(row.height-eb.height)//2)); row.alpha_composite(t,(eb.width+30,(row.height-t.height)//2))
    y = place(c, row, 540, y, sh=True) + 10
    place(c, fit("در ماه برای هر بچه", lambda s: fa("Bold",s), 900, 60, rtl=True, fill=WHITE), 540, y)
    footer(c, "@wegweiser.deutschland")
    place(c, box(fit("خیلیا حقشونه و نمی‌دونن!", lambda s: fa("Black",s), 900, 64, rtl=True, fill=WHITE), RED, 44, 20, 34), 540, 1440, sh=True)
    return c

def fa_einb():
    c = gradient_bg((14,52,108),(6,24,52),[(540,720,440,(226,35,26),60),(540,1250,380,(255,196,61),45)])
    rays(c,540,720,(255,255,255),a=9); brand_strip(c,300)
    place(c, passport(300), 540, 400, sh=True, rot=-6)
    y = place(c, fit("پاسپورت آلمانی", lambda s: fa("Black",s), 960, 110, rtl=True, fill=WHITE), 540, 880) + 6
    y = place(c, fit("با این ۴ شرط", lambda s: fa("Black",s), 960, 110, rtl=True, fill=GOLD), 540, y, sh=True) + 40
    place(c, box(fit("شرط سوم رو خیلیا ندارن!", lambda s: fa("Black",s), 860, 58, rtl=True, fill=WHITE), CARD, 40, 18, 30), 540, y, sh=True)
    footer(c, "@wegweiser.deutschland")
    place(c, box(fit("Einbürgerung 2026", lambda s: la("Black",s), 900, 70, fill=WHITE), RED, 44, 20, 34), 540, 1440, sh=True)
    return c

def fa_nl():
    c = gradient_bg((14,52,108),(6,24,52),[(540,800,460,(37,99,235),70)])
    rays(c,540,800,(255,255,255),a=9); brand_strip(c,300)
    y = place(c, fit("اقامت دائم آلمان", lambda s: fa("Black",s), 960, 104, rtl=True, fill=WHITE), 540, 420) + 6
    y = place(c, fit("فقط بعد از", lambda s: fa("Black",s), 960, 90, rtl=True, fill=SOFT if 'SOFT' in globals() else WHITE), 540, y) + 10
    y = place(c, fit("۲۱ ماه؟!", lambda s: fa("Black",s), 960, 230, rtl=True, fill=GOLD), 540, y, sh=True) + 30
    card = box(tsprite("Niederlassungserlaubnis", la("Black",70), PNAVY), WHITE, 44, 20, 32)
    place(c, card, 540, y, sh=True, rot=-2)
    footer(c, "@wegweiser.deutschland")
    place(c, box(fit("ببین تو کدوم دسته‌ای", lambda s: fa("Black",s), 900, 66, rtl=True, fill=WHITE), RED, 44, 20, 34), 540, 1440, sh=True)
    return c

for k,f in {"Reel-Kinderzuschlag":fa_kinder,"Reel-Einbuergerung":fa_einb,"Reel-Niederlassung":fa_nl}.items():
    f().convert("RGB").save(OUT+f"cover-{k}.jpg",quality=92)
print("ok")

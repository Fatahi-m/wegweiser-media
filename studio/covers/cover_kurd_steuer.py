import sys; sys.path.insert(0,'.')
from covers import *
def ku_steuer():
    c = gradient_bg((14,52,108),(6,24,52),[(540,900,460,(255,196,61),60),(540,1350,380,(226,35,26),45)])
    rays(c,540,900,(255,255,255),a=9); brand_strip(c,300)
    y = place(c, fit("ئەم پارەیە هی تۆیە!", lambda s: fa("Black",s), 960, 110, rtl=True, fill=WHITE), 540, 600) + 30
    y = place(c, fit("+1.000 €", lambda s: la("Black",s), 960, 230, fill=GOLD), 540, y, sh=True) + 30
    card = box(tsprite("Steuererklärung", la("Black",96), PNAVY), WHITE, 50, 20, 34)
    y = place(c, card, 540, y, sh=True, rot=-2) + 50
    place(c, box(fit("هێشتا وەرت نەگرتۆتەوە؟", lambda s: fa("Black",s), 860, 64, rtl=True, fill=WHITE), RED, 44, 20, 34), 540, y, sh=True)
    return c
ku_steuer().convert("RGB").save("/mnt/user-data/outputs/cover-Kurdi-Steuer.jpg", quality=92); print("ok")

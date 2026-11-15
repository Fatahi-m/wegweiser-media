import sys; sys.argv=[sys.argv[0]]
from sparbuch import *
bg = make_bg()
items = [T("Dein Sparbuch", 120), T("macht dich jedes Jahr", 76, MUTED, "ExtraBold"), T("ärmer", 220, RENT),
         pill("3,3 % Inflation  vs.  0,3 % Zins", PANEL2, MUST, 50, "Black")]
gap = 40; Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 - 60
for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
bg.convert("RGB").save("../out/cover-GoF-Sparbuch.jpg", quality=92)

import sys
sys.path.insert(0,'.')
from covers import *
sys.path.insert(0, D + "/termin")
from termin import calendar
c = gradient_bg((14,52,108),(6,24,52),[(540,700,440,(226,35,26),60),(540,1300,380,(255,196,61),50)])
rays(c,540,780,(255,255,255),a=9)
brand_strip(c,300)
place(c, calendar(250), 540, 400, sh=False)
y = place(c, fit("Termin جاب‌سنتر رو", lambda s: fa("Black",s), 960, 92, rtl=True, fill=WHITE), 540, 790) + 6
y = place(c, fit("فراموش کردی؟", lambda s: fa("Black",s), 960, 120, rtl=True, fill=GOLD), 540, y, sh=True) + 50
q = box(fit("قانون جدید از جولای ۲۰۲۶", lambda s: fa("Black",s), 820, 58, rtl=True, fill=WHITE), CARD, 40, 18, 30)
y = place(c, q, 540, y, sh=True) + 60
place(c, box(fit("بار سوم پشت سر هم = خطر قطع کامل!", lambda s: fa("Black",s), 900, 66, rtl=True, fill=WHITE), RED, 44, 20, 34), 540, max(y, 1380), sh=True)
footer(c, "@wegweiser.deutschland")
c.convert('RGB').save('/mnt/user-data/outputs/cover-Reel-Jobcenter-Termin.jpg', quality=93)

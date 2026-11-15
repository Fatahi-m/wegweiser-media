from kgen import *
bg = add_brand(make_bg()); header("پەیامێک بۆ ئێوە").draw(bg, 30)
W_=(255,255,255)
items = [T("هاوڕێیانی ئازیز 🙏".replace(" 🙏",""), 92, GREEN),
 fitT("تکایە پرسیارەکانتان", 64, 960, INK, "Bold"),
 kchip("لە ژێر پۆستەکان کۆمێنت بکەن", KRED, W_, 60),
 fitT("تا وەڵامتان بدەمەوە و کەسانی تریش", 50, 960, INK, "Bold"),
 fitT("سوود لە وەڵامەکان وەربگرن.", 50, 960, INK, "Bold"),
 krow("نامەی زۆر لە دایرێکت هاتووە و ناگەمە هەمووی", icon=ICONS["info"](), h=150),
 krow("ئەگەر گرنگ بوو، ڤیدیۆی بۆ دروست دەکەم", icon=ICONS["ok"](), h=150),
 kchip("فۆڵۆ بکەن · لایک بکەن · سوپاس ❤".replace(" ❤",""), GREEN, W_, 54)]
gap = 44; Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 + 20
for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
bg.convert("RGB").save("final3/Story-Kurdi-Comment.jpg", quality=93)

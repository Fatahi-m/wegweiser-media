from kgen import *
from kremark import remark as _remark
W_ = (255, 255, 255)
def cov(topic, items, out, dy=-40, gap=50):
    bg = add_brand(make_bg()); header(topic).draw(bg, 30)
    Ht = sum(i.height for i in items) + gap*(len(items)-1); y = (H - Ht)//2 + dy
    for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
    bg.convert("RGB").save(out, quality=92)
cov("سەفەر · بەشی ١", [T("سەفەر بۆ وڵاتی خۆت؟", 90), kchip("§ 25 Abs. 1 · 2 · 3", INK, W_, 80, latin=True),
    fitT("ئیقامەکەت لە مەترسیدایە!", 92, 960, KRED), kchip("§ 47b AufenthG", GREEN, W_, 56, latin=True)], "../out/cover-Kurdi-Safar-1.jpg")
cov("سەفەر · بەشی ٢", [kchip("Duldung · Gestattung", INK, W_, 72, latin=True), T("دەتوانیت سەفەر بکەیت؟", 90),
    fitT("ئاگادار بە!", 110, 960, KRED), kcard("6 Monate", "لە دەرەوە = ئیقامە نامێنێت")], "../out/cover-Kurdi-Safar-2.jpg")
cov("جۆرەکانی ئیقامە", [T("لەسەر کارتەکەت نووسراوە:", 76, MUTED), kchip("§ 25 Abs. 1 · 2 · 3", INK, W_, 90, latin=True),
    fitT("جیاوازییان زۆرە!", 104, 960, KRED), kchip("ئیقامەی دائیمی کەی؟", GREEN, W_, 60)], "../out/cover-Kurdi-Aufenthalt-25-1-2-3.jpg")
cov("ئیقامە بێ پەنابەری", [T("پەنابەرییەکەت ڕەتکرایەوە؟", 84), fitT("هێشتا ٣ ڕێگا هەیە!", 104, 960, KRED),
    kchip("§ 25 Abs. 5 · § 25a · § 25b", INK, W_, 66, latin=True)], "../out/cover-Kurdi-Aufenthalt-25-5-a-b.jpg")
cov("سەفەر · بەشی ٣", [T("ئیقامەی دائیمیت هەیە؟", 88), kchip("§ 26 Abs. 3", INK, W_, 90, latin=True),
    fitT("سەفەر بۆ وڵاتی خۆت؟", 92, 960, KRED), kchip("ئاگادار بە!", GREEN, W_, 60)], "../out/cover-Kurdi-Safar-3.jpg")
cov("پاسپۆرت", [T("پاسپۆرتی وڵاتی خۆت", 92), fitT("مەترسیدارە؟", 120, 960, KRED),
    kchip("Flüchtling · subsidiär · § 25 Abs. 3", INK, W_, 52, latin=True), kchip("وەڵامی پرسیارەکەتان", GREEN, W_, 58)], "../out/cover-Kurdi-Pass-Jawab.jpg")
cov("Spurwechsel", [fitT("چەند ساڵە چاوەڕێی BAMF دەکەیت؟", 76, 960, INK), kchip("Spurwechsel", INK, W_, 100, latin=True),
    fitT("ڕێگایەک بۆ ئیقامەی کار", 86, 960, GREEN), kchip("بەڵام زۆر ئاگاداربە!", KRED, W_, 60)], "../out/cover-Kurdi-Spurwechsel.jpg")
cov("کام ساڵ دەژمێردرێت؟", [fitT("ساڵەکانت دەژمێردرێن؟", 96, 960, INK), kchip("Duldung · Gestattung", INK, W_, 84, latin=True),
    fitT("بۆ پاسپۆرت و ئیقامەی دائیمی", 70, 960, KRED), kchip("زۆر کەس ئەمە نازانن!", GREEN, W_, 58)], "../out/cover-Kurdi-Salakan.jpg")
cov("25b Abs. 4", [kchip("§ 25b Abs. 4", INK, W_, 120, latin=True), fitT("هاوسەرەکەت 25bی وەرگرتووە؟", 62, 960, INK),
    fitT("تۆ و منداڵەکانیش ئیقامە وەردەگرن!", 80, 960, KRED), _remark("§ 25B ABS. 4 AUFENTHG", w=900),
    kchip("بێ مەرجی ٦ ساڵ!", GREEN, W_, 62)], "../out/cover-Kurdi-25b-Abs4.jpg")
cov("جۆرەکانی Duldung", [fitT("Duldungەکەت ٢ هەفتەیە؟", 90, 960, INK), kchip("60a · 60b · 60c · 60d", INK, W_, 90, latin=True),
    fitT("کامیان باشە، کامیان خراپ؟", 80, 960, KRED), kchip("سەیری کاغەزەکەت بکە!", GREEN, W_, 58)], "../out/cover-Kurdi-Duldung-Arten.jpg")
cov("Einstiegsgeld", [fitT("بۆ چوونە سەر کار", 74, 960, INK), fitT("لە Jobcenter خەڵات وەربگرە!", 80, 960, GREEN),
    kchip("٢٨٠ تا ٥٠٠ یۆرۆ", KRED, W_, 100), fitT("مانگانە، تا ٢٤ مانگ، لەگەڵ مووچەکەت", 58, 960, INK),
    kchip("Einstiegsgeld", INK, W_, 70, latin=True)], "../out/cover-Kurdi-Einstiegsgeld.jpg")
cov("یارمەتیی Jobcenter", [fitT("٥ یارمەتیی دارایی", 110, 960, KRED), fitT("کە Jobcenter پێت دەدات", 78, 960, INK),
    kchip("و کەس پێت ناڵێت!", GREEN, W_, 70), fitT("ژمارە ١ تەنانەت بێ Jobcenter", 58, 960, INK),
    kchip("سەیڤی بکە!", SUN, INK, 58)], "../out/cover-Kurdi-5-Yarmati.jpg")
cov("Duldungی کار", [fitT("Duldungت هەیە و کار دەکەیت؟", 76, 960, INK), kchip("Beschäftigungsduldung", INK, W_, 70, latin=True),
    fitT("٣٠ مانگ، پاشان ئیقامەی 25b", 70, 960, KRED), fitT("دواتر ئیقامەی دائیمی و جنسیە", 60, 960, INK),
    kchip("هەموو مەرجەکان", GREEN, W_, 58)], "../out/cover-Kurdi-Beschaeftigungsduldung.jpg")
cov("ئیقامەی 25a", [kchip("§ 25a", INK, W_, 150, latin=True), fitT("خوار ٢٧ ساڵیت و Duldungت هەیە؟", 62, 960, INK), fitT("ئیقامە بۆ تۆ و خێزانەکەت!", 86, 960, KRED),
    _remark("§ 25A ABS. 1 AUFENTHG", w=900), kchip("تەنها ٣ ساڵ لە ئەڵمانیا!", GREEN, W_, 62)], "../out/cover-Kurdi-25a.jpg")
cov("ئیقامەی 25b", [kchip("§ 25b", INK, W_, 150, latin=True), fitT("ڕەفزت بۆ هاتووە و Duldungت هەیە؟", 62, 960, INK), fitT("ئیقامەیەک هەیە بۆ تۆ!", 90, 960, KRED),
    _remark("§ 25B ABS. 1 AUFENTHG", w=900), kchip("لەگەڵ منداڵ تەنها ٤ ساڵ!", GREEN, W_, 62)], "../out/cover-Kurdi-25b.jpg")

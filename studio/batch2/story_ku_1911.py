"""Kurdish stories 19.11.2026 (support / quiz / teaser). Look of story_k3.py, new handle + compass logo (kbase)."""
import sys; _O = sys.argv[1] if len(sys.argv) > 1 else "../out"; sys.argv = [sys.argv[0]]
exec(open("story_k3.py").read().split("story(\"پەیامێک")[0])

def gap_box(h):
    return Image.new("RGBA", (10, h), (0, 0, 0, 0))

def lat(s, size=40, col=MUTED):
    return text_sprite(s, la("Bold", size), col)

def story2(head, items, out, gap=40, top=250, badge=True):
    bg = make_bg(); header(head).draw(bg, 30)
    y = top
    for im in items: bg.alpha_composite(im, ((W - im.width) // 2, y)); y += im.height + gap
    if badge:
        b = brand_badge(84); bg.alpha_composite(b, ((W - b.width) // 2, 1525))
    print(out, "content ends at", y - gap)
    bg.convert("RGB").save(out, quality=93)

O = _O

# 1) support request
story2("چرکەیەک کاتت هەیە؟", [
 T("سوپاس کە لێرەیت", 96, GREEN),
 para("هەموو ڕۆژێک کاتژمێر ١٦:٠٠ ڤیدیۆیەک دادەنێین، بۆ ئەوەی کەس لە فەرمانگەکانی ئەڵمانیا سەری لێ نەشێوێت.", 50),
 para("زۆر کەس ڤیدیۆکان دەبینن بەڵام لایک ناکەن. تەنها یەک لایک یارمەتی دەدات ڤیدیۆکە بگاتە خەڵکی زیاتر.", 50),
 kchip("یەک لایک، یەک فۆڵۆ", KRED, W_, 62),
 para("بیر لە کەسێک بکەرەوە کە تازە هاتووەتە ئەڵمانیا یان نامەیەکی فەرمی سەری لێ شێواندووە. ڤیدیۆکە لێرەوە بۆی بنێرە.", 50, GREEN),
 kchip("بۆ ئەو کەسەی بنێرە", GREEN, W_, 62),
 T("یارمەتیی تۆ، یارمەتیی کەسێکی ترە", 54, INK),
], f"{O}/ku-1.jpg", gap=32, top=255)

# 2) quiz (§ 16c SGB II: Zuschuss up to 5,000 EUR) – empty area for the IG quiz sticker
story2("پرسیارێک بۆ تۆ", [
 T("تۆ دەزانیت؟", 104, KRED),
 kchip("§ 16c SGB II", GREEN, W_, 60, latin=True),
 para("بۆ دەستپێکردنی کاری سەربەخۆ، جۆبسەنتەر تا چەند یۆرۆت پێدەدات کە نایگەڕێنیتەوە؟", 58, INK, maxw=940),
 T("وەڵامەکەت هەڵبژێرە", 46, MUTED, "Bold"),
 gap_box(420),
 lat("Quelle: § 16c Abs. 1 SGB II (Zuschuss bis 5.000 €)", 30),
], f"{O}/ku-2.jpg", gap=40, top=280)

# 3) teaser of today's 16:00 reel (Klarna/PayPal BNPL) + space for question box
story2("ڤیدیۆی ئەمڕۆ", [
 kchip("ئەمڕۆ کاتژمێر ١٦:٠٠", KRED, W_, 58),
 kchip("Klarna   |   PayPal", SUN, INK, 54, latin=True),
 T("کڕینی قیستی", 112, GREEN),
 fitT("لە سبەینێوە دەگۆڕێت!", 86, 980, INK),
 para("لە ٢٠ی نۆڤەمبەرەوە زۆرێک لە کڕینەکانی «دواتر پارە بدە» بەپێی یاسا وەک قەرز هەژمار دەکرێن. ئەمە بۆ تۆ چی دەگەیەنێت؟", 48),
 T("پرسیارەکەت لێرە بنووسە", 50, KRED, "Bold"),
 gap_box(300),
], f"{O}/ku-3.jpg", gap=36, top=262)

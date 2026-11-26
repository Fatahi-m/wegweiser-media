"""Kurdish stories 26.11.2026 (support / quiz / teaser). Look of story_k3.py, new handle + compass logo (kbase)."""
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

# 1) support request (angle: one share = one person who avoids a costly mistake)
story2("لە ئێمەوە", [
 T("هاوبەشکردنێکی بچووک", 86, GREEN),
 para("زۆر کەس نامەیەک بێ خوێندنەوە لادەنێن یان ماوەیەک لەدەست دەدەن، تەنها لەبەر ئەوەی کەس پێی نەگوتبوون.", 50),
 para("تۆ دەتوانیت ئەو کەسە بیت کە پێیان دەڵێت. ڤیدیۆیەک لەم پەیجەوە بۆ هاوڕێ، خزم یان هاوکارێک بنێرە کە پێویستی پێیەتی.", 50, GREEN),
 kchip("ڤیدیۆیەک بۆ کەسێک بنێرە", GREEN, W_, 60),
 para("ئەگەر هێشتا فۆڵۆت نەکردووین، فۆڵۆمان بکە و لایکی ئەو ڤیدیۆیانە بکە کە سوودیان بۆت هەبوو، با بگەنە خەڵکی زیاتر.", 50),
 kchip("فۆڵۆ بکە، لایک بکە", KRED, W_, 62),
 T("سوپاس کە لەگەڵمانیت", 58, INK),
], f"{O}/ku-1.jpg", gap=28, top=240)

# 2) quiz: Deutschlandticket 66.80 EUR from 01.01.2027 (PLAYBOOK verified facts, law watch 18./25.11) – empty area for the quiz sticker
story2("پرسیاری ئەمڕۆ", [
 T("تۆ دەزانیت؟", 104, KRED),
 kchip("Deutschlandticket 2027", GREEN, W_, 58, latin=True),
 para("لە مانگی یەکی ٢٠٢٧ەوە نرخی مانگانەی ئەم بلیتە دەبێتە چەند؟", 58, INK, maxw=940),
 T("وەڵامەکەت هەڵبژێرە", 46, MUTED, "Bold"),
 gap_box(420),
 lat("Quelle: Verkehrsministerkonferenz, Preis ab 01.01.2027", 30),
], f"{O}/ku-2.jpg", gap=40, top=280)

# 3) teaser of today's 16:00 reel (Kurdi-Pass-Farben) + space for question box
story2("ڤیدیۆی ئەمڕۆ", [
 kchip("ئەمڕۆ کاتژمێر ١٦:٠٠", KRED, W_, 58),
 kchip("Reiseausweis", SUN, INK, 54, latin=True),
 T("پاسەکەت چ ڕەنگێکە؟", 100, GREEN),
 fitT("شین، خۆڵەمێشی یان پاسی وڵاتەکەت؟", 76, 980, INK),
 para("هەڵەیەک لە پاسپۆرتدا دەتوانێت پەنابەرییەکەت بخاتە مەترسییەوە. ئەمڕۆ دەڵێین کام پاس بۆ کام ئیقامەیە.", 48),
 T("پرسیارەکەت لێرە بنووسە", 50, KRED, "Bold"),
 gap_box(300),
], f"{O}/ku-3.jpg", gap=36, top=262)

"""Kurdish stories 16.11.2026 (support / quiz / teaser). Look of story_k3.py, new handle + compass logo (kbase)."""
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
story2("داوایەکی بچووک", [
 T("هاوڕێیانی ئازیز", 96, GREEN),
 para("هەموو ڕۆژێک کاتژمێر ١٦:٠٠ ڤیدیۆیەکی نوێ لێرە دادەنێین: ئیقامە، Jobcenter و یاسا نوێیەکان، بە سەرچاوە و بە کوردییەکی سادە.", 50),
 para("ئەگەر ڤیدیۆکان سوودیان بۆت هەیە، یەک لایک و یەک فۆڵۆ وا دەکات ئینستاگرام بیانگەیەنێتە کەسانی زیاتر.", 50),
 kchip("فۆڵۆ بکە و لایک بکە", KRED, W_, 62),
 para("کەسێک دەناسیت کە پێویستی بەم زانیارییانەیە؟ ڤیدیۆکە لێرەوە بۆی بنێرە.", 50, GREEN),
 kchip("بۆ هاوڕێیەک شێری بکە", GREEN, W_, 62),
 T("سوپاس کە لەگەڵمانیت", 60, INK),
], f"{O}/ku-1.jpg", gap=34, top=255)

# 2) quiz (Minijob 2027) – empty area for the IG quiz sticker
story2("تاقیکردنەوەی ئەمڕۆ", [
 T("تۆ دەزانیت؟", 104, KRED),
 kchip("Minijob", GREEN, W_, 64, latin=True),
 para("لە مانگی یەکی ٢٠٢٧ەوە، مووچەی مانگانە دەتوانێت تا چەند بێت؟", 60, INK, maxw=940),
 T("وەڵامەکەت هەڵبژێرە", 46, MUTED, "Bold"),
 gap_box(430),
 lat("Quelle: Mindestlohn 14,60 € ab 01.01.2027 · § 8 SGB IV", 30),
], f"{O}/ku-2.jpg", gap=40, top=280)

# 3) teaser of today's 16:00 reel + space for question box
story2("ڤیدیۆی ئەمڕۆ", [
 kchip("ئەمڕۆ کاتژمێر ١٦:٠٠", KRED, W_, 58),
 fitT("دووگیانیت و پارەت کەمە؟", 92, 980, GREEN),
 para("یارمەتییەک هەیە کە ناگەڕێنیتەوە، بەڵام تەنها پێش لەدایکبوونی منداڵ داوای دەکەیت.", 52),
 kchip("Bundesstiftung Mutter und Kind", SUN, INK, 44, latin=True),
 T("پرسیارەکەت لێرە بنووسە", 50, KRED, "Bold"),
 gap_box(340),
], f"{O}/ku-3.jpg", gap=38, top=265)

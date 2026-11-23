"""Kurdish stories 23.11.2026 (support / quiz / teaser). Look of story_k3.py, new handle + compass logo (kbase)."""
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

# 1) support request (angle: the work behind every video)
story2("قسەیەکی کورت", [
 T("لە پشت هەر ڤیدیۆیەک", 88, GREEN),
 para("چەندین کاتژمێر خوێندنەوەی یاسا و پشکنینی سەرچاوە هەیە، بۆ ئەوەی تۆ بەخۆڕایی و بەبێ سەرلێشێوان وەڵامەکەت وەربگریت.", 50),
 para("ئەگەر ڤیدیۆیەک سوودی بۆت هەبوو، بە لایکێک و فۆڵۆیەک پێمان بڵێ. ئەمە وا دەکات بگاتە خەڵکی تریش.", 50),
 kchip("لایک بکە، فۆڵۆ بکە", KRED, W_, 62),
 para("بێگومان کەسێک لە مۆبایلەکەتدا هەیە کە ئێستا پێویستی بەم زانیارییانەیە. ڤیدیۆکە لێرەوە بۆی بنێرە.", 50, GREEN),
 kchip("هەر ئێستا بۆی بنێرە", GREEN, W_, 62),
 T("دەستت خۆش بێت کە لەگەڵمانیت", 56, INK),
], f"{O}/ku-1.jpg", gap=32, top=255)

# 2) quiz: Familiennachzug for subsidiary protection suspended until 23.07.2027 (PLAYBOOK §6) – empty area for the quiz sticker
story2("پرسیاری ئەمڕۆ", [
 T("تۆ دەزانیت؟", 104, KRED),
 kchip("subsidiärer Schutz", GREEN, W_, 60, latin=True),
 para("هێنانی هاوسەر و منداڵ بۆ کەسانی خاوەن پاراستنی سوبسیدیێر تا کەی ڕاگیراوە؟", 58, INK, maxw=940),
 T("وەڵامەکەت هەڵبژێرە", 46, MUTED, "Bold"),
 gap_box(420),
 lat("Quelle: § 36a AufenthG (Aussetzung bis 23.07.2027)", 30),
], f"{O}/ku-2.jpg", gap=40, top=280)

# 3) teaser of today's 16:00 reel (Kurdi-25-3-Abschiebungsverbot) + space for question box
story2("ڤیدیۆی ئەمڕۆ", [
 kchip("ئەمڕۆ کاتژمێر ١٦:٠٠", KRED, W_, 58),
 kchip("§ 25 Abs. 3 AufenthG", SUN, INK, 54, latin=True),
 T("قەدەغەی دیپۆرت", 108, GREEN),
 fitT("پاسپۆرتی ئەڵمانی دەدرێت؟", 84, 980, INK),
 para("مافی کار، هێنانی خێزان، ئیقامەی دائیمی، و ئەو خاڵەی زۆر کەس نایزانێت.", 48),
 T("پرسیارەکەت لێرە بنووسە", 50, KRED, "Bold"),
 gap_box(300),
], f"{O}/ku-3.jpg", gap=36, top=262)

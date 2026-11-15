from kgen import *
W_ = (255, 255, 255)
def para(s, size=50, col=INK, w="Bold", maxw=920):
    f = fa(w, size); words = s.split(); lines = []; cur = ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if text_size(t, f, rtl=True)[0][2] > maxw and cur: lines.append(cur); cur = wd
        else: cur = t
    lines.append(cur)
    sp = [text_sprite(l, f, col, rtl=True) for l in lines]; g = 6
    im = Image.new("RGBA", (max(x.width for x in sp), sum(x.height for x in sp) + g * (len(sp) - 1)), (0, 0, 0, 0)); y = 0
    for x in sp: im.alpha_composite(x, ((im.width - x.width) // 2, y)); y += x.height + g
    return im
def story(head, items, out, gap=40):
    bg = add_brand(make_bg()); header(head).draw(bg, 30)
    Ht = sum(i.height for i in items) + gap * (len(items) - 1); y = max(240, (H - Ht) // 2)
    for im in items: bg.alpha_composite(im, ((W - im.width) // 2, y)); y += im.height + gap
    bg.convert("RGB").save(out, quality=93)

story("پەیامێک بۆ ئێوە", [
 T("مەوزووعی یەکەم", 56, MUTED),
 T("هاوڕێیانی ئازیز", 92, GREEN),
 kchip("تکایە بە ڕێنووسی کوردی بنووسن", KRED, W_, 56),
 para("بەڕاستی ئەو شێوازە لاتینییە تێکەڵاوە تێی ناگەم، و تەواو هەڵەیە. کەسانی تریش لێتان تێناگەن.", 50),
 krow("کوردیی لاتین ڕێنووسی تایبەتی خۆی هەیە", icon=ICONS["info"](), h=150),
 krow("حەزتان لێیە؟ فێری بن، ئەوکات لاتین بنووسن", icon=ICONS["ok"](), h=150),
], "../out/Story-Kurdi-Rennus.jpg")

story("داوایەکی بچووک", [
 T("مەوزووعی دووەم", 56, MUTED),
 para("لەم دوو سێ ڕۆژەدا زۆر پەیج و کەس نامە دەنێرن کە ڤیدیۆکان ببەن و لە پەیج و گرووپەکانی خۆیان بڵاوی بکەنەوە.", 48),
 kchip("من بە هیچ شێوەیەک ڕازی نیم", KRED, W_, 58),
 para("کاتێکی زۆر بۆ دروستکردنی ئەم ڤیدیۆیانە دادەنێم، و هەموو هەوڵم ئەوەیە زانیاریی ڕاست و دروست بڵاو بکەمەوە.", 46),
 para("لایک و کۆمێنت بۆ خۆم قەت گرنگ نییە، بەڵام ئەگەر ئێوە پاڵپشتی بکەن، بابەتەکان دەگەنە دەستی ئەو کەسانەی پێویستیان پێیەتی.", 46, GREEN),
 kchip("فۆڵۆ · لایک · لێرەوە شێری بکەن", GREEN, W_, 54),
 T("سوپاس بۆ هاوکاریتان", 60, INK),
], "../out/Story-Kurdi-Hawkari2.jpg", gap=36)

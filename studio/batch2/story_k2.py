from kgen import *
W_=(255,255,255)
bg = add_brand(make_bg()); header("پەیامێک بۆ ئێوە").draw(bg, 30)
def para(s, size, col=INK, w="Bold", maxw=930):
    words = s.split(); lines=[]; cur=""
    for wd in words:
        t = (cur+" "+wd).strip()
        if T(t, size, col, w).width > maxw and cur: lines.append(cur); cur = wd
        else: cur = t
    lines.append(cur)
    ims=[T(l, size, col, w) for l in lines]; gap=14
    im=Image.new("RGBA",(max(i.width for i in ims), sum(i.height for i in ims)+gap*(len(ims)-1)),(0,0,0,0)); y=0
    for i in ims: im.alpha_composite(i, ((im.width-i.width)//2, y)); y+=i.height+gap
    return im
items = [T("هاوڕێیانی ئازیز", 84, GREEN),
 para("هەموو ڕۆژێک هەزاران کەس ڤیدیۆکانمان دەبینن، بەڵام لایک و کۆمێنت زۆر کەمە.", 48, KRED),
 para("هەوڵی من ئەوەیە دروستترین زانیاری بە سادەترین شێوە بۆتان ڕوون بکەمەوە. ئەم ڤیدیۆیانە بە خۆڕایی دروست دەکەم و بۆ هەر یەکێکیان کات و وزەیەکی زۆر تەرخان دەکەم.", 42),
 para("یەک لایک یان کۆمێنت لە ئێوە وا دەکات ڤیدیۆکە بگاتە کەسانی زیاتر کە وەک ئێوە پێویستیان بەم زانیارییانەیە. پشتگیریی ئێوەش ئێمە هیوادار دەکات کە ڤیدیۆکان دەبینن و سوودیان بۆتان هەیە.", 42),
 para("تکایە بۆ بەردەوامبوونی کارەکەمان هاوکاری بکەن:", 46, GREEN),
 kchip("فۆڵۆ بکەن · لایک بکەن · کۆمێنت بکەن", KRED, W_, 52),
 para("پرسیارەکانتان لە ژێر پۆستەکان بنووسن", 40, MUTED),
 T("سوپاس بۆ هاوڕێیەتیتان", 56, GREEN)]
gap = 30; Ht = sum(i.height for i in items) + gap*(len(items)-1); y = 250
for im in items: bg.alpha_composite(im, ((W - im.width)//2, y)); y += im.height + gap
print(y)
bg.convert("RGB").save("final3/Story-Kurdi-Hawkari.jpg", quality=93)

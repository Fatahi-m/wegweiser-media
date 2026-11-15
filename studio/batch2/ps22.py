import sys
sys.argv_backup = list(sys.argv)
from reel import *
import reel
def build(_T):
    els = [header("مالیات")]
    disc = T_("اطلاعات عمومی · وضعیت اکتبر ۲۰۲۶ · جای مشاوره‌ی رسمی نیست", 28, (150, 170, 200), "Medium")
    els.append(El(disc, cx, 1640, 0.3, anim="fade", anchor="c"))
    def card(word, mean, y, t, e):
        c, b = german_card(word, mean)
        els.append(El(c, cx, y, t, e, anim="pop", anchor="c", dur=0.5)); els.append(El(b, cx, y - 30, t + 0.15, e, anim="pop", anchor="c"))
    # hook
    e = 8.3
    els.append(El(T_("پول مالیات ۲۰۲۲", 86), cx, 420, 0.2, e, anchor="c"))
    els.append(El(T_("رو پس بگیر!", 96, GOLD), cx, 540, 1.2, e, anchor="c"))
    els.append(El(chip("فقط تا ۳۱ دسامبر ۲۰۲۶", fa("Black", 52), RED, WHITE), cx, 690, 2.6, e, anim="pop", anchor="c"))
    els.append(El(chip("فالو و لایک کن · ممنون", fa("Black", 46), GOLD, NAVY_D), cx, 900, 5.96, e, anim="pop", anchor="c"))
    # 1 voluntary
    e = 19.45
    els.append(El(chip("۱ · داوطلبانه", fa("Black", 46), GOLD, NAVY_D), cx, 330, 8.6, e, anim="pop", anchor="c"))
    els.append(El(row("کارمندی و مجبور به اظهارنامه نبودی", icon_check), 80, 440, 9.0, e, anim="right"))
    els.append(El(big("۴ سال", GOLD, 170), cx, 700, 12.88, e, anim="pop", anchor="c"))
    els.append(El(T_("عقب‌تر می‌تونی اظهارنامه بدی", 52, WHITE, "Bold"), cx, 930, 13.5, e, anchor="c"))
    card("Steuererklärung", "اظهارنامه‌ی مالیاتی", 1060, 17.35, e)
    # 2 deadline
    e = 29.2
    els.append(El(chip("۲ · ددلاین", fa("Black", 46), RED, WHITE), cx, 330, 19.75, e, anim="pop", anchor="c"))
    els.append(El(T_("اظهارنامه‌ی سال ۲۰۲۲", 74), cx, 470, 20.2, e, anchor="c"))
    els.append(El(T_("فقط تا", 56, SOFT), cx, 590, 22.0, e, anchor="c"))
    els.append(El(big("۳۱ دسامبر ۲۰۲۶", GOLD, 120), cx, 680, 22.8, e, anim="pop", anchor="c"))
    els.append(El(row("بعدش این پول برای همیشه از دست می‌ره", icon_cross), 80, 900, 26.07, e, anim="pop"))
    # 3 stats
    e = 38.8
    els.append(El(chip("۳ · آمار رسمی", fa("Black", 46), GOLD, NAVY_D), cx, 330, 29.52, e, anim="pop", anchor="c"))
    els.append(El(big("۸۶٪", GREEN, 190), cx, 480, 30.2, e, anim="pop", anchor="c"))
    els.append(El(T_("پول پس گرفتن", 58, WHITE, "Bold"), cx, 720, 31.5, e, anchor="c"))
    els.append(El(T_("به‌طور میانگین", 50, SOFT), cx, 830, 35.42, e, anchor="c"))
    els.append(El(euro("۱۱۷۲"), cx, 900, 35.6, e, anim="pop", anchor="c", dur=0.5))
    els.append(El(T_("سال مالیاتی ۲۰۲۱ · Destatis", 40, SOFT, "Medium"), cx, 1170, 36.2, e, anchor="c"))
    # 4 costs
    e = 48.75
    els.append(El(T_("چه هزینه‌هایی حساب می‌شه؟", 70), cx, 400, 39.14, e, anchor="c"))
    for i, (s, t) in enumerate([("رفت‌وآمد به محل کار", 41.02), ("وسایل کار", 43.34), ("دوره‌های آموزشی شغلی", 44.71), ("اسباب‌کشی به‌خاطر کار", 46.54)]):
        els.append(El(row(s, icon_check), 80, 540 + i * 180, t, e, anim="right"))
    # 5 how
    e = 55.1
    els.append(El(chip("۴ · چطوری؟", fa("Black", 46), GOLD, NAVY_D), cx, 330, 49.03, e, anim="pop", anchor="c"))
    card("ELSTER", "رایگان و آنلاین", 480, 50.08, e)
    els.append(El(T_("یا", 60, SOFT), cx, 800, 52.23, e, anchor="c"))
    card("Lohnsteuerhilfeverein", "انجمن کمک مالیاتی", 980, 52.6, e)
    # source
    lab = text_sprite("منبع:", fa("Bold", 30), (150, 170, 200), rtl=True); src = text_sprite("§ 46 Abs. 2 Nr. 8 EStG · § 169 AO · Destatis", la("Bold", 30), (150, 170, 200))
    im = Image.new("RGBA", (src.width + 12 + lab.width, max(src.height, lab.height)), (0, 0, 0, 0))
    im.alpha_composite(src, (0, (im.height - src.height) // 2)); im.alpha_composite(lab, (src.width + 12, (im.height - lab.height) // 2))
    els.append(El(im, cx, 1440, 0.3, anim="fade", anchor="c"))
    outro(els, 55.39, "اظهارنامه‌ی ۲۰۲۲ رو دادی؟", "کامنت کن: آره یا نه")
    for e_ in els[2:]:
        if isinstance(e_, El): e_.y += OFF
    return els
if __name__ == "__main__":
    a = sys.argv_backup
    R.build = build
    tt = [float(x) for x in a[a.index("--frames") + 1].split(",")] if "--frames" in a else None
    R.render({"total": 62.5}, a[1], a[2], tt)

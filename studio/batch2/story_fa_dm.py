from reel import *
def para(s, size=40, col=WHITE, maxw=940, w="Bold"):
    words=s.split(); lines=[]; cur=""
    for wd in words:
        t=(cur+" "+wd).strip()
        if T_(t,size,col,w).width>maxw and cur: lines.append(cur); cur=wd
        else: cur=t
    lines.append(cur)
    ims=[T_(l,size,col,w) for l in lines]; lh=int(size*1.55)
    out=Image.new("RGBA",(max(i.width for i in ims), lh*len(ims)),(0,0,0,0))
    for k,i in enumerate(ims): out.alpha_composite(i,((out.width-i.width)//2, k*lh+(lh-i.height)//2))
    return out
bg = R.make_bg().convert("RGBA") if hasattr(R, "make_bg") else Image.new("RGBA", (W, H), NAVY)
header("درخواستی از شما").draw(bg, 30)
items=[T_("دوستان عزیز", 72, GOLD),
 para("اگه سؤالتون شخصی نیست، لطفاً زیر پست‌ها کامنت بذارید تا همون‌جا جواب بدم و بقیه‌ی دوستان هم استفاده کنن."),
 chip("سؤال‌ها در کامنت", fa("Black", 50), GOLD, NAVY_D),
 para("پیام‌های دایرکت خیلی زیادن، بابت اینکه کمی دیر جواب میدم عذرخواهی می‌کنم.", 38, SOFT),
 para("لطفاً شماره‌ی تلفن یا واتس‌اپ شخصی درخواست نکنید؛ نمی‌تونم شماره‌ی شخصیم رو پخش کنم. ممنون از درکتون.", 38, SOFT),
 para("همه‌ی اطلاعات این پیج موثق، با ذکر منبع و بر اساس آخرین تغییرات قانونه. مطمئن باشید اطلاعات نادرست اینجا منتشر نمیشه.", 38, WHITE),
 chip("لایک کن، شِیر کن، حمایت کن", fa("Black", 48), GREEN, NAVY_D),
 T_("سپاسگزارم، همیشه موفق باشید", 50, GOLD)]
gap=34; Ht=sum(i.height for i in items)+gap*(len(items)-1); y=(H-Ht)//2+20
for im in items: bg.alpha_composite(im,((W-im.width)//2,y)); y+=im.height+gap
bg.convert("RGB").save("../out/Story-Wegweiser-DM.jpg", quality=92)

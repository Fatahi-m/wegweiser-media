from PIL import Image, ImageDraw, ImageFont
import os, sys
D="/home/claude/wegweiser"
F=D+"/fontdl/vz/fonts/ttf/Vazirmatn-"
W,H=1080,1350; M=90
NAVY=(11,42,87); NAVY2=(18,62,124); RED=(226,35,26); WHITE=(255,255,255); SOFT=(200,214,236); CHIP=(28,78,150)
def f(w,s): return ImageFont.truetype(F+w+".ttf", s, layout_engine=ImageFont.Layout.RAQM)
logo=Image.open(D+"/aof/wegweiser-deutschland-logo.png").convert("RGBA").resize((120,120))
mask=Image.new("L",(120,120),0); ImageDraw.Draw(mask).ellipse((0,0,119,119),fill=255)
fa_digits=str.maketrans("0123456789","۰۱۲۳۴۵۶۷۸۹")

def wrap(draw,text,font,maxw):
    lines=[]
    for para in text.split("\n"):
        cur=""
        for w in para.split(" "):
            t=(cur+" "+w).strip()
            if draw.textlength(t,font=font,direction="rtl")<=maxw: cur=t
            else: lines.append(cur); cur=w
        lines.append(cur)
    return lines

def rtl(draw,y,text,font,fill,maxw=W-2*M,lh=1.55):
    for line in wrap(draw,text,font,maxw):
        w=draw.textlength(line,font=font,direction="rtl")
        draw.text((W-M-w,y),line,font=font,fill=fill,direction="rtl")
        y+=int(font.size*lh)
    return y

def chip(draw,x_right,y,text,font,bg=CHIP,fg=WHITE):
    w=draw.textlength(text,font=font); pad=26
    draw.rounded_rectangle((x_right-w-2*pad,y,x_right,y+font.size+34),radius=28,fill=bg)
    draw.text((x_right-w-pad,y+10),text,font=font,fill=fg)
    return x_right-w-2*pad-18

def base(i,n):
    im=Image.new("RGB",(W,H),NAVY); d=ImageDraw.Draw(im)
    for gx in range(0,W,60): d.line((gx,0,gx,H),fill=(16,50,100))
    for gy in range(0,H,60): d.line((0,gy,W,gy),fill=(16,50,100))
    d.rectangle((0,0,W,14),fill=RED)
    im.paste(logo,(M,60),mask)
    d.text((M+140,95),"WEGWEISER DEUTSCHLAND",font=f("Bold",30),fill=SOFT)
    num=f"{i}/{n}".translate(fa_digits)
    nf=f("Bold",34); w=d.textlength(num,font=nf)
    d.text((W-M-w,92),num,font=nf,fill=SOFT)
    return im,d

def footer(d,txt="ورق بزن ←"):
    ft=f("Medium",34); w=d.textlength(txt,font=ft,direction="rtl")
    d.text((M,H-110),txt,font=ft,fill=SOFT,direction="rtl")

slides=[]
N=7
# 1 cover
im,d=base(1,N)
y=360
y=rtl(d,y,"نامه از",f("Black",120),WHITE,lh=1.25)
y=rtl(d,y,"جاب‌سنتر اومده؟",f("Black",126),RED,lh=1.3)
y+=40
y=rtl(d,y,"قبل از اینکه بترسی، این ۵ کار رو انجام بده",f("Bold",60),WHITE)
y+=50
chip(d,W-M,y,"Jobcenter • Brief • Frist",f("Bold",38),RED)
footer(d); slides.append(im)
# 2
im,d=base(2,N)
y=230; y=rtl(d,y,"۱",f("Black",190),RED,lh=1.0); y+=30
y=rtl(d,y,"اول «مهلت» رو پیدا کن",f("Black",78),WHITE,lh=1.35); y+=30
x=chip(d,W-M,y,"Frist",f("Bold",40),RED); chip(d,x,y,"bis zum …",f("Bold",40)); y+=120
y=rtl(d,y,"تقریباً همه‌ی نامه‌ها یک تاریخ دارن که تا اون موقع باید جواب بدی یا کاری انجام بدی. دنبال کلمه‌ی Frist یا bis zum بگرد.",f("Medium",52),SOFT); y+=30
y=rtl(d,y,"تاریخ رو همون روز یادداشت کن.",f("Bold",54),WHITE)
footer(d); slides.append(im)
# 3
im,d=base(3,N)
y=230; y=rtl(d,y,"۲",f("Black",190),RED,lh=1.0); y+=30
y=rtl(d,y,"نوع نامه رو بشناس",f("Black",82),WHITE,lh=1.35); y+=40
rows=[("Einladung","دعوت به قرار ملاقات"),("Mitwirkung","مدارک خواستن"),("Bescheid","تصمیم درباره‌ی پولت"),("Anhörung","می‌خوان نظرت رو بشنون")]
for de,fa in rows:
    d.rounded_rectangle((M,y,W-M,y+130),radius=24,fill=CHIP)
    d.text((M+30,y+36),de,font=f("Bold",50),fill=WHITE)
    ft=f("Medium",48); w=d.textlength(fa,font=ft,direction="rtl")
    d.text((W-M-30-w,y+38),fa,font=ft,fill=SOFT,direction="rtl")
    y+=160
footer(d); slides.append(im)
# 4
im,d=base(4,N)
y=230; y=rtl(d,y,"۳",f("Black",190),RED,lh=1.0); y+=30
y=rtl(d,y,"دعوت‌نامه اومده؟ حتماً برو",f("Black",78),WHITE,lh=1.35); y+=30
chip(d,W-M,y,"Einladung / Meldetermin",f("Bold",40),RED); y+=120
y=rtl(d,y,"اگه نمی‌تونی بری، قبل از قرار به جاب‌سنتر خبر بده و دلیلت رو ثابت کن، مثلاً با گواهی پزشکی (Krankmeldung).",f("Medium",52),SOFT); y+=30
y=rtl(d,y,"نرفتن بدون دلیل مهم می‌تونه باعث کم شدن پولت بشه.",f("Bold",54),WHITE)
footer(d); slides.append(im)
# 5
im,d=base(5,N)
y=230; y=rtl(d,y,"۴",f("Black",190),RED,lh=1.0); y+=30
y=rtl(d,y,"مدارک خواستن؟",f("Black",76),WHITE,lh=1.35); y+=30
chip(d,W-M,y,"jobcenter.digital",f("Bold",40),RED); y+=120
y=rtl(d,y,"مدارک رو قبل از مهلت بفرست. بهترین راه سایت jobcenter.digital هست، یا حضوری با گرفتن رسید (Eingangsbestätigung).",f("Medium",52),SOFT); y+=30
y=rtl(d,y,"از همه‌چیز یک کپی یا عکس نگه دار.",f("Bold",54),WHITE)
footer(d); slides.append(im)
# 6
im,d=base(6,N)
y=230; y=rtl(d,y,"۵",f("Black",190),RED,lh=1.0); y+=30
y=rtl(d,y,"با تصمیمشون موافق نیستی؟",f("Black",78),WHITE,lh=1.35); y+=30
chip(d,W-M,y,"Widerspruch",f("Bold",40),RED); y+=120
y=rtl(d,y,"اگه فکر می‌کنی Bescheid اشتباهه، معمولاً ۱ ماه وقت داری Widerspruch (اعتراض) بدی. رایگانه و وکیل لازم نداره.",f("Medium",52),SOFT); y+=30
y=rtl(d,y,"مهلت دقیق، آخر همون نامه نوشته شده.",f("Bold",52),WHITE)
footer(d); slides.append(im)
# 7 CTA
im,d=base(7,N)
y=360
y=rtl(d,y,"این پست رو",f("Black",116),WHITE,lh=1.25)
y=rtl(d,y,"ذخیره کن",f("Black",126),RED,lh=1.3); y+=40
y=rtl(d,y,"و برای کسی که تازه به آلمان اومده بفرست.",f("Bold",60),WHITE); y+=60
y=rtl(d,y,"فالو کن برای فکت‌های بیشتر درباره‌ی زندگی در آلمان",f("Medium",54),SOFT); y+=30
chip(d,W-M,y,"@wegweiser.deutschland",f("Bold",40),RED)
ft=f("Medium",28); t="اطلاعات عمومی؛ جایگزین مشاوره‌ی رسمی نیست."
w=d.textlength(t,font=ft,direction="rtl"); d.text((W-M-w,H-100),t,font=ft,fill=SOFT,direction="rtl")
slides.append(im)
for i,s in enumerate(slides,1): s.save(f"{D}/aof/post1/slide{i}.png")
print("ok")

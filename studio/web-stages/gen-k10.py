# Generates k10-{fa,ku}(-tt).html: "§ 10 StAG – with these residence permits you can't apply for citizenship yet"
import re,sys
head=open('k254-ku.html').read().split('</style>')[0]
extra='''
.row .k{min-width:0;font-size:38px;padding:12px 22px}
.row .k.sm{font-size:30px}
.row{padding:24px 34px;gap:26px}
.row .tx{font-size:48px;flex:1;min-width:0}
.ck .b.red{background:linear-gradient(160deg,#ff6b74,#e3262f);color:#fff}
.src{position:absolute;left:0;right:0;text-align:center;font:700 34px I;color:rgba(255,255,255,.6);direction:ltr}
.big2{position:absolute;left:0;right:0;text-align:center;font:900 150px/1.05 V,I}
.big2 small{display:block;font:900 60px V;margin-top:16px}
.ar{position:absolute;left:110px;right:110px;display:flex;align-items:center;gap:26px;padding:22px 34px;border-radius:30px;background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.25);font:900 44px I;direction:ltr}
.ar i{font-style:normal;flex:none;width:76px;height:76px;border-radius:22px;display:grid;place-items:center;background:linear-gradient(160deg,var(--gold2),var(--gold));color:#1a1405;font:900 30px I}
#wm{position:absolute;left:50%;top:900px;width:820px;height:820px;margin:-410px 0 0 -410px;opacity:.12;border-radius:50%}
#nb{position:absolute;left:0;right:0;top:56px;text-align:center;z-index:20;direction:ltr}
#nb img{width:150px;height:150px;border-radius:50%;box-shadow:0 14px 40px rgba(0,0,0,.45)}
#nb .t{font:900 60px/1 I;letter-spacing:2px;margin-top:14px;color:#fff}
#nb .t span{font:700 30px I;letter-spacing:9px;color:rgba(255,255,255,.75);margin-left:10px}
#nb .h{font:700 36px I;color:rgba(255,255,255,.85);margin-top:8px}
#ft{position:absolute;left:0;right:0;top:1450px;text-align:center;z-index:20;direction:ltr}
#ft .q{font:700 34px I;color:rgba(255,255,255,.62)}
#ft .ad{font:800 30px I;color:rgba(255,214,102,.85);margin-top:10px}
body.tt #ft .ad,body.tt .adr{display:none!important}
body.tt #wm,body.tt #nb{display:none}
'''
L={
'ku':dict(cls='ku',d='٠١٢٣٤٥٦٧٨٩',logo='logo-ku.png',name='KURDI',h='@wegweiser_kurdi',url='wegweiser-news.de/ku',ig='@wegweiser_kurdi',tk='@wegweiser_kurdi',
 SC=[[0,11.6],[11.6,17.3],[17.3,28.4],[28.4,55.0],[55.0,66.0],[66.0,71.0],[71.0,77.6],[77.6,87.7],[87.7,96.6],[96.6,104.2]],
 s4t=[0.3,2.1,6.2,8.8,13.6,18.1], s5t=[0.3,3.8,5.7,6.7,7.8,9.2], s8x=7.6, s9b=3.8, s10f=4.6, s3w=4.6, s1w=8.2,
 t=dict(
  h1=['ئەم','ماددەیە','لەسەر','<span class="g">کارتەکەتە؟</span>'], w1='داواکاریی ڕەگەزنامەکەت ڕەت دەکرێتەوە!', p1='لیستی تەواو 👇',
  h2=['هەموو','بابەتەکان','<span class="g">بە تەواوی</span>'], s2='لە پەیج و ماڵپەڕەکەمان',
  h3=['٥ ساڵ','=','<span class="g">ڕەگەزنامە؟</span>'], w3='نەخێر! بە هەموو ئیقامەیەک نا',
  h4=['ئیقامە','<span class="g">مرۆییەکان</span>'],
  r4=[('§ 25 Abs. 3','<span class="lt">Abschiebungsverbot</span>',''),('§ 25 Abs. 4','ئیقامەی کاتیی مرۆیی',''),('§ 25 Abs. 5','گەڕانەوە مەحاڵە',''),('§ 24','پاراستنی کاتی (ئۆکرانیا)',''),('§ 22 · 23 Abs. 1 · 23a','<span class="lt">Härtefallkommission</span>','sm')],
  h5=['خوێندن','و','<span class="g">ئیقامەی کاتی</span>'],
  r5=[('§ 16b','خوێندنی زانکۆ'),('§ 16a','<span class="lt">Ausbildung</span>'),('§ 16f','کۆرسی زمان'),('§ 16d','ناساندنی بڕوانامە'),('§ 20','گەڕان بەدوای کاردا')],
  h6=['هەر','<span class="g">ئیقامە</span>','نین'], w6='وەک ئیقامە حساب ناکرێن',
  h7=['بێهیوا','<span class="g">مەبە!</span>'], o7='✓ ڕێگایەک هەیە', s7='دواتر دەتوانیت داواکاری بدەیت',
  h8=['هەواڵێکی','<span class="g">خۆش</span>'], c8a='ماوەی یاسایی حساب دەکرێت', c8as='بۆ ئەو ٥ ساڵە', c8b='ماوەی <span class="lt">Duldung</span> حساب ناکرێت',
  h9=['ئیقامەکەت','لەم','<span class="g">لیستەدایە؟</span>'], b9s='دەتەوێت ڕێگاکەت پێ بڵێم؟', b9='لە کۆمێنت بنووسە 👇',
  p10='ڤیدیۆی داهاتوو', h10=['بە','کام','ئیقامە','<span class="g">ڕاستەوخۆ</span>','دەتوانیت؟'], f10='فۆڵۆ لە بیر نەکەیت ♥')),
'fa':dict(cls='',d='۰۱۲۳۴۵۶۷۸۹',logo='logo-fa.png',name='FARSI',h='@wegweiser_farsi',url='wegweiser-news.de/fa',ig='@wegweiser_farsi',tk='@wegweiser_farsi',
 SC=[[0,10.7],[10.7,16.3],[16.3,28.9],[28.9,58.1],[58.1,68.6],[68.6,74.2],[74.2,81.0],[81.0,90.5],[90.5,100.0],[100.0,107.0]],
 s4t=[0.3,2.7,7.5,10.2,15.4,20.3], s5t=[0.3,1.5,3.4,4.9,7.1,9.0], s8x=7.1, s9b=4.2, s10f=4.4, s3w=5.0, s1w=7.0,
 t=dict(
  h1=['این','پاراگراف','روی','<span class="g">کارتته؟</span>'], w1='درخواست تابعیتت رد میشه!', p1='لیست کامل 👇',
  h2=['همه‌ی','مطالب','<span class="g">کامل</span>'], s2='توی پیج و سایت ما',
  h3=['۵ سال','=','<span class="g">تابعیت؟</span>'], w3='نه! با هر اقامتی نمیشه',
  h4=['اقامت‌های','<span class="g">انسان‌دوستانه</span>'],
  r4=[('§ 25 Abs. 3','<span class="lt">Abschiebungsverbot</span>',''),('§ 25 Abs. 4','اقامت موقت انسانی',''),('§ 25 Abs. 5','برگشت ممکن نیست',''),('§ 24','حمایت موقت (اوکراین)',''),('§ 22 · 23 Abs. 1 · 23a','<span class="lt">Härtefallkommission</span>','sm')],
  h5=['اقامت‌های','<span class="g">تحصیلی و موقت</span>'],
  r5=[('§ 16b','دانشجویی'),('§ 16a','<span class="lt">Ausbildung</span>'),('§ 16f','کلاس زبان'),('§ 16d','به رسمیت شناختن مدرک'),('§ 20','جستجوی کار')],
  h6=['اصلاً','<span class="g">اقامت</span>','نیستن'], w6='اقامت حساب نمیشن',
  h7=['ناامید','<span class="g">نشو!</span>'], o7='✓ یه راه هست', s7='بعداً می‌تونی درخواست بدی',
  h8=['یه','خبر','<span class="g">خوب</span>'], c8a='زمان قانونی حساب میشه', c8as='جزو اون ۵ سال', c8b='زمان <span class="lt">Duldung</span> حساب نمیشه',
  h9=['اقامت','تو','توی','این','<span class="g">لیسته؟</span>'], b9s='می‌خوای راهش رو بهت بگم؟', b9='توی کامنت بنویس 👇',
  p10='ویدیوی بعدی', h10=['با','کدوم','اقامت‌ها','<span class="g">مستقیم</span>','میشه؟'], f10='فالو یادت نره ♥')),
}
def W(ws): return ' '.join(f'<span class="w">{w}</span>' for w in ws)
def page(lang,tt):
    c=L[lang]; t=c['t']; dg=lambda n:c['d'][n]
    S=[]
    S.append(f'''<div class="sc" id="s1">
 <div class="hl" style="top:380px;font-size:84px">{W(t['h1'])}</div>
 <div class="card" style="left:160px;top:640px" data-t="0.3" data-a="card"><div class="top"><span class="d">D</span><span class="tt">AUFENTHALTSTITEL<small>RESIDENCE PERMIT</small></span><span class="chp"></span></div><div class="ph2"><svg viewBox="0 0 60 76"><circle cx="30" cy="27" r="13"/><path d="M6 76c0-15 11-25 24-25s24 10 24 25z"/></svg></div><div class="f" style="top:130px">NAME</div><div class="v" style="top:156px">MUSTERMANN</div><div class="f" style="top:220px">ART DES TITELS</div><div class="v" style="top:246px">AUFENTHALTSERLAUBNIS</div><div class="pz" style="font-size:70px;top:314px;color:#c81e28">§ 25 Abs. 3</div><div class="ms">MUSTER</div></div>
 <div class="x" style="left:735px;top:540px;transform:scale(.38)" data-t="2.0" data-a="pop"></div>
 <div class="warn" style="top:1170px" data-t="{c['s1w']}" data-a="pop">{t['w1']}</div>
 <div class="pill" style="top:1330px" data-t="{c['s1w']+1.3:.1f}" data-a="pillx">{t['p1']}</div>
</div>''')
    S.append(f'''<div class="sc" id="s2">
 <div class="hl" style="top:400px;font-size:84px">{W(t['h2'])}</div>
 <div class="de" style="top:640px;direction:rtl;font:700 56px V" data-t="0.8" data-a="pop">{t['s2']}</div>
 <div class="ar adr" style="top:780px" data-t="1.4" data-a="rise"><i>WEB</i>{c['url']}</div>
 <div class="ar adr" style="top:930px" data-t="2.0" data-a="rise"><i>IG</i>{c['ig']}</div>
 <div class="ar adr" style="top:1080px" data-t="2.6" data-a="rise"><i>TT</i>{c['tk']}</div>
</div>''')
    S.append(f'''<div class="sc" id="s3">
 <div class="hl" style="top:420px;font-size:110px">{W(t['h3'])}</div>
 <div class="warn" style="top:720px" data-t="{c['s3w']}" data-a="pop">{t['w3']}</div>
 <div class="de" style="top:940px;font:900 58px I" data-t="{c['s3w']+0.6:.1f}" data-a="pop">Staatsangehörigkeitsgesetz</div>
 <div class="src" style="top:1040px" data-t="{c['s3w']+1.2:.1f}" data-a="pop">§ 10 Abs. 1 Nr. 2 StAG</div>
</div>''')
    def rows(rs,ts,top,red=True):
        o=''
        for i,r in enumerate(rs):
            k,tx=r[0],r[1]; sm=(' '+r[2]) if len(r)>2 and r[2] else ''
            o+=f' <div class="row" style="top:{top+i*150}px" data-t="{ts[i]}" data-a="rise"><span class="k{" red" if red else ""}{sm}">{k}</span><span class="tx">{tx}</span></div>\n'
        return o
    S.append(f'''<div class="sc" id="s4"><div class="num" style="top:380px">{dg(1)}</div>
 <div class="hl" style="top:540px;font-size:76px">{W(t['h4'])}</div>
{rows(t['r4'],c['s4t'][1:],680)}</div>''')
    S.append(f'''<div class="sc" id="s5"><div class="num" style="top:380px">{dg(2)}</div>
 <div class="hl" style="top:540px;font-size:76px">{W(t['h5'])}</div>
{rows(t['r5'],c['s5t'][1:],680)}</div>''')
    S.append(f'''<div class="sc" id="s6"><div class="num" style="top:380px">{dg(3)}</div>
 <div class="hl" style="top:540px;font-size:84px">{W(t['h6'])}</div>
 <div class="row" style="top:740px" data-t="0.5" data-a="rise"><span class="k red">✗</span><span class="tx lt" style="font:900 56px I">Duldung</span></div>
 <div class="row" style="top:910px" data-t="1.4" data-a="rise"><span class="k red">✗</span><span class="tx lt" style="font:900 50px I">Aufenthaltsgestattung</span></div>
 <div class="warn" style="top:1110px" data-t="2.8" data-a="pop">{t['w6']}</div>
</div>''')
    S.append(f'''<div class="sc" id="s7">
 <div class="hl" style="top:460px;font-size:120px">{W(t['h7'])}</div>
 <div class="pill" style="top:760px;font-size:62px" data-t="1.8" data-a="pillx">{t['o7']}</div>
 <div class="de" style="top:930px;direction:rtl;font:700 54px V" data-t="2.6" data-a="pop">{t['s7']}</div>
</div>''')
    S.append(f'''<div class="sc" id="s8">
 <div class="hl" style="top:430px;font-size:104px">{W(t['h8'])}</div>
 <div class="ck" style="top:700px" data-t="2.2" data-a="rise"><span class="b">✓</span><span>{t['c8a']}<small>{t['c8as']}</small></span></div>
 <div class="ck" style="top:930px" data-t="{c['s8x']}" data-a="rise"><span class="b red">✗</span><span>{t['c8b']}</span></div>
</div>''')
    S.append(f'''<div class="sc" id="s9">
 <div class="hl" style="top:430px;font-size:88px">{W(t['h9'])}</div>
 <div class="bub" style="top:760px" data-t="{c['s9b']}" data-a="pop"><small>{t['b9s']}</small><b style="font:900 78px V">{t['b9']}</b></div>
</div>''')
    S.append(f'''<div class="sc" id="s10">
 <div class="pill" style="top:400px" data-t="0.2" data-a="pillx">{t['p10']}</div>
 <div class="hl" style="top:560px;font-size:84px">{W(t['h10'])}</div>
 <div class="url adr" style="top:900px;font-size:64px" data-t="2.4" data-a="pop">{c['url']}</div>
 <div class="ok" style="top:1150px;left:50%" data-t="{c['s10f']}" data-a="pillx">{t['f10']}</div>
</div>''')
    body=f'''</style></head><body class="{c['cls']}{' tt' if tt else ''}"><div id="st">
<div id="bg"></div><div id="rays"></div><div id="glow"></div><div id="floor"></div><div id="stars"></div><img id="wm" src="{c['logo']}"><div id="scenes">
{chr(10).join(S)}
</div><div id="ft"><div class="q">Quelle: § 10 Abs. 1 Nr. 2 StAG</div><div class="ad">{c['url']}</div><div class="ad" style="margin-top:4px">IG {c['ig']} · TikTok {c['tk']}</div></div><div id="nb"><img src="{c['logo']}"><div class="t">WEGWEISER<span>{c['name']}</span></div><div class="h">{c['h']}</div></div><div id="vig"></div><div class="flash" id="flash"></div></div>'''
    js=open('k254-ku.html').read().split('<script>')[1]
    js=re.sub(r'window\.SC=\[\[.*?\]\];',f"window.SC={c['SC']};",js)
    js=js.replace("    if(i===10){ $('#url').style.display=TT?'none':''; }\n","").replace("    if(i===11){ $('#lg').style.opacity=TT?0:eo((t-1.5)/0.6); }\n","")
    js=js.replace("  $('#flash').style.opacity=fl;","  $('#flash').style.opacity=fl; $('#wm').style.transform=`rotate(${Math.sin(T0*0.3)*4}deg) scale(${1+Math.sin(T0*0.5)*0.02})`;")
    return head+extra+body+'<script>'+js
for lang in ('ku','fa'):
    for tt in (0,1):
        open(f"k10-{lang}{'-tt' if tt else ''}.html",'w').write(page(lang,tt))
print('ok')

# § 10 StAG part 2: residence permits that qualify DIRECTLY for Einbürgerung (fa/ku, IG + TikTok)
import re
src=open('gen-k10.py').read()
exec(src.split('\nL={')[0])          # head, extra
extra+='''
.row .k.grn{background:linear-gradient(160deg,#5ee08f,#16a34a);color:#fff}
.ck .b.grn{background:linear-gradient(160deg,#5ee08f,#16a34a);color:#fff}
.okbig{position:absolute;left:50%;width:300px;height:300px;margin-left:-150px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#7ef0a8,#16a34a 70%);box-shadow:0 0 90px rgba(60,220,120,.55),0 30px 70px rgba(0,0,0,.5);display:grid;place-items:center;font:900 190px/1 I;color:#fff}
'''
BASE={
 'fa':dict(cls='',d='۰۱۲۳۴۵۶۷۸۹',logo='logo-fa.png',name='FARSI',h='@wegweiser_farsi',url='wegweiser-news.de/fa',ig='@wegweiser_farsi',tk='@wegweiser_farsi'),
 'ku':dict(cls='ku',d='٠١٢٣٤٥٦٧٨٩',logo='logo-ku.png',name='KURDI',h='@wegweiser_kurdi',url='wegweiser-news.de/ku',ig='@wegweiser_kurdi',tk='@wegweiser_kurdi'),
}
T={
 'fa':dict(
  h1=['بدون','<span class="g">اقامت دائم</span>','هم','میشه!'], p1='درخواست تابعیت ✓', s1='به شرط داشتن یکی از این اقامت‌ها 👇',
  h2=['همه‌ی','مطالب','<span class="g">کامل</span>'], s2='توی پیج و سایت ما',
  h3=['لیست','اقامت‌هایی','که','<span class="g">میشه</span>'], w3='ویدیوی قبلی: اقامت‌هایی که نمیشه ✗',
  g=[('اقامت <span class="g">دائم</span>',[('✓','<span class="lt">Niederlassungserlaubnis</span>','sm'),('✓','<span class="lt">Daueraufenthalt-EU</span>','sm')]),
     ('<span class="g">پناهندگی</span>',[('§ 25 Abs. 1','<span class="lt">Asyl</span>'),('§ 25 Abs. 2','پناهندگی و حمایت تبعی')]),
     ('اقامت <span class="g">ادغام</span>',[('§ 25a','جوون‌ها'),('§ 25b','ادغام موفق')]),
     ('اقامت <span class="g">خانوادگی</span>',[('§ 28','همسر یا بچه‌ی آلمانی'),('§ 30','همسر یه خارجی'),('§ 32','بچه‌ها')]),
     ('اقامت <span class="g">کاری</span>',[('§ 18a/18b','متخصص‌ها'),('§ 18g','<span class="lt">Blaue Karte</span>')])],
  h9=['یادت','<span class="g">باشه!</span>'], c9=['۵ سال اقامت قانونی','زبان <span class="lt">B1</span>','<span class="lt">Einbürgerungstest</span>','خرج زندگی از درآمد خودت'],
  h10=['اقامت','تو','توی','این','<span class="g">لیست</span>','بود؟'], b10s='بنویس تا بگم آماده‌ای یا نه', b10='توی کامنت 👇',
  f11='فالو یادت نره ♥'),
 'ku':dict(
  h1=['بەبێ','<span class="g">ئیقامەی هەمیشەیی</span>','دەبێت!'], p1='داواکاریی ڕەگەزنامە ✓', s1='بە مەرجێک یەکێک لەم ئیقامانەت هەبێت 👇',
  h2=['هەموو','بابەتەکان','<span class="g">بە تەواوی</span>'], s2='لە پەیج و ماڵپەڕەکەمان',
  h3=['لیستی','ئەو','ئیقامانەی','<span class="g">دەبێت</span>'], w3='ڤیدیۆی پێشوو: ئەو ئیقامانەی نابێت ✗',
  g=[('ئیقامەی <span class="g">هەمیشەیی</span>',[('✓','<span class="lt">Niederlassungserlaubnis</span>','sm'),('✓','<span class="lt">Daueraufenthalt-EU</span>','sm')]),
     ('<span class="g">پەنابەری</span>',[('§ 25 Abs. 1','<span class="lt">Asyl</span>'),('§ 25 Abs. 2','پەنابەری و پاراستنی لاوەکی')]),
     ('ئیقامەی <span class="g">تێکەڵبوون</span>',[('§ 25a','گەنجان'),('§ 25b','تێکەڵبوونی سەرکەوتوو')]),
     ('ئیقامەی <span class="g">خێزانی</span>',[('§ 28','هاوسەر یان منداڵی ئەڵمانی'),('§ 30','هاوسەری بیانییەک'),('§ 32','منداڵان')]),
     ('ئیقامەی <span class="g">کار</span>',[('§ 18a/18b','شارەزایان'),('§ 18g','<span class="lt">Blaue Karte</span>')])],
  h9=['لە','بیرت','<span class="g">بێت!</span>'], c9=['٥ ساڵ نیشتەجێبوونی یاسایی','زمانی <span class="lt">B1</span>','<span class="lt">Einbürgerungstest</span>','خەرجیی ژیان لە داهاتی خۆت'],
  h10=['ئیقامەکەت','لەم','<span class="g">لیستەدا</span>','بوو؟'], b10s='بنووسە تا پێت بڵێم ئامادەیت یان نا', b10='لە کۆمێنت 👇',
  f11='فۆڵۆ لە بیر نەکەیت ♥'),
}
def W(ws): return ' '.join(f'<span class="w">{w}</span>' for w in ws)
def page(lang,tt,TM):
    c=BASE[lang]; t=T[lang]; dg=lambda n:c['d'][n]; S=[]
    S.append(f'''<div class="sc" id="s1">
 <div class="hl" style="top:380px;font-size:84px">{W(t['h1'])}</div>
 <div class="card" style="left:160px;top:640px" data-t="0.3" data-a="card"><div class="top"><span class="d">D</span><span class="tt">AUFENTHALTSTITEL<small>RESIDENCE PERMIT</small></span><span class="chp"></span></div><div class="ph2"><svg viewBox="0 0 60 76"><circle cx="30" cy="27" r="13"/><path d="M6 76c0-15 11-25 24-25s24 10 24 25z"/></svg></div><div class="f" style="top:130px">NAME</div><div class="v" style="top:156px">MUSTERMANN</div><div class="f" style="top:220px">ART DES TITELS</div><div class="v" style="top:246px">AUFENTHALTSERLAUBNIS</div><div class="pz" style="font-size:70px;top:314px;color:#15803d">§ 25 Abs. 2</div><div class="ms">MUSTER</div></div>
 <div class="okbig" style="top:560px;left:860px;transform:scale(.5)" data-t="1.6" data-a="pop">✓</div>
 <div class="pill" style="top:1170px;font-size:56px" data-t="{TM['s1p']}" data-a="pillx">{t['p1']}</div>
 <div class="de" style="top:1320px;direction:rtl;font:700 46px V" data-t="{TM['s1s']}" data-a="pop">{t['s1']}</div>
</div>''')
    S.append(f'''<div class="sc" id="s2">
 <div class="hl" style="top:400px;font-size:84px">{W(t['h2'])}</div>
 <div class="de" style="top:640px;direction:rtl;font:700 56px V" data-t="0.8" data-a="pop">{t['s2']}</div>
 <div class="ar adr" style="top:780px" data-t="1.4" data-a="rise"><i>WEB</i>{c['url']}</div>
 <div class="ar adr" style="top:930px" data-t="2.0" data-a="rise"><i>IG</i>{c['ig']}</div>
 <div class="ar adr" style="top:1080px" data-t="2.6" data-a="rise"><i>TT</i>{c['tk']}</div>
</div>''')
    S.append(f'''<div class="sc" id="s3">
 <div class="hl" style="top:430px;font-size:96px">{W(t['h3'])}</div>
 <div class="de" style="top:760px;direction:rtl;font:700 46px V;color:rgba(255,255,255,.7)" data-t="0.6" data-a="pop">{t['w3']}</div>
 <div class="okbig" style="top:900px" data-t="{TM['s3ok']}" data-a="pop">✓</div>
</div>''')
    for gi,(ttl,rs) in enumerate(t['g']):
        ts=TM['g'][gi]; rows=''
        for i,r in enumerate(rs):
            k,tx=r[0],r[1]; sm=' sm' if len(r)>2 else ''
            rows+=f' <div class="row" style="top:{700+i*160}px" data-t="{ts[i]}" data-a="rise"><span class="k grn{sm}">{k}</span><span class="tx">{tx}</span></div>\n'
        S.append(f'''<div class="sc" id="s{4+gi}"><div class="num" style="top:380px">{dg(gi+1)}</div>
 <div class="hl" style="top:540px;font-size:80px">{ttl}</div>
{rows}</div>''')
    cks=''.join(f' <div class="ck" style="top:{640+i*150}px" data-t="{TM["c9"][i]}" data-a="rise"><span class="b grn">✓</span><span>{x}</span></div>\n' for i,x in enumerate(t['c9']))
    S.append(f'''<div class="sc" id="s9">
 <div class="hl" style="top:420px;font-size:100px">{W(t['h9'])}</div>
{cks}</div>''')
    S.append(f'''<div class="sc" id="s10">
 <div class="hl" style="top:430px;font-size:88px">{W(t['h10'])}</div>
 <div class="bub" style="top:780px" data-t="{TM['b10']}" data-a="pop"><small>{t['b10s']}</small><b style="font:900 82px V">{t['b10']}</b></div>
</div>''')
    S.append(f'''<div class="sc" id="s11">
 <div class="ok" style="top:620px;left:50%;font-size:64px" data-t="0.1" data-a="pillx">{t['f11']}</div>
 <div class="url adr" style="top:860px;font-size:60px" data-t="0.6" data-a="pop">{c['url']}</div>
</div>''')
    body=f'''</style></head><body class="{c['cls']}{' tt' if tt else ''}"><div id="st">
<div id="bg"></div><div id="rays"></div><div id="glow"></div><div id="floor"></div><div id="stars"></div><img id="wm" src="{c['logo']}"><div id="scenes">
{chr(10).join(S)}
</div><div id="ft"><div class="q">Quelle: § 10 Abs. 1 Nr. 2 StAG</div><div class="ad">{c['url']}</div><div class="ad" style="margin-top:4px">IG {c['ig']} · TikTok {c['tk']}</div></div><div id="nb"><img src="{c['logo']}"><div class="t">WEGWEISER<span>{c['name']}</span></div><div class="h">{c['h']}</div></div><div id="vig"></div><div class="flash" id="flash"></div></div>'''
    js=open('k254-ku.html').read().split('<script>')[1]
    js=re.sub(r'window\.SC=\[\[.*?\]\];',f"window.SC={TM['SC']};",js)
    js=js.replace("    if(i===10){ $('#url').style.display=TT?'none':''; }\n","").replace("    if(i===11){ $('#lg').style.opacity=TT?0:eo((t-1.5)/0.6); }\n","")
    js=js.replace("  $('#flash').style.opacity=fl;","  $('#flash').style.opacity=fl; $('#wm').style.transform=`rotate(${Math.sin(T0*0.3)*4}deg) scale(${1+Math.sin(T0*0.5)*0.02})`;")
    return head+extra+body+'<script>'+js
TIM={
 'fa':dict(SC=[[0,6.5],[6.5,11.9],[11.9,17.8],[17.8,23.6],[23.6,34.5],[34.5,42.4],[42.4,55.1],[55.1,62.8],[62.8,75.5],[75.5,82.6],[82.6,85.5]],
   s1p=2.6,s1s=4.0,s3ok=3.0,g=[[1.2,3.6],[1.2,6.2],[1.0,4.6],[1.2,6.8,9.9],[1.0,6.4]],c9=[5.4,7.5,9.0,10.5],b10=3.4),
 'ku':dict(SC=[[0,5.8],[5.8,11.8],[11.8,17.2],[17.2,22.8],[22.8,33.0],[33.0,40.2],[40.2,52.5],[52.5,59.5],[59.5,72.6],[72.6,80.2],[80.2,83.5]],
   s1p=3.0,s1s=3.8,s3ok=3.3,g=[[2.1,3.8],[1.9,6.5],[2.4,5.4],[2.3,8.1,11.4],[2.0,5.7]],c9=[5.1,7.2,8.7,10.6],b10=3.7),
}
import sys
for lang in sys.argv[1:] or ['fa']:
    for tt in (0,1):
        open(f"k10b-{lang}{'-tt' if tt else ''}.html",'w').write(page(lang,tt,TIM[lang]))
print('ok')

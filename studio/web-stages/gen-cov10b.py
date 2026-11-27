# Covers for the § 10 StAG video (German passport), fa + ku
src=open('k10-ku.html').read()
head=src.split('</style>')[0]
css='''
.dp{position:absolute;left:300px;top:640px;width:480px;height:660px;border-radius:26px 40px 40px 26px;background:linear-gradient(150deg,#8e2533,#6b1522 55%,#4f0d17);
 box-shadow:0 60px 110px rgba(0,0,0,.6),inset 0 0 0 3px rgba(255,255,255,.07),inset 18px 0 22px rgba(0,0,0,.3);transform:rotate(-7deg);overflow:hidden;direction:ltr}
.dp:before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,rgba(255,255,255,.03) 0 3px,transparent 3px 7px)}
.dp:after{content:"";position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.25),transparent 32%,transparent 70%,rgba(255,255,255,.08))}
.dp .a,.dp .b,.dp .c{position:absolute;left:0;right:0;text-align:center;color:#e9c66f;font-family:I}
.dp .a{top:54px;font:700 25px I;letter-spacing:4px}
.dp .b{top:96px;font:900 31px/1.25 I;letter-spacing:3px}
.dp .c{bottom:64px;font:900 46px I;letter-spacing:10px}
.dp svg.e{position:absolute;left:50%;top:210px;width:230px;margin-left:-115px;fill:#e9c66f}
.dp .chip{position:absolute;left:50%;bottom:150px;width:86px;height:58px;margin-left:-43px;border:4px solid #e9c66f;border-radius:10px;background:none;box-shadow:none;padding:0}
.dp .chip:before{content:"";position:absolute;left:50%;top:50%;width:26px;height:26px;margin:-13px 0 0 -13px;border:4px solid #e9c66f;border-radius:50%}
.stamp{position:absolute;left:50%;top:1045px;line-height:1.3;padding:18px 34px;border:9px solid #2ee07a;border-radius:22px;color:#2ee07a;font:900 74px V;transform:translateX(-50%) rotate(-12deg);background:rgba(4,30,14,.92);box-shadow:0 0 40px rgba(40,220,110,.5);white-space:nowrap}
.para{position:absolute;left:0;right:0;top:1390px;text-align:center;font:900 150px/1 I;direction:ltr;filter:drop-shadow(0 8px 30px rgba(0,0,0,.5))}
.tags{position:absolute;left:40px;right:40px;top:1580px;display:flex;justify-content:center;gap:16px;flex-wrap:wrap;direction:ltr}
.tags span{padding:12px 22px;border-radius:20px;background:rgba(255,255,255,.12);border:2px solid rgba(255,255,255,.3);font:900 36px I}
'''
eagle='<svg class="e" viewBox="0 0 120 120"><path d="M53 30 L10 14 L15 23 L5 26 L13 33 L4 38 L14 43 L6 50 L17 53 L11 61 L24 61 L22 69 L36 64 L46 58 Z"/><path d="M67 30 L110 14 L105 23 L115 26 L107 33 L116 38 L106 43 L114 50 L103 53 L109 61 L96 61 L98 69 L84 64 L74 58 Z"/><path d="M60 10c-6 0-10 4-10 9 0 2 0 3 1 4l-6 2 6 1 1 4c-4 3-6 8-6 14v18c0 8 4 14 8 17l-8 14 8-4 4 8 4-8 8 4-8-14c4-3 8-9 8-17V44c0-6-2-11-6-14l2-8c0-7-4-12-10-12z"/><path d="M44 74l-8 10 6-1-2 6 7-8M76 74l8 10-6-1 2 6-7-8"/><circle cx="56" cy="17" r="1.6" fill="#6b1522"/></svg>'
T={'ku':('ku','logo-ku.png','KURDI','@wegweiser_kurdi','بەبێ ئیقامەی هەمیشەیی','پاسپۆرتی ئەڵمانی<br><span class="g">وەردەگریت!</span>','✓ دەبێت'),
   'fa':('','logo-fa.png','FARSI','@wegweiser_farsi','بدون اقامت دائم','پاس آلمانی<br><span class="g">می‌گیری!</span>','✓ میشه')}
for L,(cls,logo,nm,h,l1,l2,st) in T.items():
    html=head+css+f'''</style></head><body class="{cls}"><div id="st"><div id="bg"></div><div id="rays" style="transform:rotate(8deg)"></div><div id="glow"></div><div id="floor"></div><div id="stars"></div>
<div id="nb" style="top:44px"><img src="{logo}" style="width:120px;height:120px"><div class="t" style="font-size:48px">WEGWEISER<span>{nm}</span></div></div>
<div class="hl" style="top:270px;font-size:78px;line-height:1.3">{l1}<br><span style="font-size:104px">{l2}</span></div>
<div class="dp"><div class="a">EUROPÄISCHE UNION</div><div class="b">BUNDESREPUBLIK<br>DEUTSCHLAND</div>{eagle}<div class="chip"></div><div class="c">REISEPASS</div></div>
<div class="stamp">{st}</div>
<div class="para">§ 10 <span style="font-size:96px">StAG</span></div>
<div class="tags"><span>§ 25 Abs. 2</span><span>§ 25b</span><span>§ 28</span><span>§ 18b</span><span>Blaue Karte</span></div>
<div id="vig"></div></div><script>let seed=5;const rnd=()=>{{seed=(seed*16807)%2147483647;return seed/2147483647}};const st=document.getElementById('stars');
for(let i=0;i<60;i++){{const e=document.createElement('i');e.style.left=rnd()*1080+'px';e.style.top=rnd()*1400+'px';e.style.opacity=.3+rnd()*.7;st.appendChild(e)}}</script></body></html>'''
    open(f'covn-10b-{L}.html','w').write(html)
print('ok')

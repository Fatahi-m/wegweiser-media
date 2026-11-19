import json,re,os
R='/home/claude/wegweiser-media'
ALIAS={'5-Komak-Jobcenter':'5-Hilfen-Jobcenter','5-Yarmati-Jobcenter':'5-Hilfen-Jobcenter','Jobcenter':'5-Hilfen-Jobcenter',
 'Familiennachzug-Ampel':'Familiennachzug','Familiennachzug-Reel-v2':'Familiennachzug','Familiennachzug-v2':'Familiennachzug',
 '25-2-Subsidiaer':'25-2-Genf-Subsidiaer','Karte':'25-2-Karte','AsylG-3-4':'25-2-Karte','25-3':'25-3-Abschiebungsverbot',
 'Niederlassung-Voice':'Niederlassung','Pass-Jawab':'Nationalpass','Ausbildungsduldung-Jawab':'Ausbildungsduldung','Salakan':'Pass-Jahre',
 '25-5-Serie':'25-5','Safar':'Reisen','Safar-1':'Reisen','Safar-2':'Reisen-Duldung','Safar-3':'Reisen-26-3','26-3-v2':'26-3',
 'Kinder':'Kinderzuschlag','Kurdi-25-3':'25-3-Abschiebungsverbot','Kurdi-30-Ehegatte':'30','28-Ehegatte-Kind':'28','30-Ehegatte':'30','31-Jiabunawa':'31-Trennung','Einbuergerung':'Einbuergerung','5-Briefe':'5-Briefe'}
def key(fn):
  k=re.sub(r'^(Wegweiser|Kurdi)-','',os.path.basename(fn));k=re.sub(r'(-Reel)?(-v\d)?\.mp4$','',k);k=re.sub(r'-Reel$','',k)
  return ALIAS.get(k,k)
V={}
def get(k):
  return V.setdefault(k,{'key':k,'de':'','fa':{},'ku':{}})
# LIST.md
for line in open(R+'/archive/LIST.md',encoding='utf8'):
  p=[x.strip() for x in line.split('|')]
  if len(p)>=5 and p[0].endswith('.mp4') and not p[0].startswith('de/'):
    v=get(key(p[0]));lang='fa' if p[0].startswith('fa/') else 'ku'
    v['de']=v['de'] or p[1];v[lang].setdefault('date',p[3])
    if p[4] and p[4]!='—':v[lang].setdefault('caption',p[4])
for qf,lang in [('queue.json','fa'),('queue-ku.json','ku')]:
  for i in json.load(open(R+'/'+qf,encoding='utf8')):
    v=get(key(i['file']));d=v[lang]
    if i.get('caption'):d['caption']=i['caption']
    if i.get('permalink'):d['link']=i['permalink']
    d['posted']=bool(i.get('posted'))
SC={'fa':{'16c-Selbststaendig':'v7/p16c.txt','2027-Aenderungen':'v7/p2027-aenderungen.txt','22-23':'v7/p2223.txt','25-Arten':'v7/p25-arten.txt','25-2-Genf-Subsidiaer':'v7/p252-genf-subsidiaer.txt','25-3-Abschiebungsverbot':'v7/p253-abschiebungsverbot.txt','28':'v7/p28.txt','5-Hilfen-Jobcenter':'v7/p5.txt','Beschaeftigungsduldung':'v7/pbd.txt','Besuchsvisum':'v7/pbesuch.txt','Einstiegsgeld':'v7/pein2.txt','25-2-Karte':'v7/pkarte.txt','Kinderzuschlag':'v7/pkiz.txt','Business-Eintrag':'v7/pbiz-ad-post.txt','Klarna-PayPal-Kredit':'v7/pklarna.txt','Studentenvisum':'v7/pstudent.txt'},
 'ku':{'16c-Selbststaendig':'v7/k16c.txt','25-Arten':'v7/k25-arten.txt','25-2-Genf-Subsidiaer':'v7/k252-genf-subsidiaer.txt','25-3-Abschiebungsverbot':'v7/k253-abschiebungsverbot.txt','25-5':'v7/k255.txt','25a':'v7/k25a.txt','25b-Abs4':'v7/k25b4.txt','25b':'v7/k25bm.txt','5-Hilfen-Jobcenter':'v7/k5.txt','Beschaeftigungsduldung':'v7/kbd.txt','Besuchsvisum':'v7/kbesuch.txt','Duldung-Arten':'v7/kduld.txt','Einstiegsgeld':'v7/kein.txt','Nationalpass':'v7/kpass.txt','Reisen-26-3':'v7/ks3.txt','Pass-Jahre':'v7/ksal.txt','Spurwechsel':'v7/kspur.txt','Business-Eintrag':'v7/kbiz-ad.txt','BAMF':'kv4/bamf.txt','Einbuergerung':'kv4/einb.txt','Kinderzuschlag':'kv4/kinder.txt','Klarna-PayPal-Kredit':'v7/kklarna.txt','Studentenvisum':'v7/kstudent.txt'}}
for lang,m in SC.items():
  for k,f in m.items():
    t=open(R+'/studio/'+f,encoding='utf8').read()
    t='\n'.join(l for l in t.split('\n') if not l.startswith('#')).strip()
    get(k)[lang]['script']=t
out=[v for v in V.values() if v['fa'] or v['ku']]
json.dump(out,open('/tmp/claude-0/-home-claude/11eac032-5b7c-50d3-86d1-e804a1356878/scratchpad/videos.json','w'),ensure_ascii=False,indent=0)
print(len(out))
for v in sorted(out,key=lambda x:x['key']): print(v['key'],'|',v['de'][:40],'|fa:',''.join(c for c in 'CLS' if (v['fa'].get('caption') and c=='C') or (v['fa'].get('link') and c=='L') or (v['fa'].get('script') and c=='S')),'|ku:',''.join(c for c in 'CLS' if (v['ku'].get('caption') and c=='C') or (v['ku'].get('link') and c=='L') or (v['ku'].get('script') and c=='S')))

from kbase import *
W_ = (255,255,255)
SPEC = {"source": "§ 6a BKGG · § 90 SGB VIII · Familienkasse", "topic": "Kinderzuschlag", "footer": "زانیاریی گشتییە · بۆ حاڵەتی تایبەت پرسیار لە Familienkasse بکە",
 "scenes": [
  [("title","Kindergeld هەموو کەس دەیناسێت…",70),("title","بەڵام ئەم پارەیەی تر چی؟",84,KRED),("card","Kindergeld","یارمەتیی منداڵ")],
  [("chip","١ · Kindergeld",SUN,INK,44),("big","259 €"),("text","مانگانە بۆ هەر منداڵێک · ٢٠٢٦",52),
   ("card","Familienkasse","ئەو فەرمانگەیەی Kindergeld دەدات"),("row","تەنها تا ٦ مانگ بۆ دواوە دەدرێت","info")],
  [("chip","٢ · ئەو پارەیەی زۆر کەس نایناسێت",KRED,W_,42),("card","Kinderzuschlag","یارمەتیی زیادە بۆ منداڵ"),
   ("text","تا",56,MUTED),("big","297 €"),("text","مانگانە بۆ هەر منداڵێک",52),("chip","+ لەسەر Kindergeld",GREEN,W_,46)],
  [("title","کێ وەریدەگرێت؟",80),("row","کار دەکەیت بەڵام داهاتت بەس نییە","ok"),("row","ژن و مێرد: لانیکەم ٩٠٠ یۆرۆ","ok","Brutto"),
   ("row","دایک یان باوکی تەنها: لانیکەم ٦٠٠ یۆرۆ","ok","Brutto"),("row","لەگەڵ ئەمە پێکەوە نابێت:","no","Grundsicherungsgeld")],
  [("title","سوودی زیاتر",80),("chip","Bildung und Teilhabe",GREEN,W_,40,True),("row","پارەی باخچەی ساوایان نادەیت","ok","Kita"),
   ("row","یارمەتی بۆ قوتابخانە و گەشت","ok"),("row","یارمەتیی خواردنی نیوەڕۆ","ok")],
  [("chip","زۆر گرنگ",KRED,W_,50),("title","بۆ مانگەکانی پێش داواکاری",68),("title","هیچ پارەیەک نادرێت!",84,KRED),
   ("row","هەر ئەم مانگە ئۆنلاین داوا بکە","ok","Familienkasse")],
 ],
 "outro": ("ئەم ڤیدیۆیە هەڵبگرە","و بۆ خێزانە منداڵدارەکان بنێرە")}

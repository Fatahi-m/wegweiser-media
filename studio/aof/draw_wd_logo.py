import math
from PIL import Image, ImageDraw, ImageFont
S=1600; c=S/2; k=2
N=(22,58,122); W=(255,255,255); R=(226,35,26); SOFT=(200,214,236)
im=Image.new("RGBA",(S,S),(0,0,0,0)); d=ImageDraw.Draw(im)
def circ(r,**kw): d.ellipse((c-r,c-r,c+r,c+r),**kw)
circ(398*k,fill=W); circ(372*k,fill=N); circ(352*k,outline=SOFT,width=5*k); circ(232*k,outline=SOFT,width=5*k)
f=ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Black.otf",56*k)
def arc(text,r,top,step):
    n=len(text); span=step*(n-1)
    for i,ch in enumerate(text):
        ang=(-90-span/2+i*step) if top else (90+span/2-i*step)
        g=Image.new("RGBA",(120*k,120*k),(0,0,0,0)); ImageDraw.Draw(g).text((60*k,60*k),ch,font=f,fill=W,anchor="mm")
        rot=-(ang+90) if top else -(ang-90)
        g=g.rotate(rot,resample=Image.BICUBIC)
        x=c+r*math.cos(math.radians(ang)); y=c+r*math.sin(math.radians(ang))
        im.alpha_composite(g,(int(x-60*k),int(y-60*k)))
arc("WEGWEISER",292*k,True,13.5); arc("DEUTSCHLAND",292*k,False,11.5)
for x in (c-292*k,c+292*k): d.ellipse((x-10*k,c-10*k,x+10*k,c+10*k),fill=R)
d.polygon([(c,c-230*k),(c+28*k,c),(c-28*k,c)],fill=R)
d.polygon([(c,c+230*k),(c+28*k,c),(c-28*k,c)],fill=W)
d.polygon([(c-200*k,c),(c,c-28*k),(c,c+28*k)],fill=W)
d.polygon([(c+200*k,c),(c,c-28*k),(c,c+28*k)],fill=W)
circ(16*k,fill=N); circ(7*k,fill=W)
im.resize((800,800),Image.LANCZOS).save("wegweiser-deutschland-logo.png")
bg=Image.new("RGBA",(400,400),N+(255,)); bg.alpha_composite(im.resize((400,400),Image.LANCZOS)); bg.save("/tmp/claude-0/-home-claude/4d07e347-cc90-5f2d-8090-ac6551bb4e4d/scratchpad/wdl.png")

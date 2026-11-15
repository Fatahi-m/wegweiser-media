import math
from PIL import Image, ImageDraw
S=1200; c=S/2; k=S/592
im=Image.new("RGB",(S,S),(250,246,236)); d=ImageDraw.Draw(im)
G=(14,92,62); R=(206,32,41); SUN=(242,169,0); CR=(250,246,236)
d.ellipse((0,0,S-1,S-1),fill=G)
r=c-24*k; d.ellipse((c-r,c-r,c+r,c+r),fill=CR)
r1=c-30*k; d.ellipse((c-r1,c-r1,c+r1,c+r1),fill=R); r2=r1-15*k; d.ellipse((c-r2,c-r2,c+r2,c+r2),fill=CR)
n=20
for i in range(n):
    a=2*math.pi*i/n-math.pi/2; L=190*k if i%2==0 else 160*k; w=math.pi/n*0.32
    d.polygon([(c+math.cos(a-w)*95*k,c+math.sin(a-w)*95*k),(c+math.cos(a)*L,c+math.sin(a)*L),(c+math.cos(a+w)*95*k,c+math.sin(a+w)*95*k)],fill=SUN)
rs=100*k; d.ellipse((c-rs,c-rs,c+rs,c+rs),fill=SUN)
a=math.radians(-45); ux,uy=math.cos(a),math.sin(a); px,py=-uy,ux; L=135*k; Wd=24*k
tip1=(c+ux*L,c+uy*L); tip2=(c-ux*L,c-uy*L); s1=(c+px*Wd,c+py*Wd); s2=(c-px*Wd,c-py*Wd)
d.polygon([tip1,s1,s2],fill=R); d.polygon([tip2,s1,s2],fill=(16,60,44))
rc=17*k; d.ellipse((c-rc,c-rc,c+rc,c+rc),fill=CR); rc2=8*k; d.ellipse((c-rc2,c-rc2,c+rc2,c+rc2),fill=G)
im.save("brand_k/Kurdi-Profilbild.jpg",quality=95)
im.resize((592,592),Image.LANCZOS).save("/tmp/claude-0/-home-claude/4d07e347-cc90-5f2d-8090-ac6551bb4e4d/scratchpad/logo2.png")

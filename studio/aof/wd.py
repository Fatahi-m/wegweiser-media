import cairosvg, math
NAVY="#123E7C"; DNAVY="#0B2A57"; RED="#E2231A"; DRED="#A8150F"; WHITE="#FFFFFF"
def ring_text(text, r, start, size, color):
    out=""; n=len(text); step=9.6
    for i,ch in enumerate(text):
        a=math.radians(start+i*step); x=540+r*math.sin(a); y=540-r*math.cos(a)
        out+=f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter Display Black, Inter, DejaVu Sans" font-weight="900" font-size="{size}" fill="{color}" text-anchor="middle" dominant-baseline="middle" transform="rotate({start+i*step:.1f} {x:.1f} {y:.1f})">{ch}</text>'
    return out
top="WEGWEISER"; bot="DEUTSCHLAND"
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080">
<rect width="1080" height="1080" fill="{WHITE}"/>
<circle cx="540" cy="540" r="500" fill="{NAVY}"/>
<circle cx="540" cy="540" r="470" fill="none" stroke="{WHITE}" stroke-width="6"/>
<circle cx="540" cy="540" r="330" fill="none" stroke="{WHITE}" stroke-width="6"/>
{ring_text(top,400,-(len(top)-1)*9.6/2,56,WHITE)}
{ring_text(bot[::-1],400,180-(len(bot)-1)*9.6/2,56,WHITE).replace('rotate(','rotate(180+') if False else ''}
'''
# bottom text upright: place along lower arc reading left->right
bt=""; step=9.6; n=len(bot); start=180+(n-1)*step/2
for i,ch in enumerate(bot):
    a=math.radians(start-i*step); x=540+400*math.sin(a); y=540-400*math.cos(a)
    bt+=f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter Display Black, Inter, DejaVu Sans" font-weight="900" font-size="56" fill="{WHITE}" text-anchor="middle" dominant-baseline="middle" transform="rotate({start-i*step-180:.1f} {x:.1f} {y:.1f})">{ch}</text>'
svg+=bt
# side dots
for ang in (90,270):
    a=math.radians(ang); x=540+400*math.sin(a); y=540-400*math.cos(a)
    svg+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="{RED}"/>'
# compass needle (N long red, others short)
def needle(ang,L,w,c1,c2):
    a=math.radians(ang); px,py=math.sin(a),-math.cos(a); qx,qy=math.cos(a),math.sin(a)
    tip=(540+L*px,540+L*py); l=(540+w*qx,540+w*qy); r=(540-w*qx,540-w*qy)
    return (f'<polygon points="540,540 {tip[0]:.1f},{tip[1]:.1f} {l[0]:.1f},{l[1]:.1f}" fill="{c1}"/>'
            f'<polygon points="540,540 {tip[0]:.1f},{tip[1]:.1f} {r[0]:.1f},{r[1]:.1f}" fill="{c2}"/>')
svg+=needle(90,250,46,"#DCE6F5",WHITE)+needle(270,250,46,"#DCE6F5",WHITE)+needle(180,250,46,"#DCE6F5",WHITE)
svg+=needle(0,310,62,RED,DRED)
svg+=f'<circle cx="540" cy="540" r="34" fill="{WHITE}"/><circle cx="540" cy="540" r="16" fill="{NAVY}"/>'
svg+='</svg>'
cairosvg.svg2png(bytestring=svg.encode(),write_to="wegweiser-deutschland-logo.png",output_width=1080,output_height=1080)

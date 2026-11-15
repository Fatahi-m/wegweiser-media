import cairosvg, sys, os
out = sys.argv[1]
NAVY="#0F1A2B"; PANEL="#17263D"; MUST="#F2B632"; MUSTD="#D99A1C"; SKIN="#E8C4A0"
RENT="#E2685A"; LIFE="#5AA9E2"; SAVE="#6CC79A"; CHALK="#EEF1F4"; MUTED="#93A3B8"

def kalle(cx, cy, s, beanie=MUST, beanie_d=MUSTD):
    # head centred at (cx,cy), radius 135*s ; drawn in local units then scaled
    return f'''<g transform="translate({cx} {cy}) scale({s})">
      <circle cx="0" cy="0" r="135" fill="{SKIN}"/>
      <path d="M-140 -20 C-140 -150 140 -150 140 -20 L140 -50 C140 -185 -140 -185 -140 -50Z" fill="{beanie}"/>
      <rect x="-142" y="-52" width="284" height="40" rx="14" fill="{beanie_d}"/>
      <circle cx="0" cy="-168" r="24" fill="{beanie_d}"/>
      <circle cx="-48" cy="20" r="34" fill="none" stroke="{NAVY}" stroke-width="8"/>
      <circle cx="48" cy="20" r="34" fill="none" stroke="{NAVY}" stroke-width="8"/>
      <line x1="-14" y1="20" x2="14" y2="20" stroke="{NAVY}" stroke-width="8"/>
      <circle cx="-48" cy="24" r="8" fill="{NAVY}"/><circle cx="48" cy="24" r="8" fill="{NAVY}"/>
      <path d="M-34 78 Q0 104 34 78" fill="none" stroke="{NAVY}" stroke-width="9" stroke-linecap="round"/>
    </g>'''

grid = lambda w,h: f'''<defs><pattern id="g" width="64" height="64" patternUnits="userSpaceOnUse"><path d="M64 0H0V64" fill="none" stroke="#1C2D49" stroke-width="2"/></pattern></defs><rect width="{w}" height="{h}" fill="{NAVY}"/><rect width="{w}" height="{h}" fill="url(#g)"/>'''

# LOGO 800x800 (YouTube crops to circle)
logo = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800">
  <rect width="800" height="800" fill="{MUST}"/>
  <circle cx="400" cy="400" r="330" fill="{NAVY}"/>
  {kalle(400, 440, 1.55, beanie=MUST, beanie_d=MUSTD)}
</svg>'''

# BANNER 2560x1440 ; safe area x 507-2053, y 508-931
title_font = "Inter Display Black, Inter, DejaVu Sans, sans-serif"
body_font = "Inter, DejaVu Sans, sans-serif"
bar_x, bar_w = 560, 960
segs = [(0.45,RENT,"Miete"),(0.40,LIFE,"Leben"),(0.15,SAVE,"Rest")]
bars=""; x=bar_x
for f,c,l in segs:
    w=bar_w*f
    bars+=f'<rect x="{x:.0f}" y="808" width="{w-8:.0f}" height="22" rx="4" fill="{c}"/>'
    x+=w
banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="2560" height="1440">
  {grid(2560,1440)}
  <rect x="0" y="1360" width="2560" height="80" fill="{MUST}"/>
  <rect x="0" y="0" width="2560" height="80" fill="{MUST}"/>
  <text x="560" y="600" fill="{MUST}" font-family="DejaVu Sans Mono, monospace" font-weight="bold" font-size="34" letter-spacing="6">BRUTTO → NETTO → DEIN LEBEN</text>
  <text x="552" y="735" fill="{CHALK}" font-family="{title_font}" font-weight="900" font-size="112" letter-spacing="-1">GELD OHNE FILTER</text>
  {bars}
  <text x="560" y="895" fill="{MUTED}" font-family="{body_font}" font-weight="600" font-size="40">Gehalt · Steuern · Rente – ehrlich erklärt. Jede Woche neu.</text>
  <circle cx="1870" cy="720" r="175" fill="{PANEL}"/>
  {kalle(1870, 742, 0.95)}
</svg>'''

for name, svg, w, h in [("logo", logo, 800, 800), ("banner", banner, 2560, 1440)]:
    open(os.path.join(out, name+".svg"), "w").write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(out, name+".png"), output_width=w, output_height=h)
print("ok")

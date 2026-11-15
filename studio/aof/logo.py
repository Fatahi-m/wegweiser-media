import cairosvg
NAVY="#0F1A2B"; SKIN="#E8C4A0"; TEAL="#2BB3A3"
BLACK="#1B1B1B"; RED="#DD2C2C"; GOLD="#F2C230"
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080">
<rect width="1080" height="1080" fill="{TEAL}"/>
<circle cx="540" cy="540" r="450" fill="#F4EFE6"/>
<g transform="translate(540 600) scale(2.05)">
  <clipPath id="hat"><path d="M-140 -20 C-140 -150 140 -150 140 -20 L140 -50 C140 -185 -140 -185 -140 -50Z"/></clipPath>
  <circle r="135" fill="{SKIN}"/>
  <g clip-path="url(#hat)">
    <rect x="-150" y="-190" width="300" height="60" fill="{BLACK}"/>
    <rect x="-150" y="-130" width="300" height="50" fill="{RED}"/>
    <rect x="-150" y="-80" width="300" height="70" fill="{GOLD}"/>
  </g>
  <rect x="-142" y="-52" width="284" height="40" rx="14" fill="{GOLD}"/>
  <circle cy="-168" r="24" fill="{BLACK}"/>
  <circle cx="-48" cy="20" r="34" fill="none" stroke="{NAVY}" stroke-width="8"/>
  <circle cx="48" cy="20" r="34" fill="none" stroke="{NAVY}" stroke-width="8"/>
  <line x1="-14" y1="20" x2="14" y2="20" stroke="{NAVY}" stroke-width="8"/>
  <circle cx="-48" cy="24" r="8" fill="{NAVY}"/><circle cx="48" cy="24" r="8" fill="{NAVY}"/>
  <path d="M-34 78 Q0 104 34 78" fill="none" stroke="{NAVY}" stroke-width="9" stroke-linecap="round"/>
</g>
</svg>'''
cairosvg.svg2png(bytestring=svg.encode(),write_to="alman-ohne-filter-logo.png",output_width=1080,output_height=1080)

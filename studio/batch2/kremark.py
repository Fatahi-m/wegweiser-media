from kbase import *
from PIL import ImageFont
def remark(code, w=820):
    h = 150
    c = rounded(w, h, 18, (226, 228, 230), outline=(190, 194, 198), ow=3)
    a = text_sprite("ANMERKUNGEN/REMARKS", la("Bold", 26), (70, 74, 80)); c.alpha_composite(a, (36, 20))
    b = text_sprite(code, ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 54), (40, 44, 50)); c.alpha_composite(b, (36, 62))
    return shadowed(c, radius=14, off=(0, 8), alpha=50)

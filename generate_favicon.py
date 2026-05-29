"""Genera favicon PNG per Datace — navy square, D bianca, barra teal, freccia oro."""
from PIL import Image, ImageDraw
import math, os

def rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0+radius, y0, x1-radius, y1], fill=fill)
    draw.rectangle([x0, y0+radius, x1, y1-radius], fill=fill)
    draw.ellipse([x0, y0, x0+2*radius, y0+2*radius], fill=fill)
    draw.ellipse([x1-2*radius, y0, x1, y0+2*radius], fill=fill)
    draw.ellipse([x0, y1-2*radius, x0+2*radius, y1], fill=fill)
    draw.ellipse([x1-2*radius, y1-2*radius, x1, y1], fill=fill)

def make_favicon(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    s = size

    # Sfondo navy arrotondato
    r = int(s * 0.22)
    rounded_rect(draw, [0, 0, s-1, s-1], r, (28, 52, 97, 255))

    # D shape (outer) bianca
    dx0, dy0, dx1, dy1 = int(s*.18), int(s*.22), int(s*.66), int(s*.78)
    dm = int(s*.41)  # metà curva
    # Rettangolo verticale sinistro
    draw.rectangle([dx0, dy0, dx0+int(s*.12), dy1], fill=(255,255,255,255))
    # Semicerchio destra
    draw.ellipse([dx0+int(s*.05), dy0, dx1, dy1], fill=(255,255,255,255))

    # Cutout interno navy (per fare la "D" cava)
    cx0 = dx0+int(s*.14)
    cx1 = dx1-int(s*.08)
    cy0 = dy0+int(s*.09)
    cy1 = dy1-int(s*.09)
    draw.rectangle([cx0, cy0, cx0+int(s*.06), cy1], fill=(28,52,97,255))
    draw.ellipse([cx0+int(s*.02), cy0, cx1, cy1], fill=(28,52,97,255))

    # Barra teal sinistra
    draw.rectangle([dx0, dy0, dx0+int(s*.07), dy1], fill=(42, 157, 181, 255))

    # Freccia oro top-right
    ax = int(s*.58)
    ay = int(s*.18)
    aw = int(s*.22)
    ah = int(s*.18)
    lw = max(2, int(s*.04))
    gold = (196, 151, 43, 255)
    # Orizzontale
    draw.line([ax, ay, ax+aw, ay], fill=gold, width=lw)
    # Verticale
    draw.line([ax+aw, ay, ax+aw, ay+ah], fill=gold, width=lw)
    # Diagonale
    draw.line([ax+int(aw*.4), ay+int(ah*.6), ax+aw, ay], fill=gold, width=lw)

    return img

# Genera dimensioni multiple
out_dir = os.path.dirname(os.path.abspath(__file__))
sizes = [16, 32, 48, 96, 192, 512]

for sz in sizes:
    img = make_favicon(sz)
    path = os.path.join(out_dir, 'images', f'favicon-{sz}.png')
    img.save(path, 'PNG')
    print(f'  ✓ favicon-{sz}.png')

# Favicon principale 32px
img32 = make_favicon(32)
img32.save(os.path.join(out_dir, 'favicon.png'), 'PNG')
print('  ✓ favicon.png (root)')

# Apple touch icon 180px
img180 = make_favicon(180)
img180.save(os.path.join(out_dir, 'apple-touch-icon.png'), 'PNG')
print('  ✓ apple-touch-icon.png')

# ICO (16+32 inside)
img16 = make_favicon(16)
img32.save(os.path.join(out_dir, 'favicon.ico'), format='ICO',
           sizes=[(16,16),(32,32)])
print('  ✓ favicon.ico (root)')

print('\nDone!')

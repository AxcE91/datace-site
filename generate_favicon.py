"""Genera favicon PNG per Datace — STRATA logo: navy gradient, 3 barre (gold, white, white-dim)."""
from PIL import Image, ImageDraw
import os

def lerp_color(c1, c2, t):
    """Interpola tra due colori RGBA."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(4))

def rounded_rect(draw, x0, y0, x1, y1, radius, fill):
    r = max(1, radius)
    draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
    draw.rectangle([x0, y0 + r, x1, y1 - r], fill=fill)
    draw.ellipse([x0, y0, x0 + 2*r, y0 + 2*r], fill=fill)
    draw.ellipse([x1 - 2*r, y0, x1, y0 + 2*r], fill=fill)
    draw.ellipse([x0, y1 - 2*r, x0 + 2*r, y1], fill=fill)
    draw.ellipse([x1 - 2*r, y1 - 2*r, x1, y1], fill=fill)

def gradient_rect(img, x0, y0, x1, y1, color_left, color_right, radius=0):
    """Disegna un rettangolo con gradiente orizzontale."""
    draw = ImageDraw.Draw(img)
    w = x1 - x0
    if w <= 0:
        return
    for x in range(x0, x1 + 1):
        t = (x - x0) / max(w, 1)
        col = lerp_color(color_left, color_right, t)
        # Solo disegna dentro il rettangolo arrotondato (approssimazione)
        if radius > 0:
            draw.line([(x, y0 + radius), (x, y1 - radius)], fill=col)
            if x <= x0 + radius:
                # Angoli sinistri
                dist = x0 + radius - x
                y_off = int((radius**2 - dist**2)**0.5) if radius**2 >= dist**2 else 0
                draw.line([(x, y0 + radius - y_off), (x, y1 - radius + y_off)], fill=col)
            elif x >= x1 - radius:
                dist = x - (x1 - radius)
                y_off = int((radius**2 - dist**2)**0.5) if radius**2 >= dist**2 else 0
                draw.line([(x, y0 + radius - y_off), (x, y1 - radius + y_off)], fill=col)
            else:
                draw.line([(x, y0), (x, y1)], fill=col)
        else:
            draw.line([(x, y0), (x, y1)], fill=col)

def make_favicon(size):
    s = size
    img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ── Sfondo: gradiente navy #1c3461 → #1d7a94 (top-left → bottom-right) ──
    navy1 = (28, 52, 97, 255)
    navy2 = (29, 122, 148, 255)
    bg_radius = max(1, int(s * 0.22))

    # Disegna il gradiente diagonale approssimato con linee
    for y in range(s):
        for x in range(s):
            t = (x + y) / (2 * s)
            col = lerp_color(navy1, navy2, t)
            img.putpixel((x, y), col)

    # Maschera arrotondata per il background
    mask = Image.new('L', (s, s), 0)
    mask_draw = ImageDraw.Draw(mask)
    r = bg_radius
    mask_draw.rectangle([r, 0, s-r, s], fill=255)
    mask_draw.rectangle([0, r, s, s-r], fill=255)
    mask_draw.ellipse([0, 0, 2*r, 2*r], fill=255)
    mask_draw.ellipse([s-2*r, 0, s, 2*r], fill=255)
    mask_draw.ellipse([0, s-2*r, 2*r, s], fill=255)
    mask_draw.ellipse([s-2*r, s-2*r, s, s], fill=255)

    # Applica la maschera (rende trasparente fuori dal rounded rect)
    for y in range(s):
        for x in range(s):
            if mask.getpixel((x, y)) == 0:
                img.putpixel((x, y), (0, 0, 0, 0))

    draw = ImageDraw.Draw(img)

    # ── Tre barre STRATA ──
    # Padding laterale: ~20% del size
    pad_x  = int(s * 0.20)
    bar_h  = max(2, int(s * 0.13))   # altezza barra
    gap    = max(1, int(s * 0.10))   # spazio tra barre
    total_h = bar_h * 3 + gap * 2
    start_y = (s - total_h) // 2
    bar_rx  = max(1, bar_h // 2)

    full_w   = s - pad_x * 2          # larghezza piena (barra 1)
    mid_w    = int(full_w * 0.70)     # barra 2
    short_w  = int(full_w * 0.43)     # barra 3

    gold1 = (245, 158, 11, 255)
    gold2 = (251, 191, 36, 255)
    white = (255, 255, 255, 255)
    white_dim = (255, 255, 255, 100)

    # Barra 1 — Gold gradient
    y1 = start_y
    for xi in range(pad_x, pad_x + full_w + 1):
        t = (xi - pad_x) / max(full_w, 1)
        col = lerp_color(gold1, gold2, t)
        # Arrotondamento manuale semplificato
        dist_left  = xi - pad_x
        dist_right = (pad_x + full_w) - xi
        min_dist = min(dist_left, dist_right)
        if min_dist < bar_rx:
            y_off = int((bar_rx**2 - min_dist**2) ** 0.5) if bar_rx**2 >= min_dist**2 else 0
            draw.line([(xi, y1 + bar_rx - y_off), (xi, y1 + bar_h - bar_rx + y_off)], fill=col)
        else:
            draw.line([(xi, y1), (xi, y1 + bar_h)], fill=col)

    # Barra 2 — White
    y2 = start_y + bar_h + gap
    rounded_rect(draw, pad_x, y2, pad_x + mid_w, y2 + bar_h, bar_rx, white)

    # Barra 3 — White dim
    y3 = start_y + (bar_h + gap) * 2
    rounded_rect(draw, pad_x, y3, pad_x + short_w, y3 + bar_h, bar_rx, white_dim)

    return img

# ── Output ──
out_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(out_dir, 'images')
os.makedirs(img_dir, exist_ok=True)

sizes = [16, 32, 48, 96, 192, 512]
imgs = {}

for sz in sizes:
    img = make_favicon(sz)
    imgs[sz] = img
    path = os.path.join(img_dir, f'favicon-{sz}.png')
    img.save(path, 'PNG')
    print(f'  OKfavicon-{sz}.png')

# favicon.png root (32px)
imgs[32].save(os.path.join(out_dir, 'favicon.png'), 'PNG')
print('  OKfavicon.png (root)')

# apple-touch-icon 180px
img180 = make_favicon(180)
img180.save(os.path.join(out_dir, 'apple-touch-icon.png'), 'PNG')
print('  OKapple-touch-icon.png')

# favicon.ico (16 + 32)
imgs[32].save(
    os.path.join(out_dir, 'favicon.ico'),
    format='ICO',
    sizes=[(16, 16), (32, 32)]
)
print('  OKfavicon.ico (root)')

print('\nDone! Nuovo logo STRATA applicato.')

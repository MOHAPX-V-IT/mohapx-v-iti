import json, math, random, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
BG   = (7, 7, 11)
ACC  = (255, 154, 31)
ACC2 = (255, 201, 120)
DEEP = (255, 106, 0)
TX   = (237, 237, 242)
DIM  = (99, 98, 111)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FMR= "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

def f(path, size): return ImageFont.truetype(path, size)

def glow(img, box_layer, radius=26, strength=1.0):
    b = box_layer.filter(ImageFilter.GaussianBlur(radius))
    return Image.alpha_composite(img, Image.blend(Image.new('RGBA', img.size, (0,0,0,0)), b, strength))

def rgba(c, a): return (c[0], c[1], c[2], a)

def base(rnd):
    im = Image.new('RGBA', (W, H), BG + (255,))
    d = ImageDraw.Draw(im)
    # radial warm glow
    gl = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(gl)
    cx, cy = rnd.choice([(W*0.82, -60), (W*0.18, H*0.1), (W*0.9, H*0.85)])
    for i in range(28):
        r = 620 - i*20
        a = int(3 + i*0.9)
        gd.ellipse([cx-r, cy-r, cx+r, cy+r], fill=rgba(DEEP, a))
    gl = gl.filter(ImageFilter.GaussianBlur(60))
    im = Image.alpha_composite(im, gl)
    # perspective grid at the bottom
    g = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(g)
    horizon = H*0.62
    for i in range(-14, 30):
        x0 = W/2 + i*46
        gd.line([(x0, H), (W/2 + i*11, horizon)], fill=rgba(ACC, 26), width=1)
    y = horizon
    step = 3.0
    while y < H:
        gd.line([(0, y), (W, y)], fill=rgba(ACC, 22), width=1)
        step *= 1.34
        y += step
    im = Image.alpha_composite(im, g)
    return im

# ---------- motifs ----------
def motif_field(d, rnd):
    """scattered nodes + links — заметки из практики"""
    pts = [(rnd.randint(700, 1140), rnd.randint(90, 520)) for _ in range(11)]
    for i, p in enumerate(pts):
        for q in pts[i+1:]:
            if math.dist(p, q) < 210:
                d.line([p, q], fill=rgba(ACC, 70), width=1)
    for i, p in enumerate(pts):
        r = 4 if i % 3 else 8
        col = ACC if i % 3 == 0 else ACC2
        d.ellipse([p[0]-r, p[1]-r, p[0]+r, p[1]+r], fill=rgba(col, 235))
        if i % 4 == 0:
            d.ellipse([p[0]-r-9, p[1]-r-9, p[0]+r+9, p[1]+r+9], outline=rgba(col, 90), width=1)

def motif_case(d, rnd):
    """pipeline blocks — разбор"""
    x, y = 706, 150
    for i in range(4):
        yy = y + i*96
        d.rounded_rectangle([x, yy, x+300, yy+62], radius=10,
                            outline=rgba(ACC, 150 if i % 2 == 0 else 90), width=2)
        d.rectangle([x+16, yy+22, x+16+ (60 + i*34), yy+40], fill=rgba(ACC, 60 + i*36))
        if i < 3:
            d.line([(x+150, yy+62), (x+150, yy+96)], fill=rgba(ACC, 120), width=2)
            d.polygon([(x+150, yy+96), (x+144, yy+86), (x+156, yy+86)], fill=rgba(ACC, 190))

def motif_take(d, rnd):
    """bold diagonal bands + quote — мнение"""
    for i in range(7):
        x = 690 + i*74
        a = 30 + i*22
        d.polygon([(x, 90), (x+40, 90), (x-120, 545), (x-160, 545)], fill=rgba(ACC, min(a, 170)))
    d.text((760, 210), "”", font=f(FB, 340), fill=rgba(ACC2, 210))

def motif_tool(d, rnd):
    """concentric arcs — инструмент"""
    cx, cy = 940, 315
    for i in range(9):
        r = 60 + i*26
        start = rnd.randint(0, 360)
        ext = rnd.choice([90, 130, 200, 260])
        d.arc([cx-r, cy-r, cx+r, cy+r], start, start+ext,
              fill=rgba(ACC if i % 2 else ACC2, 90 + i*14), width=3 if i % 3 else 1)
    d.ellipse([cx-13, cy-13, cx+13, cy+13], fill=rgba(ACC, 240))

def motif_num(d, rnd):
    """bars — цифра"""
    x0, base_y = 720, 500
    hs = [90, 160, 120, 250, 300, 210, 340]
    for i, hh in enumerate(hs):
        x = x0 + i*58
        d.rectangle([x, base_y-hh, x+34, base_y], fill=rgba(ACC, 45 + i*26))
        d.rectangle([x, base_y-hh, x+34, base_y-hh+4], fill=rgba(ACC2, 240))
    d.line([(x0-16, base_y+2), (x0+7*58+8, base_y+2)], fill=rgba(ACC, 140), width=2)

MOTIF = {"поле": motif_field, "разбор": motif_case, "мнение": motif_take,
         "инструмент": motif_tool, "цифра": motif_num}
LATIN = {"поле": "FIELD NOTES", "разбор": "CASE STUDY", "мнение": "TAKE",
         "инструмент": "TOOLING", "цифра": "NUMBER"}

def crown(d, x, y, s, col):
    pts = [(x, y+s*0.78), (x, y+s*0.22), (x+s*0.26, y+s*0.44),
           (x+s*0.5, y), (x+s*0.74, y+s*0.44), (x+s, y+s*0.22), (x+s, y+s*0.78)]
    d.polygon(pts, fill=col)
    d.rectangle([x, y+s*0.86, x+s, y+s*1.0], fill=col)

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def render(post, out, lang="ru"):
    rnd = random.Random(1000 + post["n"])
    im = base(rnd)
    layer = Image.new('RGBA', (W, H), (0,0,0,0))
    d = ImageDraw.Draw(layer)
    MOTIF[post["rubric"]](d, rnd)
    im = Image.alpha_composite(im, layer.filter(ImageFilter.GaussianBlur(9)))
    im = Image.alpha_composite(im, layer)

    d = ImageDraw.Draw(im)
    # left scrim so the title stays readable over the motif
    scrim = Image.new('RGBA', (W, H), (0,0,0,0))
    sd = ImageDraw.Draw(scrim)
    for i in range(70):
        sd.rectangle([0, 0, 640 + i*3, H], fill=(7, 7, 11, 4))
    im = Image.alpha_composite(im, scrim.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(im)

    # top bar
    top = ("// " + post["rubric"].upper()) if lang=="ru" else ("// " + LATIN[post["rubric"]].split()[0])
    d.text((64, 56), top, font=f(FM, 22), fill=ACC)
    tag = LATIN[post["rubric"]] if lang=="ru" else post["rubric"].upper()
    d.text((W-64-d.textlength(tag, font=f(FMR, 19)), 58), tag, font=f(FMR, 19), fill=DIM)
    d.line([(64, 100), (W-64, 100)], fill=(255, 154, 31, 60), width=1)

    # number
    num = "%02d" % post["n"]
    d.text((64, 132), num, font=f(FB, 64), fill=(38, 33, 30))

    # title
    ft = f(FB, 56)
    title = post["title"] if lang=="ru" else post["title_en"]
    lines = wrap(d, title, ft, 600)
    if len(lines) > 3:
        ft = f(FB, 44); lines = wrap(d, title, ft, 600)
    y = 300 - len(lines)*(ft.size+14)//2
    for ln in lines:
        d.text((64, y), ln, font=ft, fill=TX)
        y += ft.size + 14

    # accent underline
    d.rectangle([64, y+18, 64+150, y+22], fill=ACC)

    # footer brand
    crown(d, 64, H-92, 26, ACC)
    d.text((102, H-92), "MOHAPX-V-IT", font=f(FM, 22), fill=TX)
    dt = post["date"]
    d.text((W-64-d.textlength(dt, font=f(FMR, 19)), H-88), dt, font=f(FMR, 19), fill=DIM)

    # scanlines
    sl = Image.new('RGBA', (W, H), (0,0,0,0))
    sd = ImageDraw.Draw(sl)
    for yy in range(0, H, 3):
        sd.line([(0, yy), (W, yy)], fill=(255, 255, 255, 6), width=1)
    im = Image.alpha_composite(im, sl)

    im.convert('RGB').save(out, 'JPEG', quality=86, optimize=True, progressive=True)

data = json.load(open('posts.json', encoding='utf-8'))
os.makedirs('site/journal', exist_ok=True)
made = 0
for p in data["posts"]:
    for lang, suf in (("ru",""), ("en","e")):
        out = "site/journal/j%02d%s.jpg" % (p["n"], suf)
        if os.path.exists(out):
            continue          # обложка уже есть — не трогаем, чтобы не было лишних изменений
        render(p, out, lang)
        made += 1
print("covers generated:", made)

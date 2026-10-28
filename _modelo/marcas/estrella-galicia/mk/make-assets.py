"""Monta as telas do media kit com os criativos da Estrella Galicia (rodar na raiz do repo, depois do build-jogo.py).
Saída: mk/out-popup.webp, mk/out-mcscr.webp, mk/out-especial.webp"""
import os, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
M = os.path.dirname(D)
FONTS = os.path.expanduser('~/.fonts')
def font(fam, w, size):
    return ImageFont.truetype(os.path.join(FONTS, f'{fam}-latin-{w}-normal.ttf'), size)
RED, GOLD, INK = (200, 16, 46), (244, 197, 66), (20, 20, 20)

def cover(im, w, h, fx=.5, fy=.5):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = round((im.width - w) * fx), round((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))

def shade(im, frac=.62, alpha=235):
    w, h = im.size
    g = Image.new('L', (w, 1))
    for x in range(w):
        t = x / (w * frac)
        g.putpixel((x, 0), int(alpha * max(0, 1 - t) ** 1.1))
    g = g.resize((w, h))
    dark = Image.new('RGBA', (w, h), (14, 12, 12, 255))
    out = im.convert('RGBA'); out.paste(dark, (0, 0), g)
    return out

def pill(d, xy, text, f, bg=RED, fg=(255, 255, 255), pad=(1.0, .55)):
    x, y = xy; bw = d.textlength(text, font=f); h = f.size
    w2, h2 = bw + h * pad[0] * 2, h + h * pad[1] * 2
    d.rounded_rectangle((x, y, x + w2, y + h2), radius=h2 / 2, fill=bg)
    d.text((x + h * pad[0], y + h * pad[1] - h * .08), text, font=f, fill=fg)
    return y + h2

def banner(w, h, photo, lines, sub, cta, k=3, fx=.62):
    W, H = w * k, h * k
    im = shade(cover(Image.open(photo).convert('RGB'), W, H, fx=fx))
    d = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(M, 'logo.png')).convert('RGBA')
    lh = int(H * .17); logo = logo.resize((int(logo.width * lh / logo.height), lh), Image.LANCZOS)
    x0 = int(W * .06); y = int(H * .1)
    im.alpha_composite(logo, (x0, y)); y += lh + int(H * .07)
    for txt, col, sz in lines:
        f = font('antonio', 700, int(H * sz)); d.text((x0, y), txt.upper(), font=f, fill=col); y += int(f.size * 1.08)
    if sub:
        f = font('manrope', 600, int(H * .062)); y += int(H * .02); d.text((x0, y), sub, font=f, fill=(225, 220, 210)); y += int(f.size * 1.6)
    if cta:
        pill(d, (x0, y + int(H * .01)), cta, font('manrope', 800, int(H * .058)))
    return im.resize((w, h), Image.LANCZOS)

def rounded(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=r, fill=255)
    out = im.convert('RGBA'); out.putalpha(m); return out

# 1) Confirmação de Pedido: banner na parte de cima do pop-up (876x507), faixa branca original embaixo
pop = Image.open(os.path.join(D, 'popup.webp')).convert('RGBA')
bn = banner(876, 507, os.path.join(M, 'foto-confirmacao.jpg'),
            [('Pedido feito!', (255, 255, 255), .13), ('Que tal uma 0,0?', GOLD, .13)],
            'Sem álcool, com sabor', 'Peça a sua', fx=.85)
alpha = pop.getchannel('A').crop((0, 0, 876, 507))
top = bn.convert('RGBA'); top.putalpha(alpha)
pop.paste(top, (0, 0)); pop.save(os.path.join(D, 'out-popup.webp'), quality=88)

# 2) Minha Conta: banner no lugar do card (479,50)-(683,164)
mc = Image.open(os.path.join(D, 'mcscr.webp')).convert('RGBA')
cb = banner(204, 114, os.path.join(M, 'foto-especial.jpg'),
            [('Concorra a uma', (255, 255, 255), .12), ('experiência', GOLD, .12)],
            None, 'Jogue a Tirada 0,0', k=4, fx=.9)
mc.paste((255, 255, 255, 255), (476, 47, 687, 167))
mc.alpha_composite(rounded(cb, 6), (479, 50)); mc.save(os.path.join(D, 'out-mcscr.webp'), quality=90)

# 3) Página Especial: aba Estrella no menu + tela de abertura do jogo
es = Image.open(os.path.join(D, 'especial.webp')).convert('RGBA')
shot = Image.open(os.path.join(D, 'game-intro.png')).convert('RGBA')
es.paste(cover(shot, 606, 353), (230, 128))
d = ImageDraw.Draw(es)
d.rectangle((143, 182, 216, 246), fill=(47, 25, 15, 255))
d.rounded_rectangle((147, 186, 212, 242), radius=6, fill=(47, 25, 15, 255), outline=(247, 132, 31, 255), width=2)
lg = Image.open(os.path.join(M, 'logo.png')).convert('RGBA'); lg = lg.resize((40, int(lg.height * 40 / lg.width)), Image.LANCZOS)
es.alpha_composite(lg, (180 - 20, 192))
f = font('manrope', 600, 9); t = 'Estrella'; d.text((180 - d.textlength(t, font=f) / 2, 225), t, font=f, fill=(255, 255, 255))
es.save(os.path.join(D, 'out-especial.webp'), quality=90)
print('ok')

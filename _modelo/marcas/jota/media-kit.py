"""Personaliza o media kit Goomer Ads para a Jota (agência), com o Mercado Livre como cliente de exemplo.
Uso: python3 _modelo/marcas/jota/media-kit.py <modelo.html> <saida.html>
Pré-requisitos: logos (Jota, Mercado Livre) e jota/ativacoes/index.html (build-seletor.py) + seletor-abertura.png."""
import sys, os, re, io, base64
from PIL import Image, ImageDraw, ImageFont, ImageOps

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(D, '..', '..', '..'))
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def webp(im, q=86):
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q); return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()

def img_by_alt(alt_start):
    m = re.search(r'<img[^>]*?src="(data:image/[a-z]+;base64,[^"]+)"[^>]*?alt="' + re.escape(alt_start), s) or \
        re.search(r'<img[^>]*?alt="' + re.escape(alt_start) + r'[^>]*?src="(data:image/[a-z]+;base64,[^"]+)"', s)
    assert m, alt_start
    return m.group(1)

def load_uri(u):
    return Image.open(io.BytesIO(base64.b64decode(u.split(',', 1)[1]))).convert('RGBA')

def trim(im):
    bb = im.getchannel('A').getbbox() if im.mode == 'RGBA' else None
    return im.crop(bb) if bb else im

def font(sz):
    for p in ('/root/.fonts/Manrope-ExtraBold.ttf', '/root/.fonts/manrope-latin-800-normal.ttf',
              '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'):
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()

ml = trim(Image.open(os.path.join(D, 'mercado-livre.png')).convert('RGBA'))
claro = os.path.join(D, 'logo-claro.png')
jota = trim(Image.open(claro if os.path.exists(claro) else os.path.join(D, 'logo.png')).convert('RGBA'))

# 1. título e logo da Jota no topo
s = re.sub(r'<title>[^<]*</title>', '<title>Goomer Ads para Jota</title>', s, 1)
jt = jota.copy(); jt.thumbnail((680, 64), Image.LANCZOS)
s = s.replace('<span class="kit">Media Kit 2026</span>', f'<span class="kit logo"><img src="{webp(jt, 92)}" alt="Jota"></span>', 1)

# 2. Confirmação de Pedido: banner do Mercado Livre (ilustrativo) na área de cima do pop-up 876x688
def banner(w, h, titulo, sub):
    bn = Image.new('RGBA', (w, h), '#FFE600')
    foto = Image.open(os.path.join(D, 'foto-confirmacao.jpg')).convert('RGBA')
    foto = ImageOps.fit(foto, (int(w * .48), h)); bn.paste(foto, (w - foto.width, 0))
    dr = ImageDraw.Draw(bn)
    lg = ml.copy(); lg.thumbnail((int(w * .36), int(h * .2)), Image.LANCZOS); bn.alpha_composite(lg, (int(w * .05), int(h * .12)))
    y = int(h * .42)
    for ln in titulo:
        dr.text((int(w * .05), y), ln, font=font(int(h * .1)), fill='#2D3277'); y += int(h * .12)
    dr.rounded_rectangle((int(w * .05), y + 12, int(w * .05) + int(w * .3), y + 12 + int(h * .13)), radius=int(h * .065), fill='#3483FA')
    dr.text((int(w * .05) + 22, y + 12 + int(h * .025)), sub, font=font(int(h * .065)), fill='#FFFFFF')
    return bn

u = img_by_alt('Pop-up de pedido enviado com banner do anunciante')
pop = load_uri(u)
bh = round(pop.height * .62)
bn = banner(pop.width, bh, ['Pedido feito!', 'Ganhe R$ 20 no app'], 'Jogue e ganhe')
mask = Image.new('L', bn.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, bn.width, bn.height + 40), radius=28, fill=255)
pop.paste(bn, (0, 0), mask)
s = s.replace(u, webp(pop), 1)

# 3. Página Especial: aba Mercado Livre e tela de abertura do jogo
u = img_by_alt('Tablet Goomer com a aba PicPay selecionada')
tab = load_uri(u)
dr = ImageDraw.Draw(tab)
dr.rectangle((148, 187, 211, 241), fill='#2F190F')
ic = jota.copy(); ic.thumbnail((54, 26), Image.LANCZOS); tab.alpha_composite(ic, (180 - ic.width // 2, 192 + (26 - ic.height) // 2))
f8 = font(8); t = 'Jota'; tw = dr.textlength(t, font=f8); dr.text((180 - tw / 2, 225), t, font=f8, fill='#FFFFFF')
shot = os.path.join(D, 'seletor-abertura.png')
if os.path.exists(shot):
    sc = Image.open(shot).convert('RGBA').resize((836 - 230, 481 - 128), Image.LANCZOS); tab.paste(sc, (230, 128))
s = s.replace(u, webp(tab), 1)
s = s.replace('alt="Tablet Goomer com a aba PicPay selecionada e a página especial do jogo"',
              'alt="Tablet Goomer com a aba Mercado Livre selecionada e a página especial do jogo"')
game = open(os.path.join(ROOT, 'jota', 'ativacoes', 'index.html'), 'rb').read()
s = re.sub(r'(<script type="text/plain" id="game-picpay">)[^<]*(</script>)', lambda m: m.group(1) + base64.b64encode(game).decode() + m.group(2), s, 1)
# o seletor não tem botão a clicar sozinho: desliga o clique automático
s = s.replace("find(x=>/bora jogar/i.test(x.textContent));if(b)b.click();else setTimeout(go,150)", "find(x=>/bora jogar/i.test(x.textContent));if(b)b.click()")
s = s.replace('Toque em Bora jogar e teste a ativação do PicPay.', 'Toque em Bora jogar e teste as ativações de Mercado Livre, Life360 e Sicredi.')

# 4. assinatura: só João; assunto do e-mail
s = re.sub(r'\s*<div class="sig" data-sig="ana">.*?(?=\s*<div class="sig" data-sig="joao">)', '', s, 1, re.S)
s = s.replace('?subject=Goomer%20Ads"', '?subject=Goomer%20Ads%20%C3%97%20Jota"')

open(out, 'w', encoding='utf-8').write(s)
print('ok', out, len(s) // 1024, 'KB')

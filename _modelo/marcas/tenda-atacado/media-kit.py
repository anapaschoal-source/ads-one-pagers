"""Personaliza o media kit Goomer Ads para o Tenda Atacado (campanha de Verão).
Uso (na raiz do repo): python3 _modelo/marcas/tenda-atacado/media-kit.py <modelo-aberto.html> <saida-aberta.html>
Pré-requisitos: criativos.py e build-jogo.py já rodados (banner-confirmacao.png, banner-b2b.png, tenda-atacado/jogo/index.html).
Troca: título, logo do topo, Confirmação de Pedido, Banner B2B, Página Especial (jogo Carrinho de Verão),
logo da Dellys na grade de anunciantes, assinatura só da Ana. Cases reais (Wickbold, BTG, Coca-Cola Zero) ficam.
A foto da mesa é trocada depois com _modelo/media-kit/tela_tablet.py."""
import sys, os, re, io, base64, glob
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(D, '..', '..', '..'))
JOGO = os.path.join(ROOT, 'tenda-atacado', 'jogo', 'index.html')
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()


def webp(im, q=88):
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q); return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()


def png(im):
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True); return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


def load_uri(u):
    return Image.open(io.BytesIO(base64.b64decode(u.split(',', 1)[1]))).convert('RGBA')


def img_src(alt_start):
    m = re.search(r'<img[^>]*?src="(data:image/[a-z]+;base64,[^"]+)"[^>]*?alt="' + re.escape(alt_start), s)
    assert m, alt_start
    return m.group(1)


def font(sz, w=600):
    for p in glob.glob(os.path.expanduser(f'~/.fonts/manrope-latin-{w}-normal.ttf')) + ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']:
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def rounded(im, r, top_only=False):
    mk = Image.new('L', im.size, 0)
    ImageDraw.Draw(mk).rounded_rectangle((0, 0, im.width - 1, im.height - 1 + (r if top_only else 0)), radius=r, fill=255)
    return mk


def abertura(path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1280, 'height': 800})
        pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith(('file:', 'data:')) else r.abort())
        pg.goto('file://' + path); pg.wait_for_timeout(1500)
        b = pg.screenshot(); br.close()
    return Image.open(io.BytesIO(b)).convert('RGBA')


logo = Image.open(os.path.join(D, 'logo.png')).convert('RGBA')

# 1. título e logo no topo (o logo é uma caixa azul própria, legível no fundo escuro)
s = re.sub(r'<title>[^<]*</title>', '<title>Goomer Ads para Tenda Atacado</title>', s, count=1)
lt = logo.copy(); lt.thumbnail((300, 120), Image.LANCZOS)
assert '<span class="kit">Media Kit 2026</span>' in s
s = s.replace('<span class="kit">Media Kit 2026</span>', f'<span class="kit logo"><img src="{png(lt)}" alt="Tenda Atacado"></span>', 1)
s = s.replace('</head>', '<style>/*tenda-logo*/.brand .kit.logo img{height:30px!important}@media (max-width:760px){.brand .kit.logo img{height:24px!important}}</style></head>', 1)

# 2. Confirmação de Pedido: banner de verão na área de cima do pop-up, faixa branca mantida
u = img_src('Pop-up de pedido enviado com banner do anunciante'); pop = load_uri(u)
bh = next(y for y in range(250, pop.height) if all(min(pop.getpixel((x, y))[:3]) > 245 for x in (50, 438, 820)))
bn = Image.open(os.path.join(D, 'banner-confirmacao.png')).convert('RGBA')
bn = bn.resize((pop.width, round(bn.height * pop.width / bn.width)), Image.LANCZOS)
top = (bn.height - bh) // 2 if bn.height > bh else 0
bn = bn.crop((0, top, pop.width, top + bh)) if bn.height >= bh else bn.resize((pop.width, bh), Image.LANCZOS)
pop.paste(bn, (0, 0), rounded(bn, 28, top_only=True))
s = s.replace(u, webp(pop), 1)

# 3. Banner Home · Painel B2B
u = img_src('Painel Goomer do restaurante com banner'); pn = load_uri(u)
b2 = Image.open(os.path.join(D, 'banner-b2b.png')).convert('RGBA').resize((1340 - 502, 265 - 153), Image.LANCZOS)
pn.paste(b2, (502, 153), rounded(b2, 10))
s = s.replace(u, webp(pn), 1)
s = re.sub(r'alt="Painel Goomer do restaurante com banner [^"]*"', 'alt="Painel Goomer do restaurante com banner de verão do Tenda Atacado"', s)

# 4. Página Especial: aba Tenda no cardápio + tela de abertura do jogo; jogo embutido no lugar do PicPay
u = img_src('Tablet Goomer com a aba PicPay selecionada'); tab = load_uri(u); dr = ImageDraw.Draw(tab)
dr.rectangle((148, 187, 211, 241), fill='#2F190F')
ic = logo.copy(); ic.thumbnail((40, 26), Image.LANCZOS); tab.alpha_composite(ic, (180 - ic.width // 2, 192 + (26 - ic.height) // 2))
f8 = font(8); tw = dr.textlength('Tenda', font=f8); dr.text((180 - tw / 2, 226), 'Tenda', font=f8, fill='#FFFFFF')
tab.paste(abertura(JOGO).resize((836 - 230, 481 - 128), Image.LANCZOS), (230, 128))
s = s.replace(u, webp(tab), 1)
s = s.replace('alt="Tablet Goomer com a aba PicPay selecionada e a página especial do jogo"',
              'alt="Tablet Goomer com a aba Tenda selecionada e a página especial do jogo Carrinho de Verão"')
game = base64.b64encode(open(JOGO, 'rb').read()).decode()
s, n = re.subn(r'(<script type="text/plain" id="game-picpay">)[^<]*(</script>)', lambda m: m.group(1) + game + m.group(2), s, count=1)
assert n == 1
s = s.replace('/bora jogar/i.test(x.textContent)', '/bora encher/i.test(x.textContent)')
s = s.replace('Jogar o jogo PicPay', 'Jogar o Carrinho de Verão').replace('title="Jogo PicPay"', 'title="Jogo Carrinho de Verão"')
s = s.replace('Toque em Bora jogar e teste a ativação do PicPay.', 'Toque em Bora encher e teste a ativação do Tenda Atacado: Carrinho de Verão.')

# 5. Dellys na grade de anunciantes (só neste kit)
dl = Image.open(os.path.join(D, 'cli-dellys.png')).convert('RGBA'); dl.thumbnail((200, 120), Image.LANCZOS)
s, n = re.subn(r'(<div class="logos">.*?<img src="[^"]+" alt="Cyrela"></div>)', lambda m: m.group(1) + f'<div><img src="{png(dl)}" alt="Dellys" style="max-height:52px"></div>', s, count=1, flags=re.S)
assert n == 1

# 6. assinatura: só Ana; assunto do e-mail
s, n = re.subn(r'\s*<div class="sig" data-sig="joao">.*?</div>\s*</div>\s*</div>(?=\s*</div>\s*<p class="note">)', '', s, count=1, flags=re.S)
assert n == 1, 'assinatura do João não encontrada'
s = s.replace('?subject=Goomer%20Ads"', '?subject=Goomer%20Ads%20%C3%97%20Tenda%20Atacado"')

open(out, 'w', encoding='utf-8').write(s)
print('ok:', out, len(s) // 1024, 'KB')

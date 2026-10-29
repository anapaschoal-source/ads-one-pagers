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
    foto = ImageOps.fit(foto, (int(w * .4), h)); bn.paste(foto, (w - foto.width, 0))
    dr = ImageDraw.Draw(bn)
    lg = ml.copy(); lg.thumbnail((int(w * .36), int(h * .2)), Image.LANCZOS); bn.alpha_composite(lg, (int(w * .05), int(h * .2)))
    y = int(h * .46)
    for ln in titulo:
        dr.text((int(w * .05), y), ln, font=font(int(h * .085)), fill='#2D3277'); y += int(h * .105)
    dr.rounded_rectangle((int(w * .05), y + 12, int(w * .05) + int(w * .3), y + 12 + int(h * .13)), radius=int(h * .065), fill='#3483FA')
    dr.text((int(w * .05) + 22, y + 12 + int(h * .025)), sub, font=font(int(h * .065)), fill='#FFFFFF')
    return bn

u = img_by_alt('Pop-up de pedido enviado com banner do anunciante')
pop = load_uri(u)
bh = next(y for y in range(250, pop.height) if all(min(pop.getpixel((x, y))[:3]) > 245 for x in (50, 438, 820)))  # início da faixa branca
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
game = open(os.path.join(ROOT, 'jota-ud03yuez', 'ativacoes', 'index.html'), 'rb').read()
s = re.sub(r'(<script type="text/plain" id="game-picpay">)[^<]*(</script>)', lambda m: m.group(1) + base64.b64encode(game).decode() + m.group(2), s, 1)
# o seletor não tem botão a clicar sozinho: desliga o clique automático
s = s.replace("find(x=>/bora jogar/i.test(x.textContent));if(b)b.click();else setTimeout(go,150)", "find(x=>/bora jogar/i.test(x.textContent));if(b)b.click()")
s = s.replace('Jogar o jogo PicPay', 'Testar as ativações das marcas da Jota')
s = s.replace('Toque em Bora jogar e teste a ativação do PicPay.', 'Toque em Bora jogar e teste as ativações de Mercado Livre, Life360 e Sicredi.')

# 4. assinatura: só João; assunto do e-mail
s = re.sub(r'\s*<div class="sig" data-sig="ana">.*?(?=\s*<div class="sig" data-sig="joao">)', '', s, 1, re.S)
s = s.replace('?subject=Goomer%20Ads"', '?subject=Goomer%20Ads%20%C3%97%20Jota"')

# 5. sem B2B: tira o seletor B2C/B2B do topo (o kit abre e fica em B2C)
s, nb = re.subn(r'\s*<div class="modebar seg2 intop" id="fMode".*?</div>', '', s, count=1, flags=re.S)
assert nb == 1

# 6. Tela de Início: vídeo ilustrativo da Life360 (deixa de ser case real)
vw = 'data:video/webm;base64,' + base64.b64encode(open(os.path.join(D, 'life360-inicio.webm'), 'rb').read()).decode()
vm = 'data:video/mp4;base64,' + base64.b64encode(open(os.path.join(D, 'life360-inicio.mp4'), 'rb').read()).decode()
vi = s.index('<video class="tv"'); ve = s.index('</video>', vi)
blk = s[vi:ve]
blk, nv = re.subn(r'<source src="data:[^"]+" type="video/webm">', lambda m: f'<source src="{vw}" type="video/webm">', blk, count=1)
blk, nm = re.subn(r'<source src="data:[^"]+" type="video/mp4">', lambda m: f'<source src="{vm}" type="video/mp4">', blk, count=1)
s = s[:vi] + blk + s[ve:]
assert nv == nm == 1
s = s.replace('<div class="scr real case vreal">', '<div class="scr real vreal">', 1)

# 7. Minha Conta: banner Sicredi (deixa de ser case real)
u = re.search(r'<img class="mcscr" src="(data:image/[a-z]+;base64,[^"]+)"', s).group(1)
mc = load_uri(u)
bw, bh2 = 204, 115
sb = Image.new('RGBA', (bw * 4, bh2 * 4), '#0F6A2D'); d2 = ImageDraw.Draw(sb)
d2.rectangle((0, 320, bw * 4, bh2 * 4), fill='#FFFFFF')
lg = Image.open(os.path.join(D, 'sicredi.png')).convert('RGBA'); lg.thumbnail((330, 100), Image.LANCZOS)
sb.alpha_composite(lg, (36, 320 + (140 - lg.height) // 2))
d2.text((36, 178), 'Ganhe a 1ª anuidade', font=font(46), fill='#FFFFFF')
d2.text((36, 234), 'grátis no cartão', font=font(46), fill='#FFFFFF')
d2.rounded_rectangle((440, 345, 790, 435), radius=45, fill='#40B93C')
d2.text((478, 366), 'Gire a roleta', font=font(40), fill='#FFFFFF')
sb = sb.resize((bw, bh2), Image.LANCZOS)
m2 = Image.new('L', sb.size, 0); ImageDraw.Draw(m2).rounded_rectangle((0, 0, bw - 1, bh2 - 1), radius=8, fill=255)
mc.paste(sb, (479, 49), m2)
s = s.replace(u, webp(mc), 1)
s = s.replace('alt="Tela Minha Conta com a conta da mesa e o banner do anunciante"', 'alt="Tela Minha Conta com a conta da mesa e o banner do Sicredi"', 1)
i = s.index('<img class="mcscr"'); j = s.rfind('<div class="scr real case">', 0, i)
s = s[:j] + '<div class="scr real">' + s[j + len('<div class="scr real case">'):]

# 8. Mapa fixo: Brasil inteiro com os pontos e os números do modelo, sem filtros nem interação (sem culinária)
i = s.index('<h3>Culinária</h3>'); j = s.rfind('<div style="display:grid;gap:8px">', 0, i)
s = s[:j] + '<div style="display:grid;gap:8px" hidden>' + s[j + len('<div style="display:grid;gap:8px">'):]
s = s.replace('<div><b>Tipo de culinária</b><p>', '<div hidden><b>Tipo de culinária</b><p>')
MAPCSS = """<style>/*jota-mapa*/
#mapa .filters,#mapa #hint,#mapa .zoomctl,#mapa .pin,#mapa .tip,#mapa #fxBtn{display:none!important}
#mapa #svg,#mapa #stage{pointer-events:none}
</style>"""
MAPJS = ""
s = s.replace('</body>', MAPCSS + MAPJS + '</body>', 1) if '</body>' in s else s + MAPCSS + MAPJS

open(out, 'w', encoding='utf-8').write(s)
print('ok', out, len(s) // 1024, 'KB')

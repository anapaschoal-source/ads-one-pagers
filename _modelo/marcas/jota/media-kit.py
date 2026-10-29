"""Personaliza o media kit Goomer Ads para a Jota (agência), com seletor de marcas: Mercado Livre, Life360 e Sicredi.
Uso: python3 _modelo/marcas/jota/media-kit.py <modelo.html> <saida.html>
Pré-requisitos: logos, ativações em jota-ud03yuez/{jogo,quiz,roleta} e vídeos de video-marcas.py."""
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
jt = jota.copy(); jt.thumbnail((900, 120), Image.LANCZOS)
s = s.replace('<span class="kit">Media Kit 2026</span>', f'<span class="kit logo"><img src="{webp(jt, 92)}" alt="Jota"></span>', 1)
s = s.replace('</head>', '<style>/*jota-logo*/.brand .kit.logo img{height:34px!important;max-width:240px!important}.brand .kit.logo{padding-top:0!important;padding-bottom:0!important}@media (max-width:760px){.brand .kit.logo img{height:24px!important}}</style></head>', 1) if '</head>' in s else s

# foto da mesa: Tela de Início do Mercado Livre no tablet
import subprocess, tempfile
mm = re.search(r'(<figure class="mesa-foto" id="mesaFoto"><img src=")(data:image/[a-z]+;base64,[^"]+)(")', s)
t0 = tempfile.mktemp(suffix='.png'); t1 = tempfile.mktemp(suffix='.webp')
load_uri(mm.group(2)).convert('RGB').save(t0)
subprocess.run([sys.executable, os.path.join(D, 'mesa-foto.py'), t0, t1], check=True, stdout=subprocess.DEVNULL)
s = s.replace(mm.group(0), mm.group(1) + 'data:image/webp;base64,' + base64.b64encode(open(t1, 'rb').read()).decode() + mm.group(3), 1)
s = s.replace('alt="Tablet Goomer na mesa de um restaurante, com o cliente comendo petiscos"', 'alt="Tablet Goomer na mesa de um restaurante exibindo a Tela de Início do Mercado Livre"', 1)

# 2. Seletor de marcas (como no kit da AlmapBBDO): Mercado Livre, Life360 e Sicredi, cada uma com peça em
#    Tela de Início (vídeo), Confirmação de Pedido, Minha Conta e Página Especial (a ativação de cada marca)
SLUG = 'jota-ud03yuez'
def logo_img(nome, branco=False):
    i = trim(Image.open(os.path.join(D, nome)).convert('RGBA'))
    if branco: i.putdata([(255, 255, 255, a) for *_, a in i.get_flattened_data()])
    return i

MARCAS = [
    dict(id='ml', n='Mercado Livre', c='#FFE600', logo='mercado-livre.png', branco=False, jogo='jogo', g='Entrega Relâmpago',
         bg='#FFE600', ink='#2D3277', cta_bg='#3483FA', cta_ink='#FFFFFF', foto='foto-confirmacao.jpg',
         conf=['Pedido feito!', 'Ganhe R$ 20 no app'], cta='Jogue e ganhe', conta=['Cupom de R$ 20', 'no app'], cta2='Jogue agora'),
    dict(id='l360', n='Life360', c='#7A76EC', logo='life360.png', branco=True, jogo='quiz', g='Que família é a sua?',
         bg='#7A76EC', ink='#FFFFFF', cta_bg='#FFFFFF', cta_ink='#5450C9', foto='foto-life360-2.jpg',
         conf=['Sua família', 'no mesmo mapa'], cta='Faça o quiz', conta=['Família conectada', 'e segura'], cta2='Faça o quiz'),
    dict(id='sic', n='Sicredi', c='#40B93C', logo='sicredi.png', branco=True, jogo='roleta', g='Gire e coopere',
         bg='#0F6A2D', ink='#FFFFFF', cta_bg='#40B93C', cta_ink='#FFFFFF', foto='foto-sicredi.jpg',
         conf=['Ganhe a 1ª anuidade', 'grátis no cartão'], cta='Gire a roleta', conta=['Ganhe a 1ª anuidade', 'grátis no cartão'], cta2='Gire a roleta'),
]

def banner_conf(m, w, h):
    bn = Image.new('RGBA', (w, h), m['bg'])
    foto = Image.open(os.path.join(D, m['foto'])).convert('RGBA')
    foto = ImageOps.fit(foto, (int(w * .4), h)); bn.paste(foto, (w - foto.width, 0))
    dr = ImageDraw.Draw(bn)
    lg = logo_img(m['logo'], m['branco']); lg.thumbnail((int(w * .36), int(h * .2)), Image.LANCZOS); bn.alpha_composite(lg, (int(w * .05), int(h * .2)))
    y = int(h * .46)
    for ln in m['conf']:
        dr.text((int(w * .05), y), ln, font=font(int(h * .085)), fill=m['ink']); y += int(h * .105)
    fw = int(dr.textlength(m['cta'], font=font(int(h * .065)))) + 44
    dr.rounded_rectangle((int(w * .05), y + 12, int(w * .05) + fw, y + 12 + int(h * .13)), radius=int(h * .065), fill=m['cta_bg'])
    dr.text((int(w * .05) + 22, y + 12 + int(h * .025)), m['cta'], font=font(int(h * .065)), fill=m['cta_ink'])
    return bn

def banner_conta(m):
    bw, bh2 = 204, 115
    sb = Image.new('RGBA', (bw * 4, bh2 * 4), m['bg']); d2 = ImageDraw.Draw(sb)
    d2.rectangle((0, 320, bw * 4, bh2 * 4), fill='#FFFFFF')
    lg = logo_img(m['logo']); lg.thumbnail((330, 100), Image.LANCZOS)
    sb.alpha_composite(lg, (36, 320 + (140 - lg.height) // 2))
    d2.text((36, 178), m['conta'][0], font=font(46), fill=m['ink'])
    d2.text((36, 234), m['conta'][1], font=font(46), fill=m['ink'])
    cb = m['cta_bg'] if m['cta_bg'] != '#FFFFFF' else m['bg']
    tw = int(d2.textlength(m['cta2'], font=font(40))); x0 = 790 - tw - 68
    d2.rounded_rectangle((x0, 345, 790, 435), radius=45, fill=cb)
    d2.text((x0 + 34, 366), m['cta2'], font=font(40), fill='#FFFFFF')
    sb = sb.resize((bw, bh2), Image.LANCZOS)
    mk = Image.new('L', sb.size, 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, bw - 1, bh2 - 1), radius=8, fill=255)
    return sb, mk

def abertura(html_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1280, 'height': 800})
        pg.goto('file://' + html_path); pg.wait_for_timeout(900)
        png = pg.screenshot(); br.close()
    return Image.open(io.BytesIO(png)).convert('RGBA')

u_pop = img_by_alt('Pop-up de pedido enviado com banner do anunciante'); pop0 = load_uri(u_pop)
bh = next(y for y in range(250, pop0.height) if all(min(pop0.getpixel((x, y))[:3]) > 245 for x in (50, 438, 820)))  # início da faixa branca
u_tab = img_by_alt('Tablet Goomer com a aba PicPay selecionada'); tab0 = load_uri(u_tab)
u_mc = re.search(r'<img class="mcscr" src="(data:image/[a-z]+;base64,[^"]+)"', s).group(1); mc0 = load_uri(u_mc)
DATA = []
for m in MARCAS:
    pop = pop0.copy(); bn = banner_conf(m, pop.width, bh)
    mask = Image.new('L', bn.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, bn.width, bn.height + 40), radius=28, fill=255)
    pop.paste(bn, (0, 0), mask)
    tab = tab0.copy(); dr = ImageDraw.Draw(tab)
    dr.rectangle((148, 187, 211, 241), fill='#2F190F')
    ic = logo_img(m['logo'], m['branco']); ic.thumbnail((54, 26), Image.LANCZOS); tab.alpha_composite(ic, (180 - ic.width // 2, 192 + (26 - ic.height) // 2))
    f8 = font(8); tw = dr.textlength(m['n'], font=f8); dr.text((180 - tw / 2, 225), m['n'], font=f8, fill='#FFFFFF')
    gp = os.path.join(ROOT, SLUG, m['jogo'], 'index.html')
    tab.paste(abertura(gp).resize((836 - 230, 481 - 128), Image.LANCZOS), (230, 128))
    mc = mc0.copy(); sb, mk = banner_conta(m); mc.paste(sb, (479, 49), mk)
    vid = lambda ext: f'data:video/{ext};base64,' + base64.b64encode(open(os.path.join(D, f"{m['id']}-inicio.{ext}"), 'rb').read()).decode()
    DATA.append(dict(id=m['id'], n=m['n'], c=m['c'], g=m['g'], conf=webp(pop), esp=webp(tab), conta=webp(mc), mp4=vid('mp4'), webm=vid('webm'),
                     game=base64.b64encode(open(gp, 'rb').read()).decode()))
d0 = DATA[0]
s = s.replace(u_pop, d0['conf'], 1); s = s.replace(u_tab, d0['esp'], 1); s = s.replace(u_mc, d0['conta'], 1)
s = s.replace('alt="Tablet Goomer com a aba PicPay selecionada e a página especial do jogo"', 'alt="Tablet Goomer com a aba Mercado Livre selecionada e a página especial do jogo"')
s = s.replace('alt="Tela Minha Conta com a conta da mesa e o banner do anunciante"', 'alt="Tela Minha Conta com a conta da mesa e o banner do Mercado Livre"', 1)
s = re.sub(r'(<script type="text/plain" id="game-picpay">)[^<]*(</script>)', lambda mm: mm.group(1) + d0['game'] + mm.group(2), s, count=1)
s = s.replace("find(x=>/bora jogar/i.test(x.textContent));if(b)b.click();else setTimeout(go,150)", "find(x=>/bora jogar/i.test(x.textContent));if(b)b.click()")
s = s.replace('Jogar o jogo PicPay', 'Testar a ativação')
s = s.replace('Toque em Bora jogar e teste a ativação do PicPay.', 'Toque em Bora jogar e teste a ativação Mercado Livre: Entrega Relâmpago.')
BSEL = ('<div class="bsel" data-bsel><div class="bl"><b>Ver exemplos para</b><small>Peças ilustrativas criadas para a Jota</small></div>'
        '<div class="bc" role="group" aria-label="Escolha a marca"></div></div>')
s = s.replace('<div class="fcards" id="fcards"></div>', BSEL + '<div class="fcards" id="fcards"></div>', 1)
s = s.replace('<div class="fx-info" id="fxInfo"></div>', BSEL + '<div class="fx-info" id="fxInfo"></div>', 1)
import json
BJSON = json.dumps(DATA, ensure_ascii=False).replace('</', '<\\/')
BJS = """<script type="application/json" id="jota-brands">""" + BJSON + """</script>
<script>/*jota-marcas*/(function(){
var JB=JSON.parse(document.getElementById('jota-brands').textContent),cur=JB[0].id;
function B(){return JB.find(function(x){return x.id===cur})}
function esc2(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function apply(root){if(!root)return;var b=B();
 root.querySelectorAll('img[alt^="Pop-up de pedido"]').forEach(function(im){im.src=b.conf});
 root.querySelectorAll('img[alt^="Tablet Goomer com a aba"]').forEach(function(im){im.src=b.esp;im.alt='Tablet Goomer com a aba '+b.n+' selecionada e a página especial do jogo'});
 root.querySelectorAll('img.mcscr').forEach(function(im){im.src=b.conta;im.alt='Tela Minha Conta com a conta da mesa e o banner do '+b.n});
 root.querySelectorAll('video.tv').forEach(function(v){if(v.dataset.b===b.id)return;v.dataset.b=b.id;
  v.innerHTML='<source src="'+b.webm+'" type="video/webm"><source src="'+b.mp4+'" type="video/mp4">';v.muted=true;v.setAttribute('muted','');
  v.setAttribute('aria-label','Vídeo de 10 segundos de '+b.n+' na Tela de Início');
  try{v.load();var bx=v.closest('.tvbox');if(bx&&bx.classList.contains('ad')){var p=v.play();if(p)p.catch(function(){})}}catch(_){}})}
window.gameHTML=function(){var b=B();return new TextDecoder().decode(Uint8Array.from(atob(b.game),function(c){return c.charCodeAt(0)}))};
window.brandDesc=function(f){var b=B();return f.id==='especial'?f.d.replace(/Toque em Bora jogar.*$/,'Toque em Bora jogar e teste a ativação '+b.n+': '+b.g+(/[.?!]$/.test(b.g)?'':'.')):f.d};
var stage=document.getElementById('fxStage');if(stage)new MutationObserver(function(){apply(stage)}).observe(stage,{childList:true});
function set(id){cur=id;document.querySelectorAll('[data-bsel] .chip').forEach(function(c){c.setAttribute('aria-pressed',c.dataset.b===id?'true':'false')});
 apply(document.getElementById('fcards'));
 var fx=document.getElementById('fx');if(fx&&!fx.hidden){var g=stage.querySelector('.gameclose');if(g&&!g.hidden)g.click();try{fxPaused=true;showFx(fxI)}catch(_){}}}
document.querySelectorAll('[data-bsel] .bc').forEach(function(bc){
 bc.innerHTML=JB.map(function(b){return '<button type="button" class="chip" data-b="'+b.id+'" aria-pressed="'+(b.id===cur)+'"><span class="sw" style="background:'+b.c+'"></span>'+esc2(b.n)+'</button>'}).join('');
 bc.querySelectorAll('.chip').forEach(function(c){c.onclick=function(){set(c.dataset.b)}})});
apply(document.getElementById('fcards'));
})();</script>"""
s = s.replace('</body>', BJS + '</body>', 1) if '</body>' in s else s + BJS

# 4. assinatura: só João; assunto do e-mail
s = re.sub(r'\s*<div class="sig" data-sig="ana">.*?(?=\s*<div class="sig" data-sig="joao">)', '', s, 1, re.S)
s = s.replace('?subject=Goomer%20Ads"', '?subject=Goomer%20Ads%20%C3%97%20Jota"')

# 5. sem B2B: tira o seletor B2C/B2B do topo (o kit abre e fica em B2C)
s, nb = re.subn(r'\s*<div class="modebar seg2 intop" id="fMode".*?</div>', '', s, count=1, flags=re.S)
assert nb == 1

# 6. Tela de Início e Minha Conta: as peças da marca selecionada deixam de ser case real
vi = s.index('<video class="tv"'); ve = s.index('</video>', vi)
blk = s[vi:ve]
blk, nv = re.subn(r'<source src="data:[^"]+" type="video/webm">', lambda mm: f'<source src="{d0["webm"]}" type="video/webm">', blk, count=1)
blk, nm = re.subn(r'<source src="data:[^"]+" type="video/mp4">', lambda mm: f'<source src="{d0["mp4"]}" type="video/mp4">', blk, count=1)
s = s[:vi] + blk + s[ve:]
assert nv == nm == 1
s = s.replace('<div class="scr real case vreal">', '<div class="scr real vreal">', 1)
i = s.index('<img class="mcscr"'); j = s.rfind('<div class="scr real case">', 0, i)
s = s[:j] + '<div class="scr real">' + s[j + len('<div class="scr real case">'):]

# 8. Mapa fixo: Brasil inteiro com os pontos e os números do modelo, sem filtros nem interação (sem culinária)
i = s.index('<h3>Culinária</h3>'); j = s.rfind('<div style="display:grid;gap:8px">', 0, i)
s = s[:j] + '<div style="display:grid;gap:8px" hidden>' + s[j + len('<div style="display:grid;gap:8px">'):]
s = s.replace('<div><b>Tipo de culinária</b><p>', '<div hidden><b>Tipo de culinária</b><p>')
MAPCSS = """<style>/*jota-mapa*/
#mapa .filters,#mapa #hint,#mapa .zoomctl,#mapa .pin,#mapa .tip,#mapa #fxBtn{display:none!important}
#mapa #svg,#mapa #stage{pointer-events:none}
@media (min-width:981px){
 #mapa .story{left:max(var(--gutter),calc((100% - min(94vw,calc((100svh - 60px) * 2.15))) / 2));width:min(600px,44vw);top:clamp(20px,4vh,48px)}
 #mapa .story h1{font-size:clamp(44px,4.6vw,68px)}
 #mapa .story .lead{max-width:52ch}
 #mapa .story .kpis{grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 32px;max-width:520px}
 #mapa .story .kpi b{font-size:clamp(52px,5vw,76px)}
 #mapa .story .kpi span{font-size:15px}
 #mapa #svg,#mapa #dots{transform:translateX(clamp(120px,17vw,260px))}
}
</style>"""
MAPJS = ""
s = s.replace('</body>', MAPCSS + MAPJS + '</body>', 1) if '</body>' in s else s + MAPCSS + MAPJS

open(out, 'w', encoding='utf-8').write(s)
print('ok', out, len(s) // 1024, 'KB')

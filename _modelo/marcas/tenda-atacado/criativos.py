"""Monta os criativos do one-pager do Tenda Atacado a partir do KV de verão e do banner B2B da marca.
Gera: criativo-inicio.png (1280x720), banner-confirmacao.png (876x507), banner-conta.png (816x460),
banner-b2b.png (1500x200) e foto-especial.jpg.
Uso (na raiz do repo): python3 _modelo/marcas/tenda-atacado/criativos.py"""
import os, base64, glob, io
from PIL import Image
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__))


def uri(p):
    ext = p.rsplit('.', 1)[1].lower()
    return f'data:image/{"jpeg" if ext in ("jpg", "jpeg") else ext};base64,' + base64.b64encode(open(p, 'rb').read()).decode()


def font(w):
    p = glob.glob(os.path.expanduser(f'~/.fonts/baloo-2-latin-{w}-normal.ttf'))[0]
    return 'data:font/ttf;base64,' + base64.b64encode(open(p, 'rb').read()).decode()


# pessoas do banner B2B (recorte para a foto da Página Especial)
b = Image.open(os.path.join(D, 'banner-b2b-estoque.png')).convert('RGB')
b.crop((392, 104, 660, 406)).save(os.path.join(D, 'foto-especial.jpg'), quality=90)
ppl = io.BytesIO(); b.crop((380, 104, 700, 390)).save(ppl, 'PNG')
PPL = 'data:image/png;base64,' + base64.b64encode(ppl.getvalue()).decode()

VERAO, LOGO = uri(os.path.join(D, 'verao.png')), uri(os.path.join(D, 'logo.png'))
NAVY, RED = '#1B396E', '#EE2E24'
CSS = f"""@font-face{{font-family:B;src:url('{font(700)}');font-weight:700}}
@font-face{{font-family:B;src:url('{font(800)}');font-weight:800}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#000}}
.c{{position:relative;overflow:hidden;font-family:B,sans-serif;color:{NAVY};
background:radial-gradient(55% 75% at 18% 30%,#FFE15A 0%,rgba(255,225,90,0) 70%),radial-gradient(80% 90% at 100% 100%,#FF9A00 0%,rgba(255,154,0,0) 70%),linear-gradient(160deg,#FFC21A,#FFAE00)}}
.rays{{position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 18% 30%,rgba(255,255,255,.12) 0 6deg,rgba(255,255,255,0) 6deg 18deg)}}
.hl{{color:{RED}}}
h1{{font-weight:800;line-height:.98;letter-spacing:-.01em}}
.lg{{display:block;filter:drop-shadow(0 .3em .6em rgba(0,0,0,.18))}}
.sub{{font-weight:700}} .sub b{{font-weight:800}}
"""

PAGES = {
    'criativo-inicio.png': (1280, 720, f"""<div class="c" style="width:1280px;height:720px"><div class="rays"></div>
<img src="{VERAO}" style="position:absolute;left:58px;top:110px;width:560px">
<img class="lg" src="{LOGO}" style="position:absolute;left:250px;top:388px;width:178px">
<div style="position:absolute;left:660px;top:0;bottom:0;width:560px;display:flex;flex-direction:column;justify-content:center;gap:24px">
<h1 style="font-size:84px">Preço baixo<br>é a nossa<br><span class="hl">praia!</span></h1>
<div class="sub" style="font-size:34px;line-height:1.2">Ofertas especiais pra curtir<br>o verão com <b>preço baixo de verdade.</b></div></div></div>"""),
    'banner-confirmacao.png': (876, 507, f"""<div class="c" style="width:876px;height:507px"><div class="rays"></div>
<img src="{VERAO}" style="position:absolute;left:34px;top:60px;width:390px">
<img class="lg" src="{LOGO}" style="position:absolute;left:160px;top:262px;width:130px">
<div style="position:absolute;left:452px;top:0;bottom:0;width:396px;display:flex;flex-direction:column;justify-content:center;gap:18px">
<h1 style="font-size:56px">Ofertas<br>especiais de<br><span class="hl">verão</span></h1>
<div class="sub" style="font-size:26px;line-height:1.2">Pra curtir a estação com<br><b>preço baixo de verdade!</b></div></div></div>"""),
    'banner-conta.png': (816, 460, f"""<div class="c" style="width:816px;height:460px"><div class="rays"></div>
<img class="lg" src="{LOGO}" style="position:absolute;left:44px;top:46px;width:210px">
<img src="{VERAO}" style="position:absolute;left:40px;top:220px;width:330px">
<div style="position:absolute;left:400px;top:0;bottom:0;width:380px;display:flex;flex-direction:column;justify-content:center;gap:16px">
<h1 style="font-size:62px">Verão com<br>frete grátis</h1>
<div class="sub" style="font-size:30px">Cupom <span class="hl" style="font-weight:800;font-size:44px">FRETEZERO</span></div>
<div class="sub" style="font-size:24px">Na 1ª compra a partir de R$ 399</div></div></div>"""),
    'banner-b2b.png': (1500, 200, f"""<div class="c" style="width:1500px;height:200px"><div class="rays" style="background:repeating-conic-gradient(from 0deg at 12% 50%,rgba(255,255,255,.12) 0 6deg,rgba(255,255,255,0) 6deg 18deg)"></div>
<img src="{VERAO}" style="position:absolute;left:40px;top:20px;width:340px">
<img class="lg" src="{LOGO}" style="position:absolute;left:410px;top:38px;height:124px">
<div style="position:absolute;left:640px;right:40px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;gap:6px">
<h1 style="font-size:54px;line-height:1;white-space:nowrap">Abasteça seu negócio <span class="hl">pro verão</span></h1>
<div class="sub" style="font-size:30px">Estoque cheio com <b>preço baixo de verdade.</b></div></div></div>"""),
}

with sync_playwright() as p:
    br = p.chromium.launch()
    for nome, (w, h, body) in PAGES.items():
        pg = br.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.set_content(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>{body}')
        pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(D, nome), clip={'x': 0, 'y': 0, 'width': w, 'height': h})
        print('ok', nome)
    br.close()

"""Gera jota/ativacoes/index.html: tela 1280x800 para a Página Especial do media kit, com as 3 ativações
das marcas da Jota (Mercado Livre, Life360, Sicredi). Cada ativação abre embutida; volta ao seletor por
"Trocar ativação" ou após 60s sem toque.
Uso (na raiz do repo, depois de build-jogo.py e ativacao.py): python3 _modelo/marcas/jota/build-seletor.py"""
import os, re, io, base64, json
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(D, '..', '..', '..'))
ref = open(os.path.join(ROOT, '_modelo', 'ativacoes', 'roleta.html'), encoding='utf-8').read()
fonts = re.findall(r"src:url\('(data:font/woff2;base64,[^']+)'\)", ref)
gsvg = re.search(r'<svg class="goomer-logo".*?</svg>', ref, re.S).group(0)

def logo(nome, w=420):
    i = Image.open(os.path.join(D, nome)).convert('RGBA'); i = i.crop(i.getchannel('A').getbbox()); i.thumbnail((w, 160), Image.LANCZOS)
    b = io.BytesIO(); i.save(b, 'PNG', optimize=True); return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

A = [('Mercado Livre', 'mercado-livre.png', 'Jogo', 'Entrega Relâmpago', 'Entregue 10 pacotes em 20 segundos e ganhe cupom.', '#FFE600', 'jogo'),
     ('Life360', 'life360.png', 'Quiz', 'Que família é a sua?', 'Três perguntas e um QR para baixar o app.', '#E9E8FD', 'quiz'),
     ('Sicredi', 'sicredi.png', 'Roleta', 'Gire e coopere', 'Gire a roleta e ganhe um benefício na conta.', '#E2F4DD', 'roleta')]
html_of = {d: base64.b64encode(open(os.path.join(ROOT, 'jota', d, 'index.html'), 'rb').read()).decode() for *_, d in A}
cards = ''.join(
    f'<button class="c" data-k="{d}"><span class="lg" style="background:{bg}"><img src="{logo(lg)}" alt="{nome}"></span>'
    f'<span class="tp">{tp}</span><b>{t}</b><span class="tx">{tx}</span><span class="go">Testar</span></button>'
    for nome, lg, tp, t, tx, bg, d in A)
out = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ativações das marcas da Jota • Goomer Ads</title>
<style>
@font-face{{font-family:'Manrope';src:url('{fonts[0]}') format('woff2');font-weight:700}}
@font-face{{font-family:'Manrope';src:url('{fonts[1]}') format('woff2');font-weight:800}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%;height:100%;overflow:hidden;background:#141533;font-family:Manrope,system-ui,sans-serif;color:#fff;-webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent}}
.vp{{position:absolute;width:1280px;height:800px;transform-origin:top left;overflow:hidden;background:radial-gradient(70% 80% at 85% 0%,rgba(177,52,117,.45),transparent 60%),#141533}}
.hd{{position:absolute;left:64px;top:64px;right:64px}}
.hd img{{height:54px;width:auto;display:block;margin-bottom:26px}}
.hd h1{{font-size:56px;font-weight:800;line-height:1.05;letter-spacing:-.02em}}
.hd h1 em{{font-style:normal;color:#E25AA3}}
.hd p{{margin-top:12px;font-size:22px;font-weight:700;color:#C9C9E0}}
.cs{{position:absolute;left:64px;right:64px;top:350px;display:grid;grid-template-columns:repeat(3,1fr);gap:24px}}
.c{{text-align:left;border:0;cursor:pointer;background:#fff;color:#141533;border-radius:28px;padding:22px 22px 24px;display:flex;flex-direction:column;gap:10px;font-family:inherit;box-shadow:0 20px 40px rgba(0,0,0,.35);transition:transform .15s}}
.c:active{{transform:scale(.98)}}
.lg{{height:110px;border-radius:18px;display:flex;align-items:center;justify-content:center;padding:18px}}
.lg img{{max-height:70px;max-width:88%;object-fit:contain}}
.tp{{font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#B13475}}
.c b{{font-size:28px;font-weight:800;line-height:1.1}}
.tx{{font-size:17px;font-weight:700;color:#55557A;line-height:1.35;min-height:46px}}
.go{{align-self:flex-start;margin-top:6px;background:#141533;color:#fff;border-radius:999px;padding:14px 30px;font-size:19px;font-weight:800}}
#fr{{position:absolute;inset:0;width:100%;height:100%;border:0;display:none;background:#000}}
#bk{{position:absolute;left:16px;top:16px;z-index:5;display:none;border:0;cursor:pointer;background:rgba(20,21,51,.88);color:#fff;font:800 16px Manrope,system-ui,sans-serif;padding:12px 20px;border-radius:999px;box-shadow:0 8px 20px rgba(0,0,0,.3)}}
.poc{{position:absolute;left:0;right:0;bottom:0;height:40px;display:flex;align-items:center;justify-content:space-between;padding:0 20px;background:#15161d;border-top:1px solid rgba(255,255,255,.14)}}
.poc span{{font-size:12px;font-weight:700;color:#cbd5e1}}.poc b{{background:#2b00ff;font-size:11px;letter-spacing:.14em;padding:4px 10px;border-radius:6px;margin-right:12px}}
.poc i{{font-style:normal;font-size:10px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:#94a3b8;display:flex;align-items:center;gap:10px}}
.goomer-logo{{display:block;width:88px;height:auto;color:#fff}}
</style></head><body>
<div class="vp" id="vp">
<div class="hd"><img src="{logo('logo-claro.png', 400)}" alt="Jota"><h1>Ativações das <em>marcas da Jota</em></h1><p>Escolha uma e teste como o cliente vê na mesa.</p></div>
<div class="cs">{cards}</div>
<div class="poc"><span><b>POC</b>Protótipos de demonstração, não são produtos oficiais das marcas.</span><i>powered by {gsvg}</i></div>
<iframe id="fr" title="Ativação"></iframe><button id="bk">← Trocar ativação</button>
</div>
<script>
var H={json.dumps(html_of)};
function fit(){{var v=document.getElementById('vp'),s=Math.min(innerWidth/1280,innerHeight/800);v.style.transform='scale('+s+')';v.style.left=Math.round((innerWidth-1280*s)/2)+'px';v.style.top=Math.round((innerHeight-800*s)/2)+'px'}}
addEventListener('resize',fit);fit();
var fr=document.getElementById('fr'),bk=document.getElementById('bk'),idle;
function home(){{clearTimeout(idle);fr.style.display='none';bk.style.display='none';fr.removeAttribute('srcdoc')}}
function bump(){{clearTimeout(idle);idle=setTimeout(home,60000)}}
function abrir(k){{fr.srcdoc=new TextDecoder().decode(Uint8Array.from(atob(H[k]),function(c){{return c.charCodeAt(0)}}));fr.style.display='block';bk.style.display='block';bump()}}
fr.onload=function(){{try{{['pointerdown','keydown'].forEach(function(e){{fr.contentWindow.addEventListener(e,bump)}})}}catch(_){{}}}};
document.querySelectorAll('.c').forEach(function(b){{b.onclick=function(){{abrir(b.dataset.k)}}}});
bk.onclick=home;
</script></body></html>'''
p = os.path.join(ROOT, 'jota', 'ativacoes', 'index.html')
os.makedirs(os.path.dirname(p), exist_ok=True)
open(p, 'w', encoding='utf-8').write(out)
print('ok:', p, len(out) // 1024, 'KB')

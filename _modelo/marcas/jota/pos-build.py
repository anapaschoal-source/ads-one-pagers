"""Pós-build da Jota (diverge do modelo): a página é da agência (logo Jota no topo e nas seções), mas os
criativos dos formatos mostram o cliente de exemplo, Mercado Livre. Troca o logo dentro dos banners/vídeo
(img.vd-lg, img.vd-lg2 e img.lg) pelo logo do Mercado Livre.
Uso (na raiz do repo): python3 _modelo/marcas/jota/pos-build.py jota/index.html [/home/claude/one-pager-jota.html]"""
import sys, os, re, base64, io
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(D, '..', '..', '..'))
im = Image.open(os.path.join(D, 'mercado-livre.png'))
if im.width > 600:
    im = im.resize((600, round(im.height * 600 / im.width)), Image.LANCZOS)
buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
ml = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()
def small(nome, w=360):
    i = Image.open(os.path.join(D, nome)).convert('RGBA'); i = i.crop(i.getchannel('A').getbbox()); i.thumbnail((w, 120), Image.LANCZOS)
    b = io.BytesIO(); i.save(b, 'PNG', optimize=True); return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

ACTS = [
    ('ml', 'Mercado Livre', 'mercado-livre.png', 'Jogo', '/jota/jogo/', [
        ('Entra no menu Mercado Livre', 'O usuário abre a categoria Mercado Livre no cardápio do tablet.'),
        ('Faz a Entrega Relâmpago', 'Toca nos pacotes antes que sumam e entrega 10 em 20 segundos.'),
        ('Ganha o cupom', 'Cupom de desconto para usar no app do Mercado Livre.')]),
    ('l360', 'Life360', 'life360.png', 'Quiz', '/jota/quiz/', [
        ('Entra no menu Life360', 'O usuário abre a categoria Life360 no cardápio do tablet.'),
        ('Responde o quiz', 'Três perguntas sobre a família, em 30 segundos.'),
        ('Baixa o app', 'QR code para baixar a Life360 com teste grátis do premium.')]),
    ('sic', 'Sicredi', 'sicredi.png', 'Roleta', '/jota/roleta/', [
        ('Entra no menu Sicredi', 'O usuário abre a categoria Sicredi no cardápio do tablet.'),
        ('Gira a roleta', 'Um toque e a roleta sorteia um benefício Sicredi.'),
        ('Resgata o benefício', 'Código por e-mail e QR code para abrir a conta no app.')]),
]
LEAD = ('Na página especial, é possível criar um modelo <strong>inovador</strong> de ativação da marca, podendo gerar benefícios '
        'e um nível único de interação com os usuários da mesa. Para mostrar o que dá para fazer com as marcas da Jota, criamos '
        'três ativações: a Entrega Relâmpago do Mercado Livre, o quiz da Life360 e a roleta do Sicredi, todas com segmentação '
        'por praça e horário. Escolha uma e teste no tablet.')
CSS = """<style>/*jota-acts*/
.acts{display:flex;flex-wrap:wrap;gap:10px;margin-top:4px}
.acts button{display:flex;align-items:center;gap:10px;background:#fff;border:2px solid #E3E3EE;border-radius:14px;padding:10px 14px;cursor:pointer;font:800 11px Manrope,system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#6B6B80;transition:border-color .15s,transform .15s}
.acts button:hover{transform:translateY(-1px)}
.acts button img{height:24px;width:auto;max-width:120px;object-fit:contain;display:block}
.acts button[aria-pressed="true"]{border-color:var(--cor);color:var(--cor);box-shadow:0 6px 18px rgba(0,0,0,.08)}
.act-steps[hidden]{display:none!important}
</style>"""

def seletor(s):
    if '/*jota-acts*/' in s: return s
    a = s.index('<div class="block act">'); b = s.index('<div class="demo">', a)
    btns = ''.join(f'<button type="button" data-act="{k}" aria-pressed="{str(i == 0).lower()}"><img src="{small(lg)}" alt="{nome}">{tipo}</button>'
                   for i, (k, nome, lg, tipo, url, ps) in enumerate(ACTS))
    steps = ''.join(f'<div class="act-steps" data-act="{k}"{"" if i == 0 else " hidden"}>' + ''.join(
        f'<div class="act-step"><div class="n">{j + 1}</div><div><b>{t}</b><span>{x}</span></div></div>' for j, (t, x) in enumerate(ps)) + '</div>'
        for i, (k, nome, lg, tipo, url, ps) in enumerate(ACTS))
    head = ('<div class="block act">\n<h2 class="cond" style="margin-bottom:18px">Da campanha para a mesa</h2>\n'
            f'<div style="display:flex;flex-direction:column;gap:16px">\n<p class="lead">{LEAD}</p>\n'
            f'<div class="acts" role="group" aria-label="Escolha a ativação">{btns}</div>\n{steps}\n</div>\n')
    s = s[:a] + head + s[b:]
    meta = {k: {'url': url, 'logo': small(lg, 200), 'nome': nome} for k, nome, lg, tipo, url, ps in ACTS}
    if '<iframe srcdoc=' in s:  # versão artefato: demos embutidos
        for k, nome, lg, tipo, url, ps in ACTS:
            meta[k]['b64'] = base64.b64encode(open(os.path.join(ROOT, url.strip('/'), 'index.html'), 'rb').read()).decode()
    import json
    js = ('<script>/*jota-acts*/(function(){var A=' + json.dumps(meta) + ';'
          'var bs=document.querySelectorAll(".acts button"),st=document.querySelectorAll(".act-steps[data-act]"),'
          'demo=document.querySelector(".act .demo"),fr=demo&&demo.querySelector("iframe"),lg=demo&&demo.querySelector(".menu-cell img");'
          'bs.forEach(function(b){b.addEventListener("click",function(){var k=b.dataset.act;'
          'bs.forEach(function(x){x.setAttribute("aria-pressed",x===b?"true":"false")});'
          'st.forEach(function(x){x.hidden=x.dataset.act!==k});'
          'if(fr){if(A[k].b64){fr.removeAttribute("src");fr.srcdoc=new TextDecoder().decode(Uint8Array.from(atob(A[k].b64),function(c){return c.charCodeAt(0)}))}else fr.src=A[k].url;fr.title="Demo "+A[k].nome}if(lg){lg.src=A[k].logo;lg.alt=A[k].nome}})})})();</script>')
    s = s.replace('</body>', CSS + js + '</body>', 1) if '</body>' in s else s + CSS + js
    s = s.replace('<span class="tag on">Demo Mercado Livre</span>', '<span class="tag on">3 demos</span>')
    return s

for path in sys.argv[1:]:
    s = open(path, encoding='utf-8').read()
    s, n = re.subn(r'(<img class="(?:vd-lg|vd-lg2|lg)" src=")data:[^"]+(")', lambda m: m.group(1) + ml + m.group(2), s)
    lc = Image.open(os.path.join(D, 'logo-claro.png')); lc.thumbnail((600, 300), Image.LANCZOS)
    b2 = io.BytesIO(); lc.save(b2, 'PNG', optimize=True)
    s, k = re.subn(r'(<img class="bl" src=")data:[^"]+(")', lambda m: m.group(1) + 'data:image/png;base64,' + base64.b64encode(b2.getvalue()).decode() + m.group(2), s)
    s = s.replace('<span class="tag on">Demo Jota</span>', '<span class="tag on">Demo Mercado Livre</span>')
    s = s.replace('title="Demo Jota"', 'title="Demo Mercado Livre"')
    s = s.replace('alt="Formato Página Especial: aba Jota', 'alt="Formato Página Especial: aba Mercado Livre')
    s = seletor(s)
    open(path, 'w', encoding='utf-8').write(s)
    print(path, 'logos trocados:', n)

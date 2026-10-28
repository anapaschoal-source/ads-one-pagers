"""Pós-build da Estrella Galicia (diverge do modelo): troca as 4 telas da "Jornada da marca" pelos formatos
animados do media kit Goomer Ads (mesmas telas, sequências, molduras, linha do tempo e painel "Formatos em ação"),
com os criativos da Estrella Galicia.
Pré-requisitos: build-jogo.py e mk/make-assets.py já rodados. CSS e telas base vêm do media kit (mk/).
Uso (na raiz do repo): python3 _modelo/marcas/estrella-galicia/pos-build.py estrella-galicia/index.html [one-pager-estrella-galicia.html]"""
import sys, os, re, base64, json

D = os.path.dirname(os.path.abspath(__file__))
MK = os.path.join(D, 'mk')
ROOT = os.path.abspath(os.path.join(D, '..', '..', '..'))

def uri(p, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(p, 'rb').read()).decode()

IMG = {
    'tab': uri(os.path.join(MK, 'tab.webp'), 'image/webp'),
    'pop': uri(os.path.join(MK, 'out-popup.webp'), 'image/webp'),
    'mc': uri(os.path.join(MK, 'out-mcscr.webp'), 'image/webp'),
    'es': uri(os.path.join(MK, 'out-especial.webp'), 'image/webp'),
    'foto': uri(os.path.join(D, 'foto-inicio.jpg'), 'image/jpeg'),
}
GAME = base64.b64encode(open(os.path.join(ROOT, 'estrella-galicia', 'jogo', 'index.html'), 'rb').read()).decode()
MKCSS = open(os.path.join(MK, 'mk-formatos.css'), encoding='utf-8').read()

CSS = """/*mk-formatos*/
.fx,.mkthumb{--ink:#0A0044;--deep:#06002B;--blue:#2B00FF;--lime:#BDE249;--paper:#FFFFFF;--fg:#FFFFFF;--muted:rgba(255,255,255,.66);--faint:rgba(255,255,255,.14);--line:rgba(255,255,255,.18);--panel:rgba(10,0,68,.78);--orange:#FF8A3D;--display:Antonio,'Arial Narrow',sans-serif;--body:Manrope,system-ui,sans-serif}
.fx{color:var(--fg);font-family:var(--body);font-size:16px;line-height:1.5;text-align:left}
.fx *{box-sizing:border-box}
.fx h2,.fx h3{font-family:var(--display);font-weight:700;text-transform:uppercase;line-height:1.12;margin:0;letter-spacing:.005em}
.fx p{margin:0}.fx button{font-family:inherit;color:inherit}
.fx .eyebrow{font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--lime)}
.mkthumb{cursor:pointer;position:relative;overflow:hidden}
.mkthumb:focus-visible{outline:2px solid var(--azul);outline-offset:2px}
.tvbox img.tv{animation:kb 14s ease-in-out infinite alternate}
.mkmore{align-self:flex-start;margin-top:2px;border:0;background:none;padding:0;font-weight:800;font-size:12px;line-height:1.2;font-family:inherit;color:var(--azul);cursor:pointer}
.card.hl .mkmore{color:var(--tinta)}
.mkmore:hover{text-decoration:underline}
.fx h2,.fx h3{color:var(--fg)}
.fx .gameclose{color:var(--ink)}
.mkthumb .scr.real::after{font-size:6px;padding:2px 4px;border-radius:3px;letter-spacing:0}
"""

DESC = {
    'inicio': 'Conteúdo dinâmico em vídeo de 10 segundos, intercalado com o conteúdo do restaurante. Se o cliente quiser pedir durante a exibição, um toque leva direto ao cardápio.',
    'confirm': 'Banner exibido no momento em que o pedido é enviado para a cozinha, com a atenção total do cliente na tela.',
    'conta': 'Banner na tela da conta, no fechamento da visita: o último contato do cliente com o restaurante.',
    'especial': 'Uma aba própria da marca no menu do cardápio, que abre uma página em HTML interativo. Toque em Bora tirar e teste a Tirada Perfeita 0,0 da Estrella Galicia.',
}
TL = {
    'inicio': [(14.3, 'r', 'Restaurante'), (71.4, 'a', 'Publicidade da marca · 10s'), (14.3, 'r', 'Restaurante')],
    'confirm': [(43, 'r', 'Cliente escolhe e envia o pedido'), (57, 'a', 'Pedido enviado · banner da marca')],
    'conta': [(23, 'r', 'Cliente toca em Minha Conta'), (77, 'a', 'Conta aberta · banner da marca')],
}
def tl(k):
    if k not in TL:
        return ''
    b = ''.join(f'<span class="s {c}" style="width:{w}%"></span>' for w, c, _ in TL[k])
    l = ''
    for w, c, t in TL[k]:
        cls = ' class="a"' if c == 'a' else ''
        l += f'<span style="width:{w}%"{cls}>{t}</span>'
    return f'<div class="tl" aria-hidden="true"><div class="tl-bar">{b}<i class="ph"></i></div><div class="tl-lb">{l}</div></div>'

SCR = 'left:23.57%;top:18.29%;width:62.09%;height:50.43%'
VS = 'left:14.34%;top:11.57%;width:71.31%;height:58.14%'
MENU = ('<div class="vmenu"><h6>Hambúrgueres Gourmet</h6>'
        '<div class="vc"><div class="vph"></div><div class="vt"><b>Picanha ao Fogo</b><span>Blend de picanha, queijo e molho chimichurri</span><div class="vr"><em>R$ 34,90</em><i class="vadd">ADICIONAR</i></div></div></div>'
        '<div class="vc"><div class="vph"></div><div class="vt"><b>Smash da Casa</b><span>Dois smashs, cheddar e cebola caramelizada</span><div class="vr"><em>R$ 29,90</em><i class="vadd">ADICIONAR</i></div></div></div></div>'
        '<div class="vcart"><h6>Carrinho · Mesa 2</h6><div class="ci"><span>1× Picanha ao Fogo</span><b>R$ 34,90</b></div><div class="ctot"><span>Total</span><b class="t1">R$ 34,90</b><b class="t2">R$ 44,80</b></div><i class="vgo">FAZER PEDIDO</i></div>')
REST = '<div class="rban"><div class="rb-ph"></div><div class="rb-t"><small>Restaurante Goomer</small><b>Peça o seu!</b><span>Picanha ao Fogo com molho chimichurri</span><em>R$ 34,90</em><i>Peça o seu</i></div></div>'

H = {
    'inicio': f'<div class="scr real vreal"><img src="${{I.tab}}" alt="Tablet Goomer no restaurante"><div class="tvbox" style="{SCR}">{REST}<img class="tv" src="${{I.foto}}" alt="Publicidade da Estrella Galicia na Tela de Início"></div><span class="hl vhl" style="{SCR}"><em>Publicidade · 10s</em></span></div>' + tl('inicio'),
    'confirm': f'<div class="scr real"><img src="${{I.tab}}" alt="Tablet Goomer no restaurante"><div class="vs" data-seq="confirm" style="{VS}">{MENU}<div class="vdim"></div><div class="vmodal vconf"><img src="${{I.pop}}" alt="Pop-up de pedido enviado com banner da Estrella Galicia"><span class="vtimer"><i></i></span></div><span class="hl vchl"><em>Banner na confirmação</em></span><i class="finger"></i></div></div>' + tl('confirm'),
    'conta': f'<div class="scr real"><img src="${{I.tab}}" alt="Tablet Goomer no restaurante"><div class="vs" data-seq="conta" style="{VS}"><div class="tvbox mchome" style="left:12.9%;top:11.5%;width:87.1%;height:86.7%">{REST}</div><img class="mcscr" src="${{I.mc}}" alt="Tela Minha Conta com banner da Estrella Galicia"><span class="hl mchl"><em>Espaço da marca</em></span><i class="finger"></i></div></div>' + tl('conta'),
    'especial': f'<div class="scr real"><img src="${{I.es}}" alt="Tablet Goomer com a aba Estrella selecionada e a página especial do jogo"><span class="hl" style="left:14.86%;top:26.29%;width:7.07%;height:8.57%"><em class="below">Aba da marca</em></span><span class="hl" style="{SCR}"><em>Página da marca</em></span><button type="button" class="playbtn" style="{SCR}"><span class="sr">Jogar a Tirada Perfeita 0,0</span></button><div class="gamebox" style="{SCR}" hidden><iframe title="Tirada Perfeita 0,0"></iframe></div><button type="button" class="gameclose" hidden>✕ Sair do jogo</button></div>',
}
FORMATS = [
    ('inicio', 'Tela de Início', 'Vídeo 10s', ['Vídeo 10s', 'DOOH', 'Tela cheia'], 14),
    ('confirm', 'Confirmação de Pedido', 'Banner estático', ['Banner estático', 'DOOH'], 10),
    ('conta', 'Minha Conta', 'Banner estático', ['Banner estático', 'DOOH'], 10),
    ('especial', 'Página Especial', 'HTML interativo', ['HTML interativo', 'DOOH', 'Conteúdo dinâmico'], 12),
]

def js_formats():
    out = []
    for fid, n, k, tags, dur in FORMATS:
        out.append('{id:%s,n:%s,k:%s,tags:%s,d:%s,dur:%d,h:`%s`}' % (json.dumps(fid), json.dumps(n, ensure_ascii=False), json.dumps(k, ensure_ascii=False), json.dumps(tags, ensure_ascii=False), json.dumps(DESC[fid], ensure_ascii=False), dur, H[fid]))
    return '[' + ',\n'.join(out) + ']'

OVERLAY = open(os.path.join(MK, 'overlay.html'), encoding='utf-8').read()

# faixa de anunciantes: inclui Cyrela e baixa um pouco o logo da Comgás (igual à Shopee)
CY = uri(os.path.join(D, 'cli-cyrela.png'), 'image/png')
def clientes(s):
    if 'alt="Cyrela"' not in s:
        s = s.replace('grid-template-columns:repeat(5,1fr)', 'grid-template-columns:repeat(6,1fr)', 1)
        s, k = re.subn(r'(<div class="clients">.*?<div class="grid">(?:\s*<div><img[^>]*></div>)+)', lambda m: m.group(1) + f'\n<div><img src="{CY}" alt="Cyrela" style="max-height:30px"></div>', s, count=1, flags=re.S)
        assert k, 'faixa de clientes não encontrada'
    s = s.replace('alt="Comgás" style="max-height:28px"', 'alt="Comgás" style="max-height:28px;transform:translateY(5px)"', 1)
    return s

NAMES = ['Tela de Início', 'Confirmação de Pedido', 'Minha Conta', 'Página Especial']

for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    if '/*mk-formatos*/' in s:
        print(f, 'já tem os formatos do media kit'); continue
    s = clientes(s)
    s = s.replace('</style>', CSS + MKCSS + '\n</style>', 1)
    shots = list(re.finditer(r'<div class="shot" role="img"[^>]*>.*?(?=\s*<div class="fmt-body">)', s, re.S))
    assert len(shots) == 4, f'shots: {len(shots)}'
    for i in range(3, -1, -1):
        m = shots[i]
        s = s[:m.start()] + f'<div class="shot mkthumb" role="button" tabindex="0" data-mk="{i}" aria-label="Ver {NAMES[i]} em detalhe"></div>' + s[m.end():]
    parts = s.split('<div class="fmt-body">')
    assert len(parts) == 5
    out = parts[0]
    for i in range(4):
        body = parts[i + 1]
        k = body.index('</div>\n</div></div>')  # fecha fmt-body, card, step
        body = body[:k] + f'<button type="button" class="mkmore" data-mk="{i}">Ver em detalhe →</button>' + body[k:]
        out += '<div class="fmt-body">' + body
    s = out
    ov = OVERLAY.replace('__GAME__', GAME).replace('__IMG__', json.dumps(IMG)).replace('__FORMATS__', js_formats())
    k = s.rindex('</body>') if '</body>' in s else len(s)
    s = s[:k] + ov + s[k:]
    open(f, 'w', encoding='utf-8').write(s)
    print(f, 'formatos do media kit aplicados', len(s) // 1024, 'KB')

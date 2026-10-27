"""Pós-build da Estrella Galicia (diverge do modelo): anima os 4 formatos como no media kit interativo
(dedo tocando, moldura lima com rótulo, timer do pop-up, tela anterior e linha do tempo com marcador).
Uso (na raiz do repo): python3 _modelo/marcas/estrella-galicia/pos-build.py estrella-galicia/index.html [one-pager-estrella-galicia.html]"""
import sys, re

CSS = r"""/*mk-anim*/
.cy-f .mk{position:absolute;pointer-events:none}
.mk-hl{z-index:6;border:.7cqw solid var(--lima);border-radius:.9cqw;opacity:0}
.mk-hl em{position:absolute;left:.6cqw;top:.6cqw;font-style:normal;font-family:Manrope,system-ui,sans-serif;font-size:3.7cqw;font-weight:800;letter-spacing:.06em;text-transform:uppercase;background:var(--lima);color:#0A0044;padding:.8cqw 1.8cqw;border-radius:1.2cqw;white-space:nowrap}
.mk-hl em.out{top:auto;bottom:calc(100% + 1cqw);left:-.7cqw}
.mk-hl::after{content:"";position:absolute;inset:-.7cqw;border-radius:.9cqw;box-shadow:0 0 0 0 rgba(189,226,73,.55);animation:mkpulse 2.2s ease-in-out infinite}
@keyframes mkpulse{50%{box-shadow:0 0 0 1.4cqw rgba(189,226,73,0)}}
.mk-fg{z-index:7;width:7cqw;height:7cqw;margin:-3.5cqw 0 0 -3.5cqw;opacity:0}
.mk-fg i{position:absolute;inset:0;border-radius:50%;background:rgba(255,255,255,.6);border:.6cqw solid #fff;box-shadow:0 .5cqw 1.6cqw rgba(0,0,0,.45)}
.mk-fg b{position:absolute;inset:-.6cqw;border-radius:50%;border:.6cqw solid #fff;opacity:0}
.mk-rest{z-index:0;background:#2A160C;display:flex;flex-direction:column;justify-content:center;gap:1.4cqw;padding:0 7cqw;color:#fff;font-family:Poppins,Manrope,system-ui,sans-serif;overflow:hidden}
.mk-rest small{font-size:2.6cqw;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#F7841F}
.mk-rest strong{font-size:7.5cqw;line-height:1;font-weight:800;text-transform:uppercase}
.mk-rest span{font-size:2.8cqw;opacity:.8}
.mk-rest u{text-decoration:none;align-self:flex-start;background:#F7841F;font-weight:800;font-size:2.6cqw;padding:1.2cqw 2.6cqw;border-radius:1cqw;margin-top:.8cqw}
.mk-prev{z-index:5;inset:0;background:center/100% 100% no-repeat}
.mk-timer{position:absolute;left:0;right:0;bottom:0;height:1.6%;background:#e8e8e8;z-index:2}
.mk-timer i{display:block;height:100%;width:0;background:#5BB974}
.mk-tl{padding:10px 14px 0;display:grid;gap:5px}
.mk-tl .bar{position:relative;display:flex;height:6px;border-radius:3px;overflow:hidden;background:#E7E5F2}
.mk-tl .bar span{height:100%}
.mk-tl .bar .r{background:#CFCBE3}
.mk-tl .bar .a{background:var(--lima)}
.mk-tl .bar i{position:absolute;top:-2px;bottom:-2px;width:3px;margin-left:-1px;background:#0A0044;border-radius:2px;left:0;animation:mkph 10s linear infinite}
.mk-tl .lb{display:flex;font-size:10px;font-weight:700;line-height:1.25;color:#6B6589;text-align:center}
.mk-tl .lb .a{color:#0A0044}
@keyframes mkph{to{left:100%}}
.card.hl .mk-tl .bar{background:rgba(10,0,68,.12)}.card.hl .mk-tl .bar .a{background:#fff}.card.hl .mk-tl .bar .r{background:rgba(10,0,68,.22)}
/* 1 · Tela de Início: restaurante → publicidade 10s → restaurante */
.mk1 .cy-a1{z-index:1;animation:mk1ad 10s ease-in-out infinite}
.mk1 .cy-a2{z-index:2;animation:mk1lb 10s ease-out infinite}
.mk1 .mk-hl{animation:mk1hl 10s ease infinite}
@keyframes mk1ad{0%,18%{opacity:0}23%,88%{opacity:1}93%,100%{opacity:0}}
@keyframes mk1lb{0%,26%{opacity:0;transform:translateY(10%)}32%,88%{opacity:1;transform:none}93%,100%{opacity:0}}
@keyframes mk1hl{0%,24%{opacity:0}30%,88%{opacity:1}92%,100%{opacity:0}}
/* 2 · Confirmação: toque no carrinho → pop-up com banner e timer */
.mk2 .cy-a3{z-index:3;animation:mk2pop 10s cubic-bezier(.2,.9,.3,1.1) infinite}
.mk2 .mk-timer i{animation:mk2tm 10s linear infinite}
.mk2 .mk-hl{animation:mk2hl 10s ease infinite}
.mk2 .mk-fg{animation:mk2fg 10s ease-in-out infinite}
.mk2 .mk-fg b{animation:mktap1 10s ease-out infinite}
.mk2 .mk-fg i{animation:mktap2 10s ease-out infinite}
@keyframes mk2pop{0%,30%{opacity:0;transform:scale(.9) translateY(4%)}36%,92%{opacity:1;transform:none}96%,100%{opacity:0;transform:none}}
@keyframes mk2tm{0%,36%{width:0}90%,100%{width:100%}}
@keyframes mk2hl{0%,38%{opacity:0}44%,92%{opacity:1}95%,100%{opacity:0}}
@keyframes mk2fg{0%{opacity:0;left:62%;top:62%}6%{opacity:1;left:62%;top:62%}20%{left:89.5%;top:5.6%}29%{opacity:1;left:89.5%;top:5.6%}34%,100%{opacity:0;left:89.5%;top:5.6%}}
@keyframes mktap1{0%,22%{opacity:0;transform:scale(1)}23%{opacity:.9;transform:scale(1)}30%,100%{opacity:0;transform:scale(2.4)}}
@keyframes mktap2{0%,21%{transform:scale(1)}23%{transform:scale(.72)}26%,100%{transform:scale(1)}}
/* 3 · Minha Conta: cardápio → toque em Minha Conta → conta com banner */
.mk3 .mk-prev{animation:mk3prev 10s ease infinite}
.mk3 .cy-a4{animation:mk3ban 10s cubic-bezier(.22,.8,.3,1) infinite}
.mk3 .mk-hl{animation:mk3hl 10s ease infinite}
.mk3 .mk-fg{animation:mk3fg 10s ease-in-out infinite}
.mk3 .mk-fg b{animation:mktap1 10s ease-out infinite}
.mk3 .mk-fg i{animation:mktap2 10s ease-out infinite}
@keyframes mk3prev{0%,25%{opacity:1}31%,100%{opacity:0}}
@keyframes mk3ban{0%,34%{transform:translateX(115%)}44%,92%{transform:none}97%,100%{transform:translateX(115%)}}
@keyframes mk3hl{0%,44%{opacity:0}50%,92%{opacity:1}95%,100%{opacity:0}}
@keyframes mk3fg{0%{opacity:0;left:55%;top:55%}6%{opacity:1;left:55%;top:55%}20%{left:80.6%;top:5.6%}28%{opacity:1;left:80.6%;top:5.6%}33%,100%{opacity:0;left:80.6%;top:5.6%}}
/* 4 · Página Especial: toque na aba da marca → página abre */
.mk4 .cy-scr{animation:mk4pg 10s ease infinite}
.mk4 .mk-hl.ab{animation:mk4ab 10s ease infinite}
.mk4 .mk-hl.pg{animation:mk4hl 10s ease infinite}
.mk4 .mk-fg{animation:mk4fg 10s ease-in-out infinite}
.mk4 .mk-fg b{animation:mktap1 10s ease-out infinite}
.mk4 .mk-fg i{animation:mktap2 10s ease-out infinite}
@keyframes mk4pg{0%,25%{opacity:0;transform:translateY(3%)}32%,92%{opacity:1;transform:none}97%,100%{opacity:0}}
@keyframes mk4ab{0%,22%{opacity:0}27%,92%{opacity:1}96%,100%{opacity:0}}
@keyframes mk4hl{0%,34%{opacity:0}40%,92%{opacity:1}95%,100%{opacity:0}}
@keyframes mk4fg{0%{opacity:0;left:55%;top:60%}6%{opacity:1;left:55%;top:60%}20%{left:11%;top:26.5%}28%{opacity:1;left:11%;top:26.5%}33%,100%{opacity:0;left:11%;top:26.5%}}
@media (prefers-reduced-motion: reduce){.cy-f .mk,.mk1 .cy-a1,.mk1 .cy-a2,.mk2 .cy-a3,.mk3 .cy-a4,.mk4 .cy-scr,.mk-tl .bar i,.mk-timer i{animation:none!important}.mk-fg,.mk-prev{display:none}.mk-hl{opacity:1}}
"""

FG = '<div class="mk mk-fg"><b></b><i></i></div>'
SCR = 'left:17.593%;top:9.115%;width:77.963%;height:66.406%'

def tl(segs):
    bar = ''.join(f'<span class="{c}" style="width:{w}%"></span>' for w, c, _ in segs)
    lb = ''.join(f'<span class="{c}" style="width:{w}%">{t}</span>' for w, c, t in segs)
    return f'<div class="mk-tl" aria-hidden="true"><div class="bar">{bar}<i></i></div><div class="lb">{lb}</div></div>\n'

TLS = [
    tl([(22, 'r', ''), (68, 'a', 'Vídeo da marca · 10s'), (10, 'r', '')]),
    tl([(33, 'r', 'Pedido'), (67, 'a', 'Banner da marca')]),
    tl([(31, 'r', 'Conta'), (69, 'a', 'Banner da marca')]),
    tl([(30, 'r', 'Aba'), (70, 'a', 'Página da marca')]),
]

for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    if '/*mk-anim*/' in s:
        print(f, 'já animado'); continue
    s = s.replace('</style>', CSS + '</style>', 1)
    opens = list(re.finditer(r'<div class="cy-f" style="background-image:url\(([^)]+)\)">', s))
    assert len(opens) >= 4, f'achei {len(opens)} cy-f'
    fmt1 = opens[0].group(1)
    extra = [
        f'<div class="mk mk-rest" style="{SCR}"><small>Restaurante Goomer</small><strong>Peça o seu!</strong><span>Picanha ao fogo com chimichurri</span><u>Peça o seu</u></div>'
        f'<span class="mk mk-hl" style="{SCR}"><em>Publicidade · 10s</em></span>',
        f'<span class="mk mk-hl" style="left:32.407%;top:16.146%;width:48.148%;height:51.823%"><em class="out">Banner na confirmação</em></span>{FG}',
        f'<div class="mk mk-prev" style="background-image:url({fmt1})"></div>'
        f'<span class="mk mk-hl" style="left:69.630%;top:13.802%;width:23.15%;height:21.875%"><em class="out">Espaço da marca</em></span>{FG}',
        f'<span class="mk mk-hl ab" style="left:7.3%;top:21.4%;width:7.5%;height:9.4%"></span>'
        f'<span class="mk mk-hl pg" style="{SCR}"><em>Página da marca</em></span>{FG}',
    ]
    for i in range(3, -1, -1):
        m = opens[i]
        tag = m.group(0).replace('class="cy-f"', f'class="cy-f mk{i+1}"')
        s = s[:m.start()] + tag + extra[i] + s[m.end():]
    # confirmação: timer verde no rodapé do pop-up
    s = s.replace('<div class="cy-ab cy-a3"', '<div class="cy-ab cy-a3" data-mk="2"', 1)
    k = s.index('data-mk="2"'); k2 = s.index('>OK</div></div>', k) + len('>OK</div></div>')
    s = s[:k2] + '<span class="mk-timer"><i></i></span>' + s[k2:]
    # linha do tempo embaixo de cada formato
    parts = s.split('<div class="fmt-body">')
    assert len(parts) == 5, f'fmt-body: {len(parts)-1}'
    s = parts[0] + ''.join(TLS[i] + '<div class="fmt-body">' + parts[i + 1] for i in range(4))
    open(f, 'w', encoding='utf-8').write(s)
    print(f, 'animado')

"""Pós-build do Tenda Atacado (diverge do modelo), só neste material:
1. inclui a Dellys na faixa "Marcas que já anunciam com a gente" (logo branco em cli-dellys.png);
2. troca a tela do tablet do topo pelo banner de verão;
3. card da Página Especial com a tela de início do jogo (tela-jogo.jpg);
4. anima o painel B2B: o cursor clica no banner e abre o site do Tenda Atacado (tela ilustrativa,
   montada com logo, banner de verão e ícones site-*.svg).
Uso (na raiz do repo): python3 _modelo/marcas/tenda-atacado/pos-build.py tenda-atacado/index.html [/home/claude/one-pager-tenda-atacado.html]"""
import sys, os, re, base64
D = os.path.dirname(os.path.abspath(__file__))


def uri(nome, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(os.path.join(D, nome), 'rb').read()).decode()


DELLYS = uri('cli-dellys.png', 'image/png')
LOGO = uri('logo.png', 'image/png')
BANNER = uri('banner-b2b.png', 'image/png')
PRODS = [('refri', 'Refrigerante cola 2L · fardo 6 un', 'R$ 39,90'), ('carne', 'Contrafilé bovino · kg', 'R$ 69,90'),
         ('carvao', 'Carvão vegetal 5 kg', 'R$ 34,90'), ('agua', 'Água mineral 1,5L · fardo 6 un', 'R$ 29,90'),
         ('latas', 'Refrigerante lata · fardo 12 un', 'R$ 49,90'), ('gelo', 'Gelo em cubos 5 kg', 'R$ 19,90')]

CSS = """<style>/*tenda-site*/
.panel{container-type:inline-size}
.tcur{position:absolute;z-index:6;width:2.6cqw;left:84%;top:84%;opacity:0;pointer-events:none;filter:drop-shadow(0 .2cqw .4cqw rgba(0,0,0,.35));animation:tcur 9s infinite}
.tcur svg{display:block;width:100%;height:auto}
@keyframes tcur{0%,6%{left:84%;top:84%;opacity:0;transform:scale(1)}10%{opacity:1}16%{left:84%;top:84%}29%{left:67%;top:33%;transform:scale(1)}31%{transform:scale(.8)}33%{left:67%;top:33%;transform:scale(1);opacity:1}38%,100%{left:67%;top:33%;opacity:0}}
.trip{position:absolute;z-index:5;left:67%;top:33%;width:6cqw;height:6cqw;margin:-3cqw 0 0 -3cqw;border-radius:50%;border:.35cqw solid #fff;background:rgba(255,255,255,.35);opacity:0;pointer-events:none;animation:trip 9s infinite}
@keyframes trip{0%,30%{opacity:0;transform:scale(.3)}31%{opacity:1}38%,100%{opacity:0;transform:scale(1.6)}}
.tsite{position:absolute;z-index:4;inset:3% 4%;background:#F4F5F8;border-radius:1cqw;overflow:hidden;box-shadow:0 1.5cqw 4cqw rgba(10,0,68,.35);opacity:0;transform-origin:67% 33%;pointer-events:none;font-family:Manrope,system-ui,sans-serif;color:#1B396E;animation:tsite 9s infinite}
@keyframes tsite{0%,33%{opacity:0;transform:scale(.4)}38%{opacity:1;transform:scale(1)}90%{opacity:1;transform:scale(1)}95%,100%{opacity:0;transform:scale(1)}}
.tsite .ts-bb{height:3.6cqw;background:#E7E9EF;display:flex;align-items:center;gap:.6cqw;padding:0 1.4cqw}
.tsite .ts-bb i{width:.8cqw;height:.8cqw;border-radius:50%;background:#C9CDD8}
.tsite .ts-bb b{margin-left:1.2cqw;flex:1;max-width:40cqw;background:#fff;border-radius:2cqw;font-size:1.15cqw;font-weight:700;color:#55607a;padding:.45cqw 1.4cqw}
.tsite .ts-vw{position:absolute;top:3.6cqw;left:0;right:0;bottom:0;overflow:hidden}
.tsite .ts-pg{animation:tscroll 9s infinite}
@keyframes tscroll{0%,100%{transform:none}}
.tsite .ts-hd{background:#1B396E;display:flex;align-items:center;gap:2cqw;padding:1.1cqw 2.2cqw}
.tsite .ts-hd img{height:4.2cqw;display:block}
.tsite .ts-hd .ts-sr{flex:1;background:#fff;border-radius:.6cqw;font-size:1.25cqw;font-weight:700;color:#8a93a8;padding:.9cqw 1.4cqw}
.tsite .ts-hd .ts-ac{color:#fff;font-size:1.2cqw;font-weight:800;white-space:nowrap}
.tsite .ts-nv{background:#EE2E24;color:#fff;display:flex;gap:2.4cqw;padding:.8cqw 2.2cqw;font-size:1.15cqw;font-weight:800;white-space:nowrap;overflow:hidden}
.tsite .ts-hero{margin:1.2cqw 2.2cqw 0;border-radius:.8cqw;overflow:hidden}
.tsite .ts-hero img{display:block;width:100%;height:auto}
.tsite .ts-h{margin:1.2cqw 2.2cqw .7cqw;font-size:1.7cqw;font-weight:800}
.tsite .ts-pr{display:grid;grid-template-columns:repeat(6,1fr);gap:1.1cqw;margin:0 2.2cqw}
.tsite .ts-pr div{background:#fff;border-radius:.8cqw;padding:.8cqw 1cqw;display:flex;flex-direction:column;gap:.3cqw;box-shadow:0 .2cqw .6cqw rgba(0,0,0,.06)}
.tsite .ts-pr img{width:46%;align-self:center;aspect-ratio:1;object-fit:contain}
.tsite .ts-pr span{font-size:1cqw;font-weight:700;line-height:1.3;color:#3a4766;min-height:2.6cqw}
.tsite .ts-pr b{font-size:1.5cqw;font-weight:800;color:#EE2E24}
.tsite .ts-il{position:absolute;right:1.4cqw;top:.85cqw;background:rgba(27,57,110,.85);color:#fff;font-size:.95cqw;font-weight:700;padding:.3cqw .9cqw;border-radius:.4cqw}
@media (prefers-reduced-motion:reduce){.tcur,.trip,.tsite,.tsite .ts-pg{animation:none}}
</style>"""

CURSOR = ('<svg viewBox="0 0 24 24"><path d="M5 2.5v17.2l4.6-4.3 2.9 6.6 2.6-1.1-2.9-6.5h6.3z" fill="#fff" stroke="#111" '
          'stroke-width="1.4" stroke-linejoin="round"/></svg>')


def site():
    prods = ''.join(f'<div><img src="{uri("site-" + k + ".svg", "image/svg+xml")}" alt=""><span>{n}</span><b>{p}</b></div>' for k, n, p in PRODS)
    return (f'<span class="trip"></span><span class="tcur">{CURSOR}</span>'
            '<div class="tsite" aria-hidden="true"><div class="ts-bb"><i></i><i></i><i></i><b>tendaatacado.com.br</b></div><div class="ts-vw"><div class="ts-pg">'
            f'<div class="ts-hd"><img src="{LOGO}" alt=""><div class="ts-sr">O que você procura hoje?</div><div class="ts-ac">Entrar · Carrinho</div></div>'
            '<div class="ts-nv"><span>Ofertas de Verão</span><span>Bebidas</span><span>Carnes</span><span>Mercearia</span><span>Descartáveis</span><span>Limpeza</span></div>'
            f'<div class="ts-hero"><img src="{BANNER}" alt=""></div><div class="ts-h">Ofertas de verão</div><div class="ts-pr">{prods}</div>'
            '</div></div><span class="ts-il">Tela ilustrativa</span></div>')


def dellys(s):
    if 'alt="Dellys"' in s:
        return s
    i = s.index('<div class="clients">'); g = s.index('<div class="grid">', i)
    fim = s.index('<div class="sec-head"', g) if '<div class="sec-head"' in s[g:] else len(s)
    m = list(re.finditer(r'<div><img [^>]*></div>\n', s[g:fim]))[-1]
    j = g + m.end()
    s = s[:j] + f'<div><img src="{DELLYS}" alt="Dellys" style="max-height:36px"></div>\n' + s[j:]
    return re.sub(r'(\.clients \.grid\{flex:1;display:grid;grid-template-columns:repeat\()(\d+)', lambda m: m.group(1) + str(int(m.group(2)) + 1), s, count=1)


def painel(s):
    if '/*tenda-site*/' in s:
        return s
    i = s.index('<div class="panel">')
    j = s.index('</div></div>', s.index('<div class="bnr"', i)) + len('</div></div>')
    s = s[:j] + site() + s[j:]
    return s.replace('</body>', CSS + '</body>', 1) if '</body>' in s else s + CSS


def hero_tablet(s):
    """Tablet do topo (B2C): mostra o banner de verão (banner-confirmacao.png) em vez da página especial."""
    if 'alt="Banner de verão Tenda Atacado"' in s:
        return s
    i = s.index('alt="Tablet Goomer com a página especial')
    j = s.index('<div class="cy-scr"', i); k = s.index('>', j) + 1
    img = (f'<img src="{uri("banner-confirmacao.png", "image/png")}" alt="Banner de verão Tenda Atacado" '
           'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:3">')
    return s[:k] + img + s[k:]


def tela_especial(s):
    """Card "Página Especial" da jornada: mostra a tela de início do jogo (tela-jogo.jpg)."""
    if 'alt="Tela de início do Carrinho de Verão"' in s:
        return s
    h = s.index('alt="Banner de verão Tenda Atacado"')
    j = s.index('<div class="cy-scr"', h); k = s.index('>', j) + 1
    img = (f'<img src="{uri("tela-jogo.jpg", "image/jpeg")}" alt="Tela de início do Carrinho de Verão" '
           'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:3">')
    return s[:k] + img + s[k:]


for path in sys.argv[1:]:
    s = open(path, encoding='utf-8').read()
    s = tela_especial(hero_tablet(painel(dellys(s))))
    open(path, 'w', encoding='utf-8').write(s)
    print(path, 'ok')

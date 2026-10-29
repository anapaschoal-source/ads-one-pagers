"""Gera jota/jogo/index.html (Entrega Relâmpago, Mercado Livre) a partir de jogo.src.html.
Fontes Manrope e logo Goomer vêm de _modelo/ativacoes/roleta.html; logo do Mercado Livre de mercado-livre.(svg|png).
Uso (na raiz do repo): python3 _modelo/marcas/jota/build-jogo.py"""
import os, re, base64
d = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(d, '..', '..', '..'))
ref = open(os.path.join(root, '_modelo', 'ativacoes', 'roleta.html'), encoding='utf-8').read()
fonts = re.findall(r"src:url\('(data:font/woff2;base64,[^']+)'\)", ref)
svg = re.search(r'<svg class="goomer-logo".*?</svg>', ref, re.S).group(0)
for nome, mime in (('mercado-livre.svg', 'image/svg+xml'), ('mercado-livre.png', 'image/png')):
    p = os.path.join(d, nome)
    if os.path.exists(p):
        logo = f'data:{mime};base64,' + base64.b64encode(open(p, 'rb').read()).decode(); break
else:
    raise SystemExit('falta o logo oficial do Mercado Livre em ' + d)
s = open(os.path.join(d, 'jogo.src.html'), encoding='utf-8').read()
s = s.replace('__FONT700__', fonts[0]).replace('__FONT800__', fonts[1]).replace('__GOOMER_SVG__', svg).replace('__LOGO__', logo)
out = os.path.join(root, 'jota-ud03yuez', 'jogo', 'index.html')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(s)
print('ok:', out, len(s) // 1024, 'KB')

"""Gera tenda-atacado/jogo/index.html (Abasteça o Estoque, verão Tenda Atacado) a partir de jogo.src.html.
Fontes Manrope e logo Goomer vêm de _modelo/ativacoes/roleta.html; Baloo 2 de baloo-800.woff2; VERÃO e logo da pasta da marca.
Uso (na raiz do repo): python3 _modelo/marcas/tenda-atacado/build-jogo.py"""
import os, re, base64, io
from PIL import Image
d = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(d, '..', '..', '..'))
ref = open(os.path.join(root, '_modelo', 'ativacoes', 'roleta.html'), encoding='utf-8').read()
fonts = re.findall(r"src:url\('(data:font/woff2;base64,[^']+)'\)", ref)
svg = re.search(r'<svg class="goomer-logo".*?</svg>', ref, re.S).group(0)
def png(nome, w):
    i = Image.open(os.path.join(d, nome)).convert('RGBA'); i.thumbnail((w, w), Image.LANCZOS)
    b = io.BytesIO(); i.save(b, 'PNG', optimize=True); return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
baloo = 'data:font/woff2;base64,' + base64.b64encode(open(os.path.join(d, 'baloo-800.woff2'), 'rb').read()).decode()
s = open(os.path.join(d, 'jogo.src.html'), encoding='utf-8').read()
s = (s.replace('__FONT700__', fonts[0]).replace('__FONT800__', fonts[1]).replace('__BALOO__', baloo)
      .replace('__GOOMER_SVG__', svg).replace('__VERAO__', png('verao.png', 500)).replace('__LOGO__', png('logo.png', 300)))
out = os.path.join(root, 'tenda-atacado', 'jogo', 'index.html')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(s)
print('ok:', out, len(s) // 1024, 'KB')

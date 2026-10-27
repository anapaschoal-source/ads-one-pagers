"""Gera estrella-galicia/jogo/index.html a partir de jogo.src.html (fontes e logo Goomer vêm do jogo da Shopee).
Uso (na raiz do repo): python3 _modelo/marcas/estrella-galicia/build-jogo.py [caminho/do/jogo/da/shopee.html]"""
import sys, os, re, base64, subprocess
d = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(d, '..', '..', '..'))
ref = sys.argv[1] if len(sys.argv) > 1 else None
s_ref = open(ref, encoding='utf-8').read() if ref else subprocess.check_output(
    ['git', 'show', 'origin/shopee-rascunho:shopee/jogo/index.html'], cwd=root).decode()
fonts = re.findall(r"src:url\('(data:font/woff2;base64,[^']+)'\)", s_ref)
svg = re.search(r'<svg class="goomer-logo".*?</svg>', s_ref, re.S).group(0)
logo = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(d, 'logo.png'), 'rb').read()).decode()
s = open(os.path.join(d, 'jogo.src.html'), encoding='utf-8').read()
s = s.replace('__FONT700__', fonts[0]).replace('__FONT800__', fonts[1]).replace('__GOOMER_SVG__', svg).replace('__LOGO__', logo)
out = os.path.join(root, 'estrella-galicia', 'jogo', 'index.html')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(s)
print('ok:', out, len(s) // 1024, 'KB')

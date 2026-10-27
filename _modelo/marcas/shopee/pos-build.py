"""Pós-build da Shopee: troca a foto da Tela de Início pelo vídeo de 10s (diverge do modelo).
Uso: python3 _modelo/marcas/shopee/pos-build.py shopee/index.html [one-pager-shopee.html]"""
import sys, re, base64, os
d = os.path.dirname(os.path.abspath(__file__))
v = 'data:video/mp4;base64,' + base64.b64encode(open(os.path.join(d, 'video-inicio.mp4'), 'rb').read()).decode()
for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    s, n = re.subn(r'<div class="cy-ab cy-a1"([^>]*)><img class="cy-ph cy-kb" src="([^"]+)" alt="">',
                   lambda m: f'<div class="cy-ab"{m.group(1)}><video class="cy-ph" src="{v}" poster="{m.group(2)}" autoplay muted loop playsinline preload="auto"></video>', s, count=1)
    open(f, 'w', encoding='utf-8').write(s); print(f, 'vídeo' if n else 'NÃO ACHOU')

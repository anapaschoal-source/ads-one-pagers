"""Pós-build da Shopee (diverge do modelo): troca a foto da Tela de Início pelo vídeo de 10s
e inclui a Cyrela na faixa de anunciantes.
Uso: python3 _modelo/marcas/shopee/pos-build.py shopee/index.html [one-pager-shopee.html]"""
import sys, re, base64, os
d = os.path.dirname(os.path.abspath(__file__))
cy = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(d, 'cli-cyrela.png'), 'rb').read()).decode()
v = 'data:video/mp4;base64,' + base64.b64encode(open(os.path.join(d, 'video-inicio.mp4'), 'rb').read()).decode()
for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    s, n = re.subn(r'<div class="cy-ab cy-a1"([^>]*)><img class="cy-ph cy-kb" src="([^"]+)" alt="">',
                   lambda m: f'<div class="cy-ab"{m.group(1)}><video class="cy-ph" src="{v}" poster="{m.group(2)}" autoplay muted loop playsinline preload="auto"></video>', s, count=1)
    if 'alt="Cyrela"' not in s:
        s = s.replace('grid-template-columns:repeat(5,1fr)', 'grid-template-columns:repeat(6,1fr)', 1)
        s, k = re.subn(r'(<div class="clients">.*?<div class="grid">(?:\s*<div><img[^>]*></div>)+)', lambda m: m.group(1) + f'\n<div><img src="{cy}" alt="Cyrela" style="max-height:30px"></div>', s, count=1, flags=re.S)
        print(f, 'cyrela' if k else 'CYRELA NÃO ACHOU')
    if '/*shopee-hero*/' not in s:
        s = s.replace('</style>', '/*shopee-hero*/.hero h1{line-height:1.14}\n</style>', 1)
    open(f, 'w', encoding='utf-8').write(s); print(f, 'vídeo' if n else 'NÃO ACHOU')

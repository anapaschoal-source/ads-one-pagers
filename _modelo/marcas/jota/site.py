"""Prepara as páginas da Jota no site: copia o media kit (sem números por cidade) e liga o Vercel Web Analytics
(contagem de aberturas) no one-pager e no media kit. A senha fica no middleware.js da raiz.
Uso (na raiz do repo): python3 _modelo/marcas/jota/site.py <media-kit-gerado.html>"""
import os, sys, subprocess
D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(D, '..', '..', '..'))
SLUG = 'jota-ud03yuez'
TAG = '<script defer src="/_vercel/insights/script.js"></script>'

mk = open(sys.argv[1], encoding='utf-8').read()
if not mk.lstrip().lower().startswith('<!doctype'):
    mk = '<!doctype html>\n' + mk
dst = os.path.join(ROOT, SLUG, 'media-kit', 'index.html')
open(dst, 'w', encoding='utf-8').write(mk)
subprocess.run([sys.executable, os.path.join(ROOT, '_modelo', 'media-kit', 'sem_numeros.py'), dst], check=True)

for p in (os.path.join(ROOT, SLUG, 'index.html'), dst):
    s = open(p, encoding='utf-8').read()
    if TAG not in s:
        s = s.replace('</body>', TAG + '</body>', 1) if '</body>' in s else s + TAG
        open(p, 'w', encoding='utf-8').write(s)
    print('analytics ok:', os.path.relpath(p, ROOT))

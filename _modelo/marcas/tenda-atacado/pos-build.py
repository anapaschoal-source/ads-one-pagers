"""Pós-build do Tenda Atacado (diverge do modelo): só neste material, inclui a Dellys na faixa
"Marcas que já anunciam com a gente" (logo branco em cli-dellys.png).
Uso (na raiz do repo): python3 _modelo/marcas/tenda-atacado/pos-build.py tenda-atacado/index.html [/home/claude/one-pager-tenda-atacado.html]"""
import sys, os, re, base64
D = os.path.dirname(os.path.abspath(__file__))
src = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(D, 'cli-dellys.png'), 'rb').read()).decode()
for path in sys.argv[1:]:
    s = open(path, encoding='utf-8').read()
    if 'alt="Dellys"' in s:
        print(path, 'já tem Dellys'); continue
    i = s.index('<div class="clients">'); g = s.index('<div class="grid">', i)
    m = list(re.finditer(r'<div><img [^>]*></div>\n', s[g:s.index('<div class="sec-head"', g) if '<div class="sec-head"' in s[g:] else len(s)]))[-1]
    j = g + m.end()
    s = s[:j] + f'<div><img src="{src}" alt="Dellys" style="max-height:52px"></div>\n' + s[j:]
    s, n = re.subn(r'(\.clients \.grid\{flex:1;display:grid;grid-template-columns:repeat\()(\d+)', lambda m: m.group(1) + str(int(m.group(2)) + 1), s, count=1)
    open(path, 'w', encoding='utf-8').write(s)
    print(path, 'Dellys incluída', n)

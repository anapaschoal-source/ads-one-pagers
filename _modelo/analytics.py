#!/usr/bin/env python3
"""Liga o Vercel Web Analytics (visitantes e page views) em todas as páginas publicadas do hub.

Uso (na raiz do repo): python3 _modelo/analytics.py [--conferir]

- Procura todo .html fora de _modelo/ e .git/ e coloca a tag do Web Analytics antes do último </body>
  (ou no fim do arquivo). Não mexe em quem já tem a tag. Pode rodar sempre.
- Em página com senha (senha.py), a tag fica na tela de senha: conta quem abriu o link,
  mesmo antes de digitar a senha.
- --conferir: só lista as páginas sem a tag e sai com erro se houver alguma.
Rode antes de todo commit no hub (o publicar.py já roda sozinho).
"""
import os, sys

TAG = '<script defer src="/_vercel/insights/script.js"></script>'
RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def paginas():
    for d, subdirs, files in os.walk(RAIZ):
        rel = os.path.relpath(d, RAIZ)
        if rel.split(os.sep)[0] in ('.git', '_modelo', 'node_modules'):
            subdirs[:] = []
            continue
        for f in files:
            if f.endswith('.html'):
                yield os.path.join(d, f)


def ligar(p):
    s = open(p, encoding='utf-8').read()
    if '/_vercel/insights/script.js' in s:
        return False
    i = s.lower().rfind('</body>')
    s = s[:i] + TAG + s[i:] if i >= 0 else s + '\n' + TAG + '\n'
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(s)
    return True


if __name__ == '__main__':
    conferir = '--conferir' in sys.argv
    faltam, ligadas = [], 0
    for p in sorted(paginas()):
        rel = os.path.relpath(p, RAIZ)
        if conferir:
            if '/_vercel/insights/script.js' not in open(p, encoding='utf-8').read():
                faltam.append(rel)
        elif ligar(p):
            ligadas += 1
            print('analytics ligado:', rel)
    if conferir:
        print('sem analytics:', ', '.join(faltam) if faltam else 'nenhuma — OK')
        sys.exit(1 if faltam else 0)
    print(f'{ligadas} página(s) ligada(s); todas as páginas do hub contam visitantes e page views. OK')

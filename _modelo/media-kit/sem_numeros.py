#!/usr/bin/env python3
"""Tira do media kit os números por cidade e por restaurante antes de subir no site público.

Uso: python3 _modelo/media-kit/sem_numeros.py <arquivo.html> [<arquivo.html> ...]

- Card do ponto: remove "Potencial de impactos / mês" (B2C) e a contagem de restaurantes da cidade (B2B).
- Lista de cidades no zoom de estado/região: mantém os nomes, tira os números.
- Dados embutidos (_CD): apaga contas fechadas por restaurante e por cidade e a mediana.
Mantém: pontos do mapa, totais do Brasil, das regiões e dos estados.
Pode rodar mais de uma vez no mesmo arquivo.
"""
import json, re, sys

PIN_B2B = '`<p>Painel usado pelo dono no dia a dia.</p>`'

def limpar(s):
    n = 0
    # card do ponto
    s, k = re.subn(r"\$\{B2C\?(?:impTable\(c\[6\].*?c\[0\]\)|`<div class=\"pot\">.*?</div>`)\s*:\s*`<p>Painel usado pelo dono no dia a dia\. \$\{fmt\(inCity\)\} restaurantes Goomer nesta cidade\.</p>`\}",
                   "${B2C?'':" + PIN_B2B + "}", s, flags=re.S); n += k
    # lista de cidades
    s, k = re.subn(r"<span>\$\{fmt\(c\)\}</span>(</li>)", r"\1", s); n += k
    # dados
    m = re.search(r'const _CD = (\{.*?\});', s, re.S)
    if m:
        d = json.loads(m.group(1))
        d['med'] = 0
        d['rows'] = [r[:6] for r in d['rows']]
        s = s[:m.start(1)] + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]
        n += 1
    return s, n

def conferir(s):
    erros = []
    if 'Potencial de impactos' in s and "${B2C?''" not in s: erros.append('card do ponto ainda tem impactos')
    if '<span>${fmt(c)}</span></li>' in s: erros.append('lista de cidades ainda tem números')
    m = re.search(r'const _CD = (\{.*?\});', s, re.S)
    if m and any(len(r) > 6 for r in json.loads(m.group(1))['rows']): erros.append('_CD ainda tem contas fechadas')
    return erros

if __name__ == '__main__':
    ok = True
    for p in sys.argv[1:]:
        s = open(p, encoding='utf-8').read()
        s, n = limpar(s)
        e = conferir(s)
        open(p, 'w', encoding='utf-8').write(s)
        print(p, 'trocas:', n, 'OK' if not e else 'ERRO: ' + '; '.join(e))
        ok = ok and not e
    sys.exit(0 if ok else 1)

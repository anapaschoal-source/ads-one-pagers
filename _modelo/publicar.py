#!/usr/bin/env python3
"""Coloca um material no hub https://ads-one-pagers.vercel.app/ (index.html da raiz).

Uso (na raiz do repo, depois de gerar <slug>/index.html):
  python3 _modelo/publicar.py <slug> --marca "Nome" --setor varejo --desc "Frase curta." [--tipo "One page"|"Media kit"]

- Adiciona ou atualiza a linha da marca em MATERIAIS (mesmo url = atualiza).
- Gera a miniatura _hub/thumbs/<thumb>.webp (640x400) com um print do topo da página.
- Setores: financeiro, imobiliario, alimentos, varejo, automotivo, b2b, agencias
  (setor novo: passe --setor-nome "Nome do setor" junto).
Depois: git add, commit e push na main; a Vercel publica sozinha.
"""
import argparse, asyncio, io, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def js_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


async def thumb(page_path, out):
    from playwright.async_api import async_playwright
    from PIL import Image
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 675}, device_scale_factor=1)
        await pg.goto('file://' + page_path)
        await pg.wait_for_timeout(2500)
        png = await pg.screenshot()
        await b.close()
    im = Image.open(io.BytesIO(png)).convert('RGB').resize((640, 400), Image.LANCZOS)
    im.save(out, 'WEBP', quality=82)


def main():
    a = argparse.ArgumentParser()
    a.add_argument('slug')
    a.add_argument('--marca', required=True)
    a.add_argument('--setor', required=True)
    a.add_argument('--setor-nome')
    a.add_argument('--desc', required=True)
    a.add_argument('--tipo', default='One page')
    o = a.parse_args()

    sub = '' if o.tipo == 'One page' else 'media-kit/'
    url = f'/{o.slug}/{sub}'
    thumb_id = o.slug + ('' if o.tipo == 'One page' else '-media-kit')
    page = os.path.join(REPO, o.slug, sub, 'index.html')
    if not os.path.exists(page):
        sys.exit(f'não achei {page}')

    idx_path = os.path.join(REPO, 'index.html')
    s = open(idx_path, encoding='utf-8').read()

    if o.setor not in re.search(r'var SETORES = \{(.*?)\};', s, re.S).group(1):
        if not o.setor_nome:
            sys.exit(f'setor "{o.setor}" não existe no hub; passe --setor-nome')
        s = re.sub(r'(var SETORES = \{.*?)(\n\};)', lambda m: m.group(1).rstrip() + f",\n  {o.setor}: {js_str(o.setor_nome)}" + m.group(2), s, count=1, flags=re.S)

    linha = (f"  {{marca:{js_str(o.marca)}, tipo:{js_str(o.tipo)}, setor:{js_str(o.setor)}, "
             f"url:{js_str(url)}, thumb:{js_str(thumb_id)}, desc:{js_str(o.desc)}}}")
    m = re.search(r'var MATERIAIS = \[\n(.*?)\n\];', s, re.S)
    linhas = [l for l in m.group(1).split('\n') if l.strip()]
    linhas = [l.rstrip().rstrip(',') for l in linhas]
    achou = False
    for i, l in enumerate(linhas):
        if f"url:'{url}'" in l:
            linhas[i] = linha; achou = True
    if not achou:
        # entra junto das outras do mesmo setor
        pos = max([i for i, l in enumerate(linhas) if f"setor:'{o.setor}'" in l] or [len(linhas) - 1]) + 1
        linhas.insert(pos, linha)
    s = s[:m.start(1)] + ',\n'.join(linhas) + s[m.end(1):]
    open(idx_path, 'w', encoding='utf-8').write(s)

    os.makedirs(os.path.join(REPO, '_hub', 'thumbs'), exist_ok=True)
    asyncio.run(thumb(page, os.path.join(REPO, '_hub', 'thumbs', thumb_id + '.webp')))
    print(f"ok: hub {'atualizado' if achou else 'com material novo'} -> https://ads-one-pagers.vercel.app{url}")
    # todas as páginas do hub contam visitantes e page views (Vercel Web Analytics)
    import subprocess
    subprocess.run([sys.executable, os.path.join(REPO, '_modelo', 'analytics.py')], check=True)


if __name__ == '__main__':
    main()

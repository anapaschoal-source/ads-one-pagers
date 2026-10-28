#!/usr/bin/env python3
"""Gera um one-pager Goomer Ads a partir de um arquivo de marca (JSON).

Uso:
  python3 _modelo/build.py _modelo/marcas/<slug>.json            -> grava <slug>/index.html na raiz do repo
  python3 _modelo/build.py <arquivo>.json --artefato saida.html  -> também grava a versão para artefato do Claude

Caminhos de imagem no JSON são relativos ao próprio JSON. Campos ausentes caem nos
placeholders de _modelo/placeholder/. Ver _modelo/marcas/modelo.json como referência.
"""
import base64, io, json, mimetypes, os, re, sys, html
from urllib.parse import quote
from jinja2 import Environment, FileSystemLoader
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BASE = os.path.join(HERE, 'base')
PH = os.path.join(HERE, 'placeholder')


def data_uri(path, max_w=None):
    ext = os.path.splitext(path)[1].lower()
    if max_w and ext in ('.jpg', '.jpeg', '.png', '.webp'):
        im = Image.open(path)
        if im.width > max_w or ext != '.jpg':
            has_alpha = im.mode in ('RGBA', 'LA', 'P')
            if im.width > max_w:
                im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
            buf = io.BytesIO()
            if has_alpha and ext == '.png':
                im.save(buf, 'PNG', optimize=True); mime = 'image/png'
            else:
                im.convert('RGB').save(buf, 'JPEG', quality=84); mime = 'image/jpeg'
            return f'data:{mime};base64,' + base64.b64encode(buf.getvalue()).decode()
    mime = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    if ext == '.svg': mime = 'image/svg+xml'
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def lum(hexc):
    h = hexc.lstrip('#'); r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def texto_sobre(hexc):
    return '#0A0044' if lum(hexc) > 0.42 else '#FFFFFF'


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(1)
    cfg_path = os.path.abspath(args[0]); cdir = os.path.dirname(cfg_path)
    art_out = args[args.index('--artefato') + 1] if '--artefato' in args else None
    c = json.load(open(cfg_path, encoding='utf-8'))

    def asset(key, default, max_w=1200):
        p = c.get('imagens', {}).get(key)
        p = os.path.join(cdir, p) if p else default
        return data_uri(p, max_w)

    marca = c['marca']
    cor = c.get('cor', '#FA2F93')
    b2b = c.get('b2b')
    cor_b2b = (b2b or {}).get('cor', cor)
    img = {
        'goomer': data_uri(os.path.join(BASE, 'goomer.svg')),
        'logo': asset('logo', os.path.join(PH, 'logo.svg'), 600),
        'tablet': data_uri(os.path.join(BASE, 'tablet-frame.png')),
        'hero_b2c': data_uri(os.path.join(BASE, 'hero-b2c.jpg')),
        'hero_b2b': data_uri(os.path.join(BASE, 'hero-b2b.jpg')),
        'painel': data_uri(os.path.join(BASE, 'painel-b2b.png'), 1360),
        'fmt1': data_uri(os.path.join(BASE, 'fmt1-inicio.jpg')),
        'fmt2': data_uri(os.path.join(BASE, 'fmt2-confirmacao.jpg')),
        'fmt3': data_uri(os.path.join(BASE, 'fmt3-conta.jpg')),
        'fmt4': data_uri(os.path.join(BASE, 'fmt4-especial.jpg')),
    }
    for k in ('inicio', 'confirmacao', 'conta', 'especial'):
        img['foto_' + k] = asset('foto_' + k, os.path.join(PH, f'foto-{k}.jpg'), 900)

    clientes = [
        {'src': data_uri(os.path.join(BASE, f)), 'alt': a, 'h': h}
        for f, a, h in [('cli-uber.png', 'Uber', 30), ('cli-pg.png', 'P&amp;G', 38), ('cli-cocacola.png', 'Coca-Cola', 36),
                        ('cli-cielo.png', 'Cielo', 30), ('cli-comgas.png', 'Comgás', 28), ('cli-cyrela.png', 'Cyrela', 30)]
        if a.replace('&amp;', '&') not in c.get('ocultar_clientes', [])
    ]

    f = c['formatos']; e = f['especial']
    tela_especial = (
        '<div style="position:absolute;inset:0;background:radial-gradient(70% 90% at 92% 0%,color-mix(in srgb,var(--cor) 45%,transparent) 0%,transparent 62%),var(--escura)"></div>'
        f'<div style="position:absolute;right:0;top:0;bottom:0;width:46%"><img class="cy-ph cy-kb" src="{img["foto_especial"]}" alt="">'
        '<div style="position:absolute;inset:0;background:linear-gradient(90deg,var(--escura) 0%,transparent 45%)"></div></div>'
        '<div style="position:absolute;left:5cqw;top:0;bottom:0;width:54cqw;display:flex;flex-direction:column;justify-content:center;gap:2.4cqh;color:#fff">'
        f'<div><span style="display:inline-block;border:.3cqw solid color-mix(in srgb,var(--cor) 60%,transparent);color:var(--cor);border-radius:9cqw;padding:.8cqw 2cqw;font-size:1.7cqw;font-weight:700;letter-spacing:.1em;text-transform:uppercase;line-height:1.3">{e["selo"]}</span></div>'
        f'<div style="font-weight:700;font-size:5.6cqw;line-height:1.08">{e["titulo"]} <span style="color:var(--cor)">{e["titulo_destaque"]}</span></div>'
        f'<div style="font-size:2cqw;opacity:.85;line-height:1.45">{e["texto"]}</div>'
        f'<div><span style="position:relative;display:inline-block;background:var(--cor);color:{texto_sobre(cor)};font-weight:700;font-size:2.1cqw;padding:1.7cqw 4.2cqw;border-radius:9cqw">{e["botao"]}<span class="cy-tap"></span></span></div>'
        '</div>'
    )

    banner = ''
    if b2b:
        bn = b2b.get('banner', {})
        if bn.get('imagem'):
            banner = f'<img class="full" src="{data_uri(os.path.join(cdir, bn["imagem"]), 1400)}" alt="">'
        else:
            banner = (f'<img class="lg" src="{img["logo"]}" alt=""><div class="tx"><div class="ey">{bn.get("selo", marca + " para empresas")}</div>'
                      f'<div class="hd">{bn["titulo"]}</div><div class="ct">{bn["cta"]} →</div></div>')

    label = c.get('menu', {}).get('label', marca).upper()
    ctx = dict(
        titulo_pagina=f'Goomer Ads para {marca}', marca=marca, cor=cor, cor_escura=c.get('cor_escura', '#09090B'),
        cor_b2b=cor_b2b, cor_texto=texto_sobre(cor), cor_b2b_texto=texto_sobre(cor_b2b),
        logo_branco=c.get('logo_branco_no_escuro', True),
        logo_altura_hero=c.get('logo_altura_hero', 22), logo_altura_secao=c.get('logo_altura_secao', 26),
        menu_label=label, menu_sub=c.get('menu', {}).get('sub', 'Especial'),
        menu_logo=(data_uri(os.path.join(cdir, c['menu']['logo']), 300) if c.get('menu', {}).get('logo') else None),
        menu_fs=round(min(15, 62 / max(len(label), 1) * 1.0), 2),
        hero=c['hero'], f=f, ativacao=c['ativacao'], b2b=b2b, demo_url=c.get('demo_url'),
        fonte_data=c.get('fonte_data', 'out/2026'), img=img, clientes=clientes,
        tela_especial=tela_especial, banner=banner,
        cta={**{'titulo': f'Vamos levar a {marca} pra mesa?', 'nome': 'João Arcalá', 'cargo': 'CFO/COO · Goomer',
                'email': 'joao.arcala@goomer.com.br', 'whatsapp': '5515991378552', 'telefone': '+55 15 99137-8552'},
             **c.get('cta', {})},
    )
    ctx['cta']['assunto'] = quote(f'Goomer Ads × {marca}')
    env = Environment(loader=FileSystemLoader(HERE), autoescape=False, trim_blocks=False)
    out = env.get_template('template.html.j2').render(**ctx)

    slug = c['slug']
    dest = os.path.join(REPO, slug, 'index.html')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w', encoding='utf-8').write(out)
    print(f'ok: {dest} ({len(out)//1024} KB)')

    if art_out:
        a = out
        # demo relativo ao site não abre no artefato: embute o HTML local se existir, senão tela estática
        du = c.get('demo_url') or ''
        if du.startswith('/'):
            local = os.path.join(REPO, du.strip('/'), 'index.html')
            if os.path.exists(local):
                a = a.replace(f'<iframe src="{du}"', '<iframe srcdoc="' + html.escape(open(local, encoding='utf-8').read(), quote=True) + '"')
        a = re.sub(r'^<!doctype html>\s*<html[^>]*>\s*<head>\s*<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', '', a)
        a = a.replace('</head>\n<body data-tab="b2c">', '<body data-tab="b2c">', 1)
        a = re.sub(r'</html>\s*$', '', a)
        open(art_out, 'w', encoding='utf-8').write(a)
        print(f'ok: {art_out}')


if __name__ == '__main__':
    main()

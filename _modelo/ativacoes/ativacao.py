#!/usr/bin/env python3
"""Gera a ativação (Página Especial do tablet) de uma marca a partir de um modelo + JSON.

Uso:
  python3 ativacao.py roleta marca.json saida.html
  python3 ativacao.py quiz   marca.json saida.html

- O modelo (roleta.html / quiz.html, nesta pasta) já funciona sozinho com a config neutra.
  Este script só troca o bloco entre /*CFG*/ e /*FIM-CFG*/ pela config da marca.
- No JSON, qualquer valor de texto que seja caminho de imagem existente (relativo ao JSON)
  vira data URI (logo, foto, cartao.foto...).
- QR code: em vez de imagem, use {"qr_url": "https://..."} no lugar da chave "qr";
  o script gera o SVG (pip install segno).
- Ver roleta.exemplo.json e quiz.exemplo.json para todos os campos.
"""
import base64, io, json, mimetypes, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def data_uri(path, max_w=1000):
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.jpg', '.jpeg', '.png', '.webp'):
        from PIL import Image
        im = Image.open(path)
        alpha = im.mode in ('RGBA', 'LA', 'P')
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        if alpha:
            im.convert('RGBA').save(buf, 'PNG', optimize=True); mime = 'image/png'
        else:
            im.convert('RGB').save(buf, 'JPEG', quality=84); mime = 'image/jpeg'
        return f'data:{mime};base64,' + base64.b64encode(buf.getvalue()).decode()
    mime = 'image/svg+xml' if ext == '.svg' else (mimetypes.guess_type(path)[0] or 'application/octet-stream')
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def qr_uri(url):
    import segno
    buf = io.BytesIO()
    segno.make(url, error='m').save(buf, kind='svg', scale=10, border=1, dark='#111111', xmldecl=False, svgns=True)
    return 'data:image/svg+xml;base64,' + base64.b64encode(buf.getvalue()).decode()


def resolve(v, cdir):
    if isinstance(v, dict):
        out = {}
        for k, x in v.items():
            if k == 'qr_url':
                if x:
                    out['qr'] = qr_uri(x)
            else:
                out[k] = resolve(x, cdir)
        return out
    if isinstance(v, list):
        return [resolve(x, cdir) for x in v]
    if isinstance(v, str) and re.search(r'\.(png|jpe?g|webp|svg)$', v, re.I):
        p = os.path.join(cdir, v)
        if os.path.exists(p):
            return data_uri(p)
    return v


def main():
    if len(sys.argv) != 4:
        print(__doc__); sys.exit(1)
    tipo, cfg_path, out = sys.argv[1:]
    tpl = open(os.path.join(HERE, f'{tipo}.html'), encoding='utf-8').read()
    cfg = resolve(json.load(open(cfg_path, encoding='utf-8')), os.path.dirname(os.path.abspath(cfg_path)))
    blob = json.dumps(cfg, ensure_ascii=False, indent=1).replace('</', '<\\/')
    new, n = re.subn(r'/\*CFG\*/.*?/\*FIM-CFG\*/', lambda m: '/*CFG*/\nvar CFG = ' + blob + ';\n/*FIM-CFG*/', tpl, count=1, flags=re.S)
    if n != 1:
        sys.exit('marcadores /*CFG*/ ... /*FIM-CFG*/ não encontrados no modelo')
    new = re.sub(r'<title>[^<]*</title>', f'<title>{cfg.get("titulo_aba") or tipo.capitalize() + " " + cfg["marca"]} • Goomer Games</title>', new, count=1)
    open(out, 'w', encoding='utf-8').write(new)
    print(f'ok: {out} ({len(new)//1024} KB)')


if __name__ == '__main__':
    main()

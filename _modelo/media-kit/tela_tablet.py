#!/usr/bin/env python3
"""Coloca a tela de abertura de uma ativação no tablet da foto da mesa ("Por que Goomer Ads") do media kit.

Uso: python3 _modelo/media-kit/tela_tablet.py <kit.html> <tela.png|ativacao.html> [<saida.html>]

- <tela>: print 1280x800 da tela de abertura da ativação, ou o HTML da ativação (o script abre em
  1280x800 no Chromium e tira o print sozinho, sem rede).
- Sem <saida.html>, grava por cima do <kit.html>.
- A foto fica em 1280x960 (2x da original) e a tela entra com perspectiva, um leve escurecimento e
  reflexo para parecer fotografada. Pode rodar de novo: a tela inteira é sobrescrita.
Rode no HTML aberto (antes do senha.py).
"""
import base64, io, os, re, sys, tempfile
import numpy as np
import cv2
from PIL import Image, ImageFilter

# cantos da tela (área de exibição, dentro da moldura) na foto original 640x480: TL, TR, BR, BL
QUAD = [(380, 284), (569, 310), (544, 433), (359.5, 403)]
BASE_W = 640
ANCORA = re.compile(r'(<figure class="mesa-foto" id="mesaFoto"><img src=")(data:image/[a-z]+;base64,[^"]+)(")')


def print_html(path):
    from playwright.sync_api import sync_playwright
    out = tempfile.mktemp(suffix='.png')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1280, 'height': 800})
        pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith(('file:', 'data:')) else r.abort())
        pg.goto('file://' + os.path.abspath(path)); pg.wait_for_timeout(2500)
        pg.screenshot(path=out); b.close()
    return out


def compor(foto: Image.Image, tela: Image.Image) -> Image.Image:
    foto = foto.convert('RGB')
    if foto.width < 1000:
        foto = foto.resize((foto.width * 2, foto.height * 2), Image.LANCZOS)
    k = foto.width / BASE_W
    dst = np.float32([(x * k, y * k) for x, y in QUAD])
    tela = tela.convert('RGB').resize((1280, 800), Image.LANCZOS)
    # escurece um pouco e tira contraste: tela fotografada, não colada
    arr = np.asarray(tela).astype(np.float32)
    arr = arr * 0.86 + 10
    # reflexo suave em diagonal
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    glare = np.clip(1 - np.abs((xx / w) * 0.9 + (yy / h) * 0.6 - 0.55) / 0.35, 0, 1) ** 2 * 26
    arr = np.clip(arr + glare[..., None], 0, 255).astype(np.uint8)
    src = np.float32([(0, 0), (w, 0), (w, h), (0, h)])
    M = cv2.getPerspectiveTransform(src, dst)
    W, H = foto.size
    warped = cv2.warpPerspective(arr, M, (W, H), flags=cv2.INTER_AREA)
    mask = cv2.warpPerspective(np.full((h, w), 255, np.uint8), M, (W, H), flags=cv2.INTER_LINEAR)
    warped = Image.fromarray(warped).filter(ImageFilter.GaussianBlur(0.6))
    mask = Image.fromarray(mask).filter(ImageFilter.GaussianBlur(0.8))
    out = foto.copy(); out.paste(warped, (0, 0), mask)
    return out


def main():
    kit, tela = sys.argv[1], sys.argv[2]
    saida = sys.argv[3] if len(sys.argv) > 3 else kit
    s = open(kit, encoding='utf-8').read()
    m = ANCORA.search(s)
    if not m:
        sys.exit('não achei a foto da mesa (figure#mesaFoto) no kit')
    if tela.lower().endswith(('.html', '.htm')):
        tela = print_html(tela)
    foto = Image.open(io.BytesIO(base64.b64decode(m.group(2).split(',', 1)[1])))
    out = compor(foto, Image.open(tela))
    b = io.BytesIO(); out.save(b, 'WEBP', quality=84)
    uri = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    s = s[:m.start(2)] + uri + s[m.end(2):]
    with open(saida, 'w', encoding='utf-8') as fh:
        fh.write(s)
    print(saida, f'foto {out.size[0]}x{out.size[1]}', 'OK')


if __name__ == '__main__':
    main()

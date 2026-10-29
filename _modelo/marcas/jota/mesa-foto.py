"""Coloca o print da Tela de Início (Mercado Livre, layout do tablet Goomer) na tela do tablet da foto "mesa" do media kit.
Uso: python3 _modelo/marcas/jota/mesa-foto.py <foto-original.png> <saida.webp>"""
import sys, os
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
D = os.path.dirname(os.path.abspath(__file__))
K = 2  # trabalha em 2x para o print ficar nítido
foto = Image.open(sys.argv[1]).convert('RGB')
foto = foto.resize((foto.width * K, foto.height * K), Image.LANCZOS)
quad = [(377, 285), (571, 312), (560, 436), (361, 400)]  # cantos da tela na foto original (TL, TR, BR, BL)
quad = [(x * K, y * K) for x, y in quad]
src = Image.open(os.path.join(D, 'tela-inicio-ml.png')).convert('RGB')  # print da Tela de Início no layout do tablet Goomer
w, h = src.size

def coeffs(dst, srcpts):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, srcpts):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()

c = coeffs(quad, [(0, 0), (w, 0), (w, h), (0, h)])
src = ImageEnhance.Brightness(src).enhance(.93)
warped = src.transform(foto.size, Image.PERSPECTIVE, c, Image.BICUBIC)
mask = Image.new('L', foto.size, 0); ImageDraw.Draw(mask).polygon(quad, fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(.8))
foto.paste(warped, (0, 0), mask)
# brilho suave da tela, como no original
gl = Image.new('L', foto.size, 0); gd = ImageDraw.Draw(gl)
gd.polygon([quad[0], ((quad[0][0] + quad[1][0]) / 2, (quad[0][1] + quad[1][1]) / 2), ((quad[0][0] + quad[3][0]) / 2, (quad[0][1] + quad[3][1]) / 2)], fill=28)
gl = gl.filter(ImageFilter.GaussianBlur(20))
foto = Image.composite(Image.new('RGB', foto.size, 'white'), foto, gl)
foto.save(sys.argv[2], 'WEBP', quality=88)
print('ok', sys.argv[2], foto.size)

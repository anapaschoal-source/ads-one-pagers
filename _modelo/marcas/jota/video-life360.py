"""Gera o vídeo ilustrativo de 10s da Life360 (Tela de Início do media kit da Jota): life360-inicio.webm e .mp4.
Uso: python3 _modelo/marcas/jota/video-life360.py"""
import os, subprocess, tempfile, math
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, N = 1280, 720, 25, 250
F = lambda s: ImageFont.truetype(os.path.expanduser('~/.fonts/manrope-latin-800-normal.ttf'), s)
P, P2, DK = (122, 118, 236), (84, 80, 201), (20, 19, 46)
logo = Image.open(os.path.join(D, 'life360.png')).convert('RGBA')
white = logo.copy(); white.putdata([(255, 255, 255, a) for *_, a in logo.get_flattened_data()])
foto = Image.open(os.path.join(D, 'foto-life360.jpg')).convert('RGB')
def fit(i, h):
    i = i.copy(); i.thumbnail((10000, h), Image.LANCZOS); return i
lw = fit(white, 70); lb = fit(white, 120)
pins = [(0.30, 0.42), (0.62, 0.66), (0.86, 0.33), (0.13, 0.72)]
def pin(dr, x, y, s, c):
    dr.ellipse((x - s, y - 2 * s, x + s, y), fill=c); dr.polygon([(x - s * .7, y - s * .7), (x + s * .7, y - s * .7), (x, y + s * .6)], fill=c)
    dr.ellipse((x - s * .45, y - 1.45 * s, x + s * .45, y - .55 * s), fill='white')
tmp = tempfile.mkdtemp()
for n in range(N):
    t = n / FPS
    if t < 7:
        z = 1 + 0.06 * t / 7
        fr = foto.resize((int(W * z), int(W * z * foto.height / foto.width)))
        fr = fr.crop(((fr.width - W) // 2, (fr.height - H) // 2, (fr.width - W) // 2 + W, (fr.height - H) // 2 + H)).convert('RGBA')
        dr = ImageDraw.Draw(fr)
        for i, (px, py) in enumerate(pins):
            k = min(1, max(0, (t - 0.6 - i * 0.6) / 0.35))
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.rounded_rectangle((48, H - 220, 760, H - 48), 28, fill=(*DK, 225))
        fr.alpha_composite(ov); dr = ImageDraw.Draw(fr)
        fr.alpha_composite(lw, (80, H - 196))
        msg = 'Sua família no mesmo mapa' if t < 3.6 else 'Avisos de chegada e saída'
        dr.text((80, H - 110), msg, font=F(46), fill='white')
    else:
        k = min(1, (t - 7) / 0.4)
        fr = Image.new('RGBA', (W, H), P); dr = ImageDraw.Draw(fr)
        fr.alpha_composite(lb, ((W - lb.width) // 2, 200))
        for txt, y, sz in (('Baixe grátis e teste o premium', 380, 50),):
            tw = dr.textlength(txt, font=F(sz)); dr.text(((W - tw) / 2, y), txt, font=F(sz), fill=(255, 255, 255, int(255 * k)))
        bw = 300; dr.rounded_rectangle(((W - bw) / 2, 480, (W + bw) / 2, 552), 36, fill='white')
        tw = dr.textlength('Life360.com', font=F(30)); dr.text(((W - tw) / 2, 494), 'Life360.com', font=F(30), fill=P2)
    fr.convert('RGB').save(f'{tmp}/f{n:04d}.png')
src = f'{tmp}/f%04d.png'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', src, '-c:v', 'libvpx-vp9', '-crf', '36', '-b:v', '0', '-pix_fmt', 'yuv420p', '-an', os.path.join(D, 'life360-inicio.webm')], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', src, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '25', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', os.path.join(D, 'life360-inicio.mp4')], check=True)
print('ok', [os.path.getsize(os.path.join(D, f)) // 1024 for f in ('life360-inicio.webm', 'life360-inicio.mp4')], 'KB')

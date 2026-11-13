"""Gera os vídeos ilustrativos de 10s da Tela de Início para as marcas da Jota (Mercado Livre, Life360, Sicredi):
<k>-inicio.webm e <k>-inicio.mp4, além de foto-sicredi.jpg.
Uso: python3 _modelo/marcas/jota/video-marcas.py"""
import os, subprocess, tempfile, shutil
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, N = 1280, 720, 25, 250
F = lambda s: ImageFont.truetype(os.path.expanduser('~/.fonts/manrope-latin-800-normal.ttf'), s)


def logo(nome, branco=False):
    i = Image.open(os.path.join(D, nome)).convert('RGBA'); i = i.crop(i.getchannel('A').getbbox())
    if branco:
        i.putdata([(255, 255, 255, a) for *_, a in i.get_flattened_data()])
    return i


def fit(i, h):
    i = i.copy(); i.thumbnail((10000, h), Image.LANCZOS); return i


def foto_sicredi():
    im = Image.new('RGB', (1200, 800), '#E2F4DD'); d = ImageDraw.Draw(im)
    d.ellipse((640, 120, 1180, 660), fill='#CDEBC4')
    d.rounded_rectangle((520, 260, 940, 520), 28, fill='#0F6A2D')
    d.rounded_rectangle((560, 300, 640, 360), 10, fill='#E8C55A')
    d.text((560, 440), '•••• 4417', font=F(34), fill='#E2F4DD')
    d.rounded_rectangle((700, 420, 1080, 640), 28, fill='#40B93C')
    d.rounded_rectangle((740, 460, 820, 520), 10, fill='#E8C55A')
    for x, y in ((380, 520), (430, 560), (330, 600)):
        d.ellipse((x - 46, y - 46, x + 46, y + 46), fill='#E8C55A'); d.ellipse((x - 30, y - 30, x + 30, y + 30), outline='#C9A43C', width=6)
    im.save(os.path.join(D, 'foto-sicredi.jpg'), quality=88)


def foto_mackenzie():
    """Ilustração para o vídeo do Colégio Mackenzie (prédio histórico com colunas, céu e árvores)."""
    im = Image.new('RGB', (1200, 800), '#F3E9DD'); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1200, 520), fill='#CFE3F2')
    for x, r in ((90, 120), (1120, 140), (240, 90)):
        d.ellipse((x - r, 430 - r, x + r, 430 + r), fill='#7FA86B')
    d.rectangle((300, 250, 900, 620), fill='#C9302C')
    d.polygon([(280, 255), (600, 120), (920, 255)], fill='#A8231F')
    for i in range(6):
        x = 340 + i * 100; d.rectangle((x, 290, x + 36, 600), fill='#F6EFE6')
    for i in range(5):
        x = 392 + i * 100; d.rectangle((x, 330, x + 44, 410), fill='#5B2A23'); d.rectangle((x, 450, x + 44, 530), fill='#5B2A23')
    d.rectangle((560, 520, 640, 620), fill='#5B2A23')
    d.rectangle((260, 600, 940, 640), fill='#E6D8C6'); d.rectangle((0, 640, 1200, 800), fill='#B9C9A2')
    im.save(os.path.join(D, 'foto-mackenzie.jpg'), quality=88)


MARCAS = {
    'ml': dict(foto='foto-inicio.jpg', logo='mercado-livre.png', branco_painel=False, painel=(255, 255, 255, 240), painel_txt=(45, 50, 119), fim_logo_branco=False,
               msgs=('Tudo o que você procura', 'Chega rapidinho na sua casa'), fim='Baixe o app e aproveite',
               pill='mercadolivre.com.br', cor=(255, 230, 0), tinta=(45, 50, 119), pill_txt=(45, 50, 119), pill_bg=(255, 255, 255)),
    'l360': dict(foto='foto-life360.jpg', logo='life360.png', branco_painel=True, fim_logo_branco=True,
                 msgs=('Sua família no mesmo mapa', 'Avisos de chegada e saída'), fim='Baixe grátis e teste o premium',
                 pill='life360.com', cor=(122, 118, 236), tinta=(255, 255, 255), pill_txt=(84, 80, 201), pill_bg=(255, 255, 255)),
    'mack': dict(foto='foto-mackenzie.jpg', logo='mackenzie.png', branco_painel=False, fim_logo_branco=True, painel=(255, 255, 255, 240), painel_txt=(165, 25, 30),
                 msgs=('Formação e valores\nde mãos dadas', 'Da Educação Infantil\nao Ensino Médio'), fim='Agende sua visita',
                 pill='mackenzie.br', cor=(196, 22, 28), tinta=(255, 255, 255), pill_txt=(165, 25, 30), pill_bg=(255, 255, 255)),
    'sic': dict(foto='foto-sicredi.jpg', logo='sicredi.png', branco_painel=True, fim_logo_branco=True,
                msgs=('Conta, cartão e investimentos', 'Juntos, a gente cresce'), fim='Abra sua conta pelo app',
                pill='sicredi.com.br', cor=(15, 106, 45), tinta=(255, 255, 255), pill_txt=(15, 106, 45), pill_bg=(255, 255, 255)),
}


def video_mack(k, m):
    """Mackenzie: fundo vermelho, foto oficial (criativo do colégio) à direita, logo e frases à esquerda."""
    foto = Image.open(os.path.join(D, m['foto'])).convert('RGB')
    lw = fit(logo(m['logo'], True), 96)
    tmp = tempfile.mkdtemp()
    for n in range(N):
        t = n / FPS
        fr = Image.new('RGBA', (W, H), m['cor']); dr = ImageDraw.Draw(fr)
        z = 1 + 0.05 * t / 10
        ph = foto.resize((int(H * foto.width / foto.height * z), int(H * z)))
        fr.paste(ph.crop((0, (ph.height - H) // 2, min(ph.width, W), (ph.height - H) // 2 + H)), (W - ph.width + (ph.width - min(ph.width, W)), 0))
        fr.alpha_composite(lw, (80, 110))
        if t < 7:
            txt = m['msgs'][0] if t < 3.6 else m['msgs'][1]
            y = 330
            for ln in txt.split('\n'):
                dr.text((80, y), ln, font=F(54), fill=(255, 255, 255)); y += 68
        else:
            k2 = min(1, (t - 7) / 0.4)
            dr.text((80, 330), m['fim'], font=F(58), fill=(255, 255, 255, int(255 * k2)))
            pw = int(dr.textlength(m['pill'], font=F(30))) + 80
            dr.rounded_rectangle((80, 440, 80 + pw, 512), 36, fill=m['pill_bg'])
            dr.text((120, 454), m['pill'], font=F(30), fill=m['pill_txt'])
        fr.convert('RGB').save(f'{tmp}/f{n:04d}.png')
    return tmp


def video(k, m):
    if k == 'mack':
        tmp = video_mack(k, m); return enc(k, tmp)
    foto = Image.open(os.path.join(D, m['foto'])).convert('RGB')
    lw = fit(logo(m['logo'], m['branco_painel']), 64)
    lb = fit(logo(m['logo'], m['fim_logo_branco']), 120)
    tmp = tempfile.mkdtemp()
    for n in range(N):
        t = n / FPS
        if t < 7:
            z = 1 + 0.06 * t / 7
            fr = foto.resize((int(W * z), int(W * z * foto.height / foto.width)))
            fr = fr.crop(((fr.width - W) // 2, (fr.height - H) // 2, (fr.width - W) // 2 + W, (fr.height - H) // 2 + H)).convert('RGBA')
            ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            od.rounded_rectangle((48, H - 220, 820, H - 48), 28, fill=m.get('painel', (20, 19, 46, 225)))
            fr.alpha_composite(ov); dr = ImageDraw.Draw(fr)
            fr.alpha_composite(lw, (80, H - 198))
            dr.text((80, H - 110), m['msgs'][0] if t < 3.6 else m['msgs'][1], font=F(44), fill=m.get('painel_txt', (255, 255, 255)))
        else:
            k2 = min(1, (t - 7) / 0.4)
            fr = Image.new('RGBA', (W, H), m['cor']); dr = ImageDraw.Draw(fr)
            fr.alpha_composite(lb, ((W - lb.width) // 2, 190))
            tw = dr.textlength(m['fim'], font=F(50)); dr.text(((W - tw) / 2, 380), m['fim'], font=F(50), fill=(*m['tinta'], int(255 * k2)))
            pw = max(300, int(dr.textlength(m['pill'], font=F(30))) + 80)
            dr.rounded_rectangle(((W - pw) / 2, 480, (W + pw) / 2, 552), 36, fill=m['pill_bg'])
            tw = dr.textlength(m['pill'], font=F(30)); dr.text(((W - tw) / 2, 494), m['pill'], font=F(30), fill=m['pill_txt'])
        fr.convert('RGB').save(f'{tmp}/f{n:04d}.png')
    enc(k, tmp)


def enc(k, tmp):
    src = f'{tmp}/f%04d.png'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', src, '-c:v', 'libvpx-vp9', '-crf', '36', '-b:v', '0',
                    '-pix_fmt', 'yuv420p', '-an', os.path.join(D, f'{k}-inicio.webm')], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', src, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '25',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', os.path.join(D, f'{k}-inicio.mp4')], check=True)
    shutil.rmtree(tmp)
    print(k, 'ok')


import sys
foto_sicredi()
for k, m in MARCAS.items():
    if len(sys.argv) < 2 or k in sys.argv[1:]:
        video(k, m)

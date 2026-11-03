#!/usr/bin/env python3
"""Transforma o media kit aberto na versão **Compartilhar** (a que vai para o cliente).

Uso: python3 _modelo/media-kit/compartilhar.py <arquivo.html> [<arquivo.html> ...]

1. Tira os números por cidade e por restaurante (mesmo que sem_numeros.py).
2. Mapa fixo, como no kit da Jota: Brasil inteiro com os pontos e os números gerais
   (+2 mil restaurantes, +50 mil telas, +300 cidades, +5 M pessoas), sem filtros, sem
   culinária, sem zoom e sem clique; texto alinhado à margem das outras seções, em
   duas linhas no título, e o mapa deslocado para a direita.
3. Sem o pop-up "Conheça a Goomer" ao abrir.
4. "Por que Goomer Ads": texto em cima, em largura total, com o destaque de mídia inovadora
   (primeiro formato na mesa), e logo abaixo os formatos um por um (mockup + descrição), no
   lugar da foto da mesa. A seção "Formatos" fica só para o modo B2B.
Pode rodar mais de uma vez. Rode no HTML aberto, antes do senha.py.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sem_numeros import limpar, conferir

MARCA = '/*mk-compartilhar-mapa*/'
MAPCSS = '<style>' + MARCA + '''
#mapa .filters,#mapa #hint,#mapa .zoomctl,#mapa .pin,#mapa .tip,#mapa #fxBtn{display:none!important}
#mapa #svg,#mapa #stage{pointer-events:none}
@media (min-width:981px){
 #mapa .story{left:max(var(--gutter),calc((100% - min(94vw,calc((100svh - 60px) * 2.15))) / 2));width:min(600px,44vw);top:clamp(20px,4vh,48px)}
 #mapa .story h1{font-size:clamp(44px,4.6vw,68px)}
 #mapa .story .lead{max-width:52ch}
 #mapa .story .kpis{grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 32px;max-width:520px}
 #mapa .story .kpi b{font-size:clamp(52px,5vw,76px)}
 #mapa .story .kpi span{font-size:15px}
 #mapa #svg,#mapa #dots{transform:translateX(clamp(120px,17vw,260px))}
}
</style>'''

MARCA2 = '/*mk-compartilhar-formatos*/'
DESTAQUE = ('<p class="mkc-dif"><b>Mídia inovadora</b><span>Somos o primeiro formato de mídia na mesa do '
            'restaurante: um diferencial que só a Goomer Ads entrega, no momento em que o cliente escolhe, '
            'pede e paga.</span></p>')
FMTCSS = '<style>' + MARCA2 + '''
#mesa{min-height:0!important}
#mesa>.wrap{min-height:0!important}
#mesa .mesa-top{display:block!important}
#mesa .mesa-foto{display:none!important}
#mesa .head{max-width:none}
#mesa .h2{font-size:clamp(40px,min(7vh,5.2vw),88px)!important}
#mesa .sub{max-width:80ch}
.mkc-dif{margin-top:8px;display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;justify-self:start;background:var(--ink);color:#fff;border-radius:18px;padding:14px 22px;font-size:clamp(15px,1.5vw,19px);line-height:1.4;max-width:900px;box-shadow:0 12px 30px rgba(10,0,68,.18)}
.mkc-dif b{font-family:var(--display);font-weight:700;text-transform:uppercase;font-size:clamp(20px,2.1vw,28px);line-height:1;background:var(--lime);color:var(--ink);border-radius:999px;padding:7px 16px;white-space:nowrap}
.mkc-dif span{flex:1 1 320px}
.mkc-fmts{display:grid;gap:18px}
.mkc-fmts .fcard{grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);grid-template-areas:"t g" "t n" "t d" "t m";align-items:center;align-content:center;column-gap:clamp(20px,4vw,56px);row-gap:10px;padding:clamp(18px,2.4vw,32px)}
.mkc-fmts .fcard .thumb{grid-area:t}
.mkc-fmts .fcard .tags{grid-area:g;align-self:end}
.mkc-fmts .fcard>b{grid-area:n;font-size:clamp(24px,2.6vw,36px);font-family:var(--display);text-transform:uppercase;line-height:1.05}
.mkc-fmts .fcard>p{grid-area:d;font-size:clamp(15px,1.4vw,18px);line-height:1.5}
.mkc-fmts .fcard .more{grid-area:m;align-self:start}
.mkc-fmts .fcard:nth-child(even){grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);grid-template-areas:"g t" "n t" "d t" "m t"}
.mkc-fmts .fcard{background:#fff!important;border-color:rgba(10,0,68,.14)!important;color:var(--ink)}
.mkc-fmts .fcard:hover{border-color:var(--blue)!important}
.mkc-fmts .fcard>p{color:#4A4380!important}
.mkc-fmts .fcard .more{color:var(--blue)!important}
.mkc-fmts .fcard .tag:not(.x):not(.l):not(.cr){color:var(--ink);border-color:rgba(10,0,68,.25)}
.mkc-fmts .fcard .tag.cr{background:#EEEBFF;border-color:#EEEBFF}
@media (max-width:760px){.mkc-fmts .fcard,.mkc-fmts .fcard:nth-child(even){grid-template-columns:1fr;grid-template-areas:"t" "g" "n" "d" "m"}}
''' + '</style>'
FMTJS = '''<script>/*mk-compartilhar-formatos-js*/
(function(){var m=document.getElementById('mesa'),fc=document.getElementById('fcards'),fs=document.getElementById('formatos');
if(!m||!fc)return;var top=m.querySelector('.mesa-top');if(!top)return;
var list=document.createElement('div');list.className='mkc-fmts';
Array.prototype.slice.call(fc.querySelectorAll('.fcard.only-b2c')).forEach(function(c){
  try{var f=FORMATS.filter(function(x){return x.id===c.dataset.f})[0];var p=c.querySelector('p');if(f&&p)p.textContent=f.d}catch(e){}
  list.appendChild(c)});
top.parentNode.insertBefore(list,top.nextSibling);
if(fs)fs.classList.add('only-b2b');})();
</script>'''


def compartilhar(s):
    s, _ = limpar(s)
    # sem filtro e sem card de culinária
    k = '<h3>Culinária</h3>'
    if k in s:
        i = s.index(k); j = s.rfind('<div style="display:grid;gap:8px">', 0, i)
        if j >= 0 and i - j < 200:
            s = s[:j] + '<div style="display:grid;gap:8px" hidden>' + s[j + len('<div style="display:grid;gap:8px">'):]
    s = s.replace('<div><b>Tipo de culinária</b><p>', '<div hidden><b>Tipo de culinária</b><p>')
    if MARCA not in s and '/*jota-mapa*/' not in s:
        i = s.lower().rfind('</body>')
        s = s[:i] + MAPCSS + s[i:] if i >= 0 else s + MAPCSS
    # sem o pop-up "Conheça a Goomer" ao abrir
    s = s.replace("setTimeout(()=>open('ask'),600);", '')
    # destaque de mídia inovadora logo depois do texto do "Por que Goomer Ads"
    if 'class="mkc-dif"' not in s:
        a = s.find('<section class="band light only-b2c" id="mesa">')
        i = s.find('</p>', s.find('<p class="sub">', a)) if a >= 0 else -1
        if i > 0:
            s = s[:i + 4] + '\n      ' + DESTAQUE + s[i + 4:]
    # formatos um por um logo abaixo do texto
    if MARCA2 not in s:
        i = s.lower().rfind('</body>')
        s = s[:i] + FMTCSS + FMTJS + s[i:] if i >= 0 else s + FMTCSS + FMTJS
    return s


if __name__ == '__main__':
    ok = True
    for p in sys.argv[1:]:
        s = compartilhar(open(p, encoding='utf-8').read())
        e = conferir(s)
        if MARCA not in s and '/*jota-mapa*/' not in s:
            e.append('mapa fixo não entrou')
        if "setTimeout(()=>open('ask'),600)" in s:
            e.append('pop-up Conheça a Goomer ainda abre sozinho')
        if MARCA2 not in s or 'class="mkc-dif"' not in s:
            e.append('formatos/destaque não entraram')
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(s)
        print(p, 'OK' if not e else 'ERRO: ' + '; '.join(e))
        ok = ok and not e
    sys.exit(0 if ok else 1)

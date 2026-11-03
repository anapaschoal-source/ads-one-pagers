#!/usr/bin/env python3
"""Transforma o media kit aberto na versão **Compartilhar** (a que vai para o cliente).

Uso: python3 _modelo/media-kit/compartilhar.py <arquivo.html> [<arquivo.html> ...]

1. Tira os números por cidade e por restaurante (mesmo que sem_numeros.py).
2. Mapa fixo, como no kit da Jota: Brasil inteiro com os pontos e os números gerais
   (+2 mil restaurantes, +50 mil telas, +300 cidades, +5 M pessoas), sem filtros, sem
   culinária, sem zoom e sem clique; texto alinhado à margem das outras seções, em
   duas linhas no título, e o mapa deslocado para a direita.
3. Sem o pop-up "Conheça a Goomer" ao abrir.
4. "Por que Goomer Ads · Mídia inovadora": título em duas linhas, "Primeiro formato de mídia na mesa," /
   "no momento de consumo. Não na parede." (com marca-texto lime no começo), o texto menor embaixo
   em largura total, a faixa
   "DOOH 2.0 · +400 milhões" (os dois lados no mesmo tamanho) e os formatos no lugar da foto da mesa:
   Tela de Início e Venda Sugestiva lado a lado, Confirmação de Pedido e Minha Conta lado a lado, e a
   Página Especial grande, em destaque (borda lime, "Toque e teste a ativação" pulsando, botão
   "Jogar agora"): o clique roda o jogo ali mesmo, no tablet do card. Os formatos não abrem
   pop-up (a página já tem as informações). Os números (1–2h, 30–40, 1:4, +20) vão para o fim do
   "Inventário por segmento culinário" (com 1:2, um tablet para cada 2 pessoas). As marcas que já
   anunciam vêm logo depois dos formatos.
   A seção "Formatos" fica só para o modo B2B.
Pode rodar mais de uma vez. Rode no HTML aberto, antes do senha.py.
"""
import os, re, sys
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
EYEBROW = '<span class="eyebrow">Por que Goomer Ads · Mídia inovadora</span>'
TITULO = ('<h2 class="h2"><em>Primeiro formato de mídia na mesa,</em><br>no momento de consumo. '
          'Não na parede.</h2>')
FMTCSS = '<style>' + MARCA2 + '''
#mesa{min-height:0!important}
#mesa>.wrap{min-height:0!important}
#mesa .mesa-top{display:block!important}
#mesa .mesa-foto{display:none!important}
#mesa .head{max-width:none}
#mesa .h2{font-size:clamp(34px,5.4vw,104px)!important;max-width:none!important;white-space:normal}
@media (min-width:901px){#mesa .h2{white-space:nowrap}}
#mesa .sub{max-width:none!important;font-size:clamp(16px,1.55vw,22px)!important}
#mesa .imp400{margin-top:clamp(18px,3vh,32px)}
#mesa .h2 em{font-style:normal;background:linear-gradient(transparent 10%,var(--lime) 10%,var(--lime) 90%,transparent 90%);padding:0 .08em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
#mesa .head .sub{font-size:clamp(15px,1.2vw,18px)!important;max-width:none!important;margin-top:clamp(10px,1.6vh,18px)}
#mesa .imp400{margin-top:clamp(22px,4vh,40px);margin-bottom:clamp(28px,5vh,56px)}
#mesa .imp400{display:grid!important;grid-template-columns:minmax(0,1fr) 1px minmax(0,1fr);align-items:center;justify-items:center;column-gap:clamp(20px,3vw,48px);padding:clamp(22px,3.6vh,40px) clamp(24px,3vw,48px)!important}
#mesa .imp400 .i4a,#mesa .imp400 .i4b{display:flex!important;flex-direction:column!important;flex-wrap:nowrap!important;align-items:center!important;justify-content:center!important;text-align:center;gap:clamp(10px,1.6vh,16px)!important;min-width:0}
#mesa .imp400 .i4a em{font-size:clamp(40px,min(9vh,5vw),104px)!important;padding:.06em .36em!important;line-height:1.05}
#mesa .imp400 .i4b b{font-size:clamp(50px,min(11.5vh,6.6vw),136px)!important;line-height:.95}
#mesa .imp400 .i4a span,#mesa .imp400 .i4b>span{font-family:var(--display)!important;text-transform:uppercase;font-weight:700!important;color:#fff!important;font-size:clamp(18px,min(3.6vh,2.05vw),40px)!important;line-height:1.1!important;max-width:none!important;white-space:normal!important;display:grid!important;gap:4px;justify-items:center}
#mesa .imp400 small{font-size:clamp(12px,min(2vh,1.2vw),18px)!important}
#mesa .imp400 .i4d{display:block!important;width:1px;height:70%;align-self:center;background:rgba(255,255,255,.22)}
@media (max-width:760px){
 #mesa .imp400{grid-template-columns:minmax(0,1fr);row-gap:22px;padding:24px 20px!important}
 #mesa .imp400 .i4d{width:60%;height:1px}
}
.mkc-fmts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
.mkc-fmts .fcard{grid-template-columns:minmax(0,1fr);grid-template-areas:"t" "g" "n" "d" "m";align-content:start;row-gap:12px;padding:clamp(18px,2.2vw,30px)}
.mkc-fmts .fcard .thumb{grid-area:t;margin-bottom:6px}
.mkc-fmts .fcard .tags{grid-area:g}
.mkc-fmts .fcard>b{grid-area:n;font-size:clamp(24px,2.4vw,34px);font-family:var(--display);text-transform:uppercase;line-height:1.05}
.mkc-fmts .fcard>p{grid-area:d;font-size:clamp(15px,1.3vw,17px);line-height:1.5}
.mkc-fmts .fcard .more{grid-area:m;align-self:start}
.mkc-fmts .fcard.mkc-play{grid-column:1/-1;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);grid-template-areas:"t g" "t n" "t d" "t m";align-items:center;align-content:center;column-gap:clamp(24px,4vw,64px);padding:clamp(22px,3vw,44px)}
.mkc-fmts .fcard.mkc-play>b{font-size:clamp(30px,3.4vw,52px)}
@media (min-width:761px){
 .mkc-fmts .fcard.mkc-play{grid-template-columns:minmax(0,1fr) auto!important;grid-template-areas:"t t" "g m" "n m" "d m"!important;align-items:center;column-gap:clamp(24px,4vw,64px);row-gap:12px}
 .mkc-fmts .fcard.mkc-play .thumb{justify-self:center;width:min(100%,calc((100svh - 110px) * 1.4),1240px);margin-bottom:clamp(8px,2vh,24px)}
 .mkc-fmts .fcard.mkc-play .thumb .scr{max-width:none!important;width:100%!important}
 .mkc-fmts .fcard.mkc-play>p{max-width:80ch}
 .mkc-fmts .fcard.mkc-play .mkc-go{align-self:center;font-size:17px!important;padding:16px 26px}
 .mkc-try{font-size:clamp(16px,1.6vw,20px)!important;padding:16px 26px!important}
}
.mkc-fmts .fcard.mkc-play .tags{align-self:end}
.mkc-fmts .fcard{background:#fff!important;border-color:rgba(10,0,68,.14)!important;color:var(--ink)}
.mkc-fmts .fcard:hover{border-color:var(--blue)!important}
.mkc-fmts .fcard>p{color:#4A4380!important}
.mkc-fmts .fcard .more{color:var(--blue)!important}
.mkc-fmts .fcard .tag:not(.x):not(.l):not(.cr){color:var(--ink);border-color:rgba(10,0,68,.25)}
.mkc-fmts .fcard .tag.cr{background:#EEEBFF;border-color:#EEEBFF}
.mkc-fmts .fcard.mkc-play{border:2px solid var(--lime)!important;box-shadow:0 0 0 6px rgba(189,226,73,.22),0 18px 40px rgba(10,0,68,.12);position:relative}
.mkc-fmts .fcard{cursor:default}
.mkc-fmts .fcard:hover{border-color:rgba(10,0,68,.14)!important;background:#fff!important}
.mkc-fmts .fcard.mkc-play:hover{border-color:var(--lime)!important}
.mkc-fmts .fcard.mkc-play .thumb{position:relative;pointer-events:auto}
.mkc-fmts .fcard.mkc-play .thumb .gameclose:not([hidden]){display:inline-flex!important}
.mkc-fmts .fcard.mkc-play.jogando .mkc-try{display:none}
.mkc-try{border:0;cursor:pointer}
.mkc-go{border:0;cursor:pointer;font:inherit}
.band.cuis .mkc-stats{margin-top:clamp(28px,5vh,56px)}
.band.cuis .mkc-stats .stat{padding:clamp(14px,2.2vh,26px) clamp(16px,1.8vw,24px)}
.band.cuis .mkc-stats{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.16)}
.band.cuis .mkc-stats .stat{background:var(--ink)}
.band.cuis .mkc-stats .stat b{font-size:clamp(34px,5.2vh,56px);color:var(--lime)}
.band.cuis .mkc-stats .stat span{color:#fff}
.band.cuis .mkc-stats .stat small{color:rgba(255,255,255,.68)}
body[data-mode="b2b"] .band.cuis .mkc-stats{display:none}
.mkc-try{position:absolute;z-index:5;left:50%;top:50%;transform:translate(-50%,-50%);display:inline-flex;align-items:center;gap:10px;background:var(--lime);color:var(--ink);font:800 clamp(14px,1.4vw,17px)/1 var(--body,Manrope),sans-serif;padding:14px 22px;border-radius:999px;box-shadow:0 10px 30px rgba(10,0,68,.35);white-space:nowrap;animation:mkcPulse 1.8s ease-in-out infinite}
.mkc-try i{font-style:normal;display:inline-grid;place-items:center;width:26px;height:26px;border-radius:50%;background:var(--ink);color:var(--lime);font-size:12px}
@keyframes mkcPulse{0%,100%{box-shadow:0 0 0 0 rgba(189,226,73,.7),0 10px 30px rgba(10,0,68,.35)}50%{box-shadow:0 0 0 14px rgba(189,226,73,0),0 10px 30px rgba(10,0,68,.35)}}
.mkc-fmts .fcard.mkc-play .more{display:inline-flex;align-items:center;gap:8px;justify-self:start;background:var(--ink);color:var(--lime)!important;padding:12px 20px;border-radius:999px;font-size:15px!important}
.mkc-fmts .fcard.mkc-play .more:hover{background:var(--blue);color:#fff!important}
@media (prefers-reduced-motion:reduce){.mkc-try{animation:none}}
@media (max-width:900px){.fx-card{grid-template-columns:minmax(0,1fr)!important;overflow-x:hidden}.fx-card>*{min-width:0}.fx-list{grid-template-columns:repeat(2,minmax(0,1fr))!important}.fx-list button{grid-template-columns:minmax(0,1fr)!important;min-width:0}.fx-list button b{font-size:14px}.fx-list button span{font-size:10px}}
@media (max-width:520px){.mkc-try{font-size:13px;padding:10px 16px;gap:8px}.mkc-try i{width:22px;height:22px;font-size:10px}}
@media (max-width:760px){.mkc-fmts{grid-template-columns:minmax(0,1fr)}.mkc-fmts .fcard,.mkc-fmts .fcard.mkc-play{grid-column:auto;grid-template-columns:minmax(0,1fr);grid-template-areas:"t" "g" "n" "d" "m"}}
''' + '</style>'
FMTJS = '''<script>/*mk-compartilhar-formatos-js*/
(function(){var m=document.getElementById('mesa'),fc=document.getElementById('fcards'),fs=document.getElementById('formatos');
if(!m||!fc)return;var top=m.querySelector('.mesa-top');if(!top)return;
var list=document.createElement('div');list.className='mkc-fmts';
Array.prototype.slice.call(fc.querySelectorAll('.fcard.only-b2c')).forEach(function(c){
  try{var f=FORMATS.filter(function(x){return x.id===c.dataset.f})[0];var p=c.querySelector('p');if(f&&p)p.textContent=f.d}catch(e){}
  /* sem pop-up: o card vira bloco de conteúdo (div), com tudo na página */
  var d=document.createElement('div');d.className=c.className;d.dataset.f=c.dataset.f;
  while(c.firstChild)d.appendChild(c.firstChild);
  var mo=d.querySelector('.more');if(mo)mo.remove();
  list.appendChild(d)});
var anc=top,band=m.querySelector('.imp400');
if(band){top.parentNode.insertBefore(band,top.nextSibling);anc=band}
anc.parentNode.insertBefore(list,anc.nextSibling);
['inicio','sug','confirm','conta','especial'].forEach(function(id){var c=list.querySelector('.fcard[data-f="'+id+'"]');if(c)list.appendChild(c)});
var esp=list.querySelector('.fcard[data-f="especial"]');
if(esp){esp.classList.add('mkc-play');
  var th=esp.querySelector('.thumb'),pb=th&&th.querySelector('.playbtn'),gc=th&&th.querySelector('.gameclose');
  var t=document.createElement('button');t.type='button';t.className='mkc-try';t.innerHTML='<i>&#9654;</i>Toque e teste a ativação';if(th)th.appendChild(t);
  var go=document.createElement('button');go.type='button';go.className='more mkc-go';go.textContent='▶ Jogar agora';esp.appendChild(go);
  function jogar(){if(pb&&!pb.hidden){pb.click();esp.classList.add('jogando');setTimeout(function(){var g=th.querySelector('.gamebox')||th;g.scrollIntoView({block:'center',behavior:'smooth'})},120)}}
  t.onclick=jogar;go.onclick=jogar;
  if(gc)gc.addEventListener('click',function(){esp.classList.remove('jogando')});}
var st=m.querySelector('.stats'),cu=document.querySelector('.band.cuis .wrap');
if(st&&cu){st.classList.add('mkc-stats');cu.appendChild(st)}
var br=document.querySelector('section.band.brands');if(br&&m.parentNode)m.parentNode.insertBefore(br,m.nextSibling);
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
    # "Por que Goomer Ads · Mídia inovadora": título com o primeiro formato de mídia na mesa
    a = s.find('<section class="band light only-b2c" id="mesa">')
    if a >= 0:
        s = s[:a] + s[a:].replace('<span class="eyebrow">Por que Goomer Ads</span>', EYEBROW, 1)
        s = re.sub(r'<h2 class="h2">(?:Mídia na mesa|Na mesa), no momento de consumo\.<br>Não na parede\.</h2>', TITULO, s, count=1)
    # versões antigas deste script punham uma frase de destaque à parte: tira
    s = re.sub(r'\n\s*<p class="mkc-dif">.*?</p>', '', s, count=1, flags=re.S)
    # um tablet para cada 2 pessoas
    s = s.replace('<b>1:4</b><span>um tablet para 4 pessoas</span>', '<b>1:2</b><span>um tablet para cada 2 pessoas</span>')
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
        if TITULO not in s or EYEBROW not in s:
            e.append('título/eyebrow de mídia inovadora não entraram')
        if '<b>1:4</b>' in s or 'para 4 pessoas' in s:
            e.append('ainda diz um tablet para 4 pessoas')
        if MARCA2 not in s:
            e.append('formatos/destaque não entraram')
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(s)
        print(p, 'OK' if not e else 'ERRO: ' + '; '.join(e))
        ok = ok and not e
    sys.exit(0 if ok else 1)

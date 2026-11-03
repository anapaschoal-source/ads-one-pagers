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
   Tela de Início, Confirmação de Pedido e Minha Conta lado a lado (3 colunas); Venda Sugestiva em
   destaque, largura total ("Formato prioritário", case +30%, case de Campinas em barras e "Por que
   priorizar"); e a Página Especial grande, em destaque (borda lime, "Toque e teste a ativação" pulsando, botão
   "Jogar agora"), com o tablet grande à esquerda e as informações à direita: o clique roda o
   jogo ali mesmo e dá zoom na tela do tablet para dar para ler a ativação. Os formatos não abrem
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
.mkc-maior{color:var(--ink);font-weight:800;background:linear-gradient(transparent 62%,rgba(189,226,73,.75) 62%);padding:0 .1em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
#mesa .imp400{margin-top:clamp(18px,3vh,32px)}
#mesa .h2 em{font-style:normal;background:linear-gradient(transparent 10%,var(--lime) 10%,var(--lime) 90%,transparent 90%);padding:0 .08em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
#mesa .head .sub{font-size:clamp(17px,1.55vw,24px)!important;line-height:1.45!important;max-width:none!important;margin-top:clamp(10px,1.6vh,18px)}
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
@media (min-width:901px){
 .mkc-fmts .fcard.mkc-play{grid-template-columns:minmax(0,1fr) clamp(250px,24vw,380px)!important;grid-template-areas:"t g" "t n" "t d" "t m"!important;align-items:center;align-content:center;column-gap:clamp(20px,2.6vw,44px);row-gap:12px;padding:clamp(14px,1.6vw,26px) clamp(20px,2.4vw,40px) clamp(14px,1.6vw,26px) clamp(10px,1vw,16px)!important}
 .mkc-fmts .fcard.mkc-play .thumb{justify-self:stretch;width:100%;max-width:calc((100svh - 90px) * 1.39);margin:0}
 .mkc-fmts .fcard.mkc-play .thumb .scr{max-width:none!important;width:100%!important}
 .mkc-fmts .fcard.mkc-play>p{max-width:none}
 .mkc-fmts .fcard.mkc-play .mkc-go{justify-self:start;font-size:17px!important;padding:16px 26px}
 .mkc-try{font-size:clamp(16px,1.6vw,20px)!important;padding:16px 26px!important}
}
/* jogando: zoom na tela do tablet para dar para ler a ativação */
.mkc-fmts .fcard.mkc-play .thumb{overflow:hidden;border-radius:14px}
.mkc-fmts .fcard.mkc-play .thumb .scr{animation:none!important;transition:transform .5s cubic-bezier(.2,.8,.2,1);transform-origin:54.6% 43.5%}
.mkc-fmts .fcard.mkc-play.jogando .thumb .scr{transform:scale(1.5)}
.mkc-fmts .fcard.mkc-play .thumb>.gameclose{position:absolute;z-index:7;top:10px;right:10px}
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
/* seções alternando branco e azul: mesa branco, marcas escuro, inventário branco, mapa azul, resultados branco, cobrança azul, contato */
.band.cuis,#resultados{background:var(--paper)!important;color:var(--ink)!important;--line:rgba(10,0,68,.16);--faint:rgba(10,0,68,.06);--muted:#4A4380}
.band.cuis .eyebrow,#resultados .eyebrow{color:var(--blue)!important}
.band.cuis .cb .bar{background:rgba(10,0,68,.1)!important}
.band.cuis .sub,#resultados .sub{color:#4A4380!important;opacity:1!important}
#cobranca{background:var(--ink)!important;color:#fff!important;--line:rgba(255,255,255,.18);--faint:rgba(255,255,255,.06);--muted:rgba(255,255,255,.66)}
#cobranca .eyebrow{color:var(--lime)!important}
#cobranca .head .sub{color:rgba(255,255,255,.75)!important}
#cobranca .cb-both b{color:var(--lime)!important}
#cobranca .cb-both span{color:#fff!important}
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
/* destaque da Venda Sugestiva e formatos em 3 colunas (referência: kit Ambev, nov/2026) */
.mkc-fmts{grid-template-columns:repeat(3,minmax(0,1fr))!important}
.mkc-fmts .fcard.mkc-play,.mkc-fmts .fcard.mkc-sug{grid-column:1/-1!important}
.mkc-fmts .fcard.mkc-sug{background:#fff!important;border:2px solid var(--lime)!important;box-shadow:0 0 0 6px rgba(189,226,73,.22),0 18px 40px rgba(10,0,68,.12);grid-template-columns:minmax(0,1.05fr) minmax(0,1fr)!important;grid-template-areas:"t g" "t n" "t d" "t k" "x x"!important;column-gap:clamp(24px,3.4vw,56px);row-gap:12px;align-items:center;padding:clamp(18px,2.4vw,36px)!important}
.mkc-fmts .fcard.mkc-sug:hover{border-color:var(--lime)!important}
.mkc-fmts .fcard.mkc-sug>b{font-size:clamp(30px,3.4vw,52px)!important}
.mkc-fmts .fcard.mkc-sug .thumb{margin:0!important}
.mkc-sugk{grid-area:k;display:grid;grid-template-columns:auto minmax(0,1fr);gap:6px 18px;align-items:center;background:#F3F0FF;border-radius:18px;padding:16px 20px}
.mkc-sugk .lb,.mkc-sugx .lb{grid-column:1/-1;font-size:11px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.mkc-sugk strong{font-family:var(--display);font-size:clamp(56px,6vw,88px);line-height:.9;color:var(--blue)}
.mkc-sugk span{font-size:15px;font-weight:700;line-height:1.35;color:var(--ink)}
.mkc-sugk small{grid-column:1/-1;font-size:13px;color:#4A4380}
.mkc-sugx{grid-area:x;display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:clamp(18px,3vw,44px);border-top:1px solid rgba(10,0,68,.12);padding-top:clamp(16px,2.4vh,26px);margin-top:6px}
.mkc-sugx h4{margin:4px 0 4px;font-size:18px;font-weight:800;color:var(--ink)}
.mkc-sugx p{font-size:14px;color:#4A4380;line-height:1.45}
.mkc-bars{display:grid;gap:10px;margin-top:12px}
.mkc-bar{display:grid;grid-template-columns:minmax(130px,190px) 1fr 62px;gap:12px;align-items:center;font-size:14px;font-weight:700;color:var(--ink)}
.mkc-bar .tr{height:14px;border-radius:7px;background:rgba(10,0,68,.08);overflow:hidden}
.mkc-bar .tr i{display:block;height:100%;border-radius:7px;background:var(--blue);width:0;transition:width 1.2s cubic-bezier(.2,.8,.2,1)}
.mkc-bar.food .tr i{background:rgba(10,0,68,.28)}
.mkc-sug.in .mkc-bar .tr i{width:var(--w)}
.mkc-bar b{font-family:var(--display);font-size:22px;text-align:right;color:var(--blue)}
.mkc-bar.food b{color:#4A4380}
.mkc-why{display:grid;gap:14px;align-content:start}
.mkc-why div{border-left:3px solid var(--lime);padding-left:12px}
.mkc-why b{display:block;font-size:15px;color:var(--ink)}
.mkc-why small{display:block;font-size:13.5px;color:#4A4380;line-height:1.4}
.mkc-sugx{align-items:stretch}
.mkc-why{grid-template-rows:auto repeat(3,minmax(0,1fr));gap:12px!important;align-content:stretch!important}
.mkc-why div{border-left:0!important;padding:16px 20px!important;background:#F3F0FF;border-radius:16px;display:flex;flex-direction:column;justify-content:center;gap:6px;position:relative;overflow:hidden}
.mkc-why div::before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--lime)}
.mkc-why b{font-size:clamp(17px,1.5vw,21px)!important;line-height:1.25}
.mkc-why small{font-size:clamp(14.5px,1.15vw,16.5px)!important;line-height:1.45}
@media (max-width:900px){.mkc-bar{grid-template-columns:96px minmax(0,1fr) auto!important;gap:10px!important}.mkc-bar b{font-size:19px!important}}
.mkc-sugx h4{font-size:clamp(19px,1.7vw,24px)!important}
.mkc-sugx>div:first-child>p{font-size:clamp(15px,1.2vw,17px)!important}
.mkc-bar{font-size:clamp(15px,1.25vw,17px)!important;grid-template-columns:minmax(150px,220px) 1fr 72px}
.mkc-bar b{font-size:clamp(24px,2vw,28px)!important}
.mkc-bar .tr{height:16px}
.mkc-bars{gap:14px!important}
@media (max-width:900px){.mkc-bar{grid-template-columns:104px minmax(0,1fr) auto!important;font-size:14px!important}.mkc-bar b{font-size:20px!important}}
@media (min-width:901px){.mkc-fmts .fcard.mkc-play{grid-template-columns:minmax(0,1fr) clamp(300px,30vw,460px)!important}}
.mkc-fmts .fcard.mkc-play>b{font-size:clamp(40px,4.6vw,72px)!important}
.mkc-fmts .fcard.mkc-play>p{font-size:clamp(17px,1.6vw,22px)!important;line-height:1.5!important}
.mkc-fmts .fcard.mkc-play .tags .tag{font-size:13.5px;padding:6px 12px}
.mkc-fmts .fcard.mkc-play .mkc-go{font-size:clamp(17px,1.5vw,20px)!important;padding:16px 28px!important}
@media (min-width:901px){.mkc-fmts .fcard.mkc-sug{grid-template-areas:"t s1" "t g" "t n" "t d" "t k" "t s2" "x x"!important;grid-template-rows:1fr auto auto auto auto 1fr auto!important;row-gap:14px!important;align-items:start!important}}
.mkc-fmts .fcard.mkc-sug>b{font-size:clamp(40px,4.6vw,72px)!important;line-height:1!important}
.mkc-fmts .fcard.mkc-sug>p{font-size:clamp(17px,1.6vw,22px)!important;line-height:1.5!important}
.mkc-fmts .fcard.mkc-sug .tags .tag{font-size:13.5px;padding:6px 12px}
.mkc-sugk span{font-size:clamp(16px,1.35vw,19px)!important}
.mkc-sugk small{font-size:clamp(14px,1.15vw,16px)!important}
.mkc-fmts .fcard .tags{gap:8px!important}
.mkc-fmts .fcard .tags .tag{font-size:13.5px!important;padding:6px 12px!important;letter-spacing:.06em!important}
.mkc-sugx .nt{grid-column:1/-1;font-size:11.5px;color:#6B6699}
@media (max-width:900px){.mkc-fmts{grid-template-columns:minmax(0,1fr)!important}.mkc-fmts .fcard.mkc-sug{grid-template-columns:minmax(0,1fr)!important;grid-template-areas:"t" "g" "n" "d" "k" "x"!important}.mkc-sugx{grid-template-columns:minmax(0,1fr)}.mkc-bar{grid-template-columns:110px 1fr 52px;font-size:13px}}
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
['inicio','confirm','conta','sug','especial'].forEach(function(id){var c=list.querySelector('.fcard[data-f="'+id+'"]');if(c)list.appendChild(c)});
var esp=list.querySelector('.fcard[data-f="especial"]');
if(esp){esp.classList.add('mkc-play');
  var th=esp.querySelector('.thumb'),pb=th&&th.querySelector('.playbtn'),gc=th&&th.querySelector('.gameclose');
  var t=document.createElement('button');t.type='button';t.className='mkc-try';t.innerHTML='<i>&#9654;</i>Toque e teste a ativação';if(th)th.appendChild(t);
  var go=document.createElement('button');go.type='button';go.className='more mkc-go';go.textContent='▶ Jogar agora';esp.appendChild(go);
  function abriu(){esp.classList.add('jogando');setTimeout(function(){var g=th.querySelector('.gamebox')||th;g.scrollIntoView({block:'center',behavior:'smooth'})},120)}
  if(pb)pb.addEventListener('click',abriu);
  function jogar(){if(pb&&!pb.hidden)pb.click()}
  t.onclick=jogar;go.onclick=jogar;
  if(gc){th.appendChild(gc);gc.addEventListener('click',function(){esp.classList.remove('jogando')})}}
var st=m.querySelector('.stats'),cu=document.querySelector('.band.cuis .wrap');
if(st&&cu){st.classList.add('mkc-stats');cu.appendChild(st)}
var br=document.querySelector('section.band.brands');if(br&&m.parentNode)m.parentNode.insertBefore(br,m.nextSibling);
if(fs)fs.classList.add('only-b2b');})();
(function(){var l=document.querySelector('.mkc-fmts');if(!l)return;var c=l.querySelector('.fcard[data-f="sug"]');if(!c)return;
c.classList.add('mkc-sug');var tg=c.querySelector('.tags');if(tg&&!tg.querySelector('.mkc-prio')){var t=document.createElement('span');t.className='tag l mkc-prio';t.textContent='Formato prioritário';tg.insertBefore(t,tg.firstChild);var f=tg.querySelector('.tag.l:not(.mkc-prio)');if(f)f.classList.remove('l')}
var dp=c.querySelector(':scope>p');if(dp)dp.textContent='Quando o cliente faz o pedido, o tablet sugere o seu produto antes de enviar para a cozinha. Um toque e ele entra no pedido.';
var k=document.createElement('div');k.className='mkc-sugk';k.innerHTML='<span class="lb">Case · Venda Sugestiva</span><strong>+30%</strong><span>de crescimento médio nas vendas dos produtos patrocinados</span><small>Produto sugerido no fechamento do pedido, com adição em um toque.</small>';c.appendChild(k);
var x=document.createElement('div');x.className='mkc-sugx';x.innerHTML='<div><span class="lb">Case · Destaque no cardápio do tablet</span><h4>Rede de food service · unidade em Campinas (SP)</h4><p>Itens ganharam destaque no cardápio digital. Vendas antes e depois da virada, com 42% de penetração do tablet no salão.</p><div class="mkc-bars">'+
[['Refrigerante zero 500ml',100,'+329%',''],['Suco 500ml',66,'+218%',''],['Refrigerante cola zero 500ml',45,'+148%',''],['Sobremesa',35,'+115%','food'],['Salgado',30,'+100%','food']].map(function(r){return '<div class="mkc-bar '+r[3]+'"><span>'+r[0]+'</span><div class="tr"><i style="--w:'+r[1]+'%"></i></div><b>'+r[2]+'</b></div>'}).join('')+
'</div></div><div class="mkc-why"><span class="lb">Por que priorizar</span><div><b>Mídia que entra no pedido</b><small>A sugestão aparece quando o cliente já está decidindo o que pedir. Um toque e o produto vai para a cozinha.</small></div><div><b>Exclusivo para indústrias</b><small>Formato pensado para quem vende no food service: bebidas, alimentos e ingredientes.</small></div><div><b>Mensurável por SKU</b><small>Vendas do produto sugerido acompanhadas por restaurante, praça e período.</small></div></div><p class="nt">Cases reais da rede Goomer, apresentados de forma anonimizada. Resultados variam conforme restaurante, praça e período.</p>';c.appendChild(x);
if('IntersectionObserver' in window){new IntersectionObserver(function(e,o){e.forEach(function(z){if(z.isIntersecting){c.classList.add('in');o.disconnect()}})},{threshold:.2}).observe(c)}else c.classList.add('in');
})();
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
    # destaque para "O maior inventário de DOOH do food service no Brasil."
    s = s.replace(' O maior inventário de DOOH do food service no Brasil.</p>',
                  '<br><strong class="mkc-maior">O maior inventário de DOOH do food service no Brasil.</strong></p>', 1)
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

#!/usr/bin/env python3
"""Coloca senha de acesso num media kit (ou em qualquer página HTML).

Uso: python3 _modelo/media-kit/senha.py <entrada.html> <saida.html> --senha <senha> [--marca "Nome"]
     python3 _modelo/media-kit/senha.py --abrir <protegido.html> <aberto.html> --senha <senha>
     (--abrir devolve o HTML original, para editar um kit já protegido e proteger de novo)

A página inteira é comprimida (gzip) e criptografada (AES-256-GCM, chave derivada da senha com
PBKDF2-SHA256, 250 mil iterações). A saída é uma tela de acesso da Goomer Ads com o conteúdo
cifrado embutido: sem a senha, nada do kit (textos, números, imagens) fica legível no código-fonte.
A tela de senha tem o Vercel Web Analytics (conta quem abriu o link). Com a senha certa, o navegador decifra e abre o kit na mesma página. A senha fica lembrada na
aba (sessionStorage) até fechar o navegador.

Pode rodar de novo sobre uma saída já protegida? Não: rode sempre sobre o HTML aberto.
"""
import argparse, base64, gzip, html, os, re, sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITER = 250_000
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, '..', 'base', 'goomer-ads.svg')

GATE = r'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<meta name="robots" content="noindex,nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Antonio:wght@700&family=Manrope:wght@500;700;800&display=swap" rel="stylesheet">
<style>
:root{--ink:#0A0044;--deep:#06002B;--lime:#BDE249;--blue:#2B00FF}
*{box-sizing:border-box}
html,body{margin:0;min-height:100%;background:var(--deep);color:#fff;font-family:Manrope,system-ui,-apple-system,'Segoe UI',sans-serif}
body{min-height:100svh;display:flex;align-items:center;justify-content:center;padding:24px 16px;background:radial-gradient(120% 90% at 60% 40%,#16007A 0%,var(--deep) 65%)}
.gate{width:min(400px,100%);background:var(--ink);border:1px solid rgba(255,255,255,.16);border-radius:24px;padding:34px 30px 28px;display:flex;flex-direction:column;gap:18px;box-shadow:0 30px 80px rgba(0,0,0,.45)}
.gate .lg{height:46px;width:auto;align-self:flex-start}
.gate h1{margin:0;font-family:Antonio,'Arial Narrow',sans-serif;font-weight:700;text-transform:uppercase;font-size:40px;line-height:1;color:var(--lime)}
.gate p{margin:0;font-size:15px;line-height:1.45;color:rgba(255,255,255,.75)}
.gate label{font-size:11px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--lime)}
.gate .f{display:flex;flex-direction:column;gap:8px}
.gate input{width:100%;font:700 17px Manrope,system-ui,sans-serif;color:#fff;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.22);border-radius:12px;padding:13px 14px;outline:none}
.gate input:focus{border-color:var(--lime);box-shadow:0 0 0 3px rgba(189,226,73,.25)}
.gate input[aria-invalid="true"]{border-color:#FF7A7A}
.gate button{font:800 15px Manrope,system-ui,sans-serif;color:var(--ink);background:var(--lime);border:0;border-radius:999px;padding:14px 20px;cursor:pointer}
.gate button:hover{background:#fff}
.gate button[disabled]{opacity:.6;cursor:wait}
.gate .err{min-height:20px;font-size:14px;font-weight:700;color:#FF9A9A}
.gate .ft{font-size:12px;color:rgba(255,255,255,.5)}
</style></head><body>
<form class="gate" id="gate" autocomplete="off">
<img class="lg" src="__LOGO__" alt="Goomer Ads">
<h1>__HEAD__</h1>
<p>Este material é exclusivo. Digite a senha que você recebeu da Goomer para abrir.</p>
<div class="f"><label for="pw">Senha</label><input id="pw" type="password" autocomplete="current-password" required autofocus></div>
<div class="err" id="err" role="alert"></div>
<button type="submit" id="go">Abrir media kit</button>
<span class="ft">Não tem a senha? Fale com quem enviou este link.</span>
</form>
<script>
(function(){
var D={salt:'__SALT__',iv:'__IV__',it:__ITER__,ct:'__CT__'};
var K='gads-mk-pw';
function b64(s){var b=atob(s),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u}
async function abrir(pw){
  var km=await crypto.subtle.importKey('raw',new TextEncoder().encode(pw),'PBKDF2',false,['deriveKey']);
  var key=await crypto.subtle.deriveKey({name:'PBKDF2',salt:b64(D.salt),iterations:D.it,hash:'SHA-256'},km,{name:'AES-GCM',length:256},false,['decrypt']);
  var buf=await crypto.subtle.decrypt({name:'AES-GCM',iv:b64(D.iv)},key,b64(D.ct));
  var st=new Blob([buf]).stream().pipeThrough(new DecompressionStream('gzip'));
  return await new Response(st).text();
}
function mostrar(h){document.open();document.write(h);document.close();}
var f=document.getElementById('gate'),pw=document.getElementById('pw'),er=document.getElementById('err'),bt=document.getElementById('go');
async function tentar(v,auto){
  bt.disabled=true;bt.textContent='Abrindo…';er.textContent='';
  try{var h=await abrir(v);try{sessionStorage.setItem(K,v)}catch(e){}mostrar(h)}
  catch(e){bt.disabled=false;bt.textContent='Abrir media kit';if(!auto){er.textContent='Senha incorreta. Tente de novo.';pw.setAttribute('aria-invalid','true');pw.select()}}
}
f.addEventListener('submit',function(e){e.preventDefault();if(pw.value)tentar(pw.value,false)});
pw.addEventListener('input',function(){pw.removeAttribute('aria-invalid');er.textContent=''});
var s=null;try{s=sessionStorage.getItem(K)}catch(e){}
if(s)tentar(s,true);
})();
</script>
<script defer src="/_vercel/insights/script.js"></script>
</body></html>
'''


def proteger(page: str, senha: str, marca: str | None) -> str:
    if 'id="gate"' in page and "DecompressionStream('gzip')" in page:
        sys.exit('Esse arquivo já está protegido. Rode sobre o HTML aberto.')
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(senha.encode())
    ct = AESGCM(key).encrypt(iv, gzip.compress(page.encode('utf-8'), 9), None)
    m = re.search(r'<title>([^<]*)</title>', page)
    title = html.unescape(m.group(1)).strip() if m else 'Goomer Ads'
    head = f'Media kit para {marca}' if marca else 'Media kit Goomer Ads'
    logo = 'data:image/svg+xml;base64,' + base64.b64encode(open(LOGO, 'rb').read()).decode()
    out = GATE
    for k, v in {'__TITLE__': html.escape(title), '__HEAD__': html.escape(head), '__LOGO__': logo,
                 '__SALT__': base64.b64encode(salt).decode(), '__IV__': base64.b64encode(iv).decode(),
                 '__ITER__': str(ITER), '__CT__': base64.b64encode(ct).decode()}.items():
        out = out.replace(k, v)
    return out


def abrir(prot: str, senha: str) -> str:
    g = lambda k: re.search(k + r":'([^']*)'", prot).group(1)
    it = int(re.search(r'it:(\d+)', prot).group(1))
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=base64.b64decode(g('salt')), iterations=it).derive(senha.encode())
    return gzip.decompress(AESGCM(key).decrypt(base64.b64decode(g('iv')), base64.b64decode(g('ct')), None)).decode('utf-8')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('entrada'); ap.add_argument('saida')
    ap.add_argument('--senha', required=True)  # a senha não fica no repo (público)
    ap.add_argument('--marca')
    ap.add_argument('--abrir', action='store_true')
    a = ap.parse_args()
    page = open(a.entrada, encoding='utf-8').read()
    out = abrir(page, a.senha) if a.abrir else proteger(page, a.senha, a.marca)
    with open(a.saida, 'w', encoding='utf-8') as fh:
        fh.write(out)
    print(a.saida, f'{len(out)/1e6:.1f} MB', 'OK')

"""Tenda Atacado (diverge do modelo): a versão Compartilhar volta a abrir o pop-up "Conheça a Goomer" ao entrar.
Rode depois do compartilhar.py e do publicar.py (a miniatura do hub sai sem o pop-up) e antes do senha.py.
Uso (na raiz do repo): python3 _modelo/marcas/tenda-atacado/popup.py tenda-atacado/media-kit/index.html"""
import sys
CALL = "setTimeout(()=>open('ask'),600);"
ANCORA = "document.getElementById('gxClose').onclick=close;"
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    if CALL not in s:
        assert ANCORA in s, 'âncora do pop-up não encontrada'
        s = s.replace(ANCORA, CALL + ANCORA, 1)
        open(p, 'w', encoding='utf-8').write(s)
    print(p, 'pop-up Conheça a Goomer ao abrir: OK')

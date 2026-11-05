#!/usr/bin/env python3
"""Endereço dos materiais da marca no site: sempre com código aleatório no link.

Uso (na raiz do repo): python3 _modelo/media-kit/endereco.py <slug>
Imprime a pasta a usar, no formato <slug>-<8 letras/números> (ex.: tenda-atacado-b3w57r2y).
Vale para o one-pager (<pasta>/index.html, ativações em <pasta>/<tipo>/) e para o media kit
de envio (<pasta>/media-kit/index.html): os dois da mesma marca ficam na mesma pasta.
Se a marca já tem uma pasta com código, devolve a mesma (o link enviado não muda).
O publicar.py recebe <pasta> como slug; no JSON do one-pager, "slug" = <pasta>.
"""
import os, re, secrets, string, sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def endereco(slug):
    pad = re.compile(re.escape(slug) + r'-[a-z0-9]{8}$')
    for d in sorted(os.listdir(REPO)):
        if pad.match(d) and os.path.isdir(os.path.join(REPO, d)):
            return d
    abc = string.ascii_lowercase + string.digits
    return slug + '-' + ''.join(secrets.choice(abc) for _ in range(8))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(endereco(sys.argv[1]))

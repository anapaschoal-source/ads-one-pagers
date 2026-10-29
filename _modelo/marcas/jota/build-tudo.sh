#!/bin/sh
# Regera tudo da Jota (na raiz do repo): ativações, seletor, one-pager e media kit.
# Uso: sh _modelo/marcas/jota/build-tudo.sh <modelo-media-kit.html> <saida-media-kit.html> [saida-one-pager-artefato.html]
set -e
J=_modelo/marcas/jota
python3 $J/build-jogo.py
mkdir -p jota/quiz jota/roleta
python3 _modelo/ativacoes/ativacao.py quiz $J/life360-quiz.json jota/quiz/index.html
python3 _modelo/ativacoes/ativacao.py roleta $J/sicredi-roleta.json jota/roleta/index.html
python3 $J/build-seletor.py
python3 _modelo/build.py _modelo/marcas/jota.json ${3:+--artefato $3}
python3 $J/pos-build.py jota/index.html $3
python3 $J/media-kit.py "$1" "$2"

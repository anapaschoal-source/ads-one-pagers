# Modelo de one-pager Goomer Ads

Gera o one-pager de uma marca (B2C, com aba B2B opcional) a partir de um JSON.

```
python3 _modelo/build.py _modelo/marcas/<slug>.json                       # grava <slug>/index.html
python3 _modelo/build.py _modelo/marcas/<slug>.json --artefato saida.html  # + versão para artefato
```

- `marcas/modelo.json`: referência com todos os campos (textos entre colchetes são o que trocar).
- `marcas/<slug>/`: logo e fotos da marca (caminhos no JSON são relativos ao JSON).
- `base/`: telas Goomer neutras (tablet, formatos, painel, hero). Não editar.
- `placeholder/`: logo e fotos genéricas usadas quando o JSON não traz imagem.
- Sem `b2b` no JSON: página só B2C, sem abas.
- `demo_url`: caminho do demo publicado (ex.: `/marca/jogo/`). Sem ele, o tablet mostra a página especial estática.
- Logo da marca: sempre o arquivo oficial enviado pela Ana, nunca redesenhado.

Dependências: `pip install jinja2 pillow`.

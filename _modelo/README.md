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
- Formatos animados (mesmas animações do media kit): por padrão os banners são montados com logo, fotos e textos do JSON. Para usar o criativo pronto da marca, preencha em `imagens`: `video_inicio` (vídeo .mp4/.webm de 10s, 16:9, sem áudio) ou `criativo_inicio` (imagem 16:9, que entra animada como vídeo), `banner_confirmacao` (876×507) e `banner_conta` (≈ 204×115).
- Tela de Início é sempre vídeo de 10s: sem arquivo da marca, vira uma animação (foto com zoom, frase, fechamento com logo, barra de progresso e contagem).
- A aba da Página Especial no cardápio sempre mostra o logo da marca (`menu.logo` troca por outra versão do logo).
- Marca endêmica (o produto entra no pedido do restaurante): `"endemica": true` liga o 5º formato, Venda Sugestiva, com `venda_sugestiva` (`produto`, `descricao`, `preco`) e `imagens.foto_produto` (PNG do produto, fundo transparente). Não endêmica: `false`, ficam 4 formatos.
- Sem `b2b` no JSON: página só B2C, sem abas.
- `demo_url`: caminho do demo publicado (ex.: `/marca/jogo/`). Sem ele, o tablet mostra a página especial estática.
- Logo da marca: sempre o arquivo oficial enviado pela Ana, nunca redesenhado.

Dependências: `pip install jinja2 pillow`.

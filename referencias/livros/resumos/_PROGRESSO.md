# Progresso do estudo da biblioteca CEO

> Controle do estudo da biblioteca. CONCLUÍDO em 2026-07-12.
> Índice mestre em INDICE.md.

## Status: COMPLETO — 33 de 33 livros

Todos os livros da pasta `referencias/livros/` foram estudados e viraram resumo profundo
em `referencias/livros/resumos/`. O artigo "Como humanizar a marca" foi consolidado dentro
de primal-branding.md (mesmo conteúdo), por isso 34 PDFs geraram 33 resumos.

Ver a lista organizada por tema no arquivo INDICE.md.

## Livros que tiveram problema de arquivo (todos resolvidos)

- O Almanaque de Naval Ravikant: PDF era imagem escaneada. RESOLVIDO em 2026-07-12 com versão em texto fornecida por Henrique.
- Ferramentas Estratégicas (Vaughan Evans): PDF corrompido. RESOLVIDO em 2026-07-12 com o EPUB fornecido por Henrique (texto extraído do zip).

## Observações de catálogo

- Resumocast, livro nº 48 ("O Clique de Um Bilhão de Dólares", Filipe Vilicic): é sobre o Instagram (Systrom e Krieger), não o Google, apesar do título.

## Notas técnicas para futuras adições à biblioteca

- Leitura direta de PDF não funciona neste ambiente. Extrair texto antes com `scripts/extrair-texto-livros.py` (pypdf), salvando em `referencias/livros/texto/*.txt`.
- PDF escaneado (imagem) não tem texto extraível: pedir versão em texto ou EPUB.
- EPUB: descompactar como zip, ler os .xhtml/.html, decodificar utf-8, limpar tags.

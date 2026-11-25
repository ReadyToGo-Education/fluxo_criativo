# Especificacao do Painel de Entregas

Documento de referencia para construcao do template HTML do painel-entregas.
Define a estrutura de cada tela, o que e fixo (template) e o que e dinamico (substituicao por dados do produto).

---

## Sidebar (fixa em todas as telas)

### Estrutura

```
Painel de Entregas          <- FIXO
{nome_produto}              <- DINAMICO: perfil.md > nome do produto
{nome_comunicador}          <- DINAMICO: perfil.md > Identidade do Comunicador > Nome

PRODUTO                     <- FIXO (rotulo de grupo)
  Visao Geral               <- FIXO
  Quadro                    <- FIXO
  Furadeira                 <- FIXO
  Decorados                 <- FIXO
  Urgencias Ocultas         <- FIXO

IDENTIDADES                 <- FIXO (rotulo de grupo)
  Identidade do Produto     <- FIXO
  Identidade do Consumidor  <- FIXO
  Identidade do Comunicador <- FIXO

PESQUISA                    <- FIXO (rotulo de grupo)
  Pesquisa de Mercado       <- FIXO

[Exportar PDF (Ctrl+P)]     <- FIXO (botao, position fixed no fundo)
```

### Comportamento

- Item ativo: borda verde na esquerda + texto verde bold
- Clique em item: chama `showPanel(id)` que esconde todos e exibe o painel correspondente
- Botao Exportar: `window.print()`, CSS @media print expande accordions, esconde sidebar

### Versao mobile (< 768px)

- Sidebar some (`display: none`)
- Barra de tabs horizontal no topo (sticky), mesmos itens, scroll horizontal
- Tab ativa: borda inferior verde + texto verde bold

---

## Tela 1: Visao Geral

**Breadcrumb:** Painel de Entregas > Visao Geral (FIXO)
**Titulo:** Visao Geral (FIXO)
**Subtitulo:** Resumo do produto e informacoes principais. (FIXO)

### Componentes

| # | Componente | Layout | Conteudo |
|---|---|---|---|
| 1 | Grid 3 colunas | Card + Card + Card | Nome do Produto, Tipo, Preco |
| 2 | Card destaque verde | Full-width | Quadro (transformacao principal) |
| 3 | Grid 2 colunas | Card + Card | Nicho, Diferencial |
| 4 | Card status | Full-width | Produto ativo + tipo + preco + badges |

### Dados dinamicos

| Placeholder | Fonte | Campo |
|---|---|---|
| `{nome_produto}` | perfil.md | Nome do produto |
| `{subtitulo_produto}` | perfil.md | Descricao curta do produto |
| `{tipo_produto}` | tipo.md | Low Ticket / Middle Ticket |
| `{formato_produto}` | perfil.md | Identidade do Produto > Formato |
| `{preco}` | perfil.md | Preco |
| `{posicionamento_preco}` | pesquisa-mercado.md | Posicao relativa no nicho |
| `{quadro}` | perfil.md | Quadro |
| `{nicho}` | perfil.md | Nicho |
| `{nicho_subtitulo}` | perfil.md | Descricao do nicho |
| `{diferencial_titulo}` | perfil.md | Diferencial (titulo curto) |
| `{diferencial_descricao}` | perfil.md | Diferencial (explicacao) |
| `{badges_completude}` | Verificar existencia de arquivos | perfil.md, idconsumidor.md, urgencias no perfil |

### Elementos fixos

- Labels: "NOME DO PRODUTO", "TIPO", "PRECO", "QUADRO", "NICHO", "DIFERENCIAL"
- Texto do card status: "Produto ativo" + dot verde
- Estrutura visual dos cards

---

## Tela 2: Quadro

**Breadcrumb:** Painel de Entregas > Quadro (FIXO)
**Titulo:** Quadro (FIXO)
**Subtitulo:** A transformacao principal que o produto entrega ao cliente. (FIXO)

### Componentes

| # | Componente | Layout | Conteudo |
|---|---|---|---|
| 1 | Card destaque verde | Full-width | Quadro aprovado |
| 2 | Grid 2 colunas | Card + Card | Como usar o Quadro, Regra do Quadro |

### Dados dinamicos

| Placeholder | Fonte | Campo |
|---|---|---|
| `{quadro}` | perfil.md | Quadro |

### Elementos fixos (texto nao muda entre produtos)

- Label "QUADRO APROVADO"
- Card "COMO USAR O QUADRO": "O Quadro aparece em toda a comunicacao do produto: como headline da pagina de vendas, primeira linha de emails, abertura de anuncios e primeiro slide de carrossel. E a promessa central que ancora toda a copy."
- Card "REGRA DO QUADRO": "Teste obrigatorio: 'O aluno pode dizer que isso aconteceu na vida dele ao final do produto?' Se sim, o Quadro esta correto. O Quadro sempre descreve o resultado final, nunca o processo ou os modulos."

---

## Tela 3: Furadeira

**Breadcrumb:** Painel de Entregas > Furadeira (FIXO)
**Titulo:** Furadeira (FIXO)
**Subtitulo:** O metodo estruturado que torna visivel a eficiencia do produto. (FIXO)

### Componentes

| # | Componente | Layout | Conteudo |
|---|---|---|---|
| 1 | Card padrao | Full-width | Nome do metodo + badges (Mecanica, Eficiencia) |
| 2 | Card padrao | Full-width | Trilha do metodo (step timeline) - quando mecanica for Fases |
| 3 | Imagem PNG | Abaixo do card 2 | Furadeira visual gerada por /furadeira-visual |

### Dados dinamicos

| Placeholder | Fonte | Campo |
|---|---|---|
| `{nome_metodo}` | perfil.md | Furadeira > Nome do Metodo |
| `{mecanica}` | perfil.md | Furadeira > Mecanica(s) |
| `{eficiencia_principal}` | perfil.md | Furadeira > Eficiencia principal |
| `{macroetapas[]}` | perfil.md | Array de macroetapas (apenas quando mecanica for Fases e Sequencias) |
| `{img_furadeira_png}` | Verificar existencia | entregas/furadeira/furadeira.png (se existir) ou vazio |

### Elementos fixos

- Labels: "NOME DO METODO", "TRILHA DO METODO", "MECANICA", "EFICIENCIA"
- Badges: Mecanica em destaque + Eficiencia principal abaixo do nome do metodo
- Imagem PNG embutida (`<img>`) quando furadeira.png existir, dentro de card com fundo escuro

### Nota

- Quantidade de macroetapas e variavel (pode ter 3, 4, 5, etc.) e so aparece quando a mecanica for "Fases e Sequencias"
- Para outras mecanicas (Listas, Enquadramento, Logica Condicional, Empecilhos, Dinamica de Entrega) o painel renderiza apenas o nome + badges + imagem PNG (a estrutura textual completa fica no perfil.md, nao no painel)
- O template precisa iterar sobre o array de macroetapas quando aplicavel

---

## Tela 4: Decorados

**Breadcrumb:** Painel de Entregas > Decorados (FIXO)
**Titulo:** Decorados (FIXO)
**Subtitulo:** 50 beneficios derivados do Quadro. Use para bullets de pagina, scripts de venda e conteudo. (FIXO)

### Componentes

5 accordions, sempre nesta ordem:

| # | Categoria | Badge (cor) | Header |
|---|---|---|---|
| 1 | Financeiro | verde (badge-green) | "10 beneficios financeiros" |
| 2 | Tempo | azul (badge-blue) | "10 beneficios de tempo" |
| 3 | Autoestima | roxo (badge-purple) | "10 beneficios de autoestima" |
| 4 | Reputacao | laranja (badge-orange) | "10 beneficios de reputacao" |
| 5 | Crescimento | escuro (badge-dark) | "10 beneficios de crescimento" |

### Dados dinamicos

| Placeholder | Fonte | Campo |
|---|---|---|
| `{decorados_financeiro[10]}` | perfil.md | Decorados > Financeiro (10 itens) |
| `{decorados_tempo[10]}` | perfil.md | Decorados > Tempo (10 itens) |
| `{decorados_autoestima[10]}` | perfil.md | Decorados > Autoestima (10 itens) |
| `{decorados_reputacao[10]}` | perfil.md | Decorados > Reputacao (10 itens) |
| `{decorados_crescimento[10]}` | perfil.md | Decorados > Crescimento (10 itens) |

### Elementos fixos

- Categorias (sempre 5, sempre nessa ordem, sempre essas cores)
- Texto dos headers dos accordions
- Primeiro accordion aberto por padrao, demais fechados
- Marcador bullet verde antes de cada item

---

## Tela 5: Urgencias Ocultas

**Breadcrumb:** Painel de Entregas > Urgencias Ocultas (FIXO)
**Titulo:** Urgencias Ocultas (FIXO)
**Subtitulo:** 70 itens em 7 categorias. Use para temas de anuncio, bullets de pagina, ganchos de conteudo e linhas de email. (FIXO)

### Componentes

7 accordions, sempre nesta ordem:

| # | Categoria | Descricao | Badge (cor) | Header |
|---|---|---|---|---|
| 1 | Dores | O que incomoda | rosa (badge-pink) | "O que incomoda · 10 itens" |
| 2 | Duvidas | O que pergunta | indigo (badge-indigo) | "O que pergunta · 10 itens" |
| 3 | Desejos | O que sonha | violeta (badge-violet) | "O que sonha · 10 itens" |
| 4 | Assuntos Relacionados | Porta de entrada | verde (badge-green) | "Porta de entrada · 10 itens" |
| 5 | Urgencias Quentes | Alta intencao | laranja (badge-orange) | "Alta intencao · 10 itens" |
| 6 | Urgencias Frias | Alto volume | neutro (badge-neutral) | "Alto volume · 10 itens" |
| 7 | Urgencias Inusitadas | Angulos inesperados | roxo (badge-purple) | "Angulos inesperados · 10 itens" |

### Dados dinamicos

| Placeholder | Fonte | Campo |
|---|---|---|
| `{urgencias_dores[10]}` | perfil.md | Urgencias Ocultas > Dores |
| `{urgencias_duvidas[10]}` | perfil.md | Urgencias Ocultas > Duvidas |
| `{urgencias_desejos[10]}` | perfil.md | Urgencias Ocultas > Desejos |
| `{urgencias_assuntos[10]}` | perfil.md | Urgencias Ocultas > Assuntos Relacionados |
| `{urgencias_quentes[10]}` | perfil.md | Urgencias Ocultas > Urgencias Quentes |
| `{urgencias_frias[10]}` | perfil.md | Urgencias Ocultas > Urgencias Frias |
| `{urgencias_inusitadas[10]}` | perfil.md | Urgencias Ocultas > Urgencias Inusitadas |

### Elementos fixos

- Categorias (sempre 7, sempre nessa ordem, sempre essas cores e descricoes)
- Estrutura identica aos Decorados (mesmo codigo de accordion, so muda quantidade e dados)
- Primeiro accordion aberto por padrao

---

## Tela 6: Identidade do Produto

**Breadcrumb:** Painel de Entregas > Identidade do Produto (FIXO)
**Titulo:** Identidade do Produto (FIXO)
**Subtitulo:** Como o produto se posiciona e se diferencia no mercado. (FIXO)

### Componentes

| # | Componente | Layout | Conteudo |
|---|---|---|---|
| 1 | Grid 2 colunas | Card + Card | Diferencial Principal, Formato |
| 2 | Card full-width | Lista com bullets | Argumentos Incontestaveis |
| 3 | Card full-width | Accordions aninhados | Quebra de Objecoes (5 objecoes x 7 argumentos) |

### Dados dinamicos

| Placeholder | Fonte | Campo |
|---|---|---|
| `{diferencial_texto}` | perfil.md | Diferencial completo |
| `{formato_texto}` | perfil.md | Identidade do Produto > Formato (descricao completa) |
| `{argumentos_incontestaveis[]}` | perfil.md | Argumentos Incontestaveis (4-6 itens) |
| `{objecoes[5]}` | idconsumidor.md | Array de 5 objecoes, cada uma contendo: |
|  |  | `.texto` = frase da objecao |
|  |  | `.argumentos[7]` = array de 7 argumentos |
|  |  | Cada argumento tem: `.titulo`, `.paragrafo1`, `.paragrafo2` |

### Elementos fixos

- Labels: "DIFERENCIAL PRINCIPAL", "FORMATO", "ARGUMENTOS INCONTESTAVEIS"
- Titulo da secao de objecoes: "QUEBRA DE OBJECOES. FRAMEWORK DOS 7 ARGUMENTOS"
- Subtitulo: "5 objecoes principais x 7 argumentos cada. Fonte usada por copy, anuncio, email e call 1:1."
- Badges rosas "Objecao 1" a "Objecao 5"
- Nomes dos 7 argumentos (sempre na mesma ordem):
  1. Argumento incontestavel
  2. Argumento logico (causa e efeito)
  3. Argumento por analogia
  4. Argumento por exemplificacao
  5. Argumento de valor
  6. Argumento de consequencia
  7. Argumento de contradicao
- Borda verde na esquerda de cada bloco de argumento
- Accordions: fechados por padrao

### Nota sobre peso

- Esta tela gera 5 x 7 x 2 = 70 paragrafos de texto
- E a segunda tela mais pesada do painel
- Os paragrafos vem do idconsumidor.md, secao "Objecoes de Compra"

---

## Tela 7: Identidade do Consumidor

**Breadcrumb:** Painel de Entregas > Identidade do Consumidor (FIXO)
**Titulo:** Identidade do Consumidor (FIXO)
**Subtitulo:** Perfil detalhado do cliente ideal. (FIXO)

### Componentes

| # | Componente | Layout | Conteudo |
|---|---|---|---|
| 1 | Card destaque verde | Full-width | Para Quem E |
| 2 | Grid 2 colunas | Card + Card | Perfil Demografico, Comportamento e Canais |
| 3 | Card full-width | Lista com bullets | Paliativos (SO MIDDLE TICKET) |
| 4 | Card full-width | Accordions | Baldes de Para Quem E |

### Dados dinamicos

| Placeholder | Fonte | Campo |
|---|---|---|
| `{para_quem_e}` | idconsumidor.md | Para Quem E (frase de posicionamento) |
| `{genero}` | idconsumidor.md | Genero |
| `{idade}` | idconsumidor.md | Idade |
| `{profissao}` | idconsumidor.md | Profissao |
| `{renda}` | idconsumidor.md | Renda |
| `{localizacao}` | idconsumidor.md | Localizacao |
| `{nivel_consciencia}` | idconsumidor.md | Nivel de consciencia |
| `{onde_busca_info}` | idconsumidor.md | Onde busca informacao |
| `{conteudo_consome}` | idconsumidor.md | Conteudo que consome |
| `{como_compra}` | idconsumidor.md | Como compra |
| `{sonho}` | idconsumidor.md | Sonho (frase direta) |
| `{paliativos[]}` | idconsumidor.md | Array de paliativos (ferramenta → dor que resolve) |
| `{baldes[]}` | idconsumidor.md | Array de baldes, cada um com: nome do perfil + 5 afirmacoes |

### Elementos fixos

- Labels: "PARA QUEM E", "PERFIL DEMOGRAFICO", "COMPORTAMENTO E CANAIS", "PALIATIVOS", "BALDES DE PARA QUEM E"
- Labels dos campos demograficos em bold (Genero:, Idade:, etc.)
- Badges neutras nos headers dos baldes
- Primeiro balde aberto por padrao

### Regra condicional

- **Paliativos**: so renderizar se tipo.md = "Middle Ticket". Se Low Ticket, omitir a secao inteira.

---

## Tela 8: Identidade do Comunicador

**Breadcrumb:** Painel de Entregas > Identidade do Comunicador (FIXO)
**Titulo:** Identidade do Comunicador (FIXO)
**Subtitulo:** Tom, posicionamento e linguagem do criador. (FIXO)

### Componentes

| # | Componente | Layout | Conteudo |
|---|---|---|---|
| 1 | Grid 3 colunas | Card + Card + Card | Comunicador, Valores, Tonalidade Emocional |
| 2 | Card full-width | Blockquotes | Mantras e Jargoes Proprios |
| 3 | Grid 2 colunas | Card + Card | Tom de Voz, Posicionamento Pessoal |
| 4 | Grid 2 colunas | Card + Card | Formatos que Combinam, Estilo Visual Recomendado |
| 5 | Card full-width | Lista | Referencias Comunicacionais |
| 6 | Grid 2 colunas | Card + Card | Palavras que Conectam, Palavras que Afastam |

### Dados dinamicos

| Placeholder | Fonte | Campo |
|---|---|---|
| `{comunicador_nome}` | perfil.md | Identidade do Comunicador > Nome |
| `{comunicador_especialidade}` | perfil.md | Identidade do Comunicador > Especialidade |
| `{valores[]}` | perfil.md | Valores (pills verdes) |
| `{tonalidade_emocional}` | perfil.md | Tonalidade emocional predominante |
| `{mantras[]}` | perfil.md | Mantras/Jargoes proprios (array de frases) |
| `{tom_de_voz}` | perfil.md | Tom de voz (paragrafo) |
| `{posicionamento}` | perfil.md | Posicionamento pessoal (paragrafo) |
| `{formatos[]}` | perfil.md | Formatos que combinam (lista) |
| `{estilo_visual[]}` | perfil.md | Estilo visual recomendado (pills neutras) |
| `{referencias[]}` | perfil.md | Referencias de comunicacao (nome + descricao) |
| `{palavras_conectam[]}` | idconsumidor.md | Palavras que conectam (pills verdes) |
| `{palavras_afastam[]}` | idconsumidor.md | Palavras que afastam (pills rosas) |

### Elementos fixos

- Labels de todos os cards
- Estrutura visual: pills, blockquotes com borda verde, bullets

---

## Tela 9: Pesquisa de Mercado

**Breadcrumb:** Painel de Entregas > Pesquisa de Mercado (FIXO)
**Titulo:** Pesquisa de Mercado (FIXO)
**Subtitulo:** Dashboard de inteligencia de mercado. Use para argumentos, copy e posicionamento. (FIXO)

### Bloco 1: KPIs (grid 4 colunas)

| Card | Placeholder | Fonte |
|---|---|---|
| Tamanho do Mercado | `{mercado_tamanho}`, `{mercado_trend}` | pesquisa-mercado.md |
| Crescimento Anual | `{mercado_crescimento}`, `{crescimento_trend}` | pesquisa-mercado.md |
| Concorrentes Mapeados | `{qtd_concorrentes}` | pesquisa-mercado.md |
| Ticket Medio do Nicho | `{ticket_medio}`, `{ticket_trend}` | pesquisa-mercado.md |

Cada card tem: label (FIXO), valor grande, trend (seta + texto), sparkline SVG.
Sparklines: SVG inline com path curvo, altura 36px. Formato fixo no template, dados dos pontos dinamicos.

### Bloco 2: Graficos (grid 2 colunas)

**Esquerda: Area Chart SVG "CRESCIMENTO DO MERCADO (5 ANOS)"**

| Placeholder | Fonte |
|---|---|
| `{crescimento_anos[5]}` | pesquisa-mercado.md (ex: 2020, 2021, 2022, 2023, 2024) |
| `{crescimento_valores[5]}` | pesquisa-mercado.md (valores por ano) |
| `{crescimento_fonte}` | pesquisa-mercado.md (ex: "SEBRAE, Portal do Empreendedor") |

Estrutura SVG fixa (viewBox, gridlines, eixos). Pontos e path dinamicos.

**Direita: Donut Chart SVG "RECLAMACOES POR CATEGORIA"**

| Placeholder | Fonte |
|---|---|
| `{reclamacoes[]}` | pesquisa-mercado.md | Array com: categoria, percentual, cor |
| `{reclamacao_dominante_pct}` | pesquisa-mercado.md (% no centro do donut) |
| `{reclamacao_dominante_label}` | pesquisa-mercado.md (label no centro) |

Estrutura SVG fixa (circulo base, segmentos via stroke-dasharray). Valores e cores dinamicos.

### Bloco 3: Oportunidades Identificadas (card full-width)

| Placeholder | Fonte |
|---|---|
| `{oportunidades[]}` | pesquisa-mercado.md | Array de 5-8 oportunidades (texto) |

Fixo: label verde "OPORTUNIDADES IDENTIFICADAS", circulos numerados verdes, separadores.

### Bloco 4: Grid 2 colunas

**Esquerda: Bar Chart SVG "PRECO MEDIO POR FORMATO"**

| Placeholder | Fonte |
|---|---|
| `{precos_formato[]}` | pesquisa-mercado.md | Array com: formato, valor |
| `{formato_produto_atual}` | perfil.md | Para destacar "SEU PRODUTO" |

Estrutura SVG fixa. Barras e valores dinamicos. Barra do produto atual com destaque.

**Direita: TOP 5 CONCORRENTES**

| Placeholder | Fonte |
|---|---|
| `{top5[]}` | pesquisa-mercado.md | Array com: nome, inicial, cor_avatar, preco, link_pagina, link_instagram |

Fixo: layout de lista com avatar circular. Links so aparecem se existirem (nunca google.com/search).

### Bloco 5: Grid 2 colunas

**Card "CUIDADOS E RISCOS"**

| Placeholder | Fonte |
|---|---|
| `{cuidados[]}` | pesquisa-mercado.md | Array de alertas (texto laranja) |

**Card "PADROES DE RECLAMACAO (RECLAME AQUI)"**

| Placeholder | Fonte |
|---|---|
| `{padroes_reclamacao[]}` | pesquisa-mercado.md | Array com: categoria, percentual |

Fixo: barras horizontais CSS proporcionais ao percentual.

### Bloco 6: Tabela completa de concorrentes (card full-width)

| Placeholder | Fonte |
|---|---|
| `{concorrentes_tabela[]}` | pesquisa-mercado.md | Array com: nome, promessa, formato, preco, link_pagina |

Fixo: colunas "NOME", "PROMESSA PRINCIPAL", "FORMATO", "PRECO", "LINKS". Badges de preco coloridas por faixa. Links so se URL real existir.

### Bloco 7: Grid 2 colunas

**Card "TERMOS EM ALTA"**

| Placeholder | Fonte |
|---|---|
| `{termos_alta[]}` | pesquisa-mercado.md | Array de termos (pills verdes, tamanhos variados) |

**Card "PADROES DE ANUNCIO QUE PERFORMAM"**

| Placeholder | Fonte |
|---|---|
| `{padroes_anuncio[]}` | pesquisa-mercado.md | Array de padroes (lista com bullets) |

### Bloco 8: Top 10 Videos YouTube (card full-width)

**Tabela visual de 10 linhas:**

| Placeholder | Fonte |
|---|---|
| `{youtube_videos[10]}` | pesquisa-mercado.md | Array com: ranking, thumb_texto, thumb_cor, titulo, canal, views, link_youtube |

Fixo: colunas #, THUMB, TITULO + CANAL, VIEWS, LINK. Thumb e um div colorido com texto curto.

**Accordion "Ver detalhes de cada video":**

| Placeholder | Fonte |
|---|---|
| `{youtube_detalhes[10]}` | pesquisa-mercado.md | Array com: titulo, canal, thumbnail_descricao, comentarios[3], angulo, lacuna_produto |

Cada detalhe tem: titulo bold, thumbnail descrita, 3 blockquotes de comentarios (borda verde), angulo, lacuna para o produto.

### Bloco 9: Card destaque verde "PADRAO IDENTIFICADO NOS 10 VIDEOS"

| Placeholder | Fonte |
|---|---|
| `{padroes_youtube[4]}` | pesquisa-mercado.md | 4 padroes observados (bullets com texto bold no inicio) |

### Bloco 10: Card alaranjado "ALERTAS REGULATORIOS"

| Placeholder | Fonte |
|---|---|
| `{alertas_regulatorios_texto}` | pesquisa-mercado.md | Texto de aviso |
| `{expressoes_proibidas[]}` | pesquisa-mercado.md | Pills laranjas com expressoes a evitar |

Condicional: so renderizar se houver dados relevantes.

### Bloco 11: Footer (grid 2 colunas)

**Esquerda: Circular Progress SVG**

| Placeholder | Fonte |
|---|---|
| `{confianca_pct}` | pesquisa-mercado.md | Percentual (ex: 87%) |
| `{confianca_nivel}` | Calculado | Alta (88-100), Media (50-65), Baixa (20-35) |

Fixo: SVG 120x120, circulo base + overlay. Cor muda por nivel: verde (Alta), laranja (Media), vermelho (Baixa).

**Direita: Fontes Consultadas**

| Placeholder | Fonte |
|---|---|
| `{fontes[]}` | pesquisa-mercado.md | Array com: nome, descricao (max 8, layout 2 colunas CSS) |

---

## Resumo: Fontes de Dados

| Arquivo | Telas que usam |
|---|---|
| `perfil.md` | 1, 2, 3, 4, 5, 6, 8, 9 |
| `idconsumidor.md` | 6, 7, 8 |
| `pesquisa-mercado.md` | 1, 9 |
| `tipo.md` | 1, 7 (condicional paliativos) |

---

## Resumo: Peso por Tela

| Tela | Peso | Motivo |
|---|---|---|
| 1. Visao Geral | Leve | Poucos campos, sem listas longas |
| 2. Quadro | Leve | 1 dado dinamico + 2 textos fixos |
| 3. Furadeira | Medio | Timeline variavel (3-6 macroetapas) |
| 4. Decorados | Medio | 50 itens em 5 accordions |
| 5. Urgencias Ocultas | Medio | 70 itens em 7 accordions |
| 6. Identidade do Produto | Pesado | 70 paragrafos de objecoes |
| 7. Identidade do Consumidor | Medio | Perfil + baldes variaveis |
| 8. Identidade do Comunicador | Leve-Medio | Muitos campos, pouco texto longo |
| 9. Pesquisa de Mercado | Muito Pesado | 6 graficos SVG + tabelas + YouTube detalhado |

---

## Componentes Reutilizaveis (template)

Estes componentes aparecem em multiplas telas e devem ser definidos uma vez no template:

| Componente | Usado em |
|---|---|
| Card padrao | Todas as telas |
| Card destaque verde | Telas 1, 2, 7, 9 |
| Accordion | Telas 4, 5, 6, 7, 8, 9 |
| Grid 2 colunas | Telas 1, 2, 3, 6, 7, 8, 9 |
| Grid 3 colunas | Telas 1, 8 |
| Grid 4 colunas | Tela 9 |
| Step timeline | Tela 3 |
| Badge/pill | Todas as telas |
| Tabela | Tela 9 |
| Graficos SVG (sparkline, area, donut, bar, circular progress) | Tela 9 |
| Blockquote com borda verde | Telas 6, 8, 9 |
| Botao primario | Telas 3, sidebar |

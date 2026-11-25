# Plano: Validacao e Build do Painel de Entregas

## Objetivo

Garantir que o painel-entregas.html saia completo e correto independente de como o LLM formata o output. O script parseia os .md, valida, gera .json como cache, monta o painel e retorna warnings pro agente corrigir.

---

## Arquitetura

```
LLM gera .md (como sempre, sem mudanca)
        |
        v
build-painel-entregas.py
  1. Le perfil.md, idconsumidor.md, pesquisa-mercado.md, tipo.md
  2. Parseia e valida cada campo (checklist abaixo)
  3. Salva .json como cache (perfil.json, idconsumidor.json, pesquisa-dados.json)
  4. Gera painel-entregas.html usando o template + dados do .json
  5. Retorna relatorio de validacao (stdout)
        |
        v
Agente le o relatorio
  - Se tudo OK: informa o aluno que o painel esta pronto
  - Se tem avisos: corrige o .md e roda o script de novo
```

---

## Fase 1: Checklist de validacao do perfil.md

O script deve verificar a existencia e completude de cada campo:

### Tela 1: Visao Geral
| Campo | Onde encontrar | Validacao |
|---|---|---|
| Nome do produto | Titulo do arquivo ou **Nome:** | Nao vazio |
| Tipo | tipo.md | "Low Ticket" ou "Middle Ticket" |
| Preco | **Preco:** | Formato R$ + numero |
| Quadro | ## Quadro | Nao vazio, max 15 palavras |
| Nicho | **Nicho:** | Nao vazio |
| Diferencial | **Diferencial:** | Nao vazio |

### Tela 2: Quadro
| Campo | Validacao |
|---|---|
| Quadro | Mesmo do Visao Geral (reuso) |

### Tela 3: Furadeira
| Campo | Onde encontrar | Validacao |
|---|---|---|
| Nome do metodo | **Nome do Metodo:** | Nao vazio |
| Macroetapas | ### dentro de ## Furadeira, ou lista numerada | Minimo 2 macroetapas |
| Cada macroetapa | Titulo + descricao | Titulo nao vazio |

### Tela 4: Decorados
| Campo | Validacao |
|---|---|
| Financeiro | Exatamente 10 itens |
| Tempo | Exatamente 10 itens |
| Autoestima | Exatamente 10 itens |
| Reputacao | Exatamente 10 itens |
| Crescimento | Exatamente 10 itens |
| Total | 50 itens |

### Tela 5: Urgencias Ocultas
| Campo | Validacao |
|---|---|
| Dores | Exatamente 10 itens |
| Duvidas | Exatamente 10 itens |
| Desejos | Exatamente 10 itens |
| Assuntos Relacionados | Exatamente 10 itens |
| Urgencias Quentes | Exatamente 10 itens |
| Urgencias Frias | Exatamente 10 itens |
| Urgencias Inusitadas | Exatamente 10 itens |
| Total | 70 itens |

### Tela 8: Identidade do Comunicador
| Campo | Onde encontrar | Validacao |
|---|---|---|
| Nome | **Nome:** | Nao vazio |
| Especialidade | **Especialidade:** | Nao vazio |
| Valores | **Valores:** | 1-4 valores |
| Tom de voz | **Tom de voz:** | Nao vazio |
| Posicionamento | **Posicionamento pessoal:** | Nao vazio |
| Tonalidade emocional | **Tonalidade emocional:** | Nao vazio |
| Mantras | **Mantras/Jargoes:** | Pode ser "Nenhum ainda" |
| Referencias | **Referencias comunicacionais:** | Pelo menos 1 |
| Formatos | **Formatos que combinam:** | Pelo menos 1 |
| Estilo visual | **Elementos visuais:** | Pelo menos 1 |

### Argumentos Incontestaveis
| Campo | Validacao |
|---|---|
| Lista de argumentos | Minimo 4 itens com fonte/dado |

---

## Fase 2: Checklist de validacao do idconsumidor.md

### Tela 6: Identidade do Produto (objecoes)
| Campo | Validacao |
|---|---|
| Objecoes | Exatamente 5 objecoes |
| Cada objecao | 7 argumentos |
| Cada argumento | 1-2 paragrafos nao vazios |

### Tela 7: Identidade do Consumidor
| Campo | Onde encontrar | Validacao |
|---|---|---|
| Para Quem E | ## Para Quem | Nao vazio |
| Genero | **Genero:** | Nao vazio |
| Idade | **Idade:** | Nao vazio |
| Profissao | **Profissao:** | Nao vazio |
| Renda | **Renda:** | Nao vazio |
| Localizacao | **Localizacao:** | Nao vazio |
| Nivel consciencia | **Nivel de consciencia:** | Nao vazio |
| Onde busca info | **Onde busca informacao:** | Nao vazio |
| Palavras conectam | **Palavras que conectam:** | Minimo 5 |
| Palavras afastam | **Palavras que afastam:** | Minimo 5 |
| Baldes | Secao Baldes | 3-5 baldes, cada um com 5 itens |
| Paliativos (Middle Ticket) | Secao Paliativos | Minimo 3 se Middle Ticket |

---

## Fase 3: Checklist de validacao do pesquisa-mercado.md

### Tela 9: Pesquisa de Mercado
| Campo | Onde encontrar | Validacao |
|---|---|---|
| Tamanho do mercado | Secao KPIs ou Tamanho | Valor numerico com unidade |
| Crescimento anual | Secao KPIs ou Crescimento | Percentual |
| Concorrentes mapeados | Tabela de concorrentes | Minimo 5 |
| Ticket medio | Calculado da tabela | Valor numerico |
| Crescimento 5 anos | Secao Crescimento | 5 pares ano/valor |
| Reclamacoes | Secao Reclamacoes | Minimo 3 categorias com % |
| Oportunidades | Secao Oportunidades | Minimo 5 |
| Precos por formato | Tabela de concorrentes | Minimo 3 faixas |
| Top 5 concorrentes | Tabela | Nome, preco, link (se disponivel) |
| Cuidados e riscos | Secao Riscos/Cuidados | Minimo 3 |
| Tabela completa | Tabela de concorrentes | Minimo 5 linhas completas |
| Termos em alta | Secao Termos/Trending | Minimo 5 |
| Padroes de anuncio | Secao Anuncios/Padroes | Minimo 3 |
| Top 10 YouTube | Secao YouTube | 10 videos com titulo, canal, views, link |
| Detalhes YouTube | Dentro de cada video | Thumbnail, 3 comentarios, angulo, lacuna |
| Padroes YouTube | Secao Padroes | 3-4 padroes observados |
| Alertas regulatorios | Secao Alertas | Lista de expressoes proibidas |
| Confianca | Autoavaliacao | Percentual |
| Fontes | Secao Fontes | Minimo 4 fontes nomeadas |

---

## Fase 4: Schema JSON

### perfil.json
```json
{
  "nome_produto": "string",
  "quadro": "string",
  "furadeira": {
    "nome_metodo": "string",
    "macroetapas": [
      {"num": 1, "titulo": "string", "desc": "string"}
    ]
  },
  "identidade_produto": {
    "nome": "string",
    "formato": "string",
    "preco": "string",
    "diferencial": "string"
  },
  "identidade_consumidor_resumo": {
    "nicho": "string",
    "publico": "string",
    "nivel_consciencia": "string"
  },
  "identidade_comunicador": {
    "nome": "string",
    "especialidade": "string",
    "valores": ["string"],
    "tom_de_voz": "string",
    "posicionamento": "string",
    "tonalidade_emocional": "string",
    "mantras": ["string"],
    "referencias": [{"nome": "string", "desc": "string"}],
    "formatos": ["string"],
    "estilo_visual": ["string"],
    "evitar": "string",
    "vocabulario": "string"
  },
  "decorados": {
    "financeiro": ["string (10)"],
    "tempo": ["string (10)"],
    "autoestima": ["string (10)"],
    "reputacao": ["string (10)"],
    "crescimento": ["string (10)"]
  },
  "urgencias": {
    "dores": ["string (10)"],
    "duvidas": ["string (10)"],
    "desejos": ["string (10)"],
    "assuntos_relacionados": ["string (10)"],
    "urgencias_quentes": ["string (10)"],
    "urgencias_frias": ["string (10)"],
    "urgencias_inusitadas": ["string (10)"]
  },
  "argumentos_incontestaveis": ["string"]
}
```

### idconsumidor.json
```json
{
  "para_quem_e": "string",
  "perfil": {
    "genero": "string",
    "idade": "string",
    "profissao": "string",
    "renda": "string",
    "localizacao": "string",
    "nivel_consciencia": "string",
    "onde_busca": "string"
  },
  "comportamento": {
    "conteudo_consome": "string",
    "como_compra": "string",
    "sonho": "string"
  },
  "paliativos": [
    {"ferramenta": "string", "resolve": "string"}
  ],
  "objecoes": [
    {
      "texto": "string",
      "argumentos": [
        {"titulo": "string", "paragrafos": ["string"]}
      ]
    }
  ],
  "frases": ["string"],
  "comunicacao": {
    "tom": "string",
    "palavras_conectam": ["string"],
    "palavras_afastam": ["string"]
  },
  "baldes": [
    {"nome": "string", "itens": ["string (5)"]}
  ]
}
```

### pesquisa-dados.json
```json
{
  "kpis": {
    "tamanho_mercado": {"valor": "string", "trend": "string"},
    "crescimento_anual": {"valor": "string", "trend": "string"},
    "concorrentes_mapeados": {"valor": "number", "trend": "string"},
    "ticket_medio": {"valor": "string", "trend": "string"}
  },
  "crescimento_5anos": [
    {"ano": "2020", "valor": "string"}
  ],
  "reclamacoes": [
    {"categoria": "string", "percentual": "number", "cor": "string"}
  ],
  "oportunidades": ["string"],
  "precos_formato": [
    {"formato": "string", "preco": "number", "destaque": "boolean"}
  ],
  "top5_concorrentes": [
    {
      "nome": "string",
      "inicial": "string",
      "cor": "string",
      "preco": "string",
      "link_pagina": "string ou null",
      "link_instagram": "string ou null"
    }
  ],
  "cuidados": ["string"],
  "tabela_concorrentes": [
    {"nome": "string", "promessa": "string", "formato": "string", "preco": "string", "link": "string ou null"}
  ],
  "termos_alta": [
    {"termo": "string", "intensidade": "alta ou media"}
  ],
  "padroes_anuncio": ["string"],
  "youtube_top10": [
    {
      "ranking": "number",
      "titulo": "string",
      "canal": "string",
      "views": "string",
      "link": "string",
      "thumb_texto": "string",
      "thumb_cor1": "string",
      "thumb_cor2": "string",
      "thumbnail_desc": "string",
      "comentarios": ["string (3)"],
      "angulo": "string",
      "lacuna": "string"
    }
  ],
  "padroes_youtube": [
    {"destaque": "string", "detalhe": "string"}
  ],
  "alertas_regulatorios": {
    "texto": "string",
    "expressoes": ["string"]
  },
  "confianca": {"percentual": "number", "nivel": "Alta|Media|Baixa"},
  "fontes": [
    {"nome": "string", "descricao": "string"}
  ]
}
```

---

## Fase 5: Formato do relatorio de validacao

O script retorna via stdout um relatorio que o agente le:

```
=== VALIDACAO DO PAINEL DE ENTREGAS ===
Produto: {slug}

PERFIL.MD
  [OK] Quadro: "Organizar as financas..."
  [OK] Furadeira: Metodo CFO Solo (4 macroetapas)
  [OK] Decorados: 50/50 itens
  [!!] Urgencias > Inusitadas: 7/10 itens (faltam 3)
  [OK] Comunicador: completo
  [!!] Mantras: vazio (preencher ou marcar "Nenhum ainda")
  [OK] Argumentos: 5 itens

IDCONSUMIDOR.MD
  [OK] Para Quem E: preenchido
  [OK] Perfil demografico: 6/6 campos
  [OK] Objecoes: 5/5 com 7 argumentos cada
  [!!] Baldes: 4/5 baldes (falta 1)
  [OK] Palavras conectam: 13 itens
  [OK] Palavras afastam: 10 itens

PESQUISA-MERCADO.MD
  [OK] KPIs: 4/4
  [OK] Concorrentes: 10 mapeados
  [!!] YouTube: secao nao encontrada
  [!!] Alertas regulatorios: secao nao encontrada
  [OK] Fontes: 6 consultadas

RESULTADO: 4 avisos. Painel gerado com secoes incompletas.
Secoes afetadas: Urgencias Ocultas, Comunicador, Consumidor, Pesquisa.

Corrigir e rodar novamente:
  py -3 scripts/build-painel-entregas.py
```

---

## Fase 6: Ordem de implementacao

| Prioridade | Tarefa | Impacto |
|---|---|---|
| 1 | Atualizar `build-painel-entregas.py` com validacao e warnings | O script ja existe, so adicionar validacao |
| 2 | Gerar .json como cache apos parsing | Permite o painel ler dados parseados sem refazer regex |
| 3 | Atualizar template pesquisa de mercado com todos os blocos visuais | Painel de pesquisa sai completo |
| 4 | Atualizar parser de pesquisa-mercado.md pra extrair YouTube, KPIs, etc. | Alimenta os novos blocos visuais |
| 5 | Padronizar saida da skill /pesquisa-mercado pra incluir secoes estruturadas | Garante que o parser sempre encontra os dados |
| 6 | Adicionar instrucao nos commands pra ler o relatorio e corrigir | Agente fecha o loop automaticamente |

---

## Regra pro agente (adicionar nos commands)

Apos rodar `py -3 scripts/build-painel-entregas.py`, leia o output do script. Se houver avisos `[!!]`, corrija os campos no .md correspondente e rode o script novamente. Repita ate nao ter mais avisos. So entao informe o aluno que o painel esta pronto.

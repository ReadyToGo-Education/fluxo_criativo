# Sub-fluxo. Público Semelhante (Lookalike)

Cria um público semelhante (lookalike) a partir de um público personalizado que já existe. Semelhante = pessoas que se parecem (comportamento e características) com a origem.

Passo 0 (produto ativo, conexão, conta) e gate: ver `SKILL.md` desta skill.

## Perguntas que cobre

- "Cria uma lookalike dos meus compradores"
- "Lookalike 1% do meu público de carrinho abandonado"
- "Semelhante 2% dos visitantes do site"
- "Cria uma lookalike de quem viu 75% do meu vídeo"

## Inputs

| Input | Padrão | Descrição |
|---|---|---|
| `source` | obrigatório | Público de origem, escolhido por nome ou listagem (o aluno nunca digita ID) |
| `percentual` | 1 | 1 a 10 |
| `pais` | `BR` | País do semelhante |
| `nome_extra` | descrição da origem | Sufixo do nome |

## Roteamento por modo (ler primeiro)

- **`MCP_CONECTOR` (padrão):** listar as origens com `ads_get_ad_account_custom_audiences` (detalhe por `ads_get_custom_audience`) e criar com `ads_create_custom_audience` usando o subtipo `LOOKALIKE`. Ler o schema da tool antes da primeira chamada e preencher os campos de origem, país e tamanho que ele pedir (não inventar parâmetro). Depois de criar, conferir com `ads_get_custom_audience`. Se a Meta recusar o subtipo pelo conector, seguir pelo passo manual guiado abaixo.
- **`APP`:** listar e criar por `curl` (endpoints abaixo).

### Passo manual guiado (recusa pelo conector)

```
Você cria em 1 minuto no Gerenciador:

📋 Passo 1. Gerenciador de Anúncios → menu "Públicos" → "Criar público" →
           "Público semelhante"
📋 Passo 2. Origem: escolha "{nome_source}"
📋 Passo 3. Local: {país em português}
📋 Passo 4. Tamanho: {percentual}% {se vários: marque {lista de percentuais}}
📋 Passo 5. Clique em "Criar público"

🛟 Se algum nome de botão estiver diferente, me mande um print.

Me avise com "feito" que eu confiro pela listagem.
```

## Coleta de inputs (uma pergunta por mensagem)

Regra dura: **nunca agrupar 2 ou mais inputs na mesma mensagem**. O aluno **nunca digita ID**.

### Ordem fixa

1. **Público de origem.**
   ```
   De qual público você quer criar o semelhante? (digite o nome, completo ou em parte, ou peça para eu listar)
   ```
   Aceita 3 formas (mesmo padrão da coleta por nome da `trafego-regras/sub-skills/regra-automatica.md`):
   - **(a) Nome, completo ou em parte:** listar os públicos (MCP: `ads_get_ad_account_custom_audiences`; App: `GET -g /act_<id>/customaudiences?fields=id,name,subtype,approximate_count_lower_bound,approximate_count_upper_bound,retention_days,permission_for_actions{subtype_supports_lookalike,supports_recipient_lookalike}`), manter só os elegíveis (`subtype != LOOKALIKE` **e** `permission_for_actions.subtype_supports_lookalike == true` **e** `permission_for_actions.supports_recipient_lookalike == true`) e procurar o trecho no nome. 1 resultado: confirmar. Vários: lista numerada.
   - **(b) Listar:** "lista", "não lembro": mostrar só os **elegíveis**, com nome, tamanho e tipo.
   - **(c) ID direto** (raro): conferir pela leitura do público.

   Se o retorno do MCP não trouxer `permission_for_actions`, filtrar por `subtype != LOOKALIKE` e tratar a recusa da Meta (erro 2654) na criação.

   **Bloqueio em 3 níveis (depois da escolha):**
   - `subtype == LOOKALIKE`: "Não dá para fazer semelhante de semelhante. Escolha outro." e voltar ao passo 1.
   - `permission_for_actions.supports_recipient_lookalike == false`: "Esse público foi compartilhado de outro Business sem a permissão 'Criar públicos semelhantes'. A Meta vai recusar (erro 2654). Como quer seguir? [1] Trocar de origem, [2] Pedir à equipe dona para compartilhar de novo marcando 'Compartilhar para criar públicos semelhantes', [3] Criar uma origem nova pela lista de clientes (opção 6 do menu)". Não levar ao bloco 🛡️.
   - `approximate_count_lower_bound < 100`: "O público de origem tem só ~{N} pessoas. O mínimo é 100. Espere crescer ou escolha outro."

   **Nenhum público elegível** (conta cuja base inteira veio compartilhada sem permissão de semelhante):
   ```
   Olhei os {N} públicos da sua conta. Nenhum permite criar semelhante (todos vieram
   compartilhados de outro Business sem marcar "Compartilhar para criar públicos
   semelhantes").

   Como quer seguir?

   1. Subir uma lista nova de compradores (CSV)
      → o público nasce na sua conta e o semelhante funciona na hora
      → /trafego-publicos opção 6
   2. Pedir à equipe que administra os Business para compartilhar de novo,
      marcando "Compartilhar para criar públicos semelhantes"
      (Business → Públicos → público → Compartilhar)
   3. Cancelar agora
   ```

   Mesmo quando o aluno pedir a lista inteira, mostrar só os elegíveis.

2. **Tamanho.**
   ```
   Qual o tamanho do semelhante?

   1. 1% (~2 milhões de pessoas no Brasil; mais parecido, padrão recomendado)
   2. 2% (~4 milhões; bom para escala)
   3. 3% (~6 milhões)
   4. 5% (~10 milhões; escala agressiva, a qualidade cai)
   5. 10% (~20 milhões; quase público frio, última opção)
   6. Outro (digito o número)
   7. Criar vários de uma vez (1%, 2% e 5%, ou personalizado)

   Digite o número (Enter para usar 1):
   ```
   - Se (6): pedir o percentual (1 a 10).
   - Se (7): ir ao passo 2b.

   **Passo 2b. Vários semelhantes.**
   ```
   Quais tamanhos quer criar?

   1. 1%, 2% e 5% (combinação clássica)
   2. 1% e 2%
   3. Personalizado (digito a lista, ex: "1, 3, 5")

   Digite o número:
   ```
   **Importante:** os N semelhantes viram **uma única confirmação no bloco 🛡️** (um lote), não N.

3. **País.**
   ```
   País do semelhante?
   1. Brasil (padrão)
   2. Outro país (digito o código de 2 letras, ex: "PT", "US")

   Digite o número:
   ```

4. **Nome.** Sugerir `[WS] LAL{%}pct-{nome_source_resumido}-{produto-slug}` e perguntar "uso esse ou prefere outro?".

**Proibido:** pedir `origin_audience_id`, `lookalike_spec.country`, `lookalike_spec.ratio` ou qualquer chave da Marketing API; agrupar inputs; pular para o bloco 🛡️ sem os passos 1 a 4.

## Tamanho mínimo da origem

A Meta exige **100 pessoas** na origem. Recomendado: 1.000 ou mais para qualidade razoável, 5.000 ou mais para ótima. A skill confere `approximate_count_lower_bound` (o campo `approximate_count` puro não existe mais na v25: devolve erro 100).

| Tamanho da origem | Permitido | Aviso |
|---|---|---|
| < 100 | ❌ | Bloqueia |
| 100 a 999 | ⚠️ | Permite, mas avisa: "a qualidade do semelhante vai ser baixa" |
| 1.000 a 4.999 | 🟡 | Aceitável |
| 5.000+ | 🟢 | Ideal |

### Origem entre 100 e 999 pessoas (ação obrigatória)

A Meta aceita, mas a qualidade fica baixa. **Não seguir direto:**

```
⚠️ O público de origem "{nome_source}" tem só {N} pessoas. A Meta aceita criar o
semelhante, mas a qualidade vai ser baixa (recomendado: 1.000 ou mais; ideal: 5.000).

Como você quer seguir?

1. Esperar a origem crescer (cancelo agora e você volta com 1.000 ou mais)
2. Criar mesmo assim (funciona, mas com sinal fraco; não se assuste se entregar mal)
3. Trocar de origem (volto ao passo 1)

Digite o número:
```

## Percentuais e tamanhos

| % | Tamanho aproximado (BR) | Quando usar |
|---|---|---|
| 1% | ~2M | Mais parecido, melhor qualidade. Padrão recomendado. |
| 2% | ~4M | Equilíbrio, bom para escala. |
| 3% | ~6M | Quando 1% e 2% saturaram. |
| 5% | ~10M | Escala agressiva, qualidade já cai. |
| 10% | ~20M | Quase público frio. Última opção. |

Recomendação: começar em 1% e ampliar conforme a campanha satura.

## Endpoint (modo App)

```
POST /act_<id>/customaudiences
{
  "name": "[WS] LAL{percentual}pct-{nome_source}-{produto-slug}",
  "subtype": "LOOKALIKE",
  "origin_audience_id": "<source_audience_id>",
  "lookalike_spec": {
    "type": "similarity",
    "country": "BR",
    "ratio": 0.01
  }
}
```

`ratio` 0.01 = 1%. `type: "similarity"` é o padrão (mais parecido). A alternativa `"reach"` (mais alcance, menos parecido) não é usada por padrão: `similarity` combina melhor com fundo de funil. No MCP, o mesmo conteúdo vai pelos campos que o schema da tool pedir.

## Resumo em linguagem natural (obrigatório, antes do bloco 🛡️)

**Um semelhante:**

```
📋 Antes de eu criar esse semelhante na sua conta, um resumo:

Vou criar o público semelhante "{nome}":
   - Baseado no público "{nome_source}" (~{tamanho_source} pessoas, qualidade {🟢 ótima | 🟡 aceitável | ⚠️ baixa})
   - {percentual}% mais parecido de {país em português}
   - Tamanho estimado: ~{tamanho formatado}

⏰ Como funciona:
   - A Meta leva de 6 a 24h para calcular as pessoas parecidas ("popular")
   - Antes disso, campanha com ele entrega quase nada
   - Depois, ele se atualiza sozinho conforme a origem cresce

Onde vai aparecer:
   Gerenciador de Anúncios → Públicos → procurar "[WS] LAL..."

Está certo? (sim segue para a confirmação final, não cancela aqui)
```

**Vários semelhantes (opção 7):**

```
📋 Vou criar 3 semelhantes do público "{nome_source}" de uma vez:

   1. [WS] LAL1pct-{nome_source}  → ~{X1} pessoas (mais parecido)
   2. [WS] LAL2pct-{nome_source}  → ~{X2} pessoas
   3. [WS] LAL5pct-{nome_source}  → ~{X5} pessoas (escala agressiva)

País: {país em português}
Tipo: mais parecido (padrão)

São 3 criações numa confirmação só. Cada um leva de 6 a 24h para popular.

Está certo? (sim segue para a confirmação final, não cancela)
```

**Tradução obrigatória:**

| Campo técnico | Tradução |
|---|---|
| `subtype: CUSTOM` | "público por lista, pixel ou interação" |
| `subtype: WEBSITE` | "público de visitantes do site" |
| `subtype: ENGAGEMENT` | "público de engajamento (vídeo, perfil, posts)" |
| `approximate_count_lower_bound: 580` | "~580 pessoas" |
| `approximate_count_lower_bound: 5800` | "~5.800 pessoas" |
| `lookalike_spec.ratio: 0.01` | "1%" |
| `lookalike_spec.country: "BR"` | "Brasil" |
| `lookalike_spec.type: "similarity"` | "mais parecido (padrão)" |
| `lookalike_spec.type: "reach"` | "mais alcance (menos parecido)" |

**Proibido no resumo:** IDs, `ratio` em decimal, `subtype` em inglês.

## Preview YAML (dentro do bloco 🛡️)

```yaml
sub_fluxo: lookalike
modo: MCP_CONECTOR | APP
source:
  nome: "[WS] Purchase-90d-curso-tarot"
  tamanho: 580
nome_final: "[WS] LAL1pct-Compradores-curso-tarot"
percentual: 1
pais: BR
type: similarity
tamanho_estimado: ~2.000.000

⚠️ A origem tem 580 pessoas. A qualidade do semelhante pode ser baixa.
   Recomendação: esperar a origem chegar a 1.000 ou mais.
```

## Depois de criar

```
✅ Público semelhante criado: [WS] LAL1pct-Compradores-curso-tarot

Tamanho estimado: ~2.000.000 (Brasil)
Status: populando (a Meta calcula em 6 a 24h)

Como usar:
- Em campanhas de público frio para escala, com anúncios de objetivo Descoberta
  da Mandala (ex: tipos Visual, Curiosidade e História).
- Combinado com anúncios de Conversão (Prova, Oportunidade).

Próximos passos:
- Criar campanha com esse semelhante: /trafego-criar-campanha
- Criar 2% e 5% também: /trafego-publicos opção 5 (mesma origem)
- Produzir os anúncios: /copy-anuncio, /criativo-estatico ou /mandala-de-anuncios
```

## Avisos

- **Semelhante não é instantâneo.** A Meta leva de 6 a 24h. Antes disso, o conjunto entrega quase nada.
- **Um país por semelhante.** Para vários países, criar vários.
- **Semelhante de lista de clientes é mais forte que semelhante de pixel** (sinal direto de compra). Para isso, criar a lista pela [`customer-match.md`](./customer-match.md) e depois usar como origem aqui.
- **Atualiza sozinho** conforme a origem cresce. Não precisa recriar.
- **Semelhante de semelhante não existe** na Meta. A skill bloqueia.

## Variação: Advantage+ semelhante (expansão automática)

A Meta tem uma versão automática do semelhante (aparece como "Lookalike Expansion" ou "Advantage Lookalike"). Em vez de fixar o percentual, o algoritmo amplia sozinho quando acha mais gente parecida.

**Quando vale:** campanha com aprendizado avançado (50 ou mais conversões), quando o aluno quer escalar sem cuidar de 3 semelhantes separados.

**Como ativar:** é configuração do **conjunto de anúncios**, não um público separado (chave "Lookalike Expansion" no Gerenciador, ou `targeting_optimization: "expansion_all"` no conjunto).

**Esta skill não liga essa chave.** Para usar, criar o semelhante aqui (1% por padrão) e ativar a expansão no Gerenciador ao montar o conjunto.

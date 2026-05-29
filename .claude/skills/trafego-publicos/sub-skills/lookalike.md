# Sub-fluxo. Lookalike Audience (LAL)

Cria Lookalike Audience a partir de uma Custom Audience source existente. Audiência semelhante = pessoas que se parecem (comportamento + características) com a source.

## Perguntas que cobre

- "Cria uma lookalike dos meus compradores"
- "Lookalike 1% do meu público de carrinho abandonado"
- "LAL 2% dos visitantes do site"
- "Cria uma lookalike de quem viu 75% do meu vídeo"

## Inputs

| Input | Default | Descrição |
|---|---|---|
| `source` | obrigatório | Audience source. Coletada via fuzzy match (nome / lista / ID) — ver "Padrão de coleta" abaixo. Aluno NUNCA digita ID cru. |
| `percentual` | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| `pais` | `BR` | País-alvo da lookalike |
| `nome_extra` | descrição da source | Sufixo do nome |

## Padrão de coleta de inputs (uma pergunta por mensagem)

Regra dura: **NUNCA agrupar 2+ inputs na mesma mensagem**. Aluno **nunca digita ID cru** — sempre via nome ou listagem.

### Ordem fixa

1. **Source audience.** Pergunta neutra:
   ```
   De qual audience você quer criar a lookalike? (digite o nome — completo ou parcial — ou peça pra eu listar)
   ```
   Aceita 3 modos (mesmo padrão da [`regra-automatica.md` Helper de molde](../../trafego-regras/sub-skills/regra-automatica.md#padrão-de-coleta-de-inputs-uma-pergunta-por-mensagem)):
   - **(a) Nome (total ou parcial):** `GET -g /act_<id>/customaudiences?fields=id,name,subtype,approximate_count_lower_bound,approximate_count_upper_bound,retention_days,permission_for_actions{subtype_supports_lookalike,supports_recipient_lookalike}` → filtrar mantendo `subtype != LOOKALIKE` **E** `permission_for_actions.subtype_supports_lookalike == true` **E** `permission_for_actions.supports_recipient_lookalike == true` → match `contains` no nome. 1 match: confirma. Múltiplos: lista numerada filtrada.
   - **(b) Listar:** "lista", "não lembro" → mostra audiences **elegíveis para LAL** (passa nos 3 filtros acima) com nome + tamanho + tipo.
   - **(c) ID direto** (raro): valida via `GET -g /<id>?fields=name,subtype,approximate_count_lower_bound,approximate_count_upper_bound,permission_for_actions{subtype_supports_lookalike,supports_recipient_lookalike}`.

   **Bloqueio em 3 níveis (após escolher source):**
   - Se `source.subtype == LOOKALIKE`: avisar "Não dá pra fazer LAL de LAL. Escolhe outra." e voltar ao passo 1.
   - Se `source.permission_for_actions.supports_recipient_lookalike == false`: bloquear com mensagem "Essa audience foi compartilhada de outro Business Manager sem a permissão 'Criar públicos semelhantes' — o Meta vai rejeitar com erro 2654. Como quer seguir? [1] Trocar de source, [2] Pedir pra equipe dona reabrir o compartilhamento marcando 'Compartilhar para criar públicos semelhantes', [3] Criar source nova via Customer Match (opção 6 do menu)". Não levar pro gate.
   - Se `source.approximate_count_lower_bound < 100`: bloquear "audience source tem só ~{N} pessoas, mínimo é 100. Espera ela crescer ou escolha outra."

   **Quando o filtro deixa 0 audiences elegíveis** (ex: conta cuja base toda veio compartilhada sem permissão de LAL):
   ```
   Olhei as {N} audiences da sua conta. Nenhuma permite criar lookalike
   pelo nosso App (todas vieram compartilhadas de outro Business Manager
   sem marcar "Compartilhar para criar públicos semelhantes").

   Como quer seguir?

   1. Subir lista nova de compradores via Customer Match (CSV)
      → audience nasce com este App, LAL funciona na hora
      → /trafego-publicos opção 6
   2. Pedir pra equipe que administra os BMs reabrir o compartilhamento
      marcando "Compartilhar para criar públicos semelhantes"
      (Business Manager → Públicos → audience → Compartilhar)
   3. Cancelar agora
   ```

   **No modo "tudo"** (quando aluno pede pra ver a lista inteira): aplicar o mesmo filtro de elegibilidade. Não despejar audiences inelegíveis na tela mesmo a pedido.

2. **Percentual.** Pergunta numerada:
   ```
   Qual o tamanho da lookalike?

   1. LAL 1% (~2M pessoas no Brasil — mais semelhante, default recomendado)
   2. LAL 2% (~4M — bom pra escala)
   3. LAL 3% (~6M)
   4. LAL 5% (~10M — pra escala agressiva, qualidade cai)
   5. LAL 10% (~20M — quase prospect frio, última opção)
   6. Outro (digito o número)
   7. **Criar várias de uma vez (1%, 2% e 5%, ou customizado)**

   Digite o número (Enter pra usar 1):
   ```
   - Se (6): pedir percentual (1-10).
   - Se (7): vai pro Sub-passo 2b abaixo.

   **Sub-passo 2b — Múltiplas LAL.** Se aluno escolheu (7):
   ```
   Quais percentuais quer criar?

   1. 1%, 2% e 5% (combinação clássica)
   2. 1% e 2% só
   3. Customizado (digito a lista, ex: "1, 3, 5")

   Digite o número:
   ```
   Coletar lista de percentuais. **Importante:** essas N audiences viram **1 única confirmação no gate 🛡️** (não N gates). Skill cria em lote.

3. **País.** Numerada:
   ```
   País-alvo da lookalike?
   1. Brasil (default)
   2. Outro país (digito o código ISO, ex: "PT", "US")

   Digite o número:
   ```

4. **Nome.** Sugerir auto-gerado seguindo `[FC] LAL{%}pct-{nome_source_resumido}-{produto-slug}` e perguntar "uso esse ou prefere outro?".

**Proibido:**
- Pedir `source_audience_id`, `lookalike_spec.country`, `lookalike_spec.ratio` ou qualquer chave da Marketing API direto ao aluno.
- Agrupar 2+ inputs na mesma mensagem.
- Pular pro Preview YAML sem passar pelos passos 1-4.

## Tamanho mínimo da source

O Meta exige mínimo de **100 pessoas** na source para criar lookalike. **Recomendação:** 1.000+ para qualidade decente, 5.000+ para qualidade ótima.

A skill verifica `approximate_count_lower_bound` da source antes de prosseguir (campo puro `approximate_count` foi removido em Meta v25 — retorna erro 100):

| Tamanho da source | Permitido | Aviso |
|---|---|---|
| < 100 | ❌ | Bloqueia. Audience source pequena demais. |
| 100 a 999 | ⚠️ | Permitido mas avisa: "qualidade da lookalike vai ser baixa" |
| 1.000 a 4.999 | 🟡 | Aceitável |
| 5.000+ | 🟢 | Ideal |

## Percentuais e tamanhos

LAL no Meta funciona por percentual da população do país-alvo:

| % | Tamanho aproximado (BR) | Quando usar |
|---|---|---|
| 1% | ~2M | Mais semelhante, melhor qualidade. Default recomendado. |
| 2% | ~4M | Equilíbrio. Boa para escala. |
| 3% | ~6M | Quando 1%/2% saturou. |
| 5% | ~10M | Para escala agressiva, qualidade já cai. |
| 10% | ~20M | Quase prospect frio. Última opção. |

A skill recomenda começar em 1% e ampliar conforme a campanha satura.

## Endpoint

```
POST /act_<id>/customaudiences
{
  "name": "[FC] LAL{percentual}pct-{nome_source}-{produto-slug}",
  "subtype": "LOOKALIKE",
  "origin_audience_id": "<source_audience_id>",
  "lookalike_spec": {
    "type": "similarity",
    "country": "BR",
    "ratio": 0.01      // 1%
  }
}
```

`type: "similarity"` é o padrão (mais semelhante). Alternativa é `"reach"` (maior alcance, menor semelhança), mas a skill usa `similarity` por default — mais alinhado à metodologia VTSD de fundo de funil.

## Resumo em linguagem natural antes do Preview YAML (obrigatório)

**Quando exibir:** sempre, após coletar todos os inputs (1-4), antes do Preview YAML.

**Formato fixo (uma LAL):**

```
📋 Antes de eu criar essa lookalike na sua conta, deixa eu te resumir:

Vou criar a lookalike "{nome}":
   - Baseada na audience "{nome_source}" (tem ~{tamanho_source_em_pt} pessoas, qualidade {🟢 ótima | 🟡 aceitável | ⚠️ baixa})
   - {percentual}% mais semelhante do {país em PT}
   - Tamanho estimado: ~{audience_size formatado em PT}

⏰ Como a lookalike funciona:
   - Meta leva 6 a 24h pra calcular as pessoas semelhantes (chamado "popular")
   - Antes de popular, se você ativar campanha com ela, vai entregar zero
   - Depois de popular, atualiza sozinha conforme a audience source cresce

Onde vai aparecer:
   Gerenciador de Anúncios → Públicos → procurar "[FC] LAL..."

Tá certo? (sim segue pro YAML, não cancela aqui)
```

**Formato fixo (múltiplas LAL — opção 7):**

```
📋 Vou criar 3 lookalikes da audience "{nome_source}" de uma vez:

   1. [FC] LAL1pct-{nome_source}  → ~{X1} pessoas (mais semelhante)
   2. [FC] LAL2pct-{nome_source}  → ~{X2} pessoas
   3. [FC] LAL5pct-{nome_source}  → ~{X5} pessoas (escala agressiva)

País: {país em PT}
Tipo: similarity (mais semelhante, padrão do curso)

Vou criar as 3 numa única confirmação. Cada uma leva 6-24h pra popular.

Tá certo? (sim cria as 3, não cancela)
```

**Regras de tradução:**

| Campo técnico | Tradução |
|---|---|
| `subtype: CUSTOM` | "audience customizada (lista, pixel ou interação)" |
| `subtype: WEBSITE` | "audience de visitantes do site" |
| `subtype: VIDEO` | "audience de quem viu vídeo" |
| `approximate_count_lower_bound: 580` | "~580 pessoas" |
| `approximate_count_lower_bound: 5800` | "~5.800 pessoas" |
| `lookalike_spec.ratio: 0.01` | "1%" |
| `lookalike_spec.country: "BR"` | "Brasil" |
| `lookalike_spec.type: "similarity"` | "mais semelhante (padrão)" |
| `lookalike_spec.type: "reach"` | "maior alcance (menos semelhante)" |

**Proibido:**
- Mostrar IDs, `ratio` em decimal, `subtype` em inglês.
- Pular esse resumo pra ir direto pro YAML.

## Preview YAML

```yaml
sub_fluxo: lookalike
source:
  id: 6123456789
  nome: "[FC] Purchase-90d-curso-tarot"
  tamanho: 580
nome_final: "[FC] LAL1pct-Compradores-curso-tarot"
percentual: 1
pais: BR
type: similarity
tamanho_estimado: ~2.000.000

⚠️ Source tem 580 pessoas. Qualidade da lookalike pode ser baixa.
   Recomendação: aguardar a source chegar em 1.000+ antes de criar LAL.

Quer criar mesmo assim? (digite SIM)
```

## Múltiplas LAL de uma vez (atalho)

A skill aceita criar múltiplas LAL da mesma source numa única confirmação:

```
A partir de "[FC] Purchase-90d-curso-tarot", criar:
[1] LAL 1% (similarity)
[2] LAL 2% (similarity)
[3] LAL 5% (similarity)

Quer criar:
1. Só a 1%
2. As 3 (1%, 2%, 5%)
3. Customizar
```

## Após criar

```
✅ Lookalike criada: [FC] LAL1pct-Compradores-curso-tarot
   ID: 6123456795

Tamanho estimado: ~2.000.000 (BR)
Status: populando (Meta calcula em ~6-24h)

Como usar:
- Em campanhas COLD para escala (Mandala VTSD: Tipo 7, 9, 11).
- Combinar com criativos de fundo de funil (oferta, autoridade).

Próximos passos:
- Para criar campanha com essa LAL: /trafego-criar-campanha
- Para criar 2% e 5% também: /trafego-publicos opção 5 (mesma source)
```

## Avisos

- **LAL não é instantânea.** Meta leva 6 a 24h para popular. Se usada antes, ad set entrega zero.
- **País único por LAL** no MVP. Para múltiplos países, criar múltiplas LAL.
- **LAL de upload (Customer File) é mais potente que LAL de pixel.** Sinal direto de compra. Pra usar isso, criar audience via [`customer-match.md`](./customer-match.md) primeiro, depois rodar essa skill `lookalike` com a audience uploaded como source.
- **Atualização da LAL** é automática conforme a source cresce. Não precisa recriar.
- **LAL de LAL não é permitida** pelo Meta. A skill bloqueia se `source.subtype == LOOKALIKE`.

## Ação obrigatória quando source tem entre 100 e 999 pessoas

A skill já bloqueia source < 100. Mas entre 100 e 999, o Meta aceita criar mas a qualidade da LAL fica baixa. **NÃO seguir direto** — apresentar ao aluno:

```
⚠️ A audience source "{nome_source}" tem só {N} pessoas. Meta aceita criar
a LAL, mas qualidade vai ser baixa (recomendado: 1.000+, ideal: 5.000+).

Como você quer seguir?

1. Esperar a source crescer (cancelo agora, você volta quando tiver 1.000+)
2. Criar mesmo assim (LAL vai funcionar, mas com sinal fraco — não se assuste se ela entregar mal)
3. Trocar de source (volto pro passo 1)

Digite o número:
```

## Variante: Advantage+ Lookalike (AI Meta)

O Meta tem uma versão automatizada da LAL chamada **Advantage+ Lookalike** (também aparece como "Lookalike Expansion" ou "Advantage Lookalike"). Em vez de você fixar o percentual (1%, 2%, etc.), o algoritmo expande automaticamente quando acha mais pessoas semelhantes e mantém qualidade similar.

**Quando vale usar:** campanhas em fase de aprendizado avançada (50+ conversões), quando você quer escalar e não quer gerenciar 3 LALs separadas (1%/2%/5%).

**Como ativar:** essa variante é configurada **no nível do conjunto de anúncios** (adset), via toggle "Lookalike Expansion" no Gerenciador, OU via `targeting_optimization: "expansion_all"` no payload do adset. **Não é uma audience separada**, é uma propriedade do adset que usa qualquer LAL como base.

**Hoje a skill não cobre essa toggle.** Pra ativar Advantage+ Lookalike, criar a LAL aqui (qualquer percentual, default 1%) e ativar a expansão manualmente no Gerenciador ao montar a campanha.

# Sub-fluxo. Bases por Nível (Iniciante, Intermediário, Avançado)

> ⚠️ **Importante:** este sub-fluxo **NÃO cria Saved Audience nativa no Meta**. A Marketing API v25 não suporta `POST` em `/saved_audiences` — a doc oficial diz "Não é possível executar esta operação neste ponto de extremidade". A solução é salvar o targeting como **recipe local** em `meus-produtos/{ativo}/trafego/publicos/saved-targeting-{nivel}-{produto}.md`, que a skill `/trafego-criar-campanha` consome injetando direto no `targeting_spec` do adset. Ver memória [[project-saved-audiences-capability-blocked]] pra contexto técnico.

Gera 3 **recipes de targeting** pré-configuradas representando os 3 níveis de consciência do consumidor do produto ativo. Combina interesses + behaviors + dados demográficos com base no `perfil.md` e `idconsumidor.md`.

## Perguntas que cobre

- "Criar públicos base de iniciantes, intermediários e avançados pro meu produto"
- "Quero 3 audiences segmentadas por nível"
- "Cria as bases prontas pra eu usar nas campanhas de COLD"
- "Públicos por consciência do problema"

## Conceito (VTSD aplicado)

A Identidade do Consumidor do produto define 3 perfis na escala de consciência (Eugene Schwartz adaptado):

| Nível | Quem é | Onde está |
|---|---|---|
| **Iniciante** | Não sabe que tem o problema, ou só sente o sintoma | Topo de funil. Interesses amplos relacionados ao tema |
| **Intermediário** | Sabe que tem problema, está pesquisando soluções | Meio de funil. Interesses + behaviors relacionados a busca |
| **Avançado** | Já testou outras soluções, busca método melhor | Fundo de funil. Lookalike de compradores ou interesses concorrentes |

A skill cria 3 Saved Audiences que materializam isso na conta Meta Ads.

## Inputs

| Input | Default | Descrição |
|---|---|---|
| `produto_slug` | produto ativo | Lê de `meus-produtos/.ativo` |
| `geo` | Brasil | Países / estados / cidades |
| `idade_min` | da Identidade do Consumidor | Ex: 25 |
| `idade_max` | da Identidade do Consumidor | Ex: 55 |
| `genero` | da Identidade | `all`, `male`, `female` |
| `idiomas` | `pt_BR` | Idiomas do Facebook |

A skill **NÃO inventa interesses**. Lê o `perfil.md` e o `idconsumidor.md` do produto ativo para extrair:
- Quadro (transformação)
- Furadeira (método)
- 3 Identidades (Comunicador / Consumidor / Produto)
- Decorados (benefícios percebidos)
- Urgências Ocultas (dores, dúvidas, desejos)

A partir desses, propõe uma lista de interesses + behaviors **antes** de criar. Aluno aprova ou ajusta.

### Bloqueio: se perfil.md ou idconsumidor.md não existem

Ambos os arquivos são **obrigatórios** pra esta sub-skill. Se algum não existir em `meus-produtos/{produto}/`, parar e instruir:

```
⚠️ Pra criar as 3 bases por nível, preciso do perfil.md e do idconsumidor.md
do produto "{produto}" — esses arquivos são gerados pelas skills do painel
de entregas do Workshop.

Faltando:
{lista de arquivos ausentes}

Pra preencher:
- Rode /produto-concepcao se ainda não fez (gera Quadro, Furadeira, Decorados,
  Urgências Ocultas, 3 Identidades)
- Ou /painel-revisar pra auditar/corrigir o que já tem

Quando os 2 arquivos estiverem prontos, volta aqui e rodo de novo.
```

**Não fazer mini-entrevista direta como fallback** — o caminho canônico do workshop é o painel de entregas. Mini-entrevista quebraria o padrão "uma única fonte de verdade do produto" do projeto.

## Padrão de coleta de inputs (uma pergunta por mensagem)

Regra dura: **NUNCA agrupar 2+ inputs na mesma mensagem**. Reforça regra global do CLAUDE.md ("Uma pergunta por mensagem, numerada quando há opção, exemplo entre parênteses quando aberta").

### Ordem fixa

1. **Produto.** Se o `.ativo` está preenchido, confirmar:
   ```
   Vou usar o produto ativo: "{produto_ativo}". Tudo certo? (sim/não, escolher outro)
   ```
   Se não houver `.ativo`: listar produtos em `meus-produtos/` e pedir escolha.

2. **Geo.** Pergunta neutra com default em destaque:
   ```
   Onde o público mora?

   1. Brasil inteiro (default)
   2. Estados específicos (digito a lista)
   3. Cidades específicas (digito a lista)
   4. Outro país

   Digite o número (Enter pra usar 1):
   ```
   Se (2)/(3): pedir lista de estados/cidades (1 input).

3. **Idade.** Pergunta única (idade_min + idade_max viram 1 resposta natural):
   ```
   Qual a faixa etária? (ex: "25-55", "18-65", "30-45")
   Sugestão da Identidade do Consumidor do produto: {idade_min}-{idade_max}.
   ```

4. **Gênero.** Numerada:
   ```
   Qual gênero?
   1. Todos (default da Identidade)
   2. Só mulheres
   3. Só homens

   Digite o número:
   ```

5. **Idiomas.** Default direto:
   ```
   Idiomas do Facebook do público?
   1. Português Brasil (default)
   2. Português Brasil + outros (digito)
   3. Sem filtro de idioma

   Digite o número:
   ```

6. **Interesses (via Helper).** Roda o Helper de Coleta de Interesses via Âncora (documentado abaixo na seção "Como propor interesses" — é o **canônico** do curso; outras skills referenciam aqui).

7. **Behaviors opcionais.** Pergunta neutra:
   ```
   Quer adicionar comportamentos (behaviors) além de interesses? (raro, mais avançado)
   1. Não (default — pula)
   2. Sim, pequena lista de behaviors comuns (Compradores online, Engaged Shoppers, etc.)
   ```

**Proibido:**
- Pedir `interests[].id`, `behaviors[].id`, `geo_locations.cities` ou qualquer estrutura da Marketing API direto ao aluno.
- Agrupar 2+ inputs na mesma mensagem.
- Pular pro Preview YAML sem passar pelos passos 1-6 (passo 7 é opcional).

## Fluxo

```
[1] Lê perfil.md + idconsumidor.md
[2] Propõe interesses por nível (3 listas separadas) + valida via Targeting Search API
[3] Mostra preview com idade/geo/idiomas
[4] Aluno aprova/ajusta cada nível
[5] Confirmação textual ("digite SIM pra eu gravar os 3 arquivos")
[6] Grava 3 arquivos locais em meus-produtos/{produto}/trafego/publicos/ (Write × 3)
[7] Devolve os 3 caminhos + frase pronta pra usar em /trafego-criar-campanha
    + sugestão de uso por estágio do funil
```

**Nada de POST na Graph API.** Sub-fluxo é 100% local depois da validação dos interesses (que usa GET na Targeting Search API, leitura-only).

## Helper canônico: Coleta de interesses via âncora (para todo o curso)

> **Este é o Helper canônico** do curso pra coleta de interesses do Meta. Outras skills (incluindo `trafego-testes/ab-generico.md` quando faz A/B de audiência) referenciam **esta seção**. Não duplicar — mantém aqui pra evitar drift.

> **Regra dura, sem exceção:** TODO interesse e behavior candidato deve ser validado contra a Targeting Search API do Meta ANTES de aparecer no preview YAML. Sem `id` retornado pela API, o termo é descartado. Nunca propor interesse com base em conhecimento geral ou suposição.

### Algoritmo obrigatório de proposta

```
1. Ler perfil.md + idconsumidor.md do produto ativo.
2. Para cada nível (Iniciante, Intermediário, Avançado):
   a. Gerar lista candidata de 8 a 12 termos a partir de:
      - Quadro (transformação)
      - Furadeira (método e seus conceitos)
      - Decorados (benefícios)
      - Urgências Ocultas (dores, dúvidas, desejos)
      - Identidade do Consumidor (nicho, behaviors)
   b. Para CADA termo da lista candidata, chamar:
        GET /search?type=adinterest&q={termo}&limit=5
      ou
        GET /search?type=adTargetingCategory&class=behaviors&q={termo}&limit=5
   c. Para cada resposta da API:
      - Se retornar pelo menos 1 resultado com fb_id válido e audience_size > 0:
          aceitar o melhor match (maior audience_size compatível)
      - Se a resposta vier vazia ou sem fb_id:
          descartar o termo silenciosamente (não inventar substituto)
   d. Se ao final do nível restarem < 3 termos validados:
      - Avisar o aluno: "Só {N} interesses do nível {X} foram encontrados no Meta.
        Sugestões: ampliar geo, abrir gênero, ou pedir para validar termos custom."
      - NÃO criar Saved Audience com menos de 3 interesses validados.
3. Listar para o aluno APENAS os termos validados, com nome oficial Meta + audience_size + fb_id.
4. Aluno aprova ou edita ANTES do preview YAML.
5. Preview YAML usa apenas { "id": fb_id, "name": nome_oficial_meta } no array `interests`/`behaviors`.
```

### Por que essa rigidez

A Marketing API rejeita `targeting.interests` com IDs inválidos. Se 1 interesse no array falhar, o POST do Saved Audience inteiro retorna erro. Validar antes evita falha de criação e rollback parcial.

### Exemplo de execução validada (produto: curso de tarot)

Termos candidatos gerados pela skill (12 para nível Iniciante):

```
Espiritualidade, Autoconhecimento, Astrologia, Mindfulness, Meditação,
Yoga, Esoterismo, Crescimento Pessoal, Bem-estar, Cristais,
Marie Claire (revistas com colunas de tarot), influenciadoras do nicho
```

Após validação via `targetingsearch`:

```
✅ VALIDADOS (com fb_id e audience_size):
   - Espiritualidade        (fb_id: 6003248338072, audience_size: 41M global)
   - Autoconhecimento       (fb_id: 6003277229371, audience_size: 28M global)
   - Astrologia             (fb_id: 6003106554403, audience_size: 36M global)
   - Mindfulness            (fb_id: 6003394661942, audience_size: 22M global)
   - Meditação              (fb_id: 6003107902433, audience_size: 65M global)
   - Yoga                   (fb_id: 6003107902434, audience_size: 110M global)
   - Esoterismo             (fb_id: 6003020834686, audience_size: 14M global)
   - Crescimento Pessoal    (fb_id: 6003130044797, audience_size: 89M global)
   - Bem-estar              (fb_id: 6003134706999, audience_size: 240M global)
   - Cristais               (fb_id: 6003225071421, audience_size: 9M global)

❌ DESCARTADOS (sem retorno da API):
   - "Marie Claire (revistas com colunas de tarot)"  → não é targeting category
   - "influenciadoras do nicho"                       → termo descritivo, não interesse
```

A skill apresenta APENAS os 10 validados ao aluno. Os 2 descartados são listados como "não encontrados no Meta" sem tentativa de substituir por suposição.

### Atalhos de busca

| Tipo de termo | Endpoint |
|---|---|
| Interesse genérico (Espiritualidade, Yoga) | `GET /search?type=adinterest&q={termo}` |
| Behavior (Engaged Shoppers, Online Shoppers) | `GET /search?type=adTargetingCategory&class=behaviors&q={termo}` |
| Demographic (income, education, life events) | `GET /search?type=adTargetingCategory&class=demographics&q={termo}` |
| Página específica (validar se existe como targeting) | `GET /search?type=adTargetingCategory&class=interests&q={nome_pagina}` |

### Idiomas
A busca aceita `locale=pt_BR` para priorizar nomenclatura em português. Default da skill: `locale=pt_BR` para todos os produtos com `genero` ou geo brasileiros.

## Saída local (não é chamada de API)

A skill **não faz POST na Graph API** neste sub-fluxo. Grava 3 arquivos locais, um por nível:

**Caminho:**
```
meus-produtos/{produto-slug}/trafego/publicos/saved-targeting-{nivel}-{produto-slug}.md
```

Onde `{nivel}` é `iniciantes`, `intermediarios` ou `avancados`.

**Conteúdo de cada arquivo** (formato fixo, consumido por `/trafego-criar-campanha`):

```markdown
---
name: "[FC] Saved-Iniciantes-curso-tarot"
nivel: iniciantes
produto: curso-tarot
created_at: 2026-05-27T16:32:00-03:00
fonte: bases-niveis sub-skill
---

# Targeting recipe — Iniciantes — curso-tarot

## Targeting spec (injetar em /adsets via targeting_spec)

```json
{
  "geo_locations": { "countries": ["BR"] },
  "age_min": 25,
  "age_max": 55,
  "genders": [2],
  "locales": [6],
  "interests": [
    { "id": "6003248338072", "name": "Espiritualidade" },
    { "id": "6003277229371", "name": "Autoconhecimento" },
    { "id": "6003106554403", "name": "Astrologia" }
  ],
  "behaviors": []
}
```

## Interesses validados (Targeting Search API)

| Nome oficial Meta | fb_id | audience_size |
|---|---|---|
| Espiritualidade | 6003248338072 | 41M global |
| Autoconhecimento | 6003277229371 | 28M global |
| Astrologia | 6003106554403 | 36M global |

## Estimativa local (via /delivery_estimate ou audience_size_lower_bound)

- users_lower_bound: ~3.200.000
- users_upper_bound: ~3.700.000
- método: delivery_estimate / fallback audience_size_lower_bound

## Como usar

Em `/trafego-criar-campanha`, quando perguntar o público do conjunto, responda:
"usa a base Iniciantes do curso-tarot"

A skill /trafego-criar-campanha lê este arquivo e injeta o `targeting_spec` direto no POST do adset.

## Rollback

Pra remover essa base: `rm meus-produtos/curso-tarot/trafego/publicos/saved-targeting-iniciantes-curso-tarot.md`
```

**Não há rollback via Graph API** — é arquivo local. Pra "deletar" basta `rm`.

**Por que recipe local em vez de Saved Audience nativa:** ver memória [[project-saved-audiences-capability-blocked]]. Meta v25 não expõe POST em `/saved_audiences`. Aluno que quiser ver a base listada no Audiences Manager precisa criar manualmente na UI usando os dados do recipe (interesses validados estão no .md, basta copiar).

## Resumo em linguagem natural antes do Preview YAML (obrigatório)

**Quando exibir:** sempre, depois de coletar todos os inputs (1-6 do "Padrão de coleta") e DEPOIS da validação dos interesses. ANTES do Preview YAML.

**Por que existe:** o Preview YAML expõe `targeting.geo_locations`, `interests[]` com IDs, `audience_size` em formato técnico, código de idioma `[6]` (que é `pt_BR`), etc. O aluno trava. O resumo traduz tudo pra português corrente.

**Formato fixo:**

```
📋 Antes de eu criar as 3 audiences na sua conta, deixa eu te resumir:

Vou criar 3 públicos salvos pro produto "{produto}":

🌱 INICIANTES — público amplo, topo de funil
   Pessoas de {idade_min} a {idade_max} anos, {gênero em PT}, no {geo em PT}, falando {idioma em PT}.
   Com interesse em: {interesse 1}, {interesse 2}, ... ({N total} interesses).
   Tamanho estimado: ~{audience_size formatado tipo "18 milhões"}.

🌿 INTERMEDIÁRIOS — meio de funil
   Mesmos parâmetros base, com interesses mais específicos: {lista}.
   Tamanho estimado: ~{audience_size formatado}.

🌳 AVANÇADOS — fundo de funil
   Mesmos parâmetros base, com interesses muito específicos: {lista}.
   Tamanho estimado: ~{audience_size formatado}.

Onde elas vão aparecer:
   Gerenciador de Anúncios → Públicos → procurar pelo prefixo "[FC] Saved-..."

Tá certo? (sim segue pro YAML técnico, não cancela aqui)
```

**Regras de tradução obrigatórias:**

| Campo técnico | Tradução |
|---|---|
| `genders: [1]` | "só homens" |
| `genders: [2]` | "só mulheres" |
| `genders: [1, 2]` ou ausente | "todos os gêneros" |
| `locales: [6]` | "Português (Brasil)" |
| `geo_locations.countries: ["BR"]` | "Brasil inteiro" |
| `geo_locations.regions: [...]` | nomes dos estados em PT |
| `geo_locations.cities: [...]` | nomes das cidades em PT |
| `interests[{id, name}]` | só o `name` (nunca o id) |
| `audience_size: 18000000` | "18 milhões" |
| `audience_size: 480000` | "480 mil" |
| `audience_size: 50000` | "50 mil" |

**Proibido neste resumo:**
- Mostrar IDs de interesses, fb_id, audience_size em número cru.
- Usar inglês técnico (`countries`, `interests`, `behaviors`).
- Pular esse resumo pra ir direto pro YAML.

**Comportamento depois:**
- "sim" → segue pro Preview YAML técnico.
- "não" → "1. Quer ajustar algo, 2. cancelar?". Se ajustar, volta ao passo correspondente.

## Preview YAML (resumido)

```yaml
sub_fluxo: bases_niveis
produto: curso-tarot

audiences:
  - nome: "[FC] Saved-Iniciantes-curso-tarot"
    targeting:
      geo: BR
      idade: 25-55
      genero: female
      idiomas: [pt_BR]
      interesses: [Espiritualidade, Autoconhecimento, Astrologia, Mindfulness]
      tamanho_estimado: 18000000

  - nome: "[FC] Saved-Intermediarios-curso-tarot"
    targeting:
      ...
      tamanho_estimado: 3200000

  - nome: "[FC] Saved-Avancados-curso-tarot"
    targeting:
      ...
      tamanho_estimado: 480000

confirma criar as 3? (digite SIM)
```

## Após criar

```
✅ 3 recipes de targeting gravadas localmente:

1. [FC] Saved-Iniciantes-curso-tarot
   📁 meus-produtos/curso-tarot/trafego/publicos/saved-targeting-iniciantes-curso-tarot.md

2. [FC] Saved-Intermediarios-curso-tarot
   📁 meus-produtos/curso-tarot/trafego/publicos/saved-targeting-intermediarios-curso-tarot.md

3. [FC] Saved-Avancados-curso-tarot
   📁 meus-produtos/curso-tarot/trafego/publicos/saved-targeting-avancados-curso-tarot.md

ℹ️ Essas recipes NÃO aparecem como Saved Audience no Gerenciador de Anúncios da
   Meta — porque a Marketing API v25 não permite criar Saved Audience via API
   (limitação da Meta). Elas vivem como .md no seu projeto e são injetadas
   direto no adset quando você rodar /trafego-criar-campanha.

Como usar na próxima campanha:

   Em /trafego-criar-campanha, quando ele perguntar "qual público você quer
   usar nesse conjunto?", responda com uma das frases prontas:

   - "usa a base Iniciantes do curso-tarot"
   - "usa a base Intermediarios do curso-tarot"
   - "usa a base Avancados do curso-tarot"

   A skill detecta automaticamente, lê o .md correspondente e injeta o
   targeting no POST do adset.

Como usar no funil:

🎯 Topo de funil (consciência da dor)
   Use Iniciantes em campanhas de descoberta (Mandala VTSD: Tipo 1, 2, 3).
   Conteúdo educativo sobre o problema.

🎯 Meio de funil (consciência da solução)
   Use Intermediários em campanhas de conversão indireta.
   Conteúdo sobre o método (Furadeira) + provas sociais.

🎯 Fundo de funil (consciência do produto)
   Use Avançados + Lookalike de compradores em campanhas de venda direta.
   CTAs de oferta, urgência, autoridade.

Próximos passos:
- Para criar campanha usando uma dessas: /trafego-criar-campanha
- Para criar lookalike a partir de uma audience de compradores: /trafego-publicos opção 5
- Para listar versões manualmente no Audiences Manager (opcional): abrir o .md,
  copiar o JSON do targeting e colar na UI da Meta em "Criar público salvo".
```

## Limitações

- **Saved Audience nativa não é criável via API.** Meta v25 só expõe `GET` no endpoint `/saved_audiences` (não `POST`/`PUT`/`DELETE`). Por isso o sub-fluxo salva como recipe local. Aluno que quiser ver listado no Audiences Manager precisa criar manualmente na UI usando os dados do recipe (interesses validados + targeting JSON estão no .md).
- **Recipe local não popula sozinha** — é só um targeting spec. A audience efetiva só "existe" quando `/trafego-criar-campanha` injeta esse spec no `targeting_spec` de um adset.
- **Interesses inventados** que o Meta não tem cadastrados são descartados na validação. A skill avisa: "Interesse 'X' não encontrado, removido".
- **Combinação de interesses dentro do nível** = OR (qualquer um). Para AND (todos juntos), o aluno pede manualmente.

## Ação obrigatória quando estimativa fica micro (< 1.000 pessoas)

Como o sub-fluxo não faz POST em `/saved_audiences` (que retornaria `audience_size`), a estimativa de tamanho é feita ANTES de gravar o recipe via uma das 2 abordagens:

### Abordagem A (preferida): `/delivery_estimate`

```
POST /act_<id>/delivery_estimate
{
  "targeting_spec": { ... mesmo targeting do recipe ... },
  "optimization_goal": "REACH"
}
```

Retorna `{users_lower_bound, users_upper_bound, estimate_ready}` sem criar audience. Usar `users_lower_bound` como referência pro alerta.

### Abordagem B (fallback): `audience_size_lower_bound` dos interesses

Se `/delivery_estimate` retornar erro (permissão, rate limit, etc.), somar o `audience_size_lower_bound` dos interesses validados via Targeting Search API e aplicar redução heurística pelo geo + idade (regra de proporcionalidade simples). Menos preciso mas funciona.

### Alerta

Se `users_lower_bound < 1.000` em qualquer dos 3 níveis, **NÃO gravar direto** o recipe daquele nível. Apresentar ao aluno:

```
⚠️ A base "{nome}" estimou ~{users_lower_bound} pessoas — pequena demais pra
o algoritmo do Meta otimizar bem (recomendado mínimo 1.000, ideal 50.000+).

Como você quer seguir?

1. Ampliar a faixa etária (volto pro passo 3 da coleta)
2. Ampliar o geo (volto pro passo 2)
3. Remover 1 ou 2 interesses muito específicos (mostro a lista)
4. Gravar mesmo assim (assumindo que vai entregar pouco)
5. Cancelar essa base específica (gravar só as outras 2)

Digite o número:
```

Bloqueio é informativo, não duro — aluno pode escolher "gravar mesmo assim" (4) ou cancelar só esse nível (5) sem afetar os outros 2.

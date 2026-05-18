# Sub-fluxo. Bases por Nível (Iniciante, Intermediário, Avançado)

Cria 3 Saved Audiences pré-configuradas representando os 3 níveis de consciência do consumidor do produto ativo. Combina interesses + behaviors + dados demográficos com base no `perfil.md` e `idconsumidor.md`.

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

## Fluxo

```
[1] Lê perfil.md + idconsumidor.md
[2] Propõe interesses por nível (3 listas separadas)
[3] Mostra preview com idade/geo/idiomas
[4] Aluno aprova/ajusta cada nível
[5] Confirmação SIM
[6] Cria as 3 saved audiences via API
[7] Devolve os 3 IDs + sugestão de uso por estágio do funil
```

## Como propor interesses

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

## Endpoint

```
POST /act_<id>/saved_audiences
{
  "name": "[FC] Saved-Iniciantes-{produto-slug}",
  "description": "Saved Audience nível Iniciante. Gerada via Workshop a partir de {produto-slug}/idconsumidor.md.",
  "targeting": {
    "geo_locations": { "countries": ["BR"] },
    "age_min": 25,
    "age_max": 55,
    "genders": [2],
    "locales": [6],          # pt_BR
    "interests": [
      { "id": "...", "name": "Espiritualidade" },
      ...
    ],
    "behaviors": [...]
  }
}
```

Repetir 3x (uma por nível) com diferenças de targeting.

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
✅ 3 Saved Audiences criadas:
1. [FC] Saved-Iniciantes-curso-tarot      ID: 6123456792
2. [FC] Saved-Intermediarios-curso-tarot  ID: 6123456793
3. [FC] Saved-Avancados-curso-tarot       ID: 6123456794

Como usar no funil:

🎯 Topo de funil (consciência da dor)
   Use SUPERCOLD ou Iniciantes em campanhas de descoberta (Mandala VTSD: Tipo 1, 2, 3).
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
```

## Limitações

- **Saved Audience é apenas combinação de targeting**, não é populada pelo Meta. Tamanho estimado é o que o Meta calcula no momento.
- **Interesses inventados** que o Meta não tem cadastrados são descartados. A skill avisa: "Interesse 'X' não encontrado, removido".
- **Bases para nichos muito específicos** (raros) podem dar tamanho < 50.000. Skill avisa e pergunta se quer ampliar geo/idade.
- **Combinação de interesses dentro do nível** = OR (qualquer um). Para AND (todos juntos), o aluno pede manualmente.

# Sub-fluxo. Bases por Nível (Iniciante, Intermediário, Avançado)

> ⚠️ **Este sub-fluxo NÃO cria público salvo na Meta.** A Marketing API v25 não aceita `POST` em `/saved_audiences` (a documentação oficial diz que a operação não é possível nesse endpoint). Por isso, cada base é salva como **arquivo local** em `meus-produtos/_global/trafego/publicos/saved-targeting-{nivel}-{produto-slug}.md`, e a segmentação entra no conjunto de anúncios na hora de criar a campanha (`/trafego-criar-campanha`).

Gera 3 **receitas de segmentação** para os 3 níveis de consciência do consumidor do produto ativo. Combina local, idade, gênero, idioma, interesses e comportamentos a partir do **resumo do produto** (`meus-produtos/{ativo}/resumo-produto.md`). Não existe questionário novo: o Severino já tem a identidade do consumidor.

Passo 0 (produto ativo, conexão, conta): ver `SKILL.md` desta skill. Este sub-fluxo não escreve na conta, então não passa pelo bloco 🛡️: antes de gravar os arquivos, uma confirmação simples ("Digite SIM para eu gravar as 3 bases").

## Perguntas que cobre

- "Criar públicos base de iniciantes, intermediários e avançados para o meu produto"
- "Quero 3 públicos segmentados por nível"
- "Cria as bases prontas para eu usar nas campanhas de público frio"
- "Públicos por consciência do problema"

## Conceito (VTSD aplicado)

A Identidade do Consumidor define 3 perfis na escala de consciência (Eugene Schwartz adaptado):

| Nível | Quem é | Onde está |
|---|---|---|
| **Iniciante** | Não sabe que tem o problema, ou só sente o sintoma | Topo de funil. Interesses amplos ligados ao tema |
| **Intermediário** | Sabe que tem o problema e pesquisa soluções | Meio de funil. Interesses e comportamentos de quem busca |
| **Avançado** | Já testou outras soluções e procura um método melhor | Fundo de funil. Semelhante de compradores ou interesses em concorrentes |

## De onde vêm os dados (sem perguntar de novo)

Ler `meus-produtos/{ativo}/resumo-produto.md` e usar:

| Dado | Seção do resumo |
|---|---|
| Idade, gênero, região | `## Público (Identidade do Consumidor)`, linha "Perfil" |
| Onde o público busca informação | `## Público`, linha "Canais" |
| Transformação | `## Quadro` |
| Método e seus conceitos | `## Furadeira` |
| Benefícios | `## Decorados principais` |
| Dores, dúvidas, desejos, assuntos relacionados | `## Urgências Ocultas` |
| Concorrentes (nível Avançado) | `## Pesquisa de mercado (síntese)`, "Concorrentes principais" |

Quando precisar de mais detalhe, ler **só** a seção indicada na tabela "Onde está o detalhe completo" do próprio resumo (ex: baldes "Para quem é" em `idconsumidor.md`, seção `## Baldes de Para Quem É`; concorrentes completos em `pesquisa-mercado.md`). Se o resumo não tiver idade ou gênero, perguntar só esse dado ao aluno.

**A skill NÃO inventa interesses.** Todo interesse proposto é conferido na Meta antes de entrar na base (ver "Helper canônico").

## Roteamento por modo (ler primeiro)

A busca de interesse por nome **não existe no MCP**.

- **`APP`:** a skill busca e valida os interesses sozinha por `curl` (`GET /search?type=adinterest` e afins) e estima o tamanho por `POST /act_<id>/delivery_estimate`.
- **`MCP_CONECTOR`:** na entrada do sub-fluxo, explicar e oferecer:
  ```
  O conector da Meta não pesquisa interesses. Hoje, a recomendação da própria Meta
  é público aberto com Advantage+ (o algoritmo encontra o público pelo anúncio).
  Como prefere seguir?

  1. Público aberto com Advantage+ (recomendado): gravo as 3 bases com local,
     idade e idioma, e deixo os interesses como sugestão
  2. Quero interesses específicos: te passo a lista por nível e você confere
     no Gerenciador quais existem (uns 5 minutos)
  3. Usar o modo App, que confere os interesses sozinho (/trafego-conexao)

  Digite o número:
  ```
  - **Opção 1:** gravar as bases com `targeting_spec` só de local, idade, gênero e idioma, e a lista de interesses candidatos numa seção "Sugestões para o Advantage+ (não conferidas)". Nenhum interesse sem conferência entra no `targeting_spec`.
  - **Opção 2:** seguir o passo manual guiado abaixo. Só os interesses que o aluno confirmar como existentes entram na base, pelo nome oficial que aparece no Gerenciador (sem ID: o Gerenciador não mostra o ID). Marcar `validacao_interesses: manual_gerenciador`.

### Passo manual guiado (MCP, opção 2)

```
Vou te passar os interesses candidatos de um nível por vez. Para cada um:

📋 Passo 1. Gerenciador de Anúncios → abra qualquer conjunto de anúncios em
           rascunho (ou comece a criar um, sem publicar)
📋 Passo 2. Em "Público", procure a "Segmentação detalhada" e clique em "Procurar"
📋 Passo 3. Digite o termo da lista e veja se ele aparece como interesse
📋 Passo 4. Me responda, para cada termo: o nome exato que apareceu, ou "não existe"

Lista do nível {Iniciante | Intermediário | Avançado}:
   1. {termo 1}
   2. {termo 2}
   ...

🛟 Se a tela estiver diferente, me mande um print.
```

Um nível por mensagem. Nível com menos de 3 interesses confirmados não é gravado (mesma regra do App).

## Coleta de inputs (uma pergunta por mensagem)

Regra dura: **nunca agrupar 2 ou mais inputs na mesma mensagem**.

### Ordem fixa

1. **Confirmar o perfil lido do resumo.**
   ```
   Vou usar o público registrado no seu produto:

   Produto: {nome do produto}
   Público: {perfil resumido: gênero, idade, região}

   Está certo? (sim ou ajustar)
   ```
   Se "ajustar": perguntar só o que mudou. Não reescrever o resumo (ajuste vale só para estas bases; para mudar o perfil do produto, `/produto-concepcao`).

2. **Local.**
   ```
   Onde o público mora?

   1. Brasil inteiro (padrão)
   2. Estados específicos (digito a lista)
   3. Cidades específicas (digito a lista)
   4. Outro país

   Digite o número (Enter para usar 1):
   ```

3. **Idade.**
   ```
   Qual a faixa etária? (ex: "25-55", "18-65", "30-45")
   Sugestão pela Identidade do Consumidor: {idade_min}-{idade_max}.
   ```

4. **Gênero.**
   ```
   Qual gênero?
   1. Todos (padrão da Identidade)
   2. Só mulheres
   3. Só homens

   Digite o número:
   ```

5. **Idioma.**
   ```
   Idioma do Facebook do público?
   1. Português (Brasil) (padrão)
   2. Português (Brasil) e outros (digito)
   3. Sem filtro de idioma

   Digite o número:
   ```

6. **Interesses.** App: rodar o "Helper canônico" abaixo. MCP: seguir a opção escolhida na entrada.

7. **Comportamentos (opcional).**
   ```
   Quer adicionar comportamentos além de interesses? (raro, mais avançado)
   1. Não (padrão, pula)
   2. Sim, uma lista curta de comportamentos comuns (compradores online etc.)
   ```

**Proibido:** pedir `interests[].id`, `behaviors[].id`, `geo_locations` ou qualquer estrutura da Marketing API; agrupar inputs; pular para a confirmação sem os passos 1 a 6 (o 7 é opcional).

## Fluxo

```
[1] Ler o resumo do produto (e só a seção de detalhe necessária)
[2] Propor interesses por nível (3 listas) e conferir na Meta
    (App: busca automática; MCP: Advantage+ ou conferência no Gerenciador)
[3] Mostrar resumo com idade, local e idioma
[4] Aluno aprova ou ajusta cada nível
[5] Confirmação simples ("digite SIM para eu gravar as 3 bases")
[6] Gravar 3 arquivos em meus-produtos/_global/trafego/publicos/
[7] Devolver os 3 caminhos, a frase pronta para /trafego-criar-campanha
    e a sugestão de uso por etapa do funil
```

**Nenhuma escrita na conta.** Depois da conferência dos interesses, tudo é local.

## Helper canônico: interesses conferidos na Meta (para todo o Severino)

> **Este é o Helper canônico** de coleta de interesses. Outras skills (como `trafego-testes/sub-skills/ab-generico.md` no A/B de audiência) apontam para esta seção. Atualizar aqui primeiro.

> **Regra dura, sem exceção:** todo interesse e comportamento candidato precisa ser conferido na Meta antes de aparecer na confirmação. No App, sem `id` devolvido pela busca, o termo é descartado. No MCP, sem confirmação do aluno no Gerenciador, o termo fica só como sugestão. Nunca propor interesse por conhecimento geral ou suposição.

### Algoritmo (modo App)

```
1. Ler o resumo do produto (Quadro, Furadeira, Decorados, Urgências Ocultas,
   Público e Canais, concorrentes da pesquisa).
2. Para cada nível (Iniciante, Intermediário, Avançado):
   a. Gerar de 8 a 12 termos candidatos a partir desses dados.
   b. Conferir cada termo:
        GET /search?type=adinterest&q={termo}&locale=pt_BR&limit=5
      ou, para comportamento:
        GET /search?type=adTargetingCategory&class=behaviors&q={termo}&limit=5
   c. Resposta com pelo menos 1 resultado com id e audience_size > 0:
        aceitar o melhor (maior audience_size compatível).
      Resposta vazia ou sem id:
        descartar o termo em silêncio (não inventar substituto).
   d. Com 2 ou mais termos aceitos, ampliar pelas sugestões da própria Meta:
        GET /search?type=adinterestsuggestion&interest_list=["<nome1>","<nome2>"]&locale=pt_BR&limit=25
      Só entram interesses que voltam com id e audience_size > 0.
   e. Se o nível ficar com menos de 3 interesses conferidos:
        avisar: "Só {N} interesses do nível {X} existem na Meta. Dá para
        ampliar o local, abrir o gênero ou conferir termos que você sugerir."
        NÃO gravar base com menos de 3 interesses conferidos.
3. Mostrar ao aluno SÓ os conferidos, com nome oficial da Meta e tamanho.
4. O aluno aprova ou edita antes da confirmação.
5. O targeting_spec usa só { "id": <id>, "name": <nome oficial> }.
```

Cada busca é um `Bash(curl ...)` separado, token lido do `.env` na própria chamada, `curl -g` quando houver colchetes na URL.

### Por que a rigidez

A Meta recusa `targeting.interests` com ID inválido. Um interesse inválido na base quebra o `targeting_spec` inteiro na criação do conjunto (`/trafego-criar-campanha` devolve erro). Conferir antes garante que a base só carrega o que a Meta aceita.

### Exemplo (produto: curso de tarot)

Candidatos gerados para o nível Iniciante:

```
Espiritualidade, Autoconhecimento, Astrologia, Mindfulness, Meditação,
Yoga, Esoterismo, Crescimento pessoal, Bem-estar, Cristais,
"revistas com colunas de tarot", "influenciadoras do nicho"
```

Depois da conferência:

```
✅ CONFERIDOS (existem na Meta):
   - Espiritualidade        (~41 milhões)
   - Autoconhecimento       (~28 milhões)
   - Astrologia             (~36 milhões)
   - Meditação              (~65 milhões)
   - Esoterismo             (~14 milhões)
   ...

❌ NÃO ENCONTRADOS:
   - "revistas com colunas de tarot"   → não é categoria de segmentação
   - "influenciadoras do nicho"        → termo descritivo, não interesse
```

(Tamanhos ilustrativos. Os IDs reais vêm sempre da busca, nunca deste exemplo.)

O aluno vê só os conferidos. Os não encontrados aparecem como "não existem na Meta", sem tentativa de troca por suposição.

### Atalhos de busca (modo App)

| Tipo de termo | Endpoint |
|---|---|
| Interesse genérico (Espiritualidade, Yoga) | `GET /search?type=adinterest&q={termo}` |
| Interesses relacionados a outros já conferidos | `GET /search?type=adinterestsuggestion&interest_list=[...]` |
| Comportamento (compradores online) | `GET /search?type=adTargetingCategory&class=behaviors&q={termo}` |
| Dado demográfico (renda, escolaridade, momentos de vida) | `GET /search?type=adTargetingCategory&class=demographics&q={termo}` |
| Página específica (se existe como interesse) | `GET /search?type=adTargetingCategory&class=interests&q={nome_pagina}` |

A busca aceita `locale=pt_BR` para trazer nomes em português (padrão da skill).

## Saída local (não é chamada de API)

Três arquivos, um por nível:

```
meus-produtos/_global/trafego/publicos/saved-targeting-{nivel}-{produto-slug}.md
```

`{nivel}`: `iniciantes`, `intermediarios` ou `avancados`.

**Conteúdo de cada arquivo** (formato fixo, lido pelo `/trafego-criar-campanha`):

````markdown
---
name: "[WS] Saved-Iniciantes-curso-tarot"
nivel: iniciantes
produto: curso-tarot
created_at: 2026-05-27T16:32:00-03:00
fonte: bases-niveis
validacao_interesses: api_search | manual_gerenciador | advantage_plus_sem_interesses
---

# Base de segmentação: Iniciantes, curso-tarot

## Targeting spec (entra no conjunto como targeting_spec)

```json
{
  "geo_locations": { "countries": ["BR"] },
  "age_min": 25,
  "age_max": 55,
  "genders": [2],
  "locales": [6],
  "interests": [
    { "id": "<id_conferido>", "name": "Espiritualidade" },
    { "id": "<id_conferido>", "name": "Autoconhecimento" },
    { "id": "<id_conferido>", "name": "Astrologia" }
  ],
  "behaviors": []
}
```

## Interesses conferidos

| Nome oficial na Meta | ID | Tamanho |
|---|---|---|
| Espiritualidade | <id_conferido> | ~41 milhões |

(No modo MCP com conferência no Gerenciador: coluna ID = "não exibido pelo Gerenciador"; os interesses entram no conjunto pela "Segmentação detalhada", antes de ativar.)

## Sugestões para o Advantage+ (não conferidas)

(Só no modo MCP, opção 1. Termos para o aluno usar como sugestão de público no Advantage+.)

## Estimativa

- users_lower_bound: ~3.200.000
- users_upper_bound: ~3.700.000
- método: delivery_estimate | audience_size dos interesses | Gerenciador

## Como usar

Em `/trafego-criar-campanha`, quando a skill perguntar o público do conjunto, responda:
"usa a base Iniciantes do curso-tarot"

A skill lê este arquivo e aplica o `targeting_spec` no conjunto.

## Como desfazer

Apagar este arquivo. Nada muda na conta da Meta.
````

**Por que arquivo local e não público salvo:** a Meta v25 só permite `GET` em `/saved_audiences`. Quem quiser ver a base listada no Gerenciador cria o público salvo manualmente com os dados do arquivo.

## Resumo em linguagem natural (obrigatório, antes da confirmação)

```
📋 Antes de eu gravar as 3 bases (nada é criado na sua conta da Meta), um resumo:

Vou gravar 3 bases de público para o produto "{produto}":

🌱 INICIANTES: público amplo, topo de funil
   Pessoas de {idade_min} a {idade_max} anos, {gênero em português}, {local em português},
   com Facebook em {idioma em português}.
   Interesses: {interesse 1}, {interesse 2}... ({N} no total).
   Tamanho estimado: ~{tamanho, ex: "18 milhões"}.

🌿 INTERMEDIÁRIOS: meio de funil
   Mesma base, com interesses mais específicos: {lista}.
   Tamanho estimado: ~{tamanho}.

🌳 AVANÇADOS: fundo de funil
   Mesma base, com interesses bem específicos: {lista}.
   Tamanho estimado: ~{tamanho}.

Onde vão ficar:
   Arquivos em meus-produtos/_global/trafego/publicos/ (eles NÃO aparecem no
   Gerenciador; a segmentação entra na conta quando você rodar /trafego-criar-campanha)

Está certo? (digite SIM para eu gravar, ou diga o que ajustar)
```

**Tradução obrigatória:**

| Campo técnico | Tradução |
|---|---|
| `genders: [1]` | "só homens" |
| `genders: [2]` | "só mulheres" |
| `genders: [1, 2]` ou ausente | "todos os gêneros" |
| `locales: [6]` | "Português (Brasil)" |
| `geo_locations.countries: ["BR"]` | "Brasil inteiro" |
| `geo_locations.regions: [...]` | nomes dos estados |
| `geo_locations.cities: [...]` | nomes das cidades |
| `interests[{id, name}]` | só o nome |
| `audience_size: 18000000` | "18 milhões" |
| `audience_size: 480000` | "480 mil" |

**Proibido no resumo:** IDs de interesse, tamanho em número cru, inglês técnico (`countries`, `interests`, `behaviors`).

## Depois de gravar

```
✅ 3 bases de segmentação gravadas:

1. [WS] Saved-Iniciantes-curso-tarot
   📁 meus-produtos/_global/trafego/publicos/saved-targeting-iniciantes-curso-tarot.md

2. [WS] Saved-Intermediarios-curso-tarot
   📁 meus-produtos/_global/trafego/publicos/saved-targeting-intermediarios-curso-tarot.md

3. [WS] Saved-Avancados-curso-tarot
   📁 meus-produtos/_global/trafego/publicos/saved-targeting-avancados-curso-tarot.md

ℹ️ Essas bases NÃO aparecem como público salvo no Gerenciador, porque a Meta não
   permite criar público salvo fora do Gerenciador. Elas ficam no seu projeto e entram
   direto no conjunto quando você rodar /trafego-criar-campanha.

Como usar na próxima campanha:

   Em /trafego-criar-campanha, quando a skill perguntar o público do conjunto,
   responda com uma das frases:

   - "usa a base Iniciantes do curso-tarot"
   - "usa a base Intermediarios do curso-tarot"
   - "usa a base Avancados do curso-tarot"

Como usar no funil:

🎯 Topo de funil (consciência da dor)
   Iniciantes, com anúncios de objetivo Descoberta da Mandala
   (ex: Explicação, Curiosidade, Problema-Solução).

🎯 Meio de funil (consciência da solução)
   Intermediários, com anúncios sobre o método (Furadeira) e prova social
   (ex: Demonstração, Prova).

🎯 Fundo de funil (consciência do produto)
   Avançados e semelhante de compradores, com anúncios de Conversão
   (ex: Comparação, Oportunidade).

Próximos passos:
- Criar campanha com uma dessas bases: /trafego-criar-campanha
- Criar semelhante a partir de um público de compradores: /trafego-publicos opção 5
- Produzir os anúncios de cada nível: /copy-anuncio ou /mandala-de-anuncios
```

## Limitações

- **Público salvo não é criável pela API** (a Meta v25 só permite leitura em `/saved_audiences`).
- **A base local não popula sozinha:** é só uma segmentação. O público só "existe" quando a segmentação entra num conjunto.
- **Interesse que não existe na Meta é descartado** na conferência: "Interesse 'X' não encontrado, removido."
- **Interesses dentro de um nível = OU** (qualquer um). Para E (todos juntos), o aluno pede de forma explícita.

## Estimativa de tamanho e alerta de base micro (< 1.000 pessoas)

A estimativa é feita antes de gravar:

### Abordagem A (preferida, modo App): `/delivery_estimate`

```
POST /act_<id>/delivery_estimate
{
  "targeting_spec": { ...mesma segmentação da base... },
  "optimization_goal": "REACH"
}
```

Devolve `{users_lower_bound, users_upper_bound, estimate_ready}` sem criar nada. Usar `users_lower_bound` para o alerta. (É uma leitura, mesmo sendo `POST`: não muda nada na conta e não passa pelo bloco 🛡️.)

### Abordagem B (reserva): tamanho dos interesses

Se o `/delivery_estimate` falhar (permissão, limite de chamadas), somar o `audience_size_lower_bound` dos interesses conferidos e reduzir de forma proporcional pelo local e pela idade. Menos preciso, mas funciona.

### Modo MCP

Sem estimativa automática. Se o aluno quiser o número, o Gerenciador mostra o "Tamanho estimado do público" ao montar a segmentação num conjunto em rascunho.

### Alerta

Se `users_lower_bound < 1.000` em algum nível, **NÃO gravar direto** aquele nível:

```
⚠️ A base "{nome}" ficou com ~{users_lower_bound} pessoas: pequena demais para o
algoritmo da Meta otimizar bem (mínimo recomendado: 1.000; ideal: 50.000 ou mais).

Como você quer seguir?

1. Ampliar a faixa etária (volto ao passo 3)
2. Ampliar o local (volto ao passo 2)
3. Tirar 1 ou 2 interesses muito específicos (mostro a lista)
4. Gravar mesmo assim (vai entregar pouco)
5. Cancelar só essa base (gravo as outras 2)

Digite o número:
```

O bloqueio é informativo: o aluno pode gravar mesmo assim (4) ou cancelar só aquele nível (5).

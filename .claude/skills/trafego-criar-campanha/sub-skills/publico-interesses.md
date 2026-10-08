# Público e Interesses. Fase 6 do /trafego-criar-campanha

Esta sub-skill aprofunda a Fase 6 (Público) do `/trafego-criar-campanha`. Traz o mapa dos 3 modos de público, o fluxo de busca de interesses na Graph API, os critérios de filtro e ranking, e o `targeting` JSON final que vai no `POST /adsets`.

Toda chamada usa `v25.0`. Cada `curl` é uma chamada `Bash` separada.

---

## 1. Os 3 modos e o que cada um gera

| Modo | Quando recomendar | `targeting_automation` | `flexible_spec` |
|---|---|---|---|
| `ADVANTAGE_PLUS` | Default. Produto novo, público não validado, qualquer trilha | `{"advantage_audience": 1}` | ausente |
| `ADVANTAGE_PLUS_COM_INTERESSES` | Nicho específico onde o algoritmo demora a achar sozinho | `{"advantage_audience": 1}` | presente, como sugestão |
| `PERSONALIZADO` | Público já validado, remarketing, ou restrição de negócio | `{"advantage_audience": 0}` | conforme a escolha |

**A diferença entre os modos 2 e 3 é semântica, não sintática.** Com `advantage_audience: 1`, os interesses são sugestão e o Meta pode entregar fora deles. Com `0`, viram restrição dura. Explique isso ao aluno, porque a expectativa errada aqui gera reclamação de "o Meta ignorou meu público".

---

## 2. Modo 1. Advantage+ puro

```json
{
  "geo_locations": { "countries": ["BR"] },
  "age_min": 18,
  "age_max": 65,
  "targeting_automation": { "advantage_audience": 1 }
}
```

Sem `genders`, sem `flexible_spec`, sem `interests`. Omitir `genders` já significa todos. Não envie `"genders": [1,2]`, que é redundante e reduz legibilidade do payload no preview.

`age_max: 65` cobre a faixa "65+" da interface. A API não aceita valor acima de 65.

---

## 3. Modo 2. Advantage+ com interesses derivados do perfil

### 3.1 Extrair termos do produto

Ler `meus-produtos/{ativo}/perfil.md` e, quando existir, `idconsumidor.md`. Extrair:

| Fonte no perfil | O que aproveitar |
|---|---|
| Quadro | Verbo + objeto principal da transformação |
| Nicho | Termo de categoria |
| Decorados | Substantivos concretos dos benefícios |
| Urgências Ocultas, categoria DESEJOS | O que a pessoa quer virar |
| Urgências Ocultas, categoria ASSUNTOS RELACIONADOS | Temas adjacentes, os melhores para interesse |
| `idconsumidor.md`, canais e referências | Nomes de figuras públicas e veículos do nicho |

Montar de 5 a 8 termos curtos em português e traduzir cada um para inglês. A base de interesses do Meta é multilíngue, mas indexa melhor em inglês, então buscar nos dois idiomas aumenta a cobertura.

### 3.2 Buscar na Graph API

Uma chamada por termo:

```
GET /v25.0/search?type=adinterest&q={termo}&limit=10&locale=pt_BR
```

Campos úteis do retorno: `id`, `name`, `audience_size_lower_bound`, `audience_size_upper_bound`, `topic`, `path`.

### 3.3 Filtrar e ranquear

Aplicar nesta ordem:

1. **Descartar `audience_size_upper_bound` abaixo de 500.000.** Público pequeno demais, encarece o CPM e trava a saída do aprendizado.
2. **Descartar `audience_size_upper_bound` acima de 500.000.000.** Genérico demais, não orienta nada. Exemplos típicos: "Comida", "Família", "Música".
3. **Deduplicar por `id`.** Termos diferentes retornam o mesmo interesse com frequência.
4. **Priorizar por aderência ao nicho.** Comparar `topic` e `path` com o nicho do produto. Interesse cujo `path` contém a categoria do produto sobe no ranking.
5. **Selecionar de 8 a 12 finais.**

### 3.4 Apresentar ao aluno

Tabela numerada com nome, ID, tamanho aproximado e a justificativa que amarra o interesse ao perfil:

```
Interesses encontrados a partir do perfil de {produto}:

| # | Interesse               | ID            | Tamanho aprox. | Por que sugeri              |
|---|-------------------------|---------------|----------------|-----------------------------|
| 1 | Leitura                 | 6003020834693 | 80M a 100M     | termo central do Quadro     |
| 2 | Desenvolvimento pessoal | 6003411521903 | 150M a 200M    | Decorado "evoluir como pessoa" |

Quais quer usar?
1. Aceitar todos
2. Escolher por número (ex: "1, 2, 4, 7")
3. Adicionar interesse manual (digite o nome, eu busco o ID)
```

### 3.5 Targeting resultante

```json
{
  "geo_locations": { "countries": ["BR"] },
  "age_min": 18,
  "age_max": 65,
  "targeting_automation": { "advantage_audience": 1 },
  "flexible_spec": [
    { "interests": [
        { "id": "6003020834693", "name": "Leitura" },
        { "id": "6003411521903", "name": "Desenvolvimento pessoal" }
    ]}
  ]
}
```

Interesses no mesmo objeto de `flexible_spec` são combinados com OU. Objetos diferentes dentro do array são combinados com E, o que estreita muito o público. **Use sempre um único objeto** salvo pedido explícito do aluno.

### 3.6 Casos de borda

| Situação | Ação |
|---|---|
| Busca retorna vazia ou só ruído | Oferecer modo 1 (Advantage+ puro) ou modo 3 (personalizado). Não insistir com interesse fraco |
| `perfil.md` não existe | Avisar e oferecer `/produto-concepcao`, ou seguir pelos modos 1 e 3 |
| Erro de autenticação | Voltar a `/trafego-conexao` |
| Aluno pede interesse que não existe na base | Mostrar os 5 mais próximos retornados e deixar ele escolher. Nunca inventar ID |

---

## 4. Modo 3. Personalizado

Perguntar o que combinar. Aceita mais de um item.

### 4.1 Públicos customizados

```
GET /v25.0/act_{id}/customaudiences?fields=id,name,subtype,approximate_count_lower_bound,approximate_count_upper_bound&limit=25
```

Apresentar em tabela numerada com nome, tipo e tamanho. Entra em `custom_audiences`.

### 4.2 Lookalikes

Mesma chamada, filtrando `subtype = LOOKALIKE`. **A skill nunca cria lookalike.** Se o aluno pedir, instruir: "Criação de lookalike é feita no Gerenciador. Crie o público lá e volte aqui."

### 4.3 Interesses específicos

Quando o aluno nomeia ("yoga e meditação"), buscar com `limit=5` e confirmar o match antes de usar. Quando ele pede busca, rodar o fluxo da seção 3.

### 4.4 Restrições demográficas

Uma pergunta por vez: idade mínima e máxima, gênero, localização, idiomas.

| Campo | Formato |
|---|---|
| `age_min` / `age_max` | 18 a 65 |
| `genders` | `[1]` masculino, `[2]` feminino, omitir para todos |
| `geo_locations.countries` | `["BR"]` |
| `geo_locations.regions` | `[{"key": "..."}]`, obtido via `GET /search?type=adgeolocation&location_types=["region"]` |
| `geo_locations.cities` | `[{"key": "...", "radius": 25, "distance_unit": "kilometer"}]` |
| `locales` | Códigos numéricos do Meta, não ISO. Português do Brasil é `6` |

### 4.5 Exclusões

Geralmente compradores ou já inscritos. Entra em `excluded_custom_audiences`.

**Regra de coerência.** Em campanha de venda direta perpétua, sugerir ativamente excluir a audiência de compradores. É o erro mais comum e mais caro de campanha perpétua: pagar para reimpactar quem já comprou.

### 4.6 Targeting resultante

```json
{
  "geo_locations": { "countries": ["BR"] },
  "age_min": 25,
  "age_max": 55,
  "genders": [2],
  "custom_audiences": [{ "id": "23848..." }],
  "excluded_custom_audiences": [{ "id": "23849..." }],
  "flexible_spec": [{ "interests": [{ "id": "6003...", "name": "Yoga" }] }],
  "targeting_automation": { "advantage_audience": 0 }
}
```

---

## 5. Posicionamentos (Fase 8)

Default é Advantage+ Placements: **omitir** `publisher_platforms` do targeting. Omissão é o que ativa automático. Não existe campo `"advantage_placement": 1`.

Para posicionamento manual:

```json
{
  "publisher_platforms": ["facebook", "instagram"],
  "facebook_positions": ["feed"],
  "instagram_positions": ["stream", "story", "reels"]
}
```

| Pedido do aluno | Configuração |
|---|---|
| "só Feed" | `publisher_platforms: ["facebook","instagram"]`, `facebook_positions: ["feed"]`, `instagram_positions: ["stream"]` |
| "só Reels e Stories" | `instagram_positions: ["reels","story"]`, `publisher_platforms: ["instagram"]` |
| "só Instagram" | `publisher_platforms: ["instagram"]` |

**Gate duro.** Qualquer posicionamento de Instagram exige `FB_INSTAGRAM_USER_ID` no `.env`. Se faltar, parar e acionar `/trafego-conexao`, opção 4 (redescobrir identificadores).

---

## 6. Special Ad Categories

Default é `[]`. Perguntar apenas quando o produto der sinal:

| Sinal no produto | Categoria |
|---|---|
| Crédito, financiamento, cartão, score | `CREDIT` |
| Vaga de emprego, curso atrelado a contratação | `EMPLOYMENT` |
| Imóvel, aluguel, financiamento imobiliário | `HOUSING` |
| Conteúdo político ou questão social | `ISSUES_ELECTIONS_POLITICS` |

**Consequência que precisa ser dita ao aluno antes de confirmar:** categoria especial restringe a segmentação. Idade trava em 18 a 65, gênero fica indisponível, o raio geográfico mínimo sobe para 24 km e lookalikes ficam bloqueados. Se o aluno marcar por engano, a campanha entrega pior sem motivo aparente.

O campo é obrigatório no `POST /campaigns`, mesmo vazio. Enviar `special_ad_categories: []`.

---

## 7. Checklist antes de fechar a Fase 6

- [ ] Modo escolhido e registrado em `audience.modo`
- [ ] `targeting` monta JSON válido, sem campo inventado
- [ ] Todo ID de interesse ou audiência veio da API, nenhum foi escrito de cabeça
- [ ] Posicionamento de Instagram tem `FB_INSTAGRAM_USER_ID` disponível
- [ ] Exclusão de compradores oferecida, quando for perpétuo de venda direta
- [ ] `special_ad_categories` confirmado pelo aluno, inclusive quando vazio

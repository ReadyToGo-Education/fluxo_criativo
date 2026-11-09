# Sub-fluxo. Duplicar Campanha, Conjunto ou Anúncio com Variação

Pega algo que já existe no Meta Ads e duplica, mudando UMA dimensão. É diferente do A/B clássico: o original continua rodando e a cópia é uma extensão, não uma comparação.

Passo 0 e gate: ver `SKILL.md` desta skill. **Leia antes a seção "Lições de campo" da `ab-generico.md`**: ela define como copiar em cada modo.

## Perguntas que cobre

- "Duplica minha melhor campanha mudando a segmentação para 25-34 anos"
- "Pega meu melhor conjunto e duplica trocando só o criativo"
- "Repete a campanha que está indo bem em outra região"
- "Cria uma cópia da campanha X com idade 35-44"

## Inputs

| Input | Padrão | Descrição |
|---|---|---|
| `entidade` | obrigatório | Campanha, conjunto ou anúncio a duplicar (por nome ou lista) |
| `dimensao_a_alterar` | obrigatório | `idade`, `geo`, `audience`, `criativo`, `posicionamento`, `lance`, `headline` |
| `valor_novo` | obrigatório | Valor da dimensão na cópia |
| `nome_sufixo` | gerado | Ex: `-25_34` |
| `manter_original` | sim | O original continua rodando |

## Coleta de inputs (uma pergunta por mensagem)

Regra dura: **nunca agrupar 2 ou mais inputs na mesma mensagem**. O aluno **nunca digita ID**.

### Ordem fixa

1. **O que duplicar.** "Qual campanha você quer duplicar? (digite o nome, completo ou em parte, ou peça para eu listar)":
   - **(a) Nome:** listar campanhas (MCP `ads_get_ad_entities`; App `GET -g /act_<id>/campaigns?fields=name,status,effective_status,insights.date_preset(last_7d){spend}`) e procurar o trecho. 1 resultado: confirmar. Vários: lista numerada. Nenhum: oferecer listar todas.
   - **(b) Listar:** campanhas ativas e pausadas dos últimos 90 dias, com nome, status e gasto de 7 dias.
   - **(c) ID direto:** conferir pela leitura e confirmar.

   **Bloqueio:** conta sem campanha: encaminhar para `/trafego-criar-campanha` e encerrar.

2. **Tamanho da cópia.** "Duplicar (1) a campanha inteira com todos os conjuntos, (2) só um conjunto dela, ou (3) só um anúncio?". Se (2) ou (3): lista numerada dos conjuntos ou anúncios (nome, CPA de 7 dias, gasto de 7 dias).

3. **O que mudar** (lista numerada: idade, região, público, criativo, posicionamento, lance, headline).

4. **Valor novo.** Ex: idade → a nova faixa. Criativo ou headline → o "Helper: escolha de criativos" da [ab-generico.md](./ab-generico.md) (biblioteca com filtro de 30 dias, sem variações automáticas, código curto V1/I1, arquivo do computador ou código direto). **Nunca pedir hash ou ID de vídeo.** Headline gerada pela skill passa pela "AUTO-REVISÃO OBRIGATÓRIA DE COPY" do CLAUDE.md antes de aparecer.

   **Criativo com vários vídeos ou imagens (Advantage+ Creative):** simplificar para `object_story_spec.video_data` ou `link_data` (1 criativo), como no passo 2 da Montagem da `ab-generico.md`. Senão, a cópia vira Advantage+ Creative também e contamina a comparação.

5. **Hipótese** ("Espero que com {valor_novo} eu consiga ___ porque ___").

6. **Manter o original** só se o aluno disser que quer pausar o original (padrão: o original continua). Pausar o original é outra escrita, com confirmação própria.

**Proibido:** pedir ID de entidade ou de criativo; pular para a confirmação sem os passos 1 a 5.

## Como copiar (por modo)

### Modo MCP
1. **Copiar pelo conector:** conjunto por `ads_create_ad_set` com `source_adset_id`; anúncio por `ads_create_ad` com `source_ad_id`. Campanha inteira: campanha casca por `ads_create_campaign` e conjuntos copiados um a um por `source_adset_id` (se o schema permitir indicar a campanha de destino), com os anúncios por `source_ad_id`. Parâmetros conforme o schema das tools.
2. **Aplicar a variação** por `ads_update_entity` (ex: idade no conjunto copiado). Em mudança de segmentação (idade, região, público, posicionamento), só se o schema aceitar mudar o campo sozinho: o conector não lê a segmentação, então não dá para reenviar a segmentação inteira com segurança.
3. **Se a cópia ou a variação falhar: duplicação guiada no Gerenciador** (passo a passo da seção "Lições de campo" da `ab-generico.md`). O aluno duplica, muda só a dimensão, deixa desativado e avisa; a skill confere pela leitura (nome, status, orçamento) e registra.

### Modo App
> ⚠️ O `/copies` **falha de forma pouco óbvia** com estrutura maior: a cópia síncrona aceita **menos de 3 objetos** (1885194), a recriação do criativo com post existente quebra (3858504, 2446347) e o conjunto exige `targeting_automation.advantage_audience` (1870227).

- **Entidade pequena (1 conjunto com 1 anúncio, menos de 3 objetos):** pode usar `/copies`:
  ```
  POST /<entity_id>/copies
  {
    "deep_copy": true,
    "rename_options": {
      "rename_strategy": "DEEP_RENAME",
      "rename_suffix": "_dup-25-34"
    },
    "status_option": "PAUSED"
  }
  ```
  Resposta: `{ "copied_campaign_id": "...", "ad_object_ids": {...} }` (ou o ID do conjunto copiado). Se vier 1885194, 3858504, 2446347 ou 1870227, passar para "ler e recriar".
- **Campanha inteira ou 2 ou mais objetos:** "ler e recriar" (seção "Lições de campo" da `ab-generico.md`): campanha casca → conjuntos com `targeting_automation` → anúncios apontando para o `creative_id` existente.

Depois, aplicar a variação na cópia:

```
POST /<copied_adset_id>
{
  "targeting": {
    "...": "mesma segmentação lida do original",
    "age_min": 25,
    "age_max": 34
  }
}
```

> Se a dimensão for `criativo` ou `headline` e precisar **subir arquivo do computador**: no App, pelo Helper da `ab-generico.md` (sub-passo 6); no MCP, imagem por URL pública ou passo manual guiado, vídeo novo sempre pelo passo manual guiado (biblioteca de mídia do Gerenciador).

## Dimensões e onde aplicar

| Dimensão | Onde muda | Campo |
|---|---|---|
| `idade` | conjunto | `targeting.age_min`, `targeting.age_max` |
| `geo` | conjunto | `targeting.geo_locations` |
| `audience` | conjunto | `targeting.custom_audiences`, `targeting.interests` |
| `criativo` | anúncio | `creative` |
| `posicionamento` | conjunto | `targeting.publisher_platforms`, `facebook_positions`, `instagram_positions` |
| `lance` | conjunto | `bid_strategy`, `bid_amount` |
| `headline` | anúncio | `creative.object_story_spec.link_data.name` |

## Sugestão de variação (atalho VTSD)

Quando o aluno pede "duplica meu melhor anúncio em outro público, mas me sugere qual":
1. Ver os públicos já usados na campanha original (no MCP, pelo nome dos públicos e conjuntos; no App, pelo `targeting`).
2. Ler o público e os interesses do produto no `meus-produtos/{ativo}/resumo-produto.md` (seção `## Público` e Urgências Ocultas) e as bases por nível já salvas em `meus-produtos/_global/trafego/publicos/saved-targeting-*.md`, se existirem.
3. Sugerir de 1 a 3 públicos alternativos pela matriz de níveis (iniciante, intermediário, avançado).

Ex: original em semelhante 1% de compradores. Sugestões:
- base "Intermediarios-curso-tarot" (já salva pela `/trafego-publicos`), ou
- semelhante 2% de compradores (mais alcance), ou
- público novo de carrinho abandonado de 30 dias (`/trafego-publicos` opção 1).

## Resumo e bloco 🛡️

Resumo em linguagem natural (o que é copiado, o que muda, onde entra, que tudo nasce pausado e que o original segue rodando), depois o bloco 🛡️ com o Preview YAML. Um "sim" para o lote inteiro (cópia + variação).

## Preview YAML (dentro do bloco 🛡️)

```yaml
sub_fluxo: duplicar_variando
modo: MCP_CONECTOR | APP
como_copia: source_id (MCP) | copies (App, 1 conjunto com 1 anúncio) | ler_e_recriar (App) | duplicacao_guiada (MCP, plano B)
entidade_original:
  tipo: campanha
  nome: "[Campanha] Tarot LAL1pct"
  status: ACTIVE (continua rodando)

copia:
  nome: "[WS-AB] dup-campanha-tarot-mudando-idade-25_34-curso-tarot"
  dimensao_alterada: idade
  valor_original: 25-55
  valor_novo: 25-34
  estrutura_copiada: campanha + 2 conjuntos + 5 anúncios

variacao_aplicada_em: todos os conjuntos copiados (mesma idade nova)

orcamento_inicial: 30 BRL/dia (igual ao original; o aluno pode ajustar)
status_inicial: PAUSED
```

## Depois de criar

```
✅ Campanha duplicada, PAUSADA: "[WS-AB] dup-campanha-tarot-mudando-idade-25_34-curso-tarot"
   O original "[Campanha] Tarot LAL1pct" continua rodando.

Hipótese salva em meus-produtos/{ativo}/entregas/trafego/testes/{slug}.md.
Próxima leitura: 12/05/2026, pelo /trafego-testes opção [11].

Para desfazer: a cópia já está pausada. Se quiser tirá-la da frente, eu arquivo por
aqui (com confirmação), ou você apaga pelo Gerenciador.
```

## Avisos

- **`deep_copy: true`** só copia a árvore inteira com **menos de 3 objetos** (limite síncrono da Meta, erro 1885194). Campanha com vários conjuntos ou anúncios: "ler e recriar" no App, cópia por `source_*_id` ou duplicação guiada no MCP.
- **Idade real ≠ nome.** No App, ler `age_min` e `age_max` do `targeting`. No MCP, pedir ao aluno para conferir no Gerenciador.
- **Públicos são reaproveitados**, não duplicados. As 2 versões usam os mesmos públicos personalizados.
- **O pixel é reaproveitado.**
- **Sobreposição de público:** se a cópia tem público muito sobreposto ao do original (ex: 25-34 dentro de 25-55), as duas disputam o mesmo leilão. A skill avisa quando a sobreposição passa de 50%.
- **Não confundir com A/B clássico:** aqui o objetivo é repetir para escalar ou variar, não comparar. Para comparar, usar as opções [1] a [8].

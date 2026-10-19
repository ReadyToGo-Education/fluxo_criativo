---
name: trafego-pixel
description: >
  Diagnóstico de pixels (Meta Pixel / conjuntos de dados) da conta de anúncios. Lê o status de cada
  pixel, o último disparo, os eventos rastreados nos últimos 7 dias, a contagem por evento, a taxa
  de deduplicação entre pixel e API de Conversões (CAPI) e destaca pixels parados. Escopo
  deliberadamente restrito: apenas leitura e diagnóstico, nunca cria, edita ou apaga evento.
  Instalar ou reinstalar o pixel numa página é com /pagina-pixel; criar evento personalizado para
  virar público é com /trafego-publicos. Use quando o aluno perguntar "meu pixel está funcionando?",
  "quais eventos meu pixel está rastreando?", "tem pixel sem atividade?", "qual foi o último
  disparo do pixel?", "minha CAPI está duplicando?".
---

# Tráfego Pixel. Diagnóstico de Pixels Meta Ads

Você é o diagnosticador de pixels da conta de anúncios. Seu papel é ler os dados do Gerenciador de Eventos (pelo conector MCP ou pela Graph API) e devolver um retrato claro da saúde dos pixels: quem está disparando, o que está sendo rastreado e quem está em silêncio.

**Princípios:**
- Apenas leitura. Esta skill nunca configura, edita, cria ou apaga evento. Instalação do pixel na página: `/pagina-pixel`. Evento personalizado para alimentar público: `/trafego-publicos`.
- Diagnóstico claro. Status verde, amarelo ou vermelho com critério explícito.
- Sem invenção. Se a leitura não devolveu o dado, marcar `null` ou `dados_disponiveis: false`.
- Foco nos últimos 7 dias. Janelas mais longas só sob pedido explícito.

**Pixel pertence à conta de anúncios, não ao produto.** Por isso o cache e os diagnósticos salvos ficam em `meus-produtos/_global/trafego/pixel/`, não na pasta do produto ativo.

---

## 🔌 Passo 0. Modo de conexão e roteamento (antes de qualquer leitura)

1. Ler `META_AUTH_MODO` do `.env` (valor não sensível): `grep "^META_AUTH_MODO=" .env | cut -d= -f2-`. Se vazio, acionar `/trafego-conexao`.
2. **Esta skill é 100% leitura: não tem bloco 🛡️ de escrita nem lacuna em nenhum dos dois modos.** Toda leitura de pixel tem tool MCP equivalente. O que muda por modo é só o transporte:
   - **`MCP_CONECTOR`:** tools do conector, descobertas pelo **final do nome** (o prefixo do servidor varia, pode ser um UUID): `ads_get_datasets`, `ads_get_dataset_details`, `ads_get_dataset_stats`, `ads_get_dataset_quality`, `ads_get_ad_entities`, `ads_get_ad_account_custom_audiences`. Sem token. Se a conta vier com `is_ads_mcp_enabled: false` ou o erro "Ads MCP is gradually being rolled out", avisar que a Meta ainda não liberou a conta no conector e oferecer o modo App pelo `/trafego-conexao`.
   - **`APP`:** `curl` GET na Graph API, `v25.0`, com `FB_ACCESS_TOKEN_PERMANENTE` inline lido do `.env` no momento da execução (presença conferida antes com `grep -q`, valor nunca exibido; na tela, `***TOKEN_MASCARADO***`) e **`curl -g`** quando o `fields` tiver chaves aninhadas (ex: `promoted_object{pixel_id}`).
3. Ver o mapa completo curl → tool na seção 2. No MCP, o `ad_account_id` vem de `FB_AD_ACCOUNT_ID` do `.env`.

### Passo 0.1. Tipo de funil do produto ativo

Os eventos "esperados" (seção 4) dependem do tipo de funil: venda direta espera `Purchase`; captação espera `Lead`.

1. Ler `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md` (seguindo a seção "Contexto Persistente do Negócio" do CLAUDE.md).
2. Inferir o tipo de funil do resumo (tipo e formato do produto) e, quando houver campanhas ativas, do objetivo delas (OUTCOME_SALES = venda direta; OUTCOME_LEADS = captação), lido na checagem da seção 1.4.
3. Só perguntar se continuar ambíguo:

```
O pixel desta conta serve principalmente para:

1. Venda direta (o evento principal é a compra)
2. Captação de leads (o evento principal é o cadastro)
3. Os dois

Digite o número:
```

Sem produto ativo, a skill roda mesmo assim (o pixel é da conta) e faz essa pergunta.

---

## 1. Inputs

### 1.1 Obrigatórios
- `ad_account_id`. Lido do `.env` (`FB_AD_ACCOUNT_ID`) ou do passo de seleção de conta do command.

### 1.2 Opcionais com padrão
| Input | Padrão | Descrição |
|---|---|---|
| `pixel_id` | nenhum (todos) | Se informado, diagnóstico só daquele pixel. Sem informar, diagnóstico de todos os pixels da conta. |
| `janela_dias` | 7 | Janela de leitura das estatísticas. Aceita 1, 7, 14, 30. |
| `incluir_eventos_zero` | `false` | Se `true`, lista eventos cadastrados que não dispararam nenhuma vez na janela. |

### 1.3 Modo de operação
A skill atende 3 sub-fluxos disparados pelo command `/trafego-pixel`:

1. **Status dos pixels:** visão de saúde por pixel da conta.
2. **Eventos rastreados:** detalhamento de um pixel específico, eventos disparados na janela.
3. **Pixels sem atividade:** destaque dos pixels da conta sem nenhum disparo na janela.

Detalhes técnicos de cada sub-fluxo em `sub-skills/status-pixels.md`, `sub-skills/eventos-rastreados.md` e `sub-skills/sem-atividade.md`.

### 1.4 Checagem extra automática: pixel usado pelas campanhas para otimização

Quando a conta tem **mais de 1 pixel ativo**, a skill **sempre** executa esta checagem como bloco final do output, sem perguntar. Saber qual pixel cada campanha usa para otimizar é crítico: pixel ativo + campanha apontando para o pixel errado = otimização cega.

```
APP:  GET -g /act_{ad_account_id}/campaigns
        ?fields=id,name,objective,status,promoted_object{pixel_id,custom_event_type}
        &effective_status=%5B%22ACTIVE%22%5D
        &limit=200
MCP:  ads_get_ad_entities (campanhas ativas; campo do objeto promovido confirmado com ads_get_field_context)
```

Em campanhas de OUTCOME_SALES (perpétuo) ou OUTCOME_LEADS (lançamento), o `promoted_object.pixel_id` revela qual pixel a campanha usa como evento de otimização. Se o objeto promovido estiver no nível do conjunto, ler nos conjuntos.

**Regras de apresentação:**
- Agrupar campanhas pelo pixel que estão usando.
- Cruzar com a saúde de cada pixel (do bloco principal): se uma campanha aponta para um pixel 🔴 (sem atividade), levantar 🚨 sinal crítico imediato.
- Se uma campanha não tem pixel no objeto promovido (ex: objetivo de tráfego), marcar como "sem otimização por evento". Não é problema.

**Output esperado:**

```
🎯 PIXEL USADO POR CAMPANHA (otimização)

Pixel "Loja Principal" (123...): 🟢 Ativo
   - Campanha: CURSO X - Perpétuo Principal    (otimiza por Purchase)
   - Campanha: CURSO X - Remarketing 30d       (otimiza por Purchase)

Pixel "Captura Lançamento" (456...): 🟢 Ativo
   - Campanha: CURSO X - Captação Leads        (otimiza por Lead)

🚨 ALERTA: a campanha "CURSO X - Black Friday" aponta para o pixel "Pixel Antigo (BR)" (🔴 sem atividade há 9 dias). A campanha está otimizando às cegas. Revisar o evento de otimização no Gerenciador de Anúncios.
```

A checagem **só roda quando**:
- O sub-fluxo principal é "Status dos pixels" OU "Sem atividade".
- A conta tem 2 ou mais pixels com `last_fired_time` no histórico (não apenas pixels nunca usados).

Em contas com pixel único, a checagem é dispensável e a skill pula sem mencionar.

---

## 2. Leituras por modo (roteamento do Passo 0)

**Modo `APP` (curl, `v25.0`):**
```
GET -g /act_{ad_account_id}/adspixels?fields=id,name,code,last_fired_time,creation_time,owner_business
GET    /{pixel_id}?fields=id,name,last_fired_time,is_unavailable,can_proxy,data_use_setting
GET    /{pixel_id}/stats?aggregation=event&start_time={ISO}&end_time={ISO}
GET    /{pixel_id}/stats?aggregation=event_total_counts&start_time={ISO}&end_time={ISO}
GET    /{pixel_id}/stats?aggregation=event_match_quality&start_time={ISO}&end_time={ISO}
```
Token inline lido do `.env` (mascarado na exibição); **`curl -g`** sempre que o `fields` tiver chaves aninhadas (ex: `promoted_object{pixel_id,custom_event_type}` na checagem da seção 1.4), senão o curl trata `{}` como padrão de nomes de arquivo e devolve resultado parcial sem erro. Exibição:

```bash
curl -gs "https://graph.facebook.com/v25.0/<PIXEL_ID>/stats?aggregation=event_total_counts&start_time=<ISO>&end_time=<ISO>&access_token=***TOKEN_MASCARADO***"
```

**Modo `MCP_CONECTOR` (tools, sem token): mapa equivalente**

| Leitura (curl APP) | Tool MCP (pelo final do nome) |
|---|---|
| `GET /adspixels` (lista pixels + `last_fired_time`) | `ads_get_datasets` |
| `GET /{pixel_id}?fields=...` (metadados do pixel) | `ads_get_dataset_details` |
| `GET /{pixel_id}/stats?aggregation=event_total_counts` (totais por evento) | `ads_get_dataset_stats` |
| `GET /{pixel_id}/stats?aggregation=event_match_quality` (qualidade de correspondência e deduplicação) | `ads_get_dataset_quality` |
| `GET /act_{id}/campaigns?fields=...promoted_object{pixel_id}` (checagem 1.4) | `ads_get_ad_entities` |
| `GET /act_{id}/customaudiences` (cruzamento com públicos) | `ads_get_ad_account_custom_audiences` |

A versão de API vigente (modo APP) é `v25.0`, alinhada com a `/trafego-insights`. No MCP, o formato do retorno de `ads_get_dataset_stats` e `ads_get_dataset_quality` difere do `aggregation=...` do curl: ler conforme o que a tool entrega (totais canônicos por evento), mantendo as mesmas regras de classificação das seções 3 a 5.

### 2.0 Leituras opcionais de eventos e parâmetros (só no MCP)

Quando o conector oferecer, duas tools de **leitura** reforçam o drill-down de eventos:

| Tool (final do nome) | O que acrescenta |
|---|---|
| `ads_pixel_event_read` | Os eventos configurados no pixel (padrão e personalizados) e a configuração de cada um. Ajuda a separar "evento que existe e não disparou" de "evento que nem está configurado". |
| `ads_pixel_parameter_read` | Os parâmetros configurados nos eventos (ex.: `value`, `currency`, `content_ids` na compra). Cobre parte do que a Graph API não mostra (seção 8). |

Os parâmetros dessas tools saem do schema na hora; nada de parâmetro inventado. **Proibido nesta skill:** `ads_pixel_event_create`, `ads_pixel_event_update`, `ads_pixel_event_delete` e qualquer tool `ads_pixel_parameter_*` de escrita. Esta skill só lê. Se o aluno quiser criar ou mudar evento, o caminho é `/trafego-publicos` (evento para público) ou `/pagina-pixel` (instalação na página).

### 2.1 Papel de cada agregação (ler antes de implementar)

A escolha errada de agregação é a causa número 1 de erro nesta skill. Cada `aggregation` devolve um formato e um propósito diferentes. Usar a errada gera contagem zerada mesmo com o pixel disparando.

| Agregação | O que retorna | Quando usar | Formato |
|---|---|---|---|
| `event_total_counts` | **Totais acumulados** por evento na janela. **Fonte canônica** para "Total 7d", contagem por evento e tabelas de detalhamento. | Sempre que precisar do total por evento na janela (status, eventos rastreados, sem atividade). | `data: [{ event: "<nome>", value: <total> }, ...]` |
| `event` | Série temporal: contagem por evento agregada por dia (ou hora). Cada evento aparece N vezes (uma por intervalo). | Só quando precisar de gráfico temporal ou comparação dia a dia. | `data: [{ event: "<nome>", value: <contagem_no_intervalo>, start_time: <ISO>, end_time: <ISO> }, ...]`, várias linhas por evento. |
| `event_match_quality` | Pontuação de qualidade de correspondência por evento (0 a 10). | Quando disponível, para relatar a qualidade de correspondência. | `data: [{ event: "<nome>", value: <score> }, ...]` |

**Regra dura:** para "quantas vezes Purchase disparou nos últimos 7 dias?", **sempre** usar `event_total_counts`. Nunca somar valores de `aggregation=event` (série temporal). Somar série temporal está sujeito a buracos de janela e formato inconsistente.

### 2.2 Erro conhecido: contagem zero com `last_fired_time` recente

Sintoma: o pixel informa `last_fired_time` há menos de 24h, mas todos os eventos aparecem com contagem 0 nos últimos 7 dias.

Causa: a leitura está usando `aggregation=event` (série temporal) como se fosse `event_total_counts`. Como o formato é diferente (várias linhas por evento, com `start_time`/`end_time`), a leitura não acha o campo `value` esperado e devolve 0.

Correção: refazer a chamada com `aggregation=event_total_counts` e ler `data[].value` direto.

**Heurística obrigatória:** se `horas_desde_ultimo_disparo < 24` E `total_eventos_7d == 0`, marcar `dados_disponiveis: false` com motivo `parser_inconsistente` e refazer a chamada com `event_total_counts` antes de classificar o pixel como sem atividade.

### 2.3 Permissões necessárias
- `ads_read` (mínimo).
- `business_management` (para pixels que pertencem a um Gerenciador de Negócios diferente do usuário).

Se a chamada retornar `OAuthException` ou permissão negada, a skill encerra com mensagem clara apontando para `/trafego-conexao` (no modo App, refazer o token com as permissões corretas pelo `/gerar-token-permanente-facebook-ads`).

---

## 3. Critério de status do pixel

Cada pixel da conta recebe um dos 3 status:

| Status | Critério |
|---|---|
| 🟢 Ativo | Último disparo há 24h ou menos **e** total de eventos > 0 nos últimos 7d |
| 🟡 Atenção | Último disparo entre 24h e 7d **ou** total de eventos < 50 nos últimos 7d |
| 🔴 Sem atividade | Último disparo há mais de 7d **ou** `last_fired_time = null` |

**Regra adicional:** se o pixel tem `is_unavailable: true`, o status é 🔴 com motivo "pixel desativado".

---

## 4. Eventos padrão monitorados

Quando o aluno pede o detalhamento de um pixel, a skill verifica explicitamente a presença e a contagem destes eventos padrão:

| Evento | O que indica |
|---|---|
| `PageView` | Tráfego chegando na página. Base de tudo. |
| `ViewContent` | Visualizou um conteúdo específico (página de produto, post). |
| `AddToCart` | Adicionou ao carrinho (perpétuo). |
| `InitiateCheckout` | Iniciou o checkout (perpétuo). |
| `Purchase` | Comprou. Métrica-norte do perpétuo. |
| `Lead` | Cadastrou como lead. Métrica-norte do lançamento. |
| `CompleteRegistration` | Concluiu cadastro. Variante de Lead. |
| `Subscribe` | Assinou (recorrência). |

Eventos personalizados são listados separadamente, sem categoria fixa.

### 4.1 Sinais críticos
- **Pixel sem `PageView`:** instalação quebrada. Página HTML criada no Severino: reinstalar com `/pagina-pixel`. Página em plataforma (Hotmart, Kiwify, Lovable etc.): conferir a configuração do pixel na própria plataforma.
- **`PageView` ativo mas `Purchase` zero há 7 dias ou mais** (perpétuo): o evento de compra não está disparando. Provável API de Conversões quebrada ou checkout sem disparo. Não é problema de campanha, mas as campanhas que dependem de `Purchase` param de otimizar.
- **`Lead` zero em conta de lançamento:** mesma lógica.
- **`InitiateCheckout` cai mais de 50%** vs a janela anterior: o fluxo de checkout quebrou. Cruzar com o output [8] Problemas Ocultos da `/trafego-analise` e, para a etapa de checkout, com a `/trafego-oferta-funil`.

---

## 5. Taxa de deduplicação (pixel no navegador × API de Conversões)

Quando o pixel tem a API de Conversões (CAPI) configurada, o Meta deduplica os eventos que chegam pelos dois lados (navegador + servidor). A skill lê o `dedup_match_keys_used` (ou o dado equivalente do `ads_get_dataset_quality` no MCP) quando disponível e calcula:

```
taxa_deduplicacao = eventos_deduplicados / total_eventos_recebidos
```

Saudável: 60% a 90%. Abaixo de 30%: a CAPI provavelmente não está enviando, ou envia com chaves de correspondência incorretas. Acima de 95%: a CAPI está duplicando demais ou o pixel do navegador está sendo bloqueado.

A skill só relata a taxa de deduplicação quando o dado está disponível. Não inventa.

---

## 6. Output esperado

Output sempre estruturado (YAML ou apresentação legível, conforme o caso). Formato bruto YAML:

```yaml
ad_account_id: act_<id>
janela_dias: 7
sub_fluxo: status_pixels | eventos_rastreados | sem_atividade
total_pixels: <n>

pixels:
  - id: <pixel_id>
    nome: <nome>
    status: ativo | atencao | sem_atividade
    ultimo_disparo: <ISO 8601> | null
    horas_desde_ultimo_disparo: <n> | null
    is_unavailable: true | false

    eventos_padrao:
      PageView: { contagem: <n>, ultimo_disparo: <ISO> | null }
      ViewContent: { ... }
      AddToCart: { ... }
      InitiateCheckout: { ... }
      Purchase: { ... }
      Lead: { ... }
      CompleteRegistration: { ... }
      Subscribe: { ... }

    eventos_custom:
      - nome: <nome_do_evento>
        contagem: <n>
        ultimo_disparo: <ISO>

    deduplicate_rate: <0.0 a 1.0> | null
    sinais_criticos:
      - <descrição curta>

resumo:
  ativos: <n>
  em_atencao: <n>
  sem_atividade: <n>
  acoes_sugeridas:
    - texto: <descrição>
      handoff: /pagina-pixel | /trafego-publicos | /trafego-analise [8] | /trafego-oferta-funil | manual
```

---

## 7. Handoffs

| Achado | Handoff sugerido |
|---|---|
| Pixel sem `PageView` há 7 dias ou mais | `/pagina-pixel` (reinstalar o pixel na página HTML) ou configuração na plataforma da página |
| Pixel com `PageView` mas sem `Purchase` (perpétuo) | Investigar a CAPI e a integração com o checkout. Conferir no Gerenciador de Eventos se o checkout dispara `Purchase` (Hotmart e Kiwify configuram a CAPI pela própria plataforma). `/pagina-checkout` ajuda a revisar a ligação da página com o checkout |
| Pixel inativo + público de remarketing secando | Resolver o pixel primeiro; depois `/trafego-publicos` (recriar o público) + `/trafego-analise` [8] |
| Taxa de deduplicação < 30% com CAPI ativa | Investigação manual no Gerenciador de Eventos (chaves de correspondência) |
| Vários pixels duplicados | Limpeza manual no Gerenciador de Negócios (não é função desta skill) |
| Aluno quer criar evento personalizado para alimentar público | `/trafego-publicos`, opção de evento personalizado |
| Pixel saudável mas atribuição ainda em dúvida | `/trafego-diagnostico` (score de confiança, variável de qualidade da atribuição) |

Se o aluno ainda não tem pixel criado, orientar a criar o Gerenciador de Negócios, a Página, a conta de anúncios e o pixel no Meta antes; depois `/trafego-conexao` e `/pagina-pixel`.

---

## 8. Limitações conhecidas

- A Graph API não expõe o **conteúdo** de cada disparo (os parâmetros enviados). Para auditar parâmetros (ex: `value`, `currency`, `content_ids` na compra), o aluno abre o Gerenciador de Eventos manualmente. No MCP, `ads_pixel_parameter_read` pode mostrar a configuração dos parâmetros (seção 2.0), mas não o conteúdo de cada disparo.
- `last_fired_time` pode ter atraso de até 30 minutos em relação ao tempo real.
- Pixels que pertencem a outro Gerenciador de Negócios exigem a permissão `business_management`. Sem ela, retornam apenas `id` e `name`.
- Eventos com qualidade de correspondência baixa não são separados nesta skill. O diagnóstico detalhado dessa qualidade é manual no Gerenciador de Eventos.

---

## 9. Cache

Esta skill **não usa o cache** da `/trafego-insights` (que é de métricas de campanha). Cache próprio, global (o pixel é da conta, não do produto):

```
meus-produtos/_global/trafego/pixel/
├── status-{YYYY-MM-DD}-{hh}.md
├── eventos-{pixel_id}-{YYYY-MM-DD}-{hh}.md
└── sem-atividade-{YYYY-MM-DD}-{hh}.md
```

Validade: 1 hora. Depois de qualquer leitura bem-sucedida, salvar. A próxima chamada na mesma hora, com os mesmos parâmetros, lê direto do arquivo. O cache nunca guarda token.

Para forçar nova leitura, o aluno pede "atualiza" (ou a flag `--refresh` na invocação).

---

## 10. Princípios que esta skill nunca viola

1. **Apenas leitura.** Nunca configurar evento, editar pixel, criar ou apagar evento personalizado. Nada de `ads_pixel_event_create/update/delete`. Isso é de `/trafego-publicos` e `/pagina-pixel`.
2. **Sempre declarar a janela** no output.
3. **Nunca inventar contagem.** Se a leitura não retornou, marcar `null`.
4. **Status sempre justificado** com o critério da seção 3.
5. **Falha parcial preserva o resto.** Se um pixel falha, os outros são relatados normalmente.
6. **Sinal crítico sempre ganha handoff.** Nunca deixar achado sem caminho de resolução.
7. **`aggregation=event_total_counts` é a única fonte canônica de totais.** Nunca somar valores de `aggregation=event` para montar a tabela "Total 7d". Ver seções 2.1 e 2.2.
8. **Validar a coerência entre `last_fired_time` e o total de eventos.** Se `last_fired_time` é de menos de 24h mas `total_eventos_7d == 0`, não classificar como sem atividade: é sinal de leitura errada. Refazer com `event_total_counts` e revalidar antes de relatar.
9. **Em conta com 2 ou mais pixels ativos, sempre executar a checagem de pixel usado pelas campanhas** (seção 1.4). É bloco final automático, não pergunta.

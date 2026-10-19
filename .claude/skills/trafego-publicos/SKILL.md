---
name: trafego-publicos
description: >
  Cria, lista e gerencia públicos (audiences) do Meta Ads: público por evento padrão do pixel,
  público por evento personalizado (com conversão personalizada opcional), público de quem viu
  25 a 100% de um vídeo, bases por nível (iniciante, intermediário, avançado) a partir do resumo
  do produto, público semelhante (lookalike), lista de clientes com hash feito no computador do
  aluno e engajamento com Instagram e Facebook. Escreve na conta Meta Ads pelo MCP da Meta
  (padrão) ou pela Marketing API (modo App). Use quando o aluno pedir "criar público",
  "audience custom", "lookalike", "público semelhante", "remarketing", "público de quem viu meu
  vídeo", "público dos compradores", "subir minha lista de clientes", "público de quem clicou no
  botão", "lista de remarketing".
user-invocable: true
---

# Tráfego Públicos. Audiences Meta Ads

Você cria e gerencia públicos na conta de anúncios. Esta skill é a única que cria público no Severino. Outras skills que precisam de público (`/trafego-criar-campanha`, `/trafego-testes`, `/trafego-escalar` no modo horizontal) chamam esta.

---

## 🛡️ Gate obrigatório antes de qualquer escrita na conta

Toda criação ou alteração de público segue a seção "GATE EM CAMADA DE CHAT ANTES DE OPERAÇÕES DE ESCRITA NA META GRAPH API" do CLAUDE.md, nos dois modos (tool do MCP ou `curl` no modo App):

1. **Resumo em linguagem natural** (sem ID, sem JSON, sem inglês técnico). O aluno confirma que o plano está certo.
2. **Bloco 🛡️ com o Preview YAML** da sub-skill logo abaixo dele. O "sim" desse bloco é a única autorização do lote: criar 3 semelhantes de uma vez, ou criar a lista de clientes e enviar todos os lotes, é um lote só.
3. Depois do "sim", executar em sequência sem reabrir o gate. Parar e perguntar de novo só se uma chamada falhar, o aluno mudar o plano ou surgir uma escrita que não estava no lote.
4. **Excluir público nunca entra no lote.** Cada exclusão tem bloco 🛡️ e "sim" próprios (regra 7 do gate). No MCP, pela tool `ads_delete_custom_audience`. No modo App, nunca rodar `curl -X DELETE` direto: guiar a exclusão no Gerenciador ou mostrar o comando sem o token para o aluno rodar (ver `sub-skills/listar.md`).
5. Nunca exibir `curl` com token. Mascarar (`***TOKEN_MASCARADO***`). Proibido heredoc Python e `curl | python3` com token (seção "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" do CLAUDE.md).

**Não passam pelo gate:** leituras (tools `ads_get_*` ou `GET` na Graph API) e o sub-fluxo `bases-niveis`, que só grava arquivos locais (confirmação simples antes de gravar).

---

## 🔌 Passo 0 obrigatório (todas as sub-skills, antes de qualquer leitura ou escrita)

1. **Produto ativo.** Ler `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md`, seguindo a seção "Contexto Persistente do Negócio" do CLAUDE.md (resumo ausente e `perfil.md` com Quadro: gerar pelo agente `gerador-resumo-produto`; sem perfil: orientar `/produto-concepcao`). O slug do produto entra no nome dos públicos. Público, Quadro, Furadeira, Decorados, Urgências Ocultas, preço e tipo vêm do resumo: nunca perguntar ao aluno o que o resumo já tem.
2. **Conexão Meta.** Ler `META_AUTH_MODO` com `grep "^META_AUTH_MODO=" .env | cut -d= -f2-` (valor não sensível, seção "LEITURA SEGURA DO .env" do CLAUDE.md).
   - **Vazio, ausente ou com valor diferente de `MCP_CONECTOR` e `APP`** (inclusive o legado `HIBRIDO`): acionar `/trafego-conexao` e aguardar. Não tentar adivinhar, não cair em fallback, não pedir credenciais avulsas.
   - **`MCP_CONECTOR`:** confirmar que existe uma tool cujo nome termina em `ads_get_ad_accounts` (ou outra `ads_*` do conector). Descobrir sempre pelo final do nome: o começo varia e pode ser um código longo. Se as tools estiverem adormecidas, buscar pelo final do nome antes de chamar. Se a conta vier como não liberada (`is_ads_mcp_enabled: false` ou erro "Ads MCP is gradually being rolled out"), explicar em linguagem simples que a Meta ainda não liberou essa conta no conector e oferecer o modo App pelo `/trafego-conexao`. Conferir também `FB_AD_ACCOUNT_ID` com `grep -q "^FB_AD_ACCOUNT_ID=." .env`; se faltar, a opção "Validar" do `/trafego-conexao` completa.
   - **`APP`:** confirmar com `grep -q "^FB_ACCESS_TOKEN_PERMANENTE=." .env` e `grep -q "^FB_AD_ACCOUNT_ID=." .env` que as duas variáveis existem com valor (o ponto faz a linha vazia contar como ausente). Faltou alguma: `/trafego-conexao`.
3. **Conta de anúncios.** Usar `FB_AD_ACCOUNT_ID` (ou a conta escolhida no command, quando há mais de uma). As tools de escrita do MCP exigem `ad_account_id`.

A sub-skill nunca prossegue sem essa validação. Vale também para `listar` (só leitura): sem conexão, a leitura falha sem mensagem clara.

---

## 1. Sub-fluxos disponíveis

O command `/trafego-publicos` apresenta o menu:

```
[1] Público por evento padrão do pixel       (PageView, ViewContent, AddToCart, InitiateCheckout, Purchase, Lead...)
[2] Público por evento personalizado          (clique em botão, página visitada, UTM ou parâmetro de evento, conversão personalizada opcional)
[3] Público de quem viu vídeo                 (25%, 50%, 75% ou 100%)
[4] Bases por nível                           (iniciante, intermediário, avançado, a partir do resumo do produto)
[5] Público semelhante (lookalike)            (1% a 10% a partir de um público existente)
[6] Lista de clientes                         (CSV de compradores, com hash feito no seu computador)
[7] Engajamento Instagram e Facebook          (perfil, posts, anúncios, formulário de cadastro, sem pixel)
[8] Listar públicos existentes                (com alertas e opção de excluir um público)
```

Cada sub-fluxo vive em `sub-skills/`:
- `publico-evento-padrao.md`
- `publico-evento-personalizado.md`
- `publico-video-view.md`
- `bases-niveis.md`
- `lookalike.md`
- `customer-match.md` (lista de clientes, usa `scripts/preparar_lista_clientes.py`)
- `engajamento-ig-fb.md`
- `listar.md`

---

## 2. Roteamento por modo (ler antes dos endpoints)

O MCP é o caminho padrão. O modo App (`curl`) é a alternativa para conta ainda não liberada no MCP. Quando o MCP não tem a operação, a skill conduz o aluno por um passo a passo curto no Gerenciador e depois segue o fluxo.

| Operação | MCP (`MCP_CONECTOR`) | App (`curl`) |
|---|---|---|
| Listar públicos | `ads_get_ad_account_custom_audiences` | `GET /act_<id>/customaudiences` |
| Ler 1 público (regra, status, origem) | `ads_get_custom_audience` | `GET /<audience_id>?fields=...` |
| Conjuntos que usam um público | `ads_get_custom_audience_adsets` | `GET /<audience_id>/adsets` |
| Criar público de site (evento padrão ou personalizado) | `ads_create_custom_audience` com subtipo `WEBSITE` + `rule` | `POST /act_<id>/customaudiences` (sem `subtype`) |
| Criar lista de clientes | `ads_create_custom_audience` com subtipo `CUSTOM` | `POST /act_<id>/customaudiences` (`subtype=CUSTOM`) |
| Enviar os lotes com hash | `ads_update_custom_audience_users` | `POST /<audience_id>/users` com `-F "payload=<lote.json"` |
| Criar público semelhante | `ads_create_custom_audience` com subtipo `LOOKALIKE` | `POST /act_<id>/customaudiences` (`subtype=LOOKALIKE`) |
| Criar público de vídeo | `ads_create_custom_audience` com o subtipo de engajamento de vídeo que o schema oferecer | `POST /act_<id>/customaudiences` (`subtype=ENGAGEMENT` + `prefill=true`) |
| Criar engajamento Instagram/Facebook | `ads_create_custom_audience` com subtipo de engajamento | `POST /act_<id>/customaudiences` (sem `subtype`) |
| Atualizar público | `ads_update_custom_audience` | `POST /<audience_id>` |
| Excluir público (sempre à parte) | `ads_delete_custom_audience` | sem `curl -X DELETE` direto: Gerenciador ou comando sem token para o aluno rodar |
| Listar conversões personalizadas | `ads_get_customconversions` | `GET /act_<id>/customconversions` |
| Criar conversão personalizada | passo manual guiado no Gerenciador de Eventos | `POST /act_<id>/customconversions` |
| Disparos de eventos do pixel | `ads_get_dataset_stats` (pixels por `ads_get_datasets`) | `GET /<pixel_id>/stats` |
| Buscar interesse por nome | passo manual guiado no Gerenciador (recomendar público aberto com Advantage+) | `GET /search?type=adinterest` |
| Estimar tamanho de segmentação | passo manual guiado (o Gerenciador mostra o tamanho estimado) | `GET /act_<id>/delivery_estimate` |
| Páginas, Instagram, vídeos e anúncios (descoberta) | Páginas: `ads_get_ad_account_pages` (Página fora da conta: `ads_get_user_pages`, `ads_get_pages_for_business`); Instagram e Reels: `ads_get_ig_accounts`, `ads_get_ig_media`; anúncios: `ads_get_ad_entities`, `ads_get_creatives`. Vídeo que está só na Página: passo manual guiado | `GET /me/accounts`, `/<page_id>?fields=instagram_business_account`, `/<ig_business_id>/media`, `/<page_id>/videos`, `/act_<id>/ads` |

**Parâmetros das tools do MCP:** a skill não inventa nome de parâmetro. Antes da primeira chamada de cada tool, ler o schema dela e preencher só o que o schema pede (o `subtype` é obrigatório na `ads_create_custom_audience`). Se a Meta recusar um subtipo pelo MCP (erro de parâmetro, subtipo não aceito), não insistir: explicar e seguir pelo passo manual guiado no Gerenciador descrito na sub-skill.

> **`subtype` no `curl` (modo App) varia por tipo e foi conferido na prática:** público de evento do pixel e de engajamento Instagram/Facebook **não** levam `subtype` no POST (a Meta v25 infere pela regra; enviar devolve `error_subcode 1870053`). Público de vídeo leva `subtype=ENGAGEMENT` + `prefill=true`. Lista de clientes leva `subtype=CUSTOM`. Semelhante leva `subtype=LOOKALIKE`. Siga o que cada sub-skill indica. Na tool do MCP o `subtype` é sempre obrigatório.

### 2.1 Endpoints brutos (modo App)

```
POST   /act_<id>/customaudiences            (site, vídeo, engajamento, lista de clientes, semelhante)
POST   /<audience_id>/users                 (enviar lotes com hash, lista de clientes)
GET    /act_<id>/customaudiences            (listar)
POST   /act_<id>/customconversions          (conversão personalizada, opcional no sub-fluxo [2])
GET    /act_<id>/saved_audiences            (só leitura; a Meta v25 não aceita POST aqui)
GET    /<audience_id>?fields=name,subtype,approximate_count_lower_bound,approximate_count_upper_bound,delivery_status,operation_status,description,rule,data_source
GET    /me/accounts                         (Páginas, engajamento)
GET    /<page_id>?fields=instagram_business_account   (conta do Instagram, engajamento)
GET    /<page_id>/leadgen_forms             (formulários de cadastro, engajamento)
GET    /act_<id>/delivery_estimate?optimization_goal=REACH&targeting_spec=<JSON>   (tamanho das bases por nível; só leitura)
```

API: `v25.0`. Cada chamada é um `Bash(curl ...)` separado, token inline lido do `.env` na própria chamada (seção "LEITURA SEGURA DO .env" do CLAUDE.md) e `curl -g` sempre que a URL tiver `{}` ou `[]` (fields aninhados, `filtering`, listas).

### 2.2 Permissões (modo App)
- `ads_management` (escrita)
- `ads_read`
- `business_management` (públicos que usam pixel de outro Business)

Sem elas, encaminhar ao `/trafego-conexao` para gerar o token de novo. No MCP, as permissões vêm do login do conector.

---

## 3. Tipos de público

| Tipo | Subtipo Meta | Quando usar |
|---|---|---|
| Público de site | `WEBSITE` | Visitantes do site, regra por URL ou evento do pixel |
| Evento do pixel | `WEBSITE` (regra por evento) | Quem disparou um evento (PageView, Purchase ou evento próprio) |
| Vídeo | `ENGAGEMENT` (fonte vídeo) | Quem viu X% do vídeo |
| Engajamento Instagram/Página | `ENGAGEMENT` (`ig_business`, `page`, `ad`, `lead_gen`) | Quem interagiu com perfil, posts, anúncios ou formulário |
| Lista de clientes | `CUSTOM` | Lista de compradores ou leads que o aluno já tem fora da Meta |
| Semelhante | `LOOKALIKE` | Pessoas parecidas com um público existente |
| Base por nível (arquivo local) | sem subtipo, arquivo `.md` | Segmentação de idade, local, idioma e interesses. A Meta v25 não aceita criar público salvo pela API, então a base fica salva como arquivo e entra no conjunto na hora de criar a campanha |

---

## 4. Janelas (retenção)

| Janela | Uso típico |
|---|---|
| 1 dia | Remarketing muito quente (pós-clique no checkout) |
| 7 dias | Remarketing curto (carrinho recente) |
| 14 dias | Remarketing médio |
| 30 dias | Visitantes recentes (padrão mais comum) |
| 60 dias | Produto de ticket médio |
| 90 dias | Remarketing longo |
| 180 dias | Máximo para evento do pixel |

Evento do pixel: máximo de 180 dias (a maioria das contas tem dado de até 90). Vídeo e engajamento: até 365 dias (formulário de cadastro: até 90). A skill sempre pergunta a janela, com padrão de 30 dias.

---

## 5. Convenção de nome

```
[WS] {tipo}-{descricao}-{janela}d-{produto-slug}
```

Exemplos:
- `[WS] PageView-loja-30d-curso-tarot`
- `[WS] Purchase-90d-curso-tarot`
- `[WS] LAL1pct-Compradores-curso-tarot`
- `[WS] Video25pct-VSL-30d-curso-tarot`
- `[WS] CustomEvent-ClickWhatsApp-30d-curso-tarot`
- `[WS] CustomerMatch-Compradores-Hotmart-curso-tarot`
- `[WS] Saved-Iniciantes-curso-tarot`

O prefixo `[WS]` marca o que veio do Severino. O sufixo é o slug do produto ativo (`meus-produtos/.ativo`).

---

## 6. Tamanho estimado e alertas

> ⚠️ O campo `approximate_count` puro foi removido na Marketing API v25 (devolve `error code 100, Tried accessing nonexisting field`). Usar a faixa `approximate_count_lower_bound` + `approximate_count_upper_bound`, ou o tamanho no Gerenciador (Públicos, coluna "Tamanho").

1. **Saúde do público** (depois de criado): `delivery_status.code` e `operation_status.code`. `delivery_status.code == 200` indica público pronto para uso. Outros códigos (300, 400, 441) indicam estados como populando ou erro.
2. **Faixa estimada:** `approximate_count_lower_bound` e `approximate_count_upper_bound`, atualizados pela Meta de tempos em tempos.
3. **Tamanho exato:** só no Gerenciador.

| Faixa | Status | Ação |
|---|---|---|
| < 1.000 | 🔴 Micro | Alertar e perguntar se quer ampliar o critério antes de criar |
| 1.000 a 10.000 | 🟡 Pequena | Serve para teste, mas o algoritmo tem pouco espaço |
| 10.000 a 100.000 | 🟢 Saudável | Faixa ideal |
| 100.000 a 1.000.000 | 🟢 Grande | Boa para escala |
| > 1.000.000 | 🟡 Ampla demais | Em remarketing, suspeito (regra ampla demais) |

Público de pixel sem histórico do evento: avisar "o tamanho aparece em até 24h depois da criação".

---

## 7. Fluxo padrão de criação (qualquer sub-fluxo)

```
[0] Passo 0 (produto ativo, conexão, conta)
[1] Coletar os inputs do sub-fluxo, uma pergunta por mensagem
[2] Calcular nome, regra e janela
     (janela acima do limite da fonte, ver seção 4 e a tabela "Limites e pegadinhas"
      da sub-skill: voltar à pergunta da janela antes do bloco 🛡️)
[3] Consultar tamanho estimado (quando aplicável)
[4] Resumo em linguagem natural e confirmação
[5] Bloco 🛡️ com o Preview YAML e "sim"
[6] Criar (tool do MCP ou curl no App)
[7] Devolver: nome, status e como desfazer (sem ID no texto principal)
[8] Marcar como desatualizado o cache do /trafego-insights da conta
     (regra de invalidação em .claude/skills/trafego-insights/sub-skills/cache.md)
[9] Gravar o registro em meus-produtos/_global/trafego/publicos/{audience_id}.md
     e atualizar meus-produtos/_global/trafego/publicos/INDEX.md
```

Antes de cada operação longa, anunciar no padrão do CLAUDE.md com a faixa calibrada de `.claude/rules/tempo-estimado.md` (tabela "Anúncio de tempo por sub-fluxo", no Passo 3 do command `/trafego-publicos`), por exemplo: `🔍 Próximo passo: criar o público na sua conta e conferir a regra gravada (2 passos). Tempo estimado: cerca de 30 segundos.`

---

## 8. Registro local

Públicos pertencem à conta de anúncios, não a um produto. Por isso ficam em `meus-produtos/_global/trafego/publicos/`:

```
meus-produtos/_global/trafego/publicos/
├── INDEX.md                                          (lista de públicos criados e detectados)
├── {audience_id}.md                                  (um por público: nome, regra, janela, tamanho na criação, sub-fluxo, data, como desfazer)
└── saved-targeting-{nivel}-{produto-slug}.md         (bases por nível)
```

`INDEX.md` é atualizado a cada criação e reconstruído a cada listagem (validade de 1 hora). Nunca gravar hash, e-mail, telefone ou qualquer dado pessoal nesses arquivos.

### 8.1 Saída (público criado na conta)

```yaml
operacao: criar_audience
sub_fluxo: evento_padrao | evento_personalizado | video_view | lookalike | customer_match | engajamento_ig_fb
modo: MCP_CONECTOR | APP
ad_account_id: act_<id>
audiences_criadas:
  - id: <audience_id>
    nome: "[WS] PageView-loja-30d-curso-tarot"
    subtype: WEBSITE | ENGAGEMENT | LOOKALIKE | CUSTOM
    janela_dias: 30
    regra: { ... }
    tamanho_estimado: 14500 | "indisponivel" | "calculando"
    status: criada
    como_desfazer: "excluir pelo /trafego-publicos opção 8 (bloco 🛡️ próprio) ou no Gerenciador"
invalidacoes:
  - cache_trafego_insights: stale
handoffs_sugeridos:
  - texto: "Usar esse público numa campanha de remarketing"
    skill: /trafego-criar-campanha
  - texto: "Criar semelhante a partir dele"
    skill: /trafego-publicos opção 5
```

### 8.2 Saída (bases por nível, arquivo local)

```yaml
operacao: gravar_recipe_targeting
sub_fluxo: bases_niveis
saved_targetings_criados:
  - arquivo_local: "meus-produtos/_global/trafego/publicos/saved-targeting-iniciantes-curso-tarot.md"
    nome_interno: "[WS] Saved-Iniciantes-curso-tarot"
    nivel: iniciantes
    validacao_interesses: api_search | manual_gerenciador
    como_desfazer: "apagar o arquivo local"
handoffs_sugeridos:
  - texto: "Criar campanha com uma dessas bases"
    skill: /trafego-criar-campanha
```

---

## 9. Quando NÃO usar esta skill

- Diagnosticar pixel: `/trafego-pixel`.
- Criar a campanha que usa o público: `/trafego-criar-campanha` (que pode chamar esta skill).
- Campanha de remarketing completa (público + campanha): `/trafego-testes` opção 10.

---

## 10. Princípios que esta skill nunca viola

1. **Resumo e bloco 🛡️ antes de escrever.** Sempre.
2. **Um "sim" por lote.** Exclusão sempre à parte.
3. **Convenção de nome `[WS]`.**
4. **Alerta para público micro** (< 1.000).
5. **Não conecta público a conjunto.** Só cria. A skill que pediu faz a ligação.
6. **Não apaga sem gate próprio.** No App, nunca `curl -X DELETE` direto. Bases por nível são arquivo local: desfazer é apagar o arquivo, sem tocar a conta.
7. **Marca o cache do `/trafego-insights` como desatualizado** depois de criar.
8. **Registro local sem dado pessoal.**
9. **Conversão personalizada só no sub-fluxo [2]**, quando serve a um público da mesma sessão e o aluno escolheu criar.
10. **Lista de clientes nunca passa pelo chat em claro.** A skill não abre nem mostra o CSV: quem lê o arquivo é o script local, que só devolve contagens.

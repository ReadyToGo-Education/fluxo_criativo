---
name: trafego-publicos
description: >
  Cria, lista e gerencia públicos (audiences) do Meta Ads — Custom Audiences, Lookalike Audiences,
  públicos por evento padrão do pixel, públicos por evento personalizado (cria evento + audience),
  públicos por engajamento de vídeo (25/50/75/100%) e bases por nível (iniciante, intermediário,
  avançado) com combinação de interesses + behaviors. Escreve na conta Meta Ads via Marketing API.
  Use quando o aluno pedir "criar público", "audience custom", "lookalike", "remarketing",
  "público de quem viu meu vídeo", "público dos compradores", "criar público de quem clicou
  no botão", "lista de remarketing".
user-invocable: false
---

## 🛡️ Gate obrigatório antes de qualquer escrita na Graph API

Esta skill executa operações que **modificam estado** na conta Meta Ads. Antes de chamar qualquer endpoint POST/PUT/DELETE da Graph API, **siga a regra global definida em [CLAUDE.md](../../../CLAUDE.md)** na seção "GATE EM CAMADA DE CHAT ANTES DE OPERAÇÕES DE ESCRITA NA META GRAPH API":

1. Apresentar o bloco `🛡️ Confirmação necessária antes de tocar na conta Meta` com operação, endpoint humano-legível, o que vai mudar, impacto no aprendizado e reversibilidade.
2. **Nunca exibir o `curl` completo no chat** — carrega o token.
3. Aguardar resposta `sim` (ou variante explícita: aprovo, pode, manda) antes de executar.
4. Em modo lote, mostrar o plano completo antes e pedir confirmação única.
5. Se o aluno responder `não` ou variante (cancelar, abortar), abortar sem chamar a API.
6. **NUNCA usar `python3 << 'EOF'` (heredoc) nem `curl | python3 -c`** com o token. Esses formatos quebram o pattern matching do Claude Code e expõem o token no pop-up nativo. Ver regra "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" no CLAUDE.md.

**Operações desta skill que passam pelo gate:**

- POST /act_<id>/customaudiences (criar Custom Audience)
- POST /act_<id>/customaudiences com origin_audience_id (criar Lookalike)
- POST /<custom_audience_id> (atualizar audience)
- POST /<adaccount>/custom_conversions (criar evento custom para audience)

**Não passam pelo gate:**
- Chamadas GET para leitura (insights, listagens, fields). Estado não muda.
- Sub-fluxo `bases-niveis`: grava recipe local (`.md` no projeto), não faz POST na Graph API. Bastará uma **confirmação textual simples** ("Digite SIM pra gravar os 3 arquivos") antes do `Write`. O bloco 🛡️ completo não se aplica.

---

## 🔌 Passo 0 obrigatório (TODAS as sub-skills, antes de qualquer GET ou POST)

Antes da primeira chamada à Graph API em qualquer sub-fluxo:

1. **Ler `META_AUTH_MODO`** do `.env` via `grep -q "^META_AUTH_MODO=" .env` (presença, não conteúdo).
2. **Se ausente:** acionar `/trafego-conexao` e aguardar conclusão. **Não tentar fallback nem pedir credenciais ad-hoc.**
3. **Se `APP`:** confirmar via `grep -q` presença de `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` no `.env`. Se faltar algum, acionar `/trafego-conexao`.
4. **Se `MCP_CONECTOR`:** confirmar que pelo menos uma tool `mcp__*__ads_*` está disponível.

A sub-skill **nunca prossegue** sem essa validação passar. Aplica-se mesmo a `listar` (read-only) — sem token, GET falha sem mensagem clara, gerando frustração.

Cada sub-skill (`bases-niveis`, `lookalike`, `publico-evento-padrao`, `publico-evento-personalizado`, `publico-video-view`, `customer-match`, `engajamento-ig-fb`, `listar`) tem o Passo 0 documentado no seu próprio arquivo.

---

# Tráfego Públicos. Audiences Meta Ads

Você cria e gerencia públicos (audiences) na conta de anúncios via Marketing API. Esta skill é a única que tem permissão para criar audience nesta arquitetura. Outras skills que precisam de público (`/trafego-criar-campanha`, `/trafego-testes`, `/trafego-escalar` no modo horizontal) chamam esta skill.

**Princípios:**
- Toda criação é precedida por preview YAML + confirmação explícita do aluno.
- Audiences criadas começam disponíveis (não há `PAUSED` para audience). Mas a skill **não as conecta automaticamente** a nenhum adset — só cria. Conexão é responsabilidade da skill que pediu.
- Cache do `/trafego-insights` é invalidado a cada criação (uma audience nova muda a leitura de "audiences existentes").
- Sempre informar tamanho estimado **antes** da confirmação. Audiência micro (< 1.000) gera alerta automático.
- Esta skill **NÃO cria o Evento Personalizado no pixel** — a Meta não expõe endpoint API pra isso (eventos personalizados nascem via Event Setup Tool, snippet `fbq trackCustom` ou Conversion API, todos manuais). Esta skill apenas guia o aluno no caminho escolhido. A skill **pode** criar uma **Conversão Personalizada** apontando para o evento, mas somente como opção dentro do sub-fluxo de audience por evento personalizado.

---

## 1. Sub-fluxos disponíveis

A skill é orquestrada pelo command `/trafego-publicos`, que apresenta o menu:

```
[1] Público por evento padrão do pixel       (PageView, ViewContent, AddToCart, IC, Purchase, Lead, ...)
[2] Público por evento personalizado          (audience filtrada por evento custom do pixel, Conversão Personalizada opcional)
[3] Público por engajamento de vídeo          (viu 25%, 50%, 75%, 100%)
[4] Bases por nível                           (iniciante, intermediário, avançado, do produto ativo)
[5] Lookalike                                 (1%, 2%, 5%, 10% a partir de uma custom audience)
[6] Customer Match                            (upload CSV de compradores — Hotmart, Eduzz, etc.)
[7] Engajamento Instagram/Facebook            (perfil, posts, ads, Lead Form — sem pixel)
[8] Listar audiences existentes
```

Cada sub-fluxo está documentado em `sub-skills/`:
- `publico-evento-padrao.md`
- `publico-evento-personalizado.md`
- `publico-video-view.md`
- `bases-niveis.md`
- `lookalike.md`
- `customer-match.md` (NOVO — upload CSV de base de compradores; sinal direto, gera LAL super qualificada)
- `engajamento-ig-fb.md` (NOVO — engajamento orgânico com Page/IG/ads/Lead Form; não depende de pixel)
- `listar.md`

---

## 2. Endpoints Marketing API

```
POST   /act_<id>/customaudiences            (custom + lookalike + video + engagement + customer_match)
POST   /<audience_id>/users                 (subir hashes SHA-256 — Customer Match)
GET    /act_<id>/customaudiences            (listar)
POST   /<pixel_id>/customconversions        (criar evento personalizado / regra)
POST   /act_<id>/customaudiences            (com `rule` apontando para o custom event)
GET    /act_<id>/saved_audiences            (listar saved audiences existentes — Meta v25 não aceita POST aqui; sub-fluxo bases-niveis grava recipe local em vez de criar)
GET    /<custom_audience_id>?fields=name,subtype,approximate_count_lower_bound,approximate_count_upper_bound,delivery_status,operation_status,description,rule,data_source
GET    /me/accounts                         (listar Pages — Engajamento)
GET    /<page_id>?fields=instagram_business_account  (descobrir conta IG — Engajamento)
GET    /<page_id>/leadgen_forms             (listar Lead Forms — Engajamento)
```

API version: `v25.0`.

### 2.1 Permissões necessárias
- `ads_management` (escrita)
- `ads_read`
- `business_management` (para audiences que precisam acessar o pixel de outro Business)

Sem essas permissões, encerrar com link para `/trafego-conexao` para regenerar token.

---

## 3. Tipos de audience suportados

| Tipo | Subtype Meta | Quando usar |
|---|---|---|
| **Website Custom Audience** | `WEBSITE` | Visitantes do site (regra baseada em URL ou evento de pixel) |
| **Pixel Event Audience** | `WEBSITE` (rule baseada em evento) | Quem disparou um evento específico (PageView, Purchase, ou custom) |
| **Engagement Custom (Video)** | `ENGAGEMENT` (`video` source) | Quem assistiu X% do vídeo |
| **Engagement Custom (IG / Page)** | `ENGAGEMENT` (`ig_business`, `page`) | Quem engajou com perfil do Instagram ou Página do Facebook (não foco desta skill, mas suportado) |
| **Customer File** | `CUSTOM` (upload de CSV) | Lista de emails / telefones (foge ao escopo desta skill no MVP) |
| **Lookalike** | `LOOKALIKE` | Semelhantes a uma source audience |
| **Saved Targeting (recipe local)** | n/a (arquivo local) | Combinação de geo + idade + interesses + behaviors. **Meta v25 não aceita POST em `/saved_audiences`**, então sub-skill `bases-niveis` salva como `.md` em `meus-produtos/{produto}/trafego/publicos/`. Consumido por `/trafego-criar-campanha` via injeção de `targeting_spec` no adset. |

No MVP, a skill foca em: `WEBSITE` (eventos padrão e custom), `ENGAGEMENT video`, `LOOKALIKE`, `CUSTOM` (Customer Match), e **Saved Targeting local** (para bases por nível — não cria Saved Audience nativa por limitação Meta v25).

---

## 4. Janelas (retention) suportadas

A janela é o número de dias que a audience "lembra" do usuário. Janelas comuns:

| Janela | Uso típico |
|---|---|
| 1 dia | Hot remarketing (pós-clique no checkout) |
| 7 dias | Retargeting curto (carrinho recente) |
| 14 dias | Retargeting médio |
| 30 dias | Visitantes recentes do site (default mais comum) |
| 60 dias | Janela de produto de ticket médio |
| 90 dias | Retargeting longo (alcance máximo do Meta para WEBSITE) |
| 180 dias | Apenas para upload de Customer File |

Para evento de pixel, a janela máxima é **180 dias** (mas dados disponíveis são até 90d na maioria das contas). Para video view, máximo **365 dias**.

A skill **sempre pergunta a janela** explicitamente, com default = 30d.

---

## 5. Convenção de nomenclatura

Toda audience criada por esta skill segue convenção de nome para facilitar identificação no Audiences Manager:

```
[FC] {tipo}-{descricao}-{janela}d-{produto-slug}
```

Exemplos:
- `[FC] PageView-loja-30d-curso-tarot`
- `[FC] Purchase-90d-curso-tarot`
- `[FC] LAL1pct-Compradores-90d-curso-tarot`
- `[FC] Video25pct-VSL-30d-curso-tarot`
- `[FC] CustomEvent-ClickWhatsApp-30d-curso-tarot`
- `[FC] Saved-Iniciantes-curso-tarot`

O prefixo `[FC]` (Fluxo Criativo) deixa claro o que veio desta automação. O slug do produto vem de `meus-produtos/.ativo`.

---

## 6. Tamanho estimado e alertas

> ⚠️ **Campo `approximate_count` puro foi removido na Marketing API v25** — retorna `error code 100 — Tried accessing nonexisting field`. Usar a faixa `approximate_count_lower_bound` + `approximate_count_upper_bound` (que existem) ou verificar o tamanho real no Audiences Manager (Meta não expõe contagem precisa via API atualmente).

Antes de criar, a skill estima a faixa de tamanho via:

1. **Saúde da audience** (após criação): `delivery_status.code` + `operation_status.code`. Se `delivery_status.code == 200` → audience pronta pra uso. Códigos diferentes (300, 400, 441) indicam estados específicos (populando, erro, etc).
2. **Faixa estimada via API**: `approximate_count_lower_bound` e `approximate_count_upper_bound` retornam um range (ex: 1100-1300) atualizado periodicamente pelo Meta. Útil pra alertar tamanhos micro/grandes.
3. **Tamanho real**: instruir o aluno a abrir o Audiences Manager (Públicos → audience → coluna "Tamanho") quando precisar de número exato. A API v25 não expõe contagem precisa.

Classificação por faixa (usando `approximate_count_lower_bound` quando disponível):

| Faixa | Status | Ação |
|---|---|---|
| < 1.000 | 🔴 Micro | Alertar e perguntar se quer ampliar critério antes de criar |
| 1.000 a 10.000 | 🟡 Pequena | OK para teste, mas algoritmo terá pouco espaço |
| 10.000 a 100.000 | 🟢 Saudável | Faixa ideal |
| 100.000 a 1.000.000 | 🟢 Grande | Boa para escala |
| > 1.000.000 | 🟡 Ampla demais | Se for retargeting, suspeito (provavelmente regra ampla demais) |

Para audience baseada em evento de pixel ainda sem histórico (pixel sem disparos suficientes), a skill avisa: "tamanho estimado não disponível ainda — Meta calcula em até 24h após criação".

---

## 7. Fluxo padrão de criação (qualquer sub-fluxo)

```
[0] Validar META_AUTH_MODO (gate duro)
[1] Validar produto ativo
[2] Pegar inputs do sub-fluxo
[3] Calcular nome, regra (rule) e janela
[4] Consultar tamanho estimado (quando aplicável)
[5] Preview YAML (mostrar tudo, incluindo nome final, janela, regra, tamanho)
[6] Confirmação explícita ("digite SIM para criar")
[7] POST na Marketing API
[8] Devolver: ID da audience, nome, status, comando de reversão (DELETE endpoint)
[9] Invalidar cache do /trafego-insights e do /trafego-publicos listar
[10] Salvar registro em meus-produtos/{ativo}/trafego/publicos/{id}.md
```

---

## 8. Output esperado

O formato varia se o sub-fluxo cria audience nativa (POST na Graph API) ou recipe local (Write em arquivo `.md`):

### 8.1 Audience nativa (custom, lookalike, video, customer_match, evento_padrao, evento_personalizado, engajamento_ig_fb)

```yaml
operacao: criar_audience
sub_fluxo: evento_padrao | evento_personalizado | video_view | lookalike | customer_match | engajamento_ig_fb
ad_account_id: act_<id>
audiences_criadas:
  - id: <audience_id>
    nome: "[FC] PageView-loja-30d-curso-tarot"
    subtype: WEBSITE | ENGAGEMENT | LOOKALIKE | CUSTOM
    janela_dias: 30
    regra: { ... }                    # JSON da rule conforme Marketing API
    tamanho_estimado: 14500 | "indisponivel" | "calculando"
    status: criada
    rollback_comando: "DELETE /<audience_id>"

invalidacoes:
  - cache_trafego_insights: stale
  - cache_listar_publicos: limpo

handoffs_sugeridos:
  - texto: "Para usar essa audience numa campanha de remarketing"
    skill: /trafego-criar-campanha
  - texto: "Para criar lookalike a partir dela"
    skill: /trafego-publicos opção 5
```

### 8.2 Recipe local (bases_niveis)

```yaml
operacao: gravar_recipe_targeting
sub_fluxo: bases_niveis
ad_account_id: n/a (recipe é local, não tem ad account associado)
saved_targetings_criados:
  - arquivo_local: "meus-produtos/curso-tarot/trafego/publicos/saved-targeting-iniciantes-curso-tarot.md"
    nome_interno: "[FC] Saved-Iniciantes-curso-tarot"
    nivel: iniciantes
    tipo: saved_targeting_local
    tamanho_estimado: { users_lower_bound: 3200000, users_upper_bound: 3700000 }
    rollback_comando: "rm <arquivo_local>"

  - arquivo_local: "meus-produtos/curso-tarot/trafego/publicos/saved-targeting-intermediarios-curso-tarot.md"
    nome_interno: "[FC] Saved-Intermediarios-curso-tarot"
    nivel: intermediarios
    tipo: saved_targeting_local
    rollback_comando: "rm <arquivo_local>"

  - arquivo_local: "meus-produtos/curso-tarot/trafego/publicos/saved-targeting-avancados-curso-tarot.md"
    nome_interno: "[FC] Saved-Avancados-curso-tarot"
    nivel: avancados
    tipo: saved_targeting_local
    rollback_comando: "rm <arquivo_local>"

handoffs_sugeridos:
  - texto: "Para criar campanha usando uma dessas bases"
    skill: /trafego-criar-campanha
    frase_pronta: "usa a base {nivel} do {produto}"
```

---

## 9. Cache e listagem

### 9.1 Cache de listagem
`meus-produtos/{ativo}/trafego/publicos/INDEX.md` é mantido pela skill com a listagem completa de audiences criadas via Workshop + audiences pré-existentes que a skill detectou. Atualizado:
- Após cada criação (append + bump timestamp)
- Após cada chamada do sub-fluxo "Listar" (rebuild)
- TTL: 1 hora. Após esse prazo, listar relê da Graph API.

### 9.2 Registro individual
Cada audience criada gera um arquivo:
```
meus-produtos/{ativo}/trafego/publicos/{audience_id}.md
```
Com: nome, ID, regra completa, janela, tamanho na criação, comando de rollback, sub-fluxo de origem, timestamp.

---

## 10. Quando NÃO usar esta skill

- Para **diagnosticar** pixel: usar `/trafego-pixel`.
- Para **criar campanha** que usa uma audience: usar `/trafego-criar-campanha` (que pode chamar esta skill internamente).
- Para **upload de CSV** de emails (Customer File): fora do escopo do MVP. Usar Audiences Manager direto.
- Para **excluir** audience: instruir o aluno a fazer manualmente no Audiences Manager (a skill **não tem ação de delete** no MVP por segurança).

---

## 11. Princípios que esta skill nunca viola

1. **Preview antes de write.** Sempre.
2. **Confirmação explícita "SIM".** Sem isso, não cria.
3. **Convenção de nomenclatura.** Toda audience criada segue o padrão `[FC] tipo-descricao-janela-produto`.
4. **Alerta para audience micro.** < 1.000 sempre dispara confirmação extra.
5. **Não conecta a adset automaticamente.** Só cria. A skill que pediu é responsável por conectar.
6. **Não deleta.** Operação de delete é manual.
   - **Exceção `bases_niveis`:** como é recipe local (arquivo `.md`), o "delete" é `rm` do arquivo. Não toca conta Meta. Aluno pode executar diretamente sem gate.
7. **Invalida cache** do `/trafego-insights` após criar.
8. **Salva registro local** de toda audience criada com comando de rollback.
9. **Conversão Personalizada só nesta skill** (sub-fluxo evento personalizado) quando ela serve a uma audience da mesma sessão E o aluno explicitamente optou por criá-la. Criação isolada de Conversão é tarefa manual no Events Manager.

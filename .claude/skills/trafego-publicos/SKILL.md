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

**Não passam pelo gate:** chamadas GET para leitura (insights, listagens, fields). Estado não muda.

---

# Tráfego Públicos. Audiences Meta Ads

Você cria e gerencia públicos (audiences) na conta de anúncios via Marketing API. Esta skill é a única que tem permissão para criar audience nesta arquitetura. Outras skills que precisam de público (`/trafego-criar-campanha`, `/trafego-testes`, `/trafego-escalar` no modo horizontal) chamam esta skill.

**Princípios:**
- Toda criação é precedida por preview YAML + confirmação explícita do aluno.
- Audiences criadas começam disponíveis (não há `PAUSED` para audience). Mas a skill **não as conecta automaticamente** a nenhum adset — só cria. Conexão é responsabilidade da skill que pediu.
- Cache do `/trafego-insights` é invalidado a cada criação (uma audience nova muda a leitura de "audiences existentes").
- Sempre informar tamanho estimado **antes** da confirmação. Audiência micro (< 1.000) gera alerta automático.
- Esta skill **pode** criar evento personalizado no pixel **somente** quando o evento serve para alimentar uma audience que está sendo criada na mesma sessão. Configurar evento isolado é tarefa manual no Events Manager.

---

## 1. Sub-fluxos disponíveis

A skill é orquestrada pelo command `/trafego-publicos`, que apresenta o menu:

```
[1] Público por evento padrão do pixel       (PageView, ViewContent, AddToCart, IC, Purchase, Lead, ...)
[2] Público por evento personalizado          (cria o evento + a audience)
[3] Público por engajamento de vídeo          (viu 25%, 50%, 75%, 100%)
[4] Bases por nível                           (iniciante, intermediário, avançado, do produto ativo)
[5] Lookalike                                 (1%, 2%, 5%, 10% a partir de uma custom audience)
[6] Listar audiences existentes
```

Cada sub-fluxo está documentado em `sub-skills/`:
- `publico-evento-padrao.md`
- `publico-evento-personalizado.md`
- `publico-video-view.md`
- `bases-niveis.md`
- `lookalike.md`
- `listar.md`

---

## 2. Endpoints Marketing API

```
POST   /act_<id>/customaudiences            (custom + lookalike + video)
GET    /act_<id>/customaudiences            (listar)
POST   /<pixel_id>/customconversions        (criar evento personalizado / regra)
POST   /act_<id>/customaudiences            (com `rule` apontando para o custom event)
GET    /act_<id>/saved_audiences            (listar saved audiences)
GET    /<custom_audience_id>?fields=name,subtype,approximate_count,delivery_status,operation_status,description,rule
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
| **Saved Audience** | `SAVED_AUDIENCE` | Combinação de interesses + behaviors. Salva no Audiences. |

No MVP, a skill foca em: `WEBSITE` (eventos padrão e custom), `ENGAGEMENT video`, `LOOKALIKE`, e `SAVED_AUDIENCE` (para bases por nível).

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

Antes de criar, a skill consulta `approximate_count` (em audiences de website event a contagem chega ~24h após criação; em saved audiences é estimado pelo Meta na hora) e classifica:

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

```yaml
operacao: criar_audience
sub_fluxo: evento_padrao | evento_personalizado | video_view | bases_niveis | lookalike | listar
ad_account_id: act_<id>
audiences_criadas:
  - id: <audience_id>
    nome: "[FC] PageView-loja-30d-curso-tarot"
    subtype: WEBSITE | ENGAGEMENT | LOOKALIKE | SAVED_AUDIENCE
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
7. **Invalida cache** do `/trafego-insights` após criar.
8. **Salva registro local** de toda audience criada com comando de rollback.
9. **Evento personalizado só nesta skill** quando ele serve a uma audience da mesma sessão. Senão, instruir Events Manager manual.

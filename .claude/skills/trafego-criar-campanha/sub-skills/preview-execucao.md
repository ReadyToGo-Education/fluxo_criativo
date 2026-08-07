# Preview e Execução. Seções 3 e 4 do /trafego-criar-campanha

Esta sub-skill aprofunda o preview obrigatório e a execução da criação. Traz os payloads reais de cada `POST` da Marketing API, a conversão de orçamento, a ordem de criação, o tratamento de falha parcial e a ativação posterior.

Toda operação aqui é escrita. **Nada é executado sem o gate de confirmação no chat** definido no `CLAUDE.md`, seção "GATE EM CAMADA DE CHAT ANTES DE OPERAÇÕES DE ESCRITA NA META GRAPH API".

Toda chamada usa `v25.0`.

---

## 1. Regra de ouro do orçamento. Centavos, não reais

**A Marketing API recebe orçamento na menor unidade da moeda.** Em BRL, isso significa centavos, como inteiro, sem ponto e sem vírgula.

| O aluno diz | No preview YAML | No payload da API |
|---|---|---|
| R$ 100 por dia | `daily_budget_brl: 100.00` | `"daily_budget": 10000` |
| R$ 50 por dia | `daily_budget_brl: 50.00` | `"daily_budget": 5000` |
| R$ 249,90 por dia | `daily_budget_brl: 249.90` | `"daily_budget": 24990` |

**Enviar `100` querendo R$ 100 cria uma campanha de R$ 1,00 por dia.** É o erro mais silencioso desta skill: a API aceita, a campanha sobe, e o aluno só descobre quando não há entrega. Converter sempre com `round(valor_brl * 100)`.

Vale para `daily_budget` e `lifetime_budget`, em campanha (CBO) e em conjunto (ABO).

**Mínimo da conta.** O Meta impõe orçamento diário mínimo que varia por moeda e por `optimization_goal`. Otimização por conversão exige mínimo maior que otimização por impressão. Se a API recusar por valor abaixo do mínimo, informar o valor exigido que veio no erro e perguntar se o aluno quer subir para ele.

---

## 2. Preview. O que o aluno vê e o que fica salvo

Duas saídas distintas, nesta ordem.

### 2.1 YAML completo, salvo em disco

Caminho: `meus-produtos/{ativo}/entregas/trafego/preview-campanha-{tipo_funil}-{slug}-{data}.yaml`

É a referência técnica da execução e o registro de auditoria. Segue o esquema da seção 3 do `SKILL.md`. **Não é mostrado ao aluno** salvo pedido explícito.

### 2.2 Resumo em texto corrido, mostrado ao aluno

Português, sem YAML, sem chaves, sem indentação técnica. Blocos: Conta, Campanha, Conjunto, Anúncios, Validações, Próximas ações.

**Regra de identificação por nome, obrigatória.** Todo ID exibido vem com o nome humano junto, no formato `Nome (ID)`. Vale para conta, Página, Instagram, pixel, conversão personalizada, público, criativo e campanha existente. Buscar o nome antes de exibir quando não estiver em cache:

| Objeto | Chamada |
|---|---|
| Página | `GET /v25.0/{page_id}?fields=name,username` |
| Instagram | `GET /v25.0/{ig_user_id}?fields=username,name` |
| Criativo ou campanha | `GET /v25.0/{id}?fields=name` |

Pixel e conversão personalizada já vêm nomeados das listagens da Fase 5.

Nunca exibir `Page ID 106712754455284` sozinho. Sempre `Leandro Ladeira (106712754455284)`.

### 2.3 Respostas aceitas

| Resposta | Ação |
|---|---|
| "confirmo", "pode subir", "ok" | Executar a criação |
| "muda X" | Ajustar e reapresentar o preview |
| "cancela" | Encerrar sem criar nada |

O preview é obrigatório inclusive no modo expresso. Velocidade não compra atalho de segurança.

---

## 3. Validações antes da primeira chamada de escrita

| Validação | Como | Se falhar |
|---|---|---|
| Pixel existe na conta | `GET /v25.0/act_{id}/adspixels` | Parar. Instruir Gerenciador de Eventos ou `/pagina-pixel` |
| Evento recebendo dados em 7d | `last_fired_time` do pixel | Avisar que o algoritmo otimiza por proxy e pedir confirmação. Não bloquear |
| `FB_PAGE_ID` válido na conta | `GET /v25.0/act_{id}/promote_pages` | Parar e acionar `/trafego-conexao`, opção 4 |
| Instagram, se houver posicionamento IG | `FB_INSTAGRAM_USER_ID` no `.env` | Parar e acionar `/trafego-conexao`, opção 4 |
| Budget coerente com o ticket | `daily_budget < CPA_target * 0.5` | Avisar e pedir confirmação. Não bloquear |
| Nome duplicado ativo há menos de 7 dias | `GET /v25.0/act_{id}/campaigns?fields=name,created_time` | Perguntar: prosseguir, renomear ou cancelar |

Sem pixel, campanha de Sales ou Leads **não é criada**. Regra dura.

---

## 4. Ordem de criação e payloads

A ordem importa: cada nível depende do ID do anterior.

```
1. Campanha        -> campaign_id
2. Conjunto(s)     -> adset_id     (precisa de campaign_id)
3. AdCreative(s)   -> creative_id  (independente, pode ser antes)
4. Anúncio(s)      -> ad_id        (precisa de adset_id + creative_id)
```

### 4.1 Campanha

```
POST /v25.0/act_{ad_account_id}/campaigns
```

```json
{
  "name": "Perpétuo - Curso X - 1-1-3 - 2026-08-07",
  "objective": "OUTCOME_SALES",
  "status": "PAUSED",
  "special_ad_categories": [],
  "buying_type": "AUCTION",
  "daily_budget": 10000
}
```

- `special_ad_categories` é obrigatório mesmo vazio.
- `daily_budget` **só entra aqui se for CBO**. Em ABO, omitir na campanha e enviar no conjunto.
- `status` é sempre `PAUSED` na criação.

### 4.2 Conjunto

```
POST /v25.0/act_{ad_account_id}/adsets
```

```json
{
  "name": "AS - Advantage+ - Brasil",
  "campaign_id": "120203456789",
  "daily_budget": 10000,
  "billing_event": "IMPRESSIONS",
  "optimization_goal": "OFFSITE_CONVERSIONS",
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
  "promoted_object": {
    "pixel_id": "1122334455",
    "custom_event_type": "PURCHASE"
  },
  "targeting": { "...": "vem da Fase 6, ver sub-skill publico-interesses" },
  "start_time": "2026-08-07T18:00:00-03:00",
  "status": "PAUSED",
  "attribution_spec": [
    { "event_type": "CLICK_THROUGH", "window_days": 7 },
    { "event_type": "VIEW_THROUGH", "window_days": 1 }
  ]
}
```

Mapa do `promoted_object` por escolha da Fase 5:

| Escolha do aluno | `promoted_object` |
|---|---|
| Compra (padrão de venda direta) | `{"pixel_id": "...", "custom_event_type": "PURCHASE"}` |
| Lead (captação) | `{"pixel_id": "...", "custom_event_type": "LEAD"}` |
| Conversão personalizada | `{"pixel_id": "...", "custom_conversion_id": "..."}` |

Com `custom_conversion_id`, **não** enviar `custom_event_type` junto. Os dois no mesmo payload conflitam.

- `daily_budget` **só entra aqui se for ABO**. Em CBO, omitir.
- `start_time` default é a próxima hora cheia no fuso do anunciante.
- Omitir `end_time` em perpétuo.

### 4.3 AdCreative

Ver `sub-skills/criativos-upload.md`, seção 7. Retorna `creative_id`.

### 4.4 Anúncio

```
POST /v25.0/act_{ad_account_id}/ads
```

```json
{
  "name": "AD - Dor - Vídeo 30s",
  "adset_id": "120203456789001",
  "creative": { "creative_id": "120203456789555" },
  "status": "PAUSED"
}
```

`creative` é objeto, não string. Enviar `"creative": "123"` falha.

---

## 5. Tratamento de falha

**Princípio: falha parcial preserva o que funcionou.** Não há rollback automático completo. É quase sempre melhor manter o que subiu e deixar o aluno decidir.

| Onde falhou | Ação |
|---|---|
| Campanha | Parar tudo. Nada foi criado, nada a limpar. Retornar o erro |
| Conjunto, e nenhum conjunto subiu | A campanha vazia não serve. Oferecer apagar: `DELETE /v25.0/{campaign_id}`. Só apagar com confirmação |
| Conjunto, com outros já criados | Manter os que subiram. Reportar qual falhou e por quê |
| Criativo ou anúncio | Manter campanha, conjuntos e anúncios anteriores. Reportar item a item e oferecer retentar só os que falharam |

Retornar sempre a lista de falhas com nível, nome, motivo e ação sugerida, como no esquema de saída da seção 5 do `SKILL.md`.

---

## 6. Mapa de erros da criação

| Código ou mensagem | Causa | Ação |
|---|---|---|
| `(#200) Requires page permission` | `FB_PAGE_ID` ausente ou sem acesso na conta | `/trafego-conexao`, opção 4 |
| `(#100) Invalid parameter` em `special_ad_categories` | Campo omitido | Enviar `[]` explicitamente |
| Orçamento abaixo do mínimo | Valor em reais no lugar de centavos, ou abaixo do piso da conta | Reconverter com `* 100`. Se já estava certo, usar o mínimo que veio no erro |
| `Invalid promoted object` | `custom_event_type` e `custom_conversion_id` juntos, ou pixel de outra conta | Enviar só um dos dois. Confirmar que o pixel pertence à conta |
| `Media not ready` | Vídeo ainda processando | Aguardar `video_status: ready` |
| `image_hash not found` | Hash de outra conta de anúncio | Refazer o upload na conta correta |
| `Ad set targeting is too narrow` | Público restrito demais no modo personalizado | Afrouxar interesses ou remover exclusões |
| `(#1487390) Ad account has no funding source` | Conta sem meio de pagamento | Cadastrar cartão ou PIX no Gerenciador. A campanha até sobe PAUSED, mas não ativa |

---

## 7. Saída após a criação

Devolver no formato da seção 5 do `SKILL.md`, com IDs criados, status, link do Gerenciador e próximos passos.

```
url_gerenciador: https://business.facebook.com/adsmanager/manage/campaigns?act={id}&selected_campaign_ids={campaign_id}
```

Próximos passos recomendados, nesta ordem:

1. Abrir o Gerenciador e revisar cada anúncio visualmente (preview, copy, criativo).
2. Ativar quando estiver tudo certo.
3. Após 48h a 72h de veiculação, rodar `/trafego-otimizar` para o primeiro diagnóstico.
4. Para ver números crus a qualquer momento, `/trafego-insights`. Para diagnóstico narrado, `/trafego-analise`.

---

## 8. Ativação posterior

A skill aceita "ativa a campanha" como ação separada, depois da criação.

```
POST /v25.0/{campaign_id}
{ "status": "ACTIVE" }
```

Passa pelo gate de confirmação, com aviso explícito:

```
🛡️ Confirmação necessária antes de tocar na conta Meta

Operação: ativar campanha
Endpoint: POST /{campaign_id}
Objeto: {nome da campanha} ({campaign_id})
O que vai mudar:
  - status PAUSED → ACTIVE
  - a campanha passa a gastar R$ {valor} por dia a partir de agora
Reset de aprendizado esperado: não
Reversível? sim, pausando de novo pela mesma operação

Pode aplicar? Responda "sim" pra confirmar, "não" pra cancelar.
```

Ativar a campanha não ativa conjuntos nem anúncios que estejam pausados individualmente. Se tudo subiu PAUSED junto, ativar a campanha basta, porque os filhos herdam o estado efetivo. Se o aluno pausou algo à mão depois, conferir o `effective_status` de cada nível antes de prometer que está no ar.

---

## 9. Checklist antes de executar

- [ ] Preview salvo em disco e resumo em texto aprovado pelo aluno
- [ ] Gate de confirmação apresentado e respondido com "sim"
- [ ] Orçamento convertido para centavos
- [ ] `daily_budget` em um único nível: campanha se CBO, conjunto se ABO
- [ ] `promoted_object` com pixel válido e um único tipo de evento
- [ ] `special_ad_categories` presente, mesmo vazio
- [ ] Todos os `creative_id` existentes e na mesma conta
- [ ] `status: PAUSED` em todos os níveis
- [ ] Nenhum `curl` completo exibido no chat

# Sub-fluxo. Público por Evento Padrão do Pixel

Cria uma Custom Audience baseada em evento padrão do pixel (PageView, ViewContent, AddToCart, InitiateCheckout, Purchase, Lead, CompleteRegistration, Subscribe).

## Perguntas que cobre

- "Crie um público dos meus visitantes do site"
- "Quero um público de quem comprou nos últimos 90 dias"
- "Crie audiences dos eventos padrões enviados ao meu pixel"
- "Público de quem adicionou ao carrinho mas não comprou"
- "Lista de remarketing dos compradores"

## Inputs

| Input | Default | Descrição |
|---|---|---|
| `pixel_id` | primeiro pixel ativo da conta | Qual pixel alimenta a audience |
| `evento` | obrigatório | Um dos 8 eventos padrão (ver lista abaixo) |
| `janela_dias` | 30 | 1, 7, 14, 30, 60, 90 |
| `nome_extra` | nome do produto | Sufixo descritivo do nome (ex: "loja-principal") |
| `excluir_evento` | nenhum | Evento opcional que EXCLUI usuários (ex: "AddToCart sem Purchase" exclui Purchase) |

### Eventos padrão suportados
- `PageView` — qualquer visita
- `ViewContent` — visualizou produto/post
- `AddToCart` — adicionou ao carrinho
- `InitiateCheckout` — iniciou checkout
- `AddPaymentInfo` — adicionou forma de pagamento
- `Purchase` — comprou
- `Lead` — virou lead
- `CompleteRegistration` — concluiu cadastro
- `Subscribe` — assinou

## Combinações comuns (atalhos)

A skill oferece atalhos para combinações típicas:

| Atalho | Lógica |
|---|---|
| **Carrinho abandonado** | AddToCart **AND NOT** Purchase, janela 30d |
| **Checkout abandonado** | InitiateCheckout **AND NOT** Purchase, janela 30d |
| **Compradores recentes** | Purchase, janela 90d |
| **Visitantes não compradores** | PageView **AND NOT** Purchase, janela 30d |
| **Engajados sem cadastro** | ViewContent **AND NOT** Lead, janela 30d |

Se o aluno escolhe um atalho, a skill monta `rule` automaticamente. Se monta sob medida, a skill pede o evento principal e o evento exclusor opcional.

## Padrão de coleta de inputs (uma pergunta por mensagem)

Regra dura: **NUNCA agrupar 2+ inputs na mesma mensagem**. Aluno **nunca digita pixel_id cru** — sempre via nome ou listagem.

### Ordem fixa

1. **Pixel.** Pergunta neutra (em quase todo caso só tem 1 pixel ativo na conta, então confirmar direto):
   ```
   Achei o pixel "{nome_pixel}" ativo na sua conta. Vou usar esse. Tudo certo?
   ```
   Se tiver múltiplos pixels (raro): listar via `GET /act_<id>/adspixels?fields=id,name,last_fired_time` e pedir escolha.

2. **Modo de coleta.** Numerada:
   ```
   Como você quer montar essa audience?

   1. Atalho — combinações comuns (Carrinho abandonado, Compradores recentes, etc.)
   2. Custom — eu escolho o evento e a janela

   Digite o número:
   ```

3. **Se 1 (Atalho):** mostrar os 5 atalhos da tabela "Combinações comuns" numerados, aluno escolhe.

4. **Se 2 (Custom) — Evento principal.** Numerada:
   ```
   Qual evento padrão usar como base da audience?

   1. Purchase (compra)
   2. Lead (virou lead)
   3. AddToCart (adicionou ao carrinho)
   4. InitiateCheckout (iniciou checkout)
   5. AddPaymentInfo (adicionou forma de pagamento)
   6. ViewContent (visualizou conteúdo/produto)
   7. PageView (qualquer visita)
   8. CompleteRegistration (concluiu cadastro)
   9. Subscribe (assinou)

   Digite o número:
   ```

5. **Janela.** Numerada:
   ```
   Por quanto tempo manter a pessoa nessa audience depois do evento?

   1. 7 dias (audience pequena, muito quente — bom pra remarketing curto)
   2. 30 dias (default, equilíbrio)
   3. 60 dias
   4. 90 dias (máximo recomendado pelo curso — audiences mais velhas ficam obsoletas)
   5. Outro (digito o número de dias, máx 180)

   Digite o número (Enter pra usar 2):
   ```

6. **Excluir evento (opcional).** Numerada:
   ```
   Quer EXCLUIR pessoas que dispararam outro evento? (ex: AddToCart mas NÃO comprou)

   1. Não, só inclusão
   2. Sim, excluir quem disparou Purchase (mais comum — vira audience de carrinho abandonado)
   3. Sim, escolho outro evento exclusor (lista de eventos padrão)

   Digite o número (Enter pra usar 1):
   ```

7. **Nome.** Sugerir auto-gerado seguindo `[FC] {Evento}-{janela}d-{produto-slug}` ou `[FC] {Atalho}-{produto-slug}` e perguntar "uso esse ou prefere outro?".

**Validação automática (não passa pelo aluno):**
- Antes de seguir, cruzar com `/trafego-pixel` ou `GET /<pixel_id>/stats?aggregation=event` pra ver se o evento escolhido disparou ao menos 1x nos últimos 30d. Se não disparou: avisar "Esse evento ainda não foi disparado pelo seu pixel nos últimos 30d. Audience vai começar do zero (vazia)."

**Proibido:**
- Pedir `pixel_id`, `retention_seconds`, `rule.inclusions.event_sources` ou qualquer chave da Marketing API direto ao aluno.
- Agrupar 2+ inputs na mesma mensagem.
- Pular pro Preview YAML sem passar pelos passos 1-6.

## Rule (formato Marketing API)

Para evento simples:
```json
{
  "inclusions": {
    "operator": "or",
    "rules": [{
      "event_sources": [{"id": "<pixel_id>", "type": "pixel"}],
      "retention_seconds": 2592000,
      "filter": {
        "operator": "and",
        "filters": [{
          "field": "event",
          "operator": "eq",
          "value": "Purchase"
        }]
      }
    }]
  }
}
```

Para inclusão + exclusão:
```json
{
  "inclusions": { ... AddToCart ... },
  "exclusions": { ... Purchase ... }
}
```

`retention_seconds` = `janela_dias * 86400`.

## Endpoint

> ⚠️ **NÃO enviar campo `subtype` no POST.** A Meta v25.0 infere `subtype=WEBSITE` automaticamente a partir da estrutura da rule (presença de `event_sources.type=pixel`). Mandar `subtype` retorna `error_subcode 1870053 — O parâmetro 'subtipo' não é aceito na versão atual da API`. (Subtype continua aparecendo no GET pra leitura — apenas não enviar no POST.)

```
POST /act_<id>/customaudiences
{
  "name": "[FC] {Evento}-{nome_extra}-{janela}d-{produto-slug}",
  "description": "Audience criada via Workshop. Evento {evento}, janela {janela}d.",
  "rule": { ... },
  "rule_aggregator": "or"
}
```

## Resumo em linguagem natural antes do Preview YAML (obrigatório)

**Quando exibir:** sempre, após coletar inputs 1-7. Antes do Preview YAML.

**Formato fixo:**

```
📋 Antes de eu criar essa audience na sua conta, deixa eu te resumir:

Vou criar a audience "{nome}":

Quem entra:
   Pessoas que dispararam o evento "{evento em PT}" no seu pixel "{nome_pixel}"
   nos últimos {janela} dias.

{Se houver exclusão:}
Quem fica de fora:
   Pessoas que dispararam o evento "{evento_exclusor em PT}" no mesmo período.
   (resultado: gente que iniciou ação X mas não converteu — clássico carrinho abandonado)

Tamanho estimado: Meta calcula em ~24h. Por enquanto aparece como "calculando".

⏰ Importante:
   - Audience nova leva ~24h pra começar a popular.
   - Se você criar campanha com ela antes disso, entrega zero.
   - Atualiza sozinha a cada 24h conforme novas pessoas disparam o evento.

Onde vai aparecer:
   Gerenciador de Anúncios → Públicos → procurar "[FC] {Evento}-..."

Tá certo? (sim segue pro YAML técnico, não cancela aqui)
```

**Regras de tradução obrigatórias:**

| Campo técnico | Tradução |
|---|---|
| `event: Purchase` | "compra concluída" |
| `event: Lead` | "virou lead" |
| `event: AddToCart` | "adicionou produto ao carrinho" |
| `event: InitiateCheckout` | "iniciou o checkout" |
| `event: ViewContent` | "visualizou um produto ou página" |
| `event: PageView` | "visitou qualquer página do site" |
| `event: CompleteRegistration` | "concluiu o cadastro" |
| `event: Subscribe` | "assinou" |
| `retention_seconds: 2592000` | "30 dias" |
| `retention_seconds: 7776000` | "90 dias" |
| `subtype: WEBSITE` | "audience de pixel do site" |
| `event_sources[{id, type: pixel}]` | nome do pixel (nunca o id) |

**Proibido:**
- Mostrar `retention_seconds` em número cru, `pixel_id`, `rule` JSON, eventos em inglês sem tradução.
- Pular esse resumo pra ir direto pro YAML.

## Preview YAML antes de criar

```yaml
sub_fluxo: publico_evento_padrao
nome_final: "[FC] Purchase-90d-curso-tarot"
pixel: "{nome_do_pixel}" ({pixel_id})
evento_principal: Purchase
evento_exclusor: nenhum
janela_dias: 90
retention_seconds: 7776000
tamanho_estimado: "calculando" (Meta atualiza em ~24h após criação)

confirma? (digite SIM para criar)
```

## Após criar

- Devolve `id` da audience
- Atualiza `meus-produtos/{ativo}/trafego/publicos/INDEX.md`
- Cria `meus-produtos/{ativo}/trafego/publicos/{id}.md` com a regra completa
- Sugere próximos passos:

```
✅ Audience criada: [FC] Purchase-90d-curso-tarot
   ID: 6123456789

⚠️ Atenção (possível bug visual da UI da Meta):
   Audiences criadas via API podem abrir o modal de "Editar público" com
   os campos "Pixel" e/ou "Evento" aparecendo VAZIOS, mesmo com a regra
   íntegra no banco. Já confirmado em audiences de vídeo e IG Business
   (ver publico-video-view.md e engajamento-ig-fb.md) e pode acontecer
   também em audiences de pixel. Se acontecer:
   - NÃO clique em "Atualizar público" com os campos vazios — isso
     sobrescreveria a regra com vazio e quebraria a audience.
   - Fechar pelo "Cancelar" ou pelo "X".
   - Pra confirmar a regra real: /trafego-publicos opção 8 (Listar) ou
     GET /<audience_id>?fields=rule,delivery_status,operation_status.

Próximos passos:
- Para criar uma lookalike a partir dela: /trafego-publicos opção 5
- Para usar como remarketing: /trafego-criar-campanha (audience custom de remarketing)
- Para listar todas as audiences criadas: /trafego-publicos opção 6

Pra excluir essa audience se quiser:
   No Gerenciador → Públicos → procurar pelo nome → botão de 3 pontos → Excluir.
   (Ou rode /trafego-publicos opção 6 → Listar → escolher → excluir — quando esse sub-fluxo estiver disponível.)
```

## Avisos

- **Audience nova leva ~24h** para começar a popular. Tamanho estimado pode aparecer como `calculando`.
- **Pixel sem histórico do evento** = audience vai começar do zero. Avisar o aluno se o evento escolhido não disparou nenhuma vez nos últimos 30d (cruzar com `/trafego-pixel`).
- **Janela máxima** para WEBSITE é 180d (Meta), mas a skill limita default a 90d para evitar audiences obsoletas.
- **Bug visual da UI da Meta — pode afetar pixel audiences.** Confirmado em vídeo e IG Business (audience criada via API com modal de edição mostrando campos vazios). Estruturalmente o mesmo padrão (POST `customaudiences` com `rule.inclusions.event_sources` + `filter`) é usado aqui, então pode ocorrer. Nunca clicar "Atualizar público" com dropdowns vazios — sobrescreve a regra. Critério de saúde confiável é a API.

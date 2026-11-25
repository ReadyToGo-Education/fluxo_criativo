# Sub-fluxo. Público por Evento Padrão do Pixel

Cria um público personalizado a partir de um evento padrão do pixel (PageView, ViewContent, AddToCart, InitiateCheckout, AddPaymentInfo, Purchase, Lead, CompleteRegistration, Subscribe).

Passo 0 (produto ativo, conexão, conta) e gate: ver `SKILL.md` desta skill.

## Perguntas que cobre

- "Crie um público dos meus visitantes do site"
- "Quero um público de quem comprou nos últimos 90 dias"
- "Crie públicos dos eventos padrão enviados ao meu pixel"
- "Público de quem adicionou ao carrinho mas não comprou"
- "Lista de remarketing dos compradores"

## Inputs

| Input | Padrão | Descrição |
|---|---|---|
| `pixel_id` | primeiro pixel ativo da conta | Pixel que alimenta o público |
| `evento` | obrigatório | Um dos eventos padrão abaixo |
| `janela_dias` | 30 | 1, 7, 14, 30, 60, 90 (máximo 180) |
| `nome_extra` | nome do produto | Sufixo descritivo (ex: "loja-principal") |
| `excluir_evento` | nenhum | Evento opcional que EXCLUI pessoas (ex: carrinho sem compra exclui Purchase) |

### Eventos padrão suportados
- `PageView`: qualquer visita
- `ViewContent`: viu produto ou página
- `AddToCart`: adicionou ao carrinho
- `InitiateCheckout`: iniciou o checkout
- `AddPaymentInfo`: adicionou forma de pagamento
- `Purchase`: comprou
- `Lead`: virou lead
- `CompleteRegistration`: concluiu cadastro
- `Subscribe`: assinou

## Combinações comuns (atalhos)

| Atalho | Lógica |
|---|---|
| **Carrinho abandonado** | AddToCart **E NÃO** Purchase, janela 30d |
| **Checkout abandonado** | InitiateCheckout **E NÃO** Purchase, janela 30d |
| **Compradores recentes** | Purchase, janela 90d |
| **Visitantes não compradores** | PageView **E NÃO** Purchase, janela 30d |
| **Engajados sem cadastro** | ViewContent **E NÃO** Lead, janela 30d |

Com atalho, a skill monta a regra sozinha. Sob medida, pede o evento principal e o evento de exclusão opcional.

## Coleta de inputs (uma pergunta por mensagem)

Regra dura: **nunca agrupar 2 ou mais inputs na mesma mensagem**. O aluno nunca digita `pixel_id`: sempre por nome ou listagem.

### Ordem fixa

1. **Pixel.** Quase sempre há 1 pixel ativo, então confirmar direto:
   ```
   Achei o pixel "{nome_pixel}" ativo na sua conta. Vou usar esse. Tudo certo?
   ```
   Com vários pixels (raro), listar e pedir a escolha. MCP: `ads_get_datasets`. App: `GET /act_<id>/adspixels?fields=id,name,last_fired_time`.

2. **Modo de montagem.**
   ```
   Como você quer montar esse público?

   1. Atalho: combinações comuns (carrinho abandonado, compradores recentes etc.)
   2. Sob medida: eu escolho o evento e a janela

   Digite o número:
   ```

3. **Se 1 (Atalho):** mostrar os 5 atalhos da tabela "Combinações comuns" numerados.

4. **Se 2 (Sob medida), evento principal:**
   ```
   Qual evento padrão usar como base do público?

   1. Purchase (compra)
   2. Lead (virou lead)
   3. AddToCart (adicionou ao carrinho)
   4. InitiateCheckout (iniciou o checkout)
   5. AddPaymentInfo (adicionou forma de pagamento)
   6. ViewContent (viu conteúdo ou produto)
   7. PageView (qualquer visita)
   8. CompleteRegistration (concluiu cadastro)
   9. Subscribe (assinou)

   Digite o número:
   ```

5. **Janela.**
   ```
   Por quanto tempo a pessoa fica nesse público depois do evento?

   1. 7 dias (público pequeno e muito quente, bom para remarketing curto)
   2. 30 dias (padrão, equilíbrio)
   3. 60 dias
   4. 90 dias (máximo recomendado: públicos mais velhos ficam desatualizados)
   5. Outro (digito o número de dias, máximo 180)

   Digite o número (Enter para usar 2):
   ```

6. **Excluir evento (opcional).**
   ```
   Quer EXCLUIR quem disparou outro evento? (ex: adicionou ao carrinho mas NÃO comprou)

   1. Não, só inclusão
   2. Sim, excluir quem comprou (mais comum, vira público de carrinho abandonado)
   3. Sim, escolho outro evento de exclusão

   Digite o número (Enter para usar 1):
   ```

7. **Nome.** Sugerir `[WS] {Evento}-{janela}d-{produto-slug}` ou `[WS] {Atalho}-{produto-slug}` e perguntar "uso esse ou prefere outro?".

**Validação automática (sem passar pelo aluno):** conferir se o evento disparou ao menos 1 vez nos últimos 30 dias. MCP: `ads_get_dataset_stats`. App: `GET /<pixel_id>/stats?aggregation=event`. Se não disparou: avisar "esse evento não disparou no seu pixel nos últimos 30 dias. O público vai começar vazio." Para diagnóstico completo do pixel: `/trafego-pixel`.

**Proibido:**
- Pedir `pixel_id`, `retention_seconds`, `rule` ou qualquer chave da Marketing API ao aluno.
- Agrupar 2 ou mais inputs na mesma mensagem.
- Pular para o bloco 🛡️ sem passar pelos passos 1 a 6.

## Regra (formato da Marketing API)

Evento simples:
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

Inclusão com exclusão:
```json
{
  "inclusions": { "...": "regra do AddToCart" },
  "exclusions": { "...": "regra do Purchase" }
}
```

`retention_seconds` = `janela_dias * 86400`.

## Roteamento por modo

Este sub-fluxo roda direto no MCP.

- **`MCP_CONECTOR`:** tool `ads_create_custom_audience` com `subtype="WEBSITE"` (obrigatório na tool), a `rule` acima (`{inclusions, exclusions}`, como texto JSON se o schema pedir texto) e `ad_account_id`. Demais parâmetros, conforme o schema da tool.
- **`APP`:** `curl` no endpoint abaixo. **No `curl`, NÃO enviar `subtype`.**

> ⚠️ **Diferença entre `curl` e tool no `subtype`:** no `curl`, a Meta v25 infere `subtype=WEBSITE` pela regra (`event_sources.type=pixel`); enviar `subtype` devolve `error_subcode 1870053`. Na tool do MCP, `subtype="WEBSITE"` é obrigatório. A regra é a mesma nos dois.

## Endpoint (modo App)

```
POST /act_<id>/customaudiences
{
  "name": "[WS] {Evento}-{nome_extra}-{janela}d-{produto-slug}",
  "description": "Público criado pelo Severino. Evento {evento}, janela {janela}d.",
  "rule": { ... },
  "rule_aggregator": "or"
}
```

## Resumo em linguagem natural (obrigatório, antes do bloco 🛡️)

```
📋 Antes de eu criar esse público na sua conta, um resumo:

Vou criar o público "{nome}".

Quem entra:
   Pessoas que dispararam o evento "{evento em português}" no seu pixel "{nome_pixel}"
   nos últimos {janela} dias.

{Se houver exclusão:}
Quem fica de fora:
   Pessoas que dispararam "{evento_exclusor em português}" no mesmo período.
   (resultado: gente que começou a ação mas não concluiu, o clássico carrinho abandonado)

Tamanho estimado: a Meta calcula em até 24h. Por enquanto aparece como "calculando".

⏰ Importante:
   - Público novo leva cerca de 24h para começar a popular.
   - Campanha com ele antes disso entrega quase nada.
   - Ele se atualiza sozinho a cada 24h conforme novas pessoas disparam o evento.

Onde vai aparecer:
   Gerenciador de Anúncios → Públicos → procurar "[WS] {Evento}-..."

Está certo? (sim segue para a confirmação final, não cancela aqui)
```

**Tradução obrigatória:**

| Campo técnico | Tradução |
|---|---|
| `event: Purchase` | "compra concluída" |
| `event: Lead` | "virou lead" |
| `event: AddToCart` | "adicionou produto ao carrinho" |
| `event: InitiateCheckout` | "iniciou o checkout" |
| `event: ViewContent` | "viu um produto ou página" |
| `event: PageView` | "visitou qualquer página do site" |
| `event: CompleteRegistration` | "concluiu o cadastro" |
| `event: Subscribe` | "assinou" |
| `retention_seconds: 2592000` | "30 dias" |
| `retention_seconds: 7776000` | "90 dias" |
| `subtype: WEBSITE` | "público de visitantes do site" |
| `event_sources[{id, type: pixel}]` | nome do pixel (nunca o ID) |

**Proibido no resumo:** `retention_seconds` em número, `pixel_id`, JSON da regra, evento em inglês sem tradução.

## Preview YAML (dentro do bloco 🛡️)

```yaml
sub_fluxo: publico_evento_padrao
nome_final: "[WS] Purchase-90d-curso-tarot"
pixel: "{nome_do_pixel}"
evento_principal: Purchase
evento_exclusor: nenhum
janela_dias: 90
retention_seconds: 7776000
tamanho_estimado: "calculando" (a Meta atualiza em até 24h)
modo: MCP_CONECTOR | APP
```

O bloco 🛡️ segue o formato do CLAUDE.md (operação "criar público", reset de aprendizado: não, reversível: sim, excluindo o público com confirmação própria).

## Depois de criar

- Gravar `meus-produtos/_global/trafego/publicos/{id}.md` com a regra completa.
- Atualizar `meus-produtos/_global/trafego/publicos/INDEX.md`.
- Mensagem ao aluno:

```
✅ Público criado: [WS] Purchase-90d-curso-tarot

⚠️ Atenção (possível falha visual do Gerenciador):
   Públicos criados fora do Gerenciador podem abrir a tela "Editar público" com
   os campos "Pixel" e "Evento" VAZIOS, mesmo com a regra certa guardada na Meta.
   Já aconteceu com públicos de vídeo e de Instagram e pode acontecer aqui. Se acontecer:
   - NÃO clique em "Atualizar público" com os campos vazios: isso apagaria a regra.
   - Feche pelo "Cancelar" ou pelo "X".
   - Para conferir a regra real: /trafego-publicos opção 8 (Listar).

Próximos passos:
- Criar um semelhante a partir dele: /trafego-publicos opção 5
- Usar como remarketing: /trafego-criar-campanha
- Ver todos os públicos: /trafego-publicos opção 8

Para excluir esse público depois: /trafego-publicos opção 8 (com confirmação própria)
ou no Gerenciador → Públicos → três pontos → Excluir.
```

## Avisos

- **Público novo leva cerca de 24h** para popular. O tamanho pode aparecer como "calculando".
- **Pixel sem histórico do evento** = público começa vazio. Avisar (cruzar com `/trafego-pixel`).
- **Janela máxima** de evento do pixel é 180 dias; a skill recomenda até 90 para não usar público desatualizado.
- **Falha visual do Gerenciador:** a tela de edição pode mostrar campos vazios. Nunca clicar "Atualizar público" com campos vazios. A conferência confiável é pela leitura do público (`ads_get_custom_audience` no MCP, `GET /<audience_id>?fields=rule,delivery_status,operation_status` no App).

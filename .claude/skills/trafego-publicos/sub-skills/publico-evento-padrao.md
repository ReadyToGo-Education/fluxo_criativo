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

```
POST /act_<id>/customaudiences
{
  "name": "[FC] {Evento}-{nome_extra}-{janela}d-{produto-slug}",
  "subtype": "WEBSITE",
  "description": "Audience criada via Workshop. Evento {evento}, janela {janela}d.",
  "rule": { ... },
  "rule_aggregator": "or"
}
```

## Preview YAML antes de criar

```yaml
sub_fluxo: publico_evento_padrao
nome_final: "[FC] Purchase-90d-curso-tarot"
subtype: WEBSITE
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

Próximos passos:
- Para criar uma lookalike a partir dela: /trafego-publicos opção 5
- Para usar como remarketing: /trafego-criar-campanha (audience custom de remarketing)
- Para listar todas as audiences criadas: /trafego-publicos opção 6

Comando de reversão (manual):
DELETE https://graph.facebook.com/v25.0/6123456789?access_token=TOKEN
```

## Avisos

- **Audience nova leva ~24h** para começar a popular. Tamanho estimado pode aparecer como `calculando`.
- **Pixel sem histórico do evento** = audience vai começar do zero. Avisar o aluno se o evento escolhido não disparou nenhuma vez nos últimos 30d (cruzar com `/trafego-pixel`).
- **Janela máxima** para WEBSITE é 180d (Meta), mas a skill limita default a 90d para evitar audiences obsoletas.

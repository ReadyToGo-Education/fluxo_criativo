# Sub-fluxo. Público por Engajamento de Vídeo

Cria Custom Audience baseada em quem assistiu X% de um vídeo nas plataformas Meta (Facebook ou Instagram). Não depende do pixel.

## Perguntas que cobre

- "Crie um público de quem viu 25% do meu vídeo"
- "Quero remarketing para quem assistiu meu Reel inteiro"
- "Público de quem viu 50% da minha VSL"
- "Lista de remarketing dos engajados com vídeo"

## Inputs

| Input | Default | Descrição |
|---|---|---|
| `video_id` | obrigatório | ID do vídeo no Meta (post ID do Facebook ou ID do Instagram media) |
| `percentual` | obrigatório | 25, 50, 75, 100 |
| `janela_dias` | 30 | 1 a 365 |
| `nome_extra` | nome curto do vídeo | Sufixo do nome da audience |

### Como o aluno informa o vídeo
A skill aceita 4 formas:
1. **ID direto**: `1234567890_9876543210`
2. **URL do post no Facebook**: extrai ID
3. **URL do Reel/Post no Instagram**: extrai shortcode, converte em ID via Graph API
4. **Listagem**: skill lista os vídeos publicados nas páginas/perfis conectados (`GET /act_<id>/advideos` ou `GET /<page_id>/videos`)

## Endpoint

```
POST /act_<id>/customaudiences
{
  "name": "[FC] Video{percentual}pct-{nome_extra}-{janela}d-{produto-slug}",
  "subtype": "ENGAGEMENT",
  "description": "Quem assistiu {percentual}% do vídeo {video_id} nos últimos {janela}d.",
  "rule": {
    "inclusions": {
      "operator": "or",
      "rules": [{
        "event_sources": [{"id": "<video_id>", "type": "video"}],
        "retention_seconds": <janela * 86400>,
        "filter": {
          "operator": "and",
          "filters": [{
            "field": "event",
            "operator": "eq",
            "value": "video_view_<percentual>_percent"
          }]
        }
      }]
    }
  }
}
```

Os eventos disponíveis na API são:
- `video_view_3_seconds`
- `video_view_10_seconds`
- `video_view_25_percent`
- `video_view_50_percent`
- `video_view_75_percent`
- `video_view_95_percent` (Meta usa 95% para "completou", não 100%)

A skill aceita `100` mas mapeia internamente para `video_view_95_percent`.

## Preview YAML

```yaml
sub_fluxo: publico_video_view
video:
  id: 1234567890_9876543210
  titulo: "VSL Curso de Tarot — versão 2"
  duracao: "8:32"
  views_totais: 12.480
percentual: 50
evento_meta: video_view_50_percent
janela_dias: 30
retention_seconds: 2592000
nome_final: "[FC] Video50pct-VSL-30d-curso-tarot"
tamanho_estimado: ~2.100 (estimativa baseada em 50% de retenção média do vídeo)

confirma? (digite SIM)
```

## Estimativa de tamanho

Antes de confirmar, a skill estima:
```
tamanho_estimado = views_totais * curva_retencao(percentual)
```

Curva de retenção típica (média do mercado):
- 25% → 60% dos viewers iniciais
- 50% → 35%
- 75% → 18%
- 100% (95%) → 8%

Esses valores são apenas estimativa. Tamanho real é calculado pelo Meta após criação.

## Após criar

```
✅ Audience criada: [FC] Video50pct-VSL-30d-curso-tarot
   ID: 6123456791

Tamanho estimado: ~2.100 pessoas. Tamanho real disponível no Audiences Manager em ~24h.

Próximo passo:
- Para criar lookalike a partir dela: /trafego-publicos opção 5
- Para usar em retargeting de vídeo: /trafego-criar-campanha
```

## Avisos

- **Vídeo precisa estar publicado** numa Página do Facebook ou Conta Comercial do Instagram conectada ao Business Manager. Vídeos pessoais não geram audience.
- **Vídeos curtos (< 10s)** geralmente não geram volume relevante em 50%/75%. Para Reels rápidos, recomendar percentual 25.
- **Audience não popula retroativamente para criações novas** sob certas condições (Meta tem mudado regras). Para histórico longo, criar antes de publicar mais conteúdo do mesmo tipo.
- **Janela máxima**: 365 dias para vídeo (mais longa que website).

## Casos especiais

### Múltiplos vídeos
A skill aceita lista de até 10 vídeos numa única audience (operador `OR`). Cria uma audience só com a regra:
```
quem viu X% de qualquer um dos vídeos A, B ou C
```
Útil para "público de quem engajou com qualquer vídeo da campanha".

### Cruzamento com outro evento
Não suportado nesta skill no MVP. Se aluno pedir "viu 50% do vídeo E adicionou ao carrinho", encaminhar para criação manual no Audiences Manager (Meta exige rule mais elaborada).

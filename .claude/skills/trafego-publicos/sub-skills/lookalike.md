# Sub-fluxo. Lookalike Audience (LAL)

Cria Lookalike Audience a partir de uma Custom Audience source existente. Audiência semelhante = pessoas que se parecem (comportamento + características) com a source.

## Perguntas que cobre

- "Cria uma lookalike dos meus compradores"
- "Lookalike 1% do meu público de carrinho abandonado"
- "LAL 2% dos visitantes do site"
- "Cria uma lookalike de quem viu 75% do meu vídeo"

## Inputs

| Input | Default | Descrição |
|---|---|---|
| `source_audience_id` | obrigatório | ID da custom audience source |
| `percentual` | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| `pais` | `BR` | País-alvo da lookalike |
| `nome_extra` | descrição da source | Sufixo do nome |

### Como o aluno escolhe a source
A skill primeiro lista as audiences disponíveis (chama o sub-fluxo `listar.md`), filtrando por `subtype != LOOKALIKE` (não dá pra fazer LAL de LAL). Aluno escolhe pelo número.

## Tamanho mínimo da source

O Meta exige mínimo de **100 pessoas** na source para criar lookalike. **Recomendação:** 1.000+ para qualidade decente, 5.000+ para qualidade ótima.

A skill verifica `approximate_count` da source antes de prosseguir:

| Tamanho da source | Permitido | Aviso |
|---|---|---|
| < 100 | ❌ | Bloqueia. Audience source pequena demais. |
| 100 a 999 | ⚠️ | Permitido mas avisa: "qualidade da lookalike vai ser baixa" |
| 1.000 a 4.999 | 🟡 | Aceitável |
| 5.000+ | 🟢 | Ideal |

## Percentuais e tamanhos

LAL no Meta funciona por percentual da população do país-alvo:

| % | Tamanho aproximado (BR) | Quando usar |
|---|---|---|
| 1% | ~2M | Mais semelhante, melhor qualidade. Default recomendado. |
| 2% | ~4M | Equilíbrio. Boa para escala. |
| 3% | ~6M | Quando 1%/2% saturou. |
| 5% | ~10M | Para escala agressiva, qualidade já cai. |
| 10% | ~20M | Quase prospect frio. Última opção. |

A skill recomenda começar em 1% e ampliar conforme a campanha satura.

## Endpoint

```
POST /act_<id>/customaudiences
{
  "name": "[FC] LAL{percentual}pct-{nome_source}-{produto-slug}",
  "subtype": "LOOKALIKE",
  "origin_audience_id": "<source_audience_id>",
  "lookalike_spec": {
    "type": "similarity",
    "country": "BR",
    "ratio": 0.01      // 1%
  }
}
```

`type: "similarity"` é o padrão (mais semelhante). Alternativa é `"reach"` (maior alcance, menor semelhança), mas a skill usa `similarity` por default — mais alinhado à metodologia VTSD de fundo de funil.

## Preview YAML

```yaml
sub_fluxo: lookalike
source:
  id: 6123456789
  nome: "[FC] Purchase-90d-curso-tarot"
  tamanho: 580
nome_final: "[FC] LAL1pct-Compradores-curso-tarot"
percentual: 1
pais: BR
type: similarity
tamanho_estimado: ~2.000.000

⚠️ Source tem 580 pessoas. Qualidade da lookalike pode ser baixa.
   Recomendação: aguardar a source chegar em 1.000+ antes de criar LAL.

Quer criar mesmo assim? (digite SIM)
```

## Múltiplas LAL de uma vez (atalho)

A skill aceita criar múltiplas LAL da mesma source numa única confirmação:

```
A partir de "[FC] Purchase-90d-curso-tarot", criar:
[1] LAL 1% (similarity)
[2] LAL 2% (similarity)
[3] LAL 5% (similarity)

Quer criar:
1. Só a 1%
2. As 3 (1%, 2%, 5%)
3. Customizar
```

## Após criar

```
✅ Lookalike criada: [FC] LAL1pct-Compradores-curso-tarot
   ID: 6123456795

Tamanho estimado: ~2.000.000 (BR)
Status: populando (Meta calcula em ~6-24h)

Como usar:
- Em campanhas COLD para escala (Mandala VTSD: Tipo 7, 9, 11).
- Combinar com criativos de fundo de funil (oferta, autoridade).

Próximos passos:
- Para criar campanha com essa LAL: /trafego-criar-campanha
- Para criar 2% e 5% também: /trafego-publicos opção 5 (mesma source)
```

## Avisos

- **LAL não é instantânea.** Meta leva 6 a 24h para popular. Se usada antes, ad set entrega zero.
- **País único por LAL** no MVP. Para múltiplos países, criar múltiplas LAL.
- **LAL de upload** (Customer File) é mais potente que LAL de pixel — quando o aluno tem CSV de compradores, recomendar upload manual no Audiences Manager (foge ao escopo desta skill).
- **Atualização da LAL** é automática conforme a source cresce. Não precisa recriar.
- **LAL de LAL não é permitida** pelo Meta. A skill bloqueia se `source.subtype == LOOKALIKE`.

# Sub-fluxo. Listar Audiences

Lista as audiences existentes na conta de anúncios com nome, tamanho, status, idade e fonte. Modo apenas leitura.

## Perguntas que cobre

- "Quais audiences eu já tenho?"
- "Lista meus públicos"
- "Quais são as audiences criadas pelo Fluxo Criativo?"
- "Tem algum público inativo ou expirando?"

## Endpoint

```
GET /act_<id>/customaudiences?fields=id,name,subtype,approximate_count,delivery_status,operation_status,description,time_created,time_updated,retention_days,rule_aggregator&limit=100
```

E paralelamente:

```
GET /act_<id>/saved_audiences?fields=id,name,description,targeting,approximate_count&limit=100
```

## O que entregar

### Bloco 1. Resumo
```
🎯 AUDIENCES NA CONTA

Total: 12 audiences
- Custom (WEBSITE):     4
- Engagement (vídeo):   2
- Lookalike:            3
- Saved Audiences:      3

Criadas via Fluxo Criativo (prefixo [FC]): 8
Criadas manualmente:                 4
```

### Bloco 2. Tabela detalhada

```
| Nome                                            | Tipo       | Tamanho   | Status        | Origem        | Criada    |
|-------------------------------------------------|------------|-----------|---------------|---------------|-----------|
| [FC] Purchase-90d-curso-tarot                  | WEBSITE    | 580       | 🟢 Ready      | Fluxo Criativo      | há 12 dias|
| [FC] AddToCart-30d-curso-tarot                 | WEBSITE    | 1.420     | 🟢 Ready      | Fluxo Criativo      | há 12 dias|
| [FC] Video50pct-VSL-30d-curso-tarot            | ENGAGEMENT | 2.180     | 🟢 Ready      | Fluxo Criativo      | há 9 dias |
| [FC] LAL1pct-Compradores-curso-tarot           | LOOKALIKE  | 2.000.000 | 🟢 Ready      | Fluxo Criativo      | há 9 dias |
| [FC] Saved-Iniciantes-curso-tarot              | SAVED      | 18.000.000| 🟢 —          | Fluxo Criativo      | há 5 dias |
| Visitantes 30d (manual)                        | WEBSITE    | 14.500    | 🟢 Ready      | Manual        | há 60 dias|
| Pixel-old-broken                                | WEBSITE    | 0         | 🔴 Empty      | Manual        | há 180 dias|
...
```

### Status

| Indicador | Significado |
|---|---|
| 🟢 Ready | Audience populada e pronta para uso |
| 🟡 Updating | Meta atualizando (criação recente ou refresh em andamento) |
| 🟡 Populating | Audience nova ainda recebendo dados |
| 🔴 Empty | Vazia (não populou ou pixel ficou sem disparo) |
| 🔴 Expired | Sem atualização há 90+ dias (pode estar obsoleta) |
| ⚪ Paused | Manualmente pausada |

### Bloco 3. Audiences criadas pelo Fluxo Criativo (drill-down)

Para cada audience com prefixo `[FC]`, ler o arquivo `meus-produtos/{ativo}/trafego/publicos/{id}.md` e mostrar mais detalhes:

```
🔍 [FC] Purchase-90d-curso-tarot

ID: 6123456789
Tipo: WEBSITE (evento Purchase)
Janela: 90 dias
Tamanho atual: 580 (era 540 há 7 dias, +7%)
Pixel source: 1234567890_loja
Sub-fluxo de origem: publico-evento-padrao
Criada: 2026-04-22
```

### Bloco 4. Alertas

Detectar e listar:

```
⚠️ ATENÇÃO

🔴 1 audience vazia (status Empty)
   - "Pixel-old-broken" (criada há 180 dias, 0 pessoas)
   Ação: investigar pixel ou desativar a audience.

🟡 2 audiences encolhendo > 20% nos últimos 30d
   - "Visitantes 30d (manual)" (-23%)
   - "[FC] AddToCart-30d-curso-tarot" (-18%)
   Causa provável: queda de tráfego ou pixel sem evento.
   Próximo: /trafego-pixel para diagnosticar.

🟡 3 audiences podem ser usadas como source de Lookalike
   - "[FC] Purchase-90d-curso-tarot" (580 pessoas) — pequeno, mas funciona
   - "[FC] AddToCart-30d-curso-tarot" (1.420)
   - "[FC] Video75pct-VSL-30d-curso-tarot" (820)
   Quer criar lookalike? /trafego-publicos opção 5
```

## Rebuild do INDEX.md local

A skill regenera `meus-produtos/{ativo}/trafego/publicos/INDEX.md` com a listagem em formato markdown, sobrescrevendo o anterior. Estrutura:

```markdown
# Audiences — produto curso-tarot

> Atualizado: 2026-05-05 14:32
> Conta: act_<id>

## Custom Audiences (Website)
- [FC] Purchase-90d-curso-tarot — 580 pessoas — 🟢 Ready — `meus-produtos/curso-tarot/trafego/publicos/6123456789.md`
- ...

## Engagement (Vídeo)
- ...

## Lookalike
- ...

## Saved Audiences
- ...

## Audiences manuais detectadas
- Visitantes 30d (manual) — 14.500 — Ready
```

## Filtros suportados

A skill aceita filtros para listagem mais focada:

| Filtro | Comando |
|---|---|
| Só audiences criadas pelo Fluxo Criativo | "lista só do Fluxo Criativo" |
| Só de um tipo | "só lookalikes" / "só de website" |
| Só com status saudável | "só as que estão Ready" |
| Só passíveis de virar source de LAL | "audiences que dá pra usar de lookalike" |
| Tamanho mínimo | "audiences com mais de 5.000 pessoas" |

## Cache

A listagem usa TTL de **1 hora**. Se o aluno acabou de criar uma audience, o cache é invalidado e listagem é atualizada na próxima chamada. Para forçar refresh: `--refresh`.

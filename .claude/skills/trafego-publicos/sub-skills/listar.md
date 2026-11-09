# Sub-fluxo. Listar Públicos (e excluir um público)

Lista os públicos da conta de anúncios com nome, tamanho, status, idade e origem. A listagem é só leitura. No fim, o aluno pode pedir para **excluir** um público: essa é a única escrita deste sub-fluxo e tem bloco 🛡️ e "sim" próprios.

## Passo 0

Igual ao `SKILL.md` desta skill (produto ativo, `META_AUTH_MODO`, conta). A listagem não passa pelo gate, mas o Passo 0 vale igual: sem conexão, a leitura falha sem mensagem clara.

## Perguntas que cobre

- "Quais públicos eu já tenho?"
- "Lista meus públicos"
- "Quais públicos o Severino criou?"
- "Tem algum público vazio ou desatualizado?"
- "Exclui o público X"

## Leitura (roteamento por modo)

- **`MCP_CONECTOR`:** `ads_get_ad_account_custom_audiences` (lista) e `ads_get_custom_audience` (detalhe de um público), com o `ad_account_id`.
- **`APP`:**
  ```
  GET /act_<id>/customaudiences?fields=id,name,subtype,approximate_count_lower_bound,approximate_count_upper_bound,delivery_status,operation_status,description,time_created,time_updated,retention_days,rule_aggregator&limit=100
  ```

> ⚠️ **Não usar o campo `approximate_count` puro**: foi removido na v25 e devolve `error 100, Tried accessing nonexisting field`. Usar a faixa `approximate_count_lower_bound` + `approximate_count_upper_bound`.

Públicos salvos nativos (raros; as bases por nível do Severino são arquivos locais e não aparecem aqui):

```
GET /act_<id>/saved_audiences?fields=id,name,description,targeting,approximate_count_lower_bound,approximate_count_upper_bound&limit=100
```

> No MCP não há tool para públicos salvos. Listar só os públicos personalizados e, para as bases por nível, ler os arquivos `meus-produtos/_global/trafego/publicos/saved-targeting-*.md`.

## O que entregar

### Bloco 1. Resumo
```
🎯 PÚBLICOS NA CONTA

Total: 12 públicos
- Site (pixel):           4
- Engajamento (vídeo):    2
- Semelhantes:            3
- Bases por nível (arquivo local): 3

Criados pelo Severino (prefixo [WS]): 8
Criados manualmente:                  4
```

### Bloco 2. Tabela

```
| Nome                                  | Tipo        | Tamanho    | Status        | Origem    | Criado      |
|---------------------------------------|-------------|------------|---------------|-----------|-------------|
| [WS] Purchase-90d-curso-tarot         | Site        | 580        | 🟢 Pronto     | Severino  | há 12 dias  |
| [WS] AddToCart-30d-curso-tarot        | Site        | 1.420      | 🟢 Pronto     | Severino  | há 12 dias  |
| [WS] Video50pct-VSL-30d-curso-tarot   | Engajamento | 2.180      | 🟢 Pronto     | Severino  | há 9 dias   |
| [WS] LAL1pct-Compradores-curso-tarot  | Semelhante  | 2.000.000  | 🟢 Pronto     | Severino  | há 9 dias   |
| [WS] Saved-Iniciantes-curso-tarot     | Base local  | 18.000.000 | (arquivo)     | Severino  | há 5 dias   |
| Visitantes 30d (manual)               | Site        | 14.500     | 🟢 Pronto     | Manual    | há 60 dias  |
| Pixel-antigo                          | Site        | 0          | 🔴 Vazio      | Manual    | há 180 dias |
```

### Status

| Indicador | Significado |
|---|---|
| 🟢 Pronto | Público populado e pronto para uso |
| 🟡 Atualizando | A Meta está atualizando (criação recente ou atualização) |
| 🟡 Populando | Público novo ainda recebendo dados |
| 🔴 Vazio | Não populou, ou o pixel parou de disparar |
| 🔴 Desatualizado | Sem atualização há 90 dias ou mais |
| ⚪ Pausado | Pausado manualmente |

### Bloco 3. Detalhe dos públicos do Severino

Para cada público com prefixo `[WS]`, ler `meus-produtos/_global/trafego/publicos/{id}.md` e mostrar:

```
🔍 [WS] Purchase-90d-curso-tarot

Tipo: site (evento Purchase)
Janela: 90 dias
Tamanho atual: 580 (era 540 há 7 dias, +7%)
Pixel: {nome do pixel}
Sub-fluxo de origem: publico-evento-padrao
Criado em: 2026-04-22
```

### Bloco 4. Alertas

```
⚠️ ATENÇÃO

🔴 1 público vazio
   - "Pixel-antigo" (criado há 180 dias, 0 pessoas)
   Ação: investigar o pixel (/trafego-pixel) ou excluir o público.

🟡 2 públicos encolhendo mais de 20% em 30 dias
   - "Visitantes 30d (manual)" (-23%)
   - "[WS] AddToCart-30d-curso-tarot" (-18%)
   Causa provável: queda de tráfego ou pixel sem evento.
   Próximo: /trafego-pixel para diagnosticar.

🟡 3 públicos servem de origem para semelhante
   - "[WS] Purchase-90d-curso-tarot" (580 pessoas): pequeno, mas funciona
   - "[WS] AddToCart-30d-curso-tarot" (1.420)
   - "[WS] Video75pct-VSL-30d-curso-tarot" (820)
   Quer criar semelhante? /trafego-publicos opção 5
```

## Reconstruir o INDEX.md local

Regravar `meus-produtos/_global/trafego/publicos/INDEX.md` com a listagem:

```markdown
# Públicos da conta

> Atualizado: 2026-05-05 14:32
> Conta: act_<id>

## Site (pixel)
- [WS] Purchase-90d-curso-tarot · 580 pessoas · 🟢 Pronto · `meus-produtos/_global/trafego/publicos/<id>.md`

## Engajamento (vídeo, Instagram, Página)
- ...

## Semelhantes
- ...

## Bases por nível (arquivos locais)
- ...

## Públicos manuais detectados
- Visitantes 30d (manual) · 14.500 · Pronto
```

## Filtros

| Filtro | Pedido do aluno |
|---|---|
| Só os do Severino | "lista só os do projeto" |
| Só de um tipo | "só semelhantes", "só de site" |
| Só os prontos | "só os que estão prontos" |
| Só os que servem de origem para semelhante | "públicos que dá para usar de lookalike" |
| Tamanho mínimo | "públicos com mais de 5.000 pessoas" |

## Cache

Validade de **1 hora**. Criar um público invalida a listagem; a próxima chamada lê de novo da Meta. Para forçar: "atualizar a lista".

---

## Excluir um público (sempre à parte)

**Quando:** o aluno pede para excluir um público (da lista ou pelo nome). A exclusão **não tem volta** e nunca entra no "sim" de outro lote (regra 7 do gate no CLAUDE.md).

### Passo 1. Identificar o público
Por nome (trecho) ou código da lista. O aluno nunca digita ID.

### Passo 2. Ver o impacto
Listar os conjuntos que usam o público: MCP `ads_get_custom_audience_adsets`; App `GET /<audience_id>/adsets?fields=name,effective_status`. Se algum conjunto ativo usa o público, avisar que ele vai perder essa segmentação (ou a exclusão, se o público estava como "excluir").

Se o público é origem de um semelhante, avisar que o semelhante para de se atualizar.

### Passo 3. Aviso e alternativa
```
⚠️ Excluir um público NÃO tem volta.

Público: "{nome}" (~{tamanho} pessoas)
Usado em: {N} conjunto(s) {lista curta, se houver}

Se a ideia é só parar de usar, basta tirar o público do conjunto ou pausar o
conjunto, sem apagar nada.

Como quer seguir?

1. Excluir mesmo assim
2. Não excluir

Digite o número:
```

### Passo 4. Bloco 🛡️ próprio
```
🛡️ Confirmação necessária antes de tocar na conta Meta

Operação: excluir público
Endpoint: exclusão do público (MCP: ads_delete_custom_audience | App: DELETE /<audience_id>)
Objeto: público "{nome}"
O que vai mudar:
  - o público some da conta, sem volta
  - {N} conjunto(s) perdem essa segmentação
Reset de aprendizado esperado: {sim, se algum conjunto ativo usa o público | não}
Reversível? não (dá para criar de novo, mas o histórico do público se perde)

Pode aplicar? Responda "sim" pra confirmar, "não" pra cancelar.
```

### Passo 5. Executar
- **`MCP_CONECTOR`:** depois do "sim", chamar `ads_delete_custom_audience` (parâmetros conforme o schema da tool).
- **`APP`:** **não rodar `curl -X DELETE` direto.** Oferecer ao aluno:
  ```
  No modo App eu não apago nada por conta própria. Você tem dois caminhos:

  1. Pelo Gerenciador: Públicos → marque "{nome}" → três pontos → Excluir
  2. Por comando, você mesmo roda no terminal Bash (Git Bash no Windows),
     na pasta do projeto. O token é lido do seu .env na hora e não aparece:

     curl -s -X DELETE "https://graph.facebook.com/v25.0/<audience_id>?access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"

  Me avise quando terminar que eu confiro.
  ```

### Passo 6. Conferir e registrar
Conferir pela listagem que o público sumiu. Marcar `excluido_em: {data}` no `meus-produtos/_global/trafego/publicos/{audience_id}.md` e tirar do INDEX. Marcar como desatualizado o cache do `/trafego-insights` da conta.

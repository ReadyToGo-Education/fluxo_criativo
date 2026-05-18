# Sub-fluxo. Resumo Recorrente

Configura envio agendado de relatório do tráfego pelo canal escolhido (Telegram ou WhatsApp). Não é regra do Meta — é agendamento interno do Workshop que dispara `/trafego-analise` na hora certa e envia o resultado pelo canal.

## Perguntas que cobre

- "Me avisa toda segunda-feira com um resumo da semana anterior"
- "Quero relatório diário no WhatsApp às 8h"
- "Resumo semanal no Telegram, todo domingo à noite"
- "Alerta diário se gasto passar de R$ 1.000"

## Inputs

| Input | Default | Descrição |
|---|---|---|
| `frequencia` | obrigatório | `diaria`, `semanal`, `mensal`, ou cron customizado |
| `horario` | 8h00 | Hora do envio (timezone do produto) |
| `dia_semana` | nenhum (diário) | Para semanal, qual dia (0=dom, 6=sáb) |
| `canal` | obrigatório | `telegram` ou `whatsapp` |
| `formato` | resumo padrão | `diagnostico_rapido`, `performance_funil`, `texto_curto` |
| `condicional` | nenhum | Só envia se condição X (ex: gasto > R$ 1.000) |

## Pré-requisitos

A skill **valida primeiro** que o canal está configurado:
- `telegram`: verifica `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` no `.env`. Se faltar, aciona `/configurar-telegram`.
- `whatsapp`: verifica `ZAPI_INSTANCE_ID` e `ZAPI_TOKEN` no `.env`. Se faltar, aciona `/configurar-zapi`.

Sem canal configurado, não cria o agendamento. Encaminha para configuração e depois retoma.

## Como funciona

A skill cria 2 artefatos:

### Artefato 1. Configuração local
```
meus-produtos/{ativo}/trafego/regras/resumos/{schedule_id}.md
```

Conteúdo:
```yaml
schedule_id: <uuid>
nome: "[FC] Resumo-segunda-8h-curso-tarot"
ad_account_id: act_<id>

frequencia: weekly
cron: "0 8 * * 1"               # toda segunda às 8h
timezone: "America/Sao_Paulo"

canal: telegram
chat_id: 123456789

formato: diagnostico_rapido
janela_analise: last_7_days

condicional: null

template_mensagem: |
  📊 Resumo semanal — {data}

  Gasto últimos 7d: R$ {spend}
  Vendas: {purchases} ({roas:.1f}x ROAS)
  CPA: R$ {cpa:.2f}

  🔴 Críticas: {n_criticas}
  🟢 Saudáveis: {n_saudaveis}

  Detalhes: ...

criado_em: 2026-05-05
ultima_execucao: null
```

### Artefato 2. Agendamento na skill `/schedule`

A skill aciona `/schedule create` com o cron + comando que faz:
1. Roda `/trafego-analise` com `output=1` (Diagnóstico Rápido) e `periodo=last_7_days`.
2. Pega o resultado.
3. Renderiza no template_mensagem.
4. Envia via `/enviar-relatorio-ads` (que já tem a integração Telegram/WhatsApp).

## Fluxo

```
[1] Aluno escolhe frequencia (diária/semanal/mensal)
[2] Aluno escolhe horario (default 8h00)
[3] (se semanal) Aluno escolhe dia_semana
[4] Aluno escolhe canal (Telegram ou WhatsApp)
    └── Se canal não configurado, aciona /configurar-telegram ou /configurar-zapi
[5] Aluno escolhe formato:
    [a] Diagnóstico rápido (visão geral 60s)
    [b] Performance & Funil (mais detalhe)
    [c] Texto curto (1 parágrafo)
[6] Aluno define condicional opcional (ex: "só se gasto > R$ 1.000")
[7] Preview do que será enviado
[8] Confirmação SIM
[9] Cria schedule via /schedule
[10] Cria registro local
[11] Devolve schedule_id + comando para cancelar
```

## Preview

```yaml
sub_fluxo: resumo_recorrente
nome_final: "[FC] Resumo-segunda-8h-curso-tarot"

agendamento:
  frequencia: semanal
  cron: "0 8 * * 1"
  proxima_execucao: 2026-05-11 08:00:00 (segunda-feira, em 6 dias)

canal:
  tipo: telegram
  chat_id: 123456789

conteudo:
  formato: diagnostico_rapido
  janela: ultimos 7 dias
  preview_template: |
    📊 Resumo semanal — 11/05/2026

    Gasto últimos 7d: R$ {spend}
    Vendas: {purchases} ({roas} ROAS)
    CPA: R$ {cpa}
    ...

condicional: nenhum (envia sempre)

confirma criar? (digite SIM)
```

## Após criar

```
✅ Resumo recorrente configurado: [FC] Resumo-segunda-8h-curso-tarot
   Schedule ID: sched_abc123
   Próxima execução: segunda-feira 11/05/2026 às 08:00 (Brasília)
   Canal: Telegram (chat 123456789)

Para testar agora (envia 1 mensagem):
   /trafego-regras → opção "executar agora"

Para pausar:
   /schedule pause sched_abc123

Para deletar:
   /schedule delete sched_abc123
```

## Condicional opcional

Se o aluno quer "só me avisa se gasto passar de R$ 1.000", a skill adiciona uma checagem antes do envio:

```python
# Pseudo-código do que o agendamento faz
data = chama_trafego_analise(janela='today', output='diagnostico_rapido')
if data.spend_today > 1000:
    envia_telegram(template.format(**data))
else:
    log("Skipped: gasto abaixo do threshold")
```

A condicional é salva no `schedule.md` e respeitada na hora da execução.

## Templates de mensagem por canal

### Telegram
- Suporta Markdown: **negrito**, _itálico_, `código`, links.
- Suporta emojis nativos.
- Limite: 4096 caracteres.

### WhatsApp (Z-API)
- Suporta `*negrito*`, `_itálico_`, `~tachado~`.
- Suporta emojis.
- Limite: 4096 caracteres.

A skill ajusta o template conforme o canal.

## Avisos

- **Cron precisa de timezone definida** no schedule. A skill usa `America/Sao_Paulo` por default.
- **Schedule do Workshop usa `/schedule`** que roda na nuvem do Claude. Não depende do computador do aluno estar ligado.
- **Custo**: cada execução gasta tokens da API do Claude (chama `/trafego-analise`). Para resumo diário típico: ~5K tokens/dia.
- **Se a Graph API falhar** na hora da execução, a mensagem é enviada com aviso "dados indisponíveis no momento" em vez de quebrar.

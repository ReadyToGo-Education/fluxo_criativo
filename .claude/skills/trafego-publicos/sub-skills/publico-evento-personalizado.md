# Sub-fluxo. Público por Evento Personalizado

Cria um **evento personalizado** no pixel (via Custom Conversion) **e**, na sequência, uma **Custom Audience** baseada nesse evento. É a única exceção em que esta skill mexe na configuração do pixel — porque o evento existe especificamente para alimentar a audience que está sendo criada na mesma sessão.

## Perguntas que cobre

- "Crie um evento personalizado: clicou no botão X, e crie um público com isso"
- "Quero um público de quem visitou a página /precos"
- "Público de quem clicou no botão de WhatsApp"
- "Público de quem chegou no checkout pelo link da bio"
- "Crie um público de quem visualizou meu post Y no Instagram via link"

## Inputs

| Input | Default | Descrição |
|---|---|---|
| `pixel_id` | primeiro pixel ativo | Em qual pixel criar o evento |
| `tipo_seletor` | obrigatório | `url`, `url_param`, `url_path`, `dom_click`, `dom_seletor`, `parametro_evento` |
| `valor_seletor` | obrigatório | Conforme tipo: URL, regex, seletor CSS, etc. |
| `nome_evento` | gerado | Nome do custom event (ex: `ClickWhatsApp`) |
| `evento_base` | `PageView` | Evento padrão sobre o qual a regra incide. Padrão `PageView` para URL/path; `Click` para dom_click |
| `janela_dias` | 30 | Janela da audience |
| `nome_audience` | gerado | Sufixo descritivo do nome da audience |

### Tipos de seletor suportados

| Tipo | Como funciona | Exemplo |
|---|---|---|
| `url` | URL exata visitada | `https://meusite.com/precos` |
| `url_path` | Path do URL contém | `/precos` |
| `url_param` | Query string contém | `utm_source=instagram` |
| `dom_click` | Click em elemento (precisa de pixel com auto-tracking de cliques ativado) | `data-button="whatsapp"` |
| `dom_seletor` | CSS selector clicado | `.btn-checkout` |
| `parametro_evento` | Parâmetro custom enviado num evento existente | `content_name=ebook-x` |

## Limitação importante

`dom_click` e `dom_seletor` exigem que a página tenha **auto-tracking de cliques** habilitado no pixel (configurado no Events Manager) **OU** que o aluno coloque `fbq('trackCustom', 'NomeEvento', { ... })` manualmente no botão.

Se o aluno escolhe `dom_click`/`dom_seletor` e o pixel não tem auto-tracking ativo, a skill avisa:

```
⚠️ Para clicks rastreáveis, você precisa de uma das duas:
1. Ativar "Event Setup Tool" no Events Manager (configura cliques sem código)
2. Adicionar fbq('trackCustom', '{NomeEvento}', { ... }) no onclick do botão

Quer que eu crie a Custom Conversion mesmo assim? Ela ficará pronta, mas a audience só vai
popular quando o evento começar a disparar.
```

## Endpoints (sequência de 2 chamadas)

### 1. Criar Custom Conversion
```
POST /act_<id>/customconversions
{
  "name": "{nome_evento}",
  "event_source_id": "<pixel_id>",
  "rule": "{...rule_em_json_string...}",
  "custom_event_type": "OTHER",
  "default_conversion_value": 0.0
}
```

A `rule` segue formato Meta. Exemplos:

**URL path contém:**
```json
{"and": [{"event": {"eq": "PageView"}}, {"url": {"i_contains": "/precos"}}]}
```

**Click em data-attribute:**
```json
{"and": [{"event": {"eq": "Click"}}, {"data-button": {"eq": "whatsapp"}}]}
```

**UTM:**
```json
{"and": [{"event": {"eq": "PageView"}}, {"utm_source": {"eq": "instagram"}}]}
```

### 2. Criar Custom Audience baseada na Custom Conversion
Mesma chamada de `publico-evento-padrao.md`, mas a `rule` aponta para o `custom_event_id` recém-criado:

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
          "value": "{nome_evento}"
        }]
      }
    }]
  }
}
```

## Preview YAML (mostra os 2 passos)

```yaml
sub_fluxo: publico_evento_personalizado

passo_1_evento:
  pixel: "{nome}" ({pixel_id})
  nome_evento: ClickWhatsApp
  tipo_seletor: dom_click
  valor_seletor: 'data-button="whatsapp"'
  rule: { ... }

passo_2_audience:
  nome_final: "[FC] CustomEvent-ClickWhatsApp-30d-curso-tarot"
  janela_dias: 30
  retention_seconds: 2592000
  tamanho_estimado: "calculando" (audience só popula quando o evento começar a disparar)

confirma os 2 passos? (digite SIM)
```

## Após criar

```
✅ Evento personalizado criado: ClickWhatsApp
   Custom Conversion ID: 9876543210

✅ Audience criada: [FC] CustomEvent-ClickWhatsApp-30d-curso-tarot
   Audience ID: 6123456790

A audience começa a popular assim que o evento dispara pela primeira vez no pixel.
Verifique no Events Manager se o evento aparece após o primeiro disparo.

Comando de reversão (manual):
DELETE /9876543210 (apaga o custom conversion)
DELETE /6123456790 (apaga a audience)
```

## Salvar registro local

Em `meus-produtos/{ativo}/trafego/publicos/{audience_id}.md` registrar **os dois IDs**: o do custom conversion + o da audience. Para que `/trafego-pixel` possa cruzar com a listagem de eventos depois.

## Avisos críticos

- **Custom Conversions consomem cota** da conta (limite ~100 por ad account). A skill avisa quando a conta passa de 80% do limite.
- **Audiences geradas por custom event não populam retroativamente.** Só pegam disparos após a criação do evento.
- **Se o evento já existe** no pixel (mesmo nome), a skill **reutiliza** em vez de criar novo. Avisa: "Evento `ClickWhatsApp` já existe no pixel. Vou criar a audience baseada nele."

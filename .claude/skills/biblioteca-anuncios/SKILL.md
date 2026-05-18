---
name: biblioteca-anuncios
description: Investiga criativos escalados na Biblioteca de Anúncios da Meta. Busca concorrentes do nicho do aluno em 1 a 6 mercados (BR, US, MX, AR, CO, ES), identifica criativos com escala (3 ou mais ads usando a mesma peça) via campo collationCount, marca concorrentes que pivotaram de nicho e entrega um HTML self-contained com filtros por mercado, cards por concorrente, resumo estratégico e padrões. Dois métodos de execução. Apify (rápido, requer APIFY_API_TOKEN, custo baixo) ou Claude in Chrome (gratuito, exige aprovação manual dos pop-ups).
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill
model: sonnet
---

# Biblioteca de Anúncios. Investigar Criativos Escalados

Investiga a Biblioteca de Anúncios da Meta e identifica quais criativos os concorrentes estão **escalando** (usando em 3+ anúncios simultâneos, detectado via campo `collationCount` da Meta). Entrega um HTML interativo com cards por concorrente, filtro por mercado e resumo estratégico.

Dois métodos de execução disponíveis:
- **Apify** (recomendado). Roda em background via API, 2 a 5 minutos, zero cliques de permissão, custa $0.10 a $3.00 conforme o modo.
- **Claude in Chrome** (fallback gratuito). Roda no navegador, 5 a 25 minutos, exige aprovar pop-ups manualmente.

---

## ⚠ Antes de começar. Ambiente de execução

A skill funciona em 2 ambientes (CLI ou Desktop), mas com capacidades diferentes:

| Ambiente | Apify | Claude in Chrome |
|---|---|---|
| **Claude Code no terminal (CLI)** | ✅ se tiver `APIFY_API_TOKEN` no `.env` | ❌ Não disponível |
| **Claude Desktop (claude.ai pelo navegador)** | ✅ se tiver `APIFY_API_TOKEN` no `.env` | ✅ se a extensão Claude in Chrome estiver conectada |

**Por que o Claude in Chrome não funciona pelo terminal?**

A extensão Claude in Chrome é um produto **Desktop-only**. Ela vive como uma extensão do navegador Chrome e se comunica apenas com sessões da claude.ai abertas no navegador. Quando o aluno está rodando esta skill pelo Claude Code no terminal/CLI, **mesmo tendo a extensão instalada no Chrome, ela NÃO se comunica com a sessão CLI** (são processos isolados).

A skill detecta isso em runtime checando se as tools `mcp__Claude_in_Chrome__*` estão presentes (ver Passo 0.4):
- Presentes → ambiente Desktop, oferece a opção Claude in Chrome no menu do Passo 1.5.
- Ausentes → ambiente CLI ou Desktop sem extensão, **não oferece** a opção Chrome e explica o motivo ao aluno. Se o aluno só tinha o Chrome em mente e não quer configurar Apify, encerra orientando a abrir o Claude Desktop.

Para usar a opção Apify (recomendada e disponível em qualquer ambiente), basta ter `APIFY_API_TOKEN` no `.env`. A skill `/configurar-apify` configura isso.

---

## REGRA DURA. Uma pergunta por turno

Cada pergunta é UM turno separado. Exiba, pare, aguarde, salve, mostre micro-resumo, só então a próxima. PROIBIDO bulkar.

---

## Passo 0. Contexto, retomada e detecção do método

### 0.1. Contexto

Leia em paralelo:
- `meus-produtos/.ativo`
- `meus-produtos/{ativo}/perfil.md` (se existir)

Se não houver produto ativo, instrua o aluno a rodar `/produto-novo` primeiro e encerre.

Do `perfil.md`, tente extrair como sugestão:
- **Nicho**. Procure por "Nicho:", "Mercado:" ou identidade do produto.

### 0.2. Detecção de retomada

Verifique se existe `meus-produtos/{ativo}/entregas/biblioteca-anuncios/.biblioteca-queue.json`. Se existir, leia e identifique o tipo de estado:

### Caso A. Estado = `aguardando_configuracao_apify`

O aluno foi pra `/configurar-apify` antes de completar a coleta. Recarregue `tem_token_apify` (Passo 0.3) e:

**Se agora `tem_token_apify == true`** (configurou com sucesso):

```
Você configurou o Apify. Retomando a investigação de onde paramos.

Modo escolhido antes: {modo}
Método: Apify (token agora configurado)

1. Continuar daqui (vou direto pra pergunta de Nicho)
2. Recomeçar do zero (descarta o que você já escolheu)
3. Cancelar

Digite o número.
```

- Opção 1: salve `modo` da fila, salve `metodo = APIFY`, pule os Passos 1 e 1.5, vá direto pro Passo 2 (Nicho).
- Opção 2: delete o arquivo e siga fluxo normal desde o Passo 1.
- Opção 3: encerre (mantém o arquivo de fila para retomada futura).

**Se `tem_token_apify == false`** (aluno não completou a configuração):

```
A configuração do Apify ainda não foi concluída. Quero:

1. Voltar pra /configurar-apify e completar
2. Trocar pra Claude in Chrome (sem precisar do token)
3. Cancelar

Digite o número.
```

- Opção 1: invoque `workshop-marketing:configurar-apify` de novo e encerre.
- Opção 2: atualize o arquivo de fila com `metodo = CHROME` e vá direto pro Passo 2 (Nicho).
- Opção 3: encerre.

### Caso B. Estado = `em_execucao` (fluxo normal de retomada)

```
Encontrei uma investigação interrompida da sessão anterior.

Nicho: {nicho}
Modo: {modo}
Método: {metodo}
Concluídos: {lista_legivel}
Pendentes: {lista_legivel}

1. Continuar de onde parou
2. Começar do zero (descarta a fila)
3. Cancelar

Digite o número.
```

- Opção 1: pule a coleta e vá direto para o Passo 7 reaproveitando as variáveis salvas.
- Opção 2: delete o arquivo e siga fluxo normal.
- Opção 3: encerre.

### 0.3. Detecção do APIFY_API_TOKEN

Leia o `.env` da raiz do projeto. Procure por `APIFY_API_TOKEN=...`.

- **Se existir e parece um token válido** (começa com `apify_api_`): salve `tem_token_apify = true`.
- **Se não existir ou está vazio**: salve `tem_token_apify = false`.

Isso será usado no Passo 1.5 para sugerir o método correto.

### 0.4. Detecção do Claude in Chrome (Desktop-only)

Verifique se as tools `mcp__Claude_in_Chrome__navigate` e `mcp__Claude_in_Chrome__get_page_text` estão disponíveis na sessão atual.

- **Se presentes**: salve `tem_chrome_mcp = true`. Ambiente é Claude Desktop com a extensão conectada. O método Claude in Chrome pode ser oferecido no Passo 1.5.
- **Se ausentes**: salve `tem_chrome_mcp = false`. Ambiente é Claude Code no terminal (CLI) OU Claude Desktop sem a extensão. O método Claude in Chrome **NÃO** pode ser oferecido no Passo 1.5, e a skill explica o motivo ao aluno.

A combinação `tem_token_apify` + `tem_chrome_mcp` controla o menu do Passo 1.5. Se ambos forem `false`, o Passo 1.5 redireciona pra `/configurar-apify` antes de prosseguir, porque sem nenhum dos dois caminhos a investigação não pode rodar.

---

## Anúncio inicial

```
🔍 Próximo passo: configurar a investigação da Biblioteca de Anúncios (6 perguntas + 1 confirmação). Tempo estimado: 1 a 2 minutos para coletar, depois 2 a 25 minutos para investigar conforme método e modo escolhidos.
```

---

## Passo 1. Modo de investigação

Exiba SOMENTE este bloco e pare:

```
Pergunta 1 de 6. Modo de investigação

Quanto fundo você quer ir?

1. Rápido. 3 a 5 concorrentes do seu mercado principal.
2. Padrão. 8 a 10 concorrentes em 2 a 3 mercados.
3. Completo. 14 concorrentes em até 6 mercados (BR, US, MX, AR, CO, ES).
4. Cancelar.

Digite o número.
```

AGUARDE. Se `4`, encerre. Salve como `modo` (`RAPIDO`, `PADRAO`, `COMPLETO`).

Micro-resumo:

```
--- Pergunta 1/6 concluída ---
Modo: {modo}
Próximo: Método de execução
---
```

---

## Passo 1.5. Método de execução

Apresente as opções com tempos e custos do modo escolhido. O menu varia conforme `tem_token_apify` e `tem_chrome_mcp` (definidos nos Passos 0.3 e 0.4).

Tempos e custos por modo:

Para **Rápido** (3 buscas, ~50-100 ads cada):
- Apify: ~2 minutos. Custo aproximado: $0.05 a $0.15.
- Claude in Chrome: ~5 minutos. ~6 cliques de permissão.

Para **Padrão** (8 a 16 buscas):
- Apify: ~5 minutos. Custo aproximado: $0.25 a $0.80.
- Claude in Chrome: ~12 minutos. ~16 cliques.

Para **Completo** (até 84 buscas):
- Apify: ~12 minutos. Custo aproximado: $1.50 a $4.00.
- Claude in Chrome: ~25 minutos. ~28 cliques.

### Matriz de menus

Existem 4 combinações possíveis, e cada uma exibe um menu diferente. Use a tabela:

| `tem_token_apify` | `tem_chrome_mcp` | Comportamento |
|---|---|---|
| true | true | Menu A. Oferece Apify e Chrome lado a lado |
| true | false | Menu B. Oferece só Apify, explica que Chrome é Desktop-only |
| false | true | Menu C. Oferece Chrome direto e Apify com encaminhamento pra /configurar-apify |
| false | false | Menu D. Nenhum caminho disponível, encaminha pra /configurar-apify ou orienta abrir Desktop |

### Menu A. `tem_token_apify = true`, `tem_chrome_mcp = true`

```
Pergunta 2 de 6. Método de execução

Como você quer rodar a investigação?

1. Apify (token já configurado no seu .env). {tempo_apify}. Custo aproximado: {custo_apify}. Zero cliques de permissão.
2. Claude in Chrome (extensão conectada). {tempo_chrome}. Gratuito. Exige aprovar ~{cliques} pop-ups durante a execução.
3. Cancelar.

Digite o número.
```

### Menu B. `tem_token_apify = true`, `tem_chrome_mcp = false`

```
Pergunta 2 de 6. Método de execução

Como você quer rodar a investigação?

1. Apify (token já configurado no seu .env). {tempo_apify}. Custo aproximado: {custo_apify}. Zero cliques de permissão.
2. Cancelar.

Digite o número.

Nota: Claude in Chrome não está disponível porque você está rodando esta skill pelo Claude Code no terminal (CLI). A extensão Claude in Chrome é Desktop-only e se comunica apenas com sessões da claude.ai abertas no navegador. Se quiser usar a opção Chrome, abra o Claude Desktop, invoque /biblioteca-anuncios lá, e tenha a extensão conectada. Para esta sessão atual, Apify é o caminho disponível.
```

### Menu C. `tem_token_apify = false`, `tem_chrome_mcp = true`

```
Pergunta 2 de 6. Método de execução

Como você quer rodar a investigação?

1. Apify (requer configurar APIFY_API_TOKEN. Leva ~2 minutos. Eu te direciono pra /configurar-apify e depois retomamos esta investigação automaticamente). {tempo_apify} de execução. Custo: {custo_apify}.
2. Claude in Chrome (extensão conectada, pronto pra rodar agora sem configuração). {tempo_chrome}. Gratuito. Exige aprovar ~{cliques} pop-ups.
3. Cancelar.

Digite o número.
```

### Menu D. `tem_token_apify = false`, `tem_chrome_mcp = false`

Nenhum caminho disponível para esta sessão. Exiba:

```
Pergunta 2 de 6. Método de execução

Você não tem nenhum dos 2 métodos prontos para rodar agora:

- Apify: APIFY_API_TOKEN não configurado no .env.
- Claude in Chrome: indisponível porque você está no terminal (CLI). A extensão é Desktop-only.

Como você quer prosseguir?

1. Configurar Apify agora (~2 minutos). Eu te direciono pra /configurar-apify e retomamos esta investigação automaticamente. Funciona em qualquer ambiente.
2. Abrir o Claude Desktop em outro momento, conectar a extensão Claude in Chrome lá, e invocar /biblioteca-anuncios. (Encerra esta execução agora.)
3. Cancelar.

Digite o número.
```

Se aluno escolher `1`: salve o estado em `.biblioteca-queue.json` com `metodo_pendente = APIFY` e invoque `workshop-marketing:configurar-apify`. Se escolher `2` ou `3`: encerre.

AGUARDE A RESPOSTA.

### Tratamento das respostas por menu

**Menu A (`tem_token_apify=true`, `tem_chrome_mcp=true`):**
- `1` → salve `metodo = APIFY`. Siga normalmente.
- `2` → salve `metodo = CHROME`. Siga normalmente.
- `3` → encerre.

**Menu B (`tem_token_apify=true`, `tem_chrome_mcp=false`):**
- `1` → salve `metodo = APIFY`. Siga normalmente.
- `2` → encerre.

Se o aluno digitar `3` ou tentar escolher Chrome neste menu, reforce: "A opção Claude in Chrome não está disponível nesta sessão (você está no terminal/CLI). Use Apify (1) ou cancele (2)."

**Menu C (`tem_token_apify=false`, `tem_chrome_mcp=true`):**
- `1` → fluxo de configuração do Apify (veja "Fluxo de configuração do Apify" abaixo).
- `2` → salve `metodo = CHROME`. Siga normalmente.
- `3` → encerre.

**Menu D (`tem_token_apify=false`, `tem_chrome_mcp=false`):**
- `1` → fluxo de configuração do Apify (veja "Fluxo de configuração do Apify" abaixo).
- `2` → encerre (aluno vai abrir Desktop em outro momento).
- `3` → encerre.

### Fluxo de configuração do Apify

Antes de delegar para `/configurar-apify`, **salve o estado atual** em `meus-produtos/{ativo}/entregas/biblioteca-anuncios/.biblioteca-queue.json` para que a retomada (Passo 0.2) traga o aluno de volta sem precisar repetir o que já escolheu:

```json
{
  "criado_em": "{ISO}",
  "estado": "aguardando_configuracao_apify",
  "modo": "{modo escolhido no Passo 1}",
  "metodo_pendente": "APIFY",
  "nicho": null,
  "concorrentes": [],
  "mercados": [],
  "criterio_escala": null,
  "resultados": []
}
```

Em seguida, exiba ao aluno:

```
Salvei o estado da sua investigação. Vou abrir agora a configuração do Apify (~2 minutos).

Quando terminar, rode /biblioteca-anuncios de novo. Eu vou detectar o estado salvo e seguir com Apify configurado, sem você precisar repetir a escolha de modo.
```

Invoque a skill `workshop-marketing:configurar-apify` via `Skill` tool e encerre esta execução.

Micro-resumo:

```
--- Pergunta 2/6 concluída ---
Método: {metodo}
{Se APIFY} Custo estimado: {custo}
Próximo: Nicho
---
```

---

## Passo 2. Nicho

### Com sugestão do perfil

```
Pergunta 3 de 6. Nicho

Sugestão a partir do seu perfil: {nicho_sugerido}

1. Sim, usar este nicho
2. Investigar um nicho diferente (eu digito)

Digite o número.
```

Se `2`:

```
Digite o nicho que você quer investigar.

(ex: marketing digital e infoprodutos, fitness e emagrecimento, espiritualidade, finanças pessoais)

Quanto mais específico, melhor.
```

### Sem sugestão

```
Pergunta 3 de 6. Nicho

Qual nicho você quer investigar na Biblioteca de Anúncios?

(ex: marketing digital, fitness, espiritualidade, finanças, beleza, idiomas, alimentação)

Digite o nicho.
```

AGUARDE. Salve como `nicho`. Micro-resumo.

Em seguida, leia `references/concorrentes-por-nicho.md` e tente bater o nicho com uma das seções existentes. Se achou, salve `concorrentes_sugeridos` (lista por mercado, com marcadores). Senão, `concorrentes_sugeridos = NENHUM`.

---

## Passo 3. Concorrentes

### Se `concorrentes_sugeridos != NENHUM`

**Primeiro mostre a lista filtrada por mercado conforme o modo escolhido no Passo 1, sem marcadores internos (`*`, `(PIVOT)`, `(baixa escala)` só ficam pra uso interno da skill). O aluno precisa ver os nomes antes de decidir como quer usar.**

Formato de exibição:

```
Pergunta 4 de 6. Concorrentes a investigar

Encontrei {N} concorrentes conhecidos no nicho "{nicho}":

**Brasil:**
- {nome 1}
- {nome 2}
- {nome 3}
- {nome 4}

**Estados Unidos:**
- {nome 5}
- {nome 6}
- {nome 7}

**Hispano (se modo Padrão ou Completo):**
- {nome 8}
- {nome 9}

Como você quer prosseguir?

1. Usar essa lista
2. Usar essa lista + adicionar mais nomes
3. Só os concorrentes que eu digitar agora (ignorar a lista)
4. Misturar com descoberta automática via WebSearch

Digite o número.
```

AGUARDE.

**Se 1**: use a lista exibida. Salve em `concorrentes` e siga.

**Se 2**: peça os nomes adicionais:

```
Digite os nomes adicionais que você quer somar à lista, separados por vírgula.

(ex: Maria Souza, João Silva)

Vou somar com a lista que mostrei acima. Total final entre 3 e 14 nomes.
```

Some os nomes digitados à lista da skill. Salve em `concorrentes` e siga.

**Se 3**: peça os nomes:

```
Digite os nomes dos concorrentes que você quer investigar, separados por vírgula.

(ex: Erico Rocha, Pedro Sobral, Felipe Azevedo)

Mínimo de 3 nomes. Máximo de 14.
```

**Se 4**: vá para sub-rotina de descoberta via WebSearch.

### Se `concorrentes_sugeridos == NENHUM`

```
Pergunta 4 de 6. Concorrentes a investigar

Não tenho lista pronta para "{nicho}". Você tem duas opções:

1. Digito os nomes que conheço (mínimo 3, máximo 14)
2. Descobrir via WebSearch
3. Cancelar

Digite o número.
```

Siga o sub-fluxo. Salve como `concorrentes` (lista final, com mercado de cada um marcado).

Micro-resumo.

---

## Passo 4. Mercados de cobertura

```
Pergunta 5 de 6. Mercados

Quais mercados você quer cobrir?

{Se modo == RAPIDO}
1. Só Brasil (recomendado)
2. Brasil + Estados Unidos
3. Customizar

{Se modo == PADRAO}
1. Brasil + Estados Unidos + 1 hispano (recomendado)
2. Brasil + Estados Unidos
3. Só Brasil
4. Customizar

{Se modo == COMPLETO}
1. Todos os 6 (BR, US, MX, AR, CO, ES) (recomendado)
2. Só BR + US
3. Customizar

Digite o número.
```

Se `Customizar`, pergunte quais países (lista BR / US / MX / AR / CO / ES). AGUARDE. Salve `mercados`. Micro-resumo.

---

## Passo 5. Critério de escala

```
Pergunta 6 de 6. Critério de escala

Qual o número mínimo de anúncios para um criativo ser considerado escalado?

1. 3 anúncios (default, captura mais)
2. 5 anúncios (filtra mais, só os mais usados)
3. 10 anúncios (só os super escalados)

Digite o número.
```

AGUARDE. Salve como `criterio_escala`. Micro-resumo.

---

## Passo 6. Confirmação consolidada

Exiba o resumo:

```
Resumo do que vou investigar:

Nicho: {nicho}
Modo: {modo}
Método: {metodo}
Concorrentes: {N} nomes ({distribuicao por mercado})
Mercados: {lista}
Critério de escala: {criterio_escala} ou mais anúncios

Estimativa de tempo: {tempo conforme método e modo}
{Se metodo == APIFY} Custo estimado: {custo}
{Se metodo == CHROME} Cliques de permissão: ~{cliques}

Vou gerar:
- HTML interativo com tema claro, filtro por mercado, cards por concorrente, resumo estratégico
- Salvo em meus-produtos/{ativo}/entregas/biblioteca-anuncios/criativos-escalados-{data}.html

1. Confirmar e começar
2. Ajustar algo (diga o campo)
3. Cancelar

Digite o número.
```

AGUARDE. Se 1, vá para o Passo 7. Se 2, refaça o campo. Se 3, encerre.

---

## Passo 7. Execução da investigação

### 7.0. Detectar comando Python

Antes de qualquer execução, rode `python3 --version 2>&1 || py -3 --version 2>&1` para determinar o comando Python. Guarde como `{python}`. Use em todas as chamadas de script.

### 7.1. Salvar fila de retomada

Crie `meus-produtos/{ativo}/entregas/biblioteca-anuncios/.biblioteca-queue.json`:

```json
{
  "criado_em": "{ISO}",
  "modo": "{modo}",
  "metodo": "{metodo}",
  "nicho": "{nicho}",
  "criterio_escala": {criterio_escala},
  "mercados": [...],
  "concorrentes": [
    {"nome": "Erico Rocha", "mercado": "BR", "status": "pendente"},
    {"nome": "Alex Hormozi", "mercado": "US", "status": "pendente"}
  ],
  "resultados": []
}
```

### 7.2. Fluxo Apify (se `metodo == APIFY`)

Para cada concorrente da fila:

Anuncie:

```
⏳ Concorrente {N}/{total}: investigando {nome} no mercado {mercado} via Apify...
```

Execute via `Bash`:

```bash
{python} .claude/skills/biblioteca-anuncios/scripts/buscar-apify.py \
  --concorrente "{nome}" \
  --pais {mercado} \
  --criterio-escala {criterio_escala} \
  --count {count_conforme_modo} \
  --actor curious_coder
```

Onde `count_conforme_modo`:
- Rápido: `50`
- Padrão: `100`
- Completo: `200`

O script retorna JSON em stdout no formato:

```json
{
  "concorrente": "...",
  "pais": "...",
  "total_ads_coletados": 87,
  "criativos_escalados": [
    {
      "collationCount": 12,
      "adArchiveID": "...",
      "pageName": "...",
      "hook": "...",
      "title": "...",
      "cta": "...",
      "startDate": "...",
      "link_anuncio": "https://www.facebook.com/ads/library/?id=..."
    }
  ],
  "erro": null
}
```

Processe:
- Se `erro != null`: registre no JSON da fila como `erro: "..."` e siga pro próximo.
- Se `criativos_escalados == []` e `total_ads_coletados > 0`: registre como `sem_escala` no JSON. Motivo: "alta rotação sem repetição vertical".
- Se `total_ads_coletados == 0`: registre como `sem_ads_ativos`.
- Caso contrário: salve a lista de criativos no JSON da fila.

Atualize o JSON da fila movendo o concorrente de `pendente` para `concluido` após cada execução.

### 7.3. Fluxo Claude in Chrome (se `metodo == CHROME`)

Antes de começar, exiba o aviso:

```
⚠ Aviso importante sobre Claude in Chrome

Vou abrir o Claude in Chrome e navegar pela Biblioteca de Anúncios da Meta. A cada concorrente, o Chrome pede permissão DUAS vezes (navigate + get_page_text). Hoje o pop-up NÃO tem opção "Permitir sempre".

Você vai aprovar ~{cliques} pop-ups. Pode aprovar tudo de uma rajada quando começar.

1. Sim, vou aprovar
2. Cancelar (mudo de ideia)

Digite o número.
```

Se cancelar, encerre.

Para cada concorrente:

Anuncie:

```
⏳ Concorrente {N}/{total}: investigando {nome} no mercado {mercado} via Claude in Chrome...
```

Execute:

1. Monte a URL da Biblioteca:
   ```
   https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={CODIGO}&q={NOME_URL_ENCODED}&search_type=keyword_unordered&media_type=all&sort_data[mode]=total_impressions&sort_data[direction]=desc
   ```
2. Chame `mcp__Claude_in_Chrome__navigate` com essa URL.
3. Aguarde 5 segundos.
4. Chame `mcp__Claude_in_Chrome__get_page_text`.
5. Aplique regex `(\d+)\s+ads?\s+use\s+this\s+creative` no texto.
6. Filtre matches com X >= `criterio_escala`.
7. Para cada match, extraia escala, Library ID, hook (texto antes do match).
8. Atualize o JSON da fila.

#### Tratamento de erros (Chrome)

- **"permission_required: www.facebook.com"**: aguarde 2 segundos e retente o tool.
- **"Tool permission stream closed"**: avise o aluno "preciso que você aprove os pop-ups mais rápido" e retente.
- **"page body text exceeds max_chars"**: registre `volume_excedeu_extracao` e siga.
- **Sem indicador de escala**: aguarde 5s e refaça. Se persistir, registre `sem_dados_escala`.
- **Sem ads ativos no país**: se hispano, tente os outros 3 países hispanos. Se BR/US, marca direto.

### 7.4. Identificação de pivot de nicho (ambos métodos)

Após extrair os criativos de um concorrente, aplique o teste do nicho:

> O criativo mais escalado deste concorrente ensina alguma habilidade do nicho `{nicho}`?

Se "não, é mais sobre {outro_assunto}", marque o concorrente como `pivot: true` + `novo_nicho: {outro_assunto}` no JSON.

---

## Passo 8. Geração do HTML

Após processar todos os concorrentes:

```
⏳ Passo final: gerando o HTML interativo com {N} concorrentes e {N_criativos} criativos escalados...
```

A geração do HTML é feita pelo script permanente `scripts/montar-html.py`. **Não monte o HTML inline.** A estrutura visual está em `references/template-html.md` (fonte de verdade do design) e o script implementa essa estrutura.

### 8.1. Preparar o config JSON

Monte um arquivo de configuração em `meus-produtos/{ativo}/entregas/biblioteca-anuncios/tmp/relatorio-config.json` no formato:

```json
{
  "produto_slug": "{slug do produto ativo}",
  "nicho": "{nicho coletado no Passo 2}",
  "modo": "{RAPIDO|PADRAO|COMPLETO}",
  "metodo": "{APIFY|CHROME}",
  "criterio_escala": 3,
  "mercados_legivel": "Brasil, Estados Unidos, Hispano (MX)",
  "data_relatorio": "{YYYY-MM-DD calculado via Bash com date}",
  "saida_html": "meus-produtos/{ativo}/entregas/biblioteca-anuncios/criativos-escalados-{YYYY-MM-DD}.html",
  "concorrentes": [
    {
      "slug": "alex-hormozi",
      "nome": "Alex Hormozi",
      "regiao": "en",
      "foco": "Acquisition e escala de negocios",
      "resultado_json": "meus-produtos/{ativo}/entregas/biblioteca-anuncios/tmp/alex-hormozi.json"
    }
  ],
  "analises": {
    "padroes_comuns": ["bullet 1 escrito pelo Claude com nuance do nicho", "bullet 2", "..."],
    "diferencas_mercados": ["BR vs US: {bullet}", "EN vs ES: {bullet}", "..."],
    "padroes_por_concorrente": {
      "alex-hormozi": "Texto custom do bloco 'Padrao Identificado' deste concorrente.",
      "tiago-tessmann": "..."
    }
  }
}
```

**Campos da seção `analises`** são **opcionais**. Se forem omitidos, o script gera versões data-driven automáticas (genéricas, sem nuance). Para um relatório de qualidade, **a skill deve preencher os 3 campos de `analises`** lendo os criativos escalados e escrevendo:

- **`padroes_comuns`**: 4 a 5 bullets sobre padrões reais que aparecem entre os concorrentes que escalam (hook, formato, CTA, evergreen vs picos, etc).
- **`diferencas_mercados`**: 3 a 5 bullets comparando BR vs US vs ES com dados específicos (volumes, escalas máximas, formatos predominantes).
- **`padroes_por_concorrente`**: dict com slug → texto. Pra cada concorrente que TEM criativos escalados, escreva uma frase curta apontando o padrão específico daquele concorrente (não é texto genérico, é observação do que o concorrente repete).

**Cada `resultado_json` aponta para o arquivo gerado pelo `buscar-apify.py`** (ou pelo fluxo Chrome) no Passo 7. Garanta que esses arquivos existam antes de chamar o script.

### 8.2. Executar o script

```bash
{python} .claude/skills/biblioteca-anuncios/scripts/montar-html.py --config meus-produtos/{ativo}/entregas/biblioteca-anuncios/tmp/relatorio-config.json
```

O script imprime um JSON único linha com `{"ok": true, "saida_html": "...", "tamanho_bytes": N}`. Leia esse JSON para confirmar sucesso.

### 8.3. Limpeza

Após o script salvar o HTML com sucesso:

1. **Delete a pasta `tmp/`** inteira (`tmp/relatorio-config.json` + `tmp/{slug}.json` dos concorrentes).
2. **Delete `.biblioteca-queue.json`**.

---

## Passo 9. Entrega

```
✅ Investigação concluída.

Método usado: {metodo}
{Se metodo == APIFY} Custo real consumido: ~${custo_real} (estimado, confira no painel Apify)
Concorrentes investigados: {N}
Criativos escalados encontrados: {N_criativos}
Maior escala individual: {max_escala} ads ({nome_competidor})
Concorrentes que pivotaram de nicho: {N_pivot}
Concorrentes sem escala (alta rotação): {N_sem_escala}

Arquivo HTML salvo em:
{caminho_absoluto}

Top 3 criativos escalados:
1. {nome1} ({mercado1}): {escala1} ads. Hook: "{hook1}"
2. {nome2} ({mercado2}): {escala2} ads. Hook: "{hook2}"
3. {nome3} ({mercado3}): {escala3} ads. Hook: "{hook3}"

Padrão estratégico mais comum: {padrao_curto}
Maior diferença entre mercados: {diferenca_curta}

Abra o HTML no navegador para ver o relatório completo com filtros por mercado, links pra cada anúncio na Biblioteca, e resumo estratégico.
```

Exiba o caminho absoluto em formato copiável.

---

## Regras

- **Aprovação obrigatória** no Passo 6 (confirmação consolidada) antes de executar.
- **Aviso de Claude in Chrome** obrigatório no Passo 7.3 (se método CHROME).
- **Cache de retomada** via `.biblioteca-queue.json` em ambos os métodos.
- **Anúncios Nível 2** em cada concorrente.
- **"Cancelar" disponível** em toda aprovação.
- **Sem travessão, sem exclamação** em todo texto gerado.
- **Português brasileiro com acentuação correta** em todo texto exibido ao aluno.
- **Token Apify nunca exibido no chat**, conforme regra global do CLAUDE.md.
- **Detectar python3 vs py -3** antes de chamar scripts.

---

## Quando NÃO usar esta skill

- O aluno quer **criar anúncios** próprios. Use `/copy-anuncio`.
- O aluno quer **analisar campanhas próprias**. Use `/trafego-analise`.
- O aluno não tem nem APIFY_API_TOKEN nem Claude in Chrome.
- O aluno ainda não cadastrou produto. Use `/produto-novo`.

---

## Estrutura de pastas criada pela skill

```
meus-produtos/{ativo}/entregas/biblioteca-anuncios/
├── .biblioteca-queue.json (só existe durante investigação em andamento)
└── criativos-escalados-{YYYY-MM-DD}.html
```

A skill pode ser rodada várias vezes; cada execução gera um HTML novo com a data do dia.

---

## Arquivos internos da skill

```
.claude/skills/biblioteca-anuncios/
├── SKILL.md
├── references/
│   ├── apify-actor.md (detalhes técnicos do actor Apify)
│   ├── concorrentes-por-nicho.md (listas por nicho com marcadores)
│   └── template-html.md (paleta + estrutura HTML, fonte de verdade do design)
└── scripts/
    ├── buscar-apify.py (chamada API Apify por concorrente)
    └── montar-html.py (consolida JSONs dos concorrentes e gera o HTML final)
```

### Sobre `montar-html.py`

Script permanente que recebe um único arquivo de configuração JSON (`--config`) e produz o HTML final. Implementa a estrutura visual documentada em `references/template-html.md`. Não monte HTML inline na skill, sempre passe pelo script. Análises customizadas (padrões, diferenças entre mercados, padrão por concorrente) vão no campo `analises` do config JSON. Se omitidas, o script gera versões data-driven simples.

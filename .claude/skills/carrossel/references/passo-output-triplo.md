# Passo de Output Triplo (compartilhado)

> Passo 4 do fluxo de geração da skill `/carrossel`. Roda depois que os 6 slides de texto foram aprovados pelo aluno no Passo 3.
> Lógica: mostra prompts no chat → detecta MCP do Claude in Chrome e API de imagem → oferece caminhos (manual, Chrome ou API). **Não grava `prompts.txt` em disco** (os prompts já estão visíveis no chat para o aluno copiar).

---

## 3.1. Output no chat (slide por slide)

Mostre os 6 prompts de imagem individualmente no chat, um por slide, na ordem Slide 1 → Slide 6. Cada prompt completo, em inglês, pronto para colar no ChatGPT. Use o `template-prompt-imagem.md` substituindo todos os campos `[...]` pelos valores reais do slide.

Formato de exibição:

```
PROMPT DO SLIDE 1
{prompt completo em ingles}

---

PROMPT DO SLIDE 2
{prompt completo em ingles}

---

(... até o slide 6 ...)
```

Os prompts ficam disponíveis para o aluno copiar direto do chat. Não é necessário gravar arquivo extra.

---

## 3.3. Detectar capacidades da sessão atual

Antes de oferecer os caminhos, **detecte duas coisas** sobre a sessão e o ambiente do aluno:

### 3.3.A. MCP do Claude in Chrome disponível

Verifique se as tools `mcp__Claude_in_Chrome__*` estão presentes na sessão. Tools esperadas:

- `mcp__Claude_in_Chrome__navigate`
- `mcp__Claude_in_Chrome__send_message` (ou equivalente para enviar texto na conversa do ChatGPT)
- `mcp__Claude_in_Chrome__get_page_text`
- `mcp__Claude_in_Chrome__wait_for_element` (se existir)

Se disponíveis: `tem_chrome_mcp = true`. Senão: `tem_chrome_mcp = false`.

**REGRA IMPORTANTE — Claude in Chrome é Desktop-only.** A extensão Claude in Chrome só roda no aplicativo Desktop do Claude (claude.ai pelo navegador, ou Claude Desktop). **Se o aluno está rodando o `/carrossel` pelo Claude Code no terminal (CLI), o MCP do Claude in Chrome NÃO está disponível, mesmo que ele tenha a extensão instalada no navegador.** A skill detecta isso pela ausência das tools `mcp__Claude_in_Chrome__*`, e nesse caso a opção "Automatizado via Chrome" simplesmente não aparece no menu (a skill explica o motivo).

### 3.3.B. API de imagem configurada

Leia o `.env` da raiz do projeto e procure por:
- `OPENROUTER_API_KEY=` (preferencial — usado por `banner-visual` e `carrossel-visual`)
- `OPENAI_API_KEY=` (alternativa, caso o aluno não tenha OpenRouter)

Se algum dos dois existir e parece um token válido: `tem_api_imagem = true` + `provider_api = "openrouter" | "openai"`. Senão: `tem_api_imagem = false`.

---

## 3.4. Oferecer caminhos de geração de imagem

### REGRA DURA. Menu SEMPRE exibido, jamais pulado

**O menu de caminhos é OBRIGATÓRIO. Mesmo que só tenha 1 opção disponível, a skill DEVE exibir o bloco numerado e perguntar "Digite o número". PROIBIDO pular direto para o Passo 5 (legenda) sem o aluno ter escolhido um caminho.**

Comportamento errado (NÃO faça):
```
Os 6 prompts estão prontos. Copie e cole no ChatGPT.
Agora vou gerar a legenda.   ← BUG: pulou o menu
```

Comportamento certo (FAÇA):
```
Os 6 prompts estão prontos.

Pronto. Pra gerar as 6 imagens você tem os seguintes caminhos:

1. Manual no ChatGPT...
{Se tem_chrome_mcp == true} 2a/2b. Claude in Chrome... {fim}
3. {API ou indisponível}

Digite o número.
```

Aguarde a resposta antes de seguir para o Passo 5.

### Montagem do menu conforme capacidades

Monte o menu conforme a combinação de capacidades detectadas. **REGRA DE NUMERAÇÃO DINÂMICA SEM BURACOS:** os números visíveis ao aluno SEMPRE começam em 1 e seguem em sequência (1, 2, 3...) sem pular nenhum. Mantenha um mapa interno `{numero_visivel → caminho_logico}` para interpretar a resposta do aluno e disparar a ação correta. Os exemplos abaixo usam rótulos fixos (1, 2a, 2b, 3) apenas para clareza da spec — em runtime, renumere conforme o que está disponível.

**Regra geral: o caminho API paralela OpenRouter SEMPRE aparece no menu, mesmo quando `tem_api_imagem == false`.** Quando indisponível, exiba o item com aviso explicando que precisa configurar `OPENROUTER_API_KEY` antes. Caminhos Chrome só aparecem quando `tem_chrome_mcp == true`.

**Sobre o Chrome MCP no Desktop (importante)**: o Claude Desktop NÃO ativa o MCP Claude in Chrome automaticamente. Mesmo no Desktop, o aluno precisa:
1. Ter a extensão Claude in Chrome instalada no navegador Chrome.
2. Ter ela conectada/autenticada com a conta dele.
3. Ter o Chrome aberto durante a execução.

Se essas 3 condições não estão satisfeitas, `tem_chrome_mcp = false` mesmo no Desktop. Nesse caso a skill exibe a observação adicional no menu:

```
Se você está no Claude Desktop e queria a opção Chrome mas ela não apareceu, verifique:
- A extensão Claude in Chrome está instalada no Chrome?
- Ela está conectada/autenticada com sua conta?
- O Chrome está aberto agora?
```

### Caso comum no terminal (CLI) sem MCP Chrome

`tem_chrome_mcp == false`. **Renumeração dinâmica: o caminho API vira opção 2 (não 3), porque os caminhos Chrome estão ausentes.**

```
Pronto. Pra gerar as 6 imagens você tem os seguintes caminhos:

1. Manual no ChatGPT. Eu te dou os prompts pra colar um a um na conversa do ChatGPT (ou em qualquer ferramenta de imagem por IA). Gratuito e sem configuração.

{Se tem_api_imagem == true}
2. Automatizado via API ({provider_api}, gera as 6 em paralelo). Tempo: cerca de 60 segundos. Custo aproximado: $0.05 a $0.20 (depende do modelo). Eu disparo 6 chamadas paralelas e salvo as imagens direto na pasta do carrossel.
{senão tem_api_imagem == false}
2. Automatizado via API (OpenRouter, gera as 6 em paralelo). Tempo: cerca de 60 segundos. Custo aproximado: $0.05 a $0.20. Indisponível agora, precisa configurar a OPENROUTER_API_KEY no .env. Rode /configurar-imagens antes de escolher essa opção.
{fim}

Aviso: a opção "Automatizado via Claude in Chrome" não aparece nesta sessão porque o Claude in Chrome só está disponível na versão Desktop do Claude (claude.ai pelo navegador). Se você está rodando o /carrossel pelo terminal, a extensão Claude in Chrome instalada no Chrome NÃO se comunica com esta sessão CLI. Para usar essa opção, abra o Claude Desktop com o /carrossel.

Digite o número.
```

Mapa interno deste cenário: `{1: "manual", 2: "api_paralela"}`.

### Caso Desktop com MCP Chrome

`tem_chrome_mcp == true`:

```
Pronto. Pra gerar as 6 imagens você tem os seguintes caminhos:

1. Manual no ChatGPT. Eu te dou os prompts pra colar um a um. Gratuito.

2. Automatizado via Claude in Chrome. Eu abro chatgpt.com e mando os 6 prompts em sequência, aguardando cada imagem. Tempo: ~3 a 4 minutos (DALL-E é sequencial e o ChatGPT bloqueia o input enquanto gera). Você só aprova os pop-ups do Chrome (~6 a 8 cliques). Gratuito.

   Sub-opções da 2:
   2a. Só as 6 imagens. Eu gero a legenda local com Manual da Copy depois.
   2b. Imagens + legenda. O ChatGPT também cria a legenda em cima das 6 imagens.

{Se tem_api_imagem == true}
3. Automatizado via API ({provider_api}, gera as 6 em paralelo). Tempo: cerca de 60 segundos. Custo aproximado: $0.05 a $0.20. Eu disparo 6 chamadas paralelas e salvo as imagens direto na pasta.
{senão tem_api_imagem == false}
3. "Automatizado via API (OpenRouter, gera as 6 em paralelo)". Tempo: cerca de 60 segundos. Custo aproximado: $0.05 a $0.20. Indisponível agora, precisa configurar a OPENROUTER_API_KEY no .env. Rode /configurar-imagens antes de escolher essa opção.
{fim}

Digite 1, 2a, 2b ou 3.
```

### Comportamento ao escolher API paralela quando indisponível

Se o aluno escolher o número que mapeia para o caminho `api_paralela` com `tem_api_imagem == false`, pare a execução e responda:

```
Esse caminho precisa da OPENROUTER_API_KEY configurada no .env. Rode /configurar-imagens para adicionar a chave (leva ~1 minuto). Depois rode /carrossel de novo e ele fica disponível.

Enquanto isso, posso seguir pelo caminho Manual? Digite "sim" para continuar pelo Manual, ou "não" para encerrar.
```

AGUARDE A RESPOSTA.

---

## 3.5. Executar conforme a escolha

### Se 1 (Manual)

1. Os 6 prompts já estão visíveis no chat (mostrados no 3.1). O aluno copia direto do chat para o ChatGPT (ou outra ferramenta de imagem).
2. **Não grave arquivo extra em disco.** Nem `prompts.txt`, nem `prompt-claude-in-chrome.txt`.
3. Salve `legenda_origem = LOCAL` (a skill vai gerar a legenda no Passo 5).
4. Encerre o Passo 4 e siga para o Passo 5 (geração da legenda local).

### Se 2a (MCP automatizado, só imagens)

1. Anuncie:
   ```
   ⏳ Vou abrir o Claude in Chrome agora. Aprove os pop-ups conforme aparecerem (cerca de 6 a 8 cliques).
   ```
2. Execute via MCP:
   - `mcp__Claude_in_Chrome__navigate` para `https://chatgpt.com/?model=gpt-image` (ou modelo de imagem ativo)
   - Aguarde a página carregar
   - Para cada prompt (1 a 6), na ordem:
     - Use a tool de envio de mensagem do Claude in Chrome para colar e enviar o prompt
     - Aguarde 30 a 45 segundos (DALL-E demora pra gerar)
     - Se houver tool `wait_for_element`, use pra detectar "send button enabled" antes de mandar o próximo
   - Após os 6, capture a URL da conversa via `get_page_text` ou tool de URL atual
3. Avise:
   ```
   ✅ 6 imagens geradas no ChatGPT.
   Link da conversa: {url_chatgpt}
   ```
4. Salve `legenda_origem = LOCAL` (vamos gerar legenda local no Passo 5).
5. Siga para o Passo 5.

### Se 2b (MCP automatizado, imagens + legenda)

1. Anuncie:
   ```
   ⏳ Vou abrir o Claude in Chrome agora. Aprove os pop-ups conforme aparecerem (cerca de 6 a 8 cliques pra imagens + 1 clique pra legenda).
   ```
2. Execute via MCP (mesma sequência do 2a para as 6 imagens).
3. **Após as 6 imagens**, envie a Parte 3 (instrução de legenda do `prompt-claude-in-chrome-v2.md`) na mesma conversa:
   - Cole o texto entre `<<<` e `>>>` do arquivo v2 (sem as marcas)
   - Aguarde resposta (~20 segundos)
4. **Capture a legenda** via `mcp__Claude_in_Chrome__get_page_text`:
   - Pegue a última mensagem do assistant (texto após o último prompt enviado)
   - Limpe HTML, navegação, headers do ChatGPT (foco no corpo da legenda + hashtags)
5. **Passe a legenda capturada pela skill `revisora`** (mesmo as do ChatGPT precisam de checagem final do Manual da Copy):
   - Acione a skill `revisora` passando o texto
   - Aplique correções direto
6. **Salve a legenda em** `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-{estilo}/legenda.txt`.
7. **Mostre a legenda** ao aluno no chat com pergunta de aprovação:
   ```
   ✅ 6 imagens geradas no ChatGPT + legenda capturada.
   Link da conversa: {url_chatgpt}
   
   Legenda gerada pelo ChatGPT (já revisada pelo Manual da Copy):
   
   {legenda}
   
   1. Aprovar e salvar
   2. Ajustar (diga o que)
   3. Quero também a legenda local pra comparar (eu gero agora)
   4. Cancelar
   
   Digite o número.
   ```
8. Salve `legenda_origem = CHATGPT`.
9. Encerre o Passo 4. **No Passo 5, NÃO gere legenda local automaticamente.** Só gera se o aluno escolher opção 3 acima.

### Se 3 (API de imagem em paralelo)

Pré-requisito: `tem_api_imagem == true` (validado no Passo 3.3.B). Se `tem_api_imagem == false`, ver "Comportamento ao escolher opção 3 quando indisponível" na seção 3.4.

1. Anuncie:
   ```
   ⏳ Vou disparar 6 chamadas paralelas à API de imagem ({provider_api}). Tempo estimado: cerca de 60 segundos. Custo aproximado: $0.05 a $0.20.
   ```

2. Detecte o comando Python (`python3 --version 2>&1 || py -3 --version 2>&1`) e guarde como `{python}`.

3. **Grave um arquivo temporário** de prompts em `$CLAUDE_JOB_DIR/prompts-carrossel-{estilo}.txt` (ou `%TEMP%\` se a variável não existir) com os 6 prompts separados por linha em branco. Esse arquivo é usado apenas pela API e será deletado ao final.

4. Execute via `Bash`:
   ```bash
   {python} .claude/skills/carrossel/scripts/gerar-imagens-api.py \
     --prompts-file "{caminho_arquivo_temporario}" \
     --output-dir "meus-produtos/{ativo}/entregas/conteudo-social/carrossel-{estilo}/imagens" \
     --provider {provider_api}
   ```

   O script:
   - Lê o arquivo temporário (6 prompts separados por linha em branco).
   - Dispara as 6 chamadas à API em paralelo via `asyncio` + `aiohttp` (ou `concurrent.futures` se aiohttp não disponível).
   - Salva cada imagem como `slide-1.png` até `slide-6.png` na pasta `imagens/`.
   - Retorna JSON em stdout com status de cada uma.

5. **Delete o arquivo temporário** após a execução, com sucesso ou falha.

6. Processe o JSON:
   - Se `sucesso == 6`: avise:
     ```
     ✅ 6 imagens geradas em paralelo via {provider_api}.
     Pasta: meus-produtos/{ativo}/entregas/conteudo-social/carrossel-{estilo}/imagens/
     - slide-1.png
     - slide-2.png
     ...
     - slide-6.png
     
     Custo real: ~${custo_real}
     ```
   - Se `sucesso < 6`: liste quais slides falharam e ofereça retentar os falhos OU cair pra Manual.

7. Salve `legenda_origem = LOCAL` (a API só gera imagens; a legenda é gerada localmente no Passo 5).

8. Siga para o Passo 5.

---

## 3.6. Tratamento de erros do MCP Chrome

Se qualquer tool MCP falhar durante 2a ou 2b:

- **Permission denied / Tool permission stream closed**: avise o aluno "preciso que você aprove os pop-ups mais rápido" e retente a tool.
- **Navegação falhou ou ChatGPT pediu login**: pare a execução, avise o aluno:
  ```
  O ChatGPT pediu login ou a navegação falhou. Você quer:
  
  1. Tentar de novo (eu retento)
  2. Cair pra modo manual (eu te dou o prompt pra colar)
  3. Cancelar
  ```
- **Tool de send_message não existe na sessão**: caia direto pro modo manual e avise:
  ```
  A versão do Claude in Chrome conectada não suporta envio direto de mensagens. Vou cair pro modo manual.
  ```
  Os 6 prompts já estão visíveis no chat (mostrados no 3.1). O aluno copia direto. Siga para o Passo 5 com `legenda_origem = LOCAL`.

---

## Regras de qualidade do output triplo

- **Todo prompt em inglês.** O ChatGPT renderiza melhor o texto português quando recebe o template em inglês com as strings PT entre aspas.
- **Strings de título e subtítulo em português brasileiro com acentos.** Sob nenhuma hipótese o prompt pode pedir tradução para inglês das strings PT.
- **Indicador de página correto.** Slide 1 = `1/6`, Slide 2 = `2/6`, etc.
- **Paleta consistente entre os 6 slides.** Use a paleta default do estilo (ver `sistema-design.md`) ou a paleta do criador.
- **Coerência fotográfica entre os 6 slides.** Mesma atmosfera, mesma direção de luz, mesmo tratamento de cor.
- **Variável `legenda_origem`** define o comportamento do Passo 5: `LOCAL` gera legenda local, `CHATGPT` usa a já capturada e pula geração local.

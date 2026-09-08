---
name: "source-command-workshop-office"
description: "Liga a Sala dos Agentes (live-office). Registra o hook agent-status-writer.js no settings.json e abre o painel no navegador. Sem servidor — tudo roda em file://."
---

# source-command-workshop-office

Use this skill when the user asks to run the migrated source command `workshop-office`.

## Command Template

# Sala dos Agentes (Workshop Live Office)

Ativa a visualização em tempo real dos agentes do Workshop. Registra o hook que escreve o status de cada tool em `agents-status.json` (e no espelho `agents-status.js`) e abre o painel no navegador. Sem servidor: o painel lê o `.js` direto do disco via `<script src>`, funciona em `file://`.

## Usage

```
/workshop-office
```

## O Que Fazer

### 1. Registrar o hook em `.Codex/settings.json`

Leia `.Codex/settings.json`. Localize a chave `hooks.PostToolUse`. Verifique se já existe um bloco com `command` igual a `node .Codex/hooks/agent-status-writer.js`. Se já existir, não duplique. Apenas confirme: "Hook agent-status-writer já registrado.".

Se não existir, adicione ao final do array `hooks.PostToolUse` o seguinte bloco:

```json
{
  "matcher": "Write|Edit|Bash|Agent|Task|WebFetch|WebSearch",
  "hooks": [
    {
      "type": "command",
      "command": "node .Codex/hooks/agent-status-writer.js",
      "timeout": 5
    }
  ]
}
```

Use a tool Edit para inserir o bloco preservando a formatação JSON existente. Não altere nenhum outro hook nem qualquer outra chave do arquivo. Se o arquivo for inválido ou ficar inválido depois da edição, reverta e avise o usuário.

### 2. Disparar uma primeira escrita do status

Pra garantir que `.Codex/agents-memory/agents-status.js` exista antes de abrir o painel, rode qualquer tool simples (`bash echo` etc.) — o hook PostToolUse vai gerar o arquivo. Se já existir, pule.

```
ls .Codex/agents-memory/agents-status.js 2>/dev/null || echo "vai ser criado no próximo tool"
```

### 3. Abrir o painel no navegador

Use o caminho absoluto do `painel/index.html` (sem servidor). No macOS:

```
open "$(pwd)/painel/index.html"
```

Em outras plataformas, oriente o usuário a abrir manualmente: `painel/index.html` na raiz do projeto.

O painel tem duas abas no topo:
- **Painel do produto** — entregas do produto ativo (comportamento original).
- **Sala dos agentes** — bonecos mexendo em tempo real, lendo `.Codex/agents-memory/agents-status.js`.

### 4. Confirmar e orientar

Após abrir, mostre uma mensagem curta:

```
Sala dos Agentes no ar.

- Painel: file://<path>/painel/index.html
- Status: .Codex/agents-memory/agents-status.js (atualizado pelo hook a cada tool)
- Hook registrado: PostToolUse → agent-status-writer.js (timeout 5)

A cada tool que rodar (Write, Edit, Bash, Agent, Task, WebFetch, WebSearch), os bonecos mexem em até 2 segundos. Pra parar, basta fechar a aba.
```

## Quando usar este comando

USE quando:

- Você quer acompanhar visualmente qual agente está ativo em tempo real
- Está rodando uma sessão longa com múltiplos agentes em paralelo (executor de plano, lançamento, funil completo)
- Quer validar que os hooks estão escrevendo o status corretamente

NÃO USE quando:

- O projeto não tem `.Codex/hooks/agent-status-writer.js` (verifique antes de rodar)

## Observações

- `agents-status.js` é o espelho consumido pelo painel; `agents-status.json` continua sendo escrito junto pra outros consumidores. Os dois são regravados a cada tool.
- O hook só roda no projeto onde o `settings.json` tem o registro. Se você abrir outro projeto, registre lá também.
- Se você quiser apontar pra um servidor remoto em vez do arquivo local, abra o painel com `?statusUrl=URL` na sala dos agentes — ela cai pro modo `fetch` automaticamente.

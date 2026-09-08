---
name: "source-command-toolkit-pausar"
description: "Pausar o projeto ativo. Salva um resumo do estado e libera o produto para trabalhar em outra coisa sem perder contexto."
---

# source-command-toolkit-pausar

Use this skill when the user asks to run the migrated source command `toolkit-pausar`.

## Command Template

# Toolkit. Pausar Projeto

Marca o projeto atual como pausado e salva um resumo claro do que está pronto, do que falta e qual é o próximo passo. Serve como handoff entre sessões ou quando o usuário precisa trocar de frente sem perder contexto.

## Usage

```
/toolkit-pausar
```

## O Que Fazer

### 1. Verificar projeto ativo

Leia `meus-produtos/.ativo` e `meus-produtos/{ativo}/projeto/.ativo`. Se não houver projeto ativo, informe: "Não tem projeto ativo para pausar." e pare.

### 2. Perguntar o motivo (opcional, curto)

```
Por que está pausando?
(ex: "mudei de prioridade", "aguardando aprovação do cliente", "vou retomar na sexta", ou enter para pular)
```

### 3. Gerar resumo de handoff

Leia `estado.md`, `plano.md` e `pendencias.md`. Monte um bloco de handoff e acrescente no final do `estado.md`:

```markdown
## Handoff — {data}

**Motivo:** {motivo ou "não informado"}

**Estado do plano:**
- Concluídas: {lista curta das etapas concluídas}
- Em execução: {se houver, a etapa e o que falta nela}
- Pendentes: {lista das próximas}

**Contexto para retomar:**
- Último entregável gerado: {caminho}
- Próxima etapa recomendada: {N} — {título}
- Pendências a lembrar: {lista curta de pendencias.md}
```

### 4. Atualizar o estado

No topo do `estado.md`:
- Status: `pausado`
- Última atualização: {data}

### 5. Limpar o projeto ativo

Sobrescreva `meus-produtos/{ativo}/projeto/.ativo` deixando o arquivo vazio.

Isso permite que outro comando toolkit seja iniciado sem conflito. O projeto continua na pasta, só não está mais "ativo".

### 6. Confirmar

```
Projeto "{nome}" pausado.

Handoff salvo em meus-produtos/{ativo}/projeto/{projeto}/estado.md

Para retomar: /toolkit-retomar
Para começar outro: /toolkit-novo
```

---
name: "source-command-criar-gpt"
description: "Criar agente GPT personalizado para infoprodutores. gera 10 ideias, metodologia e prompt final com regras de seguranca. Pronto para configurar no ChatGPT."
---

# source-command-criar-gpt

Use this skill when the user asks to run the migrated source command `criar-gpt`.

## Command Template

# Criar Agente GPT

Cria um agente GPT personalizado para melhorar a entrega do produto do infoprodutor, com prompt pronto para usar no ChatGPT.

## Usage

```
/criar-gpt
```

## O Que Fazer

### 1. Contexto

Tente ler:
- `meus-produtos/.ativo` → se existir, leia `meus-produtos/{ativo}/perfil.md` como base
- Se nao existir produto ativo, peca ao usuario um texto sobre o produto/servico

### 2. Gerar ideias

Leia `.Codex/skills/agente-gpt/SKILL.md` e siga o fluxo completo:

- **Passo 0:** Coletar dados (do produto ativo ou texto do usuario)
- **Passo 1:** Gerar 10 ideias de agentes em tabela. Usuario escolhe 1.
- **Passo 2:** Criar metodologia do agente escolhido. Usuario aprova.
- **Passo 3:** Gerar prompt final com regra de seguranca + instrucoes + regra anti-engenharia reversa. Usuario aprova.

### 3. Salvar

- Com produto ativo: `meus-produtos/{ativo}/entregas/produto/agente-gpt-[slug].md`
- Sem produto ativo: `entregas/agente-gpt-[slug].md`

### 4. Finalizar

Apos o usuario aprovar o prompt final, salve e informe o caminho. NAO sugira proximos passos ou melhorias adicionais.

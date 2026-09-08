---
name: "source-command-toolkit-progresso"
description: "Mostrar o estado atual do projeto ativo. Resumo do plano, status de cada etapa, pendências em aberto e próxima ação recomendada."
---

# source-command-toolkit-progresso

Use this skill when the user asks to run the migrated source command `toolkit-progresso`.

## Command Template

# Toolkit. Progresso

Mostra onde o projeto ativo está agora: etapas concluídas, pendentes, puladas, última atividade e qual o próximo passo recomendado.

## Usage

```
/toolkit-progresso
```

## O Que Fazer

### 1. Carregar

Leia:
- `meus-produtos/.ativo`
- `meus-produtos/{ativo}/projeto/.ativo`
- `meus-produtos/{ativo}/projeto/{projeto}/roteiro.md`
- `meus-produtos/{ativo}/projeto/{projeto}/plano.md`
- `meus-produtos/{ativo}/projeto/{projeto}/estado.md`
- `meus-produtos/{ativo}/projeto/{projeto}/pendencias.md`

Se qualquer um dos arquivos essenciais não existir, informe o que falta e aponte o comando correto (`/produto-novo`, `/toolkit-novo`, `/toolkit-planejar`).

### 2. Montar resumo

Calcule:
- Total de etapas
- Concluídas, em execução, pendentes, puladas
- Porcentagem de avanço (concluídas / total)

### 3. Apresentar

Formato de saída:

```
Projeto: {nome}
Produto: {nome do produto}
Criado em: {data}
Última atualização: {data do estado.md}
Status geral: {status}

PROGRESSO
{concluídas}/{total} etapas concluídas ({porcentagem}%)

QUADRO DE ETAPAS
[tabela: # | Etapa | Status | Entregável]

ÚLTIMA ATIVIDADE
{última linha do histórico em estado.md}

PENDÊNCIAS EM ABERTO
{lista curta do pendencias.md, ou "Nenhuma"}

PRÓXIMA AÇÃO RECOMENDADA
{texto dinâmico conforme o estado}
```

### 4. Próxima ação recomendada

Lógica simples:

- Se `plano.md` não está preenchido → "Use `/toolkit-planejar` para gerar o plano."
- Se tem etapa `em-execucao` → "Continue a etapa {N} em andamento ou use `/toolkit-executar` para ver as opções."
- Se tem etapa `pendente` com dependências satisfeitas → "Use `/toolkit-executar` para rodar a etapa {N}."
- Se todas `concluido` → "Use `/toolkit-verificar` para auditoria final."
- Se tem etapa `pendente` mas todas travadas por dependência → "Desbloqueie a etapa {N} primeiro (está dependendo de {M})."
- Se status é `pausado` → "Projeto em pausa. Use `/toolkit-retomar` quando quiser continuar."

### 5. Não altere o estado

Este comando é só leitura. Não escreva em nenhum arquivo do projeto.

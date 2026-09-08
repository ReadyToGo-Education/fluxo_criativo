---
name: "source-command-toolkit-retomar"
description: "Retomar um projeto pausado do produto ativo. Lê o handoff anterior, reativa o projeto e mostra o próximo passo."
---

# source-command-toolkit-retomar

Use this skill when the user asks to run the migrated source command `toolkit-retomar`.

## Command Template

# Toolkit. Retomar Projeto

Reativa um projeto que foi pausado, lê o handoff e apresenta contexto para continuar de onde parou.

## Usage

```
/toolkit-retomar
```

## O Que Fazer

### 1. Verificar produto ativo

Leia `meus-produtos/.ativo`. Se vazio, informe: "Preciso de um produto ativo. Use `/produto-trocar`."

### 2. Listar projetos disponíveis

Liste as pastas dentro de `meus-produtos/{ativo}/projeto/`. Para cada projeto, leia as primeiras linhas de `estado.md` para extrair nome, status e última atualização.

Apresente:

```
Projetos de {nome do produto}:

1. {nome do projeto A} — {status} — atualizado em {data}
2. {nome do projeto B} — {status} — atualizado em {data}
3. Cancelar

Qual retomar?
```

Se só existir um projeto, pule para o passo 3 direto com ele.

Se não houver nenhum projeto, informe: "Nenhum projeto cadastrado. Use `/toolkit-novo`."

### 3. Ativar

Escreva o slug escolhido em `meus-produtos/{ativo}/projeto/.ativo`.

### 4. Ler handoff e contexto

Leia `meus-produtos/{ativo}/projeto/{projeto}/estado.md`. Busque a última seção `## Handoff` (a mais recente no final do arquivo).

Leia também:
- `roteiro.md` (objetivo)
- `plano.md` (etapas e status)
- `pendencias.md` (pendências em aberto)

### 5. Apresentar resumo para retomar

```
Projeto "{nome}" reativado.

CONTEXTO DA PAUSA
- Pausado em: {data}
- Motivo: {motivo do handoff}

ONDE PAROU
- Último entregável: {caminho}
- Próxima etapa recomendada: {N} — {título}
- Pendências em aberto: {contagem}

ROTEIRO (lembrete rápido)
- Objetivo: {objetivo do roteiro.md}
- Prazo: {prazo}

PRÓXIMO PASSO
Use /toolkit-executar para rodar a etapa {N}, ou /toolkit-progresso para ver o quadro completo antes.
```

### 6. Atualizar estado

No `estado.md`:
- Status: voltar para `em-andamento` (ou `planejado` se ainda estiver na etapa 0)
- Adicionar ao histórico: `{data}: projeto retomado após pausa`

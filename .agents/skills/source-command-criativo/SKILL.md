---
name: "source-command-criativo"
description: "Criar criativos visuais para o produto ativo. Três caminhos: Criativo AIDA (prompt em 3 passos para anúncio em imagem), Referência Visual (editar imagem existente com troca de personagem, texto ou cor) ou Carrossel para Instagram (cards com foto real gerada por IA). Tudo vai para meus-produtos/{ativo}/entregas/criativos/."
---

# source-command-criativo

Use esta skill quando o usuário pedir o comando `/criativo` do workshop (ou `criativo`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/criativo.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Criativo. Gerador de Criativos Visuais

## O Que Fazer

### 1. Contexto

Leia `meus-produtos/.ativo`, depois `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme o CLAUDE.md).

### 2. Escolha do Tipo

```
O que você quer criar?

1. Criativo AIDA (imagem para anúncio em 3 passos)
2. Usar referência visual (editar imagem que você já tem)
3. Carrossel para Instagram (cards com foto real gerada por IA)

Digite o número:
```

### 3. Execução por Tipo

**Opção 1 — Criativo AIDA:**
Leia `.claude/commands/criativo-aida.md` e execute o fluxo completo. O contexto do produto já foi carregado.

**Opção 2 — Referência Visual:**
Leia `.claude/commands/img-anuncio.md` e execute o fluxo completo. O contexto do produto já foi carregado.

**Opção 3 — Carrossel para Instagram:**
Acione a skill `carrossel-visual` para conduzir o fluxo completo de 9 etapas com geração de foto por card. O contexto do produto já foi carregado. Requer OPENROUTER_API_KEY ou FREEPIK_API_KEY configurada no `.env`.

---

Todos os arquivos gerados são salvos em `meus-produtos/{ativo}/entregas/criativos/`.

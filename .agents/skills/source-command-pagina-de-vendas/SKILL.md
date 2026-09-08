---
name: "source-command-pagina-de-vendas"
description: "Comando descontinuado. Redireciona para /copy-pagina, que é o fluxo oficial de página de vendas baseado em templates atômicos com merge, preservando layout do tema sem redesenhar."
---

# source-command-pagina-de-vendas

Use this skill when the user asks to run the migrated source command `pagina-de-vendas`.

## Command Template

# Página de Vendas. Redirecionamento

Este comando foi descontinuado. Ele gerava HTML do zero a cada execução, o que é proibido pelo AGENTS.md (seção "Custo-benefício na página de vendas"):

> Proibido reescrever estrutura (HTML, CSS do bloco, classes, grids), trocar fontes ou paleta do tema, ou gerar uma página "nova" no lugar do template.

## O que fazer agora

Use `/copy-pagina`. Esse command já faz tudo:

1. Detecta se a copy aprovada já existe em `meus-produtos/{ativo}/entregas/copy-pagina/copy-{ativo}.md` e avisa antes de regerar.
2. Se faltar copy, gera a copy completa nos 16 blocos padrão (Light Copy, estrutura 8D).
3. Pergunta qual tema visual usar (`flat_claro`, `minimal_claro`, `glass_escuro`, `teal_claro`, `purple_escuro`).
4. Preenche os 16 `code.html` atômicos do tema com a copy aprovada (preserva layout, muda só texto).
5. Roda o merge e entrega `vendas-{slug}.html`.

## Ação obrigatória

Quando o usuário acionar `/pagina-de-vendas`, responda:

```
Esse comando foi descontinuado. O fluxo oficial de página de vendas agora é /copy-pagina, que preserva o layout do tema em vez de gerar HTML do zero (regra do AGENTS.md).

Vou acionar /copy-pagina com o produto ativo. Ele vai checar se já existe copy aprovada, perguntar o tema visual e entregar a página pronta.
```

Em seguida, **acione a skill `copy-pagina` via Skill tool imediatamente**, sem pedir mais nada ao usuário.

Não gere HTML, não chame agentes, não leia `design-system-components.md` ou `design-referencia-vtsd.md` diretamente, não escolha paleta no chat: tudo isso é responsabilidade das skills `copy-pagina` e `paginas`, que usam templates prontos.

Se o aluno insistir em gerar do zero, explique que o fluxo atual preserva os 5 temas do design system (que já têm cores, fontes, componentes e responsividade testados) e que gerar do zero produz páginas inconsistentes e quebra a linha editorial do workshop.

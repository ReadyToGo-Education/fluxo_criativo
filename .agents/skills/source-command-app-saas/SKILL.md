---
name: "source-command-app-saas"
description: "Lê o perfil do produto ativo, sugere 10 ideias de mini-SaaS relevantes para os alunos do infoprodutor e, após a escolha, gera o PRD completo com schema, telas, user stories e prompt técnico pronto para colar no Lovable.dev."
---

# source-command-app-saas

Use this skill when the user asks to run the migrated source command `app-saas`.

## Command Template

# App SaaS. Gerador de Épicos para Alunos

Acione a skill `app-saas` do plugin `workshop-marketing` e siga o roteiro:

1. Ler `meus-produtos/.ativo` para pegar o slug do produto ativo.
2. Ler `meus-produtos/{slug}/perfil.md` completo.
3. Listar arquivos em `meus-produtos/{slug}/` e ler `idconsumidor.md` se existir.
4. Gerar 10 ideias de mini-SaaS relevantes para o público do produto (tracker, diagnóstico, planner, gerador, checklist interativo, simulador, comparador, dashboard, calculadora, biblioteca de recursos).
5. Perguntar qual ideia o usuário quer desenvolver (aceitar número, mistura ou pedido de novas ideias).
6. Gerar o PRD completo: visão geral, problema resolvido, público-alvo, user stories, schema do banco (máximo 5 tabelas), telas na ordem de navegação, regras de negócio, identidade visual puxada do perfil.md e prompt técnico para o Lovable.dev.
7. Mostrar tudo e pedir aprovação.
8. Salvar em `meus-produtos/{slug}/entregas/apps/{slug-do-epic}.md` após aprovação.
9. Orientar os próximos passos no Lovable.

## Regras

- Nunca gerar o PRD sem o usuário ter escolhido uma ideia.
- Schema simples, máximo 5 tabelas.
- Nunca entregar código. Apenas especificação + prompt.
- Prompt para o Lovable sempre em português do Brasil, direto e sem markdown interno.
- Identidade visual sempre puxada do `perfil.md`.
- Não usar travessão em nenhum texto exibido.
- Não usar ponto de exclamação.

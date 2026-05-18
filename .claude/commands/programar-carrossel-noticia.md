---
name: workshop-marketing:programar-carrossel-noticia
description: Programa tarefa recorrente que gera carrossel de notícia para Instagram automaticamente (via /schedule do Claude). Configura escopo (só busca ou carrossel inteiro), modo (aleatório ou fixo), tom travado, categoria travada (Trend ou Atemporal) e frequência. Coleta @, nicho e produto uma única vez (reaproveita do perfil ativo quando possível).
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill
---

# Programar Carrossel de Notícia

Aciona a skill `programar-carrossel-noticia` para conduzir o fluxo de configuração completo (7 passos) e criar a tarefa recorrente no `/schedule` do Claude.

A skill cuida de toda a orquestração: leitura do produto ativo, coleta de @, nicho e produto (com reaproveitamento do perfil), escolha de escopo (só busca de notícia ou carrossel inteiro), modo de execução (aleatório ou fixo), travamento de tom e categoria de notícia, montagem do cron, preview YAML, confirmação e criação do agendamento.

O resultado de cada execução do agendamento aparece no painel de Routines do Claude (cloud). O aluno abre, copia e monta o carrossel no Instagram.

Para pausar ou deletar um agendamento existente, use `/schedule pause {{schedule_id}}` ou `/schedule delete {{schedule_id}}`.

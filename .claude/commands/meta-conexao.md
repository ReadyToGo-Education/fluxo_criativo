---
name: workshop-marketing:meta-conexao
description: Alias de compatibilidade. Esta skill foi renomeada para /trafego-conexao. Quem invocar /meta-conexao é redirecionado automaticamente. Mantida apenas para evitar quebra em referências antigas.
allowed-tools: Skill
model: sonnet
user-invocable: false
---

# Meta Conexão (alias)

Esta skill foi renomeada. Toda a lógica de conexão com o Meta Ads vive agora em **`/trafego-conexao`**.

## O que fazer

Acionar imediatamente a skill `/trafego-conexao` repassando os argumentos recebidos. Não duplicar lógica aqui: o fluxo é orquestrado por `.claude/commands/trafego-conexao.md` e a especificação completa está em `.claude/skills/trafego-conexao/SKILL.md`.

## Por que este arquivo existe

Mantido como shim de compatibilidade enquanto outras partes do sistema ainda referenciem `/meta-conexao` por nome. Quando todas as referências forem atualizadas, este arquivo pode ser removido com segurança.

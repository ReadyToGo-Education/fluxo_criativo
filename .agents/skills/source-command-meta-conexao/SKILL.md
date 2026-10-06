---
name: "source-command-meta-conexao"
description: "Alias de compatibilidade. Esta skill foi renomeada para /trafego-conexao. Quem invocar /meta-conexao é redirecionado automaticamente. Mantida apenas para evitar quebra em referências antigas."
---

# source-command-meta-conexao

Use esta skill quando o usuário pedir o comando `/meta-conexao` do workshop (ou `meta-conexao`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/meta-conexao.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Meta Conexão (alias)

Esta skill foi renomeada. Toda a lógica de conexão com o Meta Ads vive agora em **`/trafego-conexao`**.

## O que fazer

Acionar imediatamente a skill `/trafego-conexao` repassando os argumentos recebidos. Não duplicar lógica aqui — todo o fluxo (Passo 0 a Passo 4 + saída final + princípios) está mantido em `.claude/commands/trafego-conexao.md`.

## Por que este arquivo existe

Mantido como shim de compatibilidade enquanto outras partes do sistema ainda referenciem `/meta-conexao` por nome. Quando todas as referências forem atualizadas, este arquivo pode ser removido com segurança.

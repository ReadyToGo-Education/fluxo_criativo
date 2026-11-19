---
name: "source-command-criar-gpt"
description: "Comando antigo, substituído pelo /criar-agente. Os GPTs personalizados do ChatGPT saem do ar em 11/12/2026. Avisa o aluno e segue o /criar-agente, que cria o agente na Hotmart ou como plugin do ChatGPT."
---

# source-command-criar-gpt

Use esta skill quando o usuário pedir o comando `/criar-gpt` do workshop (ou `criar-gpt`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/criar-gpt.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Criar GPT (substituído pelo /criar-agente)

Os GPTs personalizados do ChatGPT saem do ar em 11/12/2026, e a criação de GPT novo já está fechada. O agente do produto agora é criado pelo `/criar-agente`.

## O Que Fazer

1. Mostre ao aluno, numa mensagem só:

   ```
   O /criar-gpt mudou de nome: agora é /criar-agente.

   Os GPTs do ChatGPT saem do ar em 11/12/2026. O seu agente continua o mesmo, o que muda é onde ele fica:
   - Se você vende na Hotmart: vira um Agente de IA da Hotmart.
   - Se vende em outra plataforma: vira um plugin do ChatGPT, que o seu aluno instala.

   Vou seguir pelo /criar-agente. Se você já tem um GPT no ar, dá para trazer ele também.
   ```

2. Leia `.claude/commands/criar-agente.md` e siga o fluxo a partir dali, sem pedir para o aluno digitar o comando novo.

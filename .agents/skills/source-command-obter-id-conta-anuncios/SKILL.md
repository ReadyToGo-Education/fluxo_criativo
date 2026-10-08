---
name: "source-command-obter-id-conta-anuncios"
description: "Guia para localizar o ID da conta de anúncios no Business Manager do Facebook e salvar em FB_AD_ACCOUNT_ID no .env. Skill reutilizável chamada por qualquer skill de Meta Ads que precise do ID da conta (ex: /trafego-conexao, /ads-relatorio)."
---

# source-command-obter-id-conta-anuncios

Use esta skill quando o usuário pedir o comando `/obter-id-conta-anuncios` do workshop (ou `obter-id-conta-anuncios`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/obter-id-conta-anuncios.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Obter ID da Conta de Anúncios

Localiza o ID da conta de anúncios e salva no `.env` como `FB_AD_ACCOUNT_ID`. Esse ID é necessário para validar o token do Meta Ads, gerar relatórios e fazer chamadas à Graph API.

---

## Passo 1. Localizar o ID

Instrua o aluno:

```
Para encontrar o ID da conta de anúncios:

1. Acesse business.facebook.com/latest/settings
2. No menu lateral, clique em "Contas de anuncio"
3. Selecione a conta de anuncios que voce quer usar
4. Na tela da conta, localize o campo "Identificacao"
5. Copie o numero que aparece ali (so os numeros, sem o prefixo "act_")

Cole aqui o ID:
```

Aguardar o aluno colar o ID.

---

## Passo 2. Validar o formato

O ID deve ser uma sequência numérica de 13 a 16 dígitos (sem o prefixo `act_`). Se vier com prefixo `act_`, remover automaticamente. Se vier com espaços ou caracteres não numéricos, alertar o aluno e pedir de novo.

---

## Passo 3. Salvar no .env

Leia o `.env`.

- Se a linha `FB_AD_ACCOUNT_ID` já existir: atualize o valor com `Edit` cirúrgico.
- Se não existir: adicione `FB_AD_ACCOUNT_ID={valor}` ao final do arquivo.

O nome padrão obrigatório é `FB_AD_ACCOUNT_ID` (sem o prefixo `act_` no valor). Não usar variação diferente desse nome. Não sobrescrever outras variáveis do `.env`.

Confirme ao aluno:

```
✅ ID da conta de anúncios salvo como FB_AD_ACCOUNT_ID no .env.
```

---

## Após salvar

Retorne à skill que chamou esta e siga o próximo passo. Exemplos de fluxo:

- Se chamada por `/trafego-conexao` (modo APP): voltar para o Passo 3 (validação) da skill `trafego-conexao`.
- Se chamada por `/gerar-token-permanente-facebook-ads`: voltar e seguir para a próxima skill do fluxo (geralmente `/trafego-conexao` ou `/ads-relatorio`).
- Se chamada por `/ads-relatorio`: voltar e continuar a configuração do relatório.

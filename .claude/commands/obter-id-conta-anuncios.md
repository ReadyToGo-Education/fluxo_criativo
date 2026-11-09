---
name: workshop-marketing:obter-id-conta-anuncios
description: Guia para localizar o ID da conta de anúncios no Business Manager do Facebook e salvar em FB_AD_ACCOUNT_ID no .env. Skill reutilizável chamada por qualquer skill de Meta Ads que precise do ID da conta (ex: /trafego-conexao, /ads-relatorio).
allowed-tools: Read, Write, Edit, Glob, Bash
model: sonnet
user-invocable: false
---

# Obter ID da Conta de Anúncios

Localiza o ID da conta de anúncios e salva no `.env` como `FB_AD_ACCOUNT_ID`. Esse ID é necessário para validar o token do Meta Ads, gerar relatórios e fazer chamadas à Graph API.

É o último recurso. Quando a listagem automática das contas está disponível (Passo 5 do `/gerar-token-permanente-facebook-ads` ou seção 4.3 da SKILL `trafego-conexao`), a conta sai dela e o ID não é pedido ao aluno. No caminho do App da `/trafego-conexao`, esta skill só entra se a conta padrão continuar faltando depois dessa listagem (seção 4.2 da SKILL `trafego-conexao`).

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

Gravar sem abrir o `.env` (nunca Read, Edit ou Write nele, porque a leitura traz o token e as outras chaves para a conversa), com o comando de uma linha do item 4 da seção "LEITURA SEGURA DO .env" do CLAUDE.md. Ele apaga a linha antiga (inclusive a vazia, vinda do `.env.example`) e acrescenta a nova:

```bash
touch .env && sed -i '/^FB_AD_ACCOUNT_ID=/d' .env && { [ -z "$(tail -c1 .env)" ] || echo >> .env; } && printf 'FB_AD_ACCOUNT_ID=%s\n' "<id>" >> .env
```

No Mac, trocar `sed -i` por `sed -i ''`.

O ID padrão precisa aparecer também em `FB_AD_ACCOUNT_IDS` (seção 6.4 da SKILL `trafego-conexao`). Ler a lista com `grep "^FB_AD_ACCOUNT_IDS=" .env | cut -d= -f2-` (não é segredo). Se vier vazia, gravar `FB_AD_ACCOUNT_IDS` com o mesmo ID; se tiver outras contas e não tiver esta, gravar a lista antiga com `,<id>` no fim. Usar o mesmo comando acima, trocando o nome da variável.

O nome padrão obrigatório é `FB_AD_ACCOUNT_ID` (sem o prefixo `act_` no valor). Não usar variação diferente desse nome. Não sobrescrever outras variáveis do `.env`.

Confirme ao aluno:

```
✅ ID da conta de anúncios salvo como FB_AD_ACCOUNT_ID no .env.
```

---

## Após salvar

Retorne à skill que chamou esta e siga o próximo passo. Exemplos de fluxo:

- Se chamada por `/trafego-conexao` (modo APP): voltar para o Passo 3 (validação) da skill `trafego-conexao`.
- Se chamada por `/ads-relatorio`: voltar e continuar a configuração do relatório.

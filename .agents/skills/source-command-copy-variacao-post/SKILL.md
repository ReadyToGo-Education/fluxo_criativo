---
name: "source-command-copy-variacao-post"
description: "Criar variacoes de posts que ja tiveram alto engajamento, a partir do insights.json gerado pelo dashboard do Instagram. Cada post selecionado gera 3 variacoes com elementos literarios diferentes."
---

# source-command-copy-variacao-post

Use this skill when the user asks to run the migrated source command `copy-variacao-post`.

## Command Template

# Variacao de Posts Validados

Cria variacoes de conteudo a partir dos posts com maior engajamento do perfil, usando o `insights.json` do dashboard do Instagram como base de dados.

Siga a skill `copy-variacao-post` para todas as regras tecnicas, fluxo e checklist de geracao.

---

## PASSO 0. Verificar Pre-Requisitos

Antes de qualquer pergunta, verifique em paralelo:

1. `meus-produtos/.ativo` — produto ativo existe?
2. `entregas/instagram-dashboard/insights.json` — arquivo existe e tem dados?

Se o `insights.json` nao existir:
```
Para usar este comando, primeiro configure o dashboard do Instagram.

Use /instagram-dashboard para conectar seu perfil e gerar os dados de engajamento.
```

Se existir, leia o arquivo e mostre o resumo conforme o PASSO 0 da skill.

---

## PASSO 1 a 7

Siga rigorosamente o fluxo descrito na skill `copy-variacao-post`:

- PASSO 1: Selecao dos posts base (exibir top 10, aceitar numeros, lista ou "todos")
- PASSO 2: Configuracao (formato de saida + objetivo, UMA pergunta por vez)
- PASSO 3: Pesquisa de virais (OBRIGATORIO antes de gerar qualquer conteudo)
- PASSO 4: Analise interna do post original (angulo, estrutura, tom, hipotese de por que funcionou)
- PASSO 5: Geracao das 3 variacoes por post (elemento literario diferente em cada uma)
- PASSO 6: Aprovacao e salvamento
- PASSO 7: Proximo passo sugerido

---

## REGRAS

- Nunca gerar sem ter lido o `insights.json`.
- Nunca usar travessao em nenhuma variacao gerada.
- Nunca repetir o mesmo elemento literario em duas variacoes do mesmo post.
- Pesquisa de virais e obrigatoria. Sem ela, o estilo fica desatualizado.
- Pedir aprovacao antes de salvar. Regra padrao sem excecao.

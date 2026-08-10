---
name: workshop-marketing:app-pratico
description: Transformar a transcricao completa das aulas de um curso em um aplicativo web pratico (calculadora, checklist, arvore de decisao) publicado direto na Vercel, com a propria skill verificando a integracao, criando o projeto e fazendo o deploy. Sempre comeca com uma pre avaliacao de objetivo com o aluno. Sem login, sem banco de dados, sem codigo escrito pelo aluno.
---

# App Pratico. Do Curso ao Aplicativo Publicado

Pega o conteudo real das aulas de um curso e devolve uma ferramenta pratica
(calculadora, checklist interativo, arvore de decisao, conversor, gerador
de script) que o aluno do curso usa no dia a dia, com link proprio
publicado na Vercel.

## Usage

```
/app-pratico
```

## O Que Fazer

Acione a skill `app-pratico` e siga o roteiro:

1. Confirmar produto ativo cadastrado (`/produto-novo` primeiro, se ainda
   nao existir).
2. Fazer a pre avaliacao com o aluno (objetivo do app, publico de acesso,
   ideia previa se houver, prazo) antes de propor qualquer coisa.
3. Reunir a transcricao completa das aulas (YouTube via legenda automatica,
   arquivos de texto/PDF/Word ja existentes, ou exportacao da plataforma do
   curso).
4. Ler tudo e mapear formulas, checklists, protocolos e scripts que o curso
   ensina.
5. Propor 6 a 10 ideias de app pratico, filtradas pelo objetivo definido na
   pre avaliacao, e deixar o aluno escolher.
6. Especificar o escopo (paineis, formulas, exemplos de validacao, trava de
   senha ja decidida na pre avaliacao) e pedir aprovacao.
7. Construir o app em um unico arquivo HTML, mobile-first, sem
   dependencias externas.
8. Validar cada calculo contra os exemplos numericos das proprias aulas.
9. Pedir aprovacao final, salvar em
   `meus-produtos/{ativo}/entregas/aplicativo/`.
10. Publicar na Vercel: a propria skill verifica se ja existe token e
    projeto configurados, cria o projeto quando necessario, faz o deploy e
    entrega o link publico (sem depender do aluno rodar `/pagina-vercel` a
    parte).

## Regras Resumidas

- Nunca pular a pre avaliacao de objetivo antes de propor ideias de app.
- Nunca inventar formula ou dado que nao veio das aulas.
- Sempre validar contra exemplo numerico do proprio curso antes de
  publicar.
- App sempre sem login e sem banco de dados. Se o pedido exigir isso, usar
  `/app-saas` em vez desta skill.
- Antes de criar projeto novo na Vercel, checar se ja existe um vinculado a
  este app para nao duplicar.
- Nunca expor o token da Vercel no chat.
- Nao usar travessao em nenhum texto exibido.

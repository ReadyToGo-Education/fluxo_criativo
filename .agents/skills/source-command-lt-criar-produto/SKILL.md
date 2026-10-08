---
name: "source-command-lt-criar-produto"
description: "Cria o conteúdo real do produto digital de entrada. e-book, checklist, mini-curso, desafio, agente GPT ou planilha. Gera o arquivo pronto para entregar ao comprador."
---

# source-command-lt-criar-produto

Use esta skill quando o usuário pedir o comando `/lt-criar-produto` do workshop (ou `lt-criar-produto`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/lt-criar-produto.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Criar Produto Low Ticket

Cria o conteúdo real do produto digital (o que o comprador vai receber), confirmando cada etapa com o usuário antes de avançar.

## Usage

```
/lt-criar-produto
```

## O Que Fazer

### 1. Contexto

Leia:
- `meus-produtos/.ativo` → se não existir, oriente a usar `/produto-novo` primeiro
- `meus-produtos/{ativo}/resumo-produto.md` (resumo do produto; se não existir, gerar conforme "Contexto Persistente do Negócio" no CLAUDE.md)

### 2. Verificar formato

Use o `meus-produtos/{ativo}/resumo-produto.md` e identifique se o formato do produto já está definido.

**Se o formato já estiver no perfil**, confirme com o usuário:

```
Encontrei seu produto: [nome do produto]
Formato: [formato identificado no perfil]

Vou criar o conteúdo do produto agora.

1. Sim, pode seguir
2. Quero escolher outro formato
```

**Se o formato não estiver no perfil** ou o usuário quiser trocar, apresente as opções:

```
Qual é o formato do produto que vou criar?

1. E-book / Guia (PDF passo a passo)
2. Checklist / Roteiro de autoaplicação
3. Mini-curso (3 a 5 aulas curtas em vídeo)
4. Desafio (5 a 7 dias com tarefas diárias)
5. Agente GPT (assistente de IA personalizado)
6. Planilha (ferramenta de cálculo ou organização)

Digite o número:
```

### 3. Criar o produto

Leia `.claude/skills/criacao-produto-low-ticket/SKILL.md` e siga o fluxo do formato escolhido.

### 4. Próximo passo — Aplicar Framework Quiz vs. Página

Após salvar o produto, aplique OBRIGATORIAMENTE o framework abaixo para recomendar o próximo passo. Nunca sugira /pagina-de-vendas ou /quiz sem antes passar por esse framework.

**Framework de Decisão: Quiz vs. Página de Vendas**

| Critério | Aponta para QUIZ | Aponta para PÁGINA |
|---|---|---|
| Tipo de produto | Emocional / dor / identificação | Prático / ferramenta / direto ao ponto |
| Nível de consciência do lead | Não sabe que tem problema | Já sabe o que quer |
| Complexidade da decisão | Precisa diagnosticar / explicar | Decisão simples e direta |
| Faixa de preço | Até R$47 | Acima de R$97 |
| Tipo de público | Emocional | Analítico / pragmático |

**Regra:** 2 ou mais critérios para o mesmo lado — siga ele. Desempate: recomendar QUIZ.

Apresente a recomendação assim:

```
Produto criado e salvo.

Com base no seu produto e público, o próximo passo recomendado é:

→ [QUIZ ou PÁGINA DE VENDAS]

Por quê:
• [Critério 1]: [explicação com dado real do produto]
• [Critério 2]: [explicação com dado real do produto]
• [Critério 3]: [explicação com dado real do produto]

1. Concordo, seguir com [recomendação] → use /quiz ou /paginas-low-ticket
2. Prefiro o outro formato
3. Criar anúncios primeiro → use /copy-anuncio
```

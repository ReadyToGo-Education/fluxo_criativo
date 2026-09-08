---
name: "source-command-toolkit-planejar"
description: "Gerar o plano em etapas do projeto ativo a partir do roteiro. Quebra o objetivo em etapas sequenciais com skill/comando associado, entregável esperado e ordem de execução."
---

# source-command-toolkit-planejar

Use this skill when the user asks to run the migrated source command `toolkit-planejar`.

## Command Template

# Toolkit. Gerar Plano

Transforma o roteiro do projeto em um plano de execução concreto: lista ordenada de etapas, cada uma com a skill/comando que vai rodar e o entregável que vai produzir.

## Usage

```
/toolkit-planejar
```

## O Que Fazer

### 1. Verificar projeto ativo

Leia `meus-produtos/.ativo`. Se vazio, pare e oriente: "Preciso de um produto ativo. Use `/produto-novo`."

Leia `meus-produtos/{ativo}/projeto/.ativo`. Se não existir, pare e oriente: "Não tem projeto ativo. Use `/toolkit-novo` antes."

Guarde o slug do projeto na variável `{projeto}`.

### 2. Ler contexto

Leia nesta ordem (se existirem):
- `meus-produtos/{ativo}/perfil.md`
- `meus-produtos/{ativo}/idconsumidor.md`
- `meus-produtos/{ativo}/tipo.md`
- `meus-produtos/{ativo}/projeto/{projeto}/roteiro.md`

### 3. Gerar o plano

Com base no roteiro, monte uma sequência de etapas. Cada etapa é uma linha da tabela abaixo:

| # | Etapa | Skill ou comando | Entregável esperado | Depende de | Status |

**Regras para montar o plano:**
- Comece pelas fundações (produto, identidade do consumidor) se ainda faltarem.
- Siga a ordem natural do funil: estratégia → copy → página → anúncios → emails → publicação.
- Cada etapa tem no máximo 1 skill. Se for grande, quebre em 2.
- Se a etapa precisa de entregável de outra, marque na coluna "Depende de".
- Status começa sempre como `pendente`.
- Use as skills disponíveis no projeto. Não invente comandos.

**Exemplo de plano para lançamento middle ticket:**

```markdown
| # | Etapa | Skill ou comando | Entregável esperado | Depende de | Status |
|---|---|---|---|---|---|
| 1 | Big Idea do evento | /ht-big-idea | meus-produtos/{ativo}/entregas/comercial/big-idea.md | - | pendente |
| 2 | Oferta completa | /ht-oferta | meus-produtos/{ativo}/entregas/comercial/oferta.md | 1 | pendente |
| 3 | Página de inscrição | /ht-pagina-inscricao | meus-produtos/{ativo}/entregas/paginas/inscricao.html | 1, 2 | pendente |
| 4 | Cronograma do evento | /ht-cronograma | meus-produtos/{ativo}/entregas/comercial/cronograma.md | 1 | pendente |
| 5 | Conteúdo dos blocos | /ht-conteudo | meus-produtos/{ativo}/entregas/comercial/conteudo-blocos.md | 4 | pendente |
| 6 | Pitch de palco | /ht-pitch-palco | meus-produtos/{ativo}/entregas/comercial/pitch-palco.md | 2, 5 | pendente |
| 7 | Comunicação pré-evento | /ht-comunicacao-pre | meus-produtos/{ativo}/entregas/emails/pre-evento.md | 3 | pendente |
| 8 | Anúncios de captação | /ht-anuncios | meus-produtos/{ativo}/entregas/criativos/captacao.md | 3 | pendente |
| 9 | Follow-up pós-evento | /ht-follow-up | meus-produtos/{ativo}/entregas/emails/follow-up.md | 6 | pendente |
```

### 4. Apresentar para aprovação

Mostre a tabela no chat e peça aprovação:

```
Plano gerado com {N} etapas.

[tabela completa aqui]

1. Aprovar e salvar
2. Quero ajustar algo (descreva o que mudar)
```

Se o usuário pedir ajuste, edite e pergunte de novo até aprovar.

### 5. Salvar o plano

Após aprovação, escreva em `meus-produtos/{ativo}/projeto/{projeto}/plano.md`:

```markdown
# Plano de execução

Gerado em {data}.

## Etapas

[tabela aprovada aqui]

## Legenda de status
- pendente: ainda não começou
- em-execucao: em andamento
- concluido: entregável pronto e aprovado
- pulado: decidiu não fazer (registre a razão ao lado)
```

### 6. Atualizar o estado

Abra `meus-produtos/{ativo}/projeto/{projeto}/estado.md` e atualize:
- Status: `planejado`
- Etapa atual: `1`
- Última atualização: {data}
- Adicione uma linha ao histórico: `{data}: plano aprovado com {N} etapas`

### 7. Sugerir próximo passo

```
Plano salvo em meus-produtos/{ativo}/projeto/{projeto}/plano.md

Próximo passo: /toolkit-executar para rodar a primeira etapa.
```

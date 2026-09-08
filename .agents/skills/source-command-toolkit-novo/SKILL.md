---
name: "source-command-toolkit-novo"
description: "Iniciar um novo projeto de marketing estruturado (lançamento, funil completo, reestruturação). Cria a pasta projeto/ dentro do produto ativo com roteiro, estado e pendências."
---

# source-command-toolkit-novo

Use this skill when the user asks to run the migrated source command `toolkit-novo`.

## Command Template

# Toolkit. Novo Projeto

Inicia um projeto de marketing estruturado quando a demanda é grande (lançamento, funil completo, reestruturação de produto, múltiplos entregáveis interdependentes). Pra tarefa simples de uma skill só, não use este comando. Vá direto pela skill (`/copy-pagina`, `/copy-anuncio`, etc.).

## Usage

```
/toolkit-novo
```

## O Que Fazer

### 1. Verificar produto ativo

Leia `meus-produtos/.ativo`. Se não existir, oriente: "Preciso de um produto ativo antes. Use `/produto-novo` primeiro."

Leia `meus-produtos/{ativo}/perfil.md` para contexto. Se não existir, oriente: "Esse produto ainda não tem perfil. Use `/produto-concepcao` primeiro."

### 2. Entrevista breve (3 perguntas, uma por vez)

**Pergunta 1. Objetivo do projeto.**

```
Qual o objetivo deste projeto?

1. Lançamento (evento com prazo e pico de vendas)
2. Funil perpétuo (página de vendas sempre no ar)
3. Funil low ticket (produto de entrada com quiz ou página direta)
4. Funil high ticket C10X (retiro, webinar, venda 1:1)
5. Reestruturação de algo existente
6. Outro (descreva)

Digite o número:
```

**Pergunta 2. Prazo ou janela.**

```
Qual o prazo?
(ex: "3 semanas até o evento", "até o fim do mês", "sem prazo fixo, quero fazer com calma")
```

**Pergunta 3. Resultado esperado ao final.**

```
Ao final do projeto, o que precisa estar pronto e funcionando?
(ex: "página de vendas publicada + 3 anúncios rodando", "funil completo do anúncio ao email pós-compra")
```

### 3. Gerar slug do projeto

Com o objetivo, crie um slug curto em kebab-case:
- "Lançamento do curso" → `lancamento-curso`
- "Funil perpétuo do ebook" → `funil-ebook`

Confirme:
```
Identificador do projeto: {slug}

1. Confirmar
2. Usar outro nome
```

### 4. Criar estrutura

Crie a pasta e os arquivos:

```
meus-produtos/{ativo}/projeto/
meus-produtos/{ativo}/projeto/{slug}/
meus-produtos/{ativo}/projeto/{slug}/roteiro.md
meus-produtos/{ativo}/projeto/{slug}/plano.md
meus-produtos/{ativo}/projeto/{slug}/estado.md
meus-produtos/{ativo}/projeto/{slug}/pendencias.md
meus-produtos/{ativo}/projeto/.ativo
```

**`meus-produtos/{ativo}/projeto/.ativo`** guarda o slug do projeto ativo (igual ao padrão do produto).

**`roteiro.md`** é o briefing. Preencha com:

```markdown
# Projeto: {nome-legivel}

## Objetivo
{objetivo escolhido na pergunta 1}

## Prazo
{resposta da pergunta 2}

## Resultado esperado
{resposta da pergunta 3}

## Produto ativo
- Slug: {ativo}
- Nome: {nome do produto lido do perfil.md}
- Tipo: {tipo lido de tipo.md se existir}

## Contexto do produto
- Quadro: {leia do perfil.md}
- Público principal: {leia do idconsumidor.md se existir}

## Criado em
{data de hoje no formato AAAA-MM-DD}
```

**`plano.md`** começa vazio com cabeçalho:

```markdown
# Plano de execução

Ainda não foi gerado. Use `/toolkit-planejar` para criar o plano em etapas.
```

**`estado.md`** começa assim:

```markdown
# Estado do projeto

- Status: novo
- Etapa atual: aguardando plano
- Última atualização: {data}

## Histórico
- {data}: projeto criado
```

**`pendencias.md`** começa vazio com cabeçalho:

```markdown
# Pendências e ideias soltas

(Nenhuma por enquanto. Use `/toolkit-anotar` para registrar algo.)
```

### 5. Confirmar e sugerir próximo passo

```
Projeto "{nome}" criado e ativado.
Pasta: meus-produtos/{ativo}/projeto/{slug}/

Próximo passo: /toolkit-planejar para gerar o plano em etapas.
```

## Quando usar este comando

USE quando:
- A tarefa tem 3 ou mais etapas distintas
- Vai gerar múltiplos entregáveis que dependem um do outro
- Você precisa manter contexto entre várias sessões
- O pedido é amplo (ex: "planeje meu lançamento", "monta o funil do zero", "reestrutura tudo")

NÃO USE quando:
- É um único entregável (um anúncio, um email, um post)
- É ajuste pontual em algo existente
- É dúvida ou pergunta rápida
- A tarefa cabe numa skill só (`/copy-pagina`, `/ht-pitch-palco`, etc.)

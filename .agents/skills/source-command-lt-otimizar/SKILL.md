---
name: "source-command-lt-otimizar"
description: "Analisar planilhas exportadas do Gerenciador de Anuncios do Meta Ads e recomendar acoes praticas de otimizacao para campanhas de produtos low ticket. Baseado em CPA dos ultimos 7 dias, estrutura CBO/ABO, Advantage+ e volume de compras em 28 dias."
---

# source-command-lt-otimizar

Use esta skill quando o usuário pedir o comando `/lt-otimizar` do workshop (ou `lt-otimizar`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/lt-otimizar.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Otimizador MetaAds Low Ticket

Agente especialista em analise e otimizacao de campanhas de trafego pago para produtos low ticket no Meta Ads. Analisa planilhas exportadas do Gerenciador de Anuncios e recomenda acoes praticas.

## Usage

```
/otimizador-metaads
```

## O Que Fazer

### 1. Contexto

Leia `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme o CLAUDE.md) para saber o valor do produto (se disponivel).
Consulte `.claude/skills/trafego-pago/SKILL.md` para referencia de metricas.

### 2. Coleta de Dados

**Passo 1. Receber a planilha:**

Peca ao usuario para enviar a planilha Excel (.xlsx ou .csv) exportada do Gerenciador de Anuncios do Meta Ads.

```
Para comecar, me envie a planilha exportada do Gerenciador de Anuncios.

Preciso que ela contenha:
- Nome da campanha
- Nome do conjunto de anuncios
- Orcamento
- Valor gasto
- Compras
- CPA (Custo por Aquisicao)
- Dados dos ultimos 7 dias

Pode arrastar o arquivo aqui ou colar o caminho.
```

**Se algum campo estiver ausente:** informar objetivamente qual campo esta faltando e solicitar que o usuario forneca antes de continuar.

**Passo 2. Perguntas obrigatorias (UMA por vez):**

Pergunta 1:
```
Qual e o valor do seu produto low ticket?
(ex: "R$47", "R$97", "R$37")
```

Pergunta 2:
```
No seu Gerenciador de Anuncios, olhando os ultimos 28 dias, quantas compras suas campanhas acumularam no total?

1. Menos de 50 compras
2. 50 ou mais compras

Como verificar: No Gerenciador de Anuncios, mude o periodo para "Ultimos 28 dias" e some a coluna "Compras" de todas as campanhas ativas.

Digite o numero:
```

Pergunta 3:
```
O orcamento das suas campanhas esta configurado a nivel de campanha ou de conjunto?

1. CBO (orcamento a nivel de campanha. o Meta distribui automaticamente entre os conjuntos)
2. ABO (orcamento a nivel de conjunto. voce define quanto cada conjunto gasta)
3. Tenho as duas estruturas

Se nao sabe: abra a campanha no Gerenciador. Se o orcamento aparece na linha da campanha, e CBO. Se aparece na linha de cada conjunto, e ABO.

Digite o numero:
```

Pergunta 4:
```
Voce ja possui alguma campanha Advantage+ (Shopping) ativa?

1. Sim, ja tenho Advantage+ ativa
2. Nao, ainda nao tenho
3. Nao sei o que e isso

Como verificar: No Gerenciador de Anuncios, procure campanhas com o icone de "+" ou o nome "Advantage+ Shopping". Esse tipo de campanha aparece com um layout diferente das campanhas comuns.

Digite o numero:
```

### 3. Calculos Automaticos

Ao receber todas as respostas, calcular:

- **CPA Alvo** = 60% do valor do produto
  - Exemplo: Produto de R$47 → CPA Alvo = R$28,20
- **Classificacao de cada conjunto:**
  - DENTRO DO CPA = CPA dos ultimos 7 dias ≤ CPA Alvo
  - ACIMA DO CPA = CPA dos ultimos 7 dias > CPA Alvo
- **Conjuntos para desativar:** gastaram mais que o valor do produto e nao venderam, OU estao com CPA maior que o valor do produto

### 4. Confirmacao

Antes de gerar o diagnostico, apresentar resumo:

```
Resumo dos dados coletados:

- Produto: [nome]
- Valor do produto: R$[valor]
- CPA Alvo (60%): R$[valor]
- Compras ultimos 28 dias: [menos de 50 / 50+]
- Estrutura: [CBO / ABO / Mista]
- Advantage+ ativa: [Sim / Nao]
- Campanhas analisadas: [quantidade]
- Conjuntos analisados: [quantidade]
- Periodo: Ultimos 7 dias

1. Tudo certo, pode analisar
2. Quero corrigir algo
```

### 5. Geracao. Metodologia de Otimizacao

Analisar SEMPRE com base nos **ultimos 7 dias**. Aplicar as regras abaixo conforme a situacao de cada conjunto.

---

#### CONJUNTOS DENTRO DO CPA (≤ 60% do valor do produto)

**Se a estrutura for CBO:**
- Aumentar 20% do orcamento da campanha
- Desativar anuncios que nao gastaram ou nao performaram
- Subir novos anuncios como Teste A/B a nivel de anuncio

**Se a estrutura for ABO:**
- Aumentar 20% do orcamento do conjunto
- Manter apenas o conjunto que esta performando bem
- Subir novos anuncios como Teste A/B a nivel de anuncio

**Em ambos os casos. Criar nova campanha teste:**
- 1 campanha
- 1 conjunto de anuncios
- Pelo menos 3 criativos com angulos bem diferentes
- Evitar similaridade entre criativos

---

#### CONDICAO ESPECIAL. 50+ Compras nos Ultimos 28 Dias

Aplicar SOMENTE se TODAS as condicoes forem verdadeiras:
1. Conjunto esta dentro do CPA nos ultimos 7 dias
2. Possui mais de 50 compras nos ultimos 28 dias
3. NAO possui campanha Advantage+ ativa

**Acao: Criar campanha Advantage+:**
- 1 campanha
- 1 conjunto de anuncios
- Pelo menos 3 criativos com angulos bem diferentes
- Estrutura: CBO
- Tipo: Advantage+ (Shopping)
- Publico: Sugestao publico comprador + Sugestao publico engajamento
- Orcamento: 50% do valor do produto por dia

---

#### SE JA POSSUI ADVANTAGE+ ATIVA

Nao criar nova campanha Advantage+.
Aplicar a mesma logica de otimizacao da estrutura atual:

- **Se a Advantage+ estiver com CBO:** aumentar 20% do orcamento, desativar anuncios que nao performaram, subir novos anuncios como Teste A/B a nivel de anuncio
- **Se a Advantage+ estiver com ABO:** aumentar 20% do orcamento, manter apenas os conjuntos performando bem, subir novos anuncios como Teste A/B a nivel de anuncio

---

#### CONJUNTOS ACIMA DO CPA (> 60% do valor do produto)

- Reduzir 20% do orcamento

**Regra de desativacao (ultimos 7 dias):**
Desativar conjuntos que:
- Gastaram mais que o valor do produto e nao venderam
- OU estao com CPA maior que o valor do produto

---

### 6. Formato da Resposta

A resposta DEVE seguir esta estrutura exata:

```
DIAGNOSTICO GERAL

Valor do Produto: R$[valor]
CPA Alvo (60%): R$[valor]
Compras ultimos 28 dias: [quantidade ou faixa]
Estrutura atual: [CBO / ABO / Mista]
Possui Advantage+ ativa: [Sim / Nao]
Periodo analisado: Ultimos 7 dias

---

ESCALAR (conjuntos dentro do CPA)

[Para cada conjunto dentro do CPA, listar:]
- Nome do conjunto
- CPA atual: R$[valor]
- Gasto ultimos 7 dias: R$[valor]
- Compras: [numero]
- Acao: [detalhar conforme CBO/ABO]

[Se aplicavel. Nova Campanha Teste:]
- Estrutura recomendada
- Orcamento sugerido
- Orientacao para criativos

[Se aplicavel. Advantage+:]
- Estrutura recomendada
- Orcamento: R$[50% do valor do produto]/dia
- Publicos sugeridos

---

AJUSTAR (conjuntos acima do CPA mas recuperaveis)

[Para cada conjunto acima do CPA mas que ainda tem potencial:]
- Nome do conjunto
- CPA atual: R$[valor]
- Acao: Reduzir 20% do orcamento
- Monitorar por mais [X] dias

---

DESATIVAR (conjuntos para pausar)

[Para cada conjunto que deve ser pausado:]
- Nome do conjunto
- Motivo: [gastou R$X sem venda / CPA R$X acima do valor do produto]
- Acao: Desativar imediatamente

---

PLANO DE ACAO (Passo a Passo)

1. [Primeira acao. ex: "Desativar o conjunto X que gastou R$80 sem nenhuma venda"]
2. [Segunda acao. ex: "Aumentar orcamento da campanha Y de R$30 para R$36 (20%)"]
3. [Terceira acao...]
...

[Numerar todas as acoes em ordem de prioridade: primeiro desativar, depois ajustar, depois escalar]
```

### 7. Regras Inegociaveis

- SEMPRE analisar com base nos ultimos 7 dias
- SEMPRE validar compras dos ultimos 28 dias antes de recomendar Advantage+
- SEMPRE validar se a estrutura e CBO ou ABO. inclusive dentro de campanhas Advantage+
- SEMPRE validar se ja existe Advantage+ ativa antes de sugerir criar uma nova
- NUNCA misturar estrategias de CBO e ABO na mesma recomendacao sem separar claramente
- NUNCA inventar metricas ou dados que nao estejam na planilha
- NUNCA falar teoria. apenas acoes executaveis com nome do conjunto e valores
- Se faltar algum dado na planilha, informar qual campo esta ausente e solicitar ao usuario

### 8. Entrega

Apos apresentar o diagnostico:

```
1. Aprovar e salvar
2. Quero ajustar algo
3. Analisar outra planilha
```

Salvar em: `meus-produtos/{ativo}/entregas/trafego/otimizacao-metaads-[data].md`

Sugerir proximo passo:
- `/copy-anuncio`. para criar novos criativos para os testes recomendados
- `/criativo-estatico` para gerar imagens dos novos anuncios

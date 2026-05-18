---
name: workshop-marketing:criativo-estatico
description: Gera criativo estático de anúncio (imagem) para Instagram. Orquestrador que pergunta o formato e direciona para a sub-skill correspondente. Cobre 4 formatos. Promessa Simples (rápido), Caixinha de Perguntas (15 ideias de pergunta + resposta, escolhe uma), Criativo Surreal (10 ideias surreais com estética editorial Cannes Lions, escolhe uma) e AIDA Completo (fluxo avançado em 3 passos). Em todos, no fim o aluno escolhe gerar a imagem colando o prompt no ChatGPT ou direto pela API. Use sempre que o usuário pedir criativo estático, anúncio em imagem, arte de anúncio, promessa simples, caixinha de perguntas, criativo surreal, anúncio surreal, anúncio AIDA ou variantes desses formatos.
allowed-tools: Read, Write, Bash, WebSearch
---

# Criativo Estático. Orquestrador de Formatos de Anúncio

Gera criativo estático de anúncio. Antes de tudo, pergunta o formato e direciona pra sub-skill correspondente. Cada formato tem fluxo próprio (número de perguntas, geração e saída).

## Usage

```
/criativo-estatico
```

## O Que Fazer

### 0. Contexto

Leia o máximo de contexto disponível sobre o produto ativo. Em ordem:

1. **`meus-produtos/.ativo`** (obrigatório). O slug do produto ativo (ex: `automacoes-inteligentes`).
2. **`meus-produtos/{ativo}/perfil.md`** (se existir). Quadro, Furadeira, Decorados, Identidades, Urgências Ocultas, nicho, público.
3. **`meus-produtos/{ativo}/idconsumidor.md`** (se existir). Identidade do Consumidor com objeções, paliativos, baldes.
4. **`meus-produtos/{ativo}/tipo.md`** (se existir). Tipo do produto (low ticket, mid ticket, high ticket).
5. **`meus-produtos/{ativo}/preco.md`** (se existir). Preço do produto.
6. **`meus-produtos/{ativo}/pesquisa-mercado.md`** (se existir). Pesquisa de mercado do nicho.

Da combinação desses arquivos, extrair pra passar pras sub-skills:

- **Nome do produto**: do `perfil.md` (cabeçalho ou seção "Nome do produto"); se não existir, **inferir do slug** capitalizando e expandindo (ex: `automacoes-inteligentes` vira "Automações Inteligentes", `curso-tarot` vira "Curso de Tarot").
- **Nicho**: do `perfil.md` (seção "Nicho"); se não existir, **inferir do nome inferido + tipo.md + preco.md** (ex: "Automações Inteligentes" + "low ticket" + "R$ 47" sugere nicho "automação com IA pra pequenos negócios").
- **O que o produto ensina ou resolve (Quadro)**: do `perfil.md` (seção "Quadro"); se não existir, **inferir do nome + tipo**.
- **Público**: do `idconsumidor.md` (resumo); se não existir, do `perfil.md` (seção "Para Quem É"); se não existir nenhum dos dois, **inferir do nicho** (ex: nicho "automação com IA pra pequenos negócios" sugere público "donos de pequenos negócios que querem economizar tempo com IA").
- **Tipo**: do `tipo.md` se existir.
- **Preço**: do `preco.md` se existir.

Esse contexto enriquecido (real + inferido) é compartilhado entre as 4 sub-skills. As sub-skills SEMPRE mostram o resumo do contexto ao aluno antes de prosseguir, marcando claramente o que veio do perfil e o que foi inferido, pedindo confirmação ou correção.

**Importante**: o objetivo é NUNCA fazer entrevista do zero quando há contexto disponível. Mesmo com perfil ausente, o slug + tipo + preço já dão pistas suficientes pra montar um chute inicial que o aluno confirma ou ajusta.

### 1. Atalho de roteamento direto (antes de mostrar o menu)

Se a mensagem inicial do aluno mencionar EXPLICITAMENTE o nome do formato, pular o menu e ir direto pra sub-skill correspondente. Termos que disparam o atalho:

| Mensagem do aluno contém | Sub-skill | Arquivo a ler |
|---|---|---|
| "promessa simples", "criativo simples", "anúncio simples", "formato simples" | Promessa Simples | `.claude/commands/criativo-estatico/promessa-simples.md` |
| "caixinha de perguntas", "caixinha", "pergunta e resposta", "anúncio nativo" | Caixinha de Perguntas | `.claude/commands/criativo-estatico/caixinha-de-perguntas.md` |
| "criativo surreal", "anúncio surreal", "surreal", "fora do mundo normal", "metáfora visual", "impacto visual", "editorial", "Cannes Lions" | Criativo Surreal | `.claude/commands/criativo-estatico/criativo-surreal.md` |
| "AIDA", "fluxo completo", "criativo avançado" | AIDA Completo | `.claude/commands/criativo-estatico/aida.md` |

Se não tiver atalho claro, seguir pro Passo 2 (menu).

### 2. Pergunta de roteamento (menu padrão)

Apresente as 4 opções:

```
Qual formato de criativo você quer criar?

1. Promessa Simples
   O tipo mais direto. Gera título, legenda e o prompt da arte.
   Ideal quando você quer rapidez e simplicidade. 3 perguntas curtas.

2. Caixinha de Perguntas
   Simula a caixinha nativa do Instagram. Gera 15 ideias de pergunta + resposta,
   você escolhe a melhor e recebe o prompt da arte.
   Ideal pra anúncio que pareça conteúdo orgânico. 1 pergunta + escolha de ideia.

3. Criativo Surreal
   Forte impacto visual fora do mundo normal (escalas impossíveis, personificações,
   metáforas visuais), com estética editorial publicitária nível Cannes Lions.
   Gera 10 ideias surreais dentro do universo do seu nicho, você escolhe a melhor
   e recebe o prompt da arte. Ideal pra criativo memorável que para o scroll.

4. AIDA Completo
   Fluxo avançado em 3 passos (cena, layout, texto). Ideal pra criativo
   profissional com controle visual total. Mais perguntas e refinamento por passo.

Em qualquer formato, no fim você escolhe gerar a imagem colando o prompt no
ChatGPT (grátis) ou direto pela API (tem custo, salva o arquivo automático).

Digite o número:
```

### 3. Roteamento

Conforme a resposta:

- **1** ou termos relacionados a Promessa Simples: leia `.claude/commands/criativo-estatico/promessa-simples.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **2** ou termos relacionados a Caixinha de Perguntas: leia `.claude/commands/criativo-estatico/caixinha-de-perguntas.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **3** ou termos relacionados a Criativo Surreal: leia `.claude/commands/criativo-estatico/criativo-surreal.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **4** ou termos relacionados a AIDA: leia `.claude/commands/criativo-estatico/aida.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.

O contexto do produto ativo (Passo 0) já está carregado. As sub-skills NÃO precisam ler `perfil.md` e `idconsumidor.md` de novo, podem usar o que já foi extraído.

## Regras

- Nunca pular a pergunta de roteamento, exceto quando o aluno mencionou explicitamente o nome do formato na primeira mensagem (atalho do Passo 1).
- As sub-skills herdam todas as regras globais do CLAUDE.md. Light Copy, auto-revisão obrigatória de copy, anúncio de próximo passo, aprovação antes de salvar, acentuação correta em pt_BR.
- O orquestrador NÃO gera copy nem texto de anúncio. Apenas roteia.
- Cada sub-skill tem fluxo próprio. O orquestrador não define perguntas, opções de saída ou regras de geração. Quem define isso é o arquivo da sub-skill.
- Se o aluno escolher um número inválido (fora de 1 a 4), repetir o menu de forma curta sem mostrar a descrição das opções de novo.
- Se a sub-skill terminar e o aluno quiser criar outro criativo de outro formato, retornar a esta skill (`/criativo-estatico`) em vez de chamar a outra sub-skill direto. O Passo 0 garante contexto fresco.

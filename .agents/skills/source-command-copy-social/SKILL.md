---
name: "source-command-copy-social"
description: "Criar conteúdo para redes sociais. Carrossel, roteiro de Reels e linha editorial de 30 dias. Baseado nas Urgências Ocultas e Decorados do produto ativo."
---

# source-command-copy-social

Use this skill when the user asks to run the migrated source command `copy-social`.

## Command Template

# Conteúdo Social

Cria conteúdo usando Urgências Ocultas como fonte de temas e Light Copy como estilo.

## O Que Fazer

### 1. Contexto

Leia `meus-produtos/{ativo}/perfil.md` e `meus-produtos/{ativo}/idconsumidor.md` se existir.

Extraia internamente: Decorados, Urgências Ocultas (7 categorias, 10 itens cada), Baldes de Conteúdo do idconsumidor.

Verifique conteúdos existentes em `meus-produtos/{ativo}/entregas/criativos/` para evitar repetir urgências já usadas.

### 2. Entrevista (UMA pergunta por vez)

**Bloco 1/3 — Tipo:**

```
O que quer criar?

1. Carrossel (7-10 slides)
2. Roteiro de Reels
3. Linha editorial (30 dias)

Digite o número:
```

**Se escolher Roteiro de Reels — Bloco 1b — Formato:**

```
Qual formato de Reels?

1. Padrão (gancho → tease → entrega → regancho → CTA)
2. DDD Pack (3 Reels prontos: Dor, Dúvida, Desejo)
3. Problema x Solução (1 hook + 5 pares problema→solução + CTA)
4. Pergunta-Resposta-Objeção (7 roteiros, um por categoria de urgência oculta)

Digite o número:
```

**Bloco 2/3 — Rede:**

```
Para qual rede?

1. Instagram
2. TikTok
3. LinkedIn
4. Várias

Digite o número:
```

**Bloco 3/3 — Objetivo** (apenas para formatos 1 e 3; pular se DDD Pack ou Pergunta-Resposta-Objeção, pois o objetivo já está embutido no formato)**:**

```
Objetivo principal?

1. Educar (entregar algo prático)
2. Engajar (gerar comentários e compartilhamentos)
3. Vender (levar para página ou checkout)
4. Atrair seguidores

Digite o número:
```

**Confirmação:**

```
Resumo:
- Tipo: [tipo]
- Formato: [formato, se Reels]
- Rede: [rede]
- Objetivo: [objetivo, se aplicável]
- Base: Urgências Ocultas do perfil

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### 3. Geração por Tipo

**Regras de estilo (aplicar em todo conteúdo):**

Antes de escrever, leia `.Codex/skills/revisora/references/manual-copy.md` e aplique. Toda peça passa pela skill `revisora` antes de ir ao usuário.

- Gancho: afirmação contra-intuitiva, paradoxo ou revelação. NUNCA pergunta.
- Entregar valor real dentro do post: quem lê aprende ou se reconhece.
- Produto não aparece nos primeiros slides ou nos primeiros 3 segundos.
- Uma ideia por post, um CTA por post.
- Sem travessão em nenhuma frase.

---

**Carrossel (7-10 slides):**

- Slide 1: gancho forte (elemento literário + abertura não óbvia)
- Slides 2-8: cada slide avança o argumento com base em Urgência Oculta ou Decorado. Sem slide que parafraseia o anterior.
- Slide final: CTA + branding mínimo
- Caption: mínimo 2 parágrafos de desenvolvimento antes do CTA, com hashtags relevantes

---

**Roteiro de Reels — Formato 1: Padrão (30-60s):**

```
[0-3s]   GANCHO    — Afirmação não óbvia. Texto na tela + fala simultâneos.
[4-15s]  TEASE     — Expande o gancho, contextualiza o problema.
[16-42s] ENTREGA   — Ensina ou revela algo concreto. NUNCA apenas prometer.
[43-48s] REGANCHO  — Texto síntese (âncora para quem assiste sem som).
[49-55s] CTA       — Convite direto e leve.
```

---

**Roteiro de Reels — Formato 2: DDD Pack:**

Gerar 3 roteiros completos em sequência, um por categoria. Cada roteiro segue a mesma estrutura de 3 partes:

- **Gancho:** afirmação contra-intuitiva, direta e curiosa. Nunca pergunta. Para no scroll imediatamente.
- **Desenvolvimento:** ensino prático com exemplos concretos (números, comparações, critérios, erros explicados). Quem lê aprende algo aplicável hoje. Sem texto genérico, sem motivação vazia.
- **CTA:** convidar a seguir o perfil. Nunca vender produto diretamente.

**Roteiro 1 — DOR:**
Mostrar um erro comum que faz o público perder dinheiro, tempo ou energia. Explicar por que acontece. Entregar uma correção prática ou mudança de perspectiva clara.

**Roteiro 2 — DÚVIDA:**
Responder uma pergunta prática e recorrente do público. Comparar opções reais. Ajudar a tomar uma decisão melhor.

**Roteiro 3 — DESEJO:**
Mostrar um cenário possível e realista. Inspirar através de clareza, controle e previsibilidade. Conectar o desejo a método e conhecimento — nunca prometer resultado milagroso.

Usar como fonte as Urgências Ocultas do `perfil.md`: Dores para o roteiro 1, Dúvidas para o roteiro 2, Desejos para o roteiro 3. Verificar em `meus-produtos/{ativo}/entregas/criativos/` quais urgências já foram usadas e priorizar as inéditas.

Entregável: 3 roteiros prontos para gravar, com texto na tela e fala diferenciados quando necessário.

---

**Roteiro de Reels — Formato 3: Problema x Solução:**

Estrutura fixa:

1. **Hook:** 1 frase criativa e direta. Para o scroll. Nunca pergunta.
2. **5 pares Problema → Solução:** cada solução deve ser técnica, específica ou pouco conhecida — valorizada por quem entende do assunto. Evitar soluções óbvias ou genéricas.
3. **CTA:** coerente com o objetivo escolhido (seguir perfil ou próximo passo de venda).

Usar as Urgências Ocultas e Decorados do `perfil.md` para selecionar os 5 problemas mais relevantes para o público. Verificar quais já foram usados em criativos anteriores e priorizar os inéditos.

Entregável: 1 roteiro completo pronto para gravar ou editar como lista animada.

---

**Roteiro de Reels — Formato 4: Pergunta-Resposta-Objeção:**

Gerar 7 roteiros, um por categoria de urgência oculta do `perfil.md`:
1. Dores
2. Dúvidas
3. Desejos
4. Assuntos Relacionados
5. Urgências Quentes
6. Urgências Frias
7. Urgências Inusitadas

Para cada categoria, usar o primeiro item não utilizado e estruturar o roteiro em 4 partes:

- **❓ Pergunta ou pensamento real do público** — linguagem natural, como se a pessoa estivesse desabafando ou pensando consigo mesma. Sem cara de propaganda. Reflete a urgência oculta de forma autêntica.
- **✅ Resposta objetiva e empática** — direta, sem enrolação.
- **🤔 Objeção comum** que o público poderia ter após a resposta.
- **🔨 Quebra da objeção + CTA** — resolve a objeção e convida para o próximo passo (seguir, DM, link na bio).

Verificar em `meus-produtos/{ativo}/entregas/criativos/` quais urgências já foram usadas. Pular as já exploradas e usar a próxima disponível de cada categoria.

Entregável: 7 roteiros completos, um por categoria, prontos para gravar.

---

**Linha editorial (30 dias):**

- Distribuir temas entre as 7 categorias de Urgências Ocultas
- Distribuir nos Baldes de Conteúdo do idconsumidor (se existir)
- Alternar formatos: carrossel, reels, stories, post estático
- CTAs estratégicos progredindo: seguidores, leads, vendas
- Para cada dia: tema, urgência ou decorado de origem, formato e objetivo

### 4. Aprovação e Salvar

Mostrar o conteúdo gerado e perguntar:

```
1. Aprovar e salvar
2. Quero ajustar algo
```

Após aprovação, salvar em:
`meus-produtos/{ativo}/entregas/criativos/[tipo]-[produto].md`

### 5. Próximo Passo

"Use `/criativo` para gerar as artes que acompanham esse conteúdo."

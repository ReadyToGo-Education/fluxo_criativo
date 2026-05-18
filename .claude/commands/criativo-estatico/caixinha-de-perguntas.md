# Caixinha de Perguntas. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 2 (Caixinha de Perguntas). Simula a caixinha nativa do Instagram (balão de pergunta + resposta solta sobre uma foto do nicho). Gera 15 ideias de pergunta + resposta hack, o aluno escolhe uma, e a sub-skill entrega título, legenda e dois prompts prontos pra colar no ChatGPT (Feed e Stories).

**Por que esse formato funciona:**
O criativo parece conteúdo orgânico, não anúncio. A caixinha cinza é um padrão visual nativo que o usuário do Instagram já confia. A resposta hack (contra-intuitiva) gera curiosidade antes de o leitor identificar que é venda.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug, ex: `automacoes-inteligentes` vira "Automações Inteligentes").
- **Nicho**: do `perfil.md` (seção "Nicho") ou inferido do nome + tipo + preço (ex: "automação com IA pra pequenos negócios").
- **Público**: do `idconsumidor.md` ou seção "Para Quem É" do `perfil.md` ou inferido do nicho.

### 1. Apresentar resumo do contexto e confirmar

SEMPRE mostre o resumo, mesmo se algum campo veio de inferência. Marque o que é real e o que foi inferido:

```
Vou usar estes dados do seu produto ativo ({slug}):

Produto: [nome do produto]
Nicho: [nicho]
Público: [resumo do público]

(Marque "✓ do perfil" pros campos extraídos diretamente do perfil.md ou idconsumidor.md.
Marque "○ inferido" pros campos que foram um chute a partir do slug, tipo ou preço.)

Está tudo certo?

1. Sim, está certo, pode seguir
2. Quero ajustar algum campo
```

**Se escolher 1**, pular pra etapa 2 (Geração das 15 perguntas).

**Se escolher 2**, perguntar qual campo ajustar e refazer só a parte indicada.

**Pergunta de ajuste (caso aluno escolha 2)**, com exemplos do nicho do produto ativo:

```
Qual é o seu produto e nicho?
(ex: [3 exemplos do mesmo universo do produto ativo])
```

**IMPORTANTE: os exemplos NUNCA podem ser genéricos.** Antes de fazer a pergunta, construa 3 exemplos do mesmo universo do produto ativo:

- Se o produto for de automação/IA: "Mentoria de Automações com IA pra criadores de conteúdo", "Curso de Agentes GPT pra atendimento", "Treinamento de N8N pra agências"
- Se for de tarot: "Curso de Tarot online pra iniciantes", "Mentoria de Leitura de Cartas pra terapeutas", "Ebook de Tarô pra autoconhecimento"
- Se for de tráfego: "Mentoria de Tráfego Pago pra criadores", "Curso de Anúncios no Meta pra agências", "Consultoria de Performance pra ecommerce"
- Se for de cafeteria: "Consultoria de Cardápio pra donos de cafeteria", "Treinamento de Barista pra equipes", "Curso de Como Abrir uma Cafeteria"
- Último recurso (se realmente não der pra inferir nicho): "Mentoria de tráfego pago pra criadores de conteúdo", "Curso de tarot online pra iniciantes", "Consultoria de cardápio pra donos de cafeteria"

Se o aluno não especificou público, assumir um plausível com base no produto/nicho e avisar antes de gerar as perguntas:

```
Você não especificou o público, então vou assumir: [público assumido]. Se quiser trocar, é só me dizer.
```

### 2. Geração das 15 perguntas + respostas

Anuncie:

```
🔍 Próximo passo: gerar 15 ideias de pergunta + resposta hack do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Gerar 15 perguntas em 3 categorias de 5 cada:

#### 🎯 Oportunidade (5 perguntas)

Pra quem ainda nem está pensando no produto. Atrai pela dor maior do negócio ou da vida (faturamento, ticket médio, resultado, transformação grande).

Exemplos do tom esperado:
- "Como dobrar o faturamento da cafeteria sem aumentar o movimento?"
- "Como conseguir 5 clientes novos por semana sem postar todo dia?"
- "Como vender curso de tarot sem parecer charlatão?"

#### 🍳 Aprofundamento (5 perguntas)

Pra quem já conhece o assunto mas tem dúvida prática. Como executar, qual material, qual horário, como precificar, qual ferramenta usar.

Exemplos do tom esperado:
- "Quantas cartas a leitura de tarot precisa ter no Instagram?"
- "Qual é o melhor horário pra postar carrossel pra donas de pet shop?"
- "Como cobrar uma consultoria de cardápio sem assustar o cliente?"

#### 🚫 Quebra de Objeção (5 perguntas)

Pra quem já considerou mas travou. São objeções reais. A pergunta pode vir como frase entre aspas (a objeção dita pelo próprio público).

Exemplos do tom esperado:
- "Cliente de cafeteria não paga caro." Será mesmo?
- "Não tenho tempo pra postar todo dia, então vai dar certo?"
- "Já tentei tráfego pago e queimei dinheiro, vale tentar de novo?"
- "Meu nicho é diferente, esse método não funciona pra mim, vai?"

#### Regras das perguntas e respostas

- **Nicho explícito em cada pergunta.** Não pode ser genérica. Sempre falar "cafeteria", "tarólogo", "consultoria de cardápio", "carrossel pra pet shop", etc.
- **Perguntas curtas e específicas.** Nada de pergunta longa ou abstrata.
- **Respostas contra-intuitivas.** Hack real, coisa que normalmente a pessoa não sabe. Nunca diquinha boba do tipo "poste todo dia" ou "use hashtag".
- **Respostas curtas.** 1 a 2 linhas no máximo. Direto ao ponto.
- **Em Quebra de Objeção**, formato pode ser: aspas com a objeção + frase curta de provocação ("Será mesmo?", "Tem certeza?", "Quanto seu concorrente cobra?").

#### Apresentação

Mostre todas as 15 numeradas de 1 a 15, separadas pelas 3 categorias:

```
Aqui estão 15 ideias de pergunta + resposta hack pro seu nicho.

🎯 OPORTUNIDADE

1. P: [pergunta 1]
   R: [resposta hack 1]

2. P: [pergunta 2]
   R: [resposta hack 2]

3. P: [pergunta 3]
   R: [resposta hack 3]

4. P: [pergunta 4]
   R: [resposta hack 4]

5. P: [pergunta 5]
   R: [resposta hack 5]

🍳 APROFUNDAMENTO

6. P: [pergunta 6]
   R: [resposta hack 6]

7. P: [pergunta 7]
   R: [resposta hack 7]

8. P: [pergunta 8]
   R: [resposta hack 8]

9. P: [pergunta 9]
   R: [resposta hack 9]

10. P: [pergunta 10]
    R: [resposta hack 10]

🚫 QUEBRA DE OBJEÇÃO

11. P: [pergunta 11 ou objeção entre aspas]
    R: [resposta hack 11]

12. P: [pergunta 12]
    R: [resposta hack 12]

13. P: [pergunta 13]
    R: [resposta hack 13]

14. P: [pergunta 14]
    R: [resposta hack 14]

15. P: [pergunta 15]
    R: [resposta hack 15]

---
Qual número você quer transformar em criativo?
```

### 3. Escolha e geração do criativo

Após o aluno escolher um número de 1 a 15, anuncie:

```
🔍 Próximo passo: gerar título, legenda e prompts pro ChatGPT. Tempo estimado: cerca de 30 segundos.
```

Gere quatro coisas a partir da pergunta + resposta escolhida:

#### A) Título do anúncio

Direto, conectado à pergunta escolhida. Light Copy aplicada.

Regras obrigatórias:
- Sem travessão (—)
- Sem exclamação (!)
- Sem pergunta no título (a pergunta vai estar na arte, o título tem outro papel)
- Sem promessa vaga
- Sem "não é X. É Y."
- Produto não aparece no lead
- Linguagem que a pessoa usaria com uma amiga

#### B) Legenda pro Instagram

2 a 3 linhas. Gera curiosidade sem entregar a resposta toda. Termina com **"Link na bio"**. Light Copy aplicada.

#### C) Prompt pro ChatGPT (formato Feed)

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

Os placeholders são:
- `[público específico]`: tag de público (ex: "donos de cafeteria", "tarólogas", "criadores de conteúdo"). Sempre específica, nunca genérica como "empreendedores".
- `[pergunta escolhida]`: a pergunta exata do número escolhido (mantendo formato, se for objeção entre aspas mantém aspas).
- `[resposta hack]`: a resposta exata do número escolhido.
- `[descrição da imagem do nicho]`: 4 a 6 referências visuais concretas do universo do nicho (ex: "cartas de tarot espalhadas, mesa mística, velas, cristais, panos rendados"; "toast bonito, mesa de café da manhã, cafeteria aconchegante, xícara de cerâmica, croissant"; "notebook aberto, gráfico de tráfego na tela, café ao lado, mesa de home office organizada").

````
Cria pra mim uma arte de um anúncio no formato de caixinha de perguntas do Instagram. Tem que parecer nativo, igualzinho à caixinha que aparece nos Stories.

No topo da arte, coloca uma tag pequena e discreta indicando o público: "Pra [público específico]". Pode ser tipo um selo, etiqueta ou pílula com design bonito.

Logo abaixo, a caixinha de pergunta nativa do Instagram (balão cinza claro), com a pergunta: "[pergunta escolhida]"

A resposta vem solta sobre a imagem, sem caixa de fundo, sem balão, só o texto sobre a foto: "[resposta hack]"

Embaixo da resposta, um botão pequeno e discreto, com design elegante, escrito "Clica aqui pra aprender". Não pode ser grande nem chamativo demais, esse botão tem que ser sutil.

A imagem de fundo tem que ser nítida, bem visível, com tema do nicho ([descrição da imagem do nicho]). Sem desfoque pesado.

Fonte grande, legível em tela de celular. Nada de fonte pequena.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Do NOT create 9:16 story composition. Composition must be optimized for feed posts and carousels. Shorter vertical framing. Exact size reference: 1080x1350.
````

#### D) Prompt pro ChatGPT (formato Stories)

Esse é fixo. Não precisa preencher placeholders.

````
Agora cria a exata mesma arte, mesmas cores, mesmo texto, mesmo visual, mesmos elementos, só diagramada pro formato Stories.

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Must occupy entire smartphone screen vertically. Exact size reference: 1080x1920.
````

### 4. Auto-revisão obrigatória

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) no título e na legenda. Corrigir direto. Nunca mostrar versão bruta.

A pergunta + resposta NÃO precisam de revisão da revisora (são conteúdo do nicho com tom específico), mas devem respeitar Light Copy nas regras do Passo 2.

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo Caixinha de Perguntas:

📌 PERGUNTA + RESPOSTA ESCOLHIDA (nº {numero})
P: [pergunta]
R: [resposta hack]

📌 TÍTULO DO ANÚNCIO
[título gerado]

📝 LEGENDA PRO INSTAGRAM
[legenda gerada terminando em "Link na bio"]

🎨 PROMPT PRO CHATGPT, FORMATO FEED
[prompt Feed preenchido, dentro de bloco de código]

📱 PROMPT PRO CHATGPT, FORMATO STORIES
[prompt Stories, dentro de bloco de código]

---
1. Aprovar e salvar
2. Quero ajustar algo
3. Voltar e escolher outra pergunta (das 15)
```

Se escolher 2, perguntar o que ajustar (título, legenda, descrição visual do nicho ou tag de público) e refazer apenas a parte indicada.

Se escolher 3, apresentar a lista das 15 perguntas novamente e perguntar o novo número.

### 6. Gerar e salvar

Após a aprovação, pergunte como o aluno quer gerar a imagem:

```
Como você quer gerar a imagem?

1. Colar no ChatGPT ou Gemini (grátis)
   Eu te entrego os prompts prontos. Você cola, gera as artes e salva.

2. Gerar agora pela API (tem custo)
   Eu mando o prompt direto pro modelo de imagem e já salvo o PNG na sua
   pasta. Custa centavos por imagem.

Digite o número:
```

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-caixinha-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-caixinha-{numero}.md`

Conteúdo do arquivo:

```markdown
# Caixinha de Perguntas nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Pergunta + Resposta escolhida (nº {numero_pergunta} das 15)

**P:** [pergunta escolhida]
**R:** [resposta hack]

## Título do anúncio

[título]

## Legenda pro Instagram

[legenda terminando em "Link na bio"]

## Prompt pro ChatGPT. Formato Feed (1080x1350, 4:5)

\`\`\`
[prompt Feed preenchido]
\`\`\`

## Prompt pro ChatGPT. Formato Stories (1080x1920, 9:16)

\`\`\`
[prompt Stories]
\`\`\`

## Como usar

1. Abra o ChatGPT (com geração de imagem habilitada).
2. Cole o **Prompt Feed** e espere a arte ser gerada.
3. Quando estiver pronto, mande "ok" no chat.
4. Cole o **Prompt Stories** pra gerar a versão vertical da mesma arte.

## Banco completo (as 15 ideias geradas nesta sessão)

[opcional: listar as 15 perguntas geradas, pra o aluno usar depois sem precisar rodar a sub-skill de novo]
```

### 6b. Modo API (só se o aluno escolheu a opção 2)

Depois de salvar o `.md`, gere a imagem pela API:

1. Leia `OPENROUTER_API_KEY` no `.env`. Se faltar, ofereça configurar com o `/configurar-imagens` ou voltar pro modo ChatGPT.

2. Pergunte o modelo:

```
Qual modelo de imagem?

1. GPT Image 2 (recomendado)
   Cerca de US$ 0,05 por imagem.
2. Gemini Nano Banana 2
   Cerca de US$ 0,07 por imagem.

Digite o número:
```

Opção 1 vira `openai/gpt-5.4-image-2`, opção 2 vira `google/gemini-3.1-flash-image-preview`.

3. Pergunte o formato:

```
Qual formato você quer gerar?

1. Feed (4:5)
2. Stories (9:16)
3. Os dois

Digite o número:
```

4. Para cada formato escolhido, grave o prompt num arquivo `.txt` na pasta de criativos:
   - Feed: o conteúdo é o Prompt Feed. Proporção `4:5`.
   - Stories: o conteúdo é o Prompt Feed mais a linha abaixo colada no fim. Proporção `9:16`. Não use o Prompt Stories do modo ChatGPT, que depende da imagem anterior e não funciona numa chamada isolada.

   Linha de adaptação para Stories (colar no fim do prompt):
   `FORMAT OVERRIDE: render this exact creative recomposed for a vertical 9:16 Instagram Stories canvas (1080x1920). Keep the same scene, text, colors and elements, only recompose the framing to fill the full vertical screen.`

5. Anuncie e rode o script, um comando por formato:

```
🔍 Próximo passo: gerar a imagem do criativo via API. Tempo estimado: cerca de 1 minuto.
```

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-caixinha-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-caixinha-{numero}-feed.png"
```

Para Stories, troque `feed` por `stories` no nome dos arquivos e `4:5` por `9:16`.

6. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Caixinha de Perguntas salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-caixinha-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

**No modo API:**

```
✅ Concluído: criativo Caixinha de Perguntas gerado e salvo.

Imagem: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-caixinha-{numero}-feed.png
(mais a versão Stories, se o aluno pediu)
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-caixinha-{numero}.md
```

Depois, nos dois modos, ofereça:

```
Quer fazer mais alguma coisa?
1. Gerar outra Caixinha de Perguntas com outra das 15 ideias
2. Trocar o nicho ou público e gerar 15 ideias novas
3. Voltar e escolher outro formato (Promessa Simples, Criativo Surreal ou AIDA Completo)
```

## Regras

- Light Copy obrigatória no título e na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- Produto NÃO aparece no lead do título nem da legenda.
- A pergunta + resposta seguem regras próprias (nicho explícito, contra-intuitiva, curta) e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira, como se estivesse pedindo pra um designer do lado.
- Tag de público no topo da arte sempre específica: "Pra donos de cafeteria", "Pra tarólogas", "Pra criadores de conteúdo". Nunca genérica tipo "Pra empreendedores".
- Descrição da imagem do nicho dá referências visuais concretas (4 a 6 elementos), sem desfoque pesado, fundo nítido.
- Botão "Clica aqui pra aprender" é pequeno e discreto. Nunca grande ou chamativo.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 15 perguntas. Não travar o fluxo.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).

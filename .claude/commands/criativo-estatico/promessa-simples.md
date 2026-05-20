# Promessa Simples. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 1 (Promessa Simples). Formato mais direto e simples que existe. Gera título do anúncio, legenda pro Instagram e dois prompts prontos pra colar no ChatGPT (Feed e Stories).

**Por que esse formato funciona:**
A maioria dos anúncios falha por excesso de copy. Promessa Simples inverte isso: pouco texto na arte, mensagem direta, sem rebuscar. É a base mais limpa pra testar uma promessa antes de complicar o criativo.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto (sem orquestrador), carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia os 3 campos da Promessa Simples (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug capitalizando, ex: `automacoes-inteligentes` vira "Automações Inteligentes").
- **O que ensina/resolve**: Quadro do `perfil.md` ou inferido do nome + tipo + preço (ex: "Automações Inteligentes" + low ticket + R$ 47 sugere "Como automatizar tarefas do seu negócio com IA").
- **Público**: do `idconsumidor.md` ou da seção "Para Quem É" do `perfil.md` ou inferido do nicho (ex: "Donos de pequenos negócios que querem economizar tempo com IA").

### 1. Apresentar resumo do contexto e confirmar

SEMPRE mostre o resumo, mesmo se algum campo veio de inferência. Marque claramente o que é real (do perfil) e o que foi inferido (chute baseado em pistas):

```
Vou usar estes dados do seu produto ativo ({slug}):

Produto: [nome do produto]
O que ensina/resolve: [Quadro real ou inferido]
Público: [público real ou inferido]

(Marque "✓ do perfil" pros campos extraídos diretamente do perfil.md ou idconsumidor.md.
Marque "○ inferido" pros campos que foram um chute a partir do slug, tipo ou preço.)

Está tudo certo?

1. Sim, está certo, pode seguir
2. Quero ajustar algum campo
```

**Se escolher 1**, pular pra etapa 3 (Geração).

**Se escolher 2**, perguntar qual campo ajustar e fazer entrevista parcial só dos campos que o aluno quer mudar. Use o Passo 2 (Entrevista) abaixo como referência das perguntas.

### 2. Entrevista parcial (só pros campos que o aluno quer ajustar)

Acionada apenas pelo "Quero ajustar algum campo" da etapa 1. Faça UMA pergunta por vez, só dos campos sinalizados.

**IMPORTANTE: os exemplos das perguntas devem ser do nicho do produto ativo, NUNCA genéricos.** Antes de fazer a pergunta, identifique o nicho do produto (a partir do contexto do Passo 0) e construa 3 exemplos do mesmo universo. Se realmente não conseguir inferir nicho nenhum, use os exemplos genéricos abaixo como último recurso.

**Pergunta sobre Produto:**

```
Qual é o seu produto?
(ex: [3 exemplos do nicho do produto ativo])
```

Exemplos por nicho (referência interna pra você construir):
- Automação/IA: "Curso de Automações com IA pra Negócios", "Mentoria de Agentes GPT", "Treinamento de N8N pra Iniciantes"
- Tarot: "Curso de Tarot Online", "Mentoria de Leitura de Cartas", "Ebook de Tarô pra Iniciantes"
- Tráfego: "Mentoria de Tráfego Pago", "Curso de Anúncios no Meta", "Consultoria de Performance"
- Cafeteria: "Consultoria de Cardápio pra Cafeterias", "Treinamento de Barista", "Curso de Como Abrir uma Cafeteria"
- Alimentação saudável / meal prep / nutrição: "Curso de Meal Prep Semanal", "Ebook de Marmitas Fit pra Rotina", "Mentoria de Reeducação Alimentar pra Quem Tem Pouco Tempo"
- Genérico (último recurso): "Curso de Inglês Fluente", "Mentoria de tráfego pago", "Ebook de Receitas Low Carb"

**Pergunta sobre o que ensina/resolve:**

```
O que ele ensina ou resolve?
(ex: [3 exemplos do nicho])
```

Construa exemplos no padrão "Como [verbo de resultado] [resultado específico] [prazo ou modo]". Sempre alinhado ao nicho.

**Pergunta sobre o público:**

```
Pra quem é?
(ex: [3 exemplos do nicho])
```

Exemplos sempre do universo do produto, nunca genéricos. Se o produto é automação com IA, exemplos: "Donos de pequenos negócios", "Coaches que querem escalar atendimento", "Agências que perdem tempo com tarefas repetitivas".

### 3. Geração

Anuncie:

```
🔍 Próximo passo: gerar título, legenda e prompts pro ChatGPT. Tempo estimado: cerca de 30 segundos.
```

Gere quatro coisas:

#### A) Título do anúncio

Simples e direto. Light Copy aplicada.

Regras obrigatórias:
- Sem travessão (—)
- Sem exclamação (!)
- Sem pergunta
- Sem promessa vaga (incluir dado, prazo ou situação concreta)
- Sem "não é X. É Y."
- Produto não aparece no lead (nada de "curso", "treinamento", nome do método)
- Linguagem que a pessoa usaria com uma amiga

#### B) Legenda pro Instagram

Simples e direta. Poucas linhas (2 a 5 linhas no máximo). Light Copy aplicada. Termina com chamada pra ação clara mas sem "link na bio" se não for de captação.

#### C) Prompt pro ChatGPT (formato Feed)

Usar o template abaixo, substituindo todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

````
Cria pra mim uma arte de um anúncio do [nome do produto], que ensina [o que ensina/resolve]. É pra [público]. Cria a copy, o texto e o layout. Faz bonito e simples. Não coloca preço na arte. Usa pouco texto na arte, no máximo uns 80 caracteres no total. Anúncio com muito texto fica ruim. Usa fonte grande, legível em tela de celular. O texto tem que ser lido facilmente mesmo num feed pequeno. Nada de fonte pequena.

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

### 5. Apresentação e aprovação

Mostre tudo junto:

```
Pronto. Aqui está o seu Promessa Simples:

📌 TÍTULO DO ANÚNCIO
[título gerado]

📝 LEGENDA PRO INSTAGRAM
[legenda gerada]

🎨 PROMPT PRO CHATGPT, FORMATO FEED
[prompt Feed preenchido, dentro de bloco de código]

📱 PROMPT PRO CHATGPT, FORMATO STORIES
[prompt Stories, dentro de bloco de código]

---
1. Aprovar e salvar
2. Quero ajustar algo
```

Se escolher 2, pergunte o que ajustar (título, legenda ou os dois) e refaça apenas a parte indicada.

### 6. Gerar e salvar

Após a aprovação, pergunte como o aluno quer gerar a imagem:

```
Como você quer gerar a imagem?

1. Colar no ChatGPT ou Gemini (grátis)
   Eu te entrego os prompts prontos. Você cola, gera as artes e salva.

2. Gerar agora pelo OpenRouter (tem custo)
   Eu mando o prompt direto pro modelo de imagem e já salvo o PNG na sua
   pasta. Custa centavos por imagem.

Digite o número:
```

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes na pasta `meus-produtos/{ativo}/entregas/criativos/` (procurar arquivos `criativo-promessa-simples-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-promessa-simples-{numero}.md`

Conteúdo do arquivo:

```markdown
# Promessa Simples nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**O que ensina/resolve:** [o que ensina/resolve]
**Público:** [público]

## Título do anúncio

[título]

## Legenda pro Instagram

[legenda]

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
```

### 6b. Modo API (só se o aluno escolheu a opção 2)

Depois de salvar o `.md`, gere apenas a imagem do Feed pela API. A versão Stories sai depois, como opção no menu do Passo 7, reaproveitando a imagem do Feed como referência visual.

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

Opção 1 vira `openai/gpt-5.4-image-2`, opção 2 vira `google/gemini-3.1-flash-image-preview`. Guarde o modelo escolhido, ele vai ser reaproveitado se o aluno pedir Stories no Passo 7.

3. Grave o Prompt Feed num arquivo `.txt` na pasta de criativos. Conteúdo é o Prompt Feed apresentado ao aluno, sem alterações.

4. Anuncie e rode o script no formato Feed (4:5):

```
🔍 Próximo passo: gerar a imagem do Feed via API. Tempo estimado: 2 a 3 minutos.
```

Use o comando Python correto da sessão (`python3` ou `py -3`), conforme a seção Execução de Scripts Python do CLAUDE.md.

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-promessa-simples-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-promessa-simples-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Promessa Simples salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-promessa-simples-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

Depois ofereça o menu padrão (3 opções):

```
Quer ajustar algo?
1. Refazer o título
2. Refazer a legenda
3. Trocar o produto, ensina/resolve ou público (refazer tudo)
4. Voltar e escolher outro formato
```

**No modo API:**

```
✅ Concluído: criativo Promessa Simples gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-promessa-simples-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-promessa-simples-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Refazer o título
3. Refazer a legenda
4. Trocar o produto, ensina/resolve ou público (refazer tudo)
5. Voltar e escolher outro formato
```

#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-promessa-simples-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-promessa-simples-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-promessa-simples-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-promessa-simples-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-promessa-simples-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções (com a primeira agora marcada como "Gerar novamente o Stories" se aluno quiser refazer).

## Regras

- Light Copy obrigatória no título e na legenda. Sem travessão, sem exclamação, sem pergunta, sem promessa vaga, sem "não é X. É Y.".
- Produto NÃO aparece no lead do título nem da legenda. Nada de "curso", "treinamento", nome do método ou sigla do programa no começo da copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar.
- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira, como se estivesse pedindo pra um designer do lado. Nada técnico, nada rebuscado.
- Nunca colocar preço na arte. Esse limite já está no template.
- A arte deve ter pouco texto, no máximo 80 caracteres no total. Esse limite já está no template.
- Os dois formatos (Feed e Stories) são a exata mesma arte, só rediagramada. O template do Stories já garante isso.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).

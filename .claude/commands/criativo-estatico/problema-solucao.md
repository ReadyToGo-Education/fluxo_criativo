# Problema-Solução. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 7 (Problema-Solução). Gera uma arte dividida verticalmente ao meio: do lado esquerdo o problema real do nicho, do lado direito a solução prática (uma ação concreta, não uma explicação). Gera 10 ideias de problema mais solução, o aluno escolhe uma, e a sub-skill entrega título, legenda e dois prompts prontos pra colar no ChatGPT (Feed e Stories).

**Por que esse formato funciona:**
A estética é de um post real de creator brasileiro, não de banner publicitário, então o leitor baixa a guarda. A divisão visual ao meio comunica a transformação antes de o leitor ler o texto: o olho bate e já entende a mudança. A solução é uma ação concreta e contra-intuitiva, o que gera o "uau, eu nunca tinha pensado nisso" que sustenta o clique.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug, ex: `automacoes-inteligentes` vira "Automações Inteligentes").
- **Nicho**: do `perfil.md` (seção "Nicho") ou inferido do nome + tipo + preço.
- **Público**: do `idconsumidor.md` ou seção "Para Quem É" do `perfil.md` ou inferido do nicho.
- **Quadro / promessa**: a transformação principal do `perfil.md`, pra alimentar o CTA (o CTA sempre carrega o benefício específico do produto).
- **Método / abordagem do produto**: o nome e o vocabulário do método da Furadeira do `perfil.md`, se houver (estoicismo, neurociência, BLW, IA, Feng Shui, etc.). Esse dado é crítico, porque as soluções das 10 ideias DEVEM usar o vocabulário e os frameworks do método do produto. Se o produto tem abordagem específica, as soluções precisam invocá-la.

### 1. Apresentar resumo do contexto e confirmar

SEMPRE mostre o resumo, mesmo se algum campo veio de inferência. Marque o que é real e o que foi inferido:

```
Vou usar estes dados do seu produto ativo ({slug}):

Produto: [nome do produto]
Nicho: [nicho]
Público: [resumo do público]
Método / abordagem: [método do produto, se houver]

(Marque "✓ do perfil" pros campos extraídos diretamente do perfil.md ou idconsumidor.md.
Marque "○ inferido" pros campos que foram um chute a partir do slug, tipo ou preço.)

Está tudo certo?

1. Sim, está certo, pode seguir
2. Quero ajustar algum campo
```

**Se escolher 1**, pular pra etapa 2 (Geração das 10 ideias).

**Se escolher 2**, perguntar qual campo ajustar e refazer só a parte indicada.

**Pergunta de ajuste (caso aluno escolha 2)**, com exemplos do nicho do produto ativo:

```
Qual é o seu produto e nicho?
(ex: [3 exemplos do mesmo universo do produto ativo])
```

**IMPORTANTE: os exemplos NUNCA podem ser genéricos.** Antes de fazer a pergunta, construa 3 exemplos do mesmo universo do produto ativo:

- Se o produto for de automação/IA: "Mentoria de Automações com IA pra criadores de conteúdo", "Curso de Agentes GPT pra atendimento", "Treinamento de N8N pra agências"
- Se for de introdução alimentar: "Curso de Introdução Alimentar pra mães de primeira viagem", "Mentoria de BLW pra famílias", "Ebook de Cardápio Infantil pra bebês de 6 meses"
- Se for de relacionamento: "Curso de Como Esquecer o Ex pra mulheres", "Mentoria de Autoestima pós-término", "Programa de Recomeço Amoroso"
- Se for de tráfego: "Mentoria de Tráfego Pago pra criadores", "Curso de Anúncios no Meta pra agências", "Consultoria de Performance pra ecommerce"
- Se for de cafeteria: "Consultoria de Cardápio pra donos de cafeteria", "Treinamento de Barista pra equipes", "Curso de Como Abrir uma Cafeteria"
- Último recurso (se realmente não der pra inferir nicho): "Mentoria de tráfego pago pra criadores de conteúdo", "Curso de introdução alimentar pra mães", "Consultoria de cardápio pra donos de cafeteria"

Se o aluno não especificou público, assumir um plausível brasileiro com base no produto/nicho e avisar antes de gerar as ideias:

```
Você não especificou o público, então vou assumir: [público assumido]. Se quiser trocar, é só me dizer.
```

### 2. Geração das 10 ideias

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias de problema mais solução do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Gere 10 ideias de Problema → Solução numa lista única numerada de 1 a 10.

Apresente SOMENTE problema e solução em texto. **Não descreva fotos ou cenas visuais na listagem.** As descrições visuais só entram quando o aluno escolher o número.

#### Regras dos Problemas

- **Em primeira pessoa.** Tom de pensamento real da pessoa, não frase publicitária. Tipo "Mando mensagem pro meu ex toda madrugada", "Tenho medo do meu bebê engasgar e travo de oferecer comida".
- **Específicos do público real.** Devem soar como coisa que a pessoa diria pra uma amiga próxima, com contradição, vergonha, especificidade. Não pode ser genérico.
- **Cobrem variações reais do público.** Cada um dos 10 problemas representa uma situação diferente que a pessoa do nicho realmente vive.

#### Regras das Soluções

- **AÇÃO PRÁTICA CONCRETA**, não explicação do mecanismo. A solução tem que dizer O QUE FAZER, não "se acalma, é normal" ou "entende que é fase". Exemplos válidos: "Aplique a regra das 15 exposições", "Corte alimentos redondos em quatro partes e use o teste do dedo", "Faça o exercício estoico da visão de cima: liste o que era ruim e releia toda manhã".
- **Contra-intuitivas e técnicas.** A pessoa lê e pensa "uau, eu nunca tinha pensado nisso assim". Se houver framework, técnica, método ou ferramenta do nicho/produto (estoicismo, neurociência, BLW, IA, Feng Shui, etc.), usa o vocabulário específico.
- **Coerentes com o contexto/método do produto.** Se o produto ensina técnicas de neurociência e filosofia estoica, as soluções têm que invocar esses frameworks. Se ensina introdução alimentar, as soluções têm que ser técnicas práticas de introdução alimentar. Use o método/abordagem do produto extraído no Passo 0 pra guiar as soluções.
- **NÃO usar travessão.** Nem "—" nem "–". Usar vírgula, ponto final ou parênteses no lugar. Travessão é vício de IA e mata a autenticidade.

#### Formato da listagem

```
Aqui estão 10 ideias de problema mais solução pro seu nicho.

**1.**
**Problema:** "[frase em primeira pessoa]"
**Solução:** "[ação prática concreta]"

**2.**
**Problema:** "[frase em primeira pessoa]"
**Solução:** "[ação prática concreta]"

...

**10.**
**Problema:** "[frase em primeira pessoa]"
**Solução:** "[ação prática concreta]"

---
Qual número você quer transformar em criativo?

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.
```

### 3. Escolha e geração do criativo

Após o aluno escolher um número de 1 a 10, anuncie:

```
🔍 Próximo passo: gerar título, legenda e prompts pro ChatGPT. Tempo estimado: cerca de 30 segundos.
```

#### Construir o contraste visual

Antes de gerar o prompt visual, **construa o contraste visual específico desse problema e dessa solução**. O contraste DEVE SAIR DO CONTEÚDO da ideia escolhida, não copiar exemplos hipotéticos.

Regra do contraste:
- O lado do problema mostra a pessoa VIVENDO a situação descrita no texto do problema (linguagem corporal, expressão, contexto material da dor).
- O lado da solução mostra a pessoa APLICANDO a solução descrita no texto (a ação concreta da solução em execução visual).
- A diferença visual entre os dois lados tem que comunicar a transformação ANTES o usuário ler o texto. Olho bate, entende a mudança.

Exemplo de raciocínio (medo de engasgo → corte + teste do dedo):
- Problema: mãe encolhida, expressão de pânico, segurando bebê afastado de prato com alimentos mal cortados (banana inteira, pedaços redondos grandes). Linguagem corporal de proteção/medo.
- Solução: mãe demonstrando claramente o teste do dedo sobre o prato, alimentos cortados em quatro partes longitudinais e tiras finas, bebê comendo com autonomia. Mãe calma, presente.

Gere quatro coisas a partir da ideia escolhida:

#### A) Título do anúncio

Conectado direto à solução, objetivo, sem floreio. Light Copy aplicada.

Regras obrigatórias:
- Sem travessão (—)
- Sem exclamação (!)
- Sem pergunta no título
- Sem promessa vaga (incluir dado, prazo ou situação concreta)
- Sem "não é X. É Y."
- Produto não aparece no lead
- Linguagem que a pessoa usaria com uma amiga

#### B) Legenda pro Instagram

2 a 3 linhas. Conecta com a solução, gera curiosidade sem entregar a solução toda. Termina com **"Link na bio"**. Light Copy aplicada.

#### C) Prompt pro ChatGPT (formato Feed)

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

````
Cria pra mim uma arte de anúncio pra Instagram no formato problema-solução. Estética nativa de UGC, foto que parece tirada por uma pessoa real no celular, dentro de casa, brasileira comum. Não é fotografia editorial, não é estúdio. É vibe de Instagram de pessoa normal.

A arte é dividida verticalmente ao meio por UMA LINHA BRANCA SÓLIDA E VISÍVEL no centro, separando claramente os dois lados.

Mesma pessoa nas duas cenas (e qualquer outro personagem recorrente, como bebê, criança ou animal), mas CENAS COM CONTRASTE VISUAL FORTE. [DESCRIÇÃO DO AVATAR BRASILEIRO REAL: idade, cabelo, estilo, contexto.]

LADO ESQUERDO (Problema):
Cena específica do problema: [DESCRIÇÃO VISUAL DETALHADA QUE MOSTRA A PESSOA VIVENDO O PROBLEMA, com linguagem corporal, expressão e contexto material da dor. Ambiente real brasileiro de classe média, iluminação coerente com o estado emocional.]

Próximo ao texto principal do lado esquerdo, uma tarjinha pequena estilo adesivo de Instagram: retângulo VERMELHO com cantos arredondados, leve sombra por baixo, ligeiramente inclinada uns 5 a 8 graus pra parecer colada no Instagram pelo criador. Texto da tarja: "PROBLEMA" em branco, sans-serif bold.

Bem perto da tarja vermelha, um emoji grande de ALERTA (⚠️), posicionado como adesivo independente, parecendo colado no Instagram pelo criador. Tamanho visível, com leve inclinação pra ter cara de adesivo.

Logo abaixo da tarja e do emoji, o texto principal do problema, em primeira pessoa, fonte sans-serif moderna bold pra ter nitidez: "[TEXTO DO PROBLEMA]"

LADO DIREITO (Solução):
Cena específica da solução: [DESCRIÇÃO VISUAL DETALHADA QUE MOSTRA A PESSOA APLICANDO A SOLUÇÃO, com a ação concreta em execução. Ambiente real, atmosfera de domínio/calma/resolução, coerente com a transformação.]

Próximo ao texto principal do lado direito, uma tarjinha pequena estilo adesivo de Instagram: retângulo VERDE com cantos arredondados, leve sombra, ligeiramente inclinada uns 5 a 8 graus no sentido oposto à do problema. Texto da tarja: "SOLUÇÃO" em branco, sans-serif bold.

Bem perto da tarja verde, um emoji grande de JOINHA (👍), posicionado como adesivo independente, parecendo colado no Instagram pelo criador. Tamanho visível, com leve inclinação pra ter cara de adesivo.

Logo abaixo da tarja e do emoji, o texto principal da solução, sans-serif moderna bold: "[TEXTO DA SOLUÇÃO]"

Os textos principais precisam de nitidez máxima, fonte sólida, contraste alto contra a foto. Se o fundo da foto for claro, texto em preto sólido. Se for escuro, texto em branco sólido. Pode ter um leve fundo semi-transparente atrás do texto pra garantir leitura, mas sutil, sem virar caixa de banner.

PROIBIDO usar travessão (nem o "—" nem o "–") em nenhum texto da arte. Use vírgula ou ponto final no lugar.

SETA NO MEIO:
Uma seta horizontal sólida apontando do lado esquerdo pro lado direito, posicionada centralizada por cima da linha branca divisora. Estilo "stitch do Instagram", seta com cara de elemento gráfico de creator (linha sólida, sem degradê, ponta de flecha simples e marcante, levemente desenhada à mão como se adicionada por um app de edição estilo CapCut ou InShot). Personalidade de creator, não de design publicitário.

CTA:
Botão CTA bem visível e evidente. Cor LARANJA sólido (fundo laranja vivo padrão), texto branco em sans-serif bold, cantos arredondados, com presença clara: "[CTA COM A PROMESSA DO PRODUTO] →". Tem que ser claramente clicável.

POSICIONAMENTO: TODOS OS ELEMENTOS (tarjas, emojis, textos, seta, botão CTA) DEVEM SUBIR um pouco do rodapé. Deixa margem generosa entre o botão CTA e a borda inferior da arte (mínimo 8-10% da altura), pra não correr risco de corte quando o Instagram exibir o anúncio. Mesmo respeito de margem no topo.

Tipografia geral: sans-serif moderna padrão de creator de Instagram (estilo Inter, Helvetica Neue), direta e legível. Bold pros textos principais. Não pode ter cara editorial pesada.

Fonte grande, legível em celular. Hiperrealismo fotográfico, pele real, expressão real, cenário real, sem 3D, sem cartoon, sem filtro de banco de imagem. Tem que parecer foto de Instagram de pessoa comum brasileira, não produção publicitária.

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

O texto do problema, o texto da solução e o CTA NÃO passam pela revisora (são conteúdo da arte com tom específico), mas devem respeitar Light Copy: sem travessão, sem exclamação, e a solução é sempre uma ação concreta, nunca uma explicação do mecanismo.

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo Problema-Solução:

📌 PROBLEMA + SOLUÇÃO ESCOLHIDA (nº {numero_ideia} das 10)
Problema: [texto do problema]
Solução: [texto da solução]

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
3. Voltar e escolher outra ideia (das 10)
```

Se escolher 2, perguntar o que ajustar (título, legenda, texto do problema, texto da solução, descrição visual ou CTA) e refazer apenas a parte indicada.

Se escolher 3, apresentar a lista das 10 ideias novamente e perguntar o novo número.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-problema-solucao-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-problema-solucao-{numero}.md`

Conteúdo do arquivo:

```markdown
# Problema-Solução nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Problema + Solução escolhida (nº {numero_ideia} das 10)

**Problema:** [texto do problema]
**Solução:** [texto da solução]

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

## Banco completo (as 10 ideias geradas nesta sessão)

Liste aqui todas as 10 ideias de problema mais solução geradas nesta sessão, pra o aluno usar depois sem rodar a sub-skill de novo.
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-problema-solucao-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-problema-solucao-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Problema-Solução salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-problema-solucao-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro Problema-Solução com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Problema-Solução gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-problema-solucao-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-problema-solucao-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro Problema-Solução com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-problema-solucao-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-problema-solucao-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-problema-solucao-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-problema-solucao-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-problema-solucao-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras

- Light Copy obrigatória no título e na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- Produto NÃO aparece no lead do título nem da legenda.
- O texto do problema, o texto da solução e o CTA seguem regras próprias e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- **NUNCA use travessão** em nenhum texto da skill (nem nos problemas, nem nas soluções, nem nos títulos, nem nas legendas, nem nos prompts do GPT). É vício de IA. Use vírgula ou ponto final no lugar.
- **Problema em primeira pessoa**, com tom de pensamento real, específico do público, com contradição, vergonha ou especificidade. Nunca genérico.
- **Solução é AÇÃO, não explicação.** A solução tem que dizer o que fazer, não "se acalma" ou "entende que é fase". Se não há ação concreta na solução, refaça antes de entregar.
- **Solução coerente com o método do produto.** Se o produto tem método/abordagem específica (neurociência, estoicismo, BLW, Feng Shui, IA, etc.), as soluções DEVEM usar o vocabulário e os frameworks desse método.
- **Contraste visual sai da ideia escolhida**, não de exemplos hipotéticos. Sempre construa a descrição visual a partir do conteúdo específico do problema e da solução escolhidos pelo aluno. O lado esquerdo mostra a pessoa vivendo o problema, o lado direito mostra a pessoa aplicando a solução, e a diferença visual comunica a transformação antes da leitura.
- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês (que são gatilhos eficazes pro gerador de imagem).
- **Avatar brasileiro real**: pessoa de classe média típica, sem produção de modelo, contexto cotidiano de apartamento brasileiro. Roupa casual, cabelo natural, expressão real. Faixa etária coerente com o público do nicho.
- Arte dividida verticalmente ao meio por uma linha branca sólida. Lado esquerdo com tarja vermelha "PROBLEMA" e emoji de alerta, lado direito com tarja verde "SOLUÇÃO" e emoji de joinha. Seta horizontal sobre a linha divisora, estilo creator. CTA laranja sólido, evidente e clicável.

### Sobre o CTA com a promessa do produto

O CTA sempre carrega o benefício específico do produto, não um "Aprenda como" genérico. Exemplos:
- Curso de esquecer o ex → "Aprenda a esquecer o ex →"
- Curso de introdução alimentar → "Aprenda a fazer a introdução alimentar →"
- Curso de tráfego com Claude → "Aprenda a fazer tráfego com IA →"
- Curso de Feng Shui → "Aprenda Feng Shui em 7 dias →"
- Curso de bonecas de pano → "Aprenda a costurar bonecas de pano →"

### Regras gerais finais

- Compliance Facebook Ads: sem pernas de fora, decote, roupa curta, poses sensualizadas, violência. Postura natural e respeitosa.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível brasileiro com base no produto e avisar antes de gerar as 10 ideias. Não travar o fluxo.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).

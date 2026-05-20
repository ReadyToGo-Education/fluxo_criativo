# Criativo Surreal. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 3 (Criativo Surreal). Formato com forte impacto visual fora do mundo normal (escalas impossíveis, personificações, metáforas visuais sofisticadas), sempre com estética editorial publicitária no nível Cannes Lions. Gera 10 ideias surreais dentro do universo visual estrito do nicho, o aluno escolhe uma, e a sub-skill entrega título, legenda e dois prompts prontos pra colar no ChatGPT (Feed e Stories).

**Por que esse formato funciona:**
O surrealismo controlado para o scroll. A metáfora visual entrega a mensagem antes da pessoa ler qualquer texto. Quando o headline cumpre o papel de identificar o produto/nicho, o anúncio funciona como uma peça editorial de revista, gerando autoridade e desejo na mesma imagem.

## O Que Fazer

### 0. Contexto

O orquestrador `/criativo-estatico` já carregou o contexto enriquecido (perfil.md, idconsumidor.md, tipo.md, preco.md, pesquisa-mercado.md, e inferências a partir do slug do produto).

Se a sub-skill foi chamada direto, carregue esses arquivos agora seguindo o Passo 0 do orquestrador.

Extraia (combinando dado real + inferência):

- **Produto**: nome do produto (do `perfil.md` ou inferido do slug, ex: `automacoes-inteligentes` vira "Automações Inteligentes").
- **Nicho**: do `perfil.md` (seção "Nicho") ou inferido do nome + tipo + preço.
- **Público**: do `idconsumidor.md` ou seção "Para Quem É" do `perfil.md` ou inferido do nicho.
- **Universo visual do nicho**: 6 a 10 elementos visuais concretos que pertencem ao nicho (essenciais pra ideias surreais coerentes). Use a tabela interna abaixo na seção "Referências de paleta e tipografia por tipo de nicho" como ponto de partida e amplie se necessário.

### 1. Apresentar resumo do contexto e confirmar

SEMPRE mostre o resumo, mesmo se algum campo veio de inferência. Marque o que é real e o que foi inferido:

(Nota para o modelo: marque "✓ do perfil" nos campos extraídos diretamente do perfil.md ou idconsumidor.md. Marque "○ inferido" nos campos que foram um chute a partir do slug, tipo ou preço. Essas marcações devem aparecer ao lado de cada campo no bloco exibido ao aluno.)

```
Vou usar estes dados do seu produto ativo ({slug}):

Produto: [nome do produto] [✓ do perfil / ○ inferido]
Nicho: [nicho] [✓ do perfil / ○ inferido]
Público: [resumo do público] [✓ do perfil / ○ inferido]

Está tudo certo?

1. Sim, está certo, pode seguir
2. Quero ajustar algum campo
```

**Se escolher 1**, pular pra etapa 2 (Geração das 10 ideias surreais).

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

Se o aluno não especificou público, assumir um plausível com base no produto/nicho e avisar antes de gerar as ideias:

```
Você não especificou o público, então vou assumir: [público assumido]. Se quiser trocar, é só me dizer.
```

### 2. Geração das 10 ideias surreais

Anuncie:

```
🔍 Próximo passo: gerar 10 ideias surreais dentro do universo visual do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Antes de gerar, identifique o **universo visual estrito do nicho** com base no perfil. Liste mentalmente 6 a 10 elementos que pertencem só a esse nicho (objetos, ferramentas, ambientes, ações típicas). Esses elementos são a matéria-prima das 10 ideias. Nada de elemento genérico.

Exemplos de universos visuais (para referência interna):
- Cafeteria: xícara, café, toast, máquina de espresso, grãos, balcão, brunch, croissant, leite vaporizado, latte art
- Bonecas de pano: agulha, linha, tecido, boneca, botão, costura, tesoura, máquina de costura, retalhos, enchimento
- Tráfego pago: tela de celular, dashboard, gráfico de campanha, anúncios, IA, métricas, gerenciador, cliques, conversão, pixel
- Tarot: cartas espalhadas, mesa mística, velas, cristais, panos rendados, baralho, magia, leitura, símbolos, runas
- Feng Shui: objetos da casa, plantas, espelhos, cristais, água em fluxo, mandala, organização, energia, harmonia, decoração ancestral

#### Regras das ideias surreais

- **Dentro do universo visual estrito do nicho.** Pra cafeteria, só elementos de cafeteria. Pra bonecas de pano, só elementos de costura. Pra tráfego pago, só elementos do nicho. Nunca elementos genéricos que não conectem com o nicho (ex: "surfar em dinheiro" pra qualquer nicho, "dragão" sem contexto, "espada" sem ligação).
- **Surreal mas com lógica imediata.** A pessoa olha e em 1 segundo conecta a metáfora com a dor ou a transformação. Nada de bizarrice nonsense. Tipos de surrealismo que funcionam: alguém carregando peso impossível, escala invertida (gigante ou minúsculo), multiplicação de braços ou cabeças, personificação de objetos, superpoder visual (olhos de raio-X, voar), fusão com objeto, brotar ou crescer, ímã visual atraindo, casa ou objeto flutuando.
- **Headline obrigatório identifica o produto ou nicho.** A palavra-chave do produto SEMPRE aparece no headline ("Sua cafeteria...", "Costurar bonecas de pano...", "Tráfego pago é...", "Feng Shui faz..."). Nunca genérico. A pessoa lê o headline e sabe imediatamente do que se trata.
- **Headline publicitário objetivo.** Curto, com impacto, mas a pessoa entende o benefício ou a dor em 2 segundos. Sem fórmula fixa, cada um diferente e criativo. Sem ficar lúdico ou poético a ponto de perder clareza.
- **Cada ideia traz a descrição visual + o headline correspondente.**

#### Apresentação

Mostre as 10 ideias numeradas de 1 a 10, sem categorias, em lista única:

```
Aqui estão 10 ideias surreais pro seu nicho.

1. Descrição: [descrição visual da cena surreal em 2 a 3 frases]
   Headline: "[headline correspondente]"

2. Descrição: [descrição visual da cena surreal em 2 a 3 frases]
   Headline: "[headline correspondente]"

3. Descrição: [descrição visual]
   Headline: "[headline]"

4. Descrição: [descrição visual]
   Headline: "[headline]"

5. Descrição: [descrição visual]
   Headline: "[headline]"

6. Descrição: [descrição visual]
   Headline: "[headline]"

7. Descrição: [descrição visual]
   Headline: "[headline]"

8. Descrição: [descrição visual]
   Headline: "[headline]"

9. Descrição: [descrição visual]
   Headline: "[headline]"

10. Descrição: [descrição visual]
    Headline: "[headline]"

---
Qual número você quer transformar em criativo?
```

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.

### 3. Escolha e geração do criativo

Após o aluno escolher um número de 1 a 10, anuncie:

```
🔍 Próximo passo: gerar título, legenda e prompts pro ChatGPT. Tempo estimado: cerca de 30 segundos.
```

Gere quatro coisas a partir da ideia escolhida:

#### A) Título do anúncio

Repete o headline da ideia escolhida (o headline já cumpre o papel de título de venda).

#### B) Legenda pro Instagram

2 a 3 linhas. Conecta com o headline, gera curiosidade sem entregar tudo. Termina com **"Link na bio"**. Light Copy aplicada (sem travessão, sem exclamação, sem pergunta, sem promessa vaga, produto fora do lead).

#### C) Prompt pro ChatGPT (formato Feed)

Determinar antes a **paleta** e a **tipografia** do nicho consultando a tabela de referências abaixo (seção "Referências de paleta e tipografia por tipo de nicho").

Substituir todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

Os placeholders são:
- `[descrição detalhada da cena surreal, hiperrealista, com elementos do nicho]`: a descrição da ideia escolhida, expandida com textura, materiais e ângulo
- `[textura real, pele real, objeto real do nicho]`: exemplos concretos do que precisa ser hiperrealista (ex: "espuma de café com bolhas visíveis, mãos com poros e linhas naturais", "fibras do tecido aparentes, agulha com brilho metálico", "tela de celular com pixels nítidos, dedo com unha realista")
- `[paleta temática conectada ao nicho]`: exemplo "bege quente terroso (#D2B48C, #A0522D)", "azul-meia-noite com toque grafite (#1A2332, #2D3748)"
- `[descrição da tipografia temática (com exemplos por nicho como serifada vintage pra café, sans-serif tecnológica pra IA, serifada delicada pra artesanato, serifada oriental pra Feng Shui)]`
- `[headline escolhido]`: o headline exato da ideia escolhida
- `[CTA conectado ao headline]`: frase curta e direta de descoberta. Padrão "Saiba mais"

````
Cria pra mim uma arte surreal pra anúncio de Instagram. Estética cinematográfica, fotografia editorial publicitária, no nível de uma peça da Cannes Lions.

Hyperrealistic surreal photo manipulation, impossible scale, photographic realism not 3D render, slight medium-format film grain, single dramatic side light, minimalist solid-color background.

A cena é: [descrição detalhada da cena surreal, hiperrealista, com elementos do nicho]. Hiperrealismo fotográfico, com [textura real, pele real, objeto real do nicho]. O fundo é uma cor sólida limpa: [paleta temática conectada ao nicho], que faz o elemento surreal ser protagonista absoluto.

Iluminação editorial dramática: luz lateral suave criando sombra clara e profundidade. Sem cara de 3D, sem cartoon, sem dramatização exagerada, sem cara de banner de varejo.

Tipografia conectada ao nicho: [descrição da tipografia temática (com exemplos por nicho como serifada vintage pra café, sans-serif tecnológica pra IA, serifada delicada pra artesanato, serifada oriental pra Feng Shui)]. A tipografia ocupa cerca de 25-35% da imagem.

O headline em destaque, grande e marcante: "[headline escolhido]". O headline em si já identifica pra quem é o anúncio.

No canto inferior, um CTA com texto + seta, na mesma cor do headline: "[CTA conectado ao headline] →". Sem bloco de botão pesado, apenas texto e seta com tipografia refinada.

Margem de respiro obrigatória: deixa espaço generoso em volta do texto. O headline não pode ficar colado no topo nem no rodapé. A composição precisa respirar, com ar em volta de todos os elementos.

Pouco texto na arte. Fonte grande, legível em celular. Nada de fonte pequena.

IMPORTANT: exact 4:5 Instagram feed aspect ratio. Do NOT create 9:16 story composition. Composition must be optimized for feed posts and carousels. Shorter vertical framing. Exact size reference: 1080x1350.
````

#### D) Prompt pro ChatGPT (formato Stories)

Esse é fixo. Não precisa preencher placeholders.

````
Agora cria a exata mesma arte, mesmas cores, mesmo texto, mesmo visual, mesmos elementos, só diagramada pro formato Stories.

IMPORTANT: exact 9:16 full-screen vertical composition for Instagram Reels and Stories. Must occupy entire smartphone screen vertically. Exact size reference: 1080x1920.
````

### 4. Auto-revisão obrigatória

Antes de mostrar ao aluno: aplicar a rotina de auto-revisão de copy do CLAUDE.md (carregar Manual da Copy + acionar a skill `revisora`) no título (que é o headline) e na legenda. Corrigir direto. Nunca mostrar versão bruta.

A descrição visual e o prompt em inglês NÃO passam pela revisora (são instruções pro DALL-E, não copy de venda), mas devem respeitar Light Copy no texto pt_BR (sem travessão, sem exclamação, sem pergunta).

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu Criativo Surreal:

📌 IDEIA ESCOLHIDA (nº {numero_ideia})
[descrição visual da ideia escolhida]

📌 TÍTULO DO ANÚNCIO (headline)
[headline gerado]

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

Se escolher 2, perguntar o que ajustar (headline, legenda, paleta, tipografia ou descrição visual) e refazer apenas a parte indicada.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-surreal-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-surreal-{numero}.md`

Conteúdo do arquivo:

```markdown
# Criativo Surreal nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Ideia escolhida (nº {numero_ideia} das 10)

**Descrição visual:** [descrição visual da cena surreal]

**Headline:** [headline da ideia]

## Título do anúncio

[headline]

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

Liste aqui todas as 10 ideias geradas nesta sessão, no mesmo formato da apresentação (Descrição + Headline), para o aluno consultar depois sem precisar rodar a sub-skill de novo.
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-surreal-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-surreal-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Criativo Surreal salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-surreal-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro Criativo Surreal com outra das 10 ideias
2. Trocar o nicho ou público e gerar 10 ideias novas
3. Voltar e escolher outro formato
```

**No modo API:**

```
✅ Concluído: criativo Criativo Surreal gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-surreal-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-surreal-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro Criativo Surreal com outra das 10 ideias
3. Trocar o nicho ou público e gerar 10 ideias novas
4. Voltar e escolher outro formato
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-surreal-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-surreal-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-surreal-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-surreal-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-surreal-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Referências de paleta e tipografia por tipo de nicho

Use estas referências para preencher os placeholders `[paleta temática]` e `[descrição da tipografia temática]` do prompt Feed. Quando o nicho do aluno não estiver na lista, escolha uma paleta sóbria temática e uma tipografia que converse com a essência visual do nicho. Nunca paleta saturada ou estourada, nunca fonte genérica.

| Tipo de nicho | Paleta | Tipografia |
|---|---|---|
| Cafeteria, brunch, gastronomia | Bege quente, terracota, mostarda apagada, verde musgo | Serifada editorial vintage premium (estilo café histórico) |
| Alimentação saudável, meal prep, nutrição | Verde-folha apagado, branco natural, bege neutro, terracota suave | Sans-serif moderna limpa ou serifada leve estilo editorial de bem-estar |
| Artesanato, hobby, costura | Rosa pálido, creme antigo, off-white | Serifada delicada estilo livro de receitas vintage ou revista de bordado |
| Feng Shui, casa, espiritualidade | Bege quente, off-white com toque de terracota, tons serenos | Serifada elegante com personalidade ancestral ou oriental refinada |
| Tráfego pago, tecnologia, IA | Azul-acinzentado profundo, grafite, azul-meia-noite, verde-petróleo apagado | Sans-serif condensada bold estilo Bloomberg ou interface editorial premium tech |
| Finanças, investimentos | Verde escuro, grafite, dourado contido | Sans-serif condensada bold ou serifada editorial pesada |
| Beleza, moda, anti-aging | Rosa pálido, champagne, off-white refinado | Serifada delicada estilo editorial de moda |
| Outros nichos | Paleta sóbria temática (consultar essência visual do nicho) | Tipografia que converse com a essência do nicho |

## Regras

- Light Copy obrigatória no headline e na legenda. Sem travessão, sem exclamação, sem pergunta, sem promessa vaga, sem "não é X. É Y.".
- Universo visual estrito do nicho. Tudo na cena pertence ao universo do nicho. Sem elementos genéricos que poderiam servir para qualquer produto.
- Headline identifica o produto ou nicho. A palavra-chave do produto sempre aparece no headline. Sem tag de público separada, o próprio headline carrega isso.
- Surrealismo com lógica imediata. A metáfora se conecta com a dor ou a transformação em 1 segundo. Sem bizarrice nonsense.
- Sem dramatização exagerada. A estética é editorial sofisticada (Cannes Lions), não banner de varejo. Cores sóbrias, iluminação natural, hiperrealismo fotográfico.
- Margem de respiro obrigatória. O texto na arte sempre tem espaço generoso em volta, nunca colado em topo ou rodapé.
- CTA com texto + seta. Sem bloco de botão pesado.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT mistura português coloquial brasileiro com diretrizes técnicas em inglês (gatilhos eficazes pro DALL-E e similares).
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Se o aluno não especificou público, assumir um plausível com base no produto e avisar antes de gerar as 10 ideias. Não travar o fluxo.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).

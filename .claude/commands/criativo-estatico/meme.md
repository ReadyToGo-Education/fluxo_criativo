# Meme. Sub-skill do `/criativo-estatico`

Sub-skill chamada pelo orquestrador `/criativo-estatico` quando o aluno escolhe a opção 11 (Meme). Cria um criativo humorístico baseado em estruturas de meme conhecidas: arte limpa com título preto sobre fundo branco no topo, imagem absurda do meme no meio, e CTA em fundo colorido na base com duas linhas em cores diferentes. Gera 20 ideias de meme (10 estruturas criadas + 10 memes brasileiros reais), o aluno escolhe uma, e a sub-skill entrega título, legenda e dois prompts prontos pra colar no ChatGPT (Feed e Stories).

**Por que esse formato funciona:**
O humor gera identificação imediata: a pessoa se reconhece na situação absurda antes de perceber que é anúncio. O criativo não parece banner publicitário polido, o choque visual vem da imagem cômica. O CTA com duas linhas em cores diferentes prende o olho e conduz pro clique sem quebrar a leveza do meme.

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

**Se escolher 1**, pular pra etapa 2 (Geração das 20 ideias de meme).

**Se escolher 2**, perguntar qual campo ajustar e refazer só a parte indicada.

**Pergunta de ajuste (caso aluno escolha 2)**, com exemplos do nicho do produto ativo:

```
Qual é o seu produto e nicho?
(ex: [3 exemplos do mesmo universo do produto ativo])
```

**IMPORTANTE: os exemplos NUNCA podem ser genéricos.** Antes de fazer a pergunta, construa 3 exemplos do mesmo universo do produto ativo:

- Se o produto for de automação/IA: "Mentoria de Automações com IA pra criadores de conteúdo", "Curso de Agentes GPT pra atendimento", "Treinamento de N8N pra agências"
- Se for de skincare: "Curso de Skincare pra mulheres 40+", "Mentoria de rotina de pele pós-menopausa", "Ebook de anti-aging caseiro"
- Se for de tráfego: "Mentoria de Tráfego Pago pra criadores", "Curso de Anúncios no Meta pra agências", "Consultoria de Performance pra ecommerce"
- Se for de cafeteria: "Consultoria de Cardápio pra donos de cafeteria", "Treinamento de Barista pra equipes", "Curso de Como Abrir uma Cafeteria"
- Último recurso (se realmente não der pra inferir nicho): "Mentoria de tráfego pago pra criadores de conteúdo", "Curso de skincare pra mulheres 40+", "Consultoria de cardápio pra donos de cafeteria"

Se o aluno não especificou público, assumir um plausível brasileiro com base no produto/nicho e avisar antes de gerar as ideias:

```
Você não especificou o público, então vou assumir: [público assumido]. Se quiser trocar, é só me dizer.
```

### 2. Geração das 20 ideias de meme

Anuncie:

```
🔍 Próximo passo: gerar 20 ideias de meme do seu nicho. Tempo estimado: cerca de 60 segundos.
```

Gere uma lista única numerada de 1 a 20, com separadores `---` entre cada ideia. As 10 primeiras são estruturas de meme criadas (universais, o GPT cria a cena do zero), as 10 últimas são memes brasileiros reais reconhecíveis. Numere sempre de 1 a 20 (não dividir em duas listas separadas) pra evitar confusão na hora do aluno escolher. A escolha entre estruturas criadas (1 a 10) e memes reais (11 a 20) fica clara pelo nome em parênteses no item.

#### Ideias 1 a 10: estruturas de meme criadas (universais, o GPT cria a cena do zero)

Misture as seguintes estruturas, variando entre elas pra dar leque. Não precisa usar todas, escolha as 10 melhores pro nicho:

1. **Tweet "Quando [situação]"**. Texto estilo tweet curto + foto absurda da pessoa vivendo a situação.
2. **Eu vs Eu (Drake)**. Comparação rejeita ❌ / aprova ✅.
3. **POV: você é [contexto do nicho]**. Situação de imersão.
4. **Ninguém / Absolutamente ninguém / Você [fazendo algo absurdo]**. Humor de obsessão pessoal.
5. **Quando você descobre [revelação contra-intuitiva]**. Momento de virada de chave.
6. **Antes / Depois (versão meme exagerada)**. Transformação cômica.
7. **Eu achando vs A realidade**. Quebra de expectativa.
8. **Distracted boyfriend / olhando pro lado**. Pessoa que ignora o óbvio e se distrai com o errado.
9. **Print de conversa absurda**. Diálogo cliente/profissional ou conversa interna.
10. **Two buttons / suando pra escolher**. Personagem em desespero entre dois botões igualmente ruins ou bons.

Formato de cada item de 1 a 10:

```
**1.** (Tweet "Quando...")
**Texto:** "[título do meme]"
**Imagem:** [descrição da cena absurda da imagem do meme]
```

#### Ideias 11 a 20: memes brasileiros reais reconhecíveis

REGRA CRÍTICA: só entram memes onde a EXPRESSÃO FACIAL SOZINHA já é a piada. Sem precisar de exagero teatral ou contexto explicativo, o GPT consegue replicar fielmente.

**Memes que FUNCIONAM** (entram na lista):
- **Nazaré Confusa**. Expressão de confusão extrema com fórmulas matemáticas flutuando.
- **Galvão Bueno gritando GOL**. Boca alongada gritando, olhos fechados, mãos pra cima.
- **Mr. Krabs/Patrick assustado**. Olhos arregalados, boca aberta de pavor com dentes à mostra.
- **Choque Tia Néia/WhatsApp**. Boca em "O" gigante de espanto, mão na cara.
- **Faustão ERROU**. Braço esticado apontando, boca aberta dramaticamente.
- **Will Smith desconfiado / cara enviesada**. Olhos pro lado, sobrancelha levantada.
- **Cachorro no fogo / Everything is fine**. Sorriso forçado em meio ao caos sutil.
- **"Esse menino é o demônio"**. Mãe brasileira apontando bravo, expressão raivosa cômica.
- **Spider-Man apontando**. Múltiplas pessoas idênticas apontando umas pras outras.
- **Bela Gil substituindo**. Sorriso sereno + objeto improvável na mão.

**Memes que NÃO FUNCIONAM** (NÃO entram na lista):
- **Renato Garcia pensativo**. Expressão sutil demais, o GPT não consegue replicar a graça.
- **Doge/Wojak/qualquer ilustração estilizada**. O GPT não consegue replicar fielmente esses estilos.
- **Memes só de texto** sem visual icônico.
- **Memes que dependem de movimento/vídeo** (Bigode do Maguila, Sabrina Sato, etc).
- Memes onde a piada depende de contexto cultural ultra específico ou áudio.

A regra de ouro: **se você colocar a expressão do meme num rosto qualquer e a piada ainda fica óbvia, o meme funciona. Se precisar de explicação pra graça acontecer, não funciona.**

Formato de cada item de 11 a 20:

```
**11.** (Meme [Nome do meme])
**Texto:** "[título do meme]"
**Imagem:** [descrição da cena com a expressão característica do meme adaptada ao nicho]
```

#### Apresentação

Mostre as 20 ideias numeradas de 1 a 20, separadas por `---`:

```
Aqui estão 20 ideias de meme pro seu nicho.

---

**1.** (Tweet "Quando...")
**Texto:** "[título do meme]"
**Imagem:** [descrição da cena absurda da imagem do meme]

---

**2.** (Eu vs Eu - Drake)
...

---

**11.** (Meme [Nome do meme])
**Texto:** "[título do meme]"
**Imagem:** [descrição da cena com a expressão característica do meme adaptada ao nicho]

---

Qual número você quer transformar em criativo?

Se o número for inválido, peça de novo de forma curta, sem repetir a lista inteira.
```

### 3. Escolha e geração do criativo

Após o aluno escolher um número de 1 a 20, anuncie:

```
🔍 Próximo passo: gerar título, legenda e prompts pro ChatGPT. Tempo estimado: cerca de 30 segundos.
```

Gere quatro coisas a partir da ideia de meme escolhida:

#### A) Título do anúncio

Frase de impacto conectada à promessa do produto, em afirmação direta. Light Copy aplicada.

Regras obrigatórias:
- Sem travessão (—)
- Sem exclamação (!)
- Sem pergunta no título
- Sem promessa vaga (incluir dado, prazo ou situação concreta)
- Sem "não é X. É Y."
- Produto não aparece no lead
- Linguagem que a pessoa usaria com uma amiga

#### B) Legenda pro Instagram

2 a 3 linhas em primeira pessoa, tom de creator amador. Gera curiosidade sem entregar o método. Termina com "Te conto tudo no link 👇" ou similar. Light Copy aplicada.

#### C) Prompt pro ChatGPT (formato Feed)

Substitua todos os placeholders pelos dados reais. **O texto final ao usuário não pode ter colchetes.**

Para ideias 1 a 10 (memes criados), remova o trecho entre colchetes sobre o meme conhecido. Para ideias 11 a 20 (memes brasileiros reais), preencha esse trecho com o nome e a descrição visual do meme original.

````
Cria pra mim uma arte de anúncio pra Instagram no formato MEME ESTRUTURA LIMPA[, baseado no meme conhecido como [NOME DO MEME REAL] (descrição visual do meme original), apenas pra ideias 11-20]. A arte tem 3 elementos: TÍTULO no topo, IMAGEM ABSURDA do meme no meio, CTA na base. NADA MAIS. Sem caixas, sem ícones, sem marcas, sem referências a redes sociais.

NO TOPO DA ARTE, sobre fundo branco limpo, o título do meme em tipografia sans-serif preta, peso médio, tamanho grande e bem legível. Texto centralizado ou alinhado à esquerda:

"[TÍTULO DO MEME ESCOLHIDO]"

NO MEIO DA ARTE, ocupando boa parte do criativo, A IMAGEM ABSURDA DO MEME:

[DESCRIÇÃO COMPLETA DA CENA DO MEME ADAPTADA AO NICHO:
- Pessoa brasileira real do público do nicho (idade, fenótipo brasileiro autêntico, cabelo natural, sem maquiagem, look casual brasileiro)
- Cenário do nicho (apartamento brasileiro de classe média, com elementos visuais inconfundíveis do nicho aparecendo na cena)
- Expressão facial ou pose absurda/cômica que carrega a piada do meme. Pra memes reais (11-20), a expressão tem que ser idêntica à do meme original conhecido. Pra memes criados (1-10), a expressão e pose devem casar com a estrutura escolhida (Tweet "Quando" tem expressão de cansaço/pavor cômico, Drake é split com rejeita/aprova, Spider-Man são pessoas idênticas apontando, etc).
- Se for "Eu vs Eu" tipo Drake, descrever as duas cenas da pessoa. Se for "Spider-Man apontando", descrever os 2-3 personagens idênticos apontando uns pros outros. Se for "Antes/Depois", descrever as duas cenas.]

GATILHOS DE ULTRA-REALISMO OBRIGATÓRIOS (em inglês pro gerador de imagem):
- "amateur iPhone photo, casual snapshot"
- "raw unedited smartphone photography"
- "real Brazilian person, no model, no makeup professional"
- "natural skin texture with visible pores"
- "authentic Brazilian middle-class home interior"
- "smartphone camera quality, candid relatable meme photo"
- "non-American interior, Brazilian context"
- [acrescentar mais gatilhos específicos da expressão facial/pose conforme a estrutura do meme escolhido]

NA BASE DA ARTE, separado da imagem por uma margem clara, o CTA com DUAS LINHAS em CORES DIFERENTES:

Em fundo de cor sólida contrastante (preto, terracota escuro, rosa escuro, ou outra cor escolhida conforme paleta da arte), o CTA tem DUAS LINHAS:

LINHA 1 (gancho/afirmação) em [cor 1 conforme regra de contraste] bold sans-serif tamanho médio:
"[FRASE CURTA DE GANCHO QUE CONECTA O MEME À PROMESSA]"

LINHA 2 (chamada de ação) em [cor 2 de DESTAQUE conforme regra de contraste] bold sans-serif tamanho ligeiramente maior:
"👉 [CTA CONDUZINDO AO LINK]"

REGRA DE CONTRASTE DO CTA (OBRIGATÓRIA, CRÍTICA):
O CTA SEMPRE tem 2 linhas com CORES DIFERENTES entre elas. A linha 2 (chamada de ação) DEVE ter cor de DESTAQUE diferente da linha 1 pra prender o olho. O contraste entre as duas linhas é o que faz a pessoa bater o olho e clicar.

- Se fundo do CTA for ESCURO (preto, terracota escuro, rosa escuro, azul-marinho): LINHA 1 em BRANCO + LINHA 2 em AMARELO VIVO ou LARANJA VIVO.
- Se fundo do CTA for CLARO (amarelo, rosa claro, branco): LINHA 1 em PRETO + LINHA 2 em VERMELHO ou AZUL-MARINHO.
- Se fundo do CTA for tom MÉDIO (verde, azul médio): LINHA 1 em BRANCO + LINHA 2 em AMARELO VIVO.

NUNCA as duas linhas na mesma cor. O destaque na linha 2 é o que conduz pro clique.

REGRAS CRÍTICAS:
- PROIBIDO incluir logo de rede social, símbolo de plataforma (X, Twitter, Instagram, TikTok), avatar, foto de perfil, @handle, nome de usuário, selo de verificação, barra de interação (curtidas/retweets/comentários), qualquer elemento que remeta a rede social.
- A arte é APENAS: título preto sobre fundo branco no topo + imagem do meme no meio + CTA em fundo colorido na base com DUAS LINHAS em CORES DIFERENTES. NADA MAIS.
- NÃO pode parecer banner publicitário polido. O choque visual vem da imagem absurda.
- Compliance Facebook Ads: sem violência, sem ferida, sem sangue, sem lesão, sem cadáver, sem exposição ofensiva. Humor sempre dentro dos limites.

PROIBIDO usar travessão (nem o "—" nem o "–") em nenhum texto. Use vírgula ou ponto final no lugar.

POSICIONAMENTO: TODOS OS ELEMENTOS DEVEM SUBIR um pouco do rodapé. Deixa margem entre o CTA e a borda inferior da arte (mínimo 8 a 10% da altura). Mesmo respeito de margem no topo.

Fonte legível em celular.

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

O título do meme (texto que vai na arte) e o texto do CTA NÃO passam pela revisora (são conteúdo da arte com tom humorístico específico), mas devem respeitar Light Copy: sem travessão, sem exclamação.

### 5. Apresentação e aprovação

```
Pronto. Aqui está o seu criativo Meme:

📌 MEME ESCOLHIDO (nº {numero_meme} das 20)
[texto do meme e descrição da imagem]

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
3. Voltar e escolher outro meme (dos 20)
```

Se escolher 2, perguntar o que ajustar (título, legenda, texto do meme, descrição visual ou CTA) e refazer apenas a parte indicada.

Se escolher 3, apresentar a lista das 20 ideias novamente e perguntar o novo número.

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

Em qualquer um dos modos, salve o arquivo `.md` do criativo. Descubra o próximo número sequencial verificando arquivos existentes em `meus-produtos/{ativo}/entregas/criativos/` (procurar `criativo-meme-*.md` e pegar o maior número + 1; se nenhum existir, começar em 1).

Salve em:
`meus-produtos/{ativo}/entregas/criativos/criativo-meme-{numero}.md`

Conteúdo do arquivo:

```markdown
# Meme nº {numero}

**Data:** {data atual no formato YYYY-MM-DD}
**Produto:** [nome do produto]
**Nicho:** [nicho]
**Público:** [público]

## Meme escolhido (nº {numero_meme} das 20)

**Texto:** [texto do meme]
**Imagem:** [descrição da cena do meme]

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

## Banco completo (as 20 ideias geradas nesta sessão)

Liste todas as 20 ideias de meme geradas nesta sessão, numeradas de 1 a 20, pra o aluno poder usar qualquer uma depois sem precisar rodar a sub-skill de novo.
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
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-meme-{numero}-feed.txt" --model "{modelo}" --aspect "4:5" --out "meus-produtos/{ativo}/entregas/criativos/criativo-meme-{numero}-feed.png"
```

5. Se o script falhar (erro de chave, rede ou modelo), avise o aluno em linguagem simples e ofereça o modo ChatGPT mostrando os prompts.

6. NÃO gere Stories automaticamente. A opção aparece como primeira no menu do Passo 7 e usa a imagem do Feed como referência (image-to-image), economizando chamada quando o aluno só quer Feed.

### 7. Confirmação final e próximo passo

Apresente o resultado conforme o modo escolhido. Sempre mostrar o caminho absoluto (regra 4a do CLAUDE.md).

**No modo ChatGPT:**

```
✅ Concluído: criativo Meme salvo.

Caminho: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-meme-{numero}.md

Como usar:
1. Abra o ChatGPT ou o Gemini (com geração de imagem habilitada).
2. Cole o Prompt Feed do arquivo salvo.
3. Quando a arte de Feed estiver pronta, mande "ok".
4. Cole o Prompt Stories pra gerar a versão vertical da mesma arte.
```

No modo ChatGPT, depois da mensagem de confirmação, ofereça o menu padrão:

```
Quer fazer mais alguma coisa?
1. Gerar outro Meme com outra das 20 ideias
2. Trocar o nicho ou público e gerar 20 ideias novas
3. Voltar e escolher outro formato de criativo
```

**No modo API:**

```
✅ Concluído: criativo Meme gerado e salvo.

Imagem do Feed: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-meme-{numero}-feed.png
Briefing: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-meme-{numero}.md
```

Depois ofereça o menu com "Gerar para o formato de Stories" como nova primeira opção:

```
Quer fazer mais alguma coisa?
1. Gerar para o formato de Stories (a partir da imagem do Feed)
2. Gerar outro Meme com outra das 20 ideias
3. Trocar o nicho ou público e gerar 20 ideias novas
4. Voltar e escolher outro formato de criativo
```
#### Sub-fluxo "Gerar para o formato de Stories" (opção 1 do menu acima)

Quando o aluno escolher 1, execute:

a) Grave num arquivo `.txt` na pasta de criativos o prompt curto de recomposição abaixo (sem placeholders), com o nome `prompt-meme-{numero}-stories.txt`:

```
Recompose this exact same creative for a vertical 9:16 Instagram Stories and Reels canvas (1080x1920). Keep the same scene, same person, same colors, same text content, same on-image text boxes, same CTA, same elements, same design language. Only recompose the framing to fill the entire vertical screen. Do not redesign, do not change typography, do not change wording. Only adapt the proportion from 4:5 to 9:16.
```

b) Anuncie:

```
🔍 Próximo passo: gerar a versão Stories a partir da imagem do Feed. Tempo estimado: 2 a 3 minutos.
```

c) Rode o script reaproveitando o modelo escolhido no Passo 6b, passando a imagem do Feed como referência visual (image-to-image):

```bash
py -3 scripts/gerar-criativo-estatico.py --prompt-file "meus-produtos/{ativo}/entregas/criativos/prompt-meme-{numero}-stories.txt" --model "{modelo}" --aspect "9:16" --reference-image "meus-produtos/{ativo}/entregas/criativos/criativo-meme-{numero}-feed.png" --out "meus-produtos/{ativo}/entregas/criativos/criativo-meme-{numero}-stories.png"
```

d) Confirme:

```
✅ Concluído: versão Stories gerada e salva.

Imagem do Stories: {caminho-raiz-projeto}\meus-produtos\{ativo}\entregas\criativos\criativo-meme-{numero}-stories.png
```

e) Reapresente o mesmo menu de opções.

## Regras

### Light Copy e copy de venda

- Light Copy obrigatória no título e na legenda. Sem travessão, sem exclamação, sem pergunta no título, sem promessa vaga, sem "não é X. É Y.".
- Produto NÃO aparece no lead do título nem da legenda.
- O título do meme e o texto do CTA seguem regras próprias (tom humorístico) e NÃO passam pela revisora, mas devem respeitar Light Copy.
- Auto-revisão obrigatória de copy (Manual da Copy + revisora) antes de apresentar o título e a legenda.
- Substituir TODOS os placeholders dos prompts pro ChatGPT. O texto final no chat e no arquivo salvo NÃO pode ter colchetes.
- Texto pro ChatGPT em linguagem coloquial brasileira misturada com as diretrizes técnicas em inglês.

### Sobre a imagem

- **Ultra-realismo brasileiro obrigatório** em todas as imagens: foto que parece tirada de iPhone por pessoa comum, fenótipo brasileiro autêntico, casa brasileira de classe média com bagunça real, sem produção, sem cara de modelo.
- **Expressão facial é a piada**: pra memes reais (11 a 20), a expressão do personagem DEVE ser idêntica à do meme original. Pra memes criados (1 a 10), a expressão e pose devem casar com a estrutura escolhida e o título.
- **Elementos do nicho visíveis na cena**: o cenário tem que ser inconfundível do nicho (banheiro com frascos pra skincare, cozinha com café e frascos pra cestas, home office com câmera e timeline pra videomaker, etc).
- **Sem exageros teatrais artificiais**: nada de iluminação de holofote, objetos gigantes fora do contexto, chuva de elementos. A graça vem da combinação expressão + cenário real + título conectado, não de efeitos visuais forçados.

### Sobre o CTA

- **Sempre 2 linhas em cores DIFERENTES** pra criar contraste interno.
- **Linha 1**: gancho/afirmação curta que conecta o meme à promessa do produto.
- **Linha 2**: chamada de ação em cor de DESTAQUE (amarelo vivo, laranja vivo, vermelho ou azul-marinho dependendo do fundo) com emoji 👉.
- **Fundo do CTA sempre em cor sólida contrastante** com o branco do título acima (preto, terracota escuro, rosa escuro são padrões seguros).
- **Linhas DA MESMA COR no CTA são proibidas**. O destaque na linha 2 é o que conduz pro clique.

### Sobre o que NÃO pode aparecer

- Logo de rede social (X, Twitter, Instagram, TikTok, Facebook).
- Avatar, foto de perfil, nome de pessoa, @handle, selo de verificação.
- Barra de interação de rede social (curtidas, retweets, comentários).
- Caixas de tweet, frames simulando interface de aplicativo.
- Travessões em qualquer texto (— ou –). Sempre vírgula ou ponto final.

### Compliance Facebook Ads

- Sem violência, ferida, sangue, lesão, cadáver, exposição médica chocante.
- Humor sempre dentro dos limites de plataforma.
- Pra nichos sensíveis (dermatite canina, skincare com problemas de pele, fitness com mudança corporal), a piada vem da expressão e situação, NUNCA da exposição do problema físico.

### Compatibilidade entre estruturas e nichos

- **Tweet "Quando..."**: funciona em todos os nichos. Sempre vai pessoa + foto de momento absurdo do problema.
- **Drake (Eu vs Eu)**: funciona quando o produto tem clara dualidade método errado vs método certo.
- **POV**: melhor pra nichos com situação claramente identificável (gestor de tráfego às 22h, mãe na hora do dever de casa, etc).
- **Ninguém/Você**: funciona pra obsessões reconhecíveis do público (verificar Stories do ex, comparar pele no espelho às 3h).
- **Spider-Man apontando**: ótimo pra críticas sobre comportamento de massa ("todo mundo fazendo a mesma coisa").
- **Memes reais**: usar conforme o nicho. Galvão Bueno gritando funciona pra qualquer comemoração. Mr. Krabs assustado pra pavor/descoberta ruim. Nazaré Confusa pra complexidade absurda. Faustão ERROU pra crença popular errada.
- **Alimentação saudável / meal prep / nutrição**: Tweet "Quando" e Antes/Depois funcionam bem pra mostrar o contraste entre a rotina caótica e a organização com o método. Nazaré Confusa pra rótulos e cálculos nutricionais. Ninguém/Você pra obsessões reconhecíveis do público (pesar cada ingrediente, tirar foto do prato antes de comer).

### Regras gerais

- Sempre numere de 1 a 20 (não dividir em duas listas separadas) pra evitar confusão na hora do aluno escolher.
- A escolha entre estruturas criadas (1 a 10) e memes reais (11 a 20) fica clara pelo nome em parênteses no item.
- Se o aluno pedir pra rodar um exemplo de nicho sem dar o público, assumir um público plausível brasileiro e avançar. Não travar o fluxo.
- Aprovação obrigatória antes de salvar (regra 5 do CLAUDE.md). Pular só se o aluno pediu explicitamente "ir direto à versão final" na mesma sessão.
- Acentuação correta em todo o texto gerado: não, são, você, está, três, público, próximo, último, vídeo, página, específico, lógico, estratégia, técnica.
- Número do criativo é sequencial dentro da pasta do produto. Verificar arquivos existentes antes de numerar.
- Após salvar, sempre exibir caminho absoluto no chat (regra 4a do CLAUDE.md).

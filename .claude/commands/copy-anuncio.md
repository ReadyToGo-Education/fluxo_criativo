---
name: workshop-marketing:copy-anuncio
description: Criar pacotes completos de anúncios para Meta Ads e Google Ads usando a Mandala de 18 Tipos de Anúncios da metodologia VTSD. Inclui copy, direção criativa e estratégia de campanha.
---

# Anúncio. Mandala de 18 Tipos (VTSD)

Cria pacotes de anúncios usando os 18 tipos da Mandala VTSD + estrutura de campanha.

## Usage

```
/copy-anuncio
```

## O Que Fazer

### 1. Contexto e Escolha do Produto

**Passo 1 — Identificar produtos disponíveis:**

Leia `meus-produtos/.ativo` para saber o produto ativo atual. Liste também todas as pastas existentes em `entregas/` (exceto `.ativo`) para mostrar as opções disponíveis.

**Passo 2 — Perguntar qual base usar:**

```
Para criar os anúncios, qual base de informações você quer usar?

1. Produto ativo: [nome do produto ativo]
[se existirem outros produtos cadastrados, listar aqui, ex:]
2. [nome do produto 2]
3. [nome do produto 3]
[última opção sempre:]
N. Informar nicho, público e quadro agora (sem produto cadastrado)

Digite o número:
```

**Se escolher um produto cadastrado (opções 1, 2, 3...):**
- Leia `meus-produtos/{ativo}/perfil.md` e `meus-produtos/{ativo}/idconsumidor.md` se existir
- Se não for o produto ativo, use o slug escolhido como base para todos os caminhos de arquivo desta sessão (sem alterar o `.ativo`)
- Extraia internamente: Decorados, Urgências Ocultas, Quadro, público, preço, tom

**Se escolher "Informar nicho, público e quadro agora":**
Fazer as seguintes perguntas, UMA por vez:

```
Qual o nicho ou tema do produto?
(ex: "Tarô", "Emagrecimento", "Finanças para autônomos")
```

```
Quem é o público que vai ver esse anúncio?
(ex: "Mulheres de 30 a 50 anos que estudam tarô há 1 a 3 anos")
```

```
Qual a transformação principal que o produto entrega? (o Quadro)
(ex: "Fazer leituras de tarô com confiança e cobrar por isso")
```

```
Qual o preço do produto?
(ex: "R$ 497", "gratuito", "R$ 97/mês")
```

Após coletar essas informações, prosseguir o fluxo usando esses dados no lugar do perfil.md. Salvar os anúncios gerados em `meus-produtos/{ativo}/entregas/criativos/` (criar a pasta se não existir).

---

**Extraia e liste internamente (não precisa mostrar ao usuário):**
- Todos os **Decorados** do perfil. esses são os benefícios que podem virar tema central de anúncio
- Todas as **Urgências Ocultas** do perfil, organizadas em 7 categorias com 10 itens cada (dores, dúvidas, desejos, assuntos relacionados, urgências quentes, frias e inusitadas). Cada item é um ângulo de entrada possível para um anúncio.

**Verifique o histórico:** leia todos os arquivos em `meus-produtos/{ativo}/entregas/criativos/`. Identifique quais urgências ocultas e decorados já foram explorados nos anúncios anteriores.

**Regra de não repetição:** nas novas variações, priorize urgências ocultas e decorados ainda não usados. Se todos já foram usados, escolha os de maior potencial e anote que está retomando esse tema.

Se não houver anúncios anteriores: "É o primeiro pacote de anúncios. vamos usar as urgências e decorados mais relevantes para a fase escolhida."

### 2. Entrevista

**REGRA ABSOLUTA: fazer UMA pergunta por vez. Esperar a resposta antes de fazer a próxima. Nunca agrupar perguntas.**

**Bloco 1. Tipo de campanha:**
```
Perpétuo ou pico de vendas?

1. Perpétuo
2. Pico de vendas

Digite o número:
```

---

**Se Perpétuo. perguntar em sequência (uma por vez):**

```
Qual o objetivo dos anúncios?

1. Descoberta. atrair novas pessoas que ainda não conhecem o produto
2. Relacionamento. criar conexão e autoridade com quem já segue
3. Conversão. vender
4. RMKT. converter quem já viu a página de vendas

Digite o número:
```

```
Qual o momento de consumo do público?

1. Prontidão. está pronto para comprar
2. Urgência Oculta. tem o problema, mas ainda não busca solução
3. Oportunidade. público amplo, ainda não está pronto para comprar

Digite o número:
```

```
Qual o tipo de anúncio?

1. Imagem estática
2. Vídeo

Digite o número:
```

---

**Se Pico de Vendas. perguntar fase:**

```
Qual fase do pico de vendas?

1. Captura
2. Aquecimento
3. Lembrete
4. Venda
5. Remarketing

Digite o número:
```

**Se Captura ou Aquecimento. perguntar em sequência (uma por vez):**

```
Qual o nome do evento?
(ex: "Workshop Tarô Desperto", "Semana da Leitura Segura")
```

```
Qual a promessa do evento?
(ex: "Aprender a fazer sua primeira tiragem completa em 3 dias")
```

```
Qual a data do evento?
(ex: "dia 15 de abril", "de 21 a 25 de maio")
```

```
Você tem uma foto sua (expert/criador) para usar no anúncio?
A foto aparece no criativo para gerar autoridade e conexão.

1. Sim, está em meus-produtos/{ativo}/entregas/paginas/assets/ (informar nome do arquivo)
2. Sim, vou colar o caminho completo
3. Não tenho agora (seguir sem foto)

Digite o número:
```

Se o usuário informar a foto, guardar o caminho para usar no JSON como `expert_photo`.
Se não tiver, seguir sem foto (o layout-evento funciona com e sem).

**Se Venda ou Remarketing. perguntar:**

```
Qual é a oferta?
(ex: "Curso Tarô em Duas Pontes por R$ 497 com bônus exclusivo até domingo")
```

---

**Confirmação antes de gerar (para qualquer caminho):**
```
Resumo do que vou criar:
- Tipo: [perpétuo ou pico de vendas]
- Objetivo/Fase: [objetivo ou fase]
- Momento: [momento de consumo, se perpétuo]
- Formato: [tipo de anúncio. se vídeo: "Vídeo (duração definida após pesquisa de tendências)"]
- [dados do evento ou oferta, se aplicável]
- Quantidade: 3 variações com tipos diferentes da Mandala da Criatividade

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

**REGRA:** nunca indicar duração do vídeo no resumo de confirmação. A duração é definida apenas na geração da copy.

### 3. Regras de Copy

**Fonte única e obrigatória:** antes de escrever qualquer gancho, desenvolvimento ou CTA, leia `.claude/skills/revisora/references/manual-copy.md`. É ali que vivem o princípio central, os **15 princípios fundamentais**, os **20 vícios proibidos** e o **checklist final (Blocos A/B/C/D)**. Toda variação passa pelo `revisora` antes de virar entregável.

**Reforços específicos de anúncio:**
- **Gancho nos primeiros 3 segundos:** afirmação contra-intuitiva, paradoxo, revelação ou quebra-padrão. NUNCA pergunta, NUNCA frase óbvia.
- **Inimigo concreto ou método antigo:** o anúncio precisa de um culpado externo (sistema, método ensinado, mito do nicho), não "você é o problema".
- **Entregar valor real no próprio post/vídeo:** a pessoa que lê ou assiste aprende algo concreto. Anúncio que só promete não converte.
- **Produto não aparece no gancho:** nada de "curso", "treinamento", nome do método nos 3s iniciais. Só a realidade do leitor.
- **CTA adequado à fase do funil** (ver tabela abaixo).

**Estrutura obrigatória para TODO vídeo (~45. 60s / ~150. 200 palavras):**

```
[0. 3s]   GANCHO      → Afirmação contra-intuitiva ou quebra-padrão.
                       Texto na tela + fala simultâneos.
[4. 15s]  TEASE       → Expande o gancho, cria tensão, contextualiza o problema.
[16. 42s] ENTREGA     → Ensina, demonstra ou revela algo real e concreto.
                       NUNCA apenas prometer. ENTREGAR dentro do vídeo.
[43. 48s] REGANCHO    → Texto na tela sintetizando a ideia central
                       (âncora visual para quem assiste sem som).
[49. 55s] CTA         → Convite direto adequado à fase. Sem urgência forçada.
```

**Para Descoberta especificamente:** duração alvo de 35. 45s. Para Captura, Conversão e demais fases: 45. 60s.

Calibrar a duração a partir dos virais encontrados na pesquisa. usar duração similar às referências.

**Três estruturas de roteiro baseadas em virais 2026:**

| Estrutura | Quando usar | Lógica de retenção |
|---|---|---|
| **Loop Perfeito** | Revelação, insights | O final conecta ao gancho. incentiva replay |
| **Tutorial de 3 Passos** | Procedimento, ensino | Cada passo avança a narrativa. pessoa assiste até o fim para completar |
| **Quebra-Padrão** | Contraste, paradoxo | Começo inesperado para o cérebro. força a pausa no scroll |

Usar estruturas diferentes nas 3 variações sempre que possível.

### 4. Geração (após aprovação do resumo)

Use a Mandala de 18 Tipos (skill vtsd-completo):

**Para Meta Ads, gere 3 variações usando tipos diferentes da Mandala da Criatividade:**
- Variação 1: [tipo escolhido]. ex: Comparação, Certo vs Errado
- Variação 2: [tipo escolhido]. ex: Prova, Demonstração
- Variação 3: [tipo escolhido]. ex: Problema-Solução, Curiosidade

**Cada variação inclui:**
- Texto principal (Light Copy. sem ponto de exclamação, sem perguntas no gancho)
- Headline (máx 40 caracteres)
- Descrição
- CTA adequado à fase

**Visual da variação. NÃO escreva direção criativa nesta skill.** Após apresentar as 3 variações de copy e o aluno aprovar, **acione automaticamente a skill `criativo-estatico`** (uma vez por variação) passando o headline, o gancho e o tom de cada variação como contexto. A `criativo-estatico` é responsável por gerar o prompt visual final pronto para colar no ChatGPT (ou outra IA escolhida pelo aluno). A `copy-anuncio` cuida só da copy. nunca duplica o trabalho de prompt visual.

**CTAs por fase:**
| Fase | CTA típico (texto na copy) | Botão Meta Ads (default) |
| --- | --- | --- |
| Descoberta | Seguir, curtir, comentar, compartilhar | LEARN_MORE (Saiba mais) |
| Relacionamento | Comentar, DM, salvar, lives | LEARN_MORE (Saiba mais) |
| Captura / Aquecimento | Quero participar, garantir minha vaga, me inscrever | SIGN_UP (Cadastre-se) |
| Conversão / Venda | Saiba mais, conheça o método, ver oferta | LEARN_MORE (Saiba mais) |
| Remarketing | Saiba mais, retomar oferta, última chance | LEARN_MORE (Saiba mais) |

**Default obrigatório do botão Meta Ads:** `LEARN_MORE` (Saiba mais). Esse é o CTA padrão para todas as fases salvo Captura/Aquecimento (que usa `SIGN_UP`). Não usar `SHOP_NOW` por default. O aluno pode trocar manualmente se quiser, mas a skill nunca sugere outro CTA sem ser perguntada.

**Estrutura de todo anúncio VTSD (texto/legenda). padrão de profundidade obrigatório:**
- **GANCHO:** premissa não óbvia. NUNCA uma pergunta, NUNCA algo óbvio para quem já está no nicho. 1. 2 frases fortes.
- **DESENVOLVIMENTO:** mínimo 2 parágrafos substanciais com argumento específico, concreto e não óbvio. Não pode ser resumo vago. precisa entregar valor por si só, mesmo sem o vídeo. Raso, curto e genérico são proibidos.
- **CTA:** convite direto adequado à fase do funil

**REGRA DE QUALIDADE:** todo anúncio deve entregar valor real. Nenhum anúncio pode ser óbvio, raso ou curto demais. O desenvolvimento deve ter profundidade suficiente para que a pessoa aprenda, entenda ou se reconheça. mesmo lendo só a legenda, sem ver o vídeo.

**Exemplos de gancho ERRADO:**
- "Sabe aquela sensação de travar na leitura?" ❌ (pergunta)
- "Você já se sentiu insegura com o tarô?" ❌ (pergunta)
- "Aprender tarô é difícil." ❌ (óbvio)
- "Você não sabe quanto cobrar?" ❌ (pergunta + óbvio)
- "Cobrar é difícil para tarotistas." ❌ (óbvio)

**Exemplos de gancho CERTO:**
- "A leitora que mais trava raramente é a que sabe menos." ✓ (contra-intuitivo)
- "Decorar os 78 significados é o caminho mais rápido para travar na leitura." ✓ (paradoxo)
- "Você não trava na tiragem por saber pouco. Você trava porque aprendeu na ordem errada." ✓ (revelação)
- "Parei de estudar os significados das cartas por 30 dias. Minha leitura melhorou." ✓ (quebra-padrão)
- "O método que todo mundo ensina primeiro no tarô é o que mais gera travamento na leitura real." ✓ (premissa não óbvia)

**Para Google Ads:**
- 15 títulos (máx 30 caracteres)
- 4 descrições (máx 90 caracteres)
- Palavras-chave + negativas

### 5. Aprovação

Após mostrar os anúncios gerados, perguntar:

```
1. Aprovar e salvar
2. Quero ajustar algo
```

Só salvar após aprovação do usuário.

### 6. Salvar Copy
`meus-produtos/{ativo}/entregas/criativos/anuncios-meta-[formato]-[objetivo]-[produto].md`

### 7. Geração Visual (imagem, vídeo ou carrossel)

Após salvar a copy, gere automaticamente os visuais usando `scripts/generate-creative.py`.

**Gerar o JSON de config** com os slides/imagens e rodar o script. O texto vem do HTML template, a IA gera apenas o BACKGROUND visual.

**REGRA ABSOLUTA PARA PROMPTS DE IA (backgrounds):**
- NUNCA pedir texto, números, letras, datas ou caracteres legíveis no prompt
- NUNCA pedir calendários, relógios com números, telas com texto visível
- SEMPRE incluir no final: "no text, no numbers, no readable characters, no logos"
- O background deve ser uma CENA, TEXTURA ou ATMOSFERA, nunca um design com informação
- Todo texto visível no criativo final vem do template HTML, nunca da IA

**Para fase Captura/Aquecimento:** usar `layout-evento` no JSON. Inclui foto do expert (campo `expert_photo`), data em destaque, nome do evento e botão CTA.

---

**Se Imagem Estática:**

Para cada variação, monte um prompt de background baseado no tipo de anúncio e no nicho do produto. O prompt deve descrever:
- Cena ou atmosfera visual que reforça o clima da copy
- Estilo fotográfico (foto real, clean, minimalista, etc.)
- Paleta de cores alinhada ao produto
- Texto overlay com o headline da variação (quando aplicável)
- Proporção: 1:1 ou 4:5 para feed

Antes de gerar qualquer prompt, pergunte qual ferramenta a pessoa vai usar.

**Se o formato for Imagem Estática:**

```
Qual IA você vai usar para gerar a imagem?

1. Midjourney
2. ChatGPT (DALL-E)
3. Leonardo AI
4. Adobe Firefly
5. Canva AI (Magic Media)
6. Stable Diffusion / ComfyUI
7. Outra — me diga qual

Sugestão: para anúncios com pessoas reais e estética fotográfica, o Midjourney
e o Leonardo AI costumam entregar os melhores resultados. Para quem já usa o
Canva no dia a dia, o Canva AI é a opção mais prática.

Digite o número:
```

**Se o formato for Vídeo:**

```
Qual IA você vai usar para gerar o vídeo?

1. HeyGen (avatar com seu rosto ou avatar pronto — melhor para talking head)
2. Pika (geração de vídeo a partir de prompt — rápido e gratuito para começar)
3. Kling (vídeo realista, ótimo para cenas com pessoas)
4. RunwayML (controle avançado de edição e geração)
5. Luma Dream Machine (realismo alto, bom para ambientes e produtos)
6. Vou gravar eu mesmo — preciso do prompt como briefing de direção
7. Outra — me diga qual

Sugestão: se você quer um talking head com script lido por avatar, o HeyGen é
o mais indicado — ele aceita o roteiro direto. Se quiser gerar o vídeo a
partir de uma descrição visual, Pika ou Kling entregam resultados mais rápidos
sem precisar de configuração.

Digite o número:
```

---

**Geração do prompt adaptado para a IA escolhida:**

Após o usuário informar a IA, gere os prompts de cada variação otimizados para aquela ferramenta específica. Use a sintaxe, estrutura e vocabulário que aquela IA melhor interpreta. Referências por ferramenta:

**Midjourney:**
- Estrutura: `[descrição da cena], [estilo], [iluminação], [câmera/ângulo], [paleta], [referência de fotógrafo ou artista se aplicável] --ar 1:1 --v 6 --style raw`
- Para 9:16: `--ar 9:16`
- Evitar verbos de ação — descrever o estado visual resultante
- Incluir termos técnicos de fotografia: `shallow depth of field`, `soft side lighting`, `editorial photography`

**ChatGPT (DALL-E):**
- Estrutura em parágrafo descritivo: "Create a photorealistic image of [cena]. The style is [estilo]. Lighting is [iluminação]. The composition shows [enquadramento]. Color palette: [paleta]. Aspect ratio: [proporção]."
- Linguagem mais direta e instrucional
- DALL-E não aceita parâmetros técnicos — tudo vai no texto corrido

**Leonardo AI:**
- Estrutura similar ao Midjourney mas sem parâmetros `--`
- Indicar o modelo a usar: `Leonardo Diffusion XL` para fotos realistas, `PhotoReal` para pessoas
- Separar elementos por vírgula: `[cena], [estilo fotográfico], [iluminação], [enquadramento], [paleta de cores]`
- Adicionar negative prompt separado: listar o que não deve aparecer

**Adobe Firefly:**
- Estrutura em inglês descritivo e simples, sem sintaxe especial
- Enfatizar o estilo com termos reconhecidos: `professional photography`, `studio light`, `clean background`
- Indicar proporção no campo de configuração, não no prompt

**Canva AI (Magic Media):**
- Prompts curtos e diretos em português ou inglês
- Descrever a cena principal + estilo visual em 1-2 frases
- Não suporta parâmetros técnicos — manter simples

**Stable Diffusion / ComfyUI:**
- Estrutura: `[qualidade: masterpiece, best quality, photorealistic], [cena], [estilo], [iluminação], [câmera]`
- Incluir negative prompt obrigatório: `(worst quality, low quality, blurry, distorted face:1.4), watermark, text`
- Indicar sampler e steps recomendados se relevante

**HeyGen:**
- Não gerar prompt de imagem — gerar o roteiro formatado para colar no campo de texto do avatar
- Incluir instruções de velocidade de fala, pausas e ênfases
- Formato: texto corrido com `[pausa]` e `[ênfase]` marcados no roteiro

**Pika:**
- Prompt em inglês descrevendo a ação e o visual da cena em movimento
- Estrutura: `[personagem/sujeito] [ação], [ambiente], [estilo cinematográfico], [iluminação], [câmera: movimento e ângulo]`
- Adicionar Motion Guidance se disponível: descrever o movimento específico esperado

**Kling:**
- Similar ao Pika — descrever cena em movimento
- Estrutura: `[cena inicial], [movimento da câmera], [ação do sujeito], [ambiente], [estilo], [iluminação]`
- Kling performa melhor com descrições de pessoas em ação realista

**RunwayML:**
- Estrutura: `[sujeito + ação], [ambiente detalhado], [estilo de câmera], [iluminação cinematográfica]`
- Indicar se é geração a partir de imagem (Image to Video) ou texto puro (Text to Video)
- Termos que funcionam bem: `cinematic`, `smooth camera movement`, `natural lighting`

**Luma Dream Machine:**
- Prompt focado na cena e atmosfera visual
- Estrutura: `[descrição da cena], [movimento da câmera], [iluminação], [atmosfera/humor visual]`
- Funciona melhor com descrições de ambientes e produtos — menos preciso com pessoas falando

**Se for gravar o próprio vídeo:**
- Gerar um briefing de direção completo em português
- Incluir: enquadramento, iluminação, postura, tom de voz, ritmo de fala, gestos, fundo, roupas recomendadas, texto na tela e momento de inserção

---

Apresente os prompts prontos para copiar e colar, um por variação.

Salve em: `meus-produtos/{ativo}/entregas/criativos/prompts-visuais-[formato]-[ia-escolhida]-[produto].md`

---

#### Opção 1 — Geração via API

**Se Imagem Estática:**

Monte o prompt de imagem para cada variação (mesma lógica descrita acima). Leia o `.env` do projeto e verifique se existe `FREEPIK_API_KEY`.

**Se existir**, gere via API:

```bash
# Imagem estática — para cada variação (substituir N pelo número):
curl -X POST "https://api.freepik.com/v1/ai/text-to-image" \
  -H "x-freepik-api-key: $FREEPIK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "PROMPT_VARIACAO_N", "num_images": 1, "image": {"size": "square_1_1"}}'
```
Salve cada imagem em: `meus-produtos/{ativo}/entregas/criativos/img-variacao-[N]-[produto].png`

Para stories: substitua `"size": "square_1_1"` por `"size": "portrait_9_16"`.
Para carrossel: repita para cada card, salvando `carrossel-card[N]-[produto].png`.

Salve em: `meus-produtos/{ativo}/entregas/criativos/img-variacao-[N]-[produto].png`

**Se não existir**, informe como configurar e ofereça a opção de prompt como alternativa imediata:

```
Não encontrei a chave do Freepik (Magnific) no .env. Você tem duas opções:

1. Configurar agora (leva 2 minutos) — eu te explico o passo a passo
2. Gerar os prompts para você colar em outra IA

Digite o número:
```

Se escolher opção 2: siga o fluxo da **Opção 2 — Gerar prompts para colar em IA** acima (perguntar qual IA antes de gerar).

**Como configurar o Freepik (Magnific) AI (gratuito para começar):**
1. Acesse freepik.com e crie uma conta gratuita (ou faça login)
2. Vá em: perfil > API Keys > Create API Key
3. Copie a chave gerada
4. Abra (ou crie) o arquivo `.env` na raiz deste projeto
5. Adicione a linha: `FREEPIK_API_KEY=sua_chave_aqui`
6. Salve o arquivo

Quando o usuário configurar, gere as imagens automaticamente.

---

**Se Vídeo:**

Use o roteiro aprovado de cada variação. Verifique no `.env` se existem as três variáveis:
- `HEYGEN_API_KEY`
- `HEYGEN_AVATAR_ID`
- `HEYGEN_VOICE_ID`

**Se todas existirem**, gere o vídeo via HeyGen:

```bash
curl -X POST "https://api.heygen.com/v2/video/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_inputs": [{
      "character": {
        "type": "avatar",
        "avatar_id": "HEYGEN_AVATAR_ID",
        "avatar_style": "normal"
      },
      "voice": {
        "type": "text",
        "input_text": "ROTEIRO_VARIACAO_N",
        "voice_id": "HEYGEN_VOICE_ID",
        "speed": 1.0
      },
      "background": {
        "type": "color",
        "value": "#f8f8f8"
      }
    }],
    "dimension": {"width": 1080, "height": 1920}
  }'
```

A API retorna um `video_id`. Faça polling a cada 30 segundos:

```bash
curl "https://api.heygen.com/v1/video_status.get?video_id=VIDEO_ID" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Quando status for `completed`, faça download do `video_url` e salve em:
`meus-produtos/{ativo}/entregas/criativos/video-variacao-[N]-[produto].mp4`

**Se faltar alguma variável**, informe e ofereça alternativa imediata:

```
Não encontrei as chaves do HeyGen no .env. Você tem duas opções:

1. Configurar agora — eu te explico o passo a passo (leva 5 minutos)
2. Gerar os prompts para você usar em outra IA de vídeo

Digite o número:
```

Se escolher opção 2: siga o fluxo da **Opção 2 — Gerar prompts para colar em IA** acima (perguntar qual IA antes de gerar).

**Como configurar o HeyGen:**

**Passo 1. Criar conta e pegar a chave da API:**
1. Acesse heygen.com e crie uma conta (plano gratuito tem créditos de teste)
2. No painel, clique no seu perfil (canto superior direito) > API
3. Clique em "Create API Key", dê um nome e copie a chave

**Passo 2. Pegar o ID do seu avatar:**
1. No painel HeyGen, vá em Avatars (menu lateral)
2. Escolha um avatar ou crie o seu com sua foto
3. Clique no avatar e copie o "Avatar ID" exibido nos detalhes

**Passo 3. Pegar o ID da voz:**
1. No painel HeyGen, vá em Voices (menu lateral)
2. Filtre por idioma: Portuguese (Brazil)
3. Ouça as opções e escolha a que mais combina com seu estilo
4. Copie o "Voice ID" da voz escolhida

**Passo 4. Configurar no projeto:**
1. Abra (ou crie) o arquivo `.env` na raiz deste projeto
2. Adicione as três linhas:
```
HEYGEN_API_KEY=sua_chave_aqui
HEYGEN_AVATAR_ID=id_do_avatar_aqui
HEYGEN_VOICE_ID=id_da_voz_aqui
```
3. Salve o arquivo

Quando o usuário configurar, gere os vídeos automaticamente.

---

### 8. Próximo Passo
"Anúncios e visuais salvos em [caminho]. Use `/copy-pagina` para criar a página de destino, ou `/criativo-estatico` para gerar mais visuais para a campanha."

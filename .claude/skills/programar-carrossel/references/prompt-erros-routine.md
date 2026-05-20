# Prompt-base. Carrossel Erros (versão para tarefa programada)

> Versão autônoma do prompt Erros (original em `carrossel/references/prompt-erros.md`), adaptada para rodar sem interação humana dentro de uma Routine do `/schedule`.
> A skill `/programar-carrossel` substitui os placeholders `{{...}}` por valores coletados na entrevista antes de criar o agendamento.
>
> O que muda em relação à versão interativa: não há coleta (os 6 dados vêm fixos no cabeçalho, incluindo o Desejo do público); não há gate de aprovação do texto (a tarefa entrega direto); e os arquivos `prompts.txt` e `legenda.txt` não são salvos no disco (a tarefa roda na nuvem). Todo o conteúdo (6 slides + 6 prompts visuais + legenda) é entregue no chat do painel de Routines. Todo o resto (estrutura dos 6 slides, critério CONTRAINTUITIVO + PRÁTICO + FUNCIONAL + SABOTADOR, regras da CTA, tamanho do texto, regras da legenda, template de prompt de imagem) é idêntico ao prompt original.

---

## Placeholders

| Placeholder | Origem | Exemplo |
|---|---|---|
| `{{HANDLE}}` | Coleta | `@nutrireal` |
| `{{NICHO_PRODUTO}}` | Coleta | `nutrição para emagrecimento sustentável, mentoria de 12 semanas` |
| `{{CORES_MARCA}}` | Coleta | `creme bege #F2EAD9 + verde-sálvia escuro #3D4A3F` ou `DEFAULT` |
| `{{TOM_FIXO}}` | Coleta | `Clássica/profissional`, `Bem-humorada`, ... ou `LIVRE` |
| `{{ESTILO_DESIGN}}` | Coleta | `Sofisticado e elegante`, `Editorial e cinematográfico`, ... |
| `{{DESEJO}}` | Coleta (pergunta extra do Erros) | `emagrecer 10 kg sem dieta restritiva`, `passar em concurso público em 1 ano`, `atrair primeiros 10 clientes pagantes` |
| `{{DATA_HOJE_REF}}` | Calculado em runtime | `[calcule a data de hoje no início da execução]` |

---

## Prompt final injetado na tarefa programada

```
Você é um especialista em criação de carrosséis virais no estilo
"Erros comuns para quem quer {{DESEJO}}" para Instagram. Seu trabalho
é gerar 1 carrossel de 6 slides que expõe erros que sabotam a pessoa
que persegue o desejo específico declarado, com ideias
contraintuitivas, práticas e funcionais, pronto para postar.

Esta tarefa roda sozinha, na nuvem, sem ninguém para responder
perguntas. NÃO pergunte nada. Execute todas as etapas direto, em ordem.

Contexto fixo do criador (já validado, não pergunte de novo):
- Instagram: {{HANDLE}}
- Nicho e produto: {{NICHO_PRODUTO}}
- Cores da marca: {{CORES_MARCA}} (se "DEFAULT", use creme bege #F2EAD9 nos slides 1-5 e verde-sálvia escuro #3D4A3F no slide 6)
- Tom da copy: {{TOM_FIXO}} (se "LIVRE", escolha sozinho o tom mais adequado ao tema)
- Estilo de design visual: {{ESTILO_DESIGN}}
- Desejo concreto do público (alvo de TODOS os erros): {{DESEJO}}

A data de hoje é {{DATA_HOJE_REF}}.

---

## Etapa 1. Geração dos 6 slides (texto)

Crie um carrossel adaptando o estilo de escrita ao tom escolhido.

### Adaptação por tom

Clássica → direta/elegante; bem-humorada → trocadilhos/ironia; técnica
→ dados; inspiracional → aspiracional; casual → conversa de amigo;
polêmica → provocações.

### Estrutura dos slides

- Slides 1-5: cada slide apresenta UM erro. Título começa com
  "Erro #N:" seguido do erro descrito como ação que a pessoa faz
  achando que está certa. Subtítulo explica por que esse
  comportamento sabota {{DESEJO}}.
- Slide 6: CTA criativa que promete eliminar os erros e atingir
  {{DESEJO}}.

### Critério das ideias — REGRA CENTRAL

CONTRAINTUITIVO + PRÁTICO + FUNCIONAL + SABOTADOR DO DESEJO:

- CONTRAINTUITIVO: vai contra o que a pessoa que quer {{DESEJO}}
  acredita.
- PRÁTICO: erro real, específico, com exemplo concreto.
- FUNCIONAL: a pessoa entende o que fazer diferente.
- SABOTADOR: cada erro precisa atrasar ou impedir {{DESEJO}}
  especificamente.

A cada execução desta tarefa, escolha um ângulo NOVO dentro do estilo
Erros, evitando repetir temas de execuções anteriores. Use a pesquisa
do nicho e o conhecimento público do mercado de "{{NICHO_PRODUTO}}"
pra encontrar erros frescos que cumprem o critério central e que
sabotam especificamente "{{DESEJO}}".

### Regras OBRIGATÓRIAS da CTA (slide 6)

1. MOTIVO CLARO.
2. RELAÇÃO DIRETA com os 5 erros e com {{DESEJO}}.
3. GERAÇÃO DE DESEJO.

Exemplos certos:
- "Siga {{HANDLE}} e alcance {{DESEJO}} sem repetir os erros que
  travam 90% das pessoas."
- "Siga {{HANDLE}} e elimine os erros que estão te afastando de
  {{DESEJO}}."

Exemplos errados (não usar):
- "Siga {{HANDLE}} para mais conteúdos."
- "Siga e fique por dentro."

### Tamanho do texto por slide

Máximo ~25 palavras. TÍTULO até 10 palavras (incluindo "Erro #N:") +
SUBTÍTULO até 15 palavras.

NÃO peça aprovação. Execute direto.

---

## Etapa 2. Output dos 6 prompts visuais

Após os 6 slides, gere os 6 prompts de imagem individualmente no chat,
um por slide, na ordem Slide 1 → Slide 6. Cada prompt completo, em
inglês, pronto para o usuário copiar e colar no ChatGPT. Use o
TEMPLATE DE PROMPT DE IMAGEM abaixo.

### Template do prompt de imagem (inglês)

Create a 4:5 aspect ratio (1080x1350px) Instagram carousel slide.

COMPOSITION (two horizontal blocks):
- TOP BLOCK (~55% of canvas height): photographic image —
  [DESCRIÇÃO DA FOTO COERENTE COM O SLIDE: cena que sugere sutilmente
  o erro/comportamento sabotador descrito, sem rosto humano visível
  ou apenas de costas/perfil]. Cinematic naturalistic lighting,
  real-world textures, shallow depth of field, slight film grain,
  no stock-photo plasticity.
- BOTTOM BLOCK (~45% of canvas height): solid color background
  [HEX_COR_FUNDO_BLOCO_INFERIOR].

TYPOGRAPHY (rendered DIRECTLY on the canvas as the dominant graphic
element):
- Render the EXACT Portuguese text below, with perfect letterforms and
  ALL accent marks intact (á é í ó ú â ê î ô û ã õ ç ü):
  - TITLE: "[TÍTULO_EXATO_DO_SLIDE — incluindo "Erro #N:" no início]"
  - SUBTITLE: "[SUBTÍTULO_EXATO_DO_SLIDE]"
- Title typography: [família tipográfica conforme tabela de estilo],
  color [HEX_COR_TEXTO_TITULO], occupying ~28-35% of the bottom block
  height, left-aligned ragged-right, leading 1.0-1.05. The "Erro #N:"
  prefix can be visually emphasized (different color or weight) if it
  serves the design.
- Subtitle typography: same family as title, lighter weight (regular or
  medium), ~35-40% of the title size, color [HEX_COR_TEXTO_SUBTITULO],
  left-aligned ragged-right, leading 1.3.
- Both texts respect 80px safe margin from canvas edges.
- Page indicator "[N]/6" in small uppercase tracking +100, top-right
  corner of the bottom block, ~24px size.

STYLE DIRECTION: [tradução visual de "{{ESTILO_DESIGN}}"].

CRITICAL TEXT RENDERING RULES (DO NOT SKIP):
- The image MUST contain the title and subtitle text rendered directly
  on the canvas, visible and perfectly legible. An image WITHOUT the
  rendered text is INVALID — do not return it.
- Render the EXACT Portuguese strings provided above. Do not paraphrase,
  translate, abbreviate, or invent text. Do not substitute words.
  The "#" symbol and the slide number must be rendered correctly.
- All letters must be perfectly formed with correct Portuguese accent
  marks. No garbled characters, no mirrored letters, no missing or
  broken accents.
- Typography is the PROTAGONIST of this composition.
- If text rendering would fail, return an error instead of an image
  without text.

QUALITY:
- Photographic realism in the top block — no 3D cartoon, no
  illustration, no AI-painterly aesthetic.
- Clean, intentional composition with breathing room.
- Output: high-resolution 1080x1350 PNG.

### Tradução do estilo de design (uso interno, aplicar no campo STYLE DIRECTION acima)

| Estilo | Tradução visual |
|---|---|
| Sofisticado e Elegante | Tipografia serifada, espaçamento generoso, paleta neutra, sem elementos decorativos |
| Editorial e Cinematográfico | Layout de revista, hierarquia tipográfica forte, espaço negativo, sofisticação |
| Despojado e Bem-humorado | Tipografia bold/rounded, cores mais vivas, elementos gráficos lúdicos |
| Energético e Vibrante | Tipografia condensada/impactante, cores fortes, energia gráfica alta |
| Sério e Técnico | Grid rígido, tipografia mono ou sans-serif limpa, dados visuais, ícones funcionais |
| Aconchegante e Humano | Tipografia casual/manuscrita, paleta quente, elementos orgânicos, atmosfera acessível |
| Provocativo e Ousado | Tipografia bold com peso, cores cruas, contraste alto, zero decoração |
| Descrição Livre | Traduzir a descrição do usuário em diretrizes visuais equivalentes |

---

## Etapa 3. Legenda do Instagram

Após os 6 slides e os 6 prompts visuais, gere a legenda do post pronta
para o usuário copiar e colar no Instagram.

### Regras obrigatórias (Manual da Copy)

- Zero travessões (—), zero pontos de exclamação, zero "Não é X. É Y.",
  zero perguntas no gancho ou na primeira linha, zero "mesmo que" e
  "sem precisar" como muleta, zero emojis, sem nome de produto, curso,
  método ou sigla nas primeiras linhas.
- A legenda entrega aprendizado, não promessa vaga.
- Número, prazo, cenário ou detalhe concreto. Zero generalização.
- Toda afirmação tem mecanismo, comparação antes/depois ou explicação
  do porquê.
- Mira a dor real do público, não a superficial.
- Tese obrigatória: a legenda explica POR QUE os erros do carrossel
  sabotam {{DESEJO}}. Não repete os slides.

### Estrutura da legenda

1. Gancho (1 a 2 linhas). Afirmação que abre o tema sem repetir o
   slide 1 do carrossel.
2. Desenvolvimento (3 a 6 linhas). Argumenta o ponto central com
   mecanismo, comparação ou exemplo concreto, conectando à sabotagem
   de {{DESEJO}}. Traz informação que NÃO está nos slides.
3. Ponte para o carrossel (1 linha). Indica que o conteúdo prático
   está nos slides.
4. CTA final (1 linha). Chamada para seguir o {{HANDLE}} + ação
   (salvar, comentar ou compartilhar) conectada com {{DESEJO}}.
5. Hashtags (opcional, até 5). Relevantes ao nicho, no final,
   separadas por espaço.

### Tom

Mesmo tom definido em {{TOM_FIXO}}. A legenda é continuação natural do
carrossel, não resumo.

### Tamanho

Entre 600 e 1200 caracteres (sem contar hashtags). Garantir que o CTA
caia ANTES do "...mais" do Instagram cortar.

---

## Etapa 4. Encerramento

Encerre com a mensagem:

> Carrossel "Erros" gerado para {{NICHO_PRODUTO}}, com foco em
> sabotar o desejo "{{DESEJO}}".
> Texto dos 6 slides + 6 prompts visuais em inglês + legenda do
> Instagram entregues acima.
> Pra postar, copie os 6 prompts visuais (um por slide) e cole no
> ChatGPT para gerar as 6 imagens, depois monte o carrossel no
> Instagram com a legenda.
```

---

## Como a skill monta o prompt final

A skill `/programar-carrossel`, no ramo Erros, usa este arquivo INTEIRO como prompt-base (não concatena Bloco A/B/C/D do `prompts-routine.md`, que serve apenas aos clássicos ainda não migrados — Sempre, Odeio, Amo, Ninguém Conta). Substitui os 7 placeholders pelos valores coletados na entrevista (incluindo o `{{DESEJO}}`, que é a pergunta extra do estilo Erros) e envia para o `/schedule create`.

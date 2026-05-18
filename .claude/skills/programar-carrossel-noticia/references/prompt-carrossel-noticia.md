# Referência. Prompt parametrizado do carrossel de notícia

> Este é o prompt-base que a skill `programar-carrossel-noticia` injeta na tarefa programada do `/schedule`.
> A skill substitui os placeholders `{{...}}` pelos valores coletados na entrevista antes de mandar para o `/schedule create`.

---

## Placeholders

| Placeholder | Origem | Exemplo |
|---|---|---|
| `{{HANDLE}}` | Entrevista (Passo 1) | `@leandroladeiran` |
| `{{NICHO}}` | Entrevista (Passo 1) | `surf` |
| `{{PRODUTO}}` | Entrevista (Passo 1) | `Mentoria Surf Pro, mentoria online de 8 semanas para surfistas intermediários` |
| `{{ESCOPO}}` | Passo 2 | `BUSCA` ou `CARROSSEL_INTEIRO` |
| `{{MODO}}` | Passo 3 (só se ESCOPO=CARROSSEL_INTEIRO) | `ALEATORIO` ou `FIXO` |
| `{{CATEGORIA_FIXA}}` | Passo 4 (só se MODO=FIXO e o aluno travou categoria) | `TREND`, `ATEMPORAL` ou `LIVRE` |
| `{{TOM_FIXO}}` | Passo 4 (só se MODO=FIXO e o aluno travou tom) | `Enérgico`, `Polêmico`, `Engraçado`, `Reflexivo`, `Didático`, `Jornalístico`, `Confessional` ou `LIVRE` |
| `{{DATA_HOJE_REF}}` | Calculado em runtime pela própria tarefa programada | `2026-05-13` |

---

## Bloco A. Cabeçalho fixo do prompt

Este bloco entra sempre, independente do escopo.

```
Você é especialista em carrosséis virais para Instagram, treinado em
narrativa de revista (entretenimento + educação) e técnicas de retenção
de jornal (curiosidade, gancho, suspense). Sua missão é gerar um
carrossel que conecta uma notícia ou curiosidade com o nicho do
criador e termina puxando seguidor para o perfil.

Contexto fixo do criador (já validado, não pergunte de novo):
- Instagram: {{HANDLE}}
- Nicho: {{NICHO}}
- Produto: {{PRODUTO}}

A data de hoje é {{DATA_HOJE_REF}}. Use essa data como referência para
qualquer filtro de frescor de notícia.
```

---

## Bloco B. Busca de notícias (sempre executa)

```
ETAPA 1. Buscar 6 ideias de notícia para o nicho

Faça DUAS buscas separadas na web. As regras são diferentes para cada
categoria.

### Categoria A. NOTÍCIA TREND (últimos 7 dias)

- Aceitar APENAS notícias publicadas nos últimos 7 dias contados a
  partir de {{DATA_HOJE_REF}}.
- Priorizar as últimas 24 a 48 horas.
- Se a data de publicação não estiver dentro da janela, descarte.
  Não reciclar notícia velha.
- Operadores sugeridos: "{{NICHO}} notícia hoje", "{{NICHO}} essa
  semana", "{{NICHO}} últimas notícias [mês corrente] [ano corrente]".
- Filtro "Past week" no Google quando disponível.
- Se NADA quente apareceu no nicho nos últimos 7 dias: pular para
  6 atemporais e avisar isso no topo da resposta.

### Categoria B. NOTÍCIA ATEMPORAL (sem prazo)

- Curiosidades, fatos chocantes, dados contraintuitivos, descobertas
  históricas, recordes, estatísticas inusitadas do nicho.
- A matéria pode ter sido publicada há meses ou anos. O critério é
  "ainda gera curiosidade hoje".
- Critério extra: tem componente de surpresa OU contradiz crença
  comum OU cita número ou recorde específico.

### Regras de fonte

- TODAS as 6 ideias precisam de URL real e direta da matéria
  (não a home do site, não placeholder).
- Se não conseguir validar uma URL, DESCARTE essa ideia e busque outra.
- Não inventar URL. Não inventar título. Se nenhuma fonte verificável,
  diga isso na resposta.
- Se a fonte é em outra língua, traduza o título e o gancho para
  português brasileiro antes de apresentar.

### Formato de apresentação

NOTÍCIAS TREND (últimos 7 dias)

1. [título] — publicada em [DD/MM/AAAA]
   Gancho: [como conecta com o nicho do criador]
   Fonte: [URL completa]

2. [...]

3. [...]


NOTÍCIAS ATEMPORAIS (curiosidades sem prazo)

1. [título]
   Gancho: [como conecta com o nicho do criador]
   Fonte: [URL completa]

2. [...]

3. [...]

Se TREND vier vazia, apresente só 6 Atemporais (numeradas 1 a 6) com
o aviso: "Nada quente nos últimos 7 dias no nicho {{NICHO}}. Vamos
com 6 ideias de Notícia Atemporal."
```

---

## Bloco C-BUSCA. Final do escopo "só busca"

> Entra no prompt SE `{{ESCOPO}} == BUSCA`. Substitui o Bloco C-CARROSSEL.

```
ETAPA 2. Encerrar aqui

Após apresentar as 6 ideias com fontes, encerre com este texto exato:

---

📰 Notícias encontradas para {{NICHO}} em {{DATA_HOJE_REF}}.

Para transformar uma delas em carrossel completo, abra o Claude Code
e rode /programar-carrossel-noticia escolhendo "Gerar carrossel
inteiro" no Passo 2, ou cole uma das 6 fontes acima em qualquer chat
do Workshop e peça "transforma essa notícia em carrossel".

---

Não escreva slides. Não gere prompts visuais. A tarefa acabou aqui.
```

---

## Bloco C-CARROSSEL. Final do escopo "carrossel inteiro"

> Entra no prompt SE `{{ESCOPO}} == CARROSSEL_INTEIRO`. Substitui o Bloco C-BUSCA.

### C-CARROSSEL.1. Seleção automática

```
ETAPA 2. Selecionar notícia e tom

Modo de seleção: {{MODO}}

Se {{MODO}} == ALEATORIO:
  - Notícia. Escolha a ideia com maior potencial viral entre as 6.
    Critério: combinação de frescor (matérias Trend de 24 a 48h
    pesam mais), tensão narrativa (escândalo, virada, recorde) e
    conexão direta com o nicho do criador.
  - Tom. Escolha o tom mais adequado à matéria escolhida entre as 7
    opções (Enérgico, Polêmico, Engraçado, Reflexivo, Didático,
    Jornalístico, Confessional). Justifique a escolha em 1 frase.

Se {{MODO}} == FIXO:
  - Filtre as 6 ideias pela categoria travada: {{CATEGORIA_FIXA}}.
    Se {{CATEGORIA_FIXA}} == LIVRE, considere as 6.
    Se {{CATEGORIA_FIXA}} == TREND, considere só as 3 Trend.
    Se {{CATEGORIA_FIXA}} == ATEMPORAL, considere só as 3 Atemporais.
  - Dentro do filtro, escolha a ideia com maior potencial viral
    pelos mesmos critérios acima.
  - Tom. Use {{TOM_FIXO}}. Se {{TOM_FIXO}} == LIVRE, escolha o tom
    mais adequado entre as 7 opções e justifique em 1 frase.

Escreva 1 parágrafo curto explicando qual notícia e qual tom foram
escolhidos antes de seguir para o carrossel.
```

### C-CARROSSEL.2. Geração do texto

```
ETAPA 3. Escrever o carrossel

Pilares obrigatórios:

1. Capa magnética e clara. Frase curta. Transmite a notícia REAL em
   até 8 palavras (quem é o protagonista, o que aconteceu, onde).
   Permitido subtítulo curto abaixo com a pegada do tom escolhido.
   Errado: "Os outros pediram pra trocar de continente." Certo:
   "Brasil ganhou tudo no Pan-Americano de Surf" + subtítulo irônico.

   Exceção para tons Reflexivo (4) e Confessional (7): capa de duas
   linhas. Primeira com o fato em 8 palavras. Segunda com a pegada
   reflexiva ou confessional.

2. Retenção a cada slide. Cada slide termina com motivo para virar
   o próximo (frase suspensa, virada, dado parcial, "mas").

3. Narrativa de revista. Conta a história como matéria curta:
   contexto, virada, dado, lição. Não é lista.

4. Fechamento que puxa o nicho. Conecta a história com a transformação
   que o produto entrega, sem vender direto.

Formato:

- 7 a 9 slides.
- 2 a 3 parágrafos curtos por slide. Nunca mais.
- Último slide: CTA fixo com este texto exato:

  Todos os dias, conteúdo sobre {{NICHO}} aqui no {{HANDLE}}.

  Me segue para receber a próxima.

Proibições absolutas de copy:

- Sem travessão.
- Sem ponto de exclamação.
- Sem pergunta na capa.
- Sem "não é X, é Y".
- Sem promessa vazia. Toda afirmação tem dado, prazo ou cena concreta.
- Sem mencionar o produto na narrativa. O produto só aparece implícito
  no nicho do CTA final.
- Sem lero-lero. Palavra genérica que sobrevive trocada por outra
  palavra genérica do nicho não pode existir. Se a frase ainda faz
  sentido trocando "essência" por "padrão" ou "jornada" por "caminho",
  reescreva com dado, cena ou número.
- Tom escolhido mantido em TODOS os slides.
- Português brasileiro com acentuação correta.

Entregue o texto formatado:

SLIDE 1 (CAPA)
[texto]

SLIDE 2
[texto]

...

SLIDE N (CTA)
Todos os dias, conteúdo sobre {{NICHO}} aqui no {{HANDLE}}.

Me segue para receber a próxima.
```

### C-CARROSSEL.3. Prompts visuais

```
ETAPA 4. Gerar prompts visuais slide a slide

Estratégia em 3 modos:

MODO 1. Composição com foto real
- Slides com pessoa, local ou evento NOMEADO na história.
- Code Interpreter (Python + Pillow + requests) busca URL, baixa
  e compõe PNG.

MODO 2. Geração ilustrativa
- Slides com cena genérica (metáfora visual, abstrato, objeto,
  silhueta sem rosto identificável).
- DALL-E gera direto a partir da descrição.

MODO 3. Composição limpa
- Slide CTA. Apenas cor sólida e texto.
- Code Interpreter compõe com Pillow.

Regra de decisão:
- Slide 1 (capa). Quase sempre Modo 1.
- Slides com personagem ou local nomeado. Modo 1.
- Slides com cena genérica ou metafórica. Modo 2.
- Slide CTA. Modo 3.

Plano B do Modo 1:
- Se nenhuma URL acessível em 2 tentativas, cai pro Modo 2 com
  descrição visual genérica (sem nomear pessoa real).

Limite duro de texto na arte do Modo 2:
- Máximo 8 palavras renderizadas direto na imagem.
- Texto longo vai pra caption do Instagram, não pra arte.

Regras visuais comuns a todos os modos:
- 1080x1350 pixels (4:5 vertical).
- Sem ícones, sem formas geométricas decorativas, sem emoji na arte.
- Paleta de 3 cores em hex, idêntica no carrossel inteiro.
- Tipografia serif editorial.

Para cada slide, gere um BLOCO SEPARADO em código com a estrutura
do modo escolhido. Separe slides com linha horizontal `---`.

Estrutura do MODO 1 (foto real):

  Use o Code Interpreter (Python + Pillow + requests) para MONTAR
  este slide, não para gerar do zero. A foto precisa ser a foto real,
  não interpretada.

  PASSO 1. Buscar fotos reais.
  Faça uma busca na web e encontre URLs acessíveis (Wikimedia
  Commons, sites oficiais de imprensa, redes sociais públicas
  oficiais) de:
  - [pessoa, local ou evento 1]
  - [pessoa, local ou evento 2]
  Liste as URLs encontradas. Se nenhuma URL funcionar em 2 tentativas,
  troque este slide para Modo 2.

  PASSO 2. Baixar e compor.
  [especificação técnica em pixels: canvas, faixas, posicionamento
  de fotos, tipografia em pontos com fonte serif do sistema,
  cores hex, margens, tratamento de cor com leve dessaturação
  e granulação]

  PASSO 3. Salvar.
  Salve como slide-N-papel.png.

  PALETA: [3 cores em hex].

Estrutura do MODO 2 (DALL-E):

  Crie uma imagem editorial vertical 4:5 (1080x1350 pixels) estilo
  cinematográfico.

  CENA: [descrição cinematográfica: personagem genérico, ação,
  ambiente, luz, lente, paleta].

  COMPOSIÇÃO: [como a imagem é dividida espacialmente].

  TEXTO QUE DEVE APARECER NA IMAGEM (português brasileiro, fonte
  serif editorial, máximo 8 palavras):
  [função do texto, cor hex]: [texto exato]

  PALETA: [3 cores em hex].

  Sem ícones, sem formas geométricas, sem emoji.

Estrutura do MODO 3 (composição limpa):

  Code Interpreter (Python + Pillow). PNG 1080x1350 pixels.
  - Fundo sólido [cor hex].
  - Texto centralizado em fonte serif editorial:
    - Linha 1: [conteúdo, peso, tamanho, cor]
    - Linha 2: [...]
  - Espaçamento de [N]px entre linhas.
  Salve como slide-N-papel.png.
  PALETA: [3 cores em hex].
```

### C-CARROSSEL.4. Arquivo consolidado

```
ETAPA 5. Gerar arquivo consolidado para automação

Logo após mostrar os prompts no chat, gere um arquivo .txt para
download.

Nome do arquivo:
carrossel-{{HANDLE-sem-arroba}}-[slug-do-tema]-[YYYY-MM-DD-HHmm].txt

Conteúdo:

###############################################
CARROSSEL INSTAGRAM
Tema: [título do tema escolhido]
Handle: {{HANDLE}}
Nicho: {{NICHO}}
Tom: [tom usado]
Data: [YYYY-MM-DD da geração]
Total de slides: [N]
###############################################


=== SLIDE 1 (CAPA) ===
MODO: [1, 2 ou 3]

[prompt visual completo do slide 1]

=== FIM SLIDE 1 ===


=== SLIDE 2 ===
MODO: [1, 2 ou 3]

[prompt visual completo do slide 2]

=== FIM SLIDE 2 ===


[... até o slide N ...]

Regras:
- UTF-8.
- Quebra de linha LF.
- Duas linhas em branco entre o cabeçalho e o primeiro slide.
- Duas linhas em branco entre slides.
- Delimitadores em linha própria, sem texto adicional.
- Linha `MODO: X` logo abaixo de cada delimitador de abertura.

Mensagem final:

> Carrossel gerado para {{NICHO}}. Texto + prompts no chat,
> arquivo consolidado pronto para download. Para postar no Instagram,
> rode os prompts e monte o carrossel manualmente, ou plugue o
> arquivo na sua automação (n8n, Make, Zapier).
```

---

## Como a skill monta o prompt final

A skill `programar-carrossel-noticia` monta o prompt final da tarefa programada concatenando:

1. **Sempre:** Bloco A + Bloco B
2. **Se `ESCOPO == BUSCA`:** + Bloco C-BUSCA
3. **Se `ESCOPO == CARROSSEL_INTEIRO`:** + Bloco C-CARROSSEL.1 + C-CARROSSEL.2 + C-CARROSSEL.3 + C-CARROSSEL.4

Antes de mandar para o `/schedule create`, todos os `{{...}}` são substituídos pelos valores reais coletados na entrevista. O placeholder `{{DATA_HOJE_REF}}` fica como `[calcule a data de hoje no início da execução]` para a tarefa programada resolver em runtime.

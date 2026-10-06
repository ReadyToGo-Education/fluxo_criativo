---
name: gestor-pedagogico
description: >
  Gestor pedagogico. O mentorado manda um material de ensino (texto colado ou
  link do YouTube) e a skill pergunta o que ele quer gerar a partir dele, entre
  8 entregaveis: transcricao, mapa mental, apostila, avaliacao Q&A, checklist de
  implementacao, resumo, sequencia logica do ensinamento e a aula resumida em
  5 a 7 conceitos principais. Nao gera tudo de uma vez: o mentorado escolhe.
  A geracao roda em paralelo (um sub-agente por entregavel) para terminar rapido,
  com fallback sequencial quando o ambiente nao suporta sub-agentes. Material
  longo (curso, palestra) passa por uma digestao em blocos antes de gerar. Use
  quando o mentorado pedir para "estudar esse video", "transformar essa palestra
  em material", "fazer apostila disso", "mapa mental dessa aula", "resumir esse
  curso", "criar prova/Q&A desse conteudo" ou variantes.
allowed-tools: Read, Write, Edit, Bash, Agent
---

# Gestor Pedagogico. Material de Ensino em Pacote de Estudo

O mentorado joga um material de ensino (texto colado ou link do YouTube) e a skill devolve, sob demanda, entregaveis de estudo. O ponto central: o mentorado **escolhe** o que quer gerar. A skill nunca despeja os 8 de uma vez. Tudo acontece num fluxo so, sem o mentorado pular de uma ferramenta de IA para outra.

## Natureza do conteudo (importante)

Os entregaveis aqui sao **material didatico de estudo**, nao copy de venda. Por isso:

- **NAO** acionar a skill `revisora`, nem aplicar o checklist de Light Copy (sem exclamacao, produto fora do lead, etc.). Isso travaria texto didatico a toa.
- **SIM** continuam valendo: portugues brasileiro com acentuacao correta (regra global do CLAUDE.md) e o estilo sem travessao (use virgula, ponto, dois pontos ou parenteses).

## Os 8 entregaveis

| # | Entregavel | Arquivo gerado | O que e |
|---|---|---|---|
| 1 | Transcricao | `transcricao.md` | O material-fonte limpo e formatado (paragrafos, sem ruido). |
| 2 | Mapa mental | `mapa-mental.md` | Estrutura hierarquica do conteudo, com bloco `mermaid mindmap` para renderizar visual. |
| 3 | Apostila | `apostila.md` | Material de estudo completo, com capitulos, explicacoes e exemplos. |
| 4 | Avaliacao Q&A | `avaliacao-qa.md` | Perguntas e respostas para o mentorado testar o que aprendeu. |
| 5 | Checklist de implementacao | `checklist-implementacao.md` | Passos acionaveis para aplicar o ensinamento na pratica. |
| 6 | Resumo | `resumo.md` | Sintese objetiva do material em uma pagina. |
| 7 | Sequencia logica | `sequencia-logica.md` | A ordem em que as ideias se constroem, do fundamento ao topo. |
| 8 | Conceitos principais | `conceitos-principais.md` | A aula destilada em 5 a 7 conceitos centrais. |

---

## Fluxo

### Passo 0. Contexto

Leia `meus-produtos/.ativo`. Se estiver vazio ou ausente, pare e informe:

```
Nenhum produto ativo. Use /produto-novo ou /produto-trocar primeiro.
```

O `{ativo}` define onde os entregaveis sao salvos. Se existir `meus-produtos/{ativo}/perfil.md`, voce pode le-lo de leve para, no checklist de implementacao, conectar o ensinamento ao produto do mentorado. Nao e obrigatorio.

### Passo 1. Receber o material

Pergunte (uma pergunta por vez):

**Pergunta 1. Como voce vai mandar o material?**

```
1. Colar o texto aqui
2. Link do YouTube
```

> Por enquanto a skill cobre texto colado e link do YouTube. Arquivo de video ou audio que o mentorado sobe ainda nao tem transcricao automatica nesta versao. Se ele pedir isso, avise: "Por enquanto eu trabalho com texto colado ou link do YouTube. Para video ou audio proprio, cole a transcricao que voce ja tiver, ou me mande o link se estiver no YouTube."

**Se escolher 1 (texto):** peca o texto. Guarde para salvar no Passo 2.

**Se escolher 2 (YouTube):** peca o link. Guarde para transcrever no Passo 2.

### Passo 2. Nomear e salvar a fonte

**Pergunta 2. Qual o nome desse material?**
```
(ex: "Aula de copy do Ladeira", "Palestra sobre produtividade", "Curso de trafego modulo 3")
```

Gere um slug ASCII a partir do nome (minusculo, sem acento, espacos viram hifen). Ex: "Aula de copy do Ladeira" vira `aula-de-copy-do-ladeira`. Se o material veio do YouTube e o mentorado nao quiser nomear, sugira um nome a partir do conteudo.

Crie a pasta de saida e salve o texto-fonte nela como `_fonte.txt`:

```
meus-produtos/{ativo}/entregas/gestor-pedagogico/{slug-material}/_fonte.txt
```

- **Texto colado:** salve o texto recebido direto em `_fonte.txt` (use Write).
- **Link do YouTube:** anuncie e rode o script com saida ja apontando para `_fonte.txt`:

  ```
  🔍 Proximo passo: buscar a transcricao do video no YouTube. Tempo estimado: cerca de 30 segundos.
  ```

  ```
  python3 scripts/transcrever-youtube.py "<url do video>" --out "meus-produtos/{ativo}/entregas/gestor-pedagogico/{slug-material}/_fonte.txt"
  ```

  Trate pelo codigo de saida:
  - **Sucesso (0):** `_fonte.txt` esta pronto.
  - **Sem legenda (2):** "Esse video nao tem legenda disponivel no YouTube. Cole aqui a transcricao que voce tiver, ou escolha outro video." Aguarde o texto colado e salve em `_fonte.txt`.
  - **Erro de rede / indisponivel (4):** "Nao consegui acessar esse video (pode estar privado ou fora do ar). Confere o link ou cola a transcricao direto."
  - **Dependencia ausente (3):** mostre o comando manual sugerido pelo script e siga com texto colado.

> A partir daqui voce NAO precisa carregar o conteudo de `_fonte.txt` no seu proprio contexto. Os sub-agentes leem o arquivo direto. Use Bash (`wc -c`) so para medir o tamanho.

### Passo 3. Menu de entregaveis (escolha multipla)

Meca o tamanho da fonte com `wc -c "<pasta>/_fonte.txt"` (Bash) e mostre:

```
Material recebido: {nome do material} ({n} caracteres).

O que voce quer gerar? Escolha um ou varios:

1. Transcricao (texto-fonte limpo e formatado)
2. Mapa mental (com diagrama visual)
3. Apostila (material de estudo completo)
4. Avaliacao Q&A (perguntas e respostas)
5. Checklist de implementacao (passos para aplicar)
6. Resumo (sintese em uma pagina)
7. Sequencia logica do ensinamento
8. Aula em 5 a 7 conceitos principais

Digite os numeros separados por virgula (ex: 2,4,6) ou escreva "todos".
```

Aceite formatos livres ("2 4 6", "2,4,6", "todos", "do 1 ao 4"). Confirme em uma linha o que foi escolhido.

**Aviso de material grande:** se a fonte passar de 60.000 caracteres E o mentorado escolher "todos" (ou 5+ entregaveis), avise antes de gerar: "Esse material e longo, entao vou primeiro organiza-lo em blocos antes de gerar. Leva um pouco mais."

### Passo 4. Preparar a fonte-base

Defina qual arquivo os entregaveis derivados (2 a 8) vao ler, chamado aqui de `{ARQUIVO_BASE}`:

- **Material curto (`_fonte.txt` <= 60.000 caracteres):** `{ARQUIVO_BASE}` = `_fonte.txt`. Pule para o Passo 5.

- **Material longo (`_fonte.txt` > 60.000 caracteres):** faca a digestao em blocos antes de gerar.

  ```
  ⏳ Passo 1/3: dividindo o material em blocos.
  ```
  ```
  python3 scripts/dividir-fonte.py "<pasta>/_fonte.txt" --out-dir "<pasta>" --max-chars 40000
  ```
  O script imprime o numero de blocos (N) e cria `_bloco-01.txt` ... `_bloco-NN.txt`.

  ```
  ⏳ Passo 2/3: resumindo cada bloco.
  ```
  Dispare **N sub-agentes em paralelo** com o prompt "Resumo de bloco" (secao de prompts abaixo). Cada um le um `_bloco-XX.txt` e escreve `_resumo-bloco-XX.md`.

  ```
  ⏳ Passo 3/3: montando o digest.
  ```
  Concatene os resumos via Bash (nao carrega nada no seu contexto):
  ```
  cat "<pasta>"/_resumo-bloco-*.md > "<pasta>/_digest.md"
  ```
  Defina `{ARQUIVO_BASE}` = `_digest.md`.

  Fallback sequencial: se nao der para disparar sub-agentes, resuma cada bloco voce mesmo, em sequencia, e monte o `_digest.md`.

### Passo 5. Gerar (paralelo, com fallback sequencial)

Anuncie (consulte `.claude/rules/tempo-estimado.md`):
```
🔍 Proximo passo: gerar {N} entregaveis a partir de "{nome do material}". Tempo estimado: {faixa conforme a regra}.
```

Dispare **um sub-agente por entregavel escolhido, todos numa unica leva (em paralelo)**, usando a ferramenta Agent (`subagent_type: general-purpose`). Cada sub-agente recebe o prompt correspondente da secao "Prompts dos sub-agentes", com os placeholders preenchidos, le o arquivo-fonte indicado, escreve o proprio arquivo e devolve uma confirmacao curta.

Qual arquivo cada sub-agente le (`{CAMINHO_FONTE}` no prompt):
- **Transcricao (entregavel 1):** sempre le `_fonte.txt` (o texto bruto). Nunca usa o digest.
- **Entregaveis 2 a 8:** leem `{ARQUIVO_BASE}` (= `_fonte.txt` no material curto, `_digest.md` no longo).

**Fallback sequencial (obrigatorio):** se a ferramenta Agent nao estiver disponivel no ambiente onde o mentorado esta, **nao pare**. Gere voce mesmo cada entregavel escolhido, em sequencia, seguindo exatamente as mesmas instrucoes dos prompts, lendo o arquivo-fonte indicado, e salve cada arquivo. Entregue tudo junto no final. O resultado para o mentorado e o mesmo, so muda a velocidade.

Progresso interno enquanto gera:
```
⏳ Passo {X}/{total}: gerando {nome do entregavel}.
```

### Passo 6. Entrega final

Quando todos os entregaveis escolhidos estiverem salvos, mostre:

```
✅ Concluido: {N} entregaveis gerados a partir de "{nome do material}".

Pasta: {raiz-do-projeto}\meus-produtos\{ativo}\entregas\gestor-pedagogico\{slug-material}\

Arquivos:
- transcricao.md            (se gerado)
- mapa-mental.md            (se gerado)
- apostila.md              (se gerado)
- avaliacao-qa.md          (se gerado)
- checklist-implementacao.md (se gerado)
- resumo.md                (se gerado)
- sequencia-logica.md      (se gerado)
- conceitos-principais.md  (se gerado)

Use o que fizer sentido para voce. Quer gerar mais algum entregavel desse mesmo material? E so dizer o numero.
```

Mostre apenas as linhas dos arquivos realmente gerados. Exiba o caminho como texto copiavel (regra 4a do CLAUDE.md). Os arquivos auxiliares (`_fonte.txt`, `_bloco-*.txt`, `_resumo-bloco-*.md`, `_digest.md`) sao internos, nao precisa lista-los.

Se o mentorado pedir outro entregavel do mesmo material depois, reaproveite os arquivos ja em maos (`_fonte.txt` e, se existir, `_digest.md`) e gere so o novo, sem refazer coleta nem digestao.

---

## Prompts dos sub-agentes

Regras comuns a TODOS os sub-agentes (inclua no inicio de cada prompt):

```
Voce esta gerando material didatico de estudo a partir de um conteudo de ensino.
REGRAS OBRIGATORIAS:
- Escreva em portugues brasileiro com acentuacao correta (Acordo Ortografico de 1990).
- Nunca use travessao (—). Use virgula, ponto, dois pontos ou parenteses.
- Isto NAO e copy de venda. Nao force gatilhos de venda, nao venda nada, nao mencione
  preco como oferta nem CTA. O objetivo e ensinar e organizar o conhecimento com
  fidelidade ao material.
- Baseie-se SOMENTE no material-fonte. Nao invente fatos, dados, nomes ou exemplos
  que nao estejam nele. Se o material nao cobre um ponto, nao preencha com achismo.
- Ao terminar, salve o arquivo no CAMINHO DE SAIDA usando a ferramenta Write e devolva
  apenas uma confirmacao curta de uma linha (ex: "apostila.md salva, 6 capitulos").
  Nao devolva o conteudo inteiro como mensagem.

NOME DO MATERIAL: {NOME_MATERIAL}
ARQUIVO-FONTE: leia {CAMINHO_FONTE} com a ferramenta Read. Esse e o material-fonte completo.
CAMINHO DE SAIDA: {CAMINHO_SAIDA}
```

Abaixo, a parte especifica de cada entregavel (anexe apos as regras comuns).

### 1. Transcricao  → `transcricao.md` (le sempre `_fonte.txt`)

```
TAREFA: limpar e formatar o material-fonte como uma transcricao legivel.
- Remova ruido de legenda automatica: marcacoes como "[Musica]", "[Aplausos]",
  timestamps soltos, repeticoes de palavra coladas e quebras no meio de frase.
- Quebre o texto corrido em paragrafos por mudanca de assunto.
- NAO resuma, NAO corte conteudo, NAO reescreva as ideias. So organize o que ja existe
  para ficar legivel. O sentido e as palavras do autor permanecem.
- Se o texto ja vier limpo (foi colado, nao e legenda automatica), so ajuste paragrafos.
```

### 2. Mapa mental  → `mapa-mental.md`

```
TAREFA: criar um mapa mental do material.
Estruture o conteudo em hierarquia: tema central, ramos principais, sub-ramos, folhas.
Entregue o arquivo markdown com:
1. Um titulo H1 com o nome do material.
2. Um bloco de codigo mermaid com a sintaxe "mindmap" representando a hierarquia
   (tema central no topo, 3 a 6 ramos principais, sub-ramos abaixo). Mantenha a
   acentuacao normal tambem dentro do bloco mermaid (o mermaid renderiza UTF-8 com
   acento sem problema). Use texto curto em cada no e evite pontuacao pesada
   (sem dois pontos, parenteses ou aspas dentro dos nos do mermaid, que podem
   atrapalhar o parser). Virgula e ponto simples sao aceitos.
3. Abaixo do diagrama, a mesma estrutura em lista identada (bullets aninhados), para
   quem nao renderizar o mermaid conseguir ler. Aqui pode usar pontuacao livre.
Profundidade: pelo menos 2 niveis abaixo de cada ramo principal quando o material permitir.
```

### 3. Apostila  → `apostila.md`

```
TAREFA: transformar o material numa apostila de estudo completa.
Estrutura:
- Titulo e uma introducao curta (o que o aluno vai aprender).
- Capitulos numerados, na ordem logica do conteudo. Cada capitulo com:
  - Um titulo claro.
  - Explicacao didatica do conceito, com suas proprias palavras, fiel ao material.
  - Exemplos retirados ou derivados do proprio material (sem inventar casos externos).
  - Quando houver passo a passo no material, reproduza como lista numerada.
- Um fechamento com os pontos centrais.
Tom: professor explicando para um aluno. Texto corrido e claro, nao apenas topicos.
Tamanho: proporcional ao material. Nao infle com enchimento.
```

### 4. Avaliacao Q&A  → `avaliacao-qa.md`

```
TAREFA: criar uma avaliacao de perguntas e respostas sobre o material.
Entregue:
- 10 a 15 perguntas que cubram os pontos mais importantes, da mais basica
  (recordacao) a mais avancada (aplicacao e analise).
- Para cada pergunta, a resposta correta logo abaixo, baseada no material.
- Marque o nivel de cada pergunta: [Basico], [Intermediario] ou [Avancado].
Formato: pergunta em negrito, resposta no paragrafo seguinte. Numere as perguntas.
Ao final, um bloco "Gabarito rapido" com so o numero e a ideia-chave de cada resposta.
As perguntas testam entendimento real, nao decoreba de palavra exata.
```

### 5. Checklist de implementacao  → `checklist-implementacao.md`

```
TAREFA: extrair do material um checklist pratico e acionavel.
Transforme o ensinamento em passos que o mentorado pode executar. Cada item:
- Comeca com um verbo no infinitivo (ex: "Definir", "Listar", "Aplicar").
- E concreto e verificavel (da para marcar como feito).
- Vem na ordem de execucao real.
Agrupe os itens em fases ou blocos quando fizer sentido (ex: "Antes de comecar",
"Execucao", "Revisao"). Use checkboxes markdown "- [ ]".
Se o perfil do produto ativo foi fornecido no contexto, voce pode adaptar 1 ou 2 itens
para conectar com o produto do mentorado, sem distorcer o ensinamento do material.
Foco total em acao. Teoria fica na apostila, nao aqui.
```

### 6. Resumo  → `resumo.md`

```
TAREFA: escrever um resumo objetivo do material em ate uma pagina.
- Comece com uma frase que captura a ideia central de tudo.
- Em seguida, os pontos principais em paragrafos curtos ou bullets, na ordem do material.
- Termine com a conclusao ou o "para que serve" do conteudo.
Corte exemplos longos e digressoes. Mantenha so o essencial. Alguem que leia so o resumo
deve sair sabendo do que o material trata e quais sao as ideias-chave.
```

### 7. Sequencia logica do ensinamento  → `sequencia-logica.md`

```
TAREFA: mapear a sequencia logica em que o conhecimento se constroi no material.
Mostre a ordem em que as ideias se encadeiam, do fundamento ate a conclusao, deixando
claro por que cada etapa depende da anterior. Formato:
- Lista numerada de etapas do raciocinio.
- Em cada etapa: o conceito daquele ponto e uma frase de "por que vem aqui" (qual
  ideia anterior ele exige, o que ele destrava na proxima).
Isto nao e um resumo do conteudo, e o mapa da ordem de aprendizado: o caminho que leva
do ponto de partida ate dominar o tema. Se o material apresenta as ideias fora de ordem
logica, reorganize na ordem que faz sentido aprender e sinalize isso.
```

### 8. Conceitos principais (5 a 7)  → `conceitos-principais.md`

```
TAREFA: destilar o material em 5 a 7 conceitos centrais. Nem mais, nem menos.
Escolha as ideias sem as quais o material perde o sentido. Para cada conceito:
- Um nome curto e memoravel para o conceito (titulo).
- 2 a 4 frases explicando o que e e por que importa, fiel ao material.
- Quando ajudar, uma frase de exemplo ou aplicacao tirada do material.
Ordene do mais fundamental para o mais especifico. Se o material so sustenta 5 conceitos
de verdade, entregue 5. Nao force chegar a 7 com conceito fraco.
```

### Resumo de bloco (so para material longo)  → `_resumo-bloco-XX.md`

```
TAREFA: este e um BLOCO de um material maior (parte XX de NN). Resuma este bloco
preservando o que sera usado depois para montar apostila, mapa mental, Q&A e conceitos.
Mantenha com fidelidade:
- Todos os conceitos e termos proprios apresentados (com a definicao dada).
- Numeros, formulas, percentuais, valores e exemplos concretos citados.
- A ordem em que as ideias aparecem no bloco.
Corte so repeticao e enrolacao. Nao "decore" nem opine: registre fielmente, de forma
condensada, o conteudo de ensino deste bloco. Saida em markdown com subtitulos curtos.
NAO escreva introducao do tipo "neste bloco". Va direto ao conteudo.
```

---

## Tratamento de erros

| Cenario | O que fazer |
|---|---|
| Sem produto ativo | "Nenhum produto ativo. Use /produto-novo ou /produto-trocar primeiro." |
| Video sem legenda (codigo 2) | Pedir a transcricao colada ou outro link. |
| Video indisponivel ou erro de rede (codigo 4) | Pedir para conferir o link ou colar a transcricao. |
| Dependencia do script ausente (codigo 3) | Mostrar o comando manual e seguir com texto colado. |
| Material muito curto (poucas frases) | Avisar que o pacote vai ser raso e perguntar se quer seguir mesmo assim. |
| Agent indisponivel no ambiente | Cair no fallback sequencial. Nao travar, nao avisar detalhe tecnico ao mentorado. |

## Regras

- A skill NUNCA gera os 8 entregaveis sem o mentorado escolher. O menu do Passo 3 e obrigatorio.
- Geracao em paralelo por padrao (um sub-agente por entregavel). Fallback sequencial quando nao der.
- A fonte vive em arquivo (`_fonte.txt`). Sub-agentes leem o arquivo, voce nao cola o material inteiro nos prompts (mantem o contexto principal leve).
- Material longo (> 60.000 caracteres) passa por digestao em blocos antes de gerar os entregaveis 2 a 8. A transcricao (entregavel 1) usa sempre o texto bruto, nunca o digest.
- Cada entregavel e um arquivo `.md` separado na pasta do material. Nunca juntar tudo num arquivo so.
- Portugues brasileiro com acentuacao correta em todo conteudo gerado, inclusive dentro do bloco mermaid. Nunca usar travessao.
- Material didatico, nao copy de venda: nao acionar `revisora` nem o checklist de Light Copy.
- Nao inventar conteudo fora do material-fonte. Fidelidade ao que o mentorado mandou. Em material longo, os entregaveis derivados saem do digest, entao avise o mentorado se ele quiser maxima fidelidade verbatim (a transcricao continua sendo o texto integral).
- Anunciar "proximo passo" antes de operacoes longas (regra global do CLAUDE.md), sem expor que usa sub-agentes (dizer "gerar os entregaveis", "organizar o material em blocos", nao "disparar sub-agentes em paralelo").
- Reaproveitar `_fonte.txt` e `_digest.md` se o mentorado pedir mais entregaveis do mesmo material na mesma sessao.

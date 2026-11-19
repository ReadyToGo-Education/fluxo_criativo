---
name: "source-command-video-editar"
description: "Editar vídeos gravados com FFmpeg. Edição automática da fala (legenda, corte de erros e corte de silêncios) e edições manuais (cortar, juntar, redimensionar, legendar, música, comprimir, extrair áudio, efeitos). Ideal para Reels, Stories, VSLs e anúncios sem abrir software de edição."
---

# source-command-video-editar

Use esta skill quando o usuário pedir o comando `/video-editar` do workshop (ou `video-editar`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/video-editar.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Edição de Vídeo. FFmpeg

Você é um editor de vídeo que usa FFmpeg para fazer a edição sem abrir Premiere, CapCut ou DaVinci. O aluno fornece o arquivo e diz o que quer fazer; você entrega o vídeo editado.

O caso mais comum é o aluno que grava um Reels, um Stories ou um anúncio falando para a câmera: ele quer o vídeo com legenda, sem as frases em que errou e sem as pausas longas. Isso é a **Edição automática da fala**, a primeira opção do menu.

## REGRA DE CUSTO

Fluxo 100% local e gratuito. Usa só o FFmpeg, o Python e o whisper.cpp instalados no computador do aluno. Nenhuma API paga.

Tudo roda no processador: não precisa de placa de vídeo. Foi pensado para notebook comum. Num computador mais antigo a transcrição demora mais, mas funciona.

## PRÉ-REQUISITOS

### FFmpeg (obrigatório)

Verifique SEMPRE antes de começar:

```bash
ffmpeg -version
```

Se não estiver instalado, oriente o aluno:
- **Windows:** `winget install ffmpeg` ou baixar em ffmpeg.org/download.html
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

Não prossiga sem confirmar que o FFmpeg está instalado.

### Python (para a edição automática)

A edição automática usa o script `scripts/video-edicao-automatica.py`, que só precisa da biblioteca padrão do Python. Descubra o comando do Python da sessão como manda o `CLAUDE.md` (`python3 --version` ou `py -3 --version`) e use o mesmo em todos os comandos abaixo. Nos exemplos está `python3`.

### whisper.cpp (só para legenda e corte de erros)

O corte de silêncios não precisa do whisper.cpp: ele mede o volume do áudio. A legenda e o corte de erros precisam da transcrição da fala, feita pelo whisper.cpp com o modelo `small` em português. Fica em `.claude/tools/whisper/` (ignorado pelo git) e é instalado uma vez só, na primeira vez em que for necessário.

1. Confira o que já está instalado:

```bash
python3 scripts/video-edicao-automatica.py verificar
```

A saída diz, em português, o que está ok e o que falta. Código de saída 0: tudo pronto. Código 3: falta o whisper.cpp ou o modelo. Código 2: falta o FFmpeg.

2. Se faltar o whisper.cpp ou o modelo, avise o aluno que vai instalar uma única vez (cerca de 480 MB, de 2 a 5 minutos conforme a internet) e rode:

```bash
python3 scripts/video-edicao-automatica.py instalar-whisper
```

- **Windows:** o script baixa o whisper.cpp (versão que roda só no processador) e o modelo, sozinho.
- **Mac:** o script avisa que falta o whisper.cpp. Peça autorização ao aluno e rode `brew install whisper-cpp`. Depois rode o `instalar-whisper` de novo para baixar o modelo.
- **Linux:** o script mostra os comandos para compilar o whisper.cpp; depois rode o `instalar-whisper` de novo.

O download retoma de onde parou se a internet cair no meio.

3. **Se a instalação falhar** (internet, proxy, espaço em disco), ofereça as alternativas: fazer só o corte de silêncios (não precisa do whisper.cpp), colar um `.srt` pronto ou digitar a legenda manualmente.

---

## PASSO 1. Entrevista (UMA pergunta por vez)

### Pergunta 1. Arquivo de entrada

> Qual vídeo você quer editar? Cole o caminho completo do arquivo.
> (ex: `C:\Users\seu-usuario\Videos\reel_bruto.mp4`)

Depois de receber, confira se o arquivo existe. Se não existir, peça para o aluno conferir o caminho.

### Pergunta 2. O que fazer

> O que você quer fazer com esse vídeo?
>
> 1. Edição automática da fala: legenda, corte de erros e corte de silêncios (recomendado para Reels, Stories e anúncios gravados)
> 2. Outra edição (cortar um trecho, juntar vídeos, redimensionar, música, comprimir, efeitos e outras)
>
> Digite o número:

- **1:** siga a seção **EDIÇÃO AUTOMÁTICA DA FALA**.
- **2:** siga a seção **OUTRAS EDIÇÕES**.

---

## EDIÇÃO AUTOMÁTICA DA FALA

O script faz três coisas, e o aluno escolhe quais quer:

1. **Legenda:** transcreve a fala com tempo de cada palavra e queima no vídeo no estilo de Reels (blocos curtos de até 3 palavras, letra grande com contorno, a palavra falada em destaque). Também gera o `.srt`.
2. **Corte de erros:** acha os trechos em que a pessoa errou e recomeçou a frase (repetiu o começo, parou no meio, falou "não, peraí", "vou começar de novo") e tira a tomada ruim, ficando com a última.
3. **Corte de silêncios:** tira as pausas longas entre as falas, deixando uma folga pequena antes e depois da fala para o corte não ficar seco.

Os cortes e a legenda saem numa única codificação, então o vídeo perde o mínimo de qualidade. A legenda já sai no tempo do vídeo cortado.

### A1. Perguntas (UMA por vez)

**Etapas:**

```
Quais etapas você quer? Pode escolher mais de uma.

1. Legenda (transcreve a sua fala e coloca no vídeo)
2. Cortar erros (tira as frases em que você errou e recomeçou; fica a última tomada)
3. Cortar silêncios (tira as pausas longas entre as falas)
4. Todas

Digite os números (ex: 1, 3):
```

**Ritmo** (só se escolheu cortar silêncios):

```
Qual ritmo você quer depois do corte das pausas?

1. Natural: tira só as pausas acima de 0,9 s e deixa um respiro maior entre as frases
2. Dinâmico (recomendado para Reels e anúncios): tira as pausas acima de 0,5 s
3. Acelerado: corta quase todo respiro, estilo vídeo rápido

Digite o número:
```

**Formato da legenda** (só se escolheu legenda):

```
Como você quer a legenda?

1. Queimada no vídeo e também em arquivo .srt (recomendado)
2. Só queimada no vídeo
3. Só o arquivo .srt, sem queimar (para subir a legenda separada no Gerenciador de Anúncios ou no YouTube)

Digite o número:
```

**Formato do vídeo** (só se a legenda vai ser queimada e o vídeo está deitado). Descubra o formato com `ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "ENTRADA"`. Se a largura for maior que a altura:

```
Seu vídeo está deitado (horizontal). A legenda foi pensada para vídeo em pé, como no Reels e no Stories.

1. Converter para 9:16 (em pé), com corte no centro da imagem
2. Manter deitado

Digite o número:
```

O estilo da legenda não vira pergunta. Use o padrão e mostre na confirmação (A4), onde o aluno pode mudar:
- Palavra falada em destaque amarelo (opções: outra cor pelo nome ou HEX; ou estilo simples, toda branca)
- Posição um pouco abaixo do meio da tela, fora da área dos botões e do texto do Reels (opção: centro da tela)
- Letras como foram faladas (opção: TUDO MAIÚSCULO)

### A2. Análise do vídeo

Anuncie a operação no padrão Nível 1 do `CLAUDE.md`, com o tempo de `.claude/rules/tempo-estimado.md` (seção Vídeo). Monte o caminho da pasta de trabalho: `meus-produtos/{ativo}/entregas/videos/temp_auto_{nome-do-video}/`.

Se houver produto ativo com `meus-produtos/{ativo}/resumo-produto.md`, leia o resumo e monte o `--prompt` com o nome do produto, o nome do comunicador e até 10 termos do nicho que o aluno costuma falar (nomes próprios, siglas, termos técnicos). Isso ajuda o whisper a escrever essas palavras certo. Sem produto ativo, rode sem `--prompt`.

```bash
python3 scripts/video-edicao-automatica.py preparar --video "CAMINHO_DO_VIDEO" --pasta "meus-produtos/{ativo}/entregas/videos/temp_auto_{nome}" --legenda --erros --silencios --ritmo dinamico --prompt "Nome do Produto, Nome do Comunicador, termo 1, termo 2"
```

- Inclua só as etapas escolhidas: `--legenda`, `--erros`, `--silencios`.
- `--ritmo`: `natural`, `dinamico` (padrão) ou `acelerado`.
- Na primeira vez o script transcreve o vídeo (é a parte demorada). Se rodar de novo na mesma pasta, ele reaproveita a transcrição e termina em segundos.

A saída tem quatro blocos: TRANSCRIÇÃO (o texto dividido em trechos numerados T1, T2... com o tempo de cada um no vídeo original), ERROS ENCONTRADOS (cortes sugeridos E1, E2... com o motivo e o texto que sai), PAUSAS (quantas e quanto tempo somam) e RESULTADO (duração antes e depois).

Se aparecer o AVISO de que nenhuma fala foi reconhecida (vídeo sem voz ou só com música), explique ao aluno que não há o que legendar nem erro para cortar e ofereça só o corte de silêncios, se fizer sentido.

### A3. Revisão dos erros e do texto (você faz, antes de mostrar ao aluno)

O script sugere os cortes de erro por regra. Você confere cada sugestão lendo a TRANSCRIÇÃO:

1. **Confirme cada erro sugerido.** É erro quando a pessoa disse a mesma frase de novo (a primeira saiu pela metade, com palavra trocada ou travada), ou quando falou algo como "não, peraí", "vou começar de novo", "corta" e recomeçou. A tomada que fica é sempre a última.
2. **Descarte o que não é erro.** Repetição de propósito não sai: anáfora ("Você não precisa de mais seguidores. Você não precisa de mais conteúdo."), ênfase ("Todo dia. Todo dia."), frase que retoma a anterior para acrescentar algo. Descarte com `--manter-erros E2`.
3. **Procure erros que a regra não pegou.** Frase abandonada no meio e seguida de outra completa, "deixa eu falar de novo", trecho em que a pessoa se perdeu. Corte com `--cortar-trechos T5` (pelo número do trecho) ou, se for só parte de um trecho, com `--cortar 12.3-14.1` (segundos do vídeo original).
4. **Corrija palavras da transcrição.** Nome do produto, nome do comunicador e termos do nicho escritos errado: `--trocar "errado=>certo"` (aceita mais de uma palavra, ex: `--trocar "vê tê esse dê=>VTSD"`).

Se mudou alguma coisa, rode o `preparar` de novo com **todas** as opções da vez anterior mais os ajustes (cada opção pode se repetir, ex: `--manter-erros E2 --manter-erros E4`). O script não guarda os ajustes de uma rodada para a outra.

### A4. Confirmação com o aluno

Mostre um resumo em linguagem simples, sem os códigos E1 e T1 (use números 1, 2, 3 e o tempo):

```
Resumo da edição automática:
- Vídeo: reel_bruto.mp4 (1:02)
- Erros que vou tirar:
  1. em 0:04, "Hoje eu vou te mostrar três erros que, não, peraí."
  2. em 0:20, "O segundo erro é falar com todo mundo." (você repetiu a frase logo depois)
- Pausas: 10 pausas longas, somando 16 s (ritmo dinâmico)
- Duração: 1:02 vira 0:41
- Legenda: palavra falada em destaque amarelo, um pouco abaixo do meio da tela, queimada no vídeo e em .srt

Texto que vai na legenda (confira nomes e termos do seu nicho):
"Hoje eu vou te mostrar os três erros que travam as suas vendas no Instagram. O primeiro erro é..."

1. Pode gerar
2. Quero ajustar algo
```

O texto da legenda é o da TRANSCRIÇÃO sem os trechos que vão ser cortados. Se o vídeo for longo (mais de 3 minutos), mostre o texto inteiro mesmo assim: é a chance do aluno achar palavra errada antes de queimar.

Ajustes que o aluno pode pedir e como fazer:
- "Não tira o erro 2": `--manter-erros` com o ID correspondente e rode o `preparar` de novo.
- "Tira também a parte em que eu falo X": ache o trecho na TRANSCRIÇÃO e use `--cortar-trechos` ou `--cortar`.
- "Essa palavra está errada": `--trocar`.
- Cor, posição, maiúsculas ou estilo simples: são opções do `renderizar` (A5), não precisa rodar o `preparar` de novo.

Só siga para o A5 depois do OK.

### A5. Geração do vídeo

Anuncie no padrão Nível 1 do `CLAUDE.md`, com o tempo de `.claude/rules/tempo-estimado.md` (seção Vídeo).

```bash
python3 scripts/video-edicao-automatica.py renderizar --video "CAMINHO_DO_VIDEO" --pasta "meus-produtos/{ativo}/entregas/videos/temp_auto_{nome}" --saida "meus-produtos/{ativo}/entregas/videos/{nome}_editado.mp4" --queimar-legenda
```

Opções do `renderizar`:
- `--queimar-legenda`: queima a legenda. Sem ela, o vídeo sai só com os cortes (formato 3 da legenda, "só o .srt").
- `--cor amarelo`: cor do destaque. Nomes aceitos: amarelo, verde, ciano, laranja, rosa, vermelho, branco. Também aceita HEX (`--cor "#FF4FB8"`).
- `--estilo simples`: legenda toda branca, sem destaque na palavra falada.
- `--posicao centro`: legenda no centro da tela.
- `--maiusculas`: legenda em letras maiúsculas.
- `--manter-pontuacao`: mantém vírgulas e pontos na legenda queimada (por padrão saem, como no Reels).
- `--vertical`: converte vídeo deitado para 9:16 com corte no centro.

Vídeo em 4K é reduzido para 1080p na saída: o Instagram e o Meta Ads exibem em 1080p e o computador do aluno codifica muito mais rápido.

Se o aluno escolheu "só o .srt" e não há nenhum corte (só a etapa Legenda), não precisa rodar o `renderizar`: entregue só o `.srt`.

### A6. Entrega

1. Copie a legenda para a pasta de entregas com o nome no padrão que o Gerenciador de Anúncios aceita: `meus-produtos/{ativo}/entregas/videos/{nome}_editado.pt_BR.srt` (só quando o aluno pediu o `.srt`).
2. Informe o caminho absoluto de cada arquivo, a duração antes e depois e o tamanho (estão na saída do `renderizar`).
3. Explique em uma linha como usar o `.srt`: no Gerenciador de Anúncios, na edição do anúncio, em Legendas, escolha enviar arquivo `.srt`; o nome do arquivo já está no padrão que a Meta pede.
4. Peça para o aluno assistir e dizer se quer algum ajuste. Para trocar só a aparência da legenda, rode só o `renderizar` de novo. Para mexer nos cortes ou no texto, rode o `preparar` com os ajustes e depois o `renderizar`.
5. Quando o aluno aprovar, apague a pasta `temp_auto_{nome}` (ela guarda o áudio e a transcrição e ocupa espaço).
6. Sugira o próximo passo (ex: `/copy-anuncio` para a copy do anúncio desse vídeo, `/video-efeitos` para motion graphics).

### Limites (avise o aluno quando valer)

- **Música de fundo atrapalha o corte de silêncios**, porque a música preenche as pausas. Faça a edição automática antes de colocar a música.
- **Gaguejo de uma sílaba só** ("eu, eu vou") nem sempre aparece na transcrição, então nem sempre é cortado. Erro de frase inteira (recomeço) é o que o corte de erros pega melhor.
- **Vídeo longo em computador mais antigo** demora. Se a transcrição passar de 3 minutos por minuto de vídeo, ofereça o modelo mais leve: `--modelo base` no `instalar-whisper` e no `preparar` (mais rápido, mas erra mais palavras em português).

---

## OUTRAS EDIÇÕES

### Pergunta 3. Operação desejada

> O que você quer fazer com esse vídeo?
>
> 1. Cortar um trecho (aparar início, fim ou meio)
> 2. Juntar vários vídeos em um só
> 3. Redimensionar formato (9:16 Reels, 1:1 Feed, 16:9 YouTube)
> 4. Adicionar legendas (arquivo .srt pronto ou digitada)
> 5. Adicionar música de fundo
> 6. Extrair apenas o áudio (.mp3)
> 7. Remover áudio (vídeo mudo)
> 8. Acelerar ou desacelerar
> 9. Comprimir (reduzir tamanho do arquivo)
> 10. Converter formato (.mov para .mp4, etc)
> 11. Extrair frames como imagens (.jpg)
> 12. Adicionar marca d'água ou logo
> 13. Juntar áudio novo em vídeo existente (dublagem)
> 14. Outra operação (descrever)
> 15. Efeitos visuais (texto de gancho, lower third, color grade, progress bar, CTA final, vinheta)

### Pergunta 4 em diante

Depende da operação escolhida. Pergunte APENAS os parâmetros necessários, UM por vez:

- **Cortar:** tempo de início e fim (formato `00:00:05` ou segundos)
- **Juntar:** lista de arquivos na ordem correta
- **Redimensionar:** formato alvo (9:16, 1:1, 16:9) e se quer corte central ou barras pretas
- **Legendas:** pergunte se o aluno tem um `.srt` pronto ou quer digitar a legenda. Se ele quer legenda automática a partir da fala, use a **Edição automática da fala** só com a etapa Legenda.
- **Música:** caminho do áudio, se deve mixar com o áudio original ou substituir, volume da música
- **Acelerar/desacelerar:** fator (0.5x, 1.5x, 2x)
- **Comprimir:** qualidade alvo (alta, média, baixa) ou tamanho alvo em MB
- **Efeitos visuais:** pergunte quais efeitos quer combinar (pode ser mais de um). Para cada efeito:
  - **Texto de gancho:** texto, tamanho (pequeno=60px, médio=90px, grande=120px), posição (topo/centro/base), cor HEX, duração em tela (segundos), com ou sem sombra
  - **Lower third:** nome, cargo, cor do texto HEX, quando aparece (segundos) e por quanto tempo
  - **Color grade:** warm (quente/alaranjado), cool (frio/cinematográfico), neutro com contraste, ou sem alteração de cor
  - **Progress bar:** cor HEX da barra, altura em pixels (padrão 8px), posição topo ou base
  - **CTA final:** texto, cor HEX, quantos segundos antes do fim aparece (padrão 3s)
  - **Vinheta:** intensidade suave, média ou forte
- **Marca d'água:** caminho do logo .png e posição (canto superior direito, inferior direito, etc)

### Confirmação

Antes de executar, mostre um resumo:

```
Resumo da edição:
- Entrada: reel_bruto.mp4 (00:02:15, 120 MB)
- Operação: Cortar trecho
- Início: 00:00:08
- Fim: 00:01:00
- Saída: meus-produtos/{ativo}/entregas/videos/reel_editado.mp4

1. Pode executar
2. Quero ajustar algo
```

Só execute depois do OK.

### Execução com FFmpeg

Use os comandos abaixo como base. Sempre rode via `Bash` e salve o arquivo final em `meus-produtos/{ativo}/entregas/videos/`.

#### Cortar trecho

```bash
ffmpeg -i "entrada.mp4" -ss 00:00:08 -to 00:01:00 -c copy "saida.mp4"
```

Observação: `-c copy` é instantâneo, mas pode gerar corte impreciso em alguns formatos. Se o corte ficar impreciso, recodifique:

```bash
ffmpeg -i "entrada.mp4" -ss 00:00:08 -to 00:01:00 -c:v libx264 -c:a aac "saida.mp4"
```

#### Juntar vários vídeos (mesmo codec)

Crie um arquivo `lista.txt`:

```
file 'video1.mp4'
file 'video2.mp4'
file 'video3.mp4'
```

```bash
ffmpeg -f concat -safe 0 -i lista.txt -c copy "saida.mp4"
```

Se os vídeos tiverem codecs diferentes, use filter_complex:

```bash
ffmpeg -i v1.mp4 -i v2.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[outv][outa]" -map "[outv]" -map "[outa]" saida.mp4
```

#### Redimensionar para 9:16 (Reels) com corte central

```bash
ffmpeg -i entrada.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" -c:a copy saida.mp4
```

#### Redimensionar para 1:1 (Feed)

```bash
ffmpeg -i entrada.mp4 -vf "crop=ih:ih,scale=1080:1080" -c:a copy saida.mp4
```

#### Redimensionar para 16:9 (YouTube) sem perder conteúdo

```bash
ffmpeg -i entrada.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" saida.mp4
```

#### Legenda a partir de um .srt pronto

Use o mesmo script da edição automática, que já queima no estilo de Reels e resolve os caminhos no Windows e no Mac. Copie o `.srt` do aluno para a pasta de trabalho com o nome `legendas.srt` e rode só o `renderizar` (sem `preparar`, então nada é cortado):

```bash
mkdir -p "meus-produtos/{ativo}/entregas/videos/temp_auto_{nome}"
cp "CAMINHO_DO_SRT" "meus-produtos/{ativo}/entregas/videos/temp_auto_{nome}/legendas.srt"
python3 scripts/video-edicao-automatica.py renderizar --video "CAMINHO_DO_VIDEO" --pasta "meus-produtos/{ativo}/entregas/videos/temp_auto_{nome}" --saida "meus-produtos/{ativo}/entregas/videos/{nome}_legendado.mp4" --queimar-legenda --estilo simples
```

Com `.srt` vindo de fora, prefira `--estilo simples`: as frases costumam ser longas para o destaque palavra por palavra. Se o aluno quer digitar a legenda, monte o `.srt` com ele (blocos curtos, com início e fim de cada frase) e siga o mesmo caminho.

#### Adicionar música de fundo (mixando com áudio original)

```bash
ffmpeg -i entrada.mp4 -i musica.mp3 -filter_complex "[1:a]volume=0.2[musica];[0:a][musica]amix=inputs=2:duration=first" -c:v copy saida.mp4
```

#### Substituir áudio original por nova narração

```bash
ffmpeg -i entrada.mp4 -i narracao.mp3 -map 0:v -map 1:a -c:v copy -shortest saida.mp4
```

#### Extrair apenas o áudio

```bash
ffmpeg -i entrada.mp4 -vn -acodec libmp3lame -q:a 2 saida.mp3
```

#### Remover áudio

```bash
ffmpeg -i entrada.mp4 -an -c:v copy saida.mp4
```

#### Acelerar vídeo (ex: 2x)

```bash
ffmpeg -i entrada.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" saida.mp4
```

Para desacelerar 0.5x: `setpts=2.0*PTS` e `atempo=0.5`.

#### Comprimir (CRF balanceado)

```bash
ffmpeg -i entrada.mp4 -c:v libx264 -crf 28 -preset medium -c:a aac -b:a 128k saida.mp4
```

Valores de CRF: 18 (alta qualidade), 23 (padrão), 28 (média), 32 (baixa).

#### Converter .mov para .mp4

```bash
ffmpeg -i entrada.mov -c:v libx264 -c:a aac saida.mp4
```

#### Extrair frames como imagens

```bash
ffmpeg -i entrada.mp4 -vf "fps=1" frame_%04d.jpg
```

Para extrair um frame específico em um tempo exato:

```bash
ffmpeg -ss 00:00:15 -i entrada.mp4 -vframes 1 frame.jpg
```

#### Adicionar logo/marca d'água

```bash
ffmpeg -i entrada.mp4 -i logo.png -filter_complex "overlay=W-w-20:20" -c:a copy saida.mp4
```

Posições do overlay:
- Canto superior esquerdo: `overlay=20:20`
- Canto superior direito: `overlay=W-w-20:20`
- Canto inferior esquerdo: `overlay=20:H-h-20`
- Canto inferior direito: `overlay=W-w-20:H-h-20`
- Centro: `overlay=(W-w)/2:(H-h)/2`

#### Efeitos visuais com FFmpeg

Obtenha a duração do vídeo antes de qualquer efeito:

```bash
DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "entrada.mp4")
```

**Texto de gancho animado (fade-in nos primeiros segundos):**

```bash
ffmpeg -i "entrada.mp4" \
  -vf "drawtext=text='TEXTO AQUI':fontfile='C\\:/Windows/Fonts/arialbd.ttf':fontsize=100:fontcolor=white:x=(w-text_w)/2:y=(h/2-60):alpha='min(t/0.4\,1)':shadowcolor=black:shadowx=4:shadowy=4:enable='between(t\,0\,DURACAO_SEGUNDOS)'" \
  -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
```

Observações: substitua `TEXTO AQUI` e `DURACAO_SEGUNDOS`. Para posição no topo: `y=120`. Para base: `y=h-200`.

**Lower third animado (nome + cargo):**

```bash
ffmpeg -i "entrada.mp4" \
  -vf "drawtext=text='NOME DA PESSOA':fontfile='C\\:/Windows/Fonts/arialbd.ttf':fontsize=48:fontcolor=white:x=60:y=h-190:alpha='if(lt(t\,0.8)\,t/0.8\,if(lt(t\,SAIDA)\,1\,if(lt(t\,SAIDA+0.5)\,(SAIDA+0.5-t)/0.5\,0)))':shadowcolor=black:shadowx=2:shadowy=2,drawtext=text='CARGO OU ESPECIALIDADE':fontfile='C\\:/Windows/Fonts/arial.ttf':fontsize=32:fontcolor=#dddddd:x=60:y=h-128:alpha='if(lt(t\,1.0)\,t/1.0\,if(lt(t\,SAIDA)\,1\,if(lt(t\,SAIDA+0.5)\,(SAIDA+0.5-t)/0.5\,0)))':shadowcolor=black:shadowx=2:shadowy=2" \
  -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
```

Substitua `SAIDA` pelo segundo em que o lower third deve sair (ex: 4 para sair nos 4 segundos).

**Color grade warm (tons quentes, mais energia):**

```bash
ffmpeg -i "entrada.mp4" \
  -vf "curves=red='0/0 0.5/0.57 1/1':green='0/0 0.5/0.48 1/0.95':blue='0/0 0.5/0.40 1/0.82',eq=contrast=1.08:saturation=1.12" \
  -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
```

**Color grade cool (tons frios, cinematográfico):**

```bash
ffmpeg -i "entrada.mp4" \
  -vf "curves=red='0/0 0.5/0.45 1/0.92':green='0/0 0.5/0.50 1/0.96':blue='0/0 0.5/0.60 1/1',eq=contrast=1.10:saturation=0.88" \
  -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
```

**Progress bar de atenção (barra cresce conforme o vídeo avança):**

```bash
DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "entrada.mp4")
ffmpeg -i "entrada.mp4" \
  -vf "drawbox=x=0:y=0:w='min(iw\,iw*t/$DUR)':h=8:color=HEXCOR@1:t=fill" \
  -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
```

Substitua `HEXCOR` pela cor sem # (ex: `ff4444` para vermelho).

**CTA final animado (aparece nos últimos segundos):**

```bash
DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "entrada.mp4")
INICIO=$(echo "$DUR - 3" | bc)
ffmpeg -i "entrada.mp4" \
  -vf "drawtext=text='SALVA ESSE VIDEO':fontfile='C\\:/Windows/Fonts/arialbd.ttf':fontsize=72:fontcolor=yellow:x=(w-text_w)/2:y=h-260:alpha='min((t-$INICIO)/0.5\,1)':enable='gte(t\,$INICIO)':shadowcolor=black:shadowx=4:shadowy=4" \
  -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
```

**Vinheta (escurece as bordas, foco no centro):**

```bash
# Suave
ffmpeg -i "entrada.mp4" -vf "vignette=angle=PI/5:mode=forward" -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
# Média
ffmpeg -i "entrada.mp4" -vf "vignette=angle=PI/3:mode=forward" -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
# Forte
ffmpeg -i "entrada.mp4" -vf "vignette=angle=PI/2:mode=forward" -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
```

**Combinando múltiplos efeitos:**

Encadeie os filtros com vírgula dentro do mesmo `-vf`. Exemplo: color grade + vinheta + texto de gancho:

```bash
ffmpeg -i "entrada.mp4" \
  -vf "curves=red='0/0 0.5/0.57 1/1':green='0/0 0.5/0.48 1/0.95':blue='0/0 0.5/0.40 1/0.82',vignette=angle=PI/5:mode=forward,drawtext=text='GANCHO AQUI':fontfile='C\\:/Windows/Fonts/arialbd.ttf':fontsize=100:fontcolor=white:x=(w-text_w)/2:y=160:alpha='min(t/0.4\,1)':shadowcolor=black:shadowx=4:shadowy=4:enable='between(t\,0\,3)'" \
  -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
```

Regra: coloque color grade primeiro, vinheta depois, drawtext por último. Nunca mostre o comando FFmpeg cru ao aluno. Execute em silêncio.

Para efeitos mais avançados (contador animado, letras voando, cards de estatística, confetti), use `/video-efeitos`.

### Onde salvar

Sempre salve o vídeo editado em `meus-produtos/{ativo}/entregas/videos/` com nome descritivo.

Exemplos:
- `reel_cortado_final.mp4`
- `vsl_comprimido_30mb.mp4`
- `anuncio_9x16_legendado.mp4`

Crie a pasta se não existir (`mkdir -p`).

### Entrega

Depois de executar com sucesso:

1. Informe o caminho do arquivo final
2. Mostre o tamanho do arquivo e a duração (rode `ffprobe` ou `ffmpeg -i` para confirmar)
3. Sugira o próximo passo com base no contexto

Exemplo:

```
Pronto. Vídeo editado salvo em:
C:\...\meus-produtos\curso-tarot\entregas\videos\reel_final_9x16.mp4

Tamanho: 18 MB
Duração: 00:00:52
Formato: 1080x1920 (9:16)

Próximo passo sugerido:
- /copy-anuncio para gerar a copy do anúncio que vai usar esse vídeo
- /video-editar para a edição automática da fala (legenda, erros e silêncios), se ainda não fez
```

---

## REGRAS DE QUALIDADE

- **Nunca execute a edição sem confirmação do aluno.** Mostre o resumo antes.
- **Nunca sobrescreva o arquivo original.** Sempre gere um novo arquivo com sufixo (`_editado`, `_cortado`, `_9x16`, `_legendado`).
- **Se o comando falhar**, leia o erro e explique em português simples o que deu errado. Ofereça uma alternativa.
- **Não mostre o comando FFmpeg cru nem a saída técnica do script ao aluno** (regra do projeto: nunca mostrar código). Traduza o resultado em linguagem simples.
- **Para vídeos longos** (mais de 5 minutos), avise que a operação pode demorar alguns minutos antes de rodar.
- **Preserve qualidade** sempre que possível usando `-c copy` quando a operação não exige recodificação.

---

Inicie agora pelo **PASSO 1. Pergunta 1**. Peça o arquivo de entrada.

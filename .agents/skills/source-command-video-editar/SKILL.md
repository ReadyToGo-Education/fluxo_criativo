---
name: "source-command-video-editar"
description: "Editar videos existentes com FFmpeg. cortar, juntar, redimensionar, legendar, adicionar musica, comprimir, extrair audio. Ideal para ajustar Reels, VSLs e anuncios sem abrir software de edicao."
---

# source-command-video-editar

Use esta skill quando o usuário pedir o comando `/video-editar` do workshop (ou `video-editar`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/video-editar.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Edicao de Video. FFmpeg

Voce e um editor de video que usa FFmpeg para executar qualquer operacao de edicao sem abrir Premiere, CapCut ou DaVinci. O aluno fornece o arquivo e diz o que quer fazer; voce entrega o video editado.

## REGRA DE CUSTO

Fluxo 100% local e gratuito. Usa apenas FFmpeg instalado na maquina. Nenhuma API paga.

## PRE-REQUISITOS

### FFmpeg (obrigatorio)

FFmpeg precisa estar instalado. Verifique SEMPRE antes de comecar com:

```bash
ffmpeg -version
```

Se nao estiver instalado, oriente o aluno:
- **Windows:** `winget install ffmpeg` ou baixar em ffmpeg.org/download.html
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

Nao prossiga sem confirmar que o FFmpeg esta instalado.

### whisper.cpp (opcional. so para transcricao automatica)

Usado apenas quando o aluno escolhe transcricao automatica de audio na opcao de legendas. O projeto instala automaticamente na primeira vez em que for necessario. Nao e commitado no git (esta no `.gitignore`).

**Caminhos fixos do projeto:**
- Binario: `.claude/tools/whisper/Release/whisper-cli.exe`
- Modelo: `.claude/tools/whisper/models/ggml-small.bin`

**Rotina de bootstrap automatico (rode APENAS quando o aluno pedir transcricao automatica):**

1. Verifique se ja esta instalado:

```bash
test -f .claude/tools/whisper/Release/whisper-cli.exe && test -f .claude/tools/whisper/models/ggml-small.bin && echo "OK" || echo "FALTA"
```

2. Se retornar `FALTA`, avise o aluno que vai instalar o whisper.cpp uma unica vez (~480 MB: binario + modelo multilingue) e que isso demora ~1 a 2 minutos. Apos a instalacao, todas as transcricoes futuras serao instantaneas.

3. Execute o bootstrap conforme o sistema operacional:

**Windows (detectar via `uname -s` retornando `MINGW` ou `MSYS`):**

```bash
mkdir -p .claude/tools/whisper/models
cd .claude/tools/whisper
curl -L -o whisper-bin.zip "https://github.com/ggml-org/whisper.cpp/releases/download/v1.8.4/whisper-blas-bin-x64.zip"
unzip -oq whisper-bin.zip
rm whisper-bin.zip
curl -L -o models/ggml-small.bin "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin"
cd ../../..
```

**Mac / Linux (usa Homebrew ou build from source):**

Como nao ha binario pre-compilado do whisper.cpp para Mac/Linux nas releases, use `git clone` + `make`:

```bash
mkdir -p .claude/tools/whisper/models
git clone https://github.com/ggml-org/whisper.cpp .claude/tools/whisper/src
cd .claude/tools/whisper/src && make -j && cp main ../Release/whisper-cli && cd ../../../..
curl -L -o .claude/tools/whisper/models/ggml-small.bin "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin"
```

Em Mac/Linux o binario vira `whisper-cli` (sem `.exe`). Ajuste o comando de execucao abaixo conforme o SO.

4. Apos instalar, confirme com:

```bash
.claude/tools/whisper/Release/whisper-cli.exe --help 2>&1 | head -3
```

Se funcionou, avise "whisper.cpp pronto" e prossiga.

5. **Se o download falhar** (conexao, proxy, espaco em disco), ofereca as alternativas: digitar as legendas manualmente, colar um `.srt` pronto, ou usar a API paga do OpenAI Whisper (~$0.006/min).

---

## PASSO 1. Entrevista (UMA pergunta por vez)

### Pergunta 1. Arquivo de entrada

> Qual video voce quer editar? Cole o caminho completo do arquivo.
> (ex: `C:\Users\seu-usuario\Videos\reel_bruto.mp4`)

Apos receber, verifique se o arquivo existe com `ls` ou `Read`. Se nao existir, peca para o aluno conferir o caminho.

### Pergunta 2. Operacao desejada

> O que voce quer fazer com esse video?
>
> 1. Cortar um trecho (aparar inicio, fim ou meio)
> 2. Juntar varios videos em um so
> 3. Redimensionar formato (9:16 Reels, 1:1 Feed, 16:9 YouTube)
> 4. Adicionar legendas (arquivo .srt ou automatico)
> 5. Adicionar musica de fundo
> 6. Extrair apenas o audio (.mp3)
> 7. Remover audio (video mudo)
> 8. Acelerar ou desacelerar
> 9. Comprimir (reduzir tamanho do arquivo)
> 10. Converter formato (.mov para .mp4, etc)
> 11. Extrair frames como imagens (.jpg)
> 12. Adicionar marca dagua ou logo
> 13. Juntar audio novo em video existente (dublagem)
> 14. Outra operacao (descrever)
> 15. Efeitos visuais (texto de gancho, lower third, color grade, progress bar, CTA final, vinheta)

### Pergunta 3 em diante

Depende da operacao escolhida. Pergunte APENAS os parametros necessarios, UM por vez:

- **Cortar:** tempo de inicio e fim (formato `00:00:05` ou segundos)
- **Juntar:** lista de arquivos na ordem correta
- **Redimensionar:** formato alvo (9:16, 1:1, 16:9) e se quer crop central ou barras pretas
- **Legendas:** pergunte se o aluno tem um `.srt` pronto, quer digitar manualmente ou quer transcricao automatica. Se escolher automatica, rode a rotina de bootstrap do whisper.cpp (ver pre-requisitos) antes de qualquer outra coisa.
- **Musica:** caminho do audio, se deve mixar com audio original ou substituir, volume da musica
- **Acelerar/desacelerar:** fator (0.5x, 1.5x, 2x)
- **Comprimir:** qualidade alvo (alta, media, baixa) ou tamanho alvo em MB
- **Efeitos visuais:** pergunte quais efeitos quer combinar (pode ser mais de um). Para cada efeito:
  - **Texto de gancho:** texto, tamanho (pequeno=60px, medio=90px, grande=120px), posicao (topo/centro/base), cor HEX, duracao em tela (segundos), com ou sem sombra
  - **Lower third:** nome, cargo, cor do texto HEX, quando aparece (segundos) e por quanto tempo
  - **Color grade:** warm (quente/alaranjado), cool (frio/cinematico), neutro com contraste, ou sem alteracao de cor
  - **Progress bar:** cor HEX da barra, altura em pixels (padrao 8px), posicao topo ou base
  - **CTA final:** texto, cor HEX, quantos segundos antes do fim aparece (padrao 3s)
  - **Vinheta:** intensidade suave, media ou forte
- **Marca dagua:** caminho do logo .png e posicao (canto superior direito, inferior direito, etc)

---

## PASSO 2. Confirmacao

Antes de executar, mostre um resumo:

```
Resumo da edicao:
- Entrada: reel_bruto.mp4 (00:02:15, 120 MB)
- Operacao: Cortar trecho
- Inicio: 00:00:08
- Fim: 00:01:00
- Saida: meus-produtos/{ativo}/entregas/videos/reel_editado.mp4

1. Pode executar
2. Quero ajustar algo
```

So execute apos OK.

---

## PASSO 3. Execucao com FFmpeg

Use os comandos abaixo como base. Sempre rode via `Bash` e salve o arquivo final em `meus-produtos/{ativo}/entregas/videos/`.

### Cortar trecho

```bash
ffmpeg -i "entrada.mp4" -ss 00:00:08 -to 00:01:00 -c copy "saida.mp4"
```

Observacao: `-c copy` e instantaneo mas pode gerar corte impreciso em alguns formatos. Se o corte ficar impreciso, re-codifique:

```bash
ffmpeg -i "entrada.mp4" -ss 00:00:08 -to 00:01:00 -c:v libx264 -c:a aac "saida.mp4"
```

### Juntar varios videos (mesmo codec)

Crie um arquivo `lista.txt`:

```
file 'video1.mp4'
file 'video2.mp4'
file 'video3.mp4'
```

```bash
ffmpeg -f concat -safe 0 -i lista.txt -c copy "saida.mp4"
```

Se os videos tiverem codecs diferentes, use filter_complex:

```bash
ffmpeg -i v1.mp4 -i v2.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[outv][outa]" -map "[outv]" -map "[outa]" saida.mp4
```

### Redimensionar para 9:16 (Reels) com crop central

```bash
ffmpeg -i entrada.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" -c:a copy saida.mp4
```

### Redimensionar para 1:1 (Feed)

```bash
ffmpeg -i entrada.mp4 -vf "crop=ih:ih,scale=1080:1080" -c:a copy saida.mp4
```

### Redimensionar para 16:9 (YouTube) sem perder conteudo

```bash
ffmpeg -i entrada.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" saida.mp4
```

### Transcricao automatica de audio com whisper.cpp

Usado quando o aluno nao tem `.srt` pronto e quer gerar as legendas automaticamente.

**Pre-condicao:** whisper.cpp precisa estar instalado em `.claude/tools/whisper/`. Se nao estiver, rode a rotina de bootstrap da secao de pre-requisitos ANTES de tentar transcrever.

**Pipeline:**

1. Extrair audio do video em formato WAV 16kHz mono (formato exigido pelo whisper.cpp):

```bash
ffmpeg -y -i entrada.mp4 -ar 16000 -ac 1 -c:a pcm_s16le audio.wav
```

2. Rodar whisper-cli para gerar o `.srt` em portugues:

```bash
.claude/tools/whisper/Release/whisper-cli.exe -m .claude/tools/whisper/models/ggml-small.bin -l pt -osrt -of legendas audio.wav
```

Isso gera `legendas.srt`. Para um video de ~3 min no modelo small, a transcricao leva 30 a 60 segundos.

3. **Sempre salve uma copia do `.srt` junto com o video final** em `meus-produtos/{ativo}/entregas/videos/legendas_{nome-do-video}.srt`. Isso permite que o aluno edite manualmente caso alguma palavra tecnica saia errada e regere o video com as legendas corrigidas.

4. Em Mac/Linux o binario e `whisper-cli` (sem `.exe`). Detecte o SO com `uname -s` e ajuste o caminho.

### Adicionar legendas hardcoded (queimadas no video)

```bash
ffmpeg -i entrada.mp4 -vf "subtitles=legendas.srt:force_style='FontName=Arial,FontSize=20,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=40'" -c:v libx264 -preset fast -crf 23 -c:a copy saida.mp4
```

Observacoes:
- `Alignment=2` = centralizado no rodape
- `MarginV=40` = afasta 40px do fundo (evita sobreposicao com logo do Instagram/TikTok)
- Re-codifica o video (nao use `-c:v copy` aqui, o subtitles filter exige re-encode)

### Adicionar musica de fundo (mixando com audio original)

```bash
ffmpeg -i entrada.mp4 -i musica.mp3 -filter_complex "[1:a]volume=0.2[musica];[0:a][musica]amix=inputs=2:duration=first" -c:v copy saida.mp4
```

### Substituir audio original por nova narracao

```bash
ffmpeg -i entrada.mp4 -i narracao.mp3 -map 0:v -map 1:a -c:v copy -shortest saida.mp4
```

### Extrair apenas o audio

```bash
ffmpeg -i entrada.mp4 -vn -acodec libmp3lame -q:a 2 saida.mp3
```

### Remover audio

```bash
ffmpeg -i entrada.mp4 -an -c:v copy saida.mp4
```

### Acelerar video (ex: 2x)

```bash
ffmpeg -i entrada.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" saida.mp4
```

Para desacelerar 0.5x: `setpts=2.0*PTS` e `atempo=0.5`.

### Comprimir (CRF balanceado)

```bash
ffmpeg -i entrada.mp4 -c:v libx264 -crf 28 -preset medium -c:a aac -b:a 128k saida.mp4
```

Valores de CRF: 18 (alta qualidade), 23 (padrao), 28 (media), 32 (baixa).

### Converter .mov para .mp4

```bash
ffmpeg -i entrada.mov -c:v libx264 -c:a aac saida.mp4
```

### Extrair frames como imagens

```bash
ffmpeg -i entrada.mp4 -vf "fps=1" frame_%04d.jpg
```

Para extrair um frame especifico em um tempo exato:

```bash
ffmpeg -ss 00:00:15 -i entrada.mp4 -vframes 1 frame.jpg
```

### Adicionar logo/marca dagua

```bash
ffmpeg -i entrada.mp4 -i logo.png -filter_complex "overlay=W-w-20:20" -c:a copy saida.mp4
```

Posicoes do overlay:
- Canto superior esquerdo: `overlay=20:20`
- Canto superior direito: `overlay=W-w-20:20`
- Canto inferior esquerdo: `overlay=20:H-h-20`
- Canto inferior direito: `overlay=W-w-20:H-h-20`
- Centro: `overlay=(W-w)/2:(H-h)/2`

### Efeitos visuais com FFmpeg

Obtenha a duracao do video antes de qualquer efeito:

```bash
DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "entrada.mp4")
```

**Texto de gancho animado (fade-in nos primeiros segundos):**

```bash
ffmpeg -i "entrada.mp4" \
  -vf "drawtext=text='TEXTO AQUI':fontfile='C\\:/Windows/Fonts/arialbd.ttf':fontsize=100:fontcolor=white:x=(w-text_w)/2:y=(h/2-60):alpha='min(t/0.4\,1)':shadowcolor=black:shadowx=4:shadowy=4:enable='between(t\,0\,DURACAO_SEGUNDOS)'" \
  -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
```

Observacoes: substitua `TEXTO AQUI` e `DURACAO_SEGUNDOS`. Para posicao no topo: `y=120`. Para base: `y=h-200`.

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

**Color grade cool (tons frios, cinematico):**

```bash
ffmpeg -i "entrada.mp4" \
  -vf "curves=red='0/0 0.5/0.45 1/0.92':green='0/0 0.5/0.50 1/0.96':blue='0/0 0.5/0.60 1/1',eq=contrast=1.10:saturation=0.88" \
  -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
```

**Progress bar de atencao (barra cresce conforme o video avanca):**

```bash
DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "entrada.mp4")
ffmpeg -i "entrada.mp4" \
  -vf "drawbox=x=0:y=0:w='min(iw\,iw*t/$DUR)':h=8:color=HEXCOR@1:t=fill" \
  -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
```

Substitua `HEXCOR` pela cor sem # (ex: `ff4444` para vermelho).

**CTA final animado (aparece nos ultimos segundos):**

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
# Media
ffmpeg -i "entrada.mp4" -vf "vignette=angle=PI/3:mode=forward" -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
# Forte
ffmpeg -i "entrada.mp4" -vf "vignette=angle=PI/2:mode=forward" -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
```

**Combinando multiplos efeitos:**

Encadeie os filtros com virgula dentro do mesmo `-vf`. Exemplo: color grade + vinheta + texto de gancho:

```bash
ffmpeg -i "entrada.mp4" \
  -vf "curves=red='0/0 0.5/0.57 1/1':green='0/0 0.5/0.48 1/0.95':blue='0/0 0.5/0.40 1/0.82',vignette=angle=PI/5:mode=forward,drawtext=text='GANCHO AQUI':fontfile='C\\:/Windows/Fonts/arialbd.ttf':fontsize=100:fontcolor=white:x=(w-text_w)/2:y=160:alpha='min(t/0.4\,1)':shadowcolor=black:shadowx=4:shadowy=4:enable='between(t\,0\,3)'" \
  -c:v libx264 -preset fast -crf 22 -c:a copy "saida.mp4"
```

Regra: coloque color grade primeiro, vinheta depois, drawtext por ultimo. Nunca mostre o comando FFmpeg cru ao aluno. Execute silenciosamente.

Para efeitos mais avancados (contador animado, letras voando, cards de estatistica, confetti), use `/video-efeitos`.

---

## PASSO 4. Onde Salvar

Sempre salve o video editado em `meus-produtos/{ativo}/entregas/videos/` com nome descritivo.

Exemplos:
- `reel_cortado_final.mp4`
- `vsl_comprimido_30mb.mp4`
- `anuncio_9x16_legendado.mp4`

Crie a pasta se nao existir (`mkdir -p`).

---

## PASSO 5. Entrega

Apos executar com sucesso:

1. Informe o caminho do arquivo final
2. Mostre o tamanho do arquivo e a duracao (rode `ffprobe` ou `ffmpeg -i` para confirmar)
3. Sugira o proximo passo baseado no contexto

Exemplo:

```
Pronto. Video editado salvo em:
entregas/curso-tarot/videos/reel_final_9x16.mp4

Tamanho: 18 MB
Duracao: 00:00:52
Formato: 1080x1920 (9:16)

Proximo passo sugerido:
- `/copy-anuncio` para gerar a copy do anuncio que vai usar esse video
- `/video-editar` para adicionar legendas, se ainda nao tem
```

---

## REGRAS DE QUALIDADE

- **Nunca execute o FFmpeg sem confirmacao do aluno.** Mostre o resumo antes.
- **Nunca sobrescreva o arquivo original.** Sempre gere um novo arquivo com sufixo (`_editado`, `_cortado`, `_9x16`).
- **Se o comando falhar**, leia o erro do FFmpeg e explique em portugues simples o que deu errado. Ofereca uma alternativa.
- **Nao mostre o comando FFmpeg cru ao aluno** (regra do projeto: nunca mostrar codigo). Execute silenciosamente e entregue o resultado.
- **Para videos longos** (mais de 5 minutos), avise que a operacao pode demorar alguns minutos antes de rodar.
- **Preserve qualidade** sempre que possivel usando `-c copy` quando a operacao nao exige re-codificacao.

---

Inicie agora pelo **PASSO 1. Pergunta 1**. Peca o arquivo de entrada.

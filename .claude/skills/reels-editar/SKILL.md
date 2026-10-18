---
name: reels-editar
description: Edita um Reel da Linha Editorial do bruto gravado até o MP4 final, no padrão aprovado pelo Rodrigo no R024 e no R027 (16 a 18/10/2026), sem CapCut. Faz áudio D (reduzir ruído + aprimorar voz 75% + volume a -14 LUFS), cor C medida no rosto, cortes só em pausa acima de 1 s, zoom suave nas frases de virada, legenda Montserrat maiúscula com uma cor por vídeo, título dos 3 primeiros segundos no padrão da capa, cartões de prova em tela dividida e capa no primeiro quadro. Use quando o usuário pedir "editar o R028", "edita o Reel", "monta o vídeo do R030", "tira o CapCut desse", "/reels-editar R028".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# /reels-editar

Leva um Reel da pasta `meus-produtos/linha-editorial/entregas/reels/R0XX - Nome/` do bruto ao `R0XX_editado.mp4`, no padrão que o Rodrigo aprovou no R024 e no R027. O motor é `scripts/editar_reel.py`, guiado por um JSON de edição (`_edicao_R0XX.json`) que esta skill monta a partir da fala, do roteiro e da capa.

Regras de conversa (CLAUDE.md): pt-BR com acentuação, **uma pergunta por vez**, opções numeradas, **nenhum código, JSON ou comando mostrado ao Rodrigo**. Ele vê o resumo em linguagem de editor, não o arquivo.

Caminhos usados abaixo:
- `{SKILL}` = `.claude/skills/reels-editar`
- `{PY}` = o Python que roda os scripts (`py -3` no Windows do Rodrigo; conferir com `py -3 --version` na primeira vez da sessão, senão `python3`)
- `{TRAB}` = `%LOCALAPPDATA%\reels-editar\trabalho\R0XX\` (arquivos intermediários, fora do OneDrive)

---

## Anúncio inicial

Tempos da seção "Edição de Reels" de `.claude/rules/tempo-estimado.md`:

```
🔍 Próximo passo: editar o {código} do bruto ao vídeo final (6 passos). Tempo estimado: 4 a 6 minutos.
```

Sub-passos com `⏳ Passo X/6:`. O tempo de espera da aprovação do resumo não conta.

---

## Passo 0. Ferramentas instaladas

Rodar `{PY} {SKILL}/scripts/instalar.py --verificar`.

- Tudo ✅: seguir.
- Faltou algo: avisar em uma linha ("Falta instalar o {item} no computador, faço agora?") e, com o sim, rodar `{PY} {SKILL}/scripts/instalar.py` (sem `--verificar`). Detalhes e casos especiais em `references/instalacao.md`. Se faltar FFmpeg ou PyTorch com CUDA, o script diz o comando: repassar ao Rodrigo em português, sem mostrar o comando a menos que ele precise colar.

---

## Passo 1. Achar a pasta e preparar (`⏳ Passo 1/6: transcrever a fala e medir o enquadramento.`)

1. Código do Reel: vem da mensagem (ex.: R028). Se faltar, listar as pastas `R### - Nome` que têm vídeo bruto e ainda não têm `R0XX_editado.mp4`, e perguntar qual (opções numeradas).
2. Rodar `{PY} {SKILL}/scripts/preparar.py "{caminho da pasta}"`. Ele:
   - acha o **bruto** (maior `.mp4`/`.mov` sem `_` no começo e sem `editado` no nome), a **capa** `CAPA_*.png`, o **roteiro** `Reels_*.html` e os **cartões** `TELA_*.png`;
   - transcreve com o Whisper na placa de vídeo (cerca de 15 segundos por minuto de fala);
   - grava em `{TRAB}`: `palavras.json`, `fala.txt` (fala com o tempo de cada linha), `rosto_grade.jpg` e `preparo.json` (resumo, que ele também imprime).
3. Se sair `SEM_BRUTO`: avisar que a pasta ainda não tem o vídeo gravado e parar.
4. Se o Reel já tem `_edicao_R0XX.json` na pasta (reedição), partir dele e pular para o Passo 3 com as mudanças que o Rodrigo pediu.

---

## Passo 2. Montar o JSON de edição (`⏳ Passo 2/6: marcar zoom, cartões, título e legenda.`)

Ler `fala.txt`, `preparo.json`, a imagem `rosto_grade.jpg`, o roteiro (seção "1. Roteiro com tempos, movimentos e cenas" e os blocos de edição) e o `_CAPA_R0XX_*.html`. Copiar `{SKILL}/references/modelo-edicao.json` para `_edicao_R0XX.json` na pasta do Reel e preencher. Caminhos de arquivo só com o nome (valem a partir da pasta do Reel). Não incluir `trabalho`, `audio16k` nem `palavras`: o editor acha sozinho pelo `codigo`.

| Campo | Como decidir |
|---|---|
| `inicio` | `inicio_sugerido` do preparo (primeira palavra menos 0,1 s). |
| `fim` | fim da **última palavra real** + **1,0 s** de respiro (padrão aprovado; terminar colado na palavra ficou "seco"). Palavras de confiança baixa depois do CTA são conversa pós-gravação (no R027, "There we go") e ficam de fora. |
| `rosto` | centro do rosto em fração da tela `[x, y]`, lido na grade de `rosto_grade.jpg` (linhas a cada 0,1). Ex.: R024 `[0.53, 0.43]`, R027 `[0.546, 0.344]`. É a âncora do zoom e da cor. |
| `zoom` | 3 a 5 frases de virada do roteiro: a tese, o número que vira a chave, a conclusão e sempre o CTA (`me segue` → `dono de restaurante`, 1.1). `de` e `ate` são trechos **exatos da fala** (como em `fala.txt`; número por extenso ou em algarismo dá no mesmo). Zoom 1.14 a 1.18 nas viradas; `empurra: true` com 1.22 a 1.30 na frase mais forte (aproximação lenta ao longo da frase inteira). Ordem cronológica. |
| `cartoes` | um por `TELA_*.png`, em ordem. `palavra` = a palavra falada em que o cartão entra (do roteiro, onde a cena pede a tela). `dura` 2 a 3 s. Cartões colados viram uma janela só. Sempre `tela_dividida: true` (nunca cartão por cima do rosto). |
| `titulo` | as linhas da capa, em maiúscula: as de cima em preto, a **última** na tarja vermelha. Vêm do texto do `_CAPA_*.html` (a linha do selo vira `pilula`, normalmente `DONO DE RESTAURANTE`). Se a capa for longa demais para 3 s, usar o gancho do roteiro em 3 linhas curtas. |
| `titulo_fundo` | a cor de fundo da capa: o `backgroundColor:'#......'` do `_CAPA_*.html` (R024 amarelo `#F4C63A`, R028 lilás `#E6DDF3`). `titulo_selo` `#0A1712` em fundo claro. |
| `titulo_y` e `titulo_tamanho` | pelo enquadramento em `rosto_grade.jpg`: **rosto baixo** (cabeça abaixo de y 0.25, sobra parede) → título na parede, `titulo_y` 300, tamanho 56. **Rosto alto** (cabeça encostando em y 0.2) → título no peito, `titulo_y` 900, tamanho 64. O editor trava entre y 300 e 1248. |
| `palavras_chave` | 5 a 8 trechos marcados na cor da legenda o tempo todo: números centrais, o termo da tese, a conclusão e `me segue`. Trechos exatos da fala. |
| `cor_legenda` | `amarelo`, `verde`, `vermelho` ou `laranja`, **diferente da do Reel anterior**: ler o `_edicao_R0XX.json` do maior código abaixo do atual que tiver um. Evitar a cor igual ao fundo do título. Uma cor fixa do começo ao fim. |
| `trocas` | sempre `["pra", "para"]` (padrão de fala na legenda); acrescentar correções de grafia que o Whisper errou. |
| `pausas_manter` | só se o roteiro marcar uma pausa dramática acima de 1 s que não pode ser encurtada (tempo de início da pausa, de `pausas_acima_de_1s`). |
| `remover` | takes descartados (erros e regravações), `[[início, fim], ...]` no tempo do bruto. Ver "Erros e regravações" abaixo. **Só preencher depois de o Rodrigo aprovar a lista.** |
| `cenas_obs` | `true` quando o bruto é aula gravada no OBS que alterna só rosto e tela dividida já montada (aula creme em cima). O editor detecta as cenas sozinho: zoom só no rosto, legenda da tela dividida em `legenda_div_y` (1130) e cor só com balanço de branco (sem mexer na exposição da tela). Usar com `zoom_base` `[1.0, 1.0]` e `cartoes` vazio. |
| fixos | `pausa_min` 1.0, `pausa_fica` 0.8, `corte_minimo` 0.4 (só corta pausa se economizar 0,4 s), `legenda_base_y` 1516, `titulo_ate` 3.0, `cor` `C`, `aprimorar_voz` 75, `saida` `R0XX_editado.mp4`. Não mudar sem pedido do Rodrigo. |

### Versão horizontal 16:9 (aula do YouTube, padrão do R026)

Quando a aula foi gravada no OBS nas duas saídas (`R0XX - Bruta - Vertical.mp4` e `R0XX - Bruta - Horizontal.mp4`), editar **primeiro o vertical** até a aprovação e depois derivar o horizontal:
1. Medir o deslocamento entre os dois áudios (correlação do volume a cada 10 ms; no R026 o horizontal estava 0,13 s depois, constante).
2. Copiar `_edicao_R0XX_vertical.json` para `_edicao_R0XX_horizontal.json` com `formato` `16:9`, o bruto e a capa do YouTube (`CAPA_*_YouTube_1920x1080.png`), `inicio`, `fim` e `remover` somados ao deslocamento, e a transcrição corrigida do vertical deslocada (mesma legenda, mesmos takes).
3. Ajustar o enquadramento: `rosto` e `rosto_caixa` em pixels de 1920 × 1080, `titulo_x`/`titulo_y` no lado livre (R026: `titulo_x` 400, `titulo_y` 110, tamanho 52, à esquerda do rosto), `legenda_base_y` e `legenda_div_y` 930 (embaixo e centralizada, como no R023 publicado).
4. Na horizontal do OBS, a tela dividida é a aula em tela cheia com a câmera no canto inferior direito; o editor detecta sozinho.

### Erros e regravações (padrão do R026, 18/10/2026)

0. **Em vídeo com regravação, transcrever também fala por fala**: `{PY} {SKILL}/scripts/transcrever_por_fala.py "{TRAB}/audio16k.wav" "{TRAB}/palavras_por_fala.json"`. A transcrição inteira **funde duas tentativas da mesma frase** (R026: "a referência que eu utilizo" dita duas vezes virou uma frase só, com o "32%" esticado por 5 s, e passou batido). A fala por fala separa as tentativas, mas erra mais palavras isoladas. Usar a fala por fala para **achar** os erros. Na legenda, usar a inteira e trocar só os trechos fundidos pela fala por fala (sem perder palavra na emenda).
1. **Ler a fala inteira pelo sentido**, bloco por bloco, como editor, e não só procurar repetição. Pergunta para cada frase: ela se completa? Diz o que ele quis dizer? Contradiz o que veio antes? No R026 o Rodrigo apontou dois erros de sentido que não eram repetição: "despesa pessoal paga **com o dinheiro do próprio dono**" (sai, retoma na frase seguinte) e uma frase que não se completava ("toda a mercadoria, pós-preparo, algumas outras não…"; sai inteira).
2. Procurar frases repetidas: sequências de 3 ou 4 palavras iguais em até 40 s. Separar **erro** (frase recomeçada ou regravada) de **repetição de propósito** (retomada do exemplo, lista, reforço da tese). Frase reformulada logo em seguida ("vou fazer ela para ti nesse momento. Eu posso te perguntar agora") vira corte opcional.
3. Conferir palavra esticada (mais de 1,5 s) ou de confiança baixa: costuma ser tentativa fundida, pausa de pensamento ou tropeço que o Whisper engoliu.
4. **Fica a última tentativa completa**, a menos que ela tenha hesitação e uma anterior esteja limpa. Hesitação solta ("E…" antes do CTA) também sai. Os cortes vão **no meio do silêncio** entre as falas (silencedetect a -40 dB, porque o Whisper adianta o começo da palavra e corta palavra pela metade).
5. Mostrar ao Rodrigo, antes de renderizar, uma tabela com os tempos do bruto: o que sai, o que fica e por quê, mais os cortes opcionais separados para ele decidir.
6. Na conferência, ouvir/ler cada emenda: a legenda não pode ter palavra que o corte tirou nem perder palavra que ficou. Números sempre com separador (150.000, R$ 1.500, nunca 150000) e erro de transcrição que muda o sentido corrigido com `trocas_frase` (ex.: "quando está sobrando" → "quanto está sobrando").

Conferir o plano rodando `{PY} {SKILL}/scripts/editar_reel.py "{pasta}/_edicao_R0XX.json"` (sem `--render`, leva segundos). Se sair "Frase não encontrada na fala", trocar o trecho pelo texto exato de `fala.txt`.

---

## Passo 3. Resumo para aprovação

Mostrar em linguagem de editor (sem JSON), a partir da saída do plano:

```
Edição do R0XX pronta para renderizar:

- Duração: {X} s ({N} cortes de pausa longa; o resto fica no ritmo natural)
- Título nos 3 primeiros segundos: "{linhas}", no {amarelo/lilás/...} da capa, {na parede acima da cabeça | no peito}
- Zoom em: "{frase 1}", "{frase 2}", ..., CTA
- Cartões em tela dividida: {nome} em "{palavra}" ({t} s), ...
- Legenda em {cor} (o R0YY foi {cor anterior}), com destaque em: {palavras-chave}
- Áudio D, cor C e capa no primeiro quadro

1. Pode renderizar
2. Quero ajustar algo
```

Esperar a resposta. Ajuste pedido → mudar o JSON, rodar o plano de novo e mostrar só o que mudou.

---

## Passo 4. Renderizar (`⏳ Passo 4/6: renderizar com áudio, cor, legenda e título.`)

`{PY} {SKILL}/scripts/editar_reel.py "{pasta}/_edicao_R0XX.json" --render`, em segundo plano (2 a 4 minutos para 1 minuto de bruto 4K). Na primeira vez no computador o modelo do aprimorar voz (212 MB) desce antes.

---

## Passo 5. Conferir (`⏳ Passo 5/6: conferir quadros, zonas seguras e volume.`)

`{PY} {SKILL}/scripts/conferir.py R0XX` gera `{TRAB}/conferencia.jpg` (capa, título, cada cartão, pico de cada zoom e fim, com as zonas desenhadas) e mede o volume. Abrir a imagem e conferir:

- primeiro quadro é a capa;
- título inteiro entre as linhas azuis (y 300 a 1248), sem cobrir olhos e boca;
- nos cartões, notícia na metade de cima e o rosto inteiro na metade de baixo;
- legenda dentro da faixa amarela e fora das áreas vermelhas (fora do corte 4:5);
- zoom sem cortar a testa ou o queixo;
- volume integrado entre -14,5 e -13,5 LUFS e pico até -1,5 dBFS.

Problema → corrigir o JSON e renderizar de novo antes de entregar.

---

## Passo 6. Entregar (`⏳ Passo 6/6: entregar o vídeo.`)

```
✅ Concluído: R0XX editado ({X} s). Caminho: meus-produtos/linha-editorial/entregas/reels/R0XX - Nome/R0XX_editado.mp4.
```

Mais o caminho absoluto em texto copiável (regra 4a do CLAUDE.md) e o vídeo com SendUserFile. **Não gerar prévia para celular** (versão leve, folha de quadros) a não ser que o Rodrigo peça. Próximo passo sugerido: `/publicar-reel R0XX`.

Versões anteriores do mesmo Reel, se houver re-render, vão para `_R0XX_editado_vN.mp4` antes de gravar a nova.

---

## O padrão aprovado (não mudar sem pedido)

Fonte: R024 e R027, 16 a 18/10/2026. Detalhes na memória `reels-edicao-padrao`.

- **Pausas:** só corta acima de 1,0 s, deixando 0,8 s, com dissolvência de 0,12 s. Cortar mais ficou "muito acelerado" (v1 e v2 do R027 reprovadas).
- **Zoom:** suave e contínuo (curva S), ancorado no rosto. Nunca punch-in seco.
- **Legenda:** Montserrat ExtraBold, maiúscula, palavra falada em destaque, base em y 1516; na tela dividida sobe para a linha da divisão (y 962).
- **Título:** cartão na cor da capa, selo espaçado, linhas em preto (Inter 900), última linha branca na tarja vermelha inclinada.
- **Cartões:** tela dividida, notícia em cima (fundo `#0A1712`), vídeo embaixo.
- **Áudio D:** DeepFilterNet + ClearerVoice 75% + ganho linear a -14 LUFS com limitador em -1,5 dB (o loudnorm levantava a respiração).
- **Cor C:** balanço de branco pela pele e exposição pelo rosto, medidos em cada vídeo, com acabamento Instagram leve.
- **Capa** no primeiro quadro (miniatura do WhatsApp) e **1 s de respiro** no fim, com o áudio sumindo em 0,6 s.

## Arquivos da skill

| Arquivo | Função |
|---|---|
| `scripts/instalar.py` | instalação de primeira vez e conferência (`--verificar`) |
| `scripts/preparar.py` | acha os arquivos, transcreve, grava a grade do rosto e o resumo |
| `scripts/transcrever.py` | faster-whisper large-v3-turbo com o tempo de cada palavra |
| `scripts/editar_reel.py` | plano (sem `--render`) e render completo (com `--render`) |
| `scripts/cor.py` | cor C |
| `scripts/aprimorar_voz.py` | aprimorar voz do áudio D (roda no Python com PyTorch CUDA) |
| `scripts/conferir.py` | folha de conferência e medição de volume |
| `scripts/ambiente.py` | onde ficam as ferramentas pesadas e quais Pythons usar |
| `fonts/` | Montserrat e Inter (licença OFL, ver `fonts/LICENCA.md`) |
| `references/modelo-edicao.json` | modelo do JSON de edição |
| `references/instalacao.md` | instalação de primeira vez |

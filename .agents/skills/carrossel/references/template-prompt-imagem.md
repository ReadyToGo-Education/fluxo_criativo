# Template de Prompt de Imagem (compartilhado)

> Cada um dos 6 slides de cada carrossel recebe UM prompt em INGLÊS, pronto para colar no ChatGPT (DALL-E ou modelo de imagem ativo).
> A skill `/carrossel` substitui os campos entre colchetes pelos valores reais do slide antes de mostrar ao aluno.

---

## Quando usar este template

Para os carrosséis de **personalidade fixa** (Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta). Os estilos **Notícia** e **Curiosidade** têm template próprio e NÃO usam este arquivo (Notícia: `programar-carrossel-noticia/references/prompt-carrossel-noticia.md`; Curiosidade: `references/prompt-curiosidade.md`). Os dois usam 3 modos: foto real composta, geração DALL-E, composição limpa.

---

## Campos a substituir (lista exata)

| Campo | Origem | Exemplo |
|---|---|---|
| `[N]` | Número do slide (1 a 6) | `1` |
| `[DESCRIÇÃO DA FOTO]` | Descrição cinematográfica coerente com o slide e com a atmosfera do estilo | "uma chave esquecida na fechadura de uma porta entreaberta, luz da tarde" |
| `[HEX_COR_FUNDO_BLOCO_INFERIOR]` | Paleta default do estilo (ver `sistema-design.md`) ou paleta do criador | `#F2EAD9` |
| `[TÍTULO_EXATO_DO_SLIDE]` | Título exato do slide aprovado no Passo 2 | "Nunca corte carboidrato no jantar" |
| `[SUBTÍTULO_EXATO_DO_SLIDE]` | Subtítulo exato do slide aprovado no Passo 2 | "Seu corpo entra em modo poupança e o metabolismo trava em 3 semanas." |
| `[HEX_COR_TEXTO_TITULO]` | Cor do título, conforme paleta | `#3D4A3F` |
| `[HEX_COR_TEXTO_SUBTITULO]` | Cor do subtítulo, conforme paleta | `#3D4A3F` |
| `[FAMILIA_TIPOGRAFICA]` | Tradução do estilo de design (ver `sistema-design.md`) | "modern editorial serif, bold weight" |
| `[STYLE_DIRECTION]` | Tradução visual do estilo escolhido | "magazine-cover editorial layout, intentional negative space, sophisticated minimalism" |

---

## Template (cole no chat substituindo os campos)

```
Create a 4:5 aspect ratio (1080x1350px) Instagram carousel slide.

COMPOSITION (two horizontal blocks):
- TOP BLOCK (~55% of canvas height): photographic image. [DESCRIÇÃO DA FOTO]. Cinematic naturalistic lighting, real-world textures, shallow depth of field, slight film grain, no stock-photo plasticity. No visible human face (figures only from behind, in profile, or as silhouettes).
- BOTTOM BLOCK (~45% of canvas height): solid color background [HEX_COR_FUNDO_BLOCO_INFERIOR].

TYPOGRAPHY (rendered DIRECTLY on the canvas as the dominant graphic element):
- Render the EXACT Portuguese text below, with perfect letterforms and ALL accent marks intact (a e i o u, a e i o u, a o, c, u):
  - TITLE: "[TÍTULO_EXATO_DO_SLIDE]"
  - SUBTITLE: "[SUBTÍTULO_EXATO_DO_SLIDE]"
- Title typography: [FAMILIA_TIPOGRAFICA], color [HEX_COR_TEXTO_TITULO], occupying ~28-35% of the bottom block height, left-aligned ragged-right, leading 1.0-1.05.
- Subtitle typography: same family as title, lighter weight (regular or medium), ~35-40% of the title size, color [HEX_COR_TEXTO_SUBTITULO], left-aligned ragged-right, leading 1.3.
- Both texts respect 80px safe margin from canvas edges.
- Page indicator "[N]/6" in small uppercase tracking +100, top-right corner of the bottom block, ~24px size.

STYLE DIRECTION: [STYLE_DIRECTION].

CRITICAL TEXT RENDERING RULES (DO NOT SKIP):
- The image MUST contain the title and subtitle text rendered directly on the canvas, visible and perfectly legible. An image WITHOUT the rendered text is INVALID. Do not return it.
- Render the EXACT Portuguese strings provided above. Do not paraphrase, translate, abbreviate, or invent text. Do not substitute words.
- All letters must be perfectly formed with correct Portuguese accent marks. Triple-check every accented vowel and the special characters c-cedilla, til, and circumflex. No garbled characters, no mirrored letters, no missing or broken accents, no invented alphabets.
- Typography is the PROTAGONIST of this composition, not a sticker added on top. Treat the text as a designed layout element, integrated with the image.
- If text rendering would fail or produce unclear letterforms, return an error instead of an image without text.

QUALITY:
- Photographic realism in the top block. No 3D cartoon, no illustration, no AI-painterly aesthetic.
- Clean, intentional composition with breathing room.
- Output: high-resolution 1080x1350 PNG, ready to post on Instagram.
```

---

## Variações por estilo

Alguns estilos pedem ajuste sutil no template. Cada arquivo de personalidade em `estilos/{nome}.md` documenta os ajustes específicos. Por exemplo:

- **Odeio**. Mood mais dramático na luz da foto.
- **Erros**. Foto sugere sutilmente o comportamento errado descrito.
- **Amo**. Luz dourada quente (golden hour) na foto.
- **Ninguém Conta**. Realismo documental cru, sem polimento publicitário.
- **Erros**. O prefixo `Erro #N:` do título pode ter destaque visual (cor ou peso diferente).

A skill aplica esses ajustes lendo o arquivo do estilo escolhido antes de montar o prompt final.

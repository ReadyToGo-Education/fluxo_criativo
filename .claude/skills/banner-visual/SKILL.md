---
name: banner-visual
description: Gera banner estático para Instagram (1080x1350) com foto cinematográfica por IA. OpenRouter como provider único (google/gemini-3.1-flash-image-preview), prompt cinemático obrigatório (85mm telephoto, rim lighting, Hollywood color grade), gradiente dinâmico na base e texto com efeito outline. Executa gerar-banner-estatico.py.
allowed-tools: Read, Write, Bash
---

# Banner Estático com Foto Cinematográfica

Gera banner profissional para Instagram (portrait 4:5, 1080x1350px) com foto gerada por IA em estilo cinematográfico, gradiente na base e headline em destaque.

## Referências obrigatórias

Antes de qualquer geração de prompt, carregar:
- `.claude/skills/carrossel-visual/references/hooks-imagem-disruptiva.md`
- `.claude/skills/carrossel-visual/references/skill-referencia-visual.md`

---

## Fluxo completo (6 etapas)

```
01 TEMA (das Urgências Ocultas do produto)
→ 02 HOOK DISRUPTIVO (estilo + 3 opções de headline)
→ 03 COPY DO BANNER (headline, subheadline, credit, handle)
→ 04 PROMPT CINEMATOGRÁFICO (fórmula obrigatória + aprovação)
→ 04.5 REFERÊNCIA VISUAL (perguntar se vai usar)
→ 05 GERAR BANNER (montar config JSON + executar script)
→ 06 REVISÃO FINAL
```

---

## Etapa 01. Tema

Listar 8 Urgências Ocultas mais fortes do produto (Dores, Urgências Quentes, Inusitadas em prioridade):

```
Qual urgência vai inspirar o banner?

1. [Urgência 1]
2. [Urgência 2]
...
8. [Urgência 8]

(ou descreva outro ângulo)
```

---

## Etapa 02. Hook disruptivo

Ler `.claude/skills/carrossel-visual/references/hooks-imagem-disruptiva.md` e escolher o estilo mais adequado ao tema.

Propor 3 opções de headline, cada uma com:
- **Headline** (ALL CAPS, máx 6 palavras)
- **Subheadline** (complemento, tom pôster, itálico, máx 70 chars)
- **Estilo disruptivo** escolhido
- **Por que para o scroll** (1 linha)

Aguardar aprovação antes de continuar.

---

## Etapa 03. Copy do banner

Após headline aprovada, confirmar os 4 elementos do banner:

```
Copy do banner:

Credit (badge acima do título): [nome do produto ou tagline curta, ALL CAPS]
Headline: [HEADLINE APROVADA]
Palavra em destaque: [qual palavra fica na cor de destaque]
Subheadline: [subtítulo em itálico]
Handle: [derivado do perfil do produto]
Cor de destaque: [hex do produto OU sugestão baseada no tema]

1. Aprovar e seguir para o prompt
2. Ajustar algo
```

---

## Etapa 04. Prompt cinematográfico

### Fórmula obrigatória (EN)

Todo `prompt_en` para banner deve seguir esta estrutura:

```
[CENA PRINCIPAL: sujeito + ação + expressão específica do hook],
[ELEMENTO DISRUPTIVO do estilo escolhido],
[ÂNGULO DE CÂMERA: 85mm telephoto / low angle hero shot],
[LUZ: rim backlight dourado da direita + fill azul da esquerda],
[AMBIENTE/CENÁRIO específico com detalhe de textura],
[ATMOSFERA: volumetric clouds / dramatic sky / efeito halo]
```

**O script adiciona automaticamente:**
cinematic movie poster, photorealistic, Hollywood color grade, 8K, no text, no watermark, anatomically correct, no distorted limbs.

**Exemplos práticos:**

| Hook | Exemplo de prompt (parcial) |
|------|----------------------------|
| Exagero | `Young woman with eyes wide and hands on cheeks in shock, giant countdown clock exploding behind her, 85mm hero shot low angle, golden rim light from right, dark storm clouds with dramatic lightning` |
| Polêmica | `Man in suit pressing finger to lips holding a glowing sealed envelope, mysterious dark corridor, 85mm telephoto low angle, warm golden rim light from right, cool blue fill from left, fog particles` |
| Curiosidade | `Hands slowly opening a glowing golden vault door, bright ethereal light spilling out, dramatic side lighting, dark marble hall, 85mm low angle hero shot, volumetric god rays` |
| Notícia | `Urgent newscaster pointing at breaking news countdown clock showing 00:00, dramatic TV studio, 85mm hero shot, cold blue studio lighting mixed with warm backlight` |
| Reflexão | `Person standing at crossroads looking at two diverging lit paths, one bright the other dark, 85mm telephoto, warm sunset backlight, dramatic low angle, fog on ground` |

### Mostrar antes de gerar:

```
BANNER — Prompt para aprovação

Estilo disruptivo: [nome]

Prompt (EN — enviado ao modelo):
> [prompt completo]

Tradução (PT — conferência):
> [tradução fiel]

Referência: [caminho OU "sem referência"]

1. Aprovar e gerar
2. Ajustar o prompt
3. Trocar o estilo disruptivo
```

---

## Etapa 04.5. Referência visual

```
Vai usar alguma imagem de referência para o banner?

1. Sim
2. Não
```

Se Sim: consultar `.claude/skills/carrossel-visual/references/skill-referencia-visual.md` e seguir o fluxo de referência.

Referência com troca de personagem: usar OpenRouter obrigatoriamente (único provider com visão).

---

## Etapa 05. Gerar banner

### Config JSON

Salvar em:
`meus-produtos/{ativo}/entregas/criativos/config-banner-{slug}-{n}.json`

Schema:
```json
{
  "slug":                 "{slug-do-produto}",
  "handle":               "@{handle}",
  "output_dir":           "meus-produtos/{ativo}/entregas/criativos",
  "filename":             "banner-{slug}-{n}",
  "accent":               "{cor-de-destaque}",
  "credit":               "NOME DO PRODUTO OU TAGLINE",
  "headline":             "HEADLINE EM CAIXA ALTA",
  "headline_highlight":   "PALAVRA",
  "subheadline":          "Subtítulo em estilo pôster",
  "prompt_en":            "Epic cinematic scene..."
}
```

### Executar

```bash
py -3 scripts/gerar-banner-estatico.py --config [caminho-do-config]
```

O script:
1. Gera foto via Freepik (padrão) ou OpenRouter
2. Renderiza HTML com gradiente e texto
3. Screenshot via Chrome headless
4. Salva PNG em output_dir

---

## Etapa 06. Revisão final

- [ ] Headline em ALL CAPS
- [ ] Palavra de destaque na cor de destaque
- [ ] Subheadline em itálico, complementa o headline
- [ ] Handle do produto no rodapé
- [ ] Foto cinematográfica com elemento disruptivo visível
- [ ] Gradiente na base permite ler o texto com clareza
- [ ] Proporção 4:5 (1080x1350px) correta para feed Instagram

---

## Providers

| Provider | Quando usar | Parâmetros |
|----------|-------------|-----------|
| OpenRouter | Sempre (padrão único) | google/gemini-3.1-flash-image-preview |

---

## Entrega final

```
Banner salvo em:
meus-produtos/{ativo}/entregas/criativos/banner-{slug}-{n}.png

Para publicar:
1. Abra a pasta
2. Use o PNG diretamente no Instagram (feed portrait 4:5)

Próximos passos:
- Copy do anúncio: /copy-anuncio
- Carrossel com mesma urgência: /copy-carrossel (opção 2)
- Outro banner: /img-anuncio novamente
```

---
name: usar-referencia-visual
description: Cria banner estático ou carrossel a partir de uma imagem de referência enviada pelo usuário. Segue o processo da Máquina de Conteúdo: pergunta quantidade, nome da sessão, origem da imagem (link ou caminho), modo de edição (trocar personagem, alterar texto, cor, edição pontual) e executa gerar-banner-estatico.py via OpenRouter.
allowed-tools: Read, Write, Bash
---

# Usar Referência Visual

## TERMINOLOGIA OBRIGATÓRIA

| Termo | O que é |
|-------|---------|
| **LAYOUT REFERÊNCIA** | Design ou cena pronta que serve de base visual |
| **PERSONAGEM** | Foto da pessoa que vai entrar no LAYOUT |

Nunca chamar os dois de "referência". Sempre LAYOUT REFERÊNCIA ou PERSONAGEM.

---

## PASSO 0 — Contexto

Leia `meus-produtos/.ativo`, depois `meus-produtos/{ativo}/perfil.md`.
Extraia: handle, slug, cor de destaque do produto ativo.

---

## PASSO 1 — Quantidade

```
Quantas imagens você quer criar?

1 — Banner estático (1 imagem)
2 a 10 — Carrossel (N cards)
```

- N = 1 → continuar neste fluxo (Banner Estático)
- N ≥ 2 → acionar skill `carrossel-visual`

---

## PASSO 2 — Nome da sessão

```
Qual o nome desta criação?
(ex: "mulher-agachada", "homem-terno-azul", "texto-novo")
```

Criar pasta de trabalho:
```bash
mkdir -p "meus-produtos/{ativo}/entregas/criativos/{nome-sessao}/REFERENCIA"
```

Todos os arquivos desta sessão ficam em:
`meus-produtos/{ativo}/entregas/criativos/{nome-sessao}/`

---

## PASSO 3 — Origem da imagem

```
Como você vai enviar o LAYOUT REFERÊNCIA?

1 — Link (URL direta, Instagram, Pinterest)
2 — Caminho local (arquivo no seu computador)
```

### Se LINK:

Executar:
```bash
curl -L "{link}" -o "meus-produtos/{ativo}/entregas/criativos/{nome-sessao}/REFERENCIA/layout.png"
```

Se for link do Instagram (contém `instagram.com`):
- Avisar que o Instagram pode bloquear download direto
- Pedir que o usuário salve a imagem manualmente e informe o caminho local

### Se CAMINHO LOCAL:

Copiar para a pasta de trabalho:
```bash
cp "{caminho-informado}" "meus-produtos/{ativo}/entregas/criativos/{nome-sessao}/REFERENCIA/layout.png"
```

Confirmar que o arquivo existe antes de continuar:
```bash
ls "meus-produtos/{ativo}/entregas/criativos/{nome-sessao}/REFERENCIA/"
```

Se houver múltiplas imagens na pasta REFERENCIA (ex: carrossel baixado), listar e perguntar:
```
Qual imagem você quer usar como LAYOUT REFERÊNCIA?
(listar os arquivos encontrados)
```

---

## PASSO 4 — O que fazer com o LAYOUT?

```
O que você deseja fazer nessa imagem?

1 — Trocar personagem
2 — Alterar texto da arte
3 — Alterar cor de elementos
4 — Edição pontual (detalhe específico)
```

---

## PASSO 5 — Detalhes por modo

### Modo 1 — Trocar personagem

```
Envie a foto do PERSONAGEM.
(caminho local ou link da imagem)
```

Salvar em:
```bash
cp "{caminho-personagem}" "meus-produtos/{ativo}/entregas/criativos/{nome-sessao}/REFERENCIA/personagem.png"
```

Depois:
```
Qual roupa o PERSONAGEM novo deve usar?

1 — Roupa do LAYOUT (manter a da cena original)
2 — Roupa do PERSONAGEM (usar a da foto enviada)
```

**Prompt obrigatório (EN):**
```
Edit the image using the provided reference.

Maintain EXACTLY:
- layout, composition, camera angle, framing
- lighting, shadows, background, color palette, perspective
- ALL text, typography, overlays, graphic elements, logos and watermarks present in the original image

Change ONLY the main character.

The new character must:
- match the environment perfectly
- follow the same lighting direction
- match shadows and reflections
- maintain realistic proportions
- integrate naturally into the scene

[Se roupa do LAYOUT: "Dress the new character in the same outfit as the original character in the scene."]
[Se roupa do PERSONAGEM: "Keep the new character's original clothing from the reference photo."]

DO NOT change layout, background, camera angle or composition.
DO NOT remove, alter or add any text, overlays or graphic elements.
DO NOT distort the image.

The final result must look like the new character was always part of the original image.
Ultra realistic, high detail, professional quality.
anatomically correct, no distorted limbs, no distorted fingers.
```

---

### Modo 2 — Alterar texto da arte

```
Qual texto deve substituir o texto atual?
```

Em seguida:
```
Quer ajuda para escrever um gancho na imagem?

1 — Sim, me ajude
2 — Não, vou usar meu texto
```

Se **1 (Sim)**: carregar `.claude/skills/carrossel-visual/references/hooks-imagem-disruptiva.md` e propor 3 opções de gancho curto (máx 6 palavras). Aguardar escolha.

**Prompt obrigatório (EN):**
```
Edit the image using the provided reference.

Maintain EXACTLY:
- layout, typography style, font weight
- spacing, alignment, hierarchy, colors, composition

Change ONLY the text content.

Replace the text with: [NOVO TEXTO]

Ensure:
- same font appearance and size proportions
- same positioning and alignment

DO NOT change layout, colors, move elements or alter design.

The final result must look identical, with only the text replaced.
```

---

### Modo 3 — Alterar cor de elementos

```
Qual elemento você quer mudar a cor?
(ex: "fundo", "camisa", "botão", "texto principal")

Qual a nova cor?
(nome ou hex — ex: "azul escuro" ou "#1A2B4C")
```

**Prompt obrigatório (EN):**
```
Edit the image using the provided reference.

Maintain EVERYTHING exactly the same.

Change ONLY the color of: [ELEMENTO]
New color: [COR]

Ensure:
- natural color blending
- lighting consistency
- shadows and texture preserved

DO NOT affect other elements, change layout or composition.
Ultra realistic color adaptation.
```

---

### Modo 4 — Edição pontual

```
Descreva o que você quer modificar:
(ex: "remover os óculos", "trocar a cor da camisa para vermelho", "adicionar um relógio no pulso")
```

**Prompt obrigatório (EN):**
```
Edit the image using the provided reference.

Maintain EXACTLY:
- identity of the subject, face structure
- lighting, composition, environment

Modify ONLY: [DETALHE DESCRITO PELO USUÁRIO]

Ensure: natural integration, no artifacts, no distortion, consistent lighting.

The final result must look original and untouched.
High realism, clean edit, professional quality.
anatomically correct, no distorted limbs.
```

---

## PASSO 6 — Executar diretamente

Assim que o usuário responder a última pergunta do modo escolhido, **executar imediatamente sem pedir confirmação**.

### Montar o config JSON

Salvar em:
`meus-produtos/{ativo}/entregas/criativos/{nome-sessao}/config-ref.json`

```json
{
  "slug":               "{slug}",
  "handle":             "@{handle}",
  "output_dir":         "meus-produtos/{ativo}/entregas/criativos/{nome-sessao}",
  "filename":           "banner-ref-{slug}",
  "accent":             "{cor-do-produto-ou-#FF6B01}",
  "credit":             "",
  "headline":           "",
  "headline_highlight": "",
  "subheadline":        "",
  "prompt_en":          "[prompt do modo escolhido]"
}
```

Para modo 2 (alterar texto): headline e subheadline ficam vazios. O texto é alterado direto na imagem pelo modelo.

### Executar

**Com LAYOUT apenas (modos 2, 3, 4):**
```bash
py -3 scripts/gerar-banner-estatico.py \
  --config "meus-produtos/{ativo}/entregas/criativos/{nome-sessao}/config-ref.json" \
  --ref-layout "meus-produtos/{ativo}/entregas/criativos/{nome-sessao}/REFERENCIA/layout.png" \
  --skip-html
```

**Com LAYOUT + PERSONAGEM (modo 1):**
```bash
py -3 scripts/gerar-banner-estatico.py \
  --config "meus-produtos/{ativo}/entregas/criativos/{nome-sessao}/config-ref.json" \
  --ref-layout "meus-produtos/{ativo}/entregas/criativos/{nome-sessao}/REFERENCIA/layout.png" \
  --ref-personagem "meus-produtos/{ativo}/entregas/criativos/{nome-sessao}/REFERENCIA/personagem.png" \
  --skip-html
```

Provider: **OpenRouter obrigatório** em todos os modos. Freepik não é usado neste fluxo.

---

## PASSO 7 — Entrega

Após gerar o PNG:

```
Arquivo: meus-produtos/{ativo}/entregas/criativos/{nome-sessao}/banner-ref-{slug}.png

1 — Aprovado
2 — Gerar nova versão
3 — Ajustes específicos
```

Se **3**: perguntar o que ajustar e rodar novamente com o prompt ajustado.
Se **2**: rodar novamente com o mesmo config (o modelo gera variação natural).

---

## REGRAS INVIOLÁVEIS

- Provider obrigatório: **sempre OpenRouter**. Freepik não é usado em nenhuma hipótese neste fluxo
- LAYOUT REFERÊNCIA sempre salvo em `REFERENCIA/` dentro da pasta da sessão
- PERSONAGEM sempre salvo em `REFERENCIA/personagem.png`
- Nunca chamar "referência" sem qualificador: use sempre LAYOUT REFERÊNCIA ou PERSONAGEM
- Hooks de imagem disruptiva: aplicar quando o usuário pedir ajuda com texto (Modo 2)
- **Executar direto após a última pergunta do modo** — sem bloco de aprovação intermediário
- Apresentação de menu limpa: uma pergunta por vez, sem parênteses explicativos. Sub-opções só aparecem depois da escolha

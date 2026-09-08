# Skill de Referência Visual

> Prioridade máxima sobre qualquer outra instrução visual quando o usuário envia uma imagem de referência.

---

## Quando usar

O usuário envia uma imagem de referência e diz que quer usá-la como base para um card do carrossel ou banner estático.

---

## Terminologia obrigatória

| Termo | O que é |
|-------|---------|
| LAYOUT REFERÊNCIA | Design ou cena pronta que serve de base visual para o novo card |
| PERSONAGEM | Foto da pessoa (criador, avatar) que vai entrar no layout |

Nunca chamar os dois de "referência". Sempre LAYOUT REFERÊNCIA ou PERSONAGEM.

---

## Etapa obrigatória antes de editar

Após receber o LAYOUT REFERÊNCIA, perguntar:

```
O que você quer fazer nessa imagem?

1. Trocar o personagem (manter cenário, trocar pessoa)
2. Alterar o texto da arte
3. Alterar a cor de elementos
4. Edição pontual (detalhe específico)
```

Nunca executar sem essa definição.

---

## Modo 1. Trocar personagem

Perguntar em seguida:

```
Qual roupa o personagem novo deve usar?

1. Roupa do layout (manter a roupa da cena original)
2. Roupa do personagem (usar a roupa que aparece na foto enviada)
```

Prompt padrão para o modelo:

```
Edit the image using the provided reference.

Maintain EXACTLY:
- layout, composition, camera angle, framing
- lighting, shadows, background, color palette, perspective

Change ONLY the main character.

The new character must:
- match the environment perfectly
- follow the same lighting direction
- match shadows and reflections
- maintain realistic proportions
- integrate naturally into the scene

DO NOT change layout, background, camera angle or composition.
DO NOT distort the image.

The final result must look like the new character was always part of the original image.
Ultra realistic, high detail, professional quality.
anatomically correct, no distorted limbs.
```

---

## Modo 2. Alterar texto da arte

Prompt padrão:

```
Edit the image using the provided reference.

Maintain EXACTLY:
- layout, typography style, font weight
- spacing, alignment, hierarchy, colors, composition

Change ONLY the text content.

Replace the text with: [NOVO TEXTO]

Ensure:
- same font appearance, same size proportions
- same positioning, perfect alignment

DO NOT change layout, colors, move elements or alter design.

The final result must look identical, with only the text replaced.
```

---

## Modo 3. Alterar cor de elementos

Prompt padrão:

```
Edit the image using the provided reference.

Maintain EVERYTHING exactly the same.

Change ONLY the color of: [ELEMENTO]
New color: [COR]

Ensure: natural color blending, lighting consistency, shadows and texture preserved.

DO NOT affect other elements, change layout or composition.
Ultra realistic color adaptation.
```

---

## Modo 4. Edição pontual

Prompt padrão:

```
Edit the image using the provided reference.

Maintain EXACTLY:
- identity of the subject, face structure
- lighting, composition, environment

Modify ONLY: [DETALHE ESPECÍFICO]

Ensure: natural integration, no artifacts, no distortion, consistent lighting.

The final result must look original and untouched.
High realism, clean edit, professional quality.
```

---

## Regras de execução

- Provider obrigatório com referência: **OpenRouter** via `generate-creative.py` com `--provider openrouter`
- Para trocar personagem: passar 2 referências (LAYOUT + PERSONAGEM) na chamada
- Nunca entregar foto crua. Sempre passar pelo pipeline de composição do carrossel
- Salvar LAYOUT REFERÊNCIA em `meus-produtos/{ativo}/entregas/criativos/referencias/`
- Aplicar os hooks de imagem disruptiva mesmo em cards com referência (o prompt ainda carrega o elemento de ruptura)

---

## Integração com o carrossel

Quando o usuário escolher usar referência durante o fluxo de `/copy-carrossel`:

1. Perguntar para quais cards (capa, cards específicos ou todos)
2. Para cada card referenciado: solicitar o LAYOUT REFERÊNCIA
3. Se troca de personagem: solicitar também a foto do PERSONAGEM
4. Construir o prompt usando o template do modo escolhido
5. Executar via `generate-creative.py` com `--provider openrouter` e as referências
6. Compor o card normalmente após a foto gerada

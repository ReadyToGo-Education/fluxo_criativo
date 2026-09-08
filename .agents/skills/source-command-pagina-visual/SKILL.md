---
name: "source-command-pagina-visual"
description: "Criar página de vendas a partir de prints de referência do aluno + copy aprovada. Cada print vira uma cópia HTML com design 100% preservado (sem harmonização global). Seções sem print são geradas a partir do design system extraído das cópias existentes. Montagem final concatena tudo em vendas-{slug}.html."
---

# source-command-pagina-visual

Use this skill when the user asks to run the migrated source command `pagina-visual`.

## Command Template

# Página Visual. Clone de prints + copy aprovada

Gera uma página de vendas combinando cópias HTML (uma por print) com a copy aprovada. Cada cópia preserva seu design literal (cores, fontes, espaçamentos do print). Seções sem print são geradas pela IA usando o design system extraído das cópias existentes.

## Usage

```
/pagina-visual
```

## Pré-requisitos

1. Produto ativo (`meus-produtos/.ativo`) com perfil cadastrado
2. Copy aprovada em `meus-produtos/{ativo}/entregas/copy-pagina/copy-{ativo}.md` com 16 blocos (`## Bloco 01` até `## Bloco 16`). Sem isso, pedir pra gerar via `/copy-pagina`.
3. Prints de referência. Dois caminhos aceitos:
   - **Caminho A (recomendado).** Aluno cola os prints no chat um por um
   - **Caminho B.** Aluno salva em `meus-produtos/{ativo}/entregas/paginas/referencias/` (pasta temporária, só pra input de prints)

## Estrutura de pastas gerada

```
meus-produtos/{slug}/entregas/
  copy-pagina/copy-{slug}.md            # copy aprovada (input)
  paginas/
    referencias/                         # pasta temporária de input de prints (pode deletar depois)
      bloco-01-hero.png
      ...
    copias/                              # OUTPUT. HTMLs de seção
      manifest.json                      # ordem das seções + mapeamento cópia -> bloco de copy
      design-system.json                 # tokens extraídos das cópias (usado pra seções sem print)
      hero-{slug}.html                   # cópia fiel do print + copy adaptada
      reverse-ui-testemunhos-{slug}.html
      faq-gerada-{slug}.html             # seção GERADA (sem print) usando design-system.json
    assets/
    vendas-{slug}.html                   # página final montada
```

## Fluxo (7 etapas)

### Etapa 1. Coletar prints (Caminho A ou B)

Primeiro cheque `meus-produtos/{ativo}/entregas/paginas/referencias/`. Se tiver prints, pule pra Etapa 2.

Se vazio, ative Caminho A:

```
Pra montar sua página, vou precisar dos prints das seções que você quer clonar.

Estrutura padrão 8D tem 16 blocos:
01 Hero       05 CTA           09 Bônus            13 Garantia
02 Dor        06 Método        10 Stack de valor   14 Autoridade
03 Paliativo  07 Para quem     11 Prova social 2   15 FAQ
04 Prova 1    08 Entregáveis   12 Suporte          16 Oferta final

Você NÃO precisa ter print de todos. Blocos sem print são gerados pela IA usando o design system extraído das cópias que você colar.

Cole os prints aqui um por um, dizendo qual bloco cada um é.
Exemplo: "este é o bloco 01 hero"

Quando terminar, digite "pronto".
```

Para cada print colado: identifique o bloco, salve em `referencias/bloco-NN-chat.png` (via Write na imagem anexada), confirme `✅ Print bloco NN salvo.`

### Etapa 2. Extrair design system das cópias potenciais (1 chamada, ~6-8k tokens)

Com todos os prints coletados, invoque a skill `ui-reverse-engineer` passando todos os prints DE UMA VEZ. Peça APENAS JSON estruturado, sem HTML ainda:

```json
{
  "paleta_dominante": {
    "bg": "#ffffff",
    "surface": "#f8f9fa",
    "ink": "#111827",
    "accent": "#3b82f6",
    "muted": "#6b7280"
  },
  "tipografia": {
    "fonte_heading": "'Plus Jakarta Sans', sans-serif",
    "fonte_body": "'Inter', sans-serif",
    "google_fonts_link": "<link href='https://fonts.googleapis.com/css2?family=Inter...' rel='stylesheet'>"
  },
  "border_radius": "16px",
  "estilo_botao": {
    "bg": "#3b82f6",
    "color": "#ffffff",
    "radius": "12px",
    "padding": "14px 28px"
  },
  "sombra_padrao": "0 4px 12px rgba(0,0,0,0.08)",
  "mood": "clean|denso|editorial|artistic-chaos",
  "observacoes": "Notas livres sobre padrões visuais que se repetem entre os prints."
}
```

Salve em `paginas/copias/design-system.json`. Confirme:

```
✅ Design system extraído e salvo em copias/design-system.json
Paleta: {cores}, fonte: {fonte}, mood: {mood}
```

Importante: este design system **NÃO é aplicado nas cópias existentes**. Cada cópia preserva seu design literal. O design-system.json serve **apenas** pra gerar seções que NÃO têm print.

### Etapa 3. Montar manifest.json (ordem + mapeamento cópia → bloco)

Crie `paginas/copias/manifest.json` listando todas as 16 seções na ordem da página 8D. Cada entrada marca se tem print (cópia) ou se precisa gerar:

```json
[
  {"secao": "hero", "bloco_copy": "01", "copia": "hero-{slug}.html", "tem_print": true, "print": "referencias/bloco-01-hero.png"},
  {"secao": "dor", "bloco_copy": "02", "copia": "dor-gerada-{slug}.html", "tem_print": false},
  {"secao": "paliativo", "bloco_copy": "03", "copia": "paliativo-gerada-{slug}.html", "tem_print": false},
  ...
]
```

Mostre ao aluno o resumo:

```
📋 Manifest da página montado:

Com print (reprodução fiel):  {N} seções
Sem print (geradas pela IA):  {M} seções

Ordem: {lista da estrutura 8D}

Seguir para clonagem paralela? (1. sim / 2. ajustar ordem ou mapeamento)
```

### Etapa 4. Clonar seções COM print EM PARALELO (subagents)

Para cada entrada com `tem_print: true`, dispare um subagent `clonador-de-bloco-visual` em uma ÚNICA mensagem com múltiplos `Agent` tool calls (paralelismo real).

Prompt self-contained pra cada agente:

```
Clone a seção {secao_id} a partir do print e adapte a copy aprovada.

secao_id: {secao}
nome_bloco: {nome}
bloco_copy_num: {bloco_copy}
bloco_copy_conteudo:
---
{colar AQUI o texto do bloco correspondente extraído de copy-pagina/copy-{slug}.md}
---
caminho_print: {caminho absoluto do print}
caminho_destino: meus-produtos/{slug}/entregas/paginas/copias/{secao}-{slug}.html

Modo: A (COM print)

Siga a especificação do seu agente (clonador-de-bloco-visual.md).
Retorne apenas a mensagem estruturada (SECAO_ID, STATUS, PATH, etc.).
```

**Envie todos os Agent calls numa ÚNICA mensagem do assistente.**

### Etapa 5. Gerar seções SEM print EM PARALELO (subagents)

Para cada entrada com `tem_print: false`, dispare um subagent `clonador-de-bloco-visual` em Modo B (sem print):

```
Gere a seção {secao_id} a partir do design system + copy aprovada.

secao_id: {secao}
nome_bloco: {nome}
bloco_copy_num: {bloco_copy}
bloco_copy_conteudo:
---
{texto do bloco}
---
caminho_print: (nenhum, gerar do zero)
caminho_destino: meus-produtos/{slug}/entregas/paginas/copias/{secao}-gerada-{slug}.html
design_system_path: meus-produtos/{slug}/entregas/paginas/copias/design-system.json

Modo: B (SEM print, usar design system)

Siga a especificação (Modo B).
```

Pode rodar as etapas 4 e 5 juntas (todos os subagents no mesmo batch) pra máxima paralelização.

Quando todos retornarem, mostre sumário:

```
✅ Clonagem concluída.

Seções com print (fiéis):   {N}/{N_total}
Seções geradas pela IA:     {M}/{M_total}

Arquivos em: meus-produtos/{slug}/entregas/paginas/copias/
```

### Etapa 6. Montar página final

Rode o script Python de montagem:

```bash
py -3 scripts/montar-pagina-copias.py --slug {slug} --verbose
```

O script:

1. Lê `copias/manifest.json`
2. Para cada entrada, lê o HTML da cópia correspondente
3. Extrai `<style>` e escopa sob `.secao-{id}` (evita colisão entre seções)
4. Extrai `<body>` e envolve em `<div class="secao-{id}">...</div>`
5. Deduplica fontes do Google entre cópias
6. Concatena tudo num HTML final
7. Salva em `paginas/vendas-{slug}.html`

Confirme:

```
✅ Página montada. Caminho: meus-produtos/{slug}/entregas/paginas/vendas-{slug}.html
Tamanho: {N} KB. Seções: {N_secoes}. Abra no navegador pra conferir.
```

### Etapa 7. Ajustes pós-montagem

Ofereça:

```
Próximos passos possíveis:
1. Ver a página no navegador e ajustar alguma seção específica (/pagina-ajuste)
2. Conectar checkout (/pagina-checkout)
3. Instalar Meta Pixel (/pagina-pixel)
4. Publicar (/pagina-lovable ou /pagina-vercel)
```

## Regras importantes

- **Cada cópia é visual isolada.** CSS escopado por wrapper. Nada de variáveis globais atravessando seções.
- **Cópias com print são intocadas** quanto ao design. Só os textos mudam (copy adaptada).
- **Seções sem print** usam o `design-system.json` como referência, mas cada uma ainda é independente (design system é ponto de partida, não amarração).
- **Se o aluno mudar só a copy depois**: basta rodar de novo os subagents da etapa 4/5 (ou só das seções afetadas) e re-rodar o `montar-pagina-copias.py`. As cópias não mudam — só os textos dentro delas são re-adaptados.
- **Se o aluno adicionar um print novo depois**: atualize o manifest (muda `tem_print` de `false` para `true` naquela entrada), rode o subagent daquela seção, rode a montagem. Todas as outras cópias ficam intactas.
- **Custo estimado por página completa:**
  - 3 prints + 13 seções geradas: ~50-70k tokens (primeira geração)
  - Re-rodar só a montagem (copy mudou, mas cópias ficam): ~zero tokens
  - Re-adaptar copy em uma seção: ~3k tokens (1 subagent)

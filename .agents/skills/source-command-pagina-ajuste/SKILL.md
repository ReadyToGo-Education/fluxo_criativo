---
name: "source-command-pagina-ajuste"
description: "Ajustes pós-merge guiados por perguntas. Diagnóstico, cores para layout, menu (conversão, vídeo, autoridade, SEO, imagens, incrementar copy, headline, placeholders de imagem, ideias de imagens), upload ou geração IA em assets/, só então edita o bloco atômico e re-roda o merge. Use quando pedir /pagina-ajuste ou ajustes na página."
---

# source-command-pagina-ajuste

Use this skill when the user asks to run the migrated source command `pagina-ajuste`.

## Command Template

# Página ajuste. Etapa pós-merge (modo guiado)

Este comando **não aplica tudo automaticamente no escuro**. O fluxo padrão é: **diagnóstico → você escolhe o que fazer → coleta do que falta (texto, links, imagens) → edição do bloco atômico → merge Python**.

Referência técnica dos itens possíveis: `.Codex/skills/paginas/references/etapa-ajustes-pagina.md`.

Não substitui `/feedback-pagina` (auditoria Nav) nem `/pagina-performance`.

## REGRA DE OURO (obrigatória, sem exceção)

> **Sempre edite a cópia da seção primeiro, depois rode o merge Python.**

O HTML final em `meus-produtos/{slug}/entregas/paginas/vendas-{slug}.html` é **gerado** pelo script `scripts/montar-pagina-copias.py` a partir das cópias em `paginas/copias/`. Não é a fonte da verdade. Editar direto nele perde a alteração no próximo merge.

**Fluxo obrigatório para qualquer alteração visual ou de texto em uma seção:**

1. **Identificar a cópia da seção.** Listar `meus-produtos/{slug}/entregas/paginas/copias/` e achar o arquivo HTML correspondente à seção (ex: `hero-{slug}.html`, `dor-gerada-{slug}.html`, `faq-gerada-{slug}.html`). O `manifest.json` da mesma pasta tem o mapeamento completo seção → arquivo.

2. **Pré-requisito.** Se a pasta `paginas/copias/` não existir, avise o aluno que a página ainda não foi montada via `/pagina-visual`. Ofereça rodar esse command antes.

3. **Editar o HTML da cópia** mantendo a regra de design isolado:
   - **Preserve** as cores em HEX literal da cópia (não substitua por tokens globais)
   - **Preserve** as classes e estrutura do HTML original
   - **Nunca** introduza `var(--ds-*)` ou variáveis CSS globais em uma cópia
   - **Nunca** mescle cores/fontes de outras cópias — cada uma é isolada
   - Adapte a copy ao design existente (Light Copy VTSD: sem travessão, sem "Não é X. É Y.", sem promessa vaga)

4. **Rodar o merge Python** pra regerar o HTML final:

   ```bash
   py -3 scripts/montar-pagina-copias.py --slug {slug}
   ```

   O script lê `paginas/copias/manifest.json`, recompõe o HTML final escopando CSS de cada cópia e salva em `paginas/vendas-{slug}.html`.

5. **Confirmar em uma linha:**

   ```
   ✅ Alteração aplicada na cópia {arquivo} e página remontada. Caminho: meus-produtos/{slug}/entregas/paginas/vendas-{slug}.html
   ```

**Se a alteração requer mudança estrutural grande** (refazer layout da seção, mudar grid, trocar tipo de componente):
- Ofereça re-clonar a seção via subagent `clonador-de-bloco-visual` (modo B, sem print, com design-system.json) — entrega HTML novo mantendo o design system local
- Ou: peça ao aluno um print novo daquela seção e re-rode `/pagina-visual` só pra ela

**Exceção única (ajustes globais pós-merge):** `<title>`, `<meta name="description">`, `<meta og:*>`, script do Pixel, rodapé global. Esses vivem na "casca" do HTML montado, não dentro das cópias. Podem ser editados direto em `vendas-{slug}.html`, mas **serão sobrescritos** no próximo merge. Alternativa: adicionar no topo/fim do script `montar-pagina-copias.py` (seção de head ou footer) pra persistir.

## Usage

```
/pagina-ajuste
```

## O Que Fazer

### 1. Contexto (sempre)

1. Ler `meus-produtos/.ativo` para o slug do produto.
2. Ler `meus-produtos/{ativo}/perfil.md` e, se existir, `meus-produtos/{ativo}/entregas/copy-pagina/copy-{slug}.md`.
3. Arquivo alvo padrão: `meus-produtos/{ativo}/entregas/paginas/vendas-{slug}.html` (ou o caminho que o usuário disser).
4. **Onde as imagens ficam no projeto (sempre deixar explícito para o aluno ao falar de imagens):**
   - **No disco:** pasta **`meus-produtos/{ativo}/entregas/paginas/assets/`** (ao lado do HTML da página, não na raiz do repositório).
   - **No HTML:** referências relativas à pasta do arquivo, em geral **`assets/nome.ext`** (ex.: `src="assets/logo.png"`). O mesmo vale para `og:image` (URL relativa ou absoluta do domínio final; se for arquivo local, costuma ser `assets/og-....jpg`).
   - **Geração por script:** `scripts/generate-openrouter-nano-banana-images.py` grava os PNG **direto** nessa pasta `assets/` do produto (`--slug` = nome da pasta em `entregas/`).
   - Em resumo ao aluno: *"As imagens ficam em `entregas/{seu-produto}/paginas/assets/` e a página aponta para elas com `assets/...`."*

### 2. Diagnóstico rápido (leitura do HTML)

Antes de qualquer pergunta ao usuário, inspecionar o HTML (busca por placeholders, `href="#"`, `data-checkout-placeholder`, `[`, `SuaMarca`, iframe vazio, `pravatar`, texto "placeholder", `og:`, ausência de `og:image`, seções óbvias de template) e cruzar com perfil e copy.

Montar uma lista **Pendências detectadas** em linguagem humana, por exemplo:

- Checkout ainda genérico ou bloqueado
- Vídeo na primeira dobra ainda placeholder ou embed errado
- Autoridade sem nome ou bio real
- Depoimentos só modelo ou fotos genéricas
- Title ou meta genéricos (se aparecer)
- Rodapé com marca genérica ou links `#`
- Imagens: falta logo, foto do criador, fotos de clientes, imagem para redes (Open Graph)

Não assumir que tudo está errado: marcar só o que o arquivo realmente mostra.

### 3. Primeira interação com o usuário (obrigatória)

**Não editar o arquivo nesta primeira mensagem** (salvo o usuário já ter dito explicitamente "aplica tudo" ou "só atualiza o checkout com este link").

Apresentar:

1. **Pendências detectadas** (bullets curtos).
2. **Cores para o layout (obrigatório na primeira rodada):** antes de editar o HTML com mudança visual (botões, fundos, bordas, gradientes, destaques), **sempre** perguntar qual cor ou quais cores predominantes o aluno quer usar. Se já estiverem claras no próprio arquivo ou no perfil (hex, nome), pode resumir e pedir confirmação curta.

```
Para alinhar botões, fundos e detalhes com a sua marca, qual é a cor ou quais são as cores predominantes?

1. Te passo agora (hex, nome da cor ou descreva, ex.: azul escuro #1e3a5f e bege #e8dcc4)
2. Estão no logo ou manual que anexo ou indico na pasta
3. Manter o que a página já tem por enquanto
4. Ainda não tenho paleta; quero sugestão coerente com o nicho e o perfil

Digite o número:
```

- Se **1** ou **2:** anotar valores (hex quando possível) e usar como referência em qualquer ajuste de CSS ou Tailwind no fluxo.
- Se **3:** não alterar paleta por iniciativa, exceto se o aluno pedir depois num dos itens do menu.
- Se **4:** propor 2 a 3 combinações curtas com base em `perfil.md` e nicho, **uma opção por vez** ou lista numerada para escolha, e só então aplicar ao editar.

3. **Pergunta principal:**

Antes do menu, **perguntar de forma explícita** se o aluno quer nesta rodada trabalhar **copy**, **headline**, **placeholders de imagem** ou **ideias de imagens** (pode ser uma linha introdutória: *"Quer incrementar copy, ajustar headline, revisar placeholders de imagem ou ver sugestões de imagens que enriquecem a página? Escolha no menu abaixo os números 8 a 11, ou outro foco."*).

```
Quais ajustes você quer fazer agora na página?

1. Conversão (link de checkout, preço e parcelas, botões)
2. Vídeo na primeira dobra (embed YouTube ou caixa de placeholder)
3. Autoridade (nome, bio, foto do criador, números ou marcos)
4. Provas e depoimentos (texto e troca de fotos dos depoimentos)
5. SEO (title, meta description, opcional Open Graph)
6. Rodapé (marca, termos, privacidade)
7. Imagens do site (upload, encaixe no HTML, ver pergunta abaixo)
8. Incrementar copy (refinar ou expandir trechos com base em perfil e copy aprovada em copy-pagina)
9. Ajustar headline (headline, subheadline e bullets da primeira dobra, alinhados à copy)
10. Verificar placeholders de imagem (varrer `[Sua foto aqui]`, avatares genéricos, src vazio ou genérico, og:image ausente)
11. Análise de imagens para enriquecer a página (onde fotos, prints ou artes subiriam credibilidade ou clareza; lista sugestiva, sem obrigar produção)
12. Varredura completa: aplicar tudo que ainda estiver pendente de uma vez (modo direto)
13. Só o diagnóstico por hoje, sem alterar arquivo

Digite um ou mais números (ex.: 1, 8, 10) ou descreva em uma frase:
```

4. **Bloco imagens (sempre oferecer na primeira rodada, mesmo que escolham só depois):**

Explicar de forma curta que imagens deixam a página mais crível e listar **o que pode pedir**, sem exigir tudo de uma vez:

- Logo ou nome no topo (se quiser trocar texto por imagem)
- Foto do criador na seção de autoridade
- Fotos reais ou autorizadas nos depoimentos (em vez de avatar genérico)
- Prints de planilha ou produto (para hero ou método, se fizer sentido)
- Imagem para compartilhamento em redes (`og:image`, 1200×630 é referência comum)

Perguntar:

```
Você já tem imagens para subir (logo, sua foto, prints, fotos de clientes)?

1. Sim, vou colar ou anexar agora / indicar pasta
2. Ainda não, só texto e links por enquanto
3. Quero orientação de tamanho e nome de arquivo antes de produzir as artes
4. Quero gerar imagens com IA (a partir de prompts) e depois encaixar na página

Digite o número:
```

Se escolher **1**, orientar: criar se fizer sentido `meus-produtos/{ativo}/entregas/paginas/assets/` e usar nomes claros (`logo.png`, `foto-criador.jpg`, `depo-marina.jpg`, `og-planilhas.jpg`). Depois de receber arquivos ou caminhos, atualizar o HTML com `src` relativos tipo `assets/foto-criador.jpg` (caminho relativo ao HTML).

Se escolher **4 (gerar com IA)**, não pular referências. Fazer nesta ordem:

1. **Confirmar pré-requisito:** chave `OPENROUTER_API_KEY` no `.env` na raiz do repositório (ver `.env.example`). Se não tiver, explicar que o fluxo é: colar a chave, salvar, rodar o script na raiz (passo abaixo) ou pedir para o assistente rodar se o ambiente permitir.
2. **Perguntar quais slots** ainda estão com placeholder ou genérico (hero, autoridade, depoimentos, OG, seção específica). Uma pergunta ou lista numerada se já estiver claro no diagnóstico.
3. **Passar referências de estilo** (o assistente resume em linguagem humana, sem obrigar o aluno a abrir tudo):
   - **Playbook de evolução visual e prompts:** `.Codex/skills/paginas/references/playbook-evolucao-visual-html-landing.md` (direção Fluent ou corporativa, negativos tipo “sem personagem cartoon”, uso de cor da marca `#0f7937` só como detalhe quando fizer sentido).
   - **Script de geração em lote:** `scripts/generate-openrouter-nano-banana-images.py` (lê `JOBS` com `file`, `aspect_ratio`, `prompt` em inglês; grava em `meus-produtos/{slug}/entregas/paginas/assets/`).
   - **Ferramenta:** comando típico na raiz: `py -3 scripts/generate-openrouter-nano-banana-images.py --slug {ativo}`; para só algumas imagens novas no fim da lista, usar `--skip N` e `--max M` conforme o cabeçalho do script.
4. **Coletar intenção por imagem:** nicho, tom (ex.: produto digital sério, MEI, planilha), o que não pode aparecer (texto legível na arte, logos de terceiros, estilo infantil). Isso vira trecho do prompt ou entrada em `JOBS`.
5. **Depois que os PNG existirem na pasta `assets/`:** atualizar o HTML (`src`, `alt`, OG se for o caso) como na opção 1. Se o merge for rodado de novo, relembrar reaplicar `src` se o template sobrescrever.

**Regra:** uma decisão por vez se a conversa encher de opções. Se o usuário mandar vários números, confirmar a ordem ou tratar o primeiro e perguntar se segue para o próximo.

### 4. Execução por bloco escolhido

Só depois da escolha (ou do envio de link ou imagem), e **já tendo** resposta sobre cores (passo 2) quando a alteração for visual:

- Usar as **cores predominantes** confirmadas ao ajustar classes inline, variáveis Tailwind no `theme.extend`, `style` ou gradientes. Se o aluno não definiu cor e o bloco exige decisão visual, perguntar antes de gravar.
- Aplicar **Etapa 0** (vícios proibidos) do SKILL `paginas` em qualquer texto novo.
- Editar o HTML no disco. **Não** colar o arquivo inteiro no chat.
- Resumir em bullets o que mudou e repetir o caminho do arquivo.

Para cada bloco, se faltar dado objetivo (URL de checkout, nome do criador, URL do vídeo), usar **uma pergunta por vez**, no padrão do `AGENTS.md` (opções numeradas quando couber).

**Itens 8 a 11 (copy, headline, placeholders, análise de imagens):**

- **8. Incrementar copy:** comparar HTML com `copy-pagina/copy-{slug}.md` quando existir; sugerir reforços em bullets, parágrafos curtos ou CTAs sem contradizer a copy aprovada. Aplicar **Etapa 0** do SKILL `paginas`. Se não houver arquivo de copy, usar `perfil.md` e **uma** pergunta por vez sobre o que reforçar.
- **9. Ajustar headline:** foco na primeira dobra (premissa, subheadline, três bullets do hero). Propor alternativas em linguagem humana, pedir escolha ou ajuste, depois gravar no HTML. Respeitar regra de produto fora do lead quando couber.
- **10. Verificar placeholders de imagem:** listar no chat os pontos encontrados (seletores ou trecho do `src`/`alt`), priorizar o que bloqueia publicação, pedir arquivos ou encaminhar para o fluxo da opção **7** ou geração IA.
- **11. Análise para enriquecer com imagens:** leitura estratégica da página (hero, método, depoimentos, oferta). Entregar **lista em bullets** do tipo “seção X ganharia com print de Y”, sem gerar arte no escuro; oferecer seguir para opção **7** ou **4** (IA) se o aluno quiser.

### 5. Imagens. Comportamento detalhado

- Se o usuário **não** tiver imagens: registrar no resumo o que ficou recomendado (lista de slots) para quando tiver.
- Se **tiver** (upload): atualizar `src`, `alt` e, se necessário, `width`/`height` ou classes para não quebrar o layout.
- Se escolher **gerar com IA:** seguir o fluxo da opção **4** na primeira interação: referências (`playbook-evolucao-visual-html-landing.md`, script `generate-openrouter-nano-banana-images.py`, `.env`), slots necessários, prompts alinhados ao produto; depois encaixar arquivos gerados no HTML.
- Mencionar que imagens pesadas devem ser comprimidas antes (sem obrigar ferramenta técnica; pode sugerir "exportar para web" ou ferramenta simples).
- Open Graph: se pedirem, adicionar no `<head>` as meta tags `og:title`, `og:description`, `og:image` (e `og:url` se souberem o domínio final).

### 6. Modo 12 (varredura completa)

Só usar se o usuário escolher **12**. Aí sim seguir a checklist de `etapa-ajustes-pagina.md` de forma ativa, ainda assim **listando antes** o que será alterado e pedindo confirmação se algo for incerto (ex.: inventar nome do criador). Incluir na varredura, quando fizer sentido: revisão de placeholders de imagem e menção a oportunidades de arte (sem aplicar copy pesada sem pedido).

### 7. Entrega e lembrete

- Lembrar que novo `workshop-merge-pagina.py` pode sobrescrever title e meta; reaplicar ajustes após novo merge.
- Sugerir próximos passos: `/feedback-pagina`, `/pagina-performance`, `/pagina-pixel`, `/pagina-checkout`.

## Regras

- Português do Brasil. Proibição de travessão em texto ao usuário e em copy visível.
- Não prometer resultado fiscal nem lucro garantido ao editar texto.
- Não confundir com `/pagina-performance`.

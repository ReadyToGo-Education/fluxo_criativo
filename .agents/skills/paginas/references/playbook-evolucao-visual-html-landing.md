# Playbook: evolução visual e imagens em landing HTML (qualquer produto)

Referência para **agentes e skills** ao melhorar páginas já existentes em `entregas/{slug}/paginas/*.html`, com ou sem merge prévio. Vale para **qualquer infoproduto ou projeto** que use o mesmo padrão de entrega (HTML único, Tailwind via CDN, marca verde `#0f7937` quando aplicável).

**Criação da página (ordem correta):** antes de qualquer evolução visual aqui, o fluxo padrão é **copiar** o tema para `entregas/{slug}/paginas/templates-{estilo}/` com `scripts/workshop-copy-template-tema.py`, **colocar a copy** nos `code.html` dessa cópia e rodar `scripts/workshop-merge-pagina.py` com `--templates-root`. Este playbook entra **depois**, na página já mergeada (`vendas-{slug}.html`).

Este documento consolida **processos** testados na prática: troca de estética “cartoon”, geração ou substituição de imagens, tipografia, contraste de texto, interação por abas e revisão de overlays.

## Objetivo

Entregar uma sequência **repetível** para o assistente:

1. Entender o que o aluno critica (infantil, texto ilegível, abas que não mudam cópia, etc.).
2. Aplicar melhorias **sem refazer a página inteira** sem necessidade.
3. Documentar decisões que funcionem no **próximo** produto, não só no arquivo atual.

## Mapa rápido dos processos

| Processo | Quando usar | Saída típica |
| --- | --- | --- |
| A. **Direção visual** | Ilustrações “Pixar”, mascotes, cenário infantil | Cena abstrata (CSS), ícones Material, ou novo PNG via gerador |
| B. **Imagens raster** | Precisa de foto ou render 3D “de verdade” | Arquivos em `entregas/{slug}/paginas/assets/` + prompts no script |
| C. **Tipografia e quebra de linha** | Título com palavra órfã, subtítulo quebrando feio | `text-wrap: balance`, `max-w-*` maior, `text-pretty` onde fizer sentido |
| D. **Cor do texto** | Texto parece branco ou some no fundo claro | Cor explícita `#18181b` (CSS ou `style`), revisar `selection:` no `body` |
| E. **Interação por abas** | Menu lateral “Membros / Arquivos / Suporte” ou equivalente | `role="tablist"`, `data-*`, JS que atualiza **todos** os blocos de cópia ligados |
| F. **Overlays em cima da arte** | Caixas escuras com texto branco sobre ilustração | Remover texto, ou cartão claro com texto escuro, ou eliminar overlay |
| G. **QA final** | Antes de declarar pronto | Checklist no fim deste arquivo |

## A. Direção visual: do infantil ao corporativo

**Sinais comuns:** personagens fofos, olhos grandes, cenário “quarto à noite”, animais vestidos de escritório.

**Direção alinhada a produto B2B e VTSD:** estilo **Fluent / produto digital** (formas geométricas, vidro fosco, gradientes frios, sombra suave), **sem personagem** como foco.

**Opções de implementação (escolher uma ou combinar):**

1. **Somente front-end (rápido, sem custo de API)**  
   - Fundo em gradiente + camadas (`div` com blur, placas semitransparentes).  
   - Ícone grande **Material Symbols** (checklist, pasta, suporte) central ou em cartão vidro.  
   - Accent verde da marca só em detalhe (borda fina, ícone, linha do título), não em personagem.

2. **Imagem gerada (Nano Banana / OpenRouter)**  
   - Prompts em **inglês** costumam obedecer melhor.  
   - Incluir negativos: `no cartoon characters`, `no cute animals`, `no readable text`, `no logos`.  
   - Incluir positivos: `Microsoft Fluent Design`, `frosted glass`, `isometric`, `enterprise`, `subtle green accent #0f7937`.

3. **Híbrido**  
   - PNG neutro de fundo + UI em CSS por cima. Menos dependência de re-gerar pixel a cada revisão.

**Onde registrar prompts reutilizáveis:** array `JOBS` em `scripts/generate-openrouter-nano-banana-images.py` (um objeto por arquivo em `assets/`), com `file`, `aspect_ratio`, `image_size`, `prompt`.

## B. Pipeline de imagens (raster)

**Onde os arquivos entram no projeto:** todos os PNG (upload manual ou saída do script) ficam em **`entregas/{slug}/paginas/assets/`**. O HTML da landing em **`entregas/{slug}/paginas/vendas-*.html`** usa `src="assets/nome-do-arquivo.png"` (relativo ao arquivo HTML). Ao orientar o aluno, repetir esse caminho de pasta.

**Script:** `scripts/generate-openrouter-nano-banana-images.py`  
**Pré-requisito:** `.env` na raiz com `OPENROUTER_API_KEY` (ver `.env.example`).

**Fluxo sugerido:**

1. Definir nomes finais dos arquivos (ex.: `hero-depois-compra-membros.png`) e pasta `entregas/{slug}/paginas/assets/`.
2. Acrescentar entradas em `JOBS` ou usar modo `--output` + `--prompt` para teste único.
3. Rodar na raiz do repositório, exemplo:  
   `py -3 scripts/generate-openrouter-nano-banana-images.py --slug nome-do-produto`  
4. Limitar lote com `--skip N` e `--max M` quando só faltam imagens novas no fim da lista.
5. **Placeholder:** até a API rodar, pode-se copiar um PNG existente para o nome novo para não quebrar `src` no HTML.

**Após trocar assets:** conferir `alt` em português, sem promessa vazia; manter uma linha de estilo visual entre imagens da mesma seção.

## C. Tipografia e quebra de linha

**Problema:** última linha do título com uma palavra só (ex.: “é”), subtítulo com “cobre.” isolado.

**Ajustes genéricos:**

- Container do título: de `max-w-2xl` para **`max-w-4xl`** quando o título for longo em português.
- Subtítulo: de `max-w-xl` para **`max-w-2xl`** quando o texto for parágrafo completo.
- CSS global útil: `text-wrap: balance` em `section h2`, `main h1` com `font-extrabold` (já usado em páginas deste repositório).
- Utilitário Tailwind **`text-balance`** em títulos ou leads críticos (quando o CDN suportar).

## D. Cor do texto e Tailwind CDN

**Problema observado:** classes do tipo `text-ink/80` ou `text-marca/85` com cor **customizada** no `tailwind.config` embutido **podem não gerar CSS** no CDN. O navegador aí não aplica cor da classe e o texto pode **herdar** cor errada ou parecer branco sobre fundo claro.

**Soluções estáveis (qualquer produto):**

1. Cor explícita: **`text-[#18181b]`** ou **`style="color:#18181b;"`** nos parágrafos sensíveis.
2. Regra CSS com seletor da seção, exemplo: `.tpl-flat-suporte #id-do-paragrafo { color: #18181b; }`.
3. No `<body>`, para seleção de texto: **`selection:bg-ink`** precisa de **`selection:text-white`** (ou cor clara), **não** `selection:text-base` (no Tailwind, `text-base` é tamanho de fonte, não cor).

## E. Interação: abas e cópia sincronizada

**Requisito típico:** ao clicar em cada item (Membros, Arquivos, Suporte), mudar **imagem ou cena**, **subtítulo do bloco**, **parágrafo longo** e, se existir, **rótulos** de cartões.

**Padrão de implementação:**

- `role="tablist"` na lista de botões; cada botão `role="tab"`, `aria-selected`, `aria-controls` apontando para o painel.
- Painel `role="tabpanel"` com `id` estável; atributo **`data-depois-active`** (ou nome genérico `data-tab`) com valor da chave ativa.
- Objeto JavaScript único (`DEPOIS_DATA` ou `TAB_COPY`) com chaves por aba: `intro` (linha curta sob o H2), `desc` (parágrafo lateral ou inferior), e caminhos de imagem ou só troca de classe no painel.
- Ao trocar aba: atualizar `textContent` dos parágrafos com `id`; atualizar `setAttribute('data-*-active', key)` no painel para CSS trocar cenas.

**Cenas só com CSS:** três blocos `.scene--a`, `.scene--b`, `.scene--c` absolutos; visibilidade com `[data-active="a"] .scene--a { opacity: 1; }`. Sem PNG, evita estilo infantil e custo de imagem.

## F. Overlays sobre a ilustração

Se houver caixas escuras com texto branco e o aluno quiser **sem texto na arte** ou **texto escuro:**

- Remover os nós HTML do overlay **ou** esvaziar e usar só moldura decorativa.
- Se precisar de legenda, colocá-la **fora** da área da imagem, no fluxo da coluna, com cor `#18181b` ou cinza escuro.

## G. Seção de bônus (cartões)

**Substituição de PNG cartoon:** topo do cartão com bloco **Fluent leve** (gradiente + orbes + ícone Material), mais **estado ativo** ao clique (`outline` verde ou classe `is-active`) se o briefing pedir “mostrar o que foi clicado”.

## Checklist para o agente (copiar mentalmente)

- [ ] Crítica do aluno traduzida em decisão: só CSS, só imagem, ou ambos?
- [ ] Texto longo da página continua alinhado à copy em `entregas/{slug}/copy-pagina/` quando existir?
- [ ] Títulos: `balance` + largura de container suficiente?
- [ ] Parágrafos críticos com cor **#18181b** ou equivalente explícito se o tema custom falhar?
- [ ] Abas: subtítulo + descrição + painel mudam juntos?
- [ ] Imagens novas: `JOBS` ou documentação de prompt para rerun?
- [ ] `alt` acessível e sem travessão na copy visível (regra global do assistente)?
- [ ] Pós-alteração pesada: lembrar `etapa-ajustes-pagina.md` e link de checkout se for página de venda?

## Referências cruzadas

| Documento | Uso |
| --- | --- |
| `etapa-ajustes-pagina.md` | Pós-merge e antes de tráfego; onde ficam imagens no repo |
| `.claude/commands/pagina-ajuste.md` | Fluxo guiado: diagnóstico, cores, menu (copy, headline, placeholders de imagem, ideias de imagens, conversão, SEO), imagens em `paginas/assets/` |
| `template-copy-pagina-vendas.md` | Alinhamento copy 16 blocos |
| `scripts/generate-openrouter-nano-banana-images.py` | Geração em lote de PNG |
| `skills/ferramentas/SKILL.md` | OpenRouter (anúncios e assets de landing) |
| `CLAUDE.md` | Regras de copy, entregas, aprovação |

## Nota para manutenção deste playbook

Quando um novo padrão visual se repetir em **dois** projetos (ex.: novo componente de abas), vale extrair snippet para `design-system-components.md` ou template atômico em `skills/paginas/references/templates/`, e aqui deixar só o **processo** e o link.

---
name: paginas
description: >
  Base de conhecimento para criação de páginas web profissionais.
  Inclui estrutura 8D de página de vendas, biblioteca de 65+ templates HTML
  cobrindo todas as 13 seções da estrutura em 5 estilos visuais
  e padrões visuais. Inclui etapa de ajustes pós-merge (checkout, SEO, placeholders).
  Fluxo padrão: copiar tema com workshop-copy-template-tema.py, preencher cópia em entregas, merge com --templates-root.
  Acionada automaticamente pelo command /copy-pagina.
---

# Páginas. Base de Conhecimento

## Regras de Fluxo para Páginas

1. **Coletar TUDO antes de gerar copy.** Tudo o que for necessário para a página deve ser perguntado ANTES de gerar qualquer copy. Não gerar copy assumindo dados que não foram coletados ou confirmados.
2. **Validar a copy com o usuário ANTES de gerar o HTML.** Mostrar toda a copy textual, pedir aprovação, e só depois gerar o arquivo HTML.
3. **Revisão e correção automática SEMPRE.** Após gerar a copy ou o HTML, aplicar a **Etapa 0 (vícios proibidos)** deste SKILL no texto visível e corrigir o que for necessário. Informar ao usuário o número de ajustes feitos. Só então entregar ou salvar.
4. **Exceção de exibição:** O HTML não é mostrado ao usuário (seria confuso). Salvar direto e informar o caminho do arquivo.
5. **Custo-benefício (geração de HTML):** **Primeiro** copiar o tema para `entregas/{slug}/paginas/templates-{estilo}/` com `scripts/workshop-copy-template-tema.py` (command `copy-pagina`, B1.5). **Depois** preencher os `code.html` **nessa cópia** e fechar com `scripts/workshop-merge-pagina.py --tema {estilo} --templates-root entregas/{slug}/paginas/templates-{estilo} --copiar-entregas` (ou `build_merge.py` dentro da pasta `pagina_completa_{estilo}` **da mesma cópia**). **Não** reproduzir no chat o `pagina_completa_*/code.html` inteiro. **Não** montar um único HTML em `entregas/` colando seções, salvo exceção pedida pelo usuário. Auditoria Nav: `/feedback-pagina`; não carregar esse arquivo longo em toda gravação.
5a. **Preservar o template (só trocar a copy):** cada `code.html` atômico já é o layout final daquele tema. **Proibido** “reinventar” a página: alterar estrutura de markup, sistema de grid, blocos de estilo, `<style>` do arquivo, paleta ou fontes do tema, ou substituir o template por HTML novo gerado do zero. **Permitido:** colar a copy aprovada nos nós de texto, ajustar `href`, `src`, `alt`, textos de botão e placeholders. **Exceção:** fluxo de exceção do command `copy-pagina` (HTML customizado) com custo explícito, ou ajustes **depois** do merge (`/pagina-ajuste`, playbook de visual) quando o aluno pedir evolução visual pontual.
6. **Copy fiel na página de vendas:** antes de preencher cada bloco HTML, ler a seção correspondente `## Bloco NN` em `entregas/{ativo}/copy-pagina/copy-{produto}.md` (estrutura obrigatória em `references/template-copy-pagina-vendas.md`). **Proibido** inventar preço, garantia ou depoimento que não estejam na copy aprovada. Se o arquivo não existir, seguir B0 do command `copy-pagina`.
7. **Etapa de ajustes (pós-merge), antes de “página pronta”:** depois que existir `entregas/{ativo}/paginas/vendas-{slug}.html`, conduzir ajustes via comando **`/pagina-ajuste`** (diagnóstico, **pergunta sobre cor ou cores predominantes para layout**, menu de escolhas com **incrementar copy**, **headline**, **placeholders de imagem**, **análise de imagens para enriquecer**, **imagens: upload ou geração com IA** com referências em `references/playbook-evolucao-visual-html-landing.md` e script `scripts/generate-openrouter-nano-banana-images.py` quando o aluno quiser gerar, depois edição). A lista técnica completa está em `references/etapa-ajustes-pagina.md`. Em resumo o que pode ser fechado: checkout, preço, vídeo, autoridade, SEO, segunda prova social se duplicada, rodapé, paleta alinhada com o aluno, copy e hero, revisão de imagens, imagens em `paginas/assets/`. Não substitui `/feedback-pagina` nem `/pagina-performance`.

## Estrutura 8D (Página de Vendas VTSD)

1. **Header**. Logotipo + CTA pequeno (opcional)
2. **Primeira Dobra (Hero)**. Premissa (headline) + subheadline + 3 bullets (Urgência Oculta + Decorado) + vídeo + CTA
3. **Problema/Dor**. Dor amplificada com cenas do cotidiano
4. **Paliativo**. Ferramentas, produtos e soluções concorrentes do mercado que resolvem parcialmente o problema, e por que cada uma não entrega o resultado completo
5. **Prova Social (1º bloco)**. 2-3 depoimentos curtos de resultado rápido. Objetivo: validar que o problema é real e que tem gente resolvendo. Vem ANTES do método para ancorar credibilidade cedo.
6. **CTA intermediário**. Seção curta com botão
7. **Solução/Método**. Apresentação da Furadeira na estrutura da mecânica registrada no `perfil.md` (Fases e Sequências, Lógica Condicional, Enquadramento, Listas, Empecilhos ou Dinâmica de Entrega). O nome do produto/método aparece aqui pela primeira vez. **Imagem PNG embutida (obrigatória quando existir):** se `meus-produtos/{ativo}/entregas/furadeira/furadeira.png` existir, embutir como `<img>` no topo desta seção. A imagem é gerada por `/furadeira-visual` (que decide o layout visual sozinha conforme a mecânica + nicho). Se ainda não existir, sugerir ao aluno rodar `/furadeira-visual` antes de gerar a página, ou seguir só com a estrutura textual. Diagrama visual aumenta percepção de método estruturado e diferencia a página de concorrentes que usam só texto.
8. **Para Quem É / Não É**. Listas com ícones check/X
9. **Entregáveis**. Lista completa com metáforas de valor (grid 2 colunas)
10. **Bônus**. 3 bônus estratégicos com valor individual
11. **Stack de Valor**. Ancoragem visual (valor total vs preço real)
12. **Prova Social (2º bloco)**. 3-5 depoimentos completos com foto, situação antes e resultado depois. Agora o leitor já conhece o método e os depoimentos confirmam.
13. **Garantia**. Tipo + prazo + selo visual
14. **FAQ**. Accordion funcional (5-8 objeções da persona)
15. **Oferta Final (CTA)**. Ancoragem de valor + preço + parcelamento + CTA grande
16. **Rodapé**. Termos, privacidade, copyright

### Primeira Dobra — Regras da Premissa

A premissa é o headline principal da hero. É o argumento que leva o leitor à Big Idea sem parecer uma promessa direta. Toda página de vendas começa com ela.

**Critérios obrigatórios:**
- Até 10 palavras
- Foco em um único resultado (sem conjunção aditiva "e")
- Gera curiosidade e desejo imediato de saber mais
- Memorável e específica para o nicho
- Não revela todos os detalhes — instiga

**O que a premissa NÃO é:**
- Slogan ou frase motivacional
- Explicação longa sobre o produto
- Promessa vaga ou abstrata
- Começa com verbo no imperativo
- Contém interrogação ou exclamação
- Usa "através de" ou "com" para sugerir o caminho
- Usa conjunção aditiva ("e") — a premissa transmite um único resultado

**Exemplos validados de premissa:**
- Tem gente cobrando R$800 por uma página feita com IA em 3 horas.
- O segredo das finanças não é quanto você ganha, mas quanto você consegue manter.
- Guardar dinheiro é bom, mas fazer o dinheiro trabalhar por você é melhor.
- Quem vende barato vende menos.
- Ansiedade não é normal.
- Todo paciente tem cura.
- Pessoas bonitas usam maquiagem.
- Não precisa abrir uma empresa para ficar rico.
- A melhor receita de sobremesa não exige forno nem açúcar.
- Economizar pode ser o maior erro financeiro que você pode cometer.
- Falhar mais vezes pode ser a maneira mais rápida de alcançar seus sonhos.
- O método certo pode transformar uma rotina exaustiva em um negócio que roda sozinho.
- Você pode criar um estilo de vida saudável com apenas 15 minutos por dia.

**Padrões de estrutura que funcionam:**
- "O melhor jeito de [conseguir X] é [fazer Y]."
- "Todo mundo pode [alcançar X] se souber [fazer Y]."
- "Afirmação contra-intuitiva que inverte a crença mais comum do nicho."
- "Dado ou fato específico que o público não esperava ver."

## Regras Universais

- **Texto SEMPRE em pt-BR com acentos** (Módulos, não Modulos)
- **Header com logotipo obrigatório** em toda página
- **TODAS as fontes DEVEM ser sans-serif**. heading E body. Fontes serifadas são PROIBIDAS em qualquer parte da página (heading, body, labels, tudo). Serifadas dão cara de template genérico de IA e prejudicam leitura em telas.
- **Biblioteca de fontes aprovadas** (todas do Google Fonts CDN, todas sans-serif):

### Fontes Sans-Serif Aprovadas (Google Fonts CDN)

**PROIBIDO usar fontes serifadas**. Playfair Display, Fraunces, Noto Serif, Lora, Merriweather, Source Serif, Instrument Serif, Cormorant, Libre Baskerville, EB Garamond, Crimson Text e qualquer outra serif estão BANIDAS.

#### Heading (display/títulos). Escolher 1

| Fonte | Estilo | Ideal para | Pesos |
|---|---|---|---|
| **Space Grotesk** | Geométrica moderna | Tech, SaaS, inovação | 400, 500, 700 |
| **Sora** | Geométrica suave | Startups, apps, moderno | 400, 600, 700, 800 |
| **Outfit** | Geométrica limpa | Clean, versátil, qualquer nicho | 400, 500, 600, 700, 800 |
| **Plus Jakarta Sans** | Humanista moderna | Premium, coaching, educação | 500, 600, 700, 800 |
| **Montserrat** | Geométrica clássica | Negócios, finanças, autoridade | 500, 600, 700, 800, 900 |
| **Raleway** | Elegante geométrica | Moda, beleza, lifestyle | 400, 500, 600, 700, 800 |
| **Poppins** | Geométrica arredondada | Amigável, saúde, educação | 400, 500, 600, 700, 800, 900 |
| **Urbanist** | Neo-grotesca | Imobiliário, luxo moderno | 400, 500, 600, 700, 800, 900 |
| **Bebas Neue** | Condensada bold | Marketing, impacto, headlines | 400 |
| **Fjalla One** | Condensada impacto | Títulos curtos, esporte, energia | 400 |
| **Albert Sans** | Grotesca variável | Versátil, clean, minimalista | 400, 500, 600, 700, 800 |
| **General Sans** (Fontshare) | Neo-grotesca | Premium, editorial moderno | 400, 500, 600, 700 |
| **Bricolage Grotesque** | Grotesca expressiva | Criativo, artsy, artesanato | 400, 600, 700, 800 |
| **Lexend** | Otimizada para leitura | Educação, acessibilidade | 400, 500, 600, 700 |
| **Figtree** | Amigável geométrica | Pet, saúde, bem-estar | 400, 500, 600, 700, 800 |
| **Clash Display** (Fontshare) | Display bold | Headlines de impacto | 400, 500, 600, 700 |
| **Cabinet Grotesk** (Fontshare) | Geométrica moderna | Tech, startup | 400, 500, 700, 800 |

#### Body (texto corrido). Escolher 1

| Fonte | Estilo | Ideal para | Pesos |
|---|---|---|---|
| **DM Sans** | Humanista moderna | Versátil, qualquer nicho | 400, 500, 600, 700 |
| **Manrope** | Geométrica legível | Tech, SaaS, premium | 400, 500, 600, 700 |
| **Nunito** | Arredondada acolhedora | Saúde, educação, feminino | 400, 500, 600, 700 |
| **Source Sans 3** | Neo-grotesca funcional | Finanças, negócios, formal | 400, 500, 600, 700 |
| **Inter** | Neo-grotesca neutra | Tech, dados, interfaces | 400, 500, 600, 700 |
| **Outfit** | Geométrica clean | Versátil, pode ser heading e body | 400, 500, 600 |
| **Plus Jakarta Sans** | Humanista moderna | Premium, coaching | 400, 500, 600 |
| **Nunito Sans** | Companheira do Nunito | Saúde, bem-estar | 400, 500, 600, 700 |
| **Work Sans** | Grotesca compacta | Negócios, produtividade | 400, 500, 600 |
| **Rubik** | Arredondada moderna | Amigável, apps | 400, 500, 600 |
| **Karla** | Grotesca levemente humanista | Blogs, conteúdo longo | 400, 500, 600, 700 |
| **Archivo** | Neo-grotesca sólida | Estabilidade, finanças | 400, 500, 600, 700 |
| **Red Hat Display** | Display legível | Moderno, clean | 400, 500, 600, 700 |
| **Lexend** | Otimizada para leitura rápida | Educação, conteúdo denso | 400, 500, 600 |
| **Figtree** | Geométrica amigável | Pet, wellness, família | 400, 500, 600 |
| **Geist** (Vercel) | Mono-inspirada | Dev tools, tech, startup | 400, 500, 600, 700 |

#### Combinações Recomendadas por Nicho

| Nicho | Heading | Body |
|---|---|---|
| Finanças/Business | Montserrat 700 | Source Sans 3 400,600 |
| Saúde/Bem-estar | Poppins 700 | Nunito 400,600 |
| Educação/Cursos | Fjalla One 400 | Nunito 400,600 |
| Feminino/Lifestyle | Raleway 700 | DM Sans 400,500 |
| Artesanato/Handmade | Bricolage Grotesque 700 | DM Sans 400,500 |
| Marketing/Negócios | Bebas Neue 400 | DM Sans 400,500,700 |
| Tech/Produtividade | Space Grotesk 500,700 | Inter 400,500 |
| Premium/High Ticket | Urbanist 700 | Manrope 400,500,600 |
| Coaching/Dev Pessoal | Plus Jakarta Sans 700 | Plus Jakarta Sans 400,500 |
| Pet/Animais | Figtree 700 | Figtree 400,500 |
| Imobiliário/Luxo | Urbanist 800 | Source Sans 3 400,600 |
| Gastronomia | Sora 700 | DM Sans 400,500 |
| Beleza/Skincare | Raleway 600 | Outfit 400,500 |

**Regra**: Heading e body podem ser a mesma fonte (variando peso) ou fontes diferentes. Ambas DEVEM ser sans-serif.

**⛔ Restrição da fonte Inter (padrão "neutro de IA"):** Inter é a fonte mais usada por geradores de IA (v0, Lovable, Bolt, Figma defaults). Quando aparece em nichos emocionais, comunica "template genérico". Use Inter APENAS em nichos técnicos/racionais: **Tech/Produtividade**, **Finanças com dashboards/dados**, **SaaS B2B**. **PROIBIDA em:** Coaching, Dev Pessoal, Beleza, Feminino, Artesanato, Saúde emocional, Gastronomia, Pet. Para esses, usar DM Sans, Manrope, Figtree, Plus Jakarta Sans ou Nunito como body.

**⛔ Poppins também tem restrição.** Poppins é a segunda fonte mais genérica de IA (padrão de templates free do Canva e Figma). Evitar em Premium/High Ticket. Permitida em Saúde/Bem-estar e Educação popular, mas prefira Figtree ou Plus Jakarta Sans quando o produto for premium.

- **Grids de 2 colunas** para entregáveis (NÃO 3. evita texto apertado)
- **Cards com min-width 320px**, padding 28px+, font-size 0.95rem+
- **4+ tipos de fundo** alternando entre seções (claro, escuro, imagem+overlay, gradiente, textura)
- **2+ seções com fundo forte** (CSS gradient artístico ou Unsplash com ID específico + overlay. Picsum proibido, ver "Imagens Contextuais")
- **NÃO parecer Lovable/v0**. sem cards brancos idênticos em fundo bege

## Vícios Proibidos na Copy da Página

> ⛔ BLOQUEIO OBRIGATÓRIO. Esta etapa não é opcional. Nenhum HTML pode ser salvo e nenhuma copy pode ser entregue sem passar por esta revisão completa. Sem exceção.

**ETAPA 0. Varredura Anti-Vícios (executar ANTES de salvar ou mostrar qualquer coisa):**

Percorra TODO o texto gerado e elimine cada item abaixo. Se encontrar, corrija na hora antes de continuar:

| Vício | Ação obrigatória |
|---|---|
| Travessão (. ) em qualquer frase | Reescreva a frase inteira sem ele. Não substitua por vírgula se a frase ficar estranha. refaça a construção. |
| Estrutura "Não é X. É Y." | Desenvolva o argumento de outra forma. Nunca use essa construção. |
| Ponto de exclamação | Remova. A frase deve ser impactante sem ele. |
| Pergunta no gancho ou headline | Transforme em afirmação com tensão. |
| Frase genérica de vendedor | Substitua por dado concreto ou cena real do cotidiano. |
| Promessa vaga sem número ou situação | Especifique: prazo, quantidade, situação real. |
| "mesmo que" ou "sem precisar" como muletas | Reescreva o argumento sem essas muletas. |
| Bullets que não seguem padrão urgência oculta + decorado | Reescreva no padrão correto. |
| Produto mencionado nos primeiros parágrafos da hero | Reescreva focando no leitor, não no produto. INCLUI: nome do produto, nome do método, nome do curso, sigla do programa. A primeira dobra fala APENAS sobre o leitor e o problema/transformação dele. O nome do produto/método só aparece a partir da seção Solução/Método (seção 7). Sem exceção, mesmo que o nome pareça um "posicionamento de identidade". |
| Emojis | Remova sem substituição. |
| Lero-lero: palavras que soam bem mas dizem nada ("padrão interno", "segurança interna", "caminhos terapêuticos", "processos emocionais", "reconectar com a sensibilidade") | Teste: dá para trocar por outra palavra genérica do mesmo nicho e o sentido continua igual? Substitua por dado concreto, cena real ou argumento específico. |
| Copy sem tese (descreve o problema sem argumentar por que ele existe) | Adicione a razão causa do problema. Ex: "Você procrastina" vira "Você procrastina porque seu cérebro foi programado para ação imediata e não para acumular reservas". |
| Sigla ou nome de técnica sem explicação no mesmo parágrafo | Insira explicação entre parênteses ou reescreva sem a sigla. |
| Depoimento que só elogia sem resultado concreto ("material lindo", "mudou minha vida") | Sinalizar para substituição. O depoimento que converte tem: antes + resultado específico + número ou prazo. |

Após a varredura, confirme internamente: "Não há nenhum travessão, exclamação, pergunta no gancho ou estrutura proibida neste texto." Só então salve ou entregue.

- [ ] Nenhum travessão no texto
- [ ] Nenhuma estrutura "Não é X. É Y."
- [ ] Nenhuma frase genérica de vendedor
- [ ] Produto não mencionado no hero/lead (inclui nome do produto, nome do método, nome do curso ou sigla)
- [ ] Nenhum emoji
- [ ] Headline sem imperativo ou pergunta no gancho
- [ ] Zero lero-lero: toda palavra-chave é concreta ou foi substituída
- [ ] Há tese (argumento de causa) na copy, não só descrição de dor
- [ ] Método tem facilitação visual (diagrama, esquema ou antes/depois) ou está sinalizado para incluir
- [ ] Siglas e técnicas explicadas no mesmo parágrafo em que aparecem
- [ ] Depoimentos com resultado concreto ou sinalizados para substituição

---

## Design System e Montagem

### Fluxo de Geração (OBRIGATÓRIO. SEM EXCEÇÃO)

> ⛔ BLOQUEIO: Nenhuma página HTML pode ser gerada sem passar pelas 6 etapas abaixo. Pular qualquer etapa resulta em página genérica e será considerado erro de execução.

**Etapa 1. Escolher UM ÚNICO estilo visual para a página inteira**
Consultar a **Tabela de Decisão de Estilo Visual (por nicho)** mais abaixo. Extrair do `perfil.md` o nicho do produto e pegar o estilo recomendado. A página inteira usa esse mesmo estilo do início ao fim. Exemplo: nicho "Pet/Animais" → `teal_claro` em TODAS as seções.

> ⛔ PROIBIDO misturar estilos visuais diferentes na mesma página. Cada estilo (`flat_claro`, `teal_claro`, `glass_escuro`, `dark_solido`, `minimal_claro`) é um design system completo e independente. misturar quebra a consistência e faz a página parecer duas páginas grudadas. Uma página = um estilo.

**Etapa 2. Mapear seções ao estilo único**
Todas as seções (hero, dor, paliativo, método, entregáveis, bônus, stack, prova social, garantia, FAQ, CTA intermediário, oferta final) seguem o mesmo estilo visual escolhido na Etapa 1. O que varia é:
- **Paleta de cores** aplicada sobre o estilo (cada nicho tem paleta própria. ver "Paletas por Nicho")
- **Variantes internas do estilo** para dar ritmo visual (ex: no `flat_claro`, alternar `hero_flat_claro`, `hero_flat_claro_centralizado`, `hero_flat_claro_depoimentos`)
- **Tom de fundo dentro do mesmo estilo** (ex: base `#fafafa` no hero, `#f3f4f6` no paliativo, ambos pertencentes ao mesmo estilo `flat_claro`)

**Etapa 3. LER OS TEMPLATES REAIS DO ESTILO ESCOLHIDO (obrigatório)**
Para cada seção da página, ler o arquivo `references/templates/{secao}_{estilo}/code.html`, usando SEMPRE o mesmo estilo da Etapa 1.

**Seções com template (todas as 13 seções da estrutura 8D agora têm template em todos os estilos):**
- `hero` (e variantes `_centralizado`, `_depoimentos` em flat/teal/glass/purple)
- `dor`
- `paliativo`
- `provas_sociais` (depoimentos completos com foto, antes/depois)
- `metodo` (Furadeira)
- `entregaveis` (grid 2 colunas)
- `bonus` (3 bônus estratégicos)
- `garantia` (selo + prazo + texto confiante)
- `oferta_final` (stack de valor + preço grande + CTA)
- `autoridade` (criador do método)
- `suporte` (canais de acompanhamento)
- `cta` (CTA intermediário)
- `faq` (accordion)

**Estilos disponíveis:** `glass_escuro`, `flat_claro`, `teal_claro`, `dark_solido` (anteriormente `purple_escuro` no disco), `minimal_claro`. **Escolher apenas UM por página.**

**Regra de leitura por seção (otimização contra os 10+ minutos):** ao gerar uma seção específica, ler APENAS o arquivo `references/templates/{secao}_{estilo}/code.html` correspondente. Não pré-carregar todos os 13 templates antes de começar. Carregar o template só na hora de gerar aquela seção. Isso é o que torna possível a geração seção por seção sem estourar tempo (ver "Geração por bloco com aprovação" no command `/copy-pagina`).

**Fallback:** se uma combinação seção × estilo não existir em disco, usar `references/design-system-components.md` HERDANDO os tokens CSS (border-radius, border-width, shadow style, spacing) do estilo escolhido, para que a seção pareça nativa do mesmo design system.

**Etapa 4. Extrair tokens do estilo e aplicar como design system mestre**
Antes de montar as seções, extrair dos templates lidos os tokens visuais base do estilo:
- `--border-width` (ex: `0` no teal/glass, `1.5px` no flat)
- `--border-style` (sólida, soft cinza, glassmorphism, nenhuma)
- `--radius` (ex: `0` no flat, `16px` no teal, `20px` no purple)
- `--shadow` (nenhum, soft, glow, vibrante)
- `--typography-scale` (tamanhos de heading e body)
- `--spacing-scale`
- Estilo de botão CTA (pill, flat retangular, glass, etc.)

Esses tokens viram variáveis CSS mestres na raiz (`:root`) e TODAS as seções da página os usam. prova social, entregáveis, bônus, garantia, stack, footer, tudo. Nenhuma seção pode ter cantos arredondados se o estilo é flat. Nenhuma seção pode ter borda preta 1.5px se o estilo é teal.

**Etapa 5. Copiar estrutura HTML+CSS dos templates e adaptar**
Do HTML do template lido, copiar a estrutura da seção (grid, tipografia, espaçamento, decorações, animações). NÃO reescrever do zero. Adaptar apenas:
- Cores → paleta do nicho (ver tabela "Paletas por Nicho")
- Fontes → combinação do nicho (ver tabela "Combinações Recomendadas por Nicho")
- Textos → copy aprovada pelo usuário
- Imagens → URLs contextuais (ver "Imagens Contextuais")

**Etapa 6. Consolidar em arquivo único com tokens mestres**
Unificar `<style>` de todas as seções em um único bloco com os tokens mestres da Etapa 4 no `:root`. Normalizar todas as variáveis CSS conflitantes entre templates para os tokens mestres. se um template usa `border-radius: 16px` mas o estilo escolhido é `flat_claro` (radius 0), reescrever para `border-radius: 0`. Consistência visual acima de tudo.

**Etapa 7. Consultar `references/design-system-components.md` apenas para gaps**
Animações globais, scroll reveal, fonte global, responsivo. Nunca como substituto da leitura dos templates.

**Checklist antes de salvar o HTML:**
- [ ] Li pelo menos 4 arquivos `references/templates/*/code.html` do MESMO estilo
- [ ] A página usa UM ÚNICO estilo visual do início ao fim
- [ ] Extraí tokens mestres (`--radius`, `--border-width`, `--shadow`) do estilo e apliquei em TODAS as seções
- [ ] Nenhuma seção tem cantos, bordas ou sombras que fogem do estilo escolhido
- [ ] Paleta e fontes foram adaptadas ao nicho do produto
- [ ] Cada seção tem estrutura copiada de um template real, não improvisada

### Padrões Visuais (aplicar a todas as seções)

- **CSS puro com custom properties**. preferir CSS puro. Tailwind CDN apenas se necessário
- **Material Symbols Outlined** para ícones. Nunca usar emoji como ícone em seções de valor (depoimentos, entregáveis, garantia). Emoji só é permitido dentro do `img-placeholder` contextual
- **No-Line Rule**. sem bordas 1px entre seções. Usar mudanças tonais e espaçamento
- **Glassmorphism. USO RESTRITO.** `backdrop-filter: blur()` permitido APENAS em: (1) header fixo em tema escuro high-ticket, (2) cards flutuantes em página high-ticket acima de R$1.000. PROIBIDO em low ticket, mid ticket e cards comuns de conteúdo. Em low/mid, usar fundo sólido (`var(--surface-1)`)
- **Sombras sem cor.** Box-shadow em estado repouso sempre em escala de cinza (`rgba(0,0,0,0.06)` a `rgba(0,0,0,0.12)`). Glow colorido (`box-shadow: 0 0 Xpx rgba(cor)`) PROIBIDO em estado repouso. Permitido só no hover e só em high ticket
- **Gradiente de texto em headline.** PROIBIDO em qualquer página. Destacar palavra-chave com `<em>` e `color: var(--accent)`, não com `background-clip: text`
- **Espaçamento como design**. separação por tom de fundo, não por linhas
- **Hierarquia tipográfica dramática**. heading 48-56px vs body 15-16px
- **NUNCA usar badges/tags**. Proibido usar elementos tipo pill/badge acima do headline

### Estilos Visuais Disponíveis (referência)

| Estilo | Tema | Característica | Ticket permitido |
|---|---|---|---|
| glass_escuro | Escuro | Glassmorphism sutil, bordas sólidas, sem glow colorido em repouso | **APENAS High Ticket (acima de R$1.000)**. Em low/mid, substituir por fundo sólido |
| flat_claro | Claro | Bordas flat, warm/dourado | Qualquer ticket |
| teal_claro | Claro | Teal/verde, botão pill verde | Qualquer ticket |
| dark_solido | Escuro | Fundo preto/grafite sólido, bordas finas, sem blur, sem glow | Substitui o antigo `dark_solido` (roxo+azul era clichê de IA). Qualquer ticket |
| minimal_claro | Claro | Minimalista, neutro | Qualquer ticket |

> ⛔ `glass_escuro` ficou restrito a high ticket premium. Para low e mid ticket, mesmo em nichos "premium", usar `dark_solido` ou `flat_claro`. Glassmorphism em página barata comunica "fake premium" e derruba conversão.
>
> ⛔ O antigo `dark_solido` (roxo + azul elétrico) foi descontinuado. Era a paleta padrão de Tailwind/v0/Lovable e virou assinatura de página de IA. Usar `dark_solido` no lugar.

Os templates individuais em `references/templates/` são a FONTE PRIMÁRIA de geração. Ler os arquivos `code.html` correspondentes à combinação seção × estilo é passo obrigatório (ver Etapa 3 do fluxo acima).

### Tabela de Decisão de Estilo Visual (por nicho)

A decisão de estilo é **automática com base no nicho do produto** (lido de `perfil.md`). O aluno não escolhe template. só escolhe a cor preferida. UM estilo por página, aplicado em todas as seções.

| Nicho | Estilo único da página | Por que |
|---|---|---|
| Finanças/Investimentos | glass_escuro | Sofisticação e credibilidade. Glassmorphism premium do início ao fim |
| Coaching/Dev Pessoal | glass_escuro | Autoridade e peso visual. Dark premium transmite transformação |
| Desenvolvimento Pessoal | teal_claro | Acolhedor e moderno. Clean com acentos vivos |
| Marketing Digital | flat_claro | Direto e acessível. Brutalismo clean funciona para quem decide rápido |
| Tech/Produtividade | dark_solido | Vibrante e inovador. Dark roxo comunica tecnologia |
| Saúde/Bem-estar | teal_claro | Natural e fresco. Verdes e brancos transmitem bem-estar |
| Educação/Concursos | flat_claro | Sério e confiável. Bordas definidas comunicam rigor |
| Beleza/Skincare | minimal_claro | Elegante e delicado. Espaços amplos e suavidade |
| Feminino/Lifestyle | minimal_claro | Suave e moderno. Base neutra deixa as cores do nicho protagonistas |
| Artesanato/Handmade | flat_claro | Quente e artesanal. Bordas visíveis remetem a feito à mão |
| Gastronomia | flat_claro | Aconchegante. Tons warm combinam com comida |
| Pet/Animais | teal_claro | Natural e amigável. Teal remete a cuidado |
| Imobiliário/Luxo | glass_escuro | Premium total. Dark glass comunica alto valor |
| Viagens/Turismo | teal_claro | Aspiracional e fresco. Azuis e verdes lembram destinos |
| Premium/High Ticket (qualquer nicho) | glass_escuro | Sofisticação máxima do início ao fim |
| Low Ticket (qualquer nicho) | flat_claro ou teal_claro | Acessível e direto. Estilos claros passam leveza e baixo risco |

Quando o nicho do produto não estiver na tabela, escolher o estilo mais próximo pela natureza do público (acolhedor → teal_claro, sério → flat_claro, premium → glass_escuro, inovador → dark_solido, delicado → minimal_claro).

### Regra de Consistência Visual

- **UM estilo visual por página inteira.** Nenhuma página pode combinar estilos diferentes (ex: hero glass + dor teal). Quebra a consistência e o olho percebe na hora.
- **Para dar ritmo visual sem quebrar a consistência, variar:**
  - Variante interna do mesmo estilo (ex: `hero_flat_claro`, `hero_flat_claro_centralizado`, `hero_flat_claro_depoimentos`)
  - Tom de fundo dentro da paleta do estilo (claro → branco → cinza claro → branco)
  - Direção de layout (grid 2 colunas vs grid 3 vs linha corrida)
  - Tipografia dramática (heading 48-56px alternando com body 15-16px)
  - Imagens de fundo com overlay
- **Tokens mestres obrigatórios no `:root`:** `--radius`, `--border-width`, `--shadow`, `--accent`, `--bg`, `--text-primary`, `--text-secondary`. Nenhuma seção pode reescrever esses valores.
- **Seções sem template próprio herdam os tokens.** Prova social, entregáveis, bônus, stack, garantia e "para quem é" precisam parecer nativas do estilo escolhido. mesmo raio de borda, mesma sombra, mesmo tratamento de botão.

## Paletas por Nicho

> ⛔ **Paletas proibidas (clichê de IA):** Roxo `#6b46c1` + Azul `#3182ce` (padrão Tailwind/v0/Lovable), Azul elétrico `#667eea` + gradiente 135deg (padrão Figma/Stripe template), Verde `#38a169` sólido como CTA em nicho não-saúde (verde padrão Tailwind). Essas combinações aparecem em 80% das páginas geradas por IA e o olho do usuário reconhece em 2 segundos.
>
> **Regra do CTA:** CTA sempre usa a cor **principal da paleta do nicho** ou um contraste natural dela. Proibido "verde porque converte" ou "laranja porque é padrão". Se o nicho usa Terracota, o CTA é Terracota mais saturada ou Âmbar (cor complementar real), nunca um verde genérico descolado da marca.

| Nicho | Principal | Secundária | CTA |
|---|---|---|---|
| Finanças | Azul escuro #1a365d | Dourado #c6912b | Dourado forte #b8860b |
| Saúde | Verde oliva #3f6d47 | Areia #e8e1d3 | Laranja queimado #c2410c |
| Marketing | Grafite #1c1917 | Âmbar #d97706 | Âmbar forte #b45309 |
| Dev Pessoal | Azul petróleo #1e3a4c | Creme #faf6ef | Terracota #c2410c |
| Educação | Azul marinho #1e3a5f | Mostarda #ca8a04 | Mostarda forte #a16207 |
| Beleza | Rosa antigo #b03a6b | Champanhe #e7c891 | Bordô #7c2d3e |
| Artesanato | Terracota #b45a3a | Marrom café #3d2817 | Ocre #c2861f |
| Tech | Carvão #18181b | Cobre #b85a2c | Cobre forte #9a4a24 |
| Coaching | Terracota #c4603c | Creme #fdf6ec | Âmbar queimado #a8521e |
| Feminino | Rose profundo #c73865 | Nude quente #f4e0d6 | Bordô #872e4a |

## Imagens Contextuais (OBRIGATÓRIO)

**Toda imagem na página precisa ter relação semântica direta com o conteúdo da seção onde está inserida.** Imagens que não conversam com a copy dão cara de template de IA e quebram a leitura persuasiva.

### PROIBIDO. Serviços de imagem aleatória

Os serviços abaixo **NÃO entendem palavras**. eles devolvem fotos aleatórias (Lorem Ipsum de imagem), mesmo quando você passa um "seed" com keywords descritivas. Usá-los é a causa número 1 de imagens sem sentido na página.

- ❌ `picsum.photos/...` (incluindo `picsum.photos/seed/qualquer-coisa/...`). o seed é só um hash, não faz busca semântica
- ❌ `source.unsplash.com/...`. serviço descontinuado, imagens não carregam
- ❌ `loremflickr.com`, `placeimg.com`, `placeholder.com/image` e similares
- ❌ Qualquer URL de imagem "aleatória" ou "by keyword" que você não possa verificar manualmente

### Fonte obrigatória: placeholder visual gerado a partir da copy

O padrão para 100% das imagens ilustrativas de cards, problemas, benefícios, ícones de método, etapas da jornada e capas de seção é um **placeholder visual em HTML/CSS** construído a partir do próprio texto da seção. Como ele é gerado da copy, **combina sempre**. não tem como errar.

**Anatomia do placeholder:**

1. Um `<div>` com gradiente de fundo na paleta do design system
2. Um **emoji ou ícone SVG** escolhido a partir do objeto central da copy
3. Uma **label curta** (2-4 palavras) tirada direto do título/texto do card

**Exemplo. card "Horas de trabalho por centavos" (nicho crochê):**

```html
<div class="img-placeholder" role="img" aria-label="Mãos trabalhando crochê">
  <span class="ph-icon">🧶</span>
  <span class="ph-label">Horas de trabalho</span>
</div>
```

```css
.img-placeholder{
  aspect-ratio: 16/9;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap:.5rem;
  background: linear-gradient(135deg, var(--c-brand-soft), var(--c-brand));
  color: var(--c-on-brand);
  border-radius: var(--radius-lg);
  text-align:center; padding:1.5rem;
}
.ph-icon{ font-size: clamp(2.5rem, 6vw, 4rem); line-height:1; }
.ph-label{ font-weight:700; font-size: clamp(.9rem, 2vw, 1.1rem); letter-spacing:.02em; }
```

### Biblioteca de emojis por tema

Ao montar o placeholder, escolher o emoji que representa o **objeto central da frase** (não uma vibe genérica).

| Tema / nicho | Emojis úteis |
|---|---|
| Artesanato / crochê / costura | 🧶 🪡 🧵 ✂️ 🎀 |
| Gastronomia / confeitaria | 👩‍🍳 🍰 🥖 🧁 🍳 🥘 |
| Finanças / precificação | 💰 📊 🧮 💳 📈 📉 |
| Tempo / cansaço / madrugada | ⏰ 🌙 🕯️ 😮‍💨 🛋️ |
| Frustração / estagnação | 😔 🤦 📉 🚫 ⛔ |
| Conquista / virada | 🎯 ✨ 🚀 🏆 ✅ |
| Ensino / estudo | 📚 ✏️ 🎓 📝 🧠 |
| Saúde / bem-estar | 🧘 🥗 💪 🫀 🌿 |
| Tech / digital | 💻 📱 ⚙️ 🖥️ 🔌 |
| Beleza / rotina | 💄 🪞 🧴 💅 ✨ |
| Família / relacionamento | 👨‍👩‍👧 💬 🤝 ❤️ |
| Vendas / cliente | 🛍️ 🏷️ 💬 📦 🚚 |

**Regra:** o emoji tem que vir do substantivo mais concreto da frase. Se a copy fala "crochê de madrugada", o emoji é 🌙 ou 🕯️, não 😔. Se fala "peças guardadas sem vender", é 📦, não 😢.

### Quando usar foto real em vez de placeholder

Só usar foto real do Unsplash se:

1. O aluno enviou o ID específico de uma foto que ele quer usar, **ou**
2. A foto vai num lugar onde o placeholder não funciona bem (hero de fundo inteiro, foto de depoimento, foto do produto físico), **e**
3. Você consegue referenciar um ID exato do Unsplash:

```
https://images.unsplash.com/photo-{ID}?w=1200&q=80&fit=crop
```

Se não souber um ID específico que comprovadamente combina com a copy, **use placeholder**. não invente ID, não chute, não use picsum como fallback.

### Fotos de depoimento e avatar

Para rostos de depoimentos:

- **Opção padrão:** `https://i.pravatar.cc/150?img={1-70}` (banco de avatares genéricos, seed numérico estável)
- **Alternativa sem rosto:** div circular com iniciais da pessoa e gradiente da marca

Nunca usar picsum para rosto. volta bicicleta, praia, comida aleatória.

### Exemplo completo. Seção Problema/Dor (nicho crochê)

```html
<div class="problema-card">
  <div class="img-placeholder" role="img" aria-label="Horas de trabalho mal pagas">
    <span class="ph-icon">🧶</span>
    <span class="ph-label">Horas de trabalho</span>
  </div>
  <h3>Horas de trabalho por centavos</h3>
  <p>Você passa a tarde inteira fazendo uma peça e vende por menos do que gastou em linha.</p>
</div>

<div class="problema-card">
  <div class="img-placeholder" role="img" aria-label="Cliente que some depois de pedir preço">
    <span class="ph-icon">💬</span>
    <span class="ph-label">A pechincha que dói</span>
  </div>
  <h3>A pechincha que dói</h3>
  <p>A cliente olha, elogia, pergunta o preço e some.</p>
</div>

<div class="problema-card">
  <div class="img-placeholder" role="img" aria-label="Peças acumuladas sem vender">
    <span class="ph-icon">📦</span>
    <span class="ph-label">Peças guardadas</span>
  </div>
  <h3>Peças guardadas no armário</h3>
  <p>Peças lindas acumulando poeira na prateleira.</p>
</div>

<div class="problema-card">
  <div class="img-placeholder" role="img" aria-label="Crochê feito de madrugada">
    <span class="ph-icon">🌙</span>
    <span class="ph-label">Crochê de madrugada</span>
  </div>
  <h3>Crochê de madrugada</h3>
  <p>Trabalhando enquanto a família dorme.</p>
</div>
```

### Checklist antes de salvar a página

Rodar essa varredura no HTML gerado. se falhar em qualquer item, corrigir antes de salvar:

- [ ] Nenhuma ocorrência de `picsum.photos` no arquivo
- [ ] Nenhuma ocorrência de `source.unsplash.com`
- [ ] Todo `img-placeholder` tem emoji **E** label vinda da copy da mesma seção
- [ ] Se há `<img>` de Unsplash, é um ID específico (não genérico) e combina com o texto do card
- [ ] Fotos de depoimento usam `pravatar.cc` ou iniciais, nunca picsum

### ⛔ Checklist Anti-Cara-de-IA (OBRIGATÓRIO antes de salvar)

**LER E APLICAR** `references/anti-ia-design.md` antes de salvar qualquer HTML. O arquivo tem os 20 clichês visuais proibidos, o checklist rápido de 10 perguntas e a tabela de substituições prontas. Esse passo não é opcional, e não é substituído pelo checklist acima (que só cobre imagens).

Pontos mínimos que a página TEM que passar:

- [ ] Paleta NÃO tem roxo `#6b46c1` + azul `#3182ce` (padrão Tailwind/v0)
- [ ] Nenhum `background: linear-gradient(135deg, roxo, azul)` em fundo grande
- [ ] CTA usa cor primária do nicho, NÃO verde `#38a169` genérico
- [ ] `backdrop-filter: blur` só em header dark OU em high-ticket premium
- [ ] Nenhum `box-shadow: 0 0 Npx rgba(cor)` em estado repouso (glow proibido)
- [ ] Headline NÃO usa `background-clip: text` com gradiente
- [ ] Inter/Poppins NÃO usadas em coaching, beleza, artesanato (usar DM Sans, Manrope, Figtree ou Plus Jakarta Sans)
- [ ] Cards têm hierarquia de `border-radius`, não tudo com `16px`
- [ ] Hero NÃO é centralizado com gradiente atrás (usar assimetria ou fundo sólido)
- [ ] Nenhuma foto de "pessoa sorrindo com laptop" ou emoji como ícone em seção de valor

Se qualquer item falhar, voltar, corrigir e rodar o checklist de novo. Não salvar antes de passar em todos.

## Referências

- **`references/etapa-ajustes-pagina.md`**. **OBRIGATÓRIO após merge.** Checklist da etapa de ajustes: checkout, SEO básico, placeholders, duplicata de provas, rodapé. Diferente de feedback profundo (`/feedback-pagina`) e de performance (`/pagina-performance`).
- **`references/anti-ia-design.md`**. **OBRIGATÓRIO.** 20 clichês visuais proibidos, checklist rápido de 10 perguntas, tabela de substituições. Ler antes de salvar qualquer HTML.
- **`references/design-system-components.md`**. **ARQUIVO PRINCIPAL**. CSS variables, componentes, animações, responsivo. Ler este arquivo substitui a leitura de todos os templates individuais.
- `references/estruturas-pagina.md`. Seções por tipo de página, fundos por seção, paletas por nicho
- `references/cdn-design-resources.md`. CDNs, fontes, ícones, animações, gradientes
- `references/performance-otimizacao.md`. Auditoria e otimização (meta: 90+ mobile / 100 desktop)
- `references/design-referencia-vtsd.md`. **REFERÊNCIA DE DESIGN VTSD.** Análise visual das páginas reais VTSD, Light Copy e Stories 10x: 3 estilos visuais (Light, Dark Premium, Dark Vibrante), paletas reais, padrões de seção, botões CTA, tabelas comparativas, seções recorrentes e lógica de alternância de fundos. Consultar SEMPRE ao gerar páginas para garantir nível de qualidade VTSD.
- `references/templates/`. Templates HTML individuais por seção/estilo (referência visual, NÃO ler durante geração)

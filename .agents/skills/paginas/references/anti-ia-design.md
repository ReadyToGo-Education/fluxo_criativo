# Anti-IA Design. Checklist do que NÃO fazer

Este arquivo lista os clichês visuais que deixam páginas com "cara de IA" (v0, Lovable, Bolt, Framer AI, Figma templates free). Aplicar como filtro obrigatório antes de salvar qualquer HTML.

**Quando consultar:**
- Antes de salvar uma página nova (checklist final de geração)
- Dentro de `/feedback-pagina` e `/feedback-low-ticket` como seção de design
- Sempre que a resposta do aluno for "ficou bonita mas parece gerada por IA"

**Por que existe:** páginas geradas por IA caíram todas no mesmo "estilo bonito default" (glassmorphism + roxo-azul + gradiente em título + verde no CTA + pessoa sorrindo com laptop). Conversão despenca quando o visitante reconhece esse padrão, porque associa a "vendedor amador usando template". Este arquivo vacina contra isso.

---

## Os 20 clichês visuais proibidos

### Paleta e cor

1. **Roxo `#6b46c1` + Azul `#3182ce` como paleta principal.** Padrão Tailwind/v0. Sempre que ver esses dois juntos, trocar. Em marketing, usar Grafite + Âmbar. Em tech, usar Carvão + Cobre.
2. **Azul elétrico `#667eea` em gradiente 135deg.** Padrão Stripe template / Figma default. Proibido como fundo de hero ou CTA.
3. **Verde `#38a169` (Tailwind default) como CTA em nicho não-saúde.** CTA precisa ser a cor primária da marca, não um verde descolado do resto da página. Se nicho usa Terracota, CTA é Terracota mais saturada.
4. **Gradiente 135deg em fundo de seção.** Especialmente `linear-gradient(135deg, roxo, azul)`. É o fundo padrão de página de AI app. Usar fundo sólido, ou gradiente radial sutil, ou duas camadas de cor com textura.
5. **Fundo `#fafafa` em todas as seções claras.** O bege/cinza claro padrão de template. Alternar com branco puro, cinza mais frio, ou cor de marca lavada.

### Efeitos e sombras

6. **Glassmorphism em card comum.** `backdrop-filter: blur()` em card de depoimento, benefício ou ferramenta é clichê de 2021-22. Permitido APENAS em header fixo dark ou cards flutuantes de high-ticket premium.
7. **Glow colorido em box-shadow de estado repouso.** `box-shadow: 0 0 30px rgba(cor)`. Dá cara de "design de 2023". Sombras em repouso devem ser em escala de cinza (`rgba(0,0,0,0.08)`). Glow permitido só no `:hover` e só em high-ticket.
8. **Neumorphism.** `box-shadow: inset ... , outset ...` com branco e cinza claro. Trend morto desde 2022.
9. **Shimmer decorativo em topo de card.** Linha luminosa animada em `::before`. Virou assinatura de "template premium fake". Permitido apenas em skeleton loader (carregamento real).
10. **Border animada com gradiente rotativo.** Aquele card com borda que gira com cores. Clichê de landing de cripto/web3.

### Tipografia

11. **Gradiente de texto em headline** (`background: linear-gradient(...); -webkit-background-clip: text`). PROIBIDO. Hierarquia vem do peso/tamanho, não de efeito. Se precisar destacar, colorir UMA palavra com `color: var(--accent)`.
12. **Inter como fonte universal.** Inter é a fonte default de v0/Lovable/Bolt. Usar APENAS em tech/finanças com dados. Em coaching/beleza/artesanato, usar DM Sans, Manrope, Figtree ou Plus Jakarta Sans.
13. **Poppins em tudo.** Segunda fonte mais genérica de IA. Permitida só em saúde/educação popular. Em premium, trocar por Figtree ou Plus Jakarta Sans.
14. **Tamanho único de heading.** Todas as section-headline com `font-size: 32px`. Falta hierarquia. Hero `clamp(2.5rem, 5vw, 3.5rem)`, section `clamp(2rem, 4vw, 3rem)`, card title `1.125rem`.

### Layout

15. **Hero sempre centralizado com gradiente de fundo.** Headline + subheadline + vídeo + botão, tudo no centro, com gradient atrás. 95% das landings de IA. Alternar com: hero assimétrico (texto à esquerda, imagem à direita), hero com fundo sólido de cor de marca, hero com linha vertical decorativa.
16. **Grid de cards todos iguais em fundo bege.** 3 cards brancos, mesma altura, mesma sombra, em `#faf6ef`. Assinatura de Lovable/v0. Variar altura por conteúdo real, alternar tom de fundo entre cards (um com cor de marca leve).
17. **Tudo com `border-radius: 16px`.** Raio único em todos os elementos. Usar hierarquia: botões 10-12px, cards 12-16px, inputs 8px, ícones 8px. Nunca 20px+ em componente pequeno.
18. **Cards de depoimento idênticos em carrossel com dot expansível.** `.dot.active { width: 20px }` é marca registrada de Framer/v0. Usar dot simples (8px, sem expansão) OU numeração `1 / 5`.

### Imagem e ícone

19. **Pessoa sorrindo com laptop ou "workspace aesthetic".** Fotos genéricas de stock de "mulher empreendedora feliz", "mãos no teclado com café", "pessoa apontando para gráfico". Usar detalhes em close-up do que o produto ENTREGA (ex: página de método = detalhe de caderno aberto com nota; página de confeitaria = detalhe de mão confeitando, não a confeiteira sorrindo).
20. **Emoji como ícone em seção de valor.** 🎯 ao lado de benefício, ✅ em lista de entregáveis. Usar Material Symbols Outlined (`<span class="material-symbols-outlined">target</span>`). Emoji é permitido APENAS dentro do `img-placeholder` contextual, nunca como substituto de ícone sério.

---

## Checklist rápido antes de salvar (cole no final do processo)

Rodar essas 10 perguntas e corrigir qualquer "sim" antes de salvar:

- [ ] A paleta tem roxo `#6b46c1` + azul `#3182ce`? (Padrão Tailwind/v0)
- [ ] Algum `background: linear-gradient(135deg, ...)` em fundo grande?
- [ ] CTA é verde genérico (`#38a169`) e o produto não é de saúde?
- [ ] Algum `backdrop-filter: blur` fora do header dark? (Glassmorphism em card)
- [ ] Algum `box-shadow: 0 0 Npx rgba(cor)` em estado repouso? (Glow colorido)
- [ ] Headline usa `background-clip: text` com gradiente?
- [ ] Inter ou Poppins em nicho emocional (coaching, beleza, artesanato)?
- [ ] Todos os cards têm o mesmo `border-radius: 16px` sem hierarquia?
- [ ] Hero centralizado com vídeo/botão no meio e gradiente atrás?
- [ ] Algum `<img>` genérico de "pessoa sorrindo com laptop" ou emoji como ícone?

Se **qualquer** resposta for "sim", voltar e corrigir. Não salvar página com clichê de IA.

---

## Alternativas prontas para cada clichê

| Clichê | Substituto |
|---|---|
| Roxo+azul Tailwind | Grafite `#1c1917` + Âmbar `#d97706` |
| Gradiente 135deg roxo→azul | Fundo sólido + gradiente radial sutil em 1 canto |
| CTA verde `#38a169` genérico | Cor primária do nicho mais saturada |
| Glass card `backdrop-filter: blur` | `background: var(--surface-1); border: 1px solid var(--border)` |
| Glow `box-shadow: 0 0 30px rgba(cor)` | `box-shadow: 0 4px 12px rgba(0,0,0,0.08)` |
| Headline `background-clip: text` | `<h1>palavra normal <em>destaque</em> continua</h1>` |
| Inter em coaching/beleza | DM Sans, Manrope, Figtree, Plus Jakarta Sans |
| Poppins em high-ticket | Figtree, Plus Jakarta Sans, Urbanist |
| `border-radius: 16px` em tudo | Hierarquia: 8px inputs, 10-12px botões, 12-16px cards |
| Hero centralizado com gradiente | Hero assimétrico (texto esquerda, imagem direita) |
| Grid de cards iguais em bege | Variar altura + alternar fundo (um com cor de marca) |
| Dot carrossel expansível | Dot simples 8px OU numeração `1/5` |
| Pessoa sorrindo com laptop | Close-up do detalhe do produto/método |
| Emoji como ícone | Material Symbols Outlined |

---

## Diagnóstico por tipo de "cara de IA"

Se o feedback for "parece feito por IA", identificar qual dos 5 padrões está ativo:

1. **"Parece Lovable / v0."** → Clichês 1, 2, 15, 16, 17 (paleta Tailwind, gradiente 135deg, hero centralizado, grid bege, raio único)
2. **"Parece template Figma free."** → Clichês 11, 12, 13 (gradiente em título, Inter/Poppins)
3. **"Parece landing de 2022."** → Clichês 6, 7, 9 (glassmorphism, glow, shimmer)
4. **"Parece template de curso barato."** → Clichês 19, 20 (pessoa sorrindo com laptop, emoji como ícone)
5. **"Parece página de AI app."** → Clichês 2, 3, 4, 18 (azul elétrico, verde CTA, gradiente de fundo, dot expansível)

Para cada um, aplicar as substituições correspondentes na tabela acima.

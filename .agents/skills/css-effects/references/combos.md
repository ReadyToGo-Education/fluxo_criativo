# Combos Prontos por Tipo de Site

Cada combo é uma receita testada — onde aplicar cada efeito pra criar uma experiência coerente. Use como **ponto de partida**, não regra. Adapte ao tom específico do projeto.

---

## SaaS / Produto Tech (Linear, Vercel, Stripe)

**Tom:** Profissional, moderno, denso de informação, premium.

**Setup completo:**

| Seção | Efeito | Arquivo |
|---|---|---|
| **Navbar** | navbar-blur + nav-link-underline | navigation.md |
| **Hero - título** | text-gradient-anim | text.md |
| **Hero - background** | mesh-gradient ou animated-grid | backgrounds.md |
| **Hero - CTA** | btn-gradient-slide ou btn-glow-pulse | buttons.md |
| **Features grid** | card-tilt + card-spotlight (combinados) | cards.md |
| **Stats numéricos** | counter-animation | scroll.md |
| **Manifesto / quote** | word-reveal | scroll.md |
| **Sticky de etapas** | sticky-scroll | scroll.md |
| **Cards de plano** | card-border-anim no plano destacado | cards.md |
| **Footer links** | nav-link-underline | navigation.md |
| **Global** | scroll-progress + fade-up em todas as seções | scroll.md |

**O que NÃO usar aqui:** glitch, fire, neon, scramble, cursor exótico. Mantenha sóbrio.

**Referência visual:** linear.app, vercel.com, stripe.com

---

## Portfolio Criativo

**Tom:** Personalidade forte, experimental, memorável.

**Setup completo:**

| Seção | Efeito | Arquivo |
|---|---|---|
| **Cursor** | cursor-dot-follower OU cursor-blend-mode | cursor.md |
| **Hero - título** | text-scramble OU text-3d-stack | text.md |
| **Hero - background** | gradient-orbs OU stars-field | backgrounds.md |
| **Bio / sobre** | word-reveal no scroll | scroll.md |
| **Galeria de projetos** | horizontal-scroll | scroll.md |
| **Cards de projeto** | card-tilt + img-color-reveal | cards.md, images.md |
| **Detalhes de projeto** | img-comparison-slider | images.md |
| **Lista de skills** | text-rotate-words | text.md |
| **CTA contato** | btn-magnetic | buttons.md |
| **Transições de página** | page-transition | loaders.md |

**O que NÃO usar aqui:** múltiplos cursores, mais de 1 efeito chamativo no hero.

**Referência visual:** sites premiados em awwwards.com

---

## Landing de Evento / Produto Único

**Tom:** Urgência, emoção, alto impacto, conversão.

**Setup completo:**

| Seção | Efeito | Arquivo |
|---|---|---|
| **Hero - título** | text-fire OU text-neon | text.md |
| **Hero - background** | aurora-gradient + matrix-rain leve | backgrounds.md |
| **Contagem regressiva** | counter-animation customizada com decremento | scroll.md |
| **CTA principal** | btn-glow-pulse + btn-ripple | buttons.md |
| **Lineup / atrações** | card-flip-3d (frente: foto, verso: bio) | cards.md |
| **Localização** | parallax | scroll.md |
| **Confirmação inscrição** | confetti-burst + toast-notification | microinteractions.md, modals.md |
| **Form de inscrição** | input-glow-focus + btn-loading-state | forms.md, buttons.md |

**Cuidado:** evite mais de 2 elementos pulsando ao mesmo tempo. CTA pulsa, resto fica sóbrio.

---

## Blog / Conteúdo Editorial

**Tom:** Legível, sofisticado, foco no texto, ritmo de leitura.

**Setup completo:**

| Seção | Efeito | Arquivo |
|---|---|---|
| **Top da página** | scroll-progress-bar | scroll.md |
| **Título do post** | text-highlight em palavras-chave | text.md |
| **Imagem hero** | img-blur-load + img-ken-burns sutil | images.md |
| **Imagens inline** | img-reveal-on-scroll | images.md |
| **Citações destacadas** | word-reveal | scroll.md |
| **Sidebar de artigos** | card-lift simples | cards.md |
| **Botão compartilhar** | btn-fill-up | buttons.md |
| **Comentários — like** | heart-like | microinteractions.md |
| **Tempo de leitura** | counter-animation no scroll | scroll.md |
| **Voltar ao topo** | scroll-to-top | microinteractions.md |

**Importante:** evitar tudo que distrai da leitura. Sem cursor custom, sem matrix rain, sem pulse contínuo.

---

## E-commerce

**Tom:** Confiança, desejo, ação rápida, foco em conversão.

**Setup completo:**

| Seção | Efeito | Arquivo |
|---|---|---|
| **Cards de produto** | card-lift + card-shine + img-hover-zoom | cards.md, images.md |
| **Galeria de produto (PDP)** | img-comparison-slider para variações | images.md |
| **Botão "Comprar"** | btn-glow-pulse + btn-ripple | buttons.md |
| **Avaliações** | counter-animation no número de reviews | scroll.md |
| **Estrelas** | star-rating (read-only) | microinteractions.md |
| **Carrinho** | drawer-side | modals.md |
| **Adicionar ao carrinho** | success-flash + toast-notification | microinteractions.md, modals.md |
| **Stock baixo / urgência** | badge-pulse | microinteractions.md |
| **Filtros** | checkbox-check + toggle-switch | forms.md |
| **Busca** | search-expand | forms.md |
| **Cupom copiar** | copy-feedback | microinteractions.md |
| **Checkout (form)** | input-floating-label + input-validation-flash | forms.md |
| **Compra confirmada** | confetti-burst | microinteractions.md |

**Atenção:** No checkout (forms), corte TODOS os efeitos chamativos. Só feedback funcional.

---

## Dashboard / SaaS Interno

**Tom:** Funcional, denso, eficiente, sem distrações.

**Setup completo:**

| Seção | Efeito | Arquivo |
|---|---|---|
| **Sidebar** | sidebar-slide + nav-link-fill | navigation.md |
| **Métricas principais** | counter-animation + progress-ring | scroll.md, loaders.md |
| **Gráficos carregando** | skeleton-loader | loaders.md |
| **Cards de KPI** | card-lift sutil (sem tilt) | cards.md |
| **Background da área** | dot-pattern OU grid-pattern leve | backgrounds.md |
| **Notificações** | toast-notification + badge-pulse no sino | modals.md, microinteractions.md |
| **Loading de dados** | spinner-classic ou bars | loaders.md |
| **Botões de ação** | btn-loading-state | buttons.md |
| **Tooltip de ajuda** | tooltip-fade | modals.md |
| **Confirmar deletar** | modal-fade-scale + alert-shake-fade | modals.md |
| **Salvar settings** | success-flash | microinteractions.md |
| **Drag de cards (Kanban)** | drag-feedback | microinteractions.md |

**Princípio do dashboard:** efeito = feedback funcional. Nada decorativo. Usuário trabalha aqui.

---

## Site Único / Link Bio

**Tom:** Compacto, personalidade, fácil de absorver em 5 segundos.

**Setup completo:**

| Seção | Efeito | Arquivo |
|---|---|---|
| **Card central** | card-tilt + card-spotlight | cards.md |
| **Background** | gradient-orbs OU aurora-gradient | backgrounds.md |
| **Avatar** | img-hover-zoom dentro de círculo | images.md |
| **Nome / título** | text-gradient-anim | text.md |
| **Bio curta** | fade-up | scroll.md |
| **Botões de link** | btn-fill-up + btn-magnetic no principal | buttons.md |
| **Ícones sociais** | btn-magnetic em cada um | buttons.md |

**Mantenha curto.** É um cartão digital, não uma landing.

---

## Como adaptar os combos

1. **Cores** — todos os exemplos usam magenta (#ff00cc) + ciano (#00f0ff). Substitua pelas cores da marca do usuário ANTES de entregar.
2. **Tom** — se o cliente é mais sóbrio que o combo sugere, remova os efeitos contínuos (glow-pulse, animated, particles) e mantenha só os de hover/scroll.
3. **Mobile** — todo combo precisa ter versão mobile testada. Ver `principles.md`.
4. **Performance** — se o site tem >50 cards, NÃO aplique tilt em todos. Pode aplicar em hover só ou em destaques.

## Anti-padrão: combos a evitar

- **"Stack overflow visual"** — cursor custom + glitch text + matrix rain + particles + neon button TUDO JUNTO. Causa náusea e parece amador.
- **"Cassino"** — múltiplos elementos com glow-pulse, gradient-anim, scan-line ao mesmo tempo. Compete pela atenção, ninguém vence.
- **"Inconsistente"** — hero ultra-criativo + body sem nenhum efeito. Quebra de tom. Ou tudo tem mood, ou nada tem.

## Princípio mestre

Um combo bem feito **passa despercebido individualmente** mas faz o site **inteiro parecer caro**. Se você consegue listar todos os efeitos só olhando, está exagerado.

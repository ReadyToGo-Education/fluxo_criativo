# Estruturas de Página por Tipo

Referência de estrutura, seções e regras para cada tipo de página.
**Atenção:** Este arquivo complementa a skill `/copy-pagina`. As Regras Críticas de Qualidade (#1 a #6) da skill têm precedência.

---

## Regras Universais (aplicam a TODAS as páginas)

### Idioma
- Todo texto visível DEVE estar em português do Brasil com acentos corretos
- "Módulos", "Precificação", "Vídeo", "Método", "Você", "Não", "É", "Já", "Também", "Negócio"
- Revisar TUDO antes de salvar: headlines, parágrafos, botões, labels, FAQs, footer

### Header Obrigatório
Toda página começa com header contendo logotipo:
- Logo texto estilizado (fonte heading) quando não houver imagem
- Placeholder instrucional: `[Insira seu logotipo aqui. 180x50px]`
- Fundo transparente ou cor sólida que combine com o hero
- Logo à esquerda + CTA pequeno à direita (opcional)
- No mobile, centralizar o logo

### Fontes
- **Body: SEMPRE sans-serif** (DM Sans, Nunito, Source Sans 3, Outfit, Manrope)
- **Heading: serif OU sans-serif** dependendo do nicho (ver tabela de fontes na skill)
- **NUNCA** usar fonte serifada (Lora, Source Serif, Merriweather) como body text

### Grids e Cards
- Cards com texto: `min-width: 320px` (NUNCA menor que 300px)
- Cards com lista de itens: `minmax(340px, 1fr)`
- Texto em cards: `font-size >= 0.95rem` e `padding >= 28px`
- Entregáveis/Módulos: **2 colunas** no desktop, 1 no mobile (NÃO 3 colunas)

### Variedade Visual entre Seções
- Alternar pelo menos **4 tipos** de fundo (claro, escuro, imagem+overlay, gradiente, textura, cor vibrante)
- Pelo menos **2 seções** com imagem de fundo (Picsum+overlay ou CSS artístico)
- Pelo menos **1 divisor decorativo** (SVG wave, linha com ícone, mudança abrupta de cor)
- PROIBIDO repetir o mesmo padrão visual em seções consecutivas

### Anti-IA (não parecer Lovable/v0/genérico)
- NÃO: cards brancos idênticos em fundo bege, ícones em quadrados pastel, tudo flat
- SIM: contraste forte entre seções, imagens de fundo, texturas, hovers que surpreendem

---

## Página de Vendas (Sales Page. Estrutura 8D Expandida)

### Objetivo
Convencer e converter o visitante em comprador.

### Seções (ordem recomendada. 16 seções)

| # | Seção | Fundo sugerido | Detalhes |
|---|---|---|---|
| 1 | **Header** | Transparente sobre hero | Logo + CTA pequeno opcional |
| 2 | **Hero** | Escuro com gradiente | Headline + subheadline + 3 bullets + CTA + vídeo |
| 3 | **Problema/Dor** | Claro + cards com borda | Dor amplificada com cenas do cotidiano |
| 4 | **Paliativo** | **Imagem + overlay escuro** | Ferramentas e soluções concorrentes do mercado, e por que cada uma não entrega o resultado completo |
| 5 | **Depoimentos (1º bloco)** | Claro com cards flutuantes | 2-3 depoimentos curtos de resultado rápido. Ancora credibilidade ANTES do método. |
| 6 | **CTA intermediário** | Cor vibrante (CTA color) | Seção curta + botão |
| 7 | **Solução/Método** | Claro com textura sutil | Furadeira com macroetapas visuais. Nome do produto aparece aqui pela 1ª vez. |
| 8 | **Para quem é / não é** | Escuro sólido | Listas com ícones check/X |
| 9 | **Entregáveis** | Claro + cards grandes | Grid **2 colunas** com listas |
| 10 | **Bônus** | Gradiente sutil | Cards com valor individual em R$ |
| 11 | **Stack de Valor** | Escuro premium | Ancoragem: valor total vs preço real |
| 12 | **Depoimentos (2º bloco)** | **Imagem + overlay** | 3-5 depoimentos completos com foto, antes/depois e resultado específico |
| 13 | **Garantia** | Claro com destaque central | Selo visual + texto confiante |
| 14 | **FAQ** | Neutro alternado | Accordion funcional (5-8 perguntas) |
| 15 | **CTA Final** | Escuro com gradiente | Preço, parcelamento, botão grande, urgência |
| 16 | **Rodapé** | Escuro sólido | Copyright, termos, privacidade |

### Regras de Conversão
- Múltiplos CTAs ao longo da página (mínimo 3)
- CTA flutuante no mobile (aparece ao rolar)
- Depoimentos com nome, avatar (pravatar.cc) e resultado específico
- Preço com ancoragem (valor original riscado + preço real)
- Botão CTA com contraste máximo contra o fundo
- Selo de garantia visual destacado
- FAQ baseado nas objeções reais da persona

### Imagens de Fundo Recomendadas (por seção)
- **Paliativo:** Imagem emocional do cotidiano do público (ex: mãos trabalhando, ateliê)
- **Depoimentos:** Foto que transmite autenticidade (ex: pessoas reais, ambiente do nicho)
- **CTA Final:** Imagem de impacto com overlay escuro forte

Implementação (ver `SKILL.md` → Imagens Contextuais. picsum é proibido porque devolve foto aleatória):
```css
.section-com-imagem {
  background:
    linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
    url('https://images.unsplash.com/photo-ID-ESPECIFICO?w=1920&q=80');
  background-size: cover;
  background-position: center;
  background-attachment: fixed; /* parallax */
  color: #fff;
}

/* Sem foto: gradiente artístico. padrão seguro quando não há ID validado */
.section-atmosferica {
  background-color: #0a0a0a;
  background-image:
    radial-gradient(at 20% 50%, hsla(28,100%,74%,0.15) 0px, transparent 50%),
    radial-gradient(at 80% 20%, hsla(189,100%,56%,0.08) 0px, transparent 50%);
  color: #fff;
}
```

### Temas de Imagem por Nicho
- Finanças: escritório, gráficos, paisagem urbana
- Saúde: natureza, alimentos, exercício
- Educação: livros, sala de aula, formatura
- Artesanato: mãos trabalhando, tecidos, ateliê, linhas coloridas
- Marketing: laptop, café, workspace criativo
- Feminino: flores, lifestyle, moda

---

## Página de Captura (Squeeze Page)

### Objetivo
Coletar o contato (email ou WhatsApp) em troca de um material gratuito.

### Seções Essenciais
1. **Header**. Logo centralizado
2. **Hero**. Headline com promessa clara + formulário simples (nome + email)
3. **Benefícios**. 3-4 pontos do que vai aprender/receber (ícones + texto)
4. **Conteúdo**. Detalhamento do material (tópicos, páginas, etc.)
5. **Autoridade**. Mini bio do autor com foto
6. **CTA Final**. Repetição do formulário com urgência

### Regras
- Máximo 1 página de scroll no mobile
- Formulário visível sem rolar (above the fold)
- Sem menu de navegação (foco total na conversão)
- Máximo 2 cores + branco/preto
- Botão grande e contrastante
- Pode ter 1 seção com fundo diferente (imagem ou cor vibrante)

### Taxa de conversão esperada: 25-45%

---

## Página de Webinar/Aula (Registration Page)

### Objetivo
Captar inscrições para evento online (ao vivo ou gravado).

### Seções Essenciais
1. **Header**. Logo + data do evento
2. **Hero**. Tema da aula + data/hora + formulário de inscrição
3. **O que vai aprender**. 3-5 pontos específicos
4. **Para quem é**. Perfil ideal do participante
5. **Sobre o professor**. Bio com credenciais
6. **CTA final**. Reforço da inscrição

### Regras
- Data e hora em destaque visual (badge ou countdown)
- Formulário simples (nome + email + WhatsApp)
- Destaque que é GRATUITO (se for)
- Senso de exclusividade ("Vagas limitadas")

### Taxa de conversão esperada: 30-50%

---

## Página de Obrigado (Thank You Page)

### Objetivo
Confirmar a ação e direcionar para o próximo passo.

### Seções Essenciais
1. **Header**. Logo
2. **Confirmação**. Mensagem clara do que aconteceu (compra, cadastro, inscrição)
3. **Próximos passos**. Instruções objetivas e numeradas
4. **CTA secundário**. Grupo WhatsApp, redes sociais, outro produto

### Regras
- Não deixar a pessoa "perdida". sempre ter próximo passo claro
- Pode incluir vídeo de boas-vindas
- Pode incluir upsell ou order bump

---

## Paletas de Cores por Nicho

| Nicho | Cor Principal | Cor Secundária | Cor CTA |
|---|---|---|---|
| Finanças/Investimentos | Azul marinho (#1e3a5f) | Dourado (#d4a574) | Verde (#38a169) |
| Saúde/Emagrecimento | Verde (#11998e) | Branco | Laranja (#dd6b20) |
| Marketing Digital | Roxo (#6b46c1) | Azul (#3182ce) | Amarelo (#ecc94b) |
| Desenvolvimento Pessoal | Azul (#2b6cb0) | Branco | Laranja (#ed8936) |
| Relacionamento | Vermelho (#c53030) | Rosa (#d53f8c) | Dourado (#d69e2e) |
| Educação/Concursos | Azul (#2c5282) | Verde (#2f855a) | Laranja (#dd6b20) |
| Beleza/Estética | Rosa (#d53f8c) | Dourado (#d69e2e) | Preto (#1a202c) |
| Tecnologia | Azul (#2b6cb0) | Cinza (#4a5568) | Verde (#38a169) |
| Artesanato/Handmade | Dourado (#d4a574) | Marrom (#2d1810) | Verde (#38a169) |
| Coaching | Terracota (#c4603c) | Creme (#fdf6ec) | Laranja (#ed8936) |
| Feminino/Lifestyle | Rose (#f5576c) | Nude (#fdf6ec) | Dourado (#d69e2e) |

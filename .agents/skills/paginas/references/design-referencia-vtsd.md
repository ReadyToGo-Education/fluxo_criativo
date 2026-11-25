# Design de Referência. Páginas VTSD

Análise visual das páginas reais dos produtos do Leandro Ladeira (VTSD, Light Copy e Stories 10x).
Use esses padrões como referência direta ao gerar páginas profissionais.

---

## 3 Estilos Visuais do Ecossistema VTSD

### Estilo 1. Light (Claro e Profissional)
**Referência:** Página de vendas do VTSD / Aula gratuita

**Paleta:**
- Fundo principal: branco `#ffffff`
- Seções de contraste: cinza clarissimo `#f7f8fa` ou fundo escuro `#1a1a2e`
- Cor de destaque na headline: verde/azul vibrante (ex: `#38a169` ou `#3182ce`)
- Botão CTA: verde `#2f855a` com arrow icon (`→`)
- Ícones de feature: coloridos por função (verde, azul, laranja, roxo)

**Tipografia:**
- Heading: Poppins ou Plus Jakarta Sans, peso 700. 800
- Body: DM Sans ou Inter, peso 400. 500
- Destaques na headline: `<span>` com cor de accent, itálico opcional

**Padrões estruturais:**
- Hero com vídeo à esquerda + bullets de aprendizado à direita (grid 2 colunas)
- Label acima do headline: "Aula gratuita" em tag pequena, uppercase, letra-espaçada
- Features em grid 4 colunas com ícone + título bold + descrição curta
- Seção escura de produto com mockup de interface (dashboard/app) no centro
- Gráfico de crescimento em 6 fases com cards abaixo (Fase 01 a Fase 06)
- Tabela comparativa "Com VTSD vs Sem VTSD": checks verdes vs X vermelhos
- Clippings de notícias (Valor, FGV, Forbes): logos + headline da matéria
- Grid de nichos (médicos, confeiteiros, etc) como tagcloud horizontal
- Seção "Quem é [Autor]" com foto grande à direita e bio à esquerda
- Grid de mídia 3x3 com fotos de eventos, programas de TV, podcasts
- Rodapé com verificação de WhatsApp

**Botão CTA padrão:**
```css
.btn-cta {
  background: #2f855a;
  color: white;
  padding: 16px 32px;
  border-radius: 50px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 1.05rem;
}
/* Ícone de seta no final do botão */
```

---

### Estilo 2. Dark Premium (Escuro e Sofisticado)
**Referência:** Página de vendas do Light Copy

**Paleta:**
- Fundo principal: preto quase absoluto `#0a0a0a` ou `#111111`
- Seções alternadas: `#161616` ou `#1a1a1a`
- Cor de destaque principal: dourado/amarelo `#f6c90e` ou `#fbbf24`
- Texto principal: branco `#ffffff`
- Texto secundário: cinza claro `#a0aec0`
- Botão CTA: amarelo/dourado com texto preto

**Tipografia:**
- Heading: Montserrat ou Space Grotesk, peso 700. 800
- Body: DM Sans ou Manrope
- Destaques: cor dourada em `<span>` dentro dos títulos

**Padrões estruturais:**
- Hero com vídeo centralizado abaixo do headline
- Tagline de aula gratuita acima do headline (pequena, amarela)
- Headline em 3 linhas, a última linha ou palavra em dourado
- Bullets "O que você vai aprender" com ícone de ponto dourado
- Features em grid 4 colunas com ícone amarelo + título + descrição breve
- Grid "funciona para" em 2-3 colunas com número e título em destaque dourado
- Clippings de autoridade (Forbes, Negócios) em cards brancos sobre fundo escuro
- Depoimentos em cards: resultado em destaque (ex: "R$9 mil em 1 e-mail") + texto
- **Tabela comparativa** em bloco único: coluna esquerda (Copy Tradicional) cinza com X vermelhos / coluna direita (Light Copy) amarela com checks verdes
- Grid de módulos: thumbnail do vídeo à esquerda + número + título colorido + descrição à direita
- Bônus adicionais com ícone e texto descritivo
- Certificado visual como mockup
- "Quem é [Autor]" em fundo ligeiramente diferente com bio e badges de credencial

**Botão CTA padrão:**
```css
.btn-cta {
  background: #f6c90e;
  color: #000000;
  padding: 18px 40px;
  border-radius: 6px;
  font-weight: 800;
  font-size: 1.1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

---

### Estilo 3. Dark Vibrante (Escuro com Acento de Cor Forte)
**Referência:** Página de vendas do Stories 10x

**Paleta:**
- Fundo principal: preto `#0d0d0d` a `#1a0a1a`
- Seções alternadas: `#12001a` ou gradiente sutil roxo/preto
- Cor de destaque: rosa/magenta `#e91e63` ou `#f50057`
- Palavra-chave no headline: rosa/magenta ou amarelo limão `#f7ef00`
- Texto principal: branco
- Botão CTA: rosa vibrante com texto branco

**Tipografia:**
- Heading: Montserrat ou Bebas Neue, tudo uppercase para headlines de impacto
- Body: DM Sans ou Nunito
- Destaques em COR FORTE com uppercase

**Padrões estruturais:**
- Headline all-caps com 2. 3 palavras em cor vibrante (rosa ou amarelo)
- "ESSE MÉTODO AUMENTA EM ATÉ 10X AS [MÉTRICA] DO SEU [CANAL]"
- Bullets de resultado em 2x2 grid (Ter ideias de / Criar stories de / Fazer as pessoas / Aumentar o alcance)
- Vídeo centralizado com play button colorido
- Features em linha horizontal (5 itens): Exemplos práticos, Apostila completa, etc.
- Badge de prova social: "+20 mil alunos" acima de headline de autoridade
- Headline de autoridade: all-caps com outline-text ou cor forte
- Fases do método em 3 círculos ou setas horizontais
- "ESSE É O EFEITO DO S10X EM DIVERSOS PERFIS". grid 2x2 de before/after screenshots
- "OS RESULTADOS SÃO ABSURDOS". carrossel de estudos de caso com screenshots de conversas
- Creators influentes: grid com foto, nome, seguidores e resultado específico
- Tabela comparativa: método tradicional (X vermelhos) vs método novo (checks coloridos)
- Grid de nichos com screenshots de resultados reais (Estética, Advocacia, Culinária, etc.)
- "DADOS DE MERCADO" como seção de credibilidade com carrossel
- FAQ em accordion
- Verificação de número de WhatsApp no rodapé

**Botão CTA padrão:**
```css
.btn-cta {
  background: #e91e63;
  color: #ffffff;
  padding: 18px 40px;
  border-radius: 50px;
  font-weight: 800;
  font-size: 1.1rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
```

---

## Seções Recorrentes em Todas as Páginas

### Hero (Primeira Dobra)
Toda página VTSD tem:
1. Label acima (ex: "Aula gratuita" ou tag do produto)
2. Headline principal com pelo menos 1 palavra em cor de destaque
3. Subheadline explicando o benefício
4. Bullets "o que vai aprender" ou "o que vai conseguir"
5. Vídeo com thumbnail e botão play
6. CTA botão grande
7. Features rápidas abaixo (4 itens: ícone + título + descrição)

### Tabela Comparativa (Com vs Sem / Tradicional vs Novo)
Elemento de conversão poderoso. Sempre 2 colunas:
- **Coluna negativa** (esquerda): o método antigo/sem o produto. fundo cinza/neutro, ícones X vermelho
- **Coluna positiva** (direita): com o produto. fundo na cor de destaque do produto, checks verdes/coloridos
- Título da coluna positiva = nome do produto

### Seção "Para Quem É"
Cards numerados (01, 02, 03, 04, 05) com:
- Número grande em cor de destaque
- Título do perfil
- Descrição de 1-2 linhas

### Estudos de Caso (Prova Social)
Dois formatos:
1. **Cards de resultado**. nome + foto + resultado em R$ ou métrica + depoimento
2. **Screenshots de conversa** (WhatsApp/DM). imagem do print + contexto em texto

### Seção "Quem é [Autor]"
- Foto profissional à direita (ou esquerda, alternando com grid de mídia)
- Bio com fatos concretos: seguidores, faturamento, prêmios, mencionar "Criador do Método VTSD"
- Badges abaixo do nome: credenciais em tag pequenas (Prêmio iBest, Hotmart Galaxy, etc.)

### Grid de Mídia
Fotos em grid 3x3 de: palestras, eventos, programas de TV, podcasts, premiações.

### FAQ Accordion
5-9 perguntas. Sempre inclui:
- "Funciona pra mim?"
- "Quando vou ver resultados?"
- "Que garantia eu tenho?"
- "Para quem é [afiliado / quem tem poucos seguidores / quem está no zero]?"

---

## Padrões de Cores por Categoria de Produto

| Tipo de Produto | Estilo | Cor Principal | Destaque |
|---|---|---|---|
| Método completo / flagship | Light (branco) | Verde `#2f855a` | Verde/azul |
| Copywriting / comunicação | Dark Premium | Preto + Dourado `#f6c90e` | Amarelo |
| Redes sociais / crescimento | Dark Vibrante | Preto + Rosa `#e91e63` | Rosa/magenta |
| Produto de entrada / free | Light (branco) | Verde ou azul | Accent vibrante |

---

## Lógica de Alternância de Seções

Seguindo o padrão das páginas VTSD, a alternância correta é:

```
Seção 1: Hero (escuro com gradiente ou claro com imagem)
Seção 2: Features rápidas (fundo diferente do hero. claro se hero escuro)
Seção 3: Produto/Agentes (escuro com mockup)
Seção 4: Prova social / depoimentos (claro com cards)
Seção 5: Autoridade / método (fundo médio ou escuro)
Seção 6: Comparativo com/sem (claro)
Seção 7: Mercado / clippings (claro ou cinza claro)
Seção 8: Currículo / módulos (escuro)
Seção 9: Bio do autor (claro ou inverso)
Seção 10: CTA final (escuro com gradiente ou cor vibrante)
```

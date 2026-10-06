---
name: "source-command-feedback-low-ticket"
description: "Faz correção completa de página de vendas low ticket. analisa copy (categorias low ticket, 7 Leis, vícios proibidos), estrutura (11 seções) e design (hierarquia visual, CTA, responsividade) em 2 blocos. Gera HTML corrigido se solicitado. Use esta skill SEMPRE que o usuário quiser revisar ou corrigir uma página de low ticket, pedir feedback de página low ticket, mencionar \"corrigir minha página low ticket\", \"analisar minha LT\", \"o que está errado na minha página de produto de entrada\", ou enviar um link de página low ticket para revisão."
---

# source-command-feedback-low-ticket

Use esta skill quando o usuário pedir o comando `/feedback-low-ticket` do workshop (ou `feedback-low-ticket`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/feedback-low-ticket.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Feedback de Página Low Ticket. Correção low ticket

Você é uma Nav do Fluxo de Leandro Ladeira. Seu papel aqui é dar feedback honesto, direto e acionável sobre a página de vendas low ticket de um mentorado. olhando com olhos de quem conhece a metodologia low ticket por dentro.

---

## REGRA DE PERFORMANCE. ENTREGA EM BLOCOS

**NUNCA gere os 2 blocos de uma vez.** Entregue um bloco por vez, aguardando o mentorado entre cada um. Isso evita timeout e respostas cortadas.

Fluxo obrigatório:
1. Coletar contexto (link da página)
2. Fazer web_fetch da página
3. Identificar automaticamente: categoria low ticket, preço, seções presentes
4. Entregar **BLOCO 1: COPY + ESTRUTURA** → perguntar se quer continuar
5. Entregar **BLOCO 2: DESIGN** → perguntar qual opção de entrega final
6. Entregar a copy corrigida e/ou HTML (se solicitado)

---

## Diferenças fundamentais entre feedback de PV e feedback de LT

| Aspecto | Página de Vendas (8D) | Página Low Ticket (low ticket) |
|---|---|---|
| Estrutura | 16 seções (8D expandida) | 11 seções low ticket |
| Vídeo de vendas | VSL obrigatório | Sem VSL. A copy é o mecanismo de venda |
| Copy | Light Copy genérica | 4 categorias low ticket + 7 Leis + parágrafo técnico |
| Blocos de feedback | 3 (Copy, Design, Depoimentos vídeo) | 2 (Copy+Estrutura, Design) |
| Foco | Argumentação, furadeira, prova social pesada | Gancho dos primeiros 5 segundos, categoria low ticket, simplicidade |
| Preço | Qualquer faixa | R$17 a R$197 |
| Entrega final | Copy corrigida ou encaminha pra /copy-pagina | Copy corrigida + HTML novo gerado direto |

---

## Erros críticos específicos de low ticket

**Preço sem ancoragem visual**
Low ticket precisa de stack de valor com "valor total" riscado e preço real em destaque. Sem ancoragem, R$47 parece caro. Com ancoragem de R$497 riscado, R$47 parece irresistível.

**Copy vendendo como se fosse produto de R$997**
Página low ticket não precisa de 20 scrolls, furadeira completa com microetapas, 8 depoimentos e 5 bônus. O público decide em segundos. Se a página parece de produto caro, o lead desconfia.

**Furadeira completa exposta**
Em low ticket, simplificar. Mostrar os entregáveis com benefício prático, não o método detalhado. A pessoa quer resultado rápido, não entender o processo.

**Falta de urgência/escassez no CTA**
Produto barato precisa de empurrão. "Comprar agora" sozinho é fraco. Prazo, vagas, preço subindo, bônus temporário.

**Muitos entregáveis diluem valor**
Quando tudo é bônus, nada é bônus. 2-3 bônus estratégicos valem mais que 7 bônus genéricos.

**Depoimento elogiando o expert sem resultado**
"O professor é incrível" não vende low ticket. "Fiz em 3 dias e já vendi 5 peças" vende.

**Produto mencionado no hero**
Mesmo em low ticket, o produto não aparece nos primeiros parágrafos. O hero fala sobre o LEITOR e o problema/transformação dele.

**Categoria low ticket errada para o produto**
Plug & Play para um curso teórico? Inadequação para um template pronto? A categoria precisa casar com o tipo de produto e público.

---

## PASSO 1. Coleta de contexto

Pergunte ao mentorado:

```
Para dar um feedback preciso na sua página low ticket, preciso do link:

Qual é o link da sua página?
```

Aguarde a resposta antes de prosseguir. O assistente identifica sozinho: categoria low ticket, preço, estrutura e problemas.

---

## PASSO 2. Acesso à página

Com o link em mãos:

1. Use `web_fetch` para carregar a página e ler o conteúdo completo
2. Identifique automaticamente:
   - **Categoria low ticket**. qual das 4 categorias a copy usa (Inadequação, Identificação com o Problema, Plug & Play, Promessa Boa Demais) ou se não se encaixa em nenhuma
   - **Preço**. extrair o valor da página
   - **Seções presentes**. mapear quais das 11 seções existem e quais faltam
3. Se a página tiver senha ou for restrita, peça print ou a copy em texto

---

## PASSO 3. BLOCO 1: Feedback de Copy + Estrutura low ticket

### Diagnóstico da Categoria low ticket (automático)

Identificar qual das 4 categorias a copy se encaixa. Se não se encaixa claramente em nenhuma, recomendar a mais adequada para o tipo de produto e público.

**Critérios de identificação:**

| Categoria | Sinal na copy | Ideal para |
|---|---|---|
| Inadequação | Coloca o leitor numa posição desconfortável, desatualizado | Cursos, aulas, métodos, frameworks |
| Identificação com o Problema | Descreve a realidade do leitor com detalhes sensoriais | Métodos, cursos práticos, mentorias |
| Plug & Play | Mostra resultado prático sem jargão, página curta | Planilhas, templates, checklists, kits |
| Promessa Boa Demais | História real com números verificáveis, tom de relato | Aulas, workshops com caso real |

### Checklist das 7 Leis

- [ ] **Ensinar em vez de prometer**. A copy entrega conhecimento real? A curiosidade vem do aprendizado?
- [ ] **Nomear cria realidade**. Tem nome próprio para o problema ou solução?
- [ ] **Produto não aparece na copy**. Nenhuma menção ao produto nos primeiros parágrafos?
- [ ] **Tom de escritor, não de vendedor**. Mostra em vez de empurrar?
- [ ] **Especificidade mata generalização**. Números, datas, valores, situações reais?
- [ ] **Informar, não vender**. A copy avisa ou ensina? Nunca vende?
- [ ] **Inimigo concreto**. Tem um culpado externo identificado?

### Checklist de Vícios Proibidos (varredura obrigatória)

Percorrer TODO o texto da página e listar cada ocorrência encontrada:

- [ ] Travessão (. )? Listar onde aparece
- [ ] Estrutura "Não é X. É Y."? Listar onde aparece
- [ ] Ponto de exclamação? Listar onde aparece
- [ ] Perguntas no gancho/headline? Listar onde aparece
- [ ] "mesmo que" / "sem precisar"? Listar onde aparece
- [ ] Emojis na copy? Listar onde aparecem
- [ ] Frases genéricas de vendedor? Listar quais
- [ ] Produto mencionado no hero/lead? Incluindo nome, método, curso, sigla

### Parágrafo Técnico/Racional

- [ ] Existe parágrafo em itálico ao final da copy de abertura?
- [ ] O parágrafo é técnico/racional (dados, lógica) e não emocional?

### Checklist das 11 Seções

Mapear quais estão presentes e quais faltam:

- [ ] 1. **Promessa (hero)**. Headline + copy da categoria + CTA
- [ ] 2. **Ferramenta**. Uma ferramenta específica dentro da entrega que resolve uma dor rápida
- [ ] 3. **Depoimento**. Com resultado específico (antes/depois, número, prazo)
- [ ] 4. **Entregáveis**. Grid 2 colunas com nome + benefício prático
- [ ] 5. **Bônus**. 2-3 bônus com valor individual em R$
- [ ] 6. **Stack de Valor**. Ancoragem visual (valor total riscado vs preço real)
- [ ] 7. **Garantia**. Tipo + prazo + selo visual
- [ ] 8. **Quem sou eu**. Mini bio com prova (número, cliente, conquista)
- [ ] 9. **FAQ**. 3-5 objeções comuns respondidas
- [ ] 10. **CTA Final**. Preço + parcelamento + botão + urgência
- [ ] 11. **Rodapé**. Copyright, termos, privacidade

### Formato de output. Bloco 1

```
## BLOCO 1: COPY + ESTRUTURA low ticket

### Diagnóstico da Categoria
Categoria identificada: [categoria ou "não se encaixa em nenhuma"]
Categoria recomendada: [se diferente da identificada]
Por quê: [explicação com base no tipo de produto e público]

### Preço Identificado
R$ [valor encontrado na página]

### Seções Presentes vs Esperadas
Presentes: [lista]
Faltando: [lista com impacto de cada ausência]

### O que está funcionando
[Pontos positivos. ser específico]

### O que precisa corrigir

**[Seção ou aspecto]**
Problema: [o que está errado]
Correção sugerida: [exemplo concreto reescrito]

### 7 Leis. Verificação
[Para cada lei: presente ou ausente, com exemplo de correção se ausente]

### Vícios Proibidos Encontrados
[Lista de cada ocorrência com localização e correção sugerida]

### Parágrafo Técnico
[Presente ou ausente. Se ausente, sugerir um exemplo]

### Prioridade máxima
[2-3 ajustes que mais impactam conversão no low ticket]
```

**Após entregar o Bloco 1, pergunte:**
```
Esse foi o feedback de copy e estrutura. Quer continuar para o feedback de design?

1. Sim, continuar para o design
2. Quero discutir algo da copy antes
```

---

## PASSO 4. BLOCO 2: Feedback de Design

### Checklist de Design (adaptado para low ticket)

**Hierarquia Visual**
- [ ] Headline é o maior elemento da primeira dobra?
- [ ] Ordem visual guia o olho até o CTA?
- [ ] Página é enxuta? (low ticket não precisa de 20 scrolls)

**CTA**
- [ ] Botão em cor contrastante com o fundo?
- [ ] Texto do botão é uma ação clara (não só "Comprar")?
- [ ] CTA aparece em múltiplos pontos (mínimo 3)?
- [ ] Tem urgência/escassez junto ao CTA?

**Preço e Ancoragem**
- [ ] Stack de valor com ancoragem visual (valor riscado + preço real)?
- [ ] Parcelamento visível?
- [ ] Preço em destaque (tamanho grande, cor contrastante)?

**Legibilidade**
- [ ] Fonte legível no mobile?
- [ ] Contraste suficiente texto/fundo?
- [ ] Parágrafos curtos (máx. 3-4 linhas)?
- [ ] Fontes são sans-serif? (serifadas = cara de template genérico)

**Responsividade**
- [ ] Funciona bem no mobile?
- [ ] Grid de entregáveis empilha corretamente?
- [ ] Botões com tamanho adequado para toque?

**Anti-IA (ler `.claude/skills/paginas/references/anti-ia-design.md`)**

Low ticket é o nicho onde "cara de IA" mais afeta conversão: o visitante decide em segundos, e se bater o olho e reconhecer "isso é Lovable/v0", sai sem clicar. Marcar cada clichê presente:

- [ ] Paleta roxo `#6b46c1` + azul `#3182ce`? (Tailwind/v0 default)
- [ ] Gradiente 135deg roxo→azul em fundo grande?
- [ ] CTA verde `#38a169` genérico em nicho que não é saúde?
- [ ] Glassmorphism (`backdrop-filter: blur`) em card de entregável ou bônus? (PROIBIDO em low ticket. Glassmorphism faz low ticket parecer "premium fake" e derruba conversão)
- [ ] Glow colorido `box-shadow: 0 0 Npx rgba(cor)` em repouso?
- [ ] Headline com gradiente de texto (`background-clip: text`)?
- [ ] Inter ou Poppins em nicho emocional?
- [ ] Estilo `glass_escuro` aplicado? (PROIBIDO em low ticket, usar `flat_claro` ou `teal_claro`)
- [ ] Hero centralizado com gradiente atrás + botão embaixo?
- [ ] Cards brancos idênticos em fundo bege (assinatura Lovable)?
- [ ] Mínimo 4 tipos de fundo diferentes entre seções? (Se não: monotonia visual)
- [ ] Contraste forte entre seções? (Não só tom-sobre-tom)
- [ ] Tem pelo menos 1 divisor decorativo (wave, linha, mudança abrupta)?
- [ ] Dot indicator do carrossel NÃO expande para linha (`width: 20px`)?

**Imagens**
- [ ] Imagens contextuais (relacionadas ao conteúdo da seção)?
- [ ] Não são genéricas tipo "pessoa sorrindo com laptop"?
- [ ] Nenhum emoji como ícone em seção de valor (entregáveis, bônus, garantia)?

Para cada "sim", usar a tabela de substituições em `anti-ia-design.md` e recomendar a troca no output.

### Formato de output. Bloco 2

```
## BLOCO 2: DESIGN

### O que está funcionando
[Pontos positivos]

### O que precisa corrigir
**[Área do problema]**
Problema: [descrição]
Correção sugerida: [ação específica]

### Prioridade máxima
[2-3 ajustes críticos de design]
```

---

## PASSO 5. Entrega final

Após os 2 blocos, pergunte:

```
Feedback completo entregue. O que quer fazer agora?

1. Receber a copy corrigida (texto pronto para copiar e colar)
2. Receber a copy corrigida + página HTML nova
3. Já tenho o que preciso
```

### Opção 1. Copy Corrigida (texto)

Reescreva toda a copy aplicando as correções. Entregue seção por seção, na ordem das 11 seções low ticket:

```
## COPY CORRIGIDA

---
### SEÇÃO 1. PROMESSA (HERO)
[Copy da categoria low ticket corrigida]
[CTA]

---
### SEÇÃO 2. FERRAMENTA
[Texto corrigido]

---
### SEÇÃO 3. DEPOIMENTO
[Depoimentos corrigidos ou orientações]

[...até a Seção 11]
```

Aplicar a varredura de vícios proibidos em toda a copy corrigida antes de entregar:
- [ ] Nenhum travessão no texto
- [ ] Nenhuma estrutura "Não é X. É Y."
- [ ] Nenhum ponto de exclamação
- [ ] Nenhuma pergunta no gancho
- [ ] Nenhum "mesmo que" / "sem precisar"
- [ ] Nenhum emoji
- [ ] Nenhuma frase genérica de vendedor
- [ ] Produto não mencionado no hero/lead

Após entregar a copy, pergunte:
```
1. Aprovar copy
2. Quero ajustar algo
```

### Opção 2. Copy Corrigida + HTML Novo

Primeiro entregar a copy corrigida (Opção 1), pedir aprovação. Depois gerar o HTML.

**Para gerar o HTML, seguir o Fluxo de Geração Obrigatório de 7 etapas** definido em `.claude/skills/paginas/SKILL.md` (seção "Fluxo de Geração"):

1. Ler `.claude/skills/paginas/SKILL.md` PRIMEIRO. fluxo completo, tabela de estilo por nicho, checklist final.
2. Escolher **UM ÚNICO estilo visual** para a página inteira pela tabela de nicho (ver regra automática de low ticket logo abaixo). PROIBIDO misturar estilos diferentes na mesma página.
3. **LER OS TEMPLATES REAIS DO ESTILO ESCOLHIDO** (OBRIGATÓRIO): para cada seção da página, abrir `.claude/skills/paginas/references/templates/{secao}_{estilo}/code.html`. todos no mesmo estilo. Mínimo 4 templates lidos por geração. Seções com template próprio: hero, dor, paliativo, metodo, cta, faq.
4. Extrair tokens mestres do estilo (`--radius`, `--border-width`, `--shadow`, tipografia, estilo de botão) e colocar no `:root`. TODAS as seções (inclusive entregáveis, bônus, stack, oferta, garantia) herdam esses tokens e parecem nativas do estilo escolhido.
5. Copiar a estrutura HTML+CSS dos templates lidos e adaptar cores/fontes/textos ao nicho. NÃO reescrever do zero.
6. Usar `references/estruturas-pagina.md` para ordem de seções e `references/design-system-components.md` apenas como fallback para seções sem template próprio e para utilitários globais (animações, responsivo, CDNs).
7. Antes de salvar, rodar o checklist do SKILL.md: confirmar que a página usa UM único estilo do início ao fim e que os tokens mestres foram aplicados em todas as seções.

**Regra de estilo automática para low ticket (tabela de decisão da skill de páginas):**
- Estilo único da página: `flat_claro` ou `teal_claro` (escolher um e usar em todas as seções)
- Motivo: estilos claros passam leveza e baixo risco, perfeito para ticket de entrada

**Regras obrigatórias do HTML:**
- Arquivo único: CSS em `<style>`, JS em `<script>` (zero dependências além de Google Fonts)
- Design profissional: tipografia sans-serif, paleta harmoniosa, espaçamentos generosos
- 100% responsivo: mobile-first com media queries
- Mínimo 4 tipos de fundo diferentes entre seções
- Pelo menos 2 seções com imagem de fundo (picsum.photos + overlay)
- Grid 2 colunas para entregáveis (NUNCA 3)
- Cards com min-width 320px, padding 28px+, font-size 0.95rem+
- Header com logotipo obrigatório
- Texto SEMPRE em pt-BR com acentos corretos
- NÃO parecer Lovable/v0 (sem cards brancos idênticos em fundo bege)
- Imagens contextuais (não genéricas). seguir processo de seleção semântica da skill de páginas
- CTA flutuante no mobile

**Estrutura obrigatória do HTML (11 seções):**
1. Promessa (hero + copy da categoria low ticket + CTA)
2. Ferramenta que resolve dor específica rápida
3. Depoimento com resultado
4. Entregáveis (grid 2 colunas)
5. Bônus com valor individual em R$
6. Stack de Valor (ancoragem visual: valor total riscado vs preço real)
7. Garantia com selo visual
8. Quem sou eu com prova
9. FAQ (3-5 objeções)
10. CTA final com preço, parcelamento, botão grande, urgência
11. Rodapé

**Varredura final antes de salvar o HTML:**
Executar a varredura de vícios proibidos em todo o texto visível da página. Nenhum HTML pode ser salvo sem passar por essa revisão.

Salvar em: `meus-produtos/{ativo}/entregas/paginas/low-ticket-corrigida-[produto].html`

Após salvar: "Pronto. Sua página corrigida foi salva em `meus-produtos/{ativo}/entregas/paginas/low-ticket-corrigida-[produto].html`. Abra no navegador para visualizar."

---

## Tom e postura no feedback

- Nav orienta, não aprova. Vocabulário: "eu recomendo", "na minha opinião"
- Não ficar só na análise. sugerir a copy pronta reescrita
- Não suavizar crítica por medo de desagradar
- Ser direto e específico: "esse headline não funciona porque..." não "talvez pudesse melhorar"

---

## Próximo Passo

Após a entrega, sugerir: `/copy-anuncio` para criar anúncios que levam tráfego para a página corrigida.

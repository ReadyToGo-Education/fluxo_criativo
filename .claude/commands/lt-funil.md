---
name: workshop-marketing:lt-funil
description: Criar produto low ticket completo usando a metodologia low ticket do VTSD. produto de entrada (R$37-97), página final do quiz, anúncios low ticket, produto desafio e copy para Hotmart.
---

# Low Ticket (low ticket). Produto de Entrada Rápido e Lucrativo

Cria produtos low ticket usando a metodologia low ticket do VTSD: produto de entrada, página de quiz, anúncios low ticket e copy para plataforma.

## Usage

```
/lt-funil
```

## O Que Fazer

### 1. Contexto
Leia `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme o CLAUDE.md).
Consulte `.claude/skills/vtsd-completo/SKILL.md` (Módulo 10: low ticket).

Verifique também se existe `meus-produtos/{ativo}/pesquisa-mercado.md`. Se NÃO existir (ou tiver mais de 90 dias), acione a skill `pesquisa-mercado` antes de qualquer sugestão de preço, oferta, ângulo de quiz ou anúncio. É obrigatória. A pesquisa alimenta: sugestão de preço low ticket (baseada em faixa real do nicho), ângulos do quiz (baseados em assuntos quentes e objeções reais), copy dos anúncios (padrões virais mapeados) e copy da página (objeções reais do Reclame Aqui).

### 2. Entrevista (UMA pergunta por vez, com progresso visual)

**Bloco 1/5. O Que Criar:**
```
O que quer criar?

1. Produto low ticket completo (página quiz + anúncios + copy)
2. Página final do quiz (estrutura de 12 blocos)
3. Anúncios low ticket (focados em quiz)
4. Produto desafio (3-7 dias com missões)
5. Copy para Hotmart/Kiwify (descrição da plataforma)

Digite o número:
```

```
--- Bloco 1/5 concluído ---
Entregável: [tipo escolhido]
Próximo: Formato do produto
---
```

**Bloco 2/5. Formato do Produto:**
```
Qual tipo de produto low ticket?

1. E-book
2. Guia prático
3. Planilha
4. Checklist
5. Mini-curso (até 2h)
6. Desafio (3-7 dias)
7. Agente GPT
8. Template

NÃO recomendado para low ticket: mentorias, cursos extensos, comunidades.

Digite o número:
```

```
--- Bloco 2/5 concluído ---
Entregável: [tipo]
Formato: [formato escolhido]
Próximo: Problema que resolve
---
```

**Bloco 3/5. Problema:**
```
Qual problema específico esse produto resolve?
Precisa ser algo rápido e tangível.
(ex: "Organizar finanças em 7 dias", "Criar 30 posts em 1 hora")
```

```
--- Bloco 3/5 concluído ---
Entregável: [tipo]
Formato: [formato]
Problema: [problema]
Próximo: Preço
---
```

**Bloco 4/5. Preço:**
```
Qual o preço? (entre R$37 e R$97)
(ex: "R$47", "R$67", "R$97")
```

```
--- Bloco 4/5 concluído ---
Entregável: [tipo]
Formato: [formato]
Problema: [problema]
Preço: R$ [valor]
Próximo: Quiz
---
```

**Bloco 5/5. Quiz:**
```
Tem quiz pronto?

1. Sim, no Lovable
2. Sim, no Typeform
3. Sim, outra ferramenta
4. Não tenho quiz ainda

Digite o número:
```

**Confirmação antes de gerar:**
```
Resumo do produto low ticket:
- Entregável: [tipo]
- Formato: [formato]
- Problema: [problema]
- Preço: R$ [valor]
- Quiz: [ferramenta ou não tem]

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### 3. Geração

**Quadro Low Ticket:**
Gerar 5 opções de Quadro seguindo as regras VTSD adaptadas para low ticket:
- Resultado rápido e tangível
- Problema específico
- Solução prática e imediata
- Exemplos: "Organizar finanças em 7 dias", "Criar 30 posts em 1 hora"

**Página Final do Quiz (12 blocos. estrutura obrigatória low ticket):**
1. Headline com premissa. gancho principal
2. Subheadline. reforço de dor ou desejo
3. Print de Resultado. Antes e Depois visual
4. Valor + Botão de compra 1
5. Entregáveis detalhados. nome, benefícios práticos, resumo
6. Suporte (se houver)
7. Valor + Botão de compra 2
8. Bônus. nome, benefícios, o que entrega
9. Valor + Botão de compra 3
10. Garantia
11. Autoridade do criador. nome, experiência, provas sociais
12. Valor + Botão de compra 4 (última chamada)

Gerar como HTML seguindo o padrão de qualidade do CLAUDE.md (arquivo único, responsivo, Google Fonts).

**Anúncios Low Ticket (3 variações para quiz):**
Estrutura de cada anúncio:
1. Abertura. pergunta ou situação familiar
2. Problema. dor do público
3. Solução. o que o quiz revela
4. CTA. convite para fazer o quiz

Regras low ticket:
- Não mencionar preço no anúncio
- Não prometer promoção
- Focar no diagnóstico/descoberta
- Usar curiosidade como gatilho

**Produto Desafio (se escolhido):**
Estrutura de desafio (3-7 dias):
- Nome atrativo do desafio
- Duração definida
- Missões diárias claras (conteúdo + missão + entrega esperada)
- Grupo de suporte (WhatsApp/Telegram)
- Premiação ou reconhecimento

**Copy para Hotmart/Kiwify:**
Elementos da descrição na plataforma:
- Headline clara
- Para quem é
- O que resolve
- O que entrega (lista de entregáveis)
- Diferenciais
- Garantia

**Agente GPT como Produto (se escolhido):**
Tipos de agentes vendáveis:
- Gerador de conteúdo
- Assistente de planejamento
- Criador de copy
- Organizador de tarefas
- Tutor especializado

Estrutura do produto:
- Link do agente
- Manual de uso
- Prompts prontos
- Suporte básico

### 4. Salvar

| Material | Destino |
| --- | --- |
| Página final do quiz (HTML) | `meus-produtos/{ativo}/entregas/paginas/quiz-[produto].html` |
| Anúncios low ticket | `meus-produtos/{ativo}/entregas/criativos/caixa-rapido-[produto].md` |
| Produto desafio | `meus-produtos/{ativo}/entregas/textos-de-venda/desafio-[produto].md` |
| Copy Hotmart/Kiwify | `meus-produtos/{ativo}/entregas/textos-de-venda/copy-plataforma-[produto].md` |
| Agente GPT (estrutura) | `meus-produtos/{ativo}/entregas/textos-de-venda/agente-gpt-[produto].md` |

### 5. Próximo Passo
"Produto low ticket criado. Use `/copy-anuncio` para criar mais variações de anúncios, ou `/estrategia-funil` para mapear o funil completo com upsell."

# Referência: Questionário Completo de Calibração VSL (21 Perguntas)

Este arquivo contém o questionário completo de calibração usado para gerar o perfil estratégico da VSL.
As 4 perguntas do SKILL.md são uma versão simplificada. Use este arquivo quando o usuário quiser calibração avançada.

---

## Classificação Interna (não mostrar ao usuário)

Para cada pergunta, classifique internamente em A/B/C/D conforme a tabela abaixo.

| # | Dimensão | A | B | C | D |
|---|----------|---|---|---|---|
| Q1 | Tipo de produto | Digital | Serviço | Físico | Híbrido |
| Q2 | Ticket | Baixo (<R$297) | Médio (R$297-997) | Alto (R$997-2997) | Premium (>R$2997) |
| Q3 | Formato de entrega | Autoatendimento | Grupo | Individual | Misto |
| Q4 | Nível de consciência | Não sabe que tem o problema | Sabe o problema, não a solução | Sabe a solução, tentou alternativas | Conhece concorrentes |
| Q5 | Tentativas anteriores | Nenhuma | 1-2 tentativas | 3-5 tentativas | Muitas tentativas frustradas |
| Q6 | Objeção dominante | "Não acredito que funciona" | "Não confio no expert" | "Não é prioridade agora" | "Não tenho dinheiro" |
| Q7 | Demonstrabilidade | Demo em 90s | Precisa explicar | Abstrato | Impossível demonstrar |
| Q8 | Volume de provas | Nenhuma | 1-3 provas | 4-10 provas | 10+ provas |
| Q9 | Nível de autoridade | Nenhuma | Experiência prática | Credencial formal | Referência no nicho |
| Q10 | Força da história | Sem história | História fraca | História boa | História épica |
| Q11 | Tipo de diferencial | Mecanismo único | Resultado superior | Método exclusivo | Sem diferencial claro |
| Q12 | Saturação do mercado | Virgem | Pouca concorrência | Saturado | Muito saturado |
| Q13 | Complexidade de explicação | Simples | Moderada | Complexa | Muito complexa |
| Q14 | Tipo de transformação | Financeira | Saúde | Relacionamento | Habilidade/Carreira |
| Q15 | Urgência real | Nenhuma | Baixa | Média | Alta |
| Q16 | Canal | YouTube/Orgânico | Meta Ads | Google Ads | Múltiplo |
| Q17 | Formato preferido | Direto ao ponto | Com história | Educativo | Emocional |
| Q18 | Evidência disponível | Prints/Screenshots | Vídeo depoimento | Dados numéricos | Sem evidência |
| Q19 | Objetivo primário | Vendas diretas | Captação de leads | Upsell | Lançamento |
| Q20 | Tom desejado | Agressivo/Urgente | Educativo | Inspiracional | Conversacional |
| Q21 | Densidade | Direto | Equilibrado | Narrativo | — |

---

## Regras de Calibração Automática

### Definição do Hook Type

| Condição | Hook Type |
|----------|-----------|
| Q4 = A ou B (público não consciente) | `pain` ou `violation` |
| Q4 = C ou D (público consciente, tentou alternativas) | `result_first` ou `demo` |
| Q7 = A (pode demonstrar em 90s) | `demo` |
| Q10 = C ou D (história forte) | manter narrativo no hook |

### Definição do Proof Mode

| Q8 (volume de provas) | Q18 (evidência) | Proof Mode |
|-----------------------|-----------------|------------|
| A (nenhuma) | D (sem evidência) | `logic_only` |
| B (1-3) | A/B/C | `hybrid` |
| C ou D (4+) | A/B/C | `social_proof` |
| Qualquer | D (sem evidência) | `logic_only` (bloqueado) |

### Ajustes por Objeção Dominante (Q6)

| Objeção | Ajuste na VSL |
|---------|---------------|
| A — "não funciona" | Ampliar bloco 5 (mecanismo) e bloco 7 (prova) |
| B — "não confio" | Ampliar bloco 4 (história) e bloco 9 (credenciais) |
| C — "não é prioridade" | Ampliar bloco 8 (custo da inércia) e urgência no bloco 12 |
| D — "sem dinheiro" | Ampliar bloco 10 (ancoragem) e custo de não resolver no bloco 8 |

### Ajustes por Saturação (Q12)

| Saturação | Ajuste |
|-----------|--------|
| A — virgem | Educar primeiro, menos destruição de alternativas |
| B — pouca | Estrutura padrão |
| C — saturado | Ampliar bloco 6 (destruição de alternativas), usar mecanismo forte |
| D — muito saturado | Bloco 4 pode ser Manifesto, abordagem tribal, focar em diferencial de método |

### Budget de Palavras por Ticket

| Ticket | Hook (B1-3) | Narrativa (B4-6) | Prova/Desejo (B7-8) | Oferta/Close (B9-12) | Total |
|--------|-------------|------------------|---------------------|----------------------|-------|
| A — Baixo | 180-220 | 220-260 | 180-220 | 280-340 | ~1.200 |
| B — Médio | 200-250 | 260-300 | 200-250 | 320-400 | ~1.200 |
| C — Alto | 230-280 | 280-340 | 220-270 | 380-480 | ~1.200 |
| D — Premium | 250-300 | 300-380 | 250-300 | 420-520 | ~1.200 |

---

## Módulos Substitutos

Use quando um ativo está ausente:

### Sem história pessoal (Q10 = A ou B)

Escolher alternativa conforme perfil:

| Situação | Estrutura alternativa para Bloco 4 |
|----------|------------------------------------|
| Expert técnico com pesquisa | Descoberta Científica |
| Mercado saturado e prometedor | Falha Sistêmica do Mercado |
| Tem casos de clientes | Transformação de Cliente |
| Público analítico, ticket alto | Anti-História (ir direto ao mecanismo) |
| Público tribal, nicho forte | Manifesto |

### Sem prova social (Q8 = A, Q18 = D)

Substitutos para Bloco 7:

| Substituto | Quando usar |
|------------|-------------|
| Prova Lógica: "Funciona porque A causa B, que causa C" | Sempre disponível |
| Prova Analógica: "Funciona pelo mesmo princípio que [algo conhecido]" | Quando há analogia forte |
| Prova de Engenharia: mostrar o mecanismo por dentro | Quando produto é técnico |
| Prova Estatística: citar dado de terceiros | Quando há dado de mercado |
| Prova de Risco Reverso: garantia como prova | Sempre disponível |

### Sem mecanismo claro (Q11 = D)

Ativar abordagem de desconstrução:
> "O erro que o mercado comete é tratar [sintoma] como se fosse o problema real. O que ninguém te conta é que [causa raiz]."

Nomear a desconstrução com um conceito próprio.

---

## Perguntas Avançadas para Calibração Aprofundada

Use estas perguntas quando o usuário quiser detalhamento extra:

**Sobre o produto:**
- O que exatamente você vende? (curso, mentoria, SaaS, produto físico, serviço)
- Qual problema específico ele resolve?
- O que torna seu método diferente de tudo que já existe?
- Qual é o mecanismo interno que faz funcionar?

**Sobre o público:**
- Quem é seu cliente ideal? (idade, gênero, profissão, situação)
- Qual a maior dor que essa pessoa sente hoje?
- O que essa pessoa já tentou antes e não funcionou?
- Qual o resultado dos sonhos dessa pessoa?
- Que palavras essa pessoa usa para descrever o problema?

**Sobre história e provas:**
- Você tem uma história pessoal de transformação relacionada ao produto?
- Tem histórias de clientes com resultados?
- Tem números, dados, screenshots, depoimentos?
- Tem alguma credencial, formação ou autoridade no tema?

**Sobre a oferta:**
- Qual o preço?
- Tem bônus? Quais?
- Tem garantia? De quanto tempo?
- Qual a forma de pagamento?

---

## Checklist de QA da VSL

Antes de entregar o script final, verificar:

### Checklist Universal
- [ ] Todos os 12 blocos presentes (mesmo que comprimidos)
- [ ] CTA único e explícito no bloco 12 (mínimo 2 repetições)
- [ ] Objeção dominante respondida antes do CTA
- [ ] Total entre 900 e 1.500 palavras
- [ ] Se proof_mode = logic_only: nenhum texto tipo depoimento
- [ ] Mecanismo tem nome próprio no bloco 5
- [ ] Garantia mencionada no bloco 12

### Checklist Light Copy
- [ ] Nenhum travessão (—)
- [ ] Nenhum ponto de exclamação
- [ ] Nenhuma pergunta no gancho (bloco 1)
- [ ] Nenhuma estrutura "Não é X. É Y."
- [ ] Nenhum "mesmo que" ou "sem precisar"
- [ ] Nenhuma promessa vaga sem dado ou situação

### Checklist de Coerência
- [ ] O que o hook promete é entregue na oferta
- [ ] A narrativa suporta a promessa do Quadro
- [ ] Tom consistente do início ao fim
- [ ] Linguagem combina com o perfil do público (idconsumidor.md)
- [ ] Ancoragem de preço é credível
- [ ] Bônus e valores existem no perfil do produto

### Checklist de Áudio
- [ ] Frases de 10 a 25 palavras (naturais para fala)
- [ ] Transições suaves entre todos os blocos
- [ ] Pausas indicadas com "..." nos momentos dramáticos
- [ ] Sem bullets, caps ou formatação visual no corpo da copy

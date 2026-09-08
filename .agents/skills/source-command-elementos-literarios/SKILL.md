---
name: "source-command-elementos-literarios"
description: "Aplicar os 26 Elementos Literários (Ladeirísticos) do Light Copy em copy existente ou criar trechos do zero. Gera 3 variações usando 1 a 3 elementos que combinam com o contexto."
---

# source-command-elementos-literarios

Use this skill when the user asks to run the migrated source command `elementos-literarios`.

## Command Template

# Elementos Literários. Aplicador de Ladeirísticos

Transforma copy comum em copy memorável usando os 26 Elementos Literários do Light Copy de Leandro Ladeira. Pode aplicar em copy existente (turbinar) ou criar trechos novos do zero.

## Usage

```
/elementos-literarios
```

## O Que Fazer

### 1. Contexto

Leia `meus-produtos/.ativo` e depois `meus-produtos/{ativo}/perfil.md` e `meus-produtos/{ativo}/idconsumidor.md` se existirem. Use o Quadro, Urgências Ocultas e tom da marca para calibrar as sugestões.

Leia também `.Codex/skills/elementos-literarios/SKILL.md` para ter os 26 elementos completos na cabeça.

### 2. Entrevista (UMA pergunta por vez)

**Pergunta 1. Modo de trabalho:**
```
O que você quer fazer?

1. Turbinar uma copy que já tenho
2. Criar um trecho do zero
3. Ver exemplos dos 26 elementos aplicados ao meu produto

Digite o número:
```

**Se escolher 1 (turbinar existente):**
- Pergunta 2: "Cole aqui a copy que você quer turbinar"
- Pergunta 3: "Onde essa copy vai ser usada?"
  ```
  1. Anúncio (gancho de 3 segundos)
  2. Headline de página
  3. Bullets de benefícios
  4. História de abertura
  5. Quebra de objeção
  6. Fechamento/CTA
  7. Email
  8. Roteiro de Reels/VSL
  9. Post de rede social
  ```

**Se escolher 2 (criar do zero):**
- Pergunta 2: "Qual o tipo de trecho que você quer criar?" (mesmas opções acima)
- Pergunta 3: "Qual a ideia central ou argumento que o trecho precisa passar?"
- Pergunta 4: "Qual tom você quer? 1) Bem-humorado 2) Sério e argumentativo 3) Provocativo 4) Inspiracional"

**Se escolher 3 (exemplos):**
- Pergunta 2: "Sobre qual aspecto do seu produto?" (sugerir Quadro, Furadeira, uma dor específica, um benefício)
- Vá direto para a geração dos exemplos.

### 3. Seleção dos Elementos

Baseado no formato escolhido, consulte a tabela de combinações da skill `elementos-literarios`:

| Formato | Elementos mais fortes |
|---|---|
| Anúncio de gancho | Hipérbole, Metáfora Visual, Setup+Punchline, Tríade Cômica |
| Headline de página | Antítese, Aforismo, Confiança Extrema, Neologismo |
| Bullets | Lista, Tríade Cômica, Jogos de Palavras |
| História de abertura | Transformar História em Copy, Autodepreciação, Desfecho Inesperado |
| Quebra de objeção | Sarcasmo/Ironia, Raciocínio Lógico Improvável, Mundo ao Contrário |
| Fechamento/CTA | Confiança Extrema, Anáfora, Aforismo |
| Email | Apelo ao Cotidiano, Setup+Punchline, Ponto de Vista |
| Reels/VSL | Hipérbole, Paródia, Onomatopeia, Personificação |

Escolha internamente 3 elementos diferentes para gerar 3 variações distintas.

### 4. Geração

Gere **3 variações** no seguinte formato:

```
=== VARIAÇÃO 1. [Nome do elemento usado] ===

[texto da copy turbinada ou criada]

Por que funciona: [1 frase explicando o efeito do elemento no argumento]

---

=== VARIAÇÃO 2. [Nome do elemento usado] ===

[texto]

Por que funciona: [1 frase]

---

=== VARIAÇÃO 3. [Nome do elemento usado] ===

[texto]

Por que funciona: [1 frase]
```

**Para o modo "ver exemplos":** gere 5 a 8 exemplos curtos cobrindo elementos diferentes, cada um com o nome do elemento e o trecho aplicado ao produto do aluno.

### 5. Checklist Obrigatório (aplicar ANTES de mostrar)

Antes de apresentar as variações, faça varredura eliminando:
- Travessão (. ) em qualquer frase
- Ponto de exclamação
- Perguntas no gancho
- Estrutura "Não é X. É Y."
- "mesmo que" ou "sem precisar" como muletas
- Promessas vagas sem dado ou situação concreta
- Elemento literário no começo da frase (tem que estar inserido naturalmente)

### 6. Aprovação

Mostre as variações e pergunte:

```
1. Gostei de uma delas, pode salvar
2. Quero gerar mais 3 variações com outros elementos
3. Quero ajustar uma variação específica
4. Quero combinar trechos de variações diferentes
```

### 7. Entrega

Se o aluno escolher salvar, salve em `meus-produtos/{ativo}/entregas/copy-pagina/elementos-literarios-{data}.md` com:
- Contexto original (copy anterior ou briefing)
- Formato de uso
- Variação escolhida e elemento aplicado
- Observações de uso

Informe o caminho e sugira próximo passo: "Quer que eu aplique essa copy em uma página (`/copy-pagina`), anúncio (`/copy-anuncio`) ou carrossel (`/copy-carrossel`)?"

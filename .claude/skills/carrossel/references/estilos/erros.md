# Estilo. Carrossel "Erros comuns para quem quer [DESEJO]"

> Carrossel que expõe erros que sabotam quem persegue um desejo específico do nicho.

---

## Coleta extra do Passo 1

**Adicionar UMA pergunta após a 1.5 do `passo-coleta-base.md`.**

### 1.6. Desejo principal do público

**Regra de exemplo personalizado.** Antes de exibir, leia `perfil.md` (Quadro, Decorados, nicho) e `idconsumidor.md` (dores, desejos, paliativos) do produto ativo. Gere 2 a 3 exemplos de desejo COERENTES com o nicho do produto e o público-alvo, em vez de exemplos genéricos.

Por exemplo:
- Produto de tarô → "tirar a primeira leitura sem trava, virar leitora consultora, deixar de depender de outros pra interpretar cartas"
- Produto de finanças → "sair do vermelho em 6 meses, montar a primeira reserva de emergência, parar de gastar tudo no dia 10"
- Produto fitness pós-parto → "voltar a calçar a calça pré-gravidez, tirar foto de praia sem culpa, ter energia pra brincar com filho sem cansar"

**Se o perfil/idconsumidor não der pistas suficientes**, use 2 exemplos neutros relacionados ao nicho do produto.

Exiba SOMENTE este bloco e pare:

```
Qual o desejo concreto do seu público?

Quanto mais específico, melhor.

(ex: {exemplo personalizado 1}, {exemplo personalizado 2}, {exemplo personalizado 3})

Digite o desejo em uma frase.
```

AGUARDE A RESPOSTA. Salve como `desejo_publico`. Só então avance para o Passo 2.

---

## Passo 2. Geração dos 6 slides (texto)

### Estrutura

- **Slides 1-5**. Cada slide apresenta UM erro. Título começa com `Erro #N:` seguido do erro descrito como ação que a pessoa faz achando que está certa.
- **Slide 6**. CTA criativa que promete eliminar os erros e atingir o desejo.

### Critério das ideias. REGRA CENTRAL

**CONTRAINTUITIVO + PRÁTICO + FUNCIONAL + SABOTADOR DO DESEJO.**

- **Contraintuitivo**. Vai contra o que a pessoa que quer [DESEJO] acredita.
- **Prático**. Erro real, específico, com exemplo concreto.
- **Funcional**. A pessoa entende o que fazer diferente.
- **Sabotador**. Cada erro precisa atrasar ou impedir [DESEJO] especificamente.

### Exemplos de referência

**Certos (desejo: emagrecer 10 kg):**
- "Erro #1: Cortar carboidrato achando que emagrece mais rápido" / "Você perde músculo, não gordura, e o metabolismo trava em 3 semanas."
- "Erro #2: Pesar todo dia para ver progresso" / "Variação de água entre 1 e 3 kg te faz desistir antes de ver resultado real."

**Errados (genéricos):**
- "Erro #1: Não ter disciplina."
- "Erro #2: Comer demais."

### Regras OBRIGATÓRIAS da CTA (slide 6)

1. **Motivo claro.**
2. **Relação direta** com erros + desejo.
3. **Geração de desejo.**

**Exemplo certo:**
- "Siga @nutrireal e emagreça sem repetir os erros que travam 90% das pessoas."

### Tamanho do texto

- **Título** até 10 palavras (incluindo `Erro #N:`).
- **Subtítulo** até 15 palavras.

---

## Passo 3 e Passo 4

Use o output triplo e a legenda compartilhados. Pasta de saída:

```
meus-produtos/{ativo}/entregas/conteudo-social/carrossel-erros/
```

---

## Paleta default

Mesma do "Nunca":
- **Slides 1-5.** `#F2EAD9` (fundo) + `#3D4A3F` (texto).
- **Slide 6.** `#3D4A3F` (fundo) + `#F2EAD9` (texto).

---

## Atmosfera fotográfica

Cenas que **sugerem sutilmente o erro/comportamento sabotador** descrito em cada slide:
- Balança, frasco com restrição, gesto repetido que indica obsessão, refeição desbalanceada
- Luz naturalista cinematográfica
- Sem rosto humano nítido

---

## Ajuste no template de prompt de imagem

No campo `TITLE` do template, mencione que o prefixo `Erro #N:` pode ter destaque visual:

```
The "Erro #N:" prefix can be visually emphasized (different color or weight) if it serves the design, while the rest of the title keeps the main color.
```

E adicione no bloco `CRITICAL TEXT RENDERING RULES`:

```
The "#" symbol and the slide number must be rendered correctly. Do not substitute or remove them.
```

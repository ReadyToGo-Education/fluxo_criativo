# Estilo. Carrossel "Eu odeio"

> Carrossel polêmico que defende pautas e causas no nicho via take forte e justificado. Identificação tribal por oposição.

---

## Coleta extra do Passo 1

**Substituição na pergunta 1.4 (tom).** Para o "Odeio", trocar a lista padrão de tons por:

```
Qual tom de polêmica você quer?

1. Polêmica clássica/sóbria (argumento direto e elegante)
2. Polêmica bem-humorada (trocadilho, ironia)
3. Polêmica técnica (defende com dado)
4. Polêmica provocativa direta (sem rodeio)
5. Polêmica inspiracional (manifesto)

Default: polêmica direta com argumento.

Digite o número.
```

---

## Passo 2. Geração dos 6 slides (texto)

### Estrutura

- **Slides 1-5**. Começam com "Eu odeio quem [comportamento, crença ou atitude]" + justificativa que sustenta o take.
- **Slide 6**. CTA polêmica (convocação tribal).

### Critério das ideias. REGRA CENTRAL

**POLÊMICO + DEFENDIDO + TRIBAL.**

- **Polêmico**. Take forte, posição clara, divide águas.
- **Defendido**. Argumento concreto (dado, lógica, consequência, exemplo). Não é raiva gratuita.
- **Tribal**. Faz a audiência sentir "exatamente, eu tambem odeio isso". Cria pertencimento.

### Cuidados com a polêmica

**Atacar comportamentos, crenças e atitudes. NUNCA pessoas, grupos protegidos ou identidades.** A polêmica é sobre o que se faz, não sobre quem se é.

### Exemplos de referência

**Certos:**
- "Eu odeio quem diz que energia não existe" / "Física quântica já provou: tudo é vibração. Negar é preguiça intelectual."
- "Eu odeio quem terceiriza problemas e cobra resultado" / "Quem não enfrenta a raiz não merece colher o fruto."

**Errados (genéricos):**
- "Eu odeio gente preguiçosa."
- "Eu odeio quem não acredita."

### Regras OBRIGATÓRIAS da CTA (slide 6)

1. **Motivo claro.**
2. **Relação** com a pauta defendida.
3. **Geração de desejo** (identidade tribal).

**Exemplos:**
- "Siga @x e faça parte de quem leva [pauta] a sério."
- "Siga @x se você também não engole [comportamento odiado]."

### Tamanho do texto

- **Título** até 12 palavras (mais espaço porque o take precisa caber).
- **Subtítulo** até 15 palavras.

---

## Passo 3 e Passo 4

Use o output triplo e a legenda compartilhados. Pasta de saída:

```
meus-produtos/{ativo}/entregas/conteudo-social/carrossel-odeio/
```

---

## Paleta default (contraste forte)

- **Slides 1-5.** Fundo preto `#111111` + texto creme `#F2EAD9`.
- **Slide 6 (CTA).** Fundo creme `#F2EAD9` + texto preto `#111111`.

Inversão proposital pra fechar com força.

---

## Atmosfera fotográfica

Cenas que **ilustram o comportamento criticado** ou que carregam **gravidade visual**:
- Situação reconhecível que ilustra o take (ex: para "Eu odeio quem terceiriza problemas" → mãos apontando algo, papel rasgado, copo vazio sob luz dura)
- Gesto simbólico, sombra, contraste forte
- Luz cinematográfica dramática (não naturalista solar)
- Sem rosto humano nítido
- Mood que sustenta o tom polêmico

---

## Ajuste no template de prompt de imagem

No template (`template-prompt-imagem.md`), troque:

```
Cinematic naturalistic lighting
```

por:

```
Cinematic dramatic lighting, mood that supports a polemic statement
```

E aumente o tamanho do título no bloco inferior:

```
occupying ~30-38% of the bottom block height (heavier presence for polemic tone)
```

(Em vez de `~28-35%`.)

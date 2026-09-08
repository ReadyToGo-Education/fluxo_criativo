---
name: "source-command-copy-roteiro"
description: "Criar roteiros de vídeo para os 3 formatos principais. Avatar IA (HeyGen), Reels 60 segundos e VVV (vídeo de vendas completo). Salva em meus-produtos/{ativo}/entregas/criativos/."
---

# source-command-copy-roteiro

Use this skill when the user asks to run the migrated source command `copy-roteiro`.

## Command Template

# Roteiro de Vídeo

Cria roteiros nos 3 formatos principais do marketing VTSD, seguindo Light Copy.

## O Que Fazer

### 1. Contexto

Leia `meus-produtos/.ativo`, depois `meus-produtos/{ativo}/perfil.md` e `meus-produtos/{ativo}/idconsumidor.md` se existir.

Extraia internamente: Quadro, Furadeira, Urgências Ocultas, tom do público.

### 2. Entrevista (UMA pergunta por vez)

**Bloco 1/3 — Formato:**

```
Qual formato de vídeo?

1. Avatar IA (roteiro para HeyGen, até 90s)
2. Reels 60 segundos (Instagram/TikTok)
3. VVV completo (vídeo de vendas, 12-20 min)

Digite o número:
```

**Bloco 2/3 — Objetivo:**

```
Qual o objetivo?

1. Vender produto
2. Educar e gerar valor
3. Captar leads
4. Engajar audiência

Digite o número:
```

**Bloco 3/3 — Plataforma:**

```
Onde será publicado?

1. Instagram
2. TikTok
3. YouTube
4. Página de vendas
5. Anúncio pago (Meta Ads)

Digite o número:
```

**Confirmação:**

```
Resumo do que vou criar:
- Formato: [formato]
- Objetivo: [objetivo]
- Plataforma: [plataforma]

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### 3. Geração por Formato

#### Avatar IA (HeyGen)

- Script até 90 segundos
- Frases curtas, máximo 15 palavras
- Indicações de expressão entre colchetes: [sorriso], [pausa], [ênfase]
- Sem travessão, sem reticências múltiplas
- Linguagem natural, tom de conversa
- Produto não aparece nos primeiros 20 segundos

#### Reels 60 segundos

```
[0-3s]   GANCHO    — Afirmação contra-intuitiva ou revelação. NUNCA pergunta.
[4-15s]  TEASE     — Expande o gancho, contextualiza o problema.
[16-42s] ENTREGA   — Ensina ou revela algo real e concreto.
[43-48s] REGANCHO  — Texto síntese da ideia central (âncora para quem assiste sem som).
[49-55s] CTA       — Convite direto e leve.
```

#### VVV Completo (8 blocos)

1. Abertura: gancho sem pergunta, premissa forte
2. Conexão: história que gera identificação
3. Problema: dor amplificada com Urgências Ocultas
4. Paliativo: por que as soluções atuais do mercado resolvem parcialmente
5. Solução: apresentação da Furadeira
6. Prova: resultados e depoimentos
7. Oferta: entregáveis, bônus, garantia, preço
8. CTA: chamada direta

### 4. Regras de Estilo

Antes de escrever, leia `.Codex/skills/revisora/references/manual-copy.md` e aplique.

- Gancho nos primeiros 3 segundos: afirmação, paradoxo ou revelação. NUNCA pergunta.
- Entregar valor real dentro do vídeo: quem assiste aprende ou se reconhece.
- Produto não aparece nos primeiros blocos.
- Argumento antes de oferta.
- Sem travessão em nenhuma frase.

Toda peça passa pela skill `revisora` antes de ir ao usuário.

### 5. Aprovação e Salvar

Mostrar o roteiro gerado e perguntar:

```
1. Aprovar e salvar
2. Quero ajustar algo
```

Após aprovação, salvar em:
`meus-produtos/{ativo}/entregas/criativos/roteiro-[formato]-[produto].md`

### 6. Próximo Passo

- Avatar: "Use `/video-heygen` para gerar o vídeo automaticamente com o avatar."
- Reels: "Grave seguindo o roteiro. Use `/criativo` para criar os criativos estáticos da campanha."
- VVV: "Use `/criativo` para criar os anúncios que vão direcionar para este vídeo."

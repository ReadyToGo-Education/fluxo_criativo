# Referência. Prompts parametrizados das tarefas programadas

> Prompts-base que a skill `/programar-carrossel` injeta na tarefa programada do `/schedule`. A skill substitui os placeholders `{{...}}` pelos valores coletados antes de enviar pro `/schedule create`.
> 
> **ARQUIVO LEGADO.** Após a migração dos 6 estilos clássicos para o modelo verbatim, NENHUM estilo do menu atual usa este arquivo. Cada estilo tem o próprio prompt-base autônomo:
>
> - Nunca → `prompt-nunca-routine.md`
> - Sempre → `prompt-sempre-routine.md`
> - Odeio → `prompt-odeio-routine.md`
> - Erros → `prompt-erros-routine.md`
> - Amo → `prompt-amo-routine.md`
> - Ninguém Conta → `prompt-ninguem-conta-routine.md`
> - Notícia → `programar-carrossel-noticia/references/prompt-carrossel-noticia.md`
> - Curiosidade → `prompt-curiosidade-routine.md`
> - Editorial → `prompt-editorial-routine.md`
>
> Este arquivo é mantido apenas como referência histórica do modelo leve (Bloco A/B/C/D) que existia antes da migração. Se um estilo futuro precisar do padrão Bloco A/B/C/D, ele pode reutilizá-lo.

---

## Placeholders globais

| Placeholder | Origem | Exemplo |
|---|---|---|
| `{{HANDLE}}` | Coleta | `@leandroladeiran` |
| `{{NICHO_PRODUTO}}` | Coleta | `surf, mentoria online de 8 semanas para surfistas intermediarios` |
| `{{ESTILO}}` | Passo 1 da skill | `Nunca`, `Sempre`, `Odeio`, `Erros`, `Amo`, `Ninguem Conta` |
| `{{DESEJO}}` | Coleta (se Erros) | `emagrecer 10kg` |
| `{{OBJETIVO}}` | Coleta (se Ninguem Conta) | `ganhar primeiro R$10 mil por mes` |
| `{{TEMAS_FIXOS}}` | Coleta (se modo FIXO) | lista dos 5 títulos |
| `{{DATA_HOJE_REF}}` | Calculado em runtime | `[calcule a data de hoje no inicio da execucao]` |

---

## Bloco A. Cabeçalho fixo

Entra sempre, independente do estilo.

```
Voce e especialista em carrosseis virais para Instagram, treinado em
narrativa argumentativa (Light Copy do Workshop Marketing IA) e
psicologia do feed (gancho, retencao, tribalismo).

Sua missao agora e gerar 1 carrossel de 6 slides no estilo "{{ESTILO}}"
para o nicho do criador, prontos pra postar.

Contexto fixo do criador (ja validado, nao pergunte de novo):
- Instagram: {{HANDLE}}
- Nicho e produto: {{NICHO_PRODUTO}}

A data de hoje e {{DATA_HOJE_REF}}.
```

---

## Bloco B-NUNCA

```
ESTILO: Nunca

Estrutura dos slides:
- Slides 1-5 comecam com "Nunca [acao]..." + justificativa em ate 15
  palavras. Cada slide entrega UMA proibicao contraintuitiva.
- Slide 6 e CTA criativa com verbo de fechamento DIFERENTE de "Nunca"
  (use "Siga", "Comece", "Salve", "Para de" etc.).

Criterio central (toda ideia precisa cumprir):
1. CONTRAINTUITIVO. Proibe algo que a maioria do nicho faz achando que e certo.
2. PRATICO. Proibicao real, especifica, com exemplo concreto do dano.
3. FUNCIONAL. A pessoa entende imediatamente o que parar de fazer.

CTA do slide 6:
- Motivo claro pra seguir o @{{HANDLE}}.
- Relacao direta com os 5 slides.
- Geracao de desejo (promete acesso continuado a esse tipo de
  proibicao reveladora).

Tamanho por slide: titulo ate 8 palavras + subtitulo ate 15 palavras.
```

---

## Bloco B-SEMPRE

```
ESTILO: Sempre

Estrutura dos slides:
- Slides 1-5 comecam com "Sempre [acao]..." + justificativa em ate 15
  palavras. Cada slide entrega UMA acao contraintuitiva que deveria
  ser feita.
- Slide 6 e CTA com verbo de fechamento DIFERENTE de "Sempre" (use
  "Siga", "Comece", "Salve", "Comeca", "Adota" etc.).

Criterio central:
1. CONTRAINTUITIVO. Vai contra o que a maioria do nicho faz.
2. PRATICO. Acao real, especifica, com exemplo concreto.
3. FUNCIONAL. Passo aplicavel ja no proximo dia.

CTA do slide 6: mesmas regras do Nunca, mas em tom afirmativo.

Tamanho: titulo ate 8 palavras + subtitulo ate 15 palavras.
```

---

## Bloco B-ODEIO

```
ESTILO: Eu odeio

Estrutura dos slides:
- Slides 1-5 comecam com "Eu odeio quem [comportamento, crenca ou
  atitude]" + justificativa que sustenta o take.
- Slide 6 e CTA polemica (convocacao tribal).

Criterio central:
1. POLEMICO. Take forte, posicao clara, divide aguas.
2. DEFENDIDO. Argumento concreto (dado, logica, consequencia, exemplo).
   Nao e raiva gratuita.
3. TRIBAL. Faz a audiencia sentir "exatamente, eu tambem odeio isso".
   Cria pertencimento.

Cuidados:
- Atacar comportamentos, crencas e atitudes. NUNCA pessoas, grupos
  protegidos ou identidades.

CTA do slide 6:
- "Siga @{{HANDLE}} e faca parte de quem leva [pauta] a serio" ou
  similar.
- Geracao de desejo via identidade tribal.

Tamanho: titulo ate 12 palavras + subtitulo ate 15 palavras.
```

---

## Bloco B-ERROS

```
ESTILO: Erros comuns para quem quer {{DESEJO}}

Estrutura dos slides:
- Slides 1-5: cada slide apresenta UM erro. Titulo comeca com
  "Erro #N:" seguido do erro descrito como acao que a pessoa faz
  achando que esta certa.
- Slide 6 e CTA que promete eliminar os erros e atingir o desejo.

Criterio central:
1. CONTRAINTUITIVO. Vai contra o que a pessoa que quer {{DESEJO}} acredita.
2. PRATICO. Erro real, especifico, com exemplo concreto.
3. FUNCIONAL. A pessoa entende o que fazer diferente.
4. SABOTADOR. Cada erro precisa atrasar ou impedir {{DESEJO}}.

CTA: "Siga @{{HANDLE}} e {atinja DESEJO} sem repetir os erros que travam
90% das pessoas".

Tamanho: titulo ate 10 palavras (incluindo "Erro #N:") + subtitulo
ate 15 palavras.
```

---

## Bloco B-AMO

```
ESTILO: Eu amo

Estrutura dos slides:
- Slides 1-5 comecam com "Eu amo quem [comportamento, atitude ou
  postura]" + justificativa que celebra com peso.
- Slide 6 e CTA tribal positiva.

Criterio central:
1. AFIRMATIVO. Take positivo forte, declaracao de admiracao com peso.
2. DEFENDIDO. Argumento concreto. Nao e elogio generico.
3. TRIBAL. Faz a audiencia sentir "exatamente, e assim que eu sou".

CTA:
- "Siga @{{HANDLE}} se voce e (ou quer ser) desse time" ou similar.
- Geracao de desejo via pertencimento.

Tamanho: titulo ate 12 palavras + subtitulo ate 15 palavras.
```

---

## Bloco B-NINGUEM-CONTA

```
ESTILO: O que ninguem te conta sobre {{OBJETIVO}}

Estrutura dos slides:
- Slides 1-5 comecam com "Ninguem te conta que [verdade oculta]" +
  explicacao. Variacao do slide 1: "O que ninguem te conta sobre
  {{OBJETIVO}}:" + verdade.
- Slide 6 e CTA de acesso continuado a verdade sem filtro.

Criterio central:
1. REVELADOR. Mostra algo que o mercado/profissionais NAO falam em
   publico.
2. DEFENDIDO. Argumento concreto, insider knowledge sustentado.
3. UTIL. Conexao direta com {{OBJETIVO}}. Saber disso muda a estrategia.

Categorias pra gerar ideias:
- Fase desconfortavel
- Custo invisivel
- Mecanica real
- Ponto de desistencia
- O que muda em voce
- Tempo real

CTA:
- "Siga @{{HANDLE}} e tenha a verdade que ninguem mais te diz sobre
  {{OBJETIVO}}" ou similar.

Tamanho: titulo ate 12 palavras + subtitulo ate 15 palavras.
```

---

## Bloco C-ALEATORIO

```
MODO DE GERACAO: aleatorio.

A cada execucao desta tarefa, escolha um angulo NOVO dentro do estilo
"{{ESTILO}}", evitando repetir temas das execucoes anteriores. Use a
pesquisa do nicho e o conhecimento publico do mercado de "{{NICHO_PRODUTO}}"
pra encontrar ideias frescas que cumprem o criterio central do estilo.

Antes de comecar, faca uma busca rapida na web por:
- "{{NICHO_PRODUTO}} erros comuns"
- "{{NICHO_PRODUTO}} contraintuitivo"
- "{{NICHO_PRODUTO}} verdades que ninguem fala"

Use isso pra ancorar o carrossel em algo real do mercado, nao em
generalidades.
```

---

## Bloco C-FIXO

```
MODO DE GERACAO: fixo.

Os 5 titulos dos slides 1-5 estao travados nos seguintes temas:

1. {{TEMA_SLIDE_1}}
2. {{TEMA_SLIDE_2}}
3. {{TEMA_SLIDE_3}}
4. {{TEMA_SLIDE_4}}
5. {{TEMA_SLIDE_5}}

A cada execucao, gere os 6 slides com EXATAMENTE esses titulos
(slide 6 e a CTA padrao do estilo). Pode variar o subtitulo (a
justificativa) entre execucoes, buscando angulos novos pra cada tema.
```

---

## Bloco D. Output

```
PROIBICOES ABSOLUTAS DE COPY (todos os slides + legenda):
- Sem travessao.
- Sem ponto de exclamacao.
- Sem pergunta na capa.
- Sem "nao e X, e Y".
- Sem "mesmo que" ou "sem precisar" como muleta.
- Sem promessa vazia. Toda afirmacao tem dado, prazo ou cena concreta.
- Sem mencionar o produto na narrativa.
- Sem lero-lero. Palavra generica que sobrevive trocada por outra
  palavra do nicho nao pode existir.
- Portugues brasileiro com acentuacao correta segundo o Acordo
  Ortografico de 1990.

OUTPUT ESPERADO desta tarefa programada:

1. Texto dos 6 slides no chat, formato:

SLIDE 1
Titulo: [...]
Subtitulo: [...]

SLIDE 2
Titulo: [...]
Subtitulo: [...]

(... ate slide 6 ...)

2. Os 6 prompts visuais em INGLES, um por slide, separados por linha
   em branco. Cada prompt segue o template 4:5 com dois blocos
   horizontais (foto cinematografica em cima, cor solida embaixo com
   texto renderizado). Indicador N/6, margens de 80px, paleta consistente.

3. Legenda do Instagram com 600 a 1200 caracteres, seguindo as
   proibicoes acima. Estrutura: gancho concreto, 3 a 5 paragrafos
   curtos de desenvolvimento, pico de tensao, virada, CTA unico
   ("Comenta CARROSSEL", "Salva o post", "Me segue para a parte 2",
   ou equivalente), 5 a 8 hashtags em uma linha unica no final.

Encerre com a mensagem:

> Carrossel "{{ESTILO}}" gerado para {{NICHO_PRODUTO}}.
> Texto + 6 prompts visuais + legenda no chat acima.
> Para postar no Instagram, cole os 6 prompts no ChatGPT (em ordem)
> e monte o carrossel manualmente.
```

---

## Como a skill monta o prompt final

A skill `/programar-carrossel` concatena, antes de chamar `/schedule create`:

1. **Sempre:** Bloco A
2. **Por estilo:** Bloco B-{ESTILO}
3. **Por modo:** Bloco C-ALEATORIO ou Bloco C-FIXO
4. **Sempre:** Bloco D

E substitui todos os `{{...}}` pelos valores coletados na entrevista.

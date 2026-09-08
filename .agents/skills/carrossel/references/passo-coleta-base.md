# Passo de Coleta Base (compartilhado)

> Sequência de 5 perguntas comuns a TODOS os estilos de carrossel. Cada estilo pode adicionar 1 pergunta extra (ex: Erros pede Desejo, Ninguém Conta pede Objetivo). Essas extras estão definidas em `estilos/{nome}.md`.

---

## Regra dura. Uma pergunta por turno

**Cada Passo é UMA pergunta separada que precisa de resposta do aluno antes do próximo Passo.** Esta regra anula qualquer orientação geral de "reduzir confirmações" do projeto.

PROIBIDO:
- Bulkar 2 ou mais perguntas no mesmo turno.
- Assumir default sem perguntar (mesmo que o perfil tenha sugestão).
- Pular direto pra geração antes de coletar TODAS as respostas.

OBRIGATÓRIO:
- Exibir UMA pergunta, parar a execução, aguardar resposta, salvar a variável, só então exibir a próxima.
- Após cada resposta, exibir um **micro-resumo de progresso** antes da próxima pergunta (formato no fim deste arquivo).
- Se o aluno responder com algo ambíguo, perguntar de novo a mesma pergunta, não avançar.

---

## Regra dura. Vocabulário com o aluno

**NUNCA use a palavra "handle" ao falar com o aluno.** Handle é jargão técnico de programação e o aluno final do workshop não entende.

Use em vez disso:
- "@" ou "@ do Instagram"
- "seu perfil"
- "usuário do Instagram"

PROIBIDO em qualquer mensagem visível ao aluno (anúncios, perguntas, micro-resumos, confirmações, entregas):
- "Encontrei o handle no .env" ❌
- "Vou usar esse handle como sugestão" ❌
- "Handle do Instagram:" como label ❌

PERMITIDO em qualquer mensagem visível ao aluno:
- "Achei seu @ no .env" ✅
- "Vou usar esse @ como sugestão" ✅
- "@ do Instagram:" como label ✅

Internamente (em código, variáveis, comentários de implementação na SKILL.md, esquemas JSON), pode continuar usando `handle` como nome de variável. Só não fale a palavra com o aluno.

---

## Passo 0. Contexto antes das perguntas

Leia em paralelo:
- `meus-produtos/.ativo` para descobrir o produto ativo.
- `meus-produtos/{ativo}/perfil.md` se existir.
- `meus-produtos/{ativo}/idconsumidor.md` se existir.
- **`.env` na raiz do projeto** para procurar `IG_USER=` (handle do Instagram salvo por outras skills como `dashboard-social`, `instagram-dashboard`, `dados-instagram`).

Do perfil, tente extrair como sugestão (não use ainda):
- **Handle do Instagram**. **Ordem de prioridade:** primeiro `IG_USER` do `.env`, depois `@`/"Instagram"/"perfil" do `perfil.md`. Quando vier do `.env`, lembre que está sem `@` (ex: `leandroladeiran`) e adicione o `@` na exibição.
- **Nicho**. Procure por "Nicho:", "Mercado:" ou identidade do produto.
- **Produto**. Combine nome + formato + público-alvo.

Se não houver produto ativo, instrua o aluno a rodar `/produto-novo` primeiro e encerre.

---

## Quantidade de perguntas por estilo

Use a tabela para preencher o cabeçalho "Pergunta X de Y" em cada pergunta exibida:

| Estilo | Total de perguntas | Perguntas extras (sobre a base de 5) |
|---|---|---|
| Nunca, Sempre, Amo, Odeio | 5 | nenhuma |
| Erros | 6 | 1.6 Desejo do público |
| Ninguém Conta | 6 | 1.6 Objetivo do público |
| Notícia | 5 (fluxo próprio) | substitui a base inteira (ver `estilos/noticia.md`) |

---

## 1.1. @ do Instagram

### Ordem de tentativa de sugestão

1. **`.env` na raiz do projeto** com a chave `IG_USER=`. Esta é a fonte preferida (salva por `dashboard-social`, `instagram-dashboard`, `dados-instagram` e outras skills). Normalize lendo sem `@` e prefixe na exibição.
2. **`perfil.md`** do produto ativo (procure `@`, "Instagram", "perfil").
3. **Nenhuma**: pergunte sem sugestão.

### Com sugestão (vinda do .env ou perfil)

```
Pergunta 1 de {total}. @ do Instagram

Sugestão: @{ig_user_sugerido}
{Se veio do .env} (achei no seu .env, salvo por outra skill do projeto)
{Se veio do perfil.md} (achei no seu perfil.md)

1. Sim, é esse mesmo
2. Outro @

Digite o número ou cole o @.
```

### Sem sugestão (nem .env nem perfil)

```
Pergunta 1 de {total}. @ do Instagram

Qual o @ do seu Instagram?

(ex: @leandroladeiran)

Digite o @.
```

AGUARDE A RESPOSTA. Quando o aluno responder:

- **Normalize o handle**: remova o `@` se vier, lowercase, sem espaços. Salve como `handle` (com `@` na frente quando exibir, sem `@` quando salvar no `.env`).
- **Se veio um @ novo (opção 2 OU resposta livre quando sem sugestão)**: salve no `.env` como `IG_USER={handle_sem_arroba}` para que outras skills reutilizem. Se a chave já existir, sobrescreva.
- **Se o aluno confirmou a sugestão (opção 1)**: não escreve no `.env` (já está lá).

Mostre o micro-resumo (formato abaixo) e prossiga para a 1.2.

---

## 1.2. Nicho e produto em uma frase

### Regra de exemplo personalizado

**O exemplo entre parênteses NÃO deve ser hardcoded.** Antes de exibir a pergunta, gere um exemplo coerente com o produto ativo, lendo `perfil.md` (Quadro, nicho, formato) e `idconsumidor.md` (público-alvo). Estrutura do exemplo:

```
{nicho do produto}, {formato do produto} de {duração} para {recorte do público-alvo}
```

Por exemplo:
- Produto "Curso de Tarô para Iniciantes" → exemplo: "tarô, curso online de 4 semanas para pessoas que querem ler as próprias cartas"
- Produto "Mentoria Fitness Pós-Parto" → exemplo: "fitness pós-parto, mentoria online de 12 semanas para mães que querem voltar a treinar sem culpa"
- Produto "Workshop de Investimentos para Médicos" → exemplo: "investimentos para médicos, workshop online de 2 semanas para médicos que ganham bem mas não sabem investir"

**Se não conseguir gerar exemplo coerente** (perfil muito vago, sem dados suficientes), use um exemplo neutro: "{nicho do produto ativo, sem outros detalhes}, formato online para {público-alvo do produto}".

### Sem sugestão (perfil sem nicho/produto identificado)

```
Pergunta 2 de {total}. Nicho e produto

Descreva o seu nicho e produto em UMA frase simples.

(ex: {exemplo personalizado a partir do perfil})

Digite a frase.
```

### Com sugestão (perfil já tem nicho + produto)

```
Pergunta 2 de {total}. Nicho e produto

Sugestão a partir do seu perfil:
{nicho_produto_sugerido}

1. Sim, usar a sugestão
2. Digitar outra

Digite o número ou cole a frase.
```

AGUARDE A RESPOSTA. Salve como `nicho_produto`. Micro-resumo. Prossiga para a 1.3.

---

## 1.3. Cores da marca

```
Pergunta 3 de {total}. Cores da marca

Qual paleta você quer usar nos slides?

1. Paleta default deste carrossel ({cor_principal} + {cor_acento})
2. Tenho a minha paleta (eu digito as cores)

Digite o número.
```

Onde `{cor_principal}` e `{cor_acento}` vêm de `sistema-design.md` conforme o estilo escolhido.

### Se 2 (digitar manualmente)

```
Cole as cores em hex. Pode mandar 2 cores (fundo + texto) ou paleta completa.

(ex: #F2EAD9 e #3D4A3F)

Digite as cores.
```

AGUARDE A RESPOSTA. Salve como `cores_marca` (`DEFAULT` ou valor digitado). Micro-resumo. Prossiga para a 1.4.

---

## 1.4. Tom de comunicação (texto)

```
Pergunta 4 de {total}. Tom da copy

Qual tom você quer no texto dos slides?

1. Clássica/profissional (direta, elegante)
2. Bem-humorada (trocadilhos, ironia)
3. Técnica (dados, mecanismos)
4. Inspiracional (aspiracional)
5. Descontraída/casual (conversa de amigo)
6. Polêmica/provocativa (provocações diretas)

Digite o número.
```

AGUARDE A RESPOSTA. Salve como `tom_texto`. Micro-resumo. Prossiga para a 1.5.

> Observação. Os carrosséis **Odeio**, **Amo** e **Ninguém Conta** trocam ou complementam esta lista por tons próprios (polêmica em 5 sabores, afirmativa apaixonada, crua). Cada arquivo de estilo documenta a substituição.

---

## 1.5. Estilo de design visual

```
Pergunta 5 de {total}. Estilo de design

Qual o estilo de design visual?

1. Sofisticado e elegante
2. Editorial e cinematográfico
3. Despojado e bem-humorado
4. Energético e vibrante
5. Sério e técnico
6. Aconchegante e humano
7. Provocativo e ousado

Você também pode descrever livremente (ex: minimalista escandinavo, anos 70 brasileiro).

Digite o número ou descreva.
```

AGUARDE A RESPOSTA. Salve como `estilo_design`. Micro-resumo. **NUNCA mencione termos técnicos de tipografia ao aluno** (serifada, condensada, leading). Use só os rótulos da lista.

---

## Encerramento da coleta base

Após capturar `handle`, `nicho_produto`, `cores_marca`, `tom_texto` e `estilo_design`:

- Se o estilo de carrossel **NÃO** pede input extra (Nunca, Sempre, Odeio, Amo), vá para a **Confirmação consolidada** (ver SKILL.md do `/carrossel`, Passo 2.5).
- Se o estilo pede input extra (Erros pede Desejo, Ninguém Conta pede Objetivo), execute a pergunta extra documentada no arquivo do estilo ANTES da confirmação consolidada.

---

## Formato do micro-resumo entre perguntas

Após cada resposta, antes de exibir a próxima pergunta, mostre:

```
--- Pergunta {N}/{total} concluída ---
{label}: {valor escolhido}
Próximo: {label da próxima pergunta}
---
```

Exemplo:

```
--- Pergunta 1/5 concluída ---
@ do Instagram: @inglesatleta
Próximo: Nicho e produto
---
```

Esse bloco serve para o aluno entender em qual ponto do fluxo está e revisar o que já respondeu. **Não pular este bloco.**

---

## Atalhos quando o produto ativo já tem todos os dados

Se TODAS as 5 variáveis acima podem ser preenchidas a partir do `perfil.md` (handle, nicho/produto, paleta, tom default coerente, estilo de design fixo da marca), a skill ainda assim DEVE exibir cada pergunta, mas pode pré-preencher com sugestão e oferecer "1. Sim ({valor sugerido})" como atalho. Aluno tem direito de revisar.
